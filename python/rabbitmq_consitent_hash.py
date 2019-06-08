import os
import pika
import time

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True, verbose=True)

credentials = pika.PlainCredentials(
    os.environ.get('AMQP_USERNAME', 'username'),
    os.environ.get('AMQP_PASSWORD', 'password')
    )
conn = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('AMQP_HOST', 'amqp_host'),
    virtual_host=os.environ.get('AMQP_VHOST', 'amqp_vhost'),
    credentials=credentials
    ))
ch   = conn.channel()

ch.exchange_declare(exchange="e", exchange_type="x-consistent-hash", durable=True)

for q in ["q1", "q2", "q3", "q4"]:
    ch.queue_declare(queue=q, durable=True)
    ch.queue_purge(queue=q)

for q in ["q1", "q2"]:
    ch.queue_bind(exchange="e", queue=q, routing_key="1")

for q in ["q3", "q4"]:
    ch.queue_bind(exchange="e", queue=q, routing_key="2")

n = 100000

for rk in list(map(lambda s: str(s), range(0, n))):
    ch.basic_publish(exchange="e", routing_key=rk, body="")
print("Done publishing.")

print("Waiting for routing to finish...")
# in order to keep this example simpler and focused,
# wait for a few seconds instead of using publisher confirms and waiting for those
time.sleep(5)

print("Done.")
conn.close()