import logging
import argparse
import zmq
import threading
import json
import math
import time

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class ClientTask:
    """ClientTask"""

    def __init__(self, id, ip):
        self.id = id
        self.server_ip = ip
        print(f"Device ID: {self.id}")
        print(f"Server IP: {self.server_ip}")

    def generateData(self, socket):
        threading.Timer(5, self.generateData, [socket]).start()
        t = time.time()
        temperature = 10 * math.sin(2 * math.pi * t / 150) + 30
        humidity = self.id + 60
        sensor_data_json = {"temperature": temperature, "humidity": humidity}
        sensor_data = json.dumps(sensor_data_json)
        socket.send_string(sensor_data)
        print(f"Request {sensor_data} sent..")

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = "sensor-%d" % self.id
        socket.identity = identity.encode("ascii")
        socket.connect(f"tcp://{self.server_ip}:5570")
        self.generateData(socket)

        print("Sensor %s started" % (identity))

        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv()
                    msg_json = json.loads(msg.decode())
                    print("Client %s received: %s" % (identity, msg_json))
                    if msg_json["action"] == "red":
                        pass
                    if msg_json["action"] == "green":
                        pass

        socket.close()
        context.term()


def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip", type=str, required=False, help="IP address", default="127.0.0.1"
    )
    parser.add_argument("--id", type=int, required=False, help="ID", default=1)

    args = parser.parse_args()
    ip = args.ip
    id = args.id
    client = ClientTask(id=id, ip=ip)
    client.run()


if __name__ == "__main__":
    main()
