import zmq
import threading

MsgList = []
Status = 1
threadLock = threading.Lock()

context = zmq.Context()
socket = context.socket(zmq.PUSH)


def zmq_bind(port):
	string = "tcp://*:%d" % port
	socket.bind(string)


class SendThread(threading.Thread):
	def run(self):
		global Status
		while len(MsgList):
			msg = MsgList.pop(0)
			socket.send(msg, 0)
		threadLock.acquire()
		Status = 1
		threadLock.release()


def send_msg(msg):
	MsgList.append(msg)
	global Status
	threadLock.acquire()
	if Status:
		Status = 0
		sendThread = SendThread()
		sendThread.start()
	threadLock.release()