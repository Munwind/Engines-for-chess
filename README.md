# Classic Heuristic Algorithms for chess AI

## Introduction
 Chess is made up of tactics and strategy. For tactics you calculate moves and replies and look
 if any of the move sequences leads to forced advantage or disadvantage. Essentially you search
 among all possible variations. For strategy you judge a position without too much calculation.

 Our engine will use classic heuristic algorithms like MinMax and Alpha-Beta pruning and some other methods to optimize engine's performance.

## Requirements
To use my code, you only need to have this in your device

* **python 3.11.5**
* **pygame 2.5.2**

## Algorithms
In this project, algorithms that we used for optimizing our engines
* **Minimax**
* **Alpha-Beta pruning**
* **Move Ordering**
* **Quiescence search**
* **Evaluate and Minimax for end game**

## How to use our code
You can install the required library by using the command below in the Command Prompt

`git clone https://github.com/Munwind/Engines-for-chess.git`

`pip install -q -r requirement.txt`

`python main.py`

## Note
* **To change to DEPTH of the board, you can access the file "ChessAI" and change the DEPTH at the line 3**
* **Make sure that you access the images folder in the file "main.py" in the line 19**
* **To play with the AI, in the file "main.py", in the line 37 you can change "humanPlayWhite = True" to play White**

## Future Improvements
* **Using neutral network to improve End Game's performance**
* **Introduce an evaluation bar to visually represent the advantages of both approaches.**
* **Offer the flexibility to choose between AI vs. AI, human vs. AI, and player vs. player (PvP) and difficuties modes within the program without needing to modify the source code.**

 

 
