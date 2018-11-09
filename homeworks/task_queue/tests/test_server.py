from unittest import TestCase

import time
import socket
import os
import subprocess

from server import TaskQueueServer


class ServerBaseTest(TestCase):
    def setUp(self):
        self.server = subprocess.Popen(['python', 'server.py', '-t 3'])
        # даем серверу время на запуск
        time.sleep(0.5)

    def tearDown(self):
        self.server.terminate()
        self.server.wait()

    def send(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 5555))
        s.send(command)
        data = s.recv(1000000)
        s.close()
        return data
        
    def del_journal(self):
        try:
            os.remove("data.dir")
            os.remove("data.dat")
            os.remove("data.bak")
        except FileNotFoundError:
            pass

    def test_base_scenario(self):
        task_id = self.send(b'ADD 1 5 12345')
        self.assertEqual(b'YES', self.send(b'IN 1 ' + task_id))

        self.assertEqual(task_id + b' 5 12345', self.send(b'GET 1'))
        self.assertEqual(b'YES', self.send(b'IN 1 ' + task_id))
        self.assertEqual(b'YES', self.send(b'ACK 1 ' + task_id))
        self.assertEqual(b'NO', self.send(b'ACK 1 ' + task_id))
        self.assertEqual(b'NO', self.send(b'IN 1 ' + task_id))

    def test_two_tasks(self):
        first_task_id = self.send(b'ADD 1 5 12345')
        second_task_id = self.send(b'ADD 1 5 12345')
        self.assertEqual(b'YES', self.send(b'IN 1 ' + first_task_id))
        self.assertEqual(b'YES', self.send(b'IN 1 ' + second_task_id))

        self.assertEqual(first_task_id + b' 5 12345', self.send(b'GET 1'))
        self.assertEqual(b'YES', self.send(b'IN 1 ' + first_task_id))
        self.assertEqual(b'YES', self.send(b'IN 1 ' + second_task_id))
        self.assertEqual(second_task_id + b' 5 12345', self.send(b'GET 1'))

        self.assertEqual(b'YES', self.send(b'ACK 1 ' + second_task_id))
        self.assertEqual(b'NO', self.send(b'ACK 1 ' + second_task_id))

    def test_long_input(self):
        data = '12345' * 1000
        data = '{} {}'.format(len(data), data)
        data = data.encode('utf')
        task_id = self.send(b'ADD 1 ' + data)
        self.assertEqual(b'YES', self.send(b'IN 1 ' + task_id))
        self.assertEqual(task_id + b' ' + data, self.send(b'GET 1'))

    def test_wrong_command(self):
        self.assertEqual(b'ERROR', self.send(b'ADDD 1 5 12345'))
    
    def test_timeout(self):
        first_task_id = self.send(b'ADD a 3 111')
        second_task_id = self.send(b'ADD a 3 222')
        third_task_id = self.send(b'ADD a 3 333')
        self.assertEqual(first_task_id + b' 3 111', self.send(b'GET a'))
        time.sleep(2)
        self.assertEqual(second_task_id + b' 3 222', self.send(b'GET a'))
        time.sleep(2)
        self.assertEqual(first_task_id + b' 3 111', self.send(b'GET a'))
        self.assertEqual(third_task_id + b' 3 333', self.send(b'GET a'))
        self.assertEqual(b'YES', self.send(b'ACK a ' + first_task_id))
        time.sleep(1)
        self.assertEqual(b'NO', self.send(b'ACK a ' + second_task_id))
        self.send(b'GET a')
        self.assertEqual(b'YES', self.send(b'ACK a ' + second_task_id))
        self.assertEqual(b'YES', self.send(b'ACK a ' + third_task_id))
        
    def test_saving(self):
        first_task_id = self.send(b'ADD z 3 111')
        second_task_id = self.send(b'ADD z 3 222') 
        third_task_id = self.send(b'ADD z 3 333') 
        self.assertEqual(first_task_id + b' 3 111', self.send(b'GET z'))
        self.assertEqual(second_task_id + b' 3 222', self.send(b'GET z'))
        self.assertEqual(b'OK', self.send(b'SAVE'))
        self.tearDown()
        self.setUp()
        self.assertEqual(b'YES', self.send(b'ACK z ' + first_task_id))
        self.assertEqual(b'YES', self.send(b'ACK z ' + second_task_id))
        self.assertEqual(third_task_id + b' 3 333', self.send(b'GET z'))
        self.assertEqual(b'YES', self.send(b'ACK z ' + third_task_id))
        self.del_journal()

if __name__ == '__main__':
    unittest.main()