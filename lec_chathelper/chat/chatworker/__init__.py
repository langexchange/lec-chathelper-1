
from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
import sys
import logging
from celery.contrib.abortable import AbortableAsyncResult

logger = logging.getLogger(__name__)

class ChatWorkerConsumer:
    def __init__(self, commitCount, conf):
        self.conf = conf
        self.consumer = Consumer(conf)
        self.commitCount = commitCount
        self.handlers = {}

    def register(self, topicName, handlerInstance):
      self.handlers[topicName] = handlerInstance

    def callHandler(self, message):
      topicName = message.topic()
      if topicName not in self.handlers:
        logger.error('There is no handler for this {}'.format(topicName))
      logger.info('Call handler {} for msg {}'.format(self.handlers[topicName], message.value()))
      self.handlers[topicName].handle(message)
    
    def createTopicsIfNotExists(self, num_partitions=1, replication_factor=1):
      admin_client = AdminClient({'bootstrap.servers': self.conf["bootstrap.servers"]})
      topic_metadata = admin_client.list_topics(timeout = 5)

      new_topics = []
      for topic in self.handlers:
        if topic not in topic_metadata.topics:
          new_topic = NewTopic(topic=topic, num_partitions=num_partitions, replication_factor=replication_factor)
          new_topics.append(new_topic)

        else:
          logger.debug("Topic {} already exists".format(topic))

      if not new_topics:
        return

      futures = admin_client.create_topics(new_topics)
      for topic_name in futures:
        try:
          futures[topic_name].result()
          logger.debug("Create topic {} with num_partitions {} and replication_factor {}".format(topic_name, num_partitions, replication_factor))
        except Exception as e:
          logger.warn("Failed to create topic {}: {}".format(topic_name, e))


    def initPullLoop(self, task_id):
      logger.debug('initPullLoop get call by {}'.format(ChatWorkerConsumer.__name__))
      try:
        logger.debug('Before subscribe topics')
        self.createTopicsIfNotExists(num_partitions=1, replication_factor=1)
        self.consumer.subscribe(list(self.handlers.keys()))
        logger.debug('After subscribe topics')
        msg_count = 0
        while True:
            if AbortableAsyncResult(task_id).is_aborted():
                logger.warning('Task aborted')
                return
            msg = self.consumer.poll(timeout=1.0)
            logger.debug('Loop ...')
            if msg is None: continue

            if msg.error():
                logger.debug('Encounter error')
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.error('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    logger.exception(msg.error())
                    raise KafkaException(msg.error())
            else:
                logger.debug('Before call handler')
                self.callHandler(msg)
                msg_count += 1
                if msg_count % self.commitCount == 0:
                    self.consumer.commit(asynchronous=True)
      finally:
        logger.debug('Close {}'.format(ChatWorkerConsumer.__name__))
        self.consumer.close()