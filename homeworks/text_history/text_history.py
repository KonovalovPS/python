class TextHistory:
    
    def __init__(self, text=''):
        self._text = text
        self._version = 0
        self.hist = {}
        
    @property
    def version(self):
        return self._version
    
    @property
    def text(self):
        return self._text
    
    def insert(self, text, pos=None):
        if pos == None:
            pos = len(self.text)
        self.action(InsertAction(pos, text, from_version=self._version, to_version=self._version + 1))
        return self.version
    
    def replace(self, text, pos=None):
        if pos == None:
            pos = len(self.text)
        self.action(ReplaceAction(pos, text, from_version=self._version, to_version=self._version + 1))
        return self.version
    
    def delete(self, pos, length):
        self.action(DeleteAction(pos, length, from_version=self._version, to_version=self._version + 1))
        return self.version
    
    def action(self, obj):
        if obj.from_version != self.version or \
        obj.from_version >= obj.to_version:
            raise ValueError('Несоответствие версий')
        self._text = obj.apply(self.text)
        self._version = obj.to_version
        self.hist.update({self.version: obj})
        return self.version
    
    def get_actions(self, from_version=None, to_version=None):
        max_key = 0
        if len(self.hist) != 0:
            max_key = max(self.hist.keys())
        if from_version == None:
            from_version = 0
        if to_version == None:
            max_key += 1
            to_version = max_key
        if from_version < 0 or to_version > max_key or to_version < from_version:   
            raise ValueError('Недопустимые версии')
        arr = []
        for key in self.hist:
            if from_version < key < to_version:
                arr.append(self.hist[key])          
                
        if arr:
            arr = optimization(arr)
            
        return arr

class Action:
    def __init__(self, from_version, to_version):
        self.from_version = from_version
        self.to_version = to_version

class InsertAction(Action):
    def __init__(self, pos, text, from_version, to_version):
        self.text = text
        self.pos = pos
        super().__init__(from_version, to_version)
        
    def apply(self, text):
        if self.pos==None:
            self.pos = len(self.text)
        if self.pos < 0 or self.pos > len(text):
            raise ValueError('Недопустимая позиция')
        text = '{}{}{}'.format(text[:self.pos], self.text, text[self.pos:])
        return text
        
    def __repr__(self):
        return 'InsertAction({!r}, {!r}, {!r}, {!r})'.format(self.pos, self.text, self.from_version, self.to_version)
        
class ReplaceAction(Action):
    def __init__(self, pos, text, from_version, to_version):
        self.text = text
        self.pos = pos
        super().__init__(from_version, to_version)

    def apply(self, text):
        if self.pos==None:
            self.pos = len(self.text)
        if self.pos < 0 or self.pos > len(text):
            raise ValueError('Недопустимая позиция')
        text = '{}{}{}'.format(text[:self.pos], self.text, text[self.pos + len(self.text):])
        return text

    def __repr__(self):
        return 'ReplaceAction({!r}, {!r}, {!r}, {!r})'.format(self.pos, self.text, self.from_version, self.to_version)
    
class DeleteAction(Action):
    def __init__(self, pos, length, from_version, to_version):
        self.length = length
        self.pos = pos
        super().__init__(from_version, to_version)
    
    def apply(self, text): 
        if self.pos < 0 or self.pos + self.length > len(text):
            raise ValueError('Недопустимая позиция')
        text = '{}{}'.format(text[:self.pos], text[self.pos + self.length:])
        return text
    
    def __repr__(self):
        return 'DeleteAction({!r}, {!r}, {!r}, {!r})'.format(self.pos, self.length, self.from_version, self.to_version)
        
        
def optimization(arr):
    optimize_arr = [arr[0]]
    last_obj = arr[0]
    for each in arr[1:]:
        obj = each
        if (isinstance(obj, DeleteAction) and isinstance(last_obj, DeleteAction)
        and obj.pos <= last_obj.pos and obj.pos + last_obj.length >= last_obj.pos):
            optimize_arr.pop()
            new_obj = DeleteAction(obj.pos, last_obj.length + obj.length, last_obj.from_version, obj.to_version)
            optimize_arr.append(new_obj)
            obj = new_obj
            
        elif isinstance(obj, InsertAction) and isinstance(last_obj, InsertAction):
            if obj.pos == last_obj.pos + len(last_obj.text):
                optimize_arr.pop()
                new_obj = InsertAction(last_obj.pos, last_obj.text + obj.text, last_obj.from_version, obj.to_version)
                optimize_arr.append(new_obj)
                obj = new_obj
                
            elif obj.pos == last_obj.pos:
                optimize_arr.pop()
                new_obj = InsertAction(last_obj.pos, obj.text + last_obj.text, last_obj.from_version, obj.to_version)
                optimize_arr.append(new_obj)
                obj = new_obj
                
            else:
                optimize_arr.append(obj)
        else:
            optimize_arr.append(obj)
            
        last_obj = obj
        
    arr = optimize_arr
    return arr