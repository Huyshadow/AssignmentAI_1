from level import Level
import numpy as num
import copy

class GamePlay:
    left ="LEFT"
    right = 'RIGHT'
    up    = 'UP'
    down  = 'DOWN'
    switch = 'SWITCH'

    @staticmethod
    def opposite_action(action:str, check):
        if action == GamePlay.down:
            return check == GamePlay.up
        if action == GamePlay.up:
            return check == GamePlay.down
        if action == GamePlay.left:
            return check == GamePlay.right
        if action == GamePlay.right:
            return check == GamePlay.left
        if action == GamePlay.switch:
            return check == GamePlay.switch
        return False

    @staticmethod
    def take_action_set():
        return [GamePlay.up,GamePlay.down,GamePlay.left,GamePlay.right,GamePlay.switch]
    
    @staticmethod
    def decode_action(action_check):
        for action in GamePlay.take_action_set():
            if action[0] == action_check:
                return action
            
class State:
    def __init__(self, cur:list, goal: list, board_state: dict):
        self.cur = copy.copy(cur)
        self.goal = copy.copy(goal)
        self.board_state = copy.copy(board_state)

    def standing(self):
        return len(self.cur) == 2

    def splited(self):
        return len(self.cur) == 4 \
            and Blozorx.calculate_distance(self.cur[:2], self.cur[2:]) != 1
        
    def lying(self):
        return not self.standing() and not self.splited()

    def goal(self):
        return self.standing() \
            and self.cur == self.goal

    def available(self,x,y):
        return (0 <= x < self.board_state.shape[0])\
            and (0 <= y < self.board_state.shape[1])\
            and self.board_state[x,y]

    def __eq__(self, other):
        return num.array_equal(self.board_state,other.board_state) \
            and self.cur == other.cur

