from __future__ import print_function
import httplib2
from apiclient import discovery
from email import encoders
from oauth2client import tools
from oauth2client import file, client, tools
from apiclient import errors
from oauth2client import tools
from Emails import authorization


SCOPES = 'https://mail.google.com/'
client_secret = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

# Building an instance of the Gmail authorization class
authInstance = authorization.Auth(SCOPES, client_secret, APPLICATION_NAME)
# Building an instance of the credentials method
credentials = authInstance.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)


def get_labels():
    """Returns a list of labels from the authorized Gmail Account"""
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
