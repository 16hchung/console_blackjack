# Console Blackjack (design document)
I've implemented a TUI for playing blackjack (where possible actions are either hit or stand). I also used deep Q-learning to train  along with an AI player (trained using deep Q-learning)

## Usage
### Requirements
Unix system, python3.6, anaconda, pip, pytorch 1.2, and cuda toolkit

### Installing dependencies
After downloading the contents of this repository, cd into `console_blackjack/` and run the following:
```
$ conda env create --file environment.yaml python=3.6
```

### Playing the game
Run the command below and follow the prompts listed. Note that your screen must have at least 50 rows and 100 columns.
```
$ python3 -m blackjack.play
```
Note: I did some basic user-testing with my siblings and friends on MacOS Sierra 10.14 and Ubuntu 16.04. In case the program doesn't behave properly, please watch `demo.mov` to see how the game is played.

## Design Choices
  

## Resources
### External libraries
pytorch, numpy/pandas, openAI-gym, tqdm, and matplotlib

### Written resources
- Based training code off of this pytorch tutorial: https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
- Card ASCII art by ejm98: https://www.asciiart.eu/miscellaneous/playing-cards
- Ported much of code in `blackjack/view/` from previous card game: https://github.com/16hchung/egyptian_ratscrew
