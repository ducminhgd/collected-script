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
vhost = os.environ.get('AMQP_VHOST', 'amqp_vhost')

for queue in data:
    # DELETE auto generated queue
    # if queue['vhost'] == vhost and queue['name'].find('amq.gen') == 0:
    #     print(requests.delete('{}{}/{}'.format(url, 'virtual_host', queue['name']), auth=(auth_data['username'], auth_data['password'])).content)
    

    # Delete queues without consumers
    if queue['consumers'] == 0 and queue['messages_ready']>=500 :
        print(queue['name'] + ' | READY: ' + str(queue['messages_ready']))
        # status = requests.delete('{}{}/{}'.format(url, vhost, queue['name']), auth=(auth_data['username'], auth_data['password'])).status_code
        # if status == 204:
        #     print('{} is deleted'.format(queue['name']))
