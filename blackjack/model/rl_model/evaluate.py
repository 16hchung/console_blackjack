import gym
from tqdm import tqdm
import random

from ..player import Action

def loop_game_count_wins(params_fname, n_hands, use_rand):
	env = gym.make('Blackjack-v1', params_fname=params_fname)
	n_wins = 0
	for _ in tqdm(range(n_hands)):
		reward = 0
		done = False
		while reward == 0 and done == False:
			if use_rand:
				action = Action(random.randint(0,1)+1)
			else:
				action = env.player.action()
			_, reward, done, _ = env.step(action)
		if reward > 0:
			n_wins += 1
		if done:
			env.reset()
	return n_wins

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--params_fname', type=str, default='params_state_dict.pkl')
	parser.add_argument('--n_hands', type=int, default=10000)
	parser.add_argument('--baseline', action='store_true')
	args = parser.parse_args()

	n_wins = loop_game_count_wins(args.params_fname, args.n_hands, args.baseline)
	print('Won {0:} / {1:} hands: {2:.3f}%'.format(n_wins, args.n_hands, n_wins/args.n_hands*100))

if __name__=='__main__':
	main()
