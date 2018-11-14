import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import sys
sys.path.append("../")
from BaseGame import *
import time
import threading 

NAME = 'Arkanoid'

class Storage(Scorer):
    def __init__():
        self.table = {}
        
        
class Game(BaseGame):

    def __init__(self):
        self.win_borders = (30, 60, 0, 0)
        self.level = 26
        self.stage = [[self.level, 29], [self.level, 30], [self.level, 31], [self.level, 32], [self.level, 33]]
        self.ball = [24, 30]
        self.keys = (KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN)
        self.key = ''
        self.idx = 0
        self.col_monsters = 4
        self.monsters = set()
        self.score = 0
        self.health = 7
        self.monster = ['♣', '$', '♠']
            
    def monsters_add(self, win, lvl):
        if lvl == 0:
            win.addstr(27, 16, 'НЕ ЗАЖИМАЙТЕ КЛАВИШИ, УДАЧИ!')
        else:
            win.addstr(27, 16, 'NEXT LEVEL: LAST MONSTERS WENT HOME')
            if lvl % 3 == 2:
                win.addstr(27, 9, 'NEXT LEVEL: LAST DAMNED CAPITALISTS WENT HOME')
            win.addstr(self.level + 1, 0, ' '* 60)
            curses.delay_output(1000)
            #time.sleep(1.5)
        def clear_output():
            time.sleep(4)
            win.addstr(27, 0, ' '* 60)
        t = threading.Thread(target = clear_output)
        t.start()
        
        self.stage = [[self.level, 29], [self.level, 30], [self.level, 31], [self.level, 32], [self.level, 33]]
            
        for i in range(self.win_borders[1])[14:-14]: 
            for j in range(self.win_borders[0])[7: 7 + self.col_monsters]: 
                self.monsters.add((j, i))
                win.addch(j, i, self.monster[lvl % 3])
                
    def ball_behavior(self, dx, dy):
        delete_monsters = []
        if self.ball[0] == 28:
            dx *= -1
            self.health -= 1
            if self.health == 0:
                return 'gameover', '_', '_'
        if self.ball[0] == 0:
            dx *= -1               
        if self.ball[1] in (58, 2):
            dy *= -1  
        if self.ball[0] + dx == self.stage[0][0] and self.stage[0][1] <= self.ball[1] <= self.stage[0][1] + 4:
            dx *= -1
        
        if self.ball[0] + dx == self.stage[0][0] and \
        (self.stage[0][1] - 1 == self.ball[1] or self.stage[0][1] + 5 == self.ball[1]):
            dx *= -1
            dy *= -1
        
        if (self.ball[0], self.ball[1]) in self.monsters:
            self.monsters.remove((self.ball[0], self.ball[1]))
            delete_monsters.append((self.ball[0], self.ball[1]))
            self.score += 10
        
        if (self.ball[0] + dx, self.ball[1]) in self.monsters:
            self.monsters.remove((self.ball[0] + dx, self.ball[1]))
            delete_monsters.append((self.ball[0] + dx, self.ball[1]))
            self.score += 10
            if (self.ball[0], self.ball[1] + dy) in self.monsters:
                self.monsters.remove((self.ball[0], self.ball[1] + dy))
                delete_monsters.append((self.ball[0], self.ball[1] + dy))
                self.score += 10
                dx *= -1
                dy *= -1
            else:
                dy *= -1
                
        elif (self.ball[0] + dx, self.ball[1]) not in self.monsters and \
        (self.ball[0], self.ball[1] + dy) not in self.monsters and\
        (self.ball[0] + dx, self.ball[1] + dy) in self.monsters:
            self.monsters.remove((self.ball[0] + dx, self.ball[1] + dy))
            delete_monsters.append((self.ball[0] + dx, self.ball[1] + dy))
            self.score += 10
            dx *= -1
            dy *= -1
                
        return dx, dy, delete_monsters

    def loop(self, win):
        dx = -1
        dy = 1
        lvl = 0
        self.monsters_add(win, lvl)
        
        for each in self.stage:
            win.addch(each[0], each[1], '=')
        self.idx = 0
        win.border(0)
        win.addstr(0, 27, ' Arkanoid ')
        
        
        while True:
            time.sleep(0.025)
            win.addstr(5, 50, 'level: {}'.format(lvl + 1))
            win.addstr(3, 50, '♥' * self.health + 'x'*(7 - self.health))
            win.border(0)
            win.addstr(0, 25, ' Arkanoid ')    
            win.addstr(29, 10, 'Right: → ')
            win.addstr(29, 25, 'Left: ← ')
            win.addstr(29, 40, 'Stop: ↑↓')
            win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
            win.addstr(0, 45, ' Monsters:{}'.format(len(self.monsters)))    
            win.timeout(99)
            
            win.addch(self.ball[0], self.ball[1], ' ')
            dx, dy, delete = self.ball_behavior(dx, dy)
            if dx == 'gameover':
                break
            self.ball[0] += dx
            self.ball[1] += dy
            for each in delete:
                win.addch(each[0], each[1], ' ')
            win.addch(self.ball[0], self.ball[1], 'o')
           
            event = win.getch()
            if event == 27: # Escape
                break
            elif event == KEY_RIGHT:
                self.idx = 1
            elif event == KEY_LEFT:
                self.idx = -1     
            elif event in (KEY_DOWN, KEY_UP):
                self.idx = 0
            
            for i in range(2):
                if self.idx == -1 and self.stage[0][1] == 1:
                    continue
                if self.idx == 1 and self.stage[2][1] == self.win_borders[1] - 4:
                    continue
                
                for each in self.stage:
                    win.addch(each[0], each[1], ' ')
                for each in self.stage:
                    each[1] += self.idx
                    win.addch(each[0], each[1], '=') 
                  
            if len(self.monsters) <= 25:
                self.level -= 1
                lvl += 1
                self.monsters_add(win, lvl)
                win.addch(self.ball[0], self.ball[1], ' ')
                self.ball = [24, 30]
                dx = -1
                
    
    def run(self):     
                
        curses.initscr()
        
        win = curses.newwin(*self.win_borders)
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)
        
        try:
            self.loop(win)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

        win.nodelay(0)
        win.keypad(0)
        curses.echo()
        curses.endwin() 
        print("\nScore - {}".format(self.score))
        
if __name__ == '__main__':
    Game().run()