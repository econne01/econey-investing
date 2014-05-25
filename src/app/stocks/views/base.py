from settings.common import Settings

class EconeyBaseViewHandler(object):

    def is_file_allowed(self, filename):
        return ('.' in filename
                    and filename.rsplit('.', 1)[1] in Settings.ALLOWED_UPLOAD_EXTENSIONS)