class Blozorx:
    TRIGGER_OF_MAP = {
        'none'  : 'none',
        'hide'  : 'hide',
        'unhide': 'unhide',
        'toggle': 'toggle'
    }

    CELL_TYPE_MAP = {
        'normal'     : 0,
        'fragile'    : 1,
        'flexible'   : 2,
        'x_btn'      : 3,
        'o_btn'      : 4,
        'split_btn'  : 5,
    }

    def __init__(self, level):
        self.level_display(level)

    def level_display(self,level):
        self.level_id = Level(level)
        #Create Board when we play
        self.board = num.zeros(self.level_id.board.shape, dtype='int') 

        self.btn_target_map = {}

        for x,y in self.level_id.fragile_cells:
            self.board[x,y] = self.CELL_TYPE_MAP['fragile']

        for x,y,target_list in self.level_id.x_btn:
            self.board[x,y] = self.CELL_TYPE_MAP['x_btn']
            for bx,by,_ in target_list:
                self.board[bx,by] = self.CELL_TYPE_MAP['flexible']
            self.btn_target_map[(x,y)] = target_list

        for x,y,target_list in self.level_id.o_btn:
            self.board[x,y] = self.CELL_TYPE_MAP['o_btn']
            for bx,by,_ in target_list:
                self.board[bx,by] = self.CELL_TYPE_MAP['flexible']
            self.btn_target_map[(x,y)] = target_list

        for x,y,target_list in self.level_id.split_btn_list:
            self.board[x,y] = self.CELL_TYPE_MAP['split_btn']
            self.btn_target_map[(x,y)] = target_list

        #Initialize the start state
        self.init_state = State(cur = self.level_id.start,
                                goal = self.level_id.goal,
                                board_state = self.level_id.board)
    
    def possible_actions_nows(self, state:State):
        possile_actions = []

        if state.standing():
            x,y = state.cur
            if state.available(x-2,y) and state.available(x-1,y):
                possile_actions.append(GamePlay.up)
            if state.available(x+2,y) and state.available(x+1,y):
                possile_actions.append(GamePlay.down)
            if state.available(x,y-2) and state.available(x,y-1):
                possile_actions.append(GamePlay.left)
            if state.available(x,y+2) and state.available(x,y+1):
                possile_actions.append(GamePlay.right)

        elif state.lying():        
            x0,y0,x1,y1 = state.cur
            if y0 == y1: #column_lying
                if state.available(x0-1,y0) and self.board[x0-1,y0] != self.CELL_TYPE_MAP['fragile']:
                    possile_actions.append(GamePlay.up)
                if state.available(x1+1,y0) and self.board[x1+1,y0] != self.CELL_TYPE_MAP['fragile']:
                    possile_actions.append(GamePlay.down)
                if state.available(x0,y0-1) and state.available(x1,y1-1):
                    possile_actions.append(GamePlay.left)
                if state.available(x0,y0+1) and state.available(x1,y1+1):
                    possile_actions.append(GamePlay.right)
                
            else:
                if state.available(x0-1,y0) and state.available(x1-1,y1):
                    possile_actions.append(GamePlay.up)
                if state.available(x0+1,y0) and state.available(x1+1,y1):
                    possile_actions.append(GamePlay.down)
                if state.available(x0,y0-1) and self.board[x0,y0-1] != self.CELL_TYPE_MAP['fragile']:
                    possile_actions.append(GamePlay.left)
                if state.available(x0,y1+1) and self.board[x0,y1+1] != self.CELL_TYPE_MAP['fragile']:
                    possile_actions.append(GamePlay.right)
                

        else:  # block is splited
            x,y,_,_ = state.cur
            possile_actions.append(GamePlay.switch)
            if state.available(x-1,y):
                possile_actions.append(GamePlay.up)
            if state.available(x+1,y):
                possile_actions.append(GamePlay.down)
            if state.available(x,y-1):
                possile_actions.append(GamePlay.left)
            if state.available(x,y+1):
                possile_actions.append(GamePlay.right)
            
        return possile_actions

    def _move_block(self, state:State, action):
        if state.standing(): 
            x,y = state.cur
            if action == GamePlay.up:
                state.cur = [x-2,y,x-1,y]
            elif action == GamePlay.down:
                state.cur = [x+1,y,x+2,y]
            elif action == GamePlay.left:
                state.cur = [x,y-2,x,y-1]
            elif action == GamePlay.right:
                state.cur = [x,y+1,x,y+2]
        elif state.lying():        
            x0,y0,x1,y1 = state.cur
            if y0 == y1: #column
                if action == GamePlay.up:
                    state.cur = [x0-1,y0]
                elif action == GamePlay.down:
                    state.cur = [x1+1,y0]
                elif action == GamePlay.left:
                    state.cur = [x0,y0-1,x1,y1-1]
                elif action == GamePlay.right:
                    state.cur = [x0,y0+1,x1,y1+1]   
            else:
                if action == GamePlay.up:
                    state.cur = [x0-1,y0,x1-1,y1]
                elif action == GamePlay.down:
                    state.cur = [x0+1,y0,x1+1,y1]
                elif action == GamePlay.left:
                    state.cur = [x0,y0-1]
                elif action == GamePlay.right:
                    state.cur = [x0,y1+1]
        else:  #Truong hop Block Da Split :V 
            x0,y0,x1,y1 = state.cur
            if action == GamePlay.up:
                state.cur = [x0-1,y0,x1,y1]
            elif action == GamePlay.down:
                state.cur = [x0+1,y0,x1,y1]
            elif action == GamePlay.left:
                state.cur = [x0,y0-1,x1,y1]
            elif action == GamePlay.right:
                state.cur = [x0,y0+1,x1,y1]
            if not state.splited():
                #Trong truong hop khi chung hop nhat lai voi nhau
                x0,y0,x1,y1 = state.cur
                state.cur = [min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)]
                

    def ActivateO_Button(self, x, y, state:State):
        if self.board[x,y] != self.CELL_TYPE_MAP['o_btn']: return
        for tx,ty,trigger_type in self.btn_target_map[(x,y)]:
            if trigger_type == self.TRIGGER_OF_MAP['hide']:
                state.board_state[tx,ty] = False
            elif trigger_type == self.TRIGGER_OF_MAP['unhide']:
                state.board_state[tx,ty] = True
            elif trigger_type == self.TRIGGER_OF_MAP['toggle']:
                state.board_state[tx,ty] ^= True
        
    def ActivateX_Button(self, x, y, state:State):
        if self.board[x,y] != self.CELL_TYPE_MAP['x_btn']: return

        for tx,ty,trigger_type in self.btn_target_map[(x,y)]:
            if trigger_type == self.TRIGGER_OF_MAP['hide']:
                state.board_state[tx,ty] = False
            elif trigger_type == self.TRIGGER_OF_MAP['unhide']:
                state.board_state[tx,ty] = True
            elif trigger_type == self.TRIGGER_OF_MAP['toggle']:
                state.board_state[tx,ty] ^= True #Dao bit lai khi nhan lai tung lan

    def ActivateSplit_Button(self, x, y, state:State):
        #Truong hop buoc vao o split 
        #Neu Khi Khong c
        if self.board[x,y] != self.CELL_TYPE_MAP['split_btn']: return
        state.cur = self.btn_target_map[(x,y)][0] + self.btn_target_map[(x,y)][1]

    def _trigger_button(self, state):
        if state.standing():
            x,y = state.cur
            self.ActivateO_Button(x, y, state)
            self.ActivateX_Button(x, y, state)
            self.ActivateSplit_Button(x, y, state)
        elif state.lying():
            x0,y0,x1,y1 = state.cur
            self.ActivateO_Button(x0, y0, state)
            self.ActivateO_Button(x1, y1, state)
        else: # split state
            x,y,_,_ = state.cur
            self.ActivateO_Button(x, y, state)

    def playing(self, state:State, action, inplace=False):
        if not inplace:
            state = copy.deepcopy(state)

        if action == GamePlay.switch:
            if state.splited():
                state.cur = state.cur[2:]+state.cur[:2]
        else:
            is_split_state = state.splited()
            self._move_block(state, action)
            if not is_split_state or state.splited():
                self._trigger_button(state)

        if not inplace:
            return state
    
    def possible_move(self, state:State, action, inplace=False):
        if action in self.get_possible_actions(state):
            return True,self.playing(state, action, inplace)
        return False,None

    @staticmethod
    def calculate_distance(x,y):
        #Using mahhattan Distance
        return abs(x[0]-y[0]) + abs(x[1]-y[1]) 
    
if __name__ == '__main__':
    p1 = Blozorx(2)
    # p2 = Blozorx(2)
    # print(p1.do_action(p1.init_state,'UP',inplace=False) == p2.init_state)
    p1 = State([1,2],[3,4],{})
    print(p1.standing())
    print(GamePlay.take_action_set())
    print(GamePlay.opposite_action(GamePlay.up, GamePlay.down))