import json
import numpy as num

class Level:
    def __init__(self, level):
        self.level= level
        self.runLevel(f'./level/{level}')
    
    def runLevel(self,path_level):
        with open(path_level,'r') as file_map:
            map_bloxoz = json.load(file_map)
        self.board = num.asarray(map_bloxoz.get('map'), dtype=bool)
        self.size_y, self.size_x = self.board.shape
        
        self.start = map_bloxoz.get('start')
        self.goal = map_bloxoz.get('end')

        tmp_board = num.asarray(map_bloxoz.get('map'), dtype=int)
        self.fragile_cells = [(r,c) for r,c in zip(*num.where(tmp_board == 2))]

        self.x_btn_list = map_bloxoz.get('x_btn_list')
        self.o_btn_list = map_bloxoz.get('o_btn_list')
        self.split_btn_list = map_bloxoz.get('split_btn_list')
    

if __name__ == '__main__':
    level = Level('level_15.json')
    print('Level',f'{level.level}')
    print('Start:',level.start)
    print('Goal :',level.goal)
    print('Fragile:',level.fragile_cells)
    print('X Button List:',level.x_btn_list)
    print('O Button List:',level.o_btn_list)    
    print('Split Btton List:',level.split_btn_list)
    print('Map:',level.board)