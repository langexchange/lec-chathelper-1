from confluent_kafka import Producer
import socket
import json

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}
producer = Producer(conf)

"""
{
  jid:
  state: friend;
}

{
  jid:
  state: unfriend;
}
"""

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

def push_friend_state():
    with open("./mock/friendstate.json", "r") as file:
      data_set = json.load(file)
      for data in data_set:
        producer.produce("chathelper-friendstate", value=json.dumps(data), callback=acked)
        producer.poll(1)

push_friend_state()

"""
{
  jid: ;
  #Anything personal information changed:
  nickname:
}
"""
# def push_user_update():
#     with open("./mock/userupdate.json", "r") as file:
#       data_set = json.load(file)
#       for data in data_set:
#         producer.produce("chathelper-userinfo", value=json.dumps(data), callback=acked)
#         producer.poll(1)


# push_user_update()