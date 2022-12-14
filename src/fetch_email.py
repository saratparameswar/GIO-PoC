import configparser
from src.utils.graph import Graph


def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['./config/azure_config.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        # print('1. Display access token')
        print('1. List my inbox')
        print('2. Send mail')
        # print('4. List users (requires app-only)')
        # print('5. Make a Graph call')
        # print("6. Retrieve an attachment's ID")
        print("3. Save an attachment with an ID")
        print("4. Save all attachments of last day")
        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        # elif choice == 1:
        #     display_access_token(graph)
        elif choice == 1:
            list_inbox(graph)
        elif choice == 2:
            send_mail(graph)
        # elif choice == 4:
        #     list_users(graph)
        # elif choice == 5:
        #     make_graph_call(graph)
        # elif choice == 6:
        #     for_attachment_details(graph)
        elif choice == 3:
            to_download_file(graph)
        elif choice == 4:
            for_all_attachments(graph)
        else:
            print('Invalid choice!\n')


def greet_user(graph: Graph):
    user = graph.get_user()
    print('Hello,', user['displayName'])
    # For Work/school accounts, email is in mail property
    # Personal accounts, email is in userPrincipalName
    print('Email:', user['mail'] or user['userPrincipalName'], '\n')


def display_access_token(graph: Graph):
    token = graph.get_user_token()
    print('User token:', token, '\n')


def list_inbox(graph: Graph):
    message_page = graph.get_inbox()

    # Output each message's details
    for message in message_page['value']:
        print("Id", message['id'])
        print('Message:', message['subject'])
        print('  From:', message['from']['emailAddress']['name'])
        print('  Status:', 'Read' if message['isRead'] else 'Unread')
        print('  Received:', message['receivedDateTime'])

    # If @odata.nextLink is present
    more_available = '@odata.nextLink' in message_page
    print('\nMore messages available?', more_available, '\n')


def for_attachment_details(graph: Graph):
    """
    Input: ID of the email
    Output: Details(ID, Name, Type of content) of the attachment in the particular email
    """

    email_message_id = str(input('Enter ID of the email:'))
    attachment_items = graph.get_attachments_details(email_message_id)['value']
    for attachment in attachment_items:
        print(' Attachment Name: ', attachment['name'])
        print(' Attachment ID: ', attachment['id'])
        print(' Attachment Type: ', attachment['contentType'])
    more_available = '@odata.context' in attachment_items
    print('\nMore messages available?', more_available, '\n')


def to_download_file(graph: Graph):
    graph.download_file()
    print('All attachments has been saved')


def send_mail(graph: Graph):
    # Send mail to the signed-in user
    # Get the user for their email address
    # user = graph.get_user()  # made change
    # user_email = user['mail'] or user['userPrincipalName']  # made change
    user_email = str(input("Enter the recipient email: "))
    attachment_name = input('Enter name of the attachment: ')
    graph.send_mail(attachment_name, user_email)
    print('Mail sent.\n')
    return


def for_all_attachments(graph: Graph):
    graph.download_all_attachments()
    print('All attachments has been saved')


def list_users(graph: Graph):
    # TODO
    return


def make_graph_call(graph: Graph):
    # TODO
    return


main()
