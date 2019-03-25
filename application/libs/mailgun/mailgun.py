import requests

def send(email):
    key = 'key-d2e513ab0d5ef69d59324bc55b2778cd'
    sandbox = 'sandboxdfb0126042a64248929ed54a28a15ee4.mailgun.org'
    recipient = email

    request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
    request = requests.post(request_url, auth=('api', key), data={
        'from': 'support@opsdojo.com',
        'to': recipient,
        'subject': 'Hello',
        'text': 'Hello from Mailgun'
    })
