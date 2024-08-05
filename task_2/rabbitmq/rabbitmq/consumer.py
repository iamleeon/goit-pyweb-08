import json
import pika
import time

from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="email_queue", durable=True)
print(" [*] Waiting for emails. To exit press CTRL+C")


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact_id = message["id"]
    print(f" [x] Received email {message} for {contact_id}")
    contact = Contact.objects(id=contact_id).first()

    if contact:
        print(f" [x] Sending email to {contact.email_address}")
        time.sleep(1)
        contact.is_sent = True
        contact.save()
        print(f" [x] Done: {method.delivery_tag}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="email_queue", on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
