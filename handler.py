import boto3
import json


COMMITTEES = {
    # TODO verify that these are the tags used by the commitment form
    # (as opposed to the tags that start with colons).
    # Sub-TODO: 'Basebuilding' doesn't seem to be an existing tag in AN,
    # maybe it's 'Interest_Basebuilding' instead.
    'Basebuilding': 'basebuilding@surjbayarea.org',
    'Communications': 'communications@surjbayarea.org',
    'Fundraising': 'fundraising@surjbayarea.org',
    'Mobilization': 'mobilization@surjbayarea.org',
    'Queer & Trans': 'queertrans@surjbayarea.org',
    'Youth & Families': 'youthandfamilies@surjbayarea.org',
    'Policy': 'policy@surjbayarea.org',
    # TODO get contact email for Accessibility Working Group
    'Accessibility Working Group': '',
}

# TODO use an official surj email address instead (as the sender) - verify it in SES
SOURCE_EMAIL = 'danajfallon@gmail.com'


def send_email(to_addresses, subject, body):
    client = boto3.client('ses', region_name='us-west-1')
    print('SENDING EMAIL')
    print(to_addresses, subject, body)
    response = client.send_email(
        Destination={
            'ToAddresses': to_addresses
            },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=SOURCE_EMAIL,
    )
    print('EMAIL SENT', response)


def action_network_webhook(event, context):
    print('RECEIVED EVENT:', event)

    body = event.get('body')
    if body:
        body = json.loads(body)
        print('EVENT BODY:', body)
        for body_element in body:
            submission = body.get('osdi:submission', {})
            added_tags = submission.get('add_tags', [])
            if not added_tags:
                continue
            person = submission.get('person')
            email_addresses = person.get('email_addresses')
            if not email_addresses:
                continue
            # prefer primary email address if there are multiple
            email_address = sorted(email_addresses, key=lambda x: x.get('is_primary', False))[0]
            for tag in added_tags:
                if tag in COMMITTEES:
                    # send an email to the relevant committee
                    subject = 'New committee member'
                    body = f'{email_address} has indicated interest in joining your committee!'
                    to_address = COMMITTEES[tag]
                    if not to_address:
                        print('No contact email address for committee:', tag)
                        continue
                    send_email([to_address], subject, body)

    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Success',
        })
    }

    return response
