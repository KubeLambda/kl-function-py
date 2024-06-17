from rocketmq.client import PushConsumer, ConsumeStatus, Producer, Message, SendResult
from invoker import invoke
import time

class ProducerManager:
    def __init__(self, group_id: str, name_server_address: str) -> None:
        self.producer = Producer(group_id)
        self.producer.set_name_server_address(name_server_address)
        self.producer.start()

    def send_message(self, topic, keys, tags, body) -> SendResult:
        msg = Message(topic)
        msg.set_keys(keys)
        msg.set_tags(tags)
        msg.set_body(body)
        sendResult = self.producer.send_sync(msg)
        print(sendResult.status, sendResult.msg_id, sendResult.offset)
        return sendResult

class ConsumerWithProducer:
    def __init__(self, group_id: str, name_server_address: str, producer_manager: ProducerManager):
        self.consumer = PushConsumer(group_id)
        self.consumer.set_name_server_address(name_server_address)
        self.producer_manager = producer_manager

    def callback(self, message) -> ConsumeStatus:
        print(message.id, message.body, message.get_property('property'))
        context = {}
        response = invoke(message.body, context)
        
        # Send response to responseTopic
        self.producer_manager.send_message('responseTopic', '', '', response)
        
        return ConsumeStatus.CONSUME_SUCCESS

    def start_consume_message(self):
        self.consumer.subscribe('requestTopic', self.callback)
        print('Start consuming messages')
        self.consumer.start()

        while True:
            time.sleep(3600)

if __name__ == "__main__":
    producer_manager = ProducerManager('webhook-adapter', '0.0.0.0:9876')
    consumer_with_producer = ConsumerWithProducer('webhook-adapter', '0.0.0.0:9876', producer_manager)
    consumer_with_producer.start_consume_message()
