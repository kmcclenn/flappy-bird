from game_funcs import Game
import datetime
from tqdm import tqdm

policy = lambda info: ((datetime.datetime.now() - datetime.datetime.fromtimestamp(info[7])).total_seconds()*1000) % 1000 < 20
alwaysFalse = lambda info: False

game = Game(policy=policy)

rollout = game.get_rollout()
print(rollout)

# game.run()
