from kafka import KafkaConsumer

if __name__ == '__main__':
    servers = ['192.168.186.100:9092', ]
    consumer = KafkaConsumer(
        bootstrap_servers=servers,
        auto_offset_reset='latest',  # 重置偏移量 earliest移到最早的可用消息，latest最新的消息，默认为latest
    )
    consumer.subscribe(topics=['test'])
    for msg in consumer:
        print((msg.value).decode('utf8'))
