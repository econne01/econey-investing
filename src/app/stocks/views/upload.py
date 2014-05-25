import os
from flask import render_template, request
from app import app
from werkzeug.utils import secure_filename

from settings.common import Settings
from app.stocks.views import EconeyBaseViewHandler

@app.route('/upload', methods=['GET', 'POST'])
def upload_form():
    handler = EconeyBaseViewHandler()

    filename = None
    if request.method == 'POST':
        file = request.files['file']
        if file and handler.is_file_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('uploadForm.html', uploaded_filename=filename)
