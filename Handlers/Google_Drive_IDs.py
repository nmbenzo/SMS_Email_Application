from Handlers.file_imports import active_student_req_reg


td_id = '0ADUIPThXplYvUk9PVA' # unique ID from the Team Drive URL
folder_id = '1NNvjFLCjGl9oMwWuTKlzyt0N4aBT0QEf' # unique ID from the folder URL (2019)
my_email = 'nbenzschawel@usfca.edu'

#Spring Registration - will need to update if deleted
SCOPES = 'https://www.googleapis.com/auth/drive'

Excel = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

file_name = 'SEVIS Registration.xlsx'
uploaded_file_name = 'SEVIS Registration'
drive_file_name = 'SEVIS Registration_MASTER'
timeline_name = 'SEVIS REGISTRATION 19'

"""Google Drive API Handlers"""
# Specifies the desired upload location and mimeType
FOLDER_MIME = 'application/vnd.google-apps.folder'


SHEET_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
DOC_MIMETYPE = 'application/vnd.google-apps.document'
VID_MIMETYPE = 'application/vnd.google-apps.video'
