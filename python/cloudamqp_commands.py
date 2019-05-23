import requests
import json
import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True, verbose=True)

auth_data = {
    'username': os.environ.get('AMQP_USERNAME', 'username'),
    'password': os.environ.get('AMQP_PASSWORD', 'password'),
}
host = os.environ.get('AMQP_HOST', 'amqp_host')
url = 'https://{}/api/queues/'.format(host)
response = requests.get(url, auth=(auth_data['username'], auth_data['password']))
data = json.loads(response.content)
vhost = os.environ.get('AMQP_HOST', 'amqp_host')

for queue in data:
    # if queue['vhost'] == vhost and queue['name'].find('amq.gen') == 0:
    #     print(requests.delete('{}{}/{}'.format(url, 'virtual_host', queue['name']), auth=(auth_data['username'], auth_data['password'])).content)
    # if queue['name'] == 'teko.monitor':
    #     print(json.dumps(queue))
    if queue['consumers'] == 0:
        print(queue['name'] + ' | READY: ' + str(queue['messages_ready']))
