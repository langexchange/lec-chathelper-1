
from confluent_kafka import Consumer, KafkaError, KafkaException
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
    
    def initPullLoop(self, task_id):
      logger.debug('initPullLoop get call by {}'.format(ChatWorkerConsumer.__name__))
      try:
        logger.debug('Before subscribe topics')
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