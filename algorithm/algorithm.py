import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection

from Bloxoz import Blozorx, State
from algorithm.bfs import breath_first_search
from algorithm.dfs import depth_first_search
from algorithm.a_search import a_search

"""'MONTECARLO': monte_carlo_search """
class Algorithm:
    Algorithm_For_Game={
        'DFS':depth_first_search,
        'BFS':breath_first_search,
        'A*': a_search,
    }
    def __init__(self,algorithm):
        self.algo = algorithm
        self.algorithm_using= self.Algorithm_For_Game[algorithm]
    
    def running(self, game:Blozorx, state:State = None, sender:Connection = None):
        return self.algorithm_using(game,state,sender)

if __name__ == '__main__':
    #DFS
    with open('results/dfs.txt','w') as f:
         for level in range(33):
            try:
                f.write(f'\n----Level {level+1:02d}----\n')
                game = Blozorx(level+1)
                explore_node_num, path, exe_time_s = Algorithm('DFS').running(game)
                print(f'Level {level+1:02d} {int(exe_time_s*1000)}ms')
                f.write(f'Explored: {explore_node_num} nodes\n')
                if path is not None:
                    f.write(f'Step num: {len(path)}\n')
                    f.write(f'Step : {"-".join(path)}\n')
                else:
                    f.write(f'NO SOLUTION FOUND!\n')
                f.write(f'Time : {int(exe_time_s*1000)}ms\n')
            except:
                f.write('ERROR!\n')
    #BFS
    """ with open('results/bfs.txt','w') as f:
         for level in range(33):
            try:
                f.write(f'\n----Level {level+1:02d}----\n')
                game = Blozorx(level+1)
                explore_node_num, path, exe_time_s = Algorithm('BFS').running(game)
                print(f'Level {level+1:02d} {int(exe_time_s*1000)}ms')
                f.write(f'Explored: {explore_node_num} nodes\n')
                if path is not None:
                    f.write(f'Step num: {len(path)}\n')
                    f.write(f'Step : {"-".join(path)}\n')
                else:
                    f.write(f'NO SOLUTION FOUND!\n')
                f.write(f'Time : {int(exe_time_s*1000)}ms\n')
            except:
                f.write('ERROR!\n') """
    #A
    """ with open('results/a.txt','w') as f:
        for level in range(33):
            try:
                f.write(f'\n----Level {level+1:02d}----\n')
                game = Blozorx(level+1)
                explore_node_num, path, exe_time_s = Algorithm('A*').running(game)
                print(f'Level {level+1:02d} {int(exe_time_s*1000)}ms')
                f.write(f'Explored: {explore_node_num} nodes\n')
                if path is not None:
                    f.write(f'Step num: {len(path)}\n')
                    f.write(f'Step : {"-".join(path)}\n')
                else:
                    f.write(f'NO SOLUTION FOUND!\n')
                f.write(f'Time : {int(exe_time_s*1000)}ms\n') 
            except:
                f.write('ERROR!\n') """