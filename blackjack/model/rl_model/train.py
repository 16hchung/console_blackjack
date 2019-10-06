import gym
import math
import random
import pandas as pd
from itertools import count
from collections import namedtuple

import torch
import torch.optim as optim
import torch.nn.functional as F

from .decider import DQN
from ..player import Action

BURN_PERIOD = 50000
BATCH_SIZE = 128*4
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 5

Transition = namedtuple('Transition',
	('state', 'action', 'next_state', 'reward')
)

class ReplayMemory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.memory = []
		self.position = 0

	def push(self, *args):
		"""Saves a transition."""
		if len(self.memory) < self.capacity:
			self.memory.append(None)
		self.memory[self.position] = Transition(*args)
		self.position = (self.position + 1) % self.capacity

	def sample(self, batch_size):
		return random.sample(self.memory, batch_size)

	def __len__(self):
		return len(self.memory)

class TrainLogger:
	def __init__(self, info_keys, log_freq=100):
		self.all_info = pd.DataFrame(columns=info_keys  + ['iter'])
		self.iter = 0
		self.log_freq = log_freq

	def log(self, info):
		try:
			info['iter'] = self.iter
			self.all_info = self.all_info.append(info, ignore_index=True)
			self.iter += 1
			if self.iter % self.log_freq == 0:
				print(info)
		except:
			pass

	def plot(self, col_names):
		pass

	def finish(self, fname):
		try:
			self.all_info.to_csv('indv_'+fname)
			moving_avged = self.all_info.rolling(window=100, min_periods=1).mean()
			moving_avged.to_csv('avged_'+fname)
		except:
			pass

def select_action(state, device, policy_net, env, steps_done):
	n_actions = env.action_space.n
	sample = random.random()
	steps_done = max(0, steps_done - BURN_PERIOD)
	eps_threshold = EPS_END + (EPS_START - EPS_END) * \
		math.exp(-1. * steps_done / EPS_DECAY)
	if sample > eps_threshold and steps_done > 0:
		with torch.no_grad():
			return policy_net(state).max(0)[1].view(1, 1), False
	else:
		return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long), True

def optimize_model(policy_net, target_net, optimizer, memory, device):
	if len(memory) < BATCH_SIZE:
		return None
	transitions = memory.sample(BATCH_SIZE)
	batch = Transition(*zip(*transitions))

	# Compute a mask of non-final states and concatenate the batch elements
	non_final_mask = torch.tensor(tuple(
		map(lambda s: s is not None, batch.next_state)),
		device=device, 
		dtype=torch.uint8
	).bool()
	non_final_next_states = torch.stack(
		[s for s in batch.next_state if s is not None]
	)
	state_batch = torch.stack(batch.state)
	action_batch = torch.cat(batch.action)
	reward_batch = torch.cat(batch.reward)

	# Compute Q(s_t, a) 
	state_action_values = policy_net(state_batch).gather(1, action_batch)

	# Compute V(s_{t+1}) for all next states.
	next_state_values = torch.zeros(BATCH_SIZE, device=device)
	next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
	# Compute the expected Q values
	expected_state_action_values = (next_state_values * GAMMA) + reward_batch

	# Compute Huber loss
	loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

	# Optimize the model
	optimizer.zero_grad()
	loss.backward()
	for param in policy_net.parameters():
		param.grad.data.clamp_(-1, 1)
	optimizer.step()
	return loss.item()

def train(num_episodes, out_params_file, log_file):
	env = gym.make('Blackjack-v1')
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	policy_net = DQN().to(device).float()
	policy_net.train()
	target_net = DQN().to(device).float()

	target_net.load_state_dict(policy_net.state_dict())
	target_net.eval()

	#optimizer = optim.RMSprop(policy_net.parameters(), lr=.00001, weight_decay=.001)
	optimizer = optim.Adam(policy_net.parameters(), lr=.001, weight_decay=.01)
	memory = ReplayMemory(20000)

	info_keys = env.info_keys + ['reward', 'action']
	logger = TrainLogger(info_keys)

	steps_done = 0
	loss = None
	for i_episode in range(num_episodes):
		# Init environment and state
		state = torch.from_numpy(env.reset()).float().to(device)
		for t in count():
			# Select and perform action
			step_outpts = []
			reward = 0; done = False
			orig_state = state
			while reward == 0 and not done:
				action, was_rand = select_action(state, device, policy_net, env, steps_done)
				action_e = Action(action.item()+1)
				step_outpt = env.step(action_e)
				[next_state, reward, done, _] = step_outpt
				step_outpts.append(step_outpt)
				state = torch.from_numpy(next_state).float().to(device)
				steps_done += 1

			reward = step_outpts[-1][1] # if hit and don't bust, use ultimate outcome as reward
			reward_t = torch.tensor([reward], device=device).float()
			state = orig_state
			for [next_state, _, done, info] in step_outpts:
				# Log info for plotting
				more_info = {
					'action': action.item(),
					'reward': reward,
					'rand_action': was_rand
				}
				# Turn output to tensors
				next_state = torch.from_numpy(next_state).float().to(device)
				if done: next_state = None

				# Store transition in memory
				memory.push(state, action, next_state, reward_t)

				# Move to next state
				state = next_state

				more_info['loss'] = loss
				info.update(more_info)
				logger.log(info)
			if done:
				loss = optimize_model(policy_net, target_net, optimizer, memory, device)
				break
		# Update target network
		if i_episode % TARGET_UPDATE == 0:
			target_net.load_state_dict(policy_net.state_dict())

	torch.save(policy_net.state_dict(), out_params_file)
	logger.finish(log_file)

if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--n_eps', type=int, default=10000)
	parser.add_argument('--out_params', default='params_state_dict.pkl')
	parser.add_argument('--log_file', default='train_log.csv')
	args = parser.parse_args()

	import time
	start = time.time()
	train(args.n_eps, args.out_params, args.log_file)
	print('finished in {} minutes'.format((time.time() - start) / 60))
	# TODO: save parameters



