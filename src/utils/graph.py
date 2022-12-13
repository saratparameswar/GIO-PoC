import base64
import json
import os
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient


def draft_attachment(template_name):
    template_path = './template_files/' + template_name
    if not os.path.exists(template_path):
        print('file is not found')
        return
    with open(template_path, 'rb') as upload:
        media_content = base64.b64encode(upload.read())

    data_body = {
        '@odata.type': '#microsoft.graph.fileAttachment',
        'contentBytes': media_content.decode('utf-8'),
        'name': os.path.basename(template_path)
    }
    return data_body


class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id=tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)

    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    def get_user(self):
        endpoint = '/me'
        # Only request specific properties
        select = 'displayName,mail,userPrincipalName'
        request_url = f'{endpoint}?$select={select}'

        user_response = self.user_client.get(request_url)
        return user_response.json()

    def get_inbox(self):
        endpoint = '/me/mailFolders/inbox/messages'
        # Only request specific properties
        select = 'from,isRead,receivedDateTime,subject,hasAttachments'
        # Get at most 25 results
        top = 25
        # Sort by received time, newest first
        order_by = 'receivedDateTime DESC'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        inbox_response = self.user_client.get(request_url)
        return inbox_response.json()

    def get_attachments_details(self, email_message_id):
        request_url = f'/me/messages/{email_message_id}/attachments'
        attachment_response = self.user_client.get(request_url)
        return attachment_response.json()

    def download_file(self):
        """
        Input: ID of the email
        Output: Each attachment will be saved
        """
        # save_folder = os.getcwd()
        save_folder = './binder_files'  # made change
        message_id = str(input('Enter ID of the email:'))
        attachment_items = Graph.get_attachments_details(self, message_id)['value']  # try except-ID related

        for attachment in attachment_items:
            file_name = attachment['name']
            file_id = attachment['id']
            request_url = f'/me/messages/{message_id}/attachments/{file_id}/$value'
            attachment_content = self.user_client.get(request_url)
            print('Saving file {0}...'.format(file_name))
            with open(os.path.join(save_folder, file_name), 'wb') as _f:  # look for exceptions
                _f.write(attachment_content.content)

    def send_mail(self, template_name: str, recipient: str):
        request_body = {
            'message': {
                'subject': template_name,
                'body': {
                    'contentType': 'text',
                    'content': 'Body related to' + ' ' + template_name
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': recipient
                        }
                    }
                ],
                'attachments': [
                    draft_attachment(template_name)
                ]
            }
        }

        request_url = '/me/sendmail'

        self.user_client.post(request_url,
                              data=json.dumps(request_body),
                              headers={'Content-Type': 'application/json'})
