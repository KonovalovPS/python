import argparse
import socket
import random
import string
import re
import shelve
import time
import threading

class Task:
    def __init__(self, length, data):
        self.length = length.decode()
        self.data = data.decode()
        self.id = ''.join(random.choice(string.ascii_uppercase +
                        string.ascii_lowercase +
                        string.digits) for _ in range(7))
        self.status = 'waiting'

class TaskQueueServer():
    def __init__(self, ip, port, path, timeout):
        self.ip = ip
        self.port = port
        self.path = path
        self.timeout = timeout

    #queues = {}
    file = shelve.open('data')
    if file:
        queues = file['queues']
    else:
        queues = {}
    
    def timeout_check(self, task, queue):
        time.sleep(self.timeout)
        if task.status == 'received':
            task.status = 'waiting'
            
    def recvall(self, current_connection):
        data = b''
        while True:
            buffer = current_connection.recv(2048)
            data += buffer
            if len(buffer) < 2048:
                break
        return data
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(10)
        while True:
            current_connection, address = s.accept()
            while True:
                data = self.recvall(current_connection)
                if not data:
                    break
                command = self.what_function(data)
                if command == 'ADD':
                    self.add(data, current_connection)
                    
                elif command == 'GET':
                    self.get(data, current_connection)                
                    
                elif command == 'ACK':
                    self.ack(data, current_connection)   
                        
                elif command == 'IN':
                    self.func_in(data, current_connection) 
                    
                elif command == 'SAVE':
                    self.save(current_connection)
                    
                else:
                    current_connection.send(b'ERROR')
            current_connection.close()
                    
    def add(self, data, current_connection):
        queue_name = data.split()[1]
        if queue_name not in self.queues.keys():
            self.queues[queue_name] = []
        new_task = Task(*data.split()[2:])
        self.queues[queue_name].append(new_task)
        current_connection.send(bytes(new_task.id, encoding = 'utf8'))
    
    def get(self, data, current_connection):
        queue_name = data.split()[1]
        if queue_name in self.queues.keys():
            for task in self.queues[queue_name]:
                if task.status == 'waiting':
                    task.status = 'received'
                    current_connection.send(bytes('{0.id} {0.length} {0.data}'.format(task), encoding = 'utf8'))
                    t = threading.Thread(target = self.timeout_check, args = (task, self.queues[queue_name]))
                    t.start()
                    break
            else:
                current_connection.send(b'NONE')
        else:
            current_connection.send(b'NONE')

    def ack(self, data, current_connection):
        queue_name = data.split()[1]
        id = data.split()[2].decode()
        if queue_name in self.queues.keys():
            for task in self.queues[queue_name]:
                if task.id == id and task.status == 'received':
                    self.queues[queue_name].remove(task)
                    current_connection.send(b'YES')
                    break
            else:
                current_connection.send(b'NO')
        else:
            current_connection.send(b'NONE')   
        
    def func_in(self, data, current_connection):
        queue_name = data.split()[1]
        id = data.split()[2].decode()
        if queue_name in self.queues.keys():
            for task in self.queues[queue_name]:
                if task.id == id:
                    current_connection.send(b'YES')
                    break
            else:
                current_connection.send(b'NO')
        else:
            current_connection.send(b'NONE')
            
    def save(self, current_connection):
        file = shelve.open('data')
        file['queues'] = self.queues
        file.close()
        current_connection.send(b'OK')
        
    def what_function(self, string):
        string = string.decode()
        if re.fullmatch(r'ADD \S+ \d+ \S+\s{0,1}', string):
            return 'ADD'
            
        elif re.fullmatch(r'GET \S+\s{0,1}', string):
            return 'GET'
            
        elif re.fullmatch(r'ACK \S+ \S+\s{0,1}', string):
            return 'ACK'
    
        elif re.fullmatch(r'IN \S+ \S+\s{0,1}', string):
            return 'IN'
            
        elif re.fullmatch(r'SAVE\s{0,1}', string):    
            return 'SAVE'
        

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
   
if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()