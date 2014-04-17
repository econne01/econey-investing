import requests
import sqlite3

from settings import common

class BLSDataFetcher(object):
    ''' For more info:
        http://www.bls.gov/help/hlpforma.htm#CE
    '''
    db_table = 'macro_jobs'
    base_url = 'http://api.bls.gov/publicAPI/v1/timeseries/data/'

    series_codes = {
        'jobs': 'CE',
    }

    adjustment_codes = {
        'adjusted': 'S',
        'unadjusted': 'U',
    }

    supersector_codes = {
        'total_nonfarm': '00',
        'private': '08',
    }

    industry_codes = {
        'total': '000000',
    }

    datatype_codes = {
        'all_employees': '01',
        'avg_weekly_hours': '02',
        'avg_hourly_earnings': '03',
        'diffusion_idx_1mo_sa': '21',
    }

    def import_data(self, data, options):
        ''' Insert/Update data into local database
        '''
        conn = sqlite3.connect(common.DATABASE)
        c = conn.cursor()

        for row in data:
            c.execute('UPDATE ' + self.db_table + '''
                SET value=?,
                    series_prefix=?,
                    adjusted=?,
                    supersector=?,
                    industry=?,
                    datatype=?
                WHERE year=? and month=? and series_key=?''',
                (
                    row['value'],
                    self.series_codes[options['series']],
                    self.adjustment_codes[options['adjustment']],
                    self.supersector_codes[options['supersector']],
                    self.industry_codes[options['industry']],
                    self.datatype_codes[options['datatype']],
                    row['year'],
                    row['period'][-2:], # has format 'M02'
                    self.get_series_key(options)
                )
            )
            if c.rowcount == 0:
                c.execute('INSERT into ' + self.db_table + '''
                    (
                          year, month, series_key,
                          series_prefix, adjusted, supersector,
                          industry, datatype, value
                    )
                    values (?,?,?,?,?,?,?,?,?)''',
                    (
                        row['year'],
                        row['period'][-2:], # has format 'M02'
                        self.get_series_key(options),
                        self.series_codes[options['series']],
                        self.adjustment_codes[options['adjustment']],
                        self.supersector_codes[options['supersector']],
                        self.industry_codes[options['industry']],
                        self.datatype_codes[options['datatype']],
                        row['value'],
                    )
                )

        conn.commit()
        conn.close()

    def get_series_key(self, options):
        return ''.join([
            self.series_codes[options['series']],
            self.adjustment_codes[options['adjustment']],
            self.supersector_codes[options['supersector']],
            self.industry_codes[options['industry']],
            self.datatype_codes[options['datatype']],
        ])

    def run(self, **kwargs):
        ''' Import BLS data to local database
        '''
        # Configure default options here
        options = {
            'series': 'jobs',
            'adjustment': 'adjusted',
            'supersector': 'total_nonfarm',
            'industry': 'total',
            'datatype': 'all_employees',
        }

        # Override with options from kwargs
        for choice in options:
            if hasattr(kwargs, choice):
                options[choice] = kwargs[choice]

        # Get results from API
        series_key = self.get_series_key(options)
        r = requests.get(self.base_url + series_key)

        data = r.json()['Results']['series'][0]['data']
        self.import_data(data, options)
