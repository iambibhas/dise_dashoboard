import os
import xlrd
from optparse import make_option


from django.core.management.base import BaseCommand, CommandError
from common.models import Cluster, Block, EducationDistrict, Village, State
from django.conf import settings

from common.models import Cluster, Block, Village, State, EducationDistrict
from schools.models import School, AcademicYear, YearlyData


class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports Basic data files'
    option_list = BaseCommand.option_list + (
        make_option('--year',
            dest="year",
            help='import for specific academic year'
        ),
    )

    INDEXES = {
        'district': 0,
        'District_Name': 0,

        'school_code': 1,
        'School_Code': 1,

        'school_name': 2,
        'School_Name': 2,

        'block': 3,
        'Block_Name': 3,

        'cluster': 4,
        'Cluster_Name': 4,

        'village': 5,
        'Village_Name': 5,

        'pincode': 6,
        'Pincode': 6
    }

    def process_row(self, row, year=None):
        district, created = EducationDistrict.objects.get_or_create(
            name=row[self.INDEXES['District_Name']]
        )
        village, created = Village.objects.get_or_create(
            name=row[self.INDEXES['Village_Name']]
        )
        block, created = Block.objects.get_or_create(
            name=row[self.INDEXES['Block_Name']],
        )
        block.education_district = district
        block.save()

        cluster, created = Cluster.objects.get_or_create(
            name=row[self.INDEXES['Cluster_Name']],
            block=block
        )
        school, created = School.objects.get_or_create(
            code=unicode(int(row[self.INDEXES['School_Code']])),
        )
        school.name = unicode(row[self.INDEXES['School_Name']])
        school.pincode= int(row[self.INDEXES['Pincode']])
        school.save()

        yearly_data, created = YearlyData.objects.get_or_create(
            school=school,
            academic_year=year
        )
        yearly_data.cluster = cluster
        yearly_data.village = village
        yearly_data.save()

    def handle(self, *args, **options):
        year = None

        if 'year' in options:
            from_year, to_year = options.get('year').split('-')
            year = AcademicYear.objects.get(from_year=from_year, to_year=to_year)

        for basic_data in args:
            full_path = os.path.join(settings.DATADUMP_ROOT, basic_data)
            try:
                fp = xlrd.open_workbook(full_path)
                for sheet in fp.sheets():
                    print "Sheet: ", sheet
                    print "#"*20
                    for idx in range(1, sheet.nrows):
                        row = sheet.row_values(idx)
                        if not row[self.INDEXES['School_Code']]:
                            continue
                        self.process_row(row, year)

                        if idx % 100 == 0:
                            print "%s/%s: %s%% done." % (idx, sheet.nrows, (idx/float(sheet.nrows))*100)

            except Exception as e:
                print str(e)
