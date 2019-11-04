import paho.mqtt.client as mqtt

broker_url = "0.0.0.0"
broker_port = 1883

client = mqtt.Client()
client.connect(broker_url, broker_port)
client.subscribe("TestingTopic", qos=1)