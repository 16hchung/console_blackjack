'''
submodule using RL to choose action, using following tutorial as template:
https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
'''

from gym.envs.registration import register

register(
	id='Blackjack-v1',
	entry_point='blackjack.model.rl_model.gym_env:BlackjackEnv',
)
