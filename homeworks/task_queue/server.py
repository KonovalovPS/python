import argparse
import socket
import random
import string

class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self.ip = ip
        self.port = port
        self.path = path
        self.timeout = timeout

    queue = {}

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(10)
        while True:
            current_connection, address = s.accept()
            while True:
                data = current_connection.recv(2048)
                if self.is_add(data):
                    queue_name = data.split()[1]
                    if queue_name not in self.queue.keys():
                        self.queue[queue_name] = Queue(*data.split())
                        self.queue[queue_name].id = ''.join(random.choice(string.ascii_uppercase +
                        string.ascii_lowercase +
                        string.digits) for _ in range(32))
                else:
                    current_connection.send(b'no\n')
    
    def is_add(self, string):
        if string.split()[0] == b'ADD' and\
        int(string.split()[2]) <= 1000000:
            return True
        return False

def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip adress')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()

class Queue:
    def __init__(queue_name, length, data):
        self.queue_name = queue_name
        self.length = length
        self.data = [data]
        
    def add(data):
        self.data.append(data)
        
    
if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()