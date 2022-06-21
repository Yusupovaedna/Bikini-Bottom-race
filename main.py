from game import game_loop
from input import run_neuro_cycle as run_neuro_cycle1
from inputL import run_neuro_cycle as run_neuro_cycle2
import time

if __name__ == '__main__':
    time.sleep(0.1)
    # run_neuro_cycle1()
    time.sleep(0.1)
    run_neuro_cycle2()
    # time.sleep(3)
    game_loop()