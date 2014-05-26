import csv
import sqlite3

from flask import render_template, request
from app import app

from settings.common import Settings
from app.stocks.views import EconeyBaseViewHandler

class StockHistoryUploader(EconeyBaseViewHandler):

    db_name= 'stocks.db'
    table_name = 'results_year'

    # Columns of upload file must contain Ticker, Year, then any optional data columns
    column_format = {
        'fixed': ['ticker', 'year'],
        'optional': ['revenue']
    }

    def is_file_format_accepted(self, headers):
        ''' Check to confirm proper column format
        '''
        fixed_cnt = len(self.column_format['fixed'])
        if len(headers) < fixed_cnt:
            return False

        # Confirm file has the required Columns
        for i, col in enumerate(self.column_format['fixed']):
            if headers[i].lower() != col:
                return False

        for col in headers[fixed_cnt:]:
            if col.lower() not in self.column_format['optional']:
                return False

        return True

    def save_file_data(self, file):
        ''' If file is in proper format, update database with data from file
        '''
        from app import query_db

        row_cnt = 0
        reader = csv.DictReader(file)

        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        if self.is_file_format_accepted(reader.fieldnames):
            for row in reader:
                row = dict((k.lower(), v) for k,v in row.iteritems())
                print row
                row_cnt += 1
                try:
                    # Try to INSERT
                    qry = '''
                        INSERT INTO {}
                        ({})
                        VALUES ({});
                    '''.format(
                        self.table_name,
                        ','.join(reader.fieldnames),
                        ','.join(['?' for field in reader.fieldnames]),
                    )

                    args = [row[field] for field in reader.fieldnames]
                    query_db(qry, args)
                except sqlite3.IntegrityError as e:
                    # If row already exists, then update it
                    qry = '''
                        UPDATE {}
                        SET {}
                        WHERE {}
                    '''.format(
                        self.table_name,
                        ','.join([field + '=?' for field in self.column_format['optional']]),
                        ' AND '.join([field + '=?' for field in self.column_format['fixed']]),
                    )
                    args = [row[field] for field in self.column_format['optional']]
                    args += [row[field] for field in self.column_format['fixed']]
                    query_db(qry, args)

        return row_cnt

@app.route('/upload', methods=['GET', 'POST'])
def upload_form():
    handler = StockHistoryUploader()

    filename = None
    if request.method == 'POST':
        file = request.files['file']
        if file and handler.is_file_allowed(file):
            handler.save_file_data(file)

    return render_template('uploadForm.html', uploaded_filename=filename)
