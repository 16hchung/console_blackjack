import gym
import math
import random
from itertools import count
from collections import namedtuple

import torch
import torch.optim as optim
import torch.nn.functional as F

from .decider import DQN

BATCH_SIZE = 128
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10

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
	def __init__(self):
		self.all_info = {}
		self.avgd_info = {}
		self.iters = 0

	def log(self, info):
		self.iters += 1

	def finish(self, fname):
		pass

def select_action(state, device, policy_net, env, steps_done):
	n_actions = env.action_space.n
	sample = random.random()
	eps_threshold = EPS_END + (EPS_START - EPS_END) * \
		math.exp(-1. * steps_done / EPS_DECAY)
	if sample > eps_threshold:
		with torch.no_grad():
			return policy_net(state).max(0)[1].view(1, 1)
	else:
		return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)

def optimize_model(policy_net, target_net, optimizer, memory, device):
	if len(memory) < BATCH_SIZE:
		return
	transitions = memory.sample(BATCH_SIZE)
	batch = Transition(*zip(*transitions))

	# Compute a mask of non-final states and concatenate the batch elements
	non_final_mask = torch.tensor(tuple(
		map(lambda s: s is not None, batch.next_state)),
		device=device, 
		dtype=torch.uint8
	)
	non_final_next_states = torch.cat(
		[s for s in batch.next_state if s is not None]
	)
	state_batch = torch.cat(batch.state)
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

def train(num_episodes):
	env = gym.make('Blackjack-v1')
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	policy_net = DQN().to(device).float()
	target_net = DQN().to(device).float()

	target_net.load_state_dict(policy_net.state_dict())
	target_net.eval()

	optimizer = optim.RMSprop(policy_net.parameters())
	memory = ReplayMemory(10000)

	steps_done = 0
	for i_episode in range(num_episodes):
		# Init environment and state
		state = torch.from_numpy(env.reset()).float().to(device)
		for t in count():
			# Select and perform action
			action = select_action(state, device, policy_net, env, steps_done)
			next_state, reward, done, info = env.step(action.item())
			reward = torch.tensor([reward], device=device).float()
			next_state = torch.from_numpy([next_state]).float().to(device)
			if done: next_state = None
			steps_done += 1

			# Store transition in memory
			memory.push(state, action, next_state, reward)

			# Move to next state
			state = next_state

			optimize_model(policy_net, target_net, optimizer, memory, device)
			if done:
				break
		# Update target network
		if i_episode % TARGET_UPDATE == 0:
			target_net.load_state_dict(policy_net.state_dict())

if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--n_eps', type=int, default=50)
	args = parser.parse_args()

	train(args.n_eps)


