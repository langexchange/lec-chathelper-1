from json import loads
from confluent_kafka import Consumer, KafkaError, KafkaException
import sys



conf = {'bootstrap.servers': "localhost:9092",
        'group.id': "chathelper",
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False}  

consumer = Consumer(conf)


def msg_process(msg):
    msg = msg.value()
    print('{} added to'.format(msg.decode()))

running = True
MIN_COMMIT_COUNT = 5

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

basic_consume_loop(consumer, ["chathelper-friendstate", "chathelper-userupdate"])
def shutdown():
    running = False