import pandas as pd
import matplotlib.pyplot as plt

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--train_fname', type=str)
	parser.add_argument('--out_fname', type=str)
	args = parser.parse_args()

	reward_col = 'Reward (avg over previous 100 iters)'

	logged_info = pd.read_csv(args.train_fname)
	columns = list(logged_info.columns)
	columns[2] = reward_col
	logged_info.columns = columns
	logged_info[reward_col].iloc[::1000].plot(y=reward_col, kind='line', title='Averaged Reward over Training Iterations')
	plt.savefig(args.out_fname)

if __name__=='__main__':
	main()
