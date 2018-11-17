from collections.abc import MutableMapping
import os

class DirDict(MutableMapping):

    def __init__(self, path):
        if os.path.isdir(path):
            self.path = path
        else:
            raise FileNotFoundError ('No such directory')
    
    def __len__(self):
        len = 0
        for each in os.listdir(self.path):
            if os.path.isfile('{}/{}'.format(self.path, each)):
                len += 1
        return len
    
    def __iter__(self):
        for each in os.listdir(self.path):
            if os.path.isfile('{}/{}'.format(self.path, each)):
                yield each
            
    def __getitem__(self, file_name):
       if os.path.exists('{}/{}'.format(self.path, file_name)):
            with open('{}/{}'.format(self.path, file_name), 'r') as f:
                return f.read()
       raise FileNotFoundError('No such file')
    
    def __setitem__(self, file_name, value):
        with open('{}/{}'.format(self.path, file_name), 'w') as f:
            f.write(value)
            
    def __delitem__(self, file_name):
        os.remove(file_name)