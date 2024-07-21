from game_funcs import Game
import datetime
from tqdm import tqdm

policy = lambda info: ((datetime.datetime.now() - info["start_time"]).total_seconds()*1000) % 1000 < 20
alwaysFalse = lambda info: False

game = Game(policy=None)

# rollout = game.get_rollout()

game.run()
