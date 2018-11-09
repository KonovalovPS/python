import argparse
import socket
import random
import string
import re
import shelve
import time
from datetime import datetime
from collections import OrderedDict

class Task:
    def __init__(self, length, data):
        self.length = length.decode()
        self.data = data.decode()
        self.id = ''.join(random.choice(string.ascii_uppercase +
                        string.ascii_lowercase +
                        string.digits) for _ in range(7))
        self.status = 'waiting'

    def get_dict(self):
        return {self.id:{'length': self.length, 'data': self.data, 'status': self.status}}

class Queue:
    def __init__(self, data):
        self.queue = OrderedDict()

    def add(self, data, timeout):
        queue = self.queue
        self._timeout_check(queue, timeout)
        new_task = Task(*data.split()[2:])
        queue.update(new_task.get_dict())
        return bytes(new_task.id, encoding = 'utf8')
    
    def get(self, data, timeout):
        queue = self.queue
        self._timeout_check(queue, timeout)
        for task in queue:
            if queue[task]['status'] == 'waiting':
                queue[task]['status'] = 'received'
                queue[task]['time_get'] = datetime.now()
                return bytes(f'{task} {queue[task]["length"]} {queue[task]["data"]}', encoding = 'utf8')
                break
        else:
            return b'NONE'

    def ack(self, data, timeout):
        id = data.split()[2].decode()
        queue = self.queue
        self._timeout_check(queue, timeout)
        if id in queue.keys() and queue[id]['status'] == 'received':
            queue.pop(id)
            return b'YES'
        else:
            return b'NO'
  
            
    def func_in(self, data, timeout):
        queue = self.queue
        self._timeout_check(queue, timeout)
        id = data.split()[2].decode()
        if id in queue.keys():
            return b'YES'
        else:
            return b'NO'
            
        
    def _timeout_check(self, queue, timeout):   
        counter = 2
        for idx in queue:
            if queue[idx]['status'] == 'received':
                if (datetime.now() - queue[idx]['time_get']).total_seconds() > timeout:
                    queue[idx]['status'] = 'waiting'
                else:
                    break
            else:
                counter -= 1
                if counter == 0:
                    break        
        
class TaskQueueServer:
    def __init__(self, ip, port, path, timeout):
        self.ip = ip
        self.port = port
        self.path = path
        self.timeout = timeout
        self.queues = self._get_queues()
        
    def _get_queues(self):
        file = shelve.open('data')
        if file:
            queues = file['queues']
            return queues
        queues = {}
        return queues

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(10)
        while True:
            current_connection, address = s.accept()
            while True:
                data = self._recvall(current_connection)
                if not data:
                    break
                command = self._what_function(data)
                
                
                if command == 'SAVE':
                    current_connection.send(self._save())
                    continue
                    
                queue_name = data.split()[1]
                
                if command == 'ADD':
                    if queue_name not in self.queues.keys():
                        self.queues[queue_name] = Queue(data)
                    current_connection.send(self.queues[queue_name].add(data, self.timeout))
                    continue
                    
                elif queue_name not in self.queues.keys() and command in ['GET', 'ACK', 'IN']:
                    current_connection.send(b'NONE')
                    continue
                    
                elif command == 'GET':               
                        current_connection.send(self.queues[queue_name].get(data, self.timeout))              
                    
                elif command == 'ACK':
                    current_connection.send(self.queues[queue_name].ack(data, self.timeout))   
                        
                elif command == 'IN':
                    current_connection.send(self.queues[queue_name].func_in(data, self.timeout))
                    
                else:
                    current_connection.send(b'ERROR')
            current_connection.close()
        
    def _save(self):
        file = shelve.open('data')
        file['queues'] = self.queues
        file.close()
        return b'OK'

    def _recvall(self, current_connection):
        data = b''
        while True:
            buffer = current_connection.recv(2048)
            data += buffer
            if len(buffer) < 2048:
                break
        return data
        
    def _what_function(self, string):
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