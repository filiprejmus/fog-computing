import logging
import random
import zmq
import sys

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class ClientTask:
    """ClientTask"""

    def __init__(self, id):
        self.id = id

    def generateData(self):
        # temperature = round(
        #     random.uniform(20, 30), 2
        # )  # generate temperature between 20 and 30 degrees Celsius
        temperature = self.id * 20
        humidity = self.id + 60
        return (temperature, humidity)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = "sensor-%d" % self.id
        socket.identity = identity.encode("ascii")
        socket.connect("tcp://localhost:5570")
        print("Sensor %s started" % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            print("Request #%d sent.." % (reqs))
            data = self.generateData()
            socket.send_string("Sensor data: %s, %s" % (data[0], data[1]))
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv()
                    print("Client %s received: %s" % (identity, msg))

        socket.close()
        context.term()


def main():
    client = ClientTask(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    client.run()


if __name__ == "__main__":
    main()
