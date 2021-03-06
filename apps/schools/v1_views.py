from django.views.generic import View, FormView, TemplateView
from django.db.models import Count, Min, Sum, Avg, F, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from django.core import serializers
from django.db import connection

from common import SumCase
from common.views import JSONResponseMixin
from schools.models import YearlyData, School, SchoolManaagement,\
DrinkingWaterSource, BoundaryWallType, search_choices, YESNO, MDM_STATUS


DEFAULT_LIMIT = 20


def ptr_filtered_ids(ptr_min, ptr_max, academic_year_id):
    """
    Returns list of school codes that have ptr more than given
    >>> ptr_filtered_ids(0, 35, 0)
    [..., results, ...]
    """
    params = [ptr_min, ptr_max, academic_year_id]
    cursor = connection.cursor()
    cursor.execute("SELECT code FROM view_ptr WHERE ptr >= %s AND ptr <= %s AND academic_year_id = %s", params)
    return [
        row[0] for row in cursor.fetchall()
    ]


class V1SearchView(View, JSONResponseMixin):
    def get(self, *args, **kwargs):
        params = self.request.GET
        results = {}
        schools = School.objects.values('id', 'code', 'name')

        try:
            limit = int(params.get('limit', DEFAULT_LIMIT))
        except ValueError:
            limit = DEFAULT_LIMIT

        filters = params.getlist('filters')
        query = {}

        if params.get('year', ''):
            query['yearlydata__academic_year_id'] = params.get('year', '')

        if params.get('area_type', ''):
            query['yearlydata__area_type'] = params.get('area_type', '')

        if params.get('management', ''):
            if params.get('management') == 'govt':
                govt_mgmt = SchoolManaagement.objects.filter(
                    Q(name__iexact='Department of Education') |
                    Q(name__iexact='Central Govt.')
                )
                query['yearlydata__management_id__in'] = govt_mgmt
            elif params.get('management') == 'pvt':
                pvt_mgmt = SchoolManaagement.objects.exclude(
                    Q(name__iexact='Department of Education') |
                    Q(name__iexact='Central Govt.')
                )
                query['yearlydata__management_id__in'] = pvt_mgmt

        if 'no_electricity' in filters:
            query['yearlydata__electricity_status'] = search_choices(YESNO, 'No')

        if 'no_secure_wall' in filters:
            insecure_wall_types = BoundaryWallType.objects.exclude(name__iexact="Pucca")
            query['yearlydata__boundary_wall_type_id__in'] = insecure_wall_types

        if 'no_mdm' in filters:
            query['yearlydata__middaymeal_status__in'] = [
                search_choices(MDM_STATUS, 'Not applicable'),
                search_choices(MDM_STATUS, 'Not provided'),
            ]

        if 'no_library' in filters:
            query['yearlydata__library_available'] = search_choices(YESNO, 'No')

        if 'no_ramp' in filters:
            query['yearlydata__ramp_available'] = search_choices(YESNO, 'No')

        if 'no_blackboard' in filters:
            query['yearlydata__blackboard_count'] = 0

        if 'no_playground' in filters:
            query['yearlydata__playground_available'] = search_choices(YESNO, 'No')

        if 'no_medical' in filters:
            query['yearlydata__medical_checkup'] = search_choices(YESNO, 'No')

        if 'no_room_hm' in filters:
            query['yearlydata__room_for_headmaster'] = search_choices(YESNO, 'No')

        if 'no_hm' in filters:
            query['yearlydata__teachercount__headteacher'] = search_choices(YESNO, 'No')

        if 'no_sdmc_constituted' in filters:
            query['yearlydata__sdmc_constituted'] = search_choices(YESNO, 'No')

        if 'no_sdmc_meeting' in filters:
            query['yearlydata__sdmc_meeting_count'] = 0

        if 'no_textbook' in filters:
            query['yearlydata__textbook_received'] = search_choices(YESNO, 'No')

        if 'weakersec_children_enrolled' in filters:
            query['yearlydata__weakersec_children_enrolled__gt'] = 0

        if 'no_water' in filters:
            try:
                query['yearlydata__drinking_water_source'] = DrinkingWaterSource.objects.get(name__iexact="None")
            except:
                # 5 should be the id of "None" source
                query['yearlydata__drinking_water_source_id'] = 5

        # All the non-aggregation non-annotation queries go above this
        schools = schools.filter(**query)

        if 'no_toilet' in filters:
            schools = schools.annotate(total_toilets=Sum('yearlydata__toilet__count'))
            schools = schools.filter(total_toilets=0)

        if 'girl_boy_ratio' in filters:
            schools = schools.annotate(
                total_girls=Sum('yearlydata__enrolment__total_girls'),
                total_boys=Sum('yearlydata__enrolment__total_boys'),
            )
            schools = schools.filter(total_girls__lt=F('total_boys'))

        if 'enrolment' in filters:
            enrolment_min = params.get('enrolment_min') if params.get('enrolment_min') else 0
            enrolment_max = params.get('enrolment_max') if params.get('enrolment_max') else 25
            schools = schools.annotate(
                total_students=Sum('yearlydata__enrolment__total'),
            ).filter(
                total_students__gt=enrolment_min,
                total_students__lt=enrolment_max
            )

        if 'ptr' in filters:
            ptr_min = params.get('ptr_min') if params.get('ptr_min') else 0
            ptr_max = params.get('ptr_max') if params.get('ptr_max') else 35
            ptr_filtered_id_list = ptr_filtered_ids(ptr_min, ptr_max, params.get('year'))
            schools = schools.filter(
                code__in=ptr_filtered_id_list
            )

        if 'no_girls_toilet' in filters:
            schools = schools.annotate(
                girl_toilet_count=SumCase(
                    'yearlydata__toilet__count',
                    when='"schools_toilet"."type" = \'girl\''
                )
            )
            schools = schools.filter(girl_toilet_count=0)

        if 'needs_repair' in filters:
            schools = schools.annotate(
                repair_count=SumCase(
                    'yearlydata__room__count',
                    when='"schools_room"."type" = \'class\' AND "schools_room"."condition" <> \'good\''
                )
            )
            schools = schools.filter(repair_count__gt=0).order_by('-repair_count')

        if 'classroom_count' in filters:
            classroom_min = params.get('classroom_min') if params.get('classroom_min') else 0
            classroom_max = params.get('classroom_max') if params.get('classroom_max') else 50
            schools = schools.annotate(
                classroom_count=SumCase(
                    'yearlydata__room__count',
                    when='"schools_room"."type" = \'class\''
                )
            )
            schools = schools.filter(
                classroom_count__gte=classroom_min,
                classroom_count__lte=classroom_max
            )

        if 'teacher_count' in filters:
            teacher_min = params.get('teacher_min') if params.get('teacher_min') else 0
            teacher_max = params.get('teacher_max') if params.get('teacher_max') else 50
            schools = schools.filter(
                yearlydata__teachercount__total__gte=teacher_min,
                yearlydata__teachercount__total__lte=teacher_max
            )

        if 'ngirls' in filters:
            ngirls_class = int(params.get('ngirls_class')) if params.get('ngirls_class') else 1
            ngirls_min = params.get('ngirls_min') if params.get('ngirls_min') else 50
            ngirls_max = params.get('ngirls_max') if params.get('ngirls_max') else 50
            schools = schools.annotate(
                girls=SumCase(
                    'yearlydata__enrolment__total_girls',
                    # sql injection prone, change
                    when='"schools_enrolment"."klass" = %s' % ngirls_class
                )
            ).filter(
                girls__range=(ngirls_min, ngirls_max)
            )

        if 'nboys' in filters:
            nboys_class = int(params.get('nboys_class')) if params.get('nboys_class') else 1
            nboys_min = params.get('nboys_min') if params.get('nboys_min') else 50
            nboys_max = params.get('nboys_max') if params.get('nboys_max') else 50
            schools = schools.annotate(
                boys=SumCase(
                    'yearlydata__enrolment__total_boys',
                    # sql injection prone, change
                    when='"schools_enrolment"."klass" = %s' % nboys_class
                )
            ).filter(
                boys__range=(nboys_min, nboys_max)
            )

        schools = schools[:limit]
        print schools.query
        # schools_json = serializers.serialize("json", schools)
        results = {
            'results': list(schools)
        }
        return self.render_to_response(results)
