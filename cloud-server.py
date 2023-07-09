import zmq
import sys
import time
from random import randint, random
import threading


class ServerTask:
    """ServerTask"""

    def __init__(self):
        self.data = []
        self.response_data = 0
        self.client_idents = set({str.encode("sensor-1"), str.encode("sensor-2")})

    def calculate_data_and_send(self, frontend):
        threading.Timer(15, self.calculate_data_and_send, [frontend]).start()
        response_data = str.encode(
            "Sensor data: %s, %s"
            % (
                str(len(self.data)),
                str(len(self.data)),
            )
        )
        for ident in self.client_idents:
            print("Sending %s to %s", response_data, ident)

            frontend.send_multipart([ident, response_data])

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind("tcp://*:5570")
        self.calculate_data_and_send(frontend)
        print("Worker started")
        while True:
            ident, msg = frontend.recv_multipart()
            self.data.append(msg.decode())
            print("Cloud worker received %s from %s" % (msg, ident))

        context.term()


def main():
    """main function"""
    server = ServerTask()
    server.run()


if __name__ == "__main__":
    main()
