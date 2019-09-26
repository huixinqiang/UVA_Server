import zmq

context = zmq.Context()
socket = context.socket(zmq.PULL)


def zmq_connect(IP, port):
    string = "tcp://%s:%d" % (IP, port)
    socket.connect(string)


def recv_msg():
    byteArray = socket.recv(0)
    return byteArray
