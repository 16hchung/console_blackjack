# Console Blackjack (design document)
I've implemented a TUI for playing blackjack (where possible actions are either hit or stand). I also used deep Q-learning to train  along with an AI player (trained using deep Q-learning)
#### Results
My baseline is a dummy player who chose whether to hit or run randomly. This player has a win rate of ~29.9%.

My AI player after training had a win rate of ~43.2%.

## Usage
#### Requirements
Unix system, python3.6, anaconda, pip, pytorch 1.2, and cuda toolkit

#### Installing dependencies
After downloading the contents of this repository, cd into `console_blackjack/` and run the following:
```
$ conda env create --file environment.yaml python=3.6
```

#### Playing the game
Run the command below and follow the prompts listed. Note that your screen must have at least 50 rows and 100 columns.
```
$ python3 -m blackjack.play
```
Note: I did some basic user-testing with my siblings and friends on MacOS Sierra 10.14 and Ubuntu 16.04. In case the program doesn't behave properly, please watch `demo.mov` to see how the game is played.
 
## Design Choices
I'd never used reinforcement learning outside of a course problem set (which dealt with a discrete state space). As such, I wanted to try my hand at deep Q-learning. To mimic card counting strategies, I had my state space include not only the dealer card and properties of my hand, but also counts of low, medium, and high-valued cards normalized by shoe size. I used a simple Q-network with dropout so as to avoid overfitting, and trained using Adam optimization, which is better for cases with sparse rewards.

In terms of architecture, I used a model-view-controller structure, placing any curses-related code in `view/`, any gameplay or data-heavy code in `model/`, and any orchestrating code in `controller/`. My reinforcement-learning-related files (including the Q-network, training, and evaluation) were kept in `model/rl_model/`.

## Resources
#### External libraries
pytorch, numpy/pandas, openAI-gym, tqdm, curses, and matplotlib

#### Written resources
- Based training code off of this pytorch tutorial: https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
- Card ASCII art by ejm98: https://www.asciiart.eu/miscellaneous/playing-cards
- Ported much of code in `blackjack/view/` from previous card game: https://github.com/16hchung/egyptian_ratscrew
