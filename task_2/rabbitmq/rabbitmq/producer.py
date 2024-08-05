import json
import pika
import sys

from faker import Faker
from datetime import datetime
from models import Contact

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="email_newsletter", exchange_type="direct")
channel.queue_declare(queue="email_queue", durable=True)
channel.queue_bind(exchange="email_newsletter", queue="email_queue")

fake = Faker()


def contact_generator(number=5):
    contacts = list()
    for i in range(number):
        contact = Contact(
            full_name=fake.name(),
            email_address=fake.email()
        )
        contact.save()
        contacts.append(contact)
    return contacts


def main():
    contacts = contact_generator(5)
    for contact in contacts:
        message = {
            "id": str(contact.id),
            "payload": f"Email address: {contact.email_address}",
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange="email_newsletter",
            routing_key="email_queue",
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

        print(" [x] Email sent %r" % message)

    connection.close()


if __name__ == "__main__":
    main()
