# Huey Plays Go: implementing self-playing Go models. 

Motivations for this project: 
- Go's mechanics are extremely simple, but the state space of games is vast, making it a great application for ML.
- I got interested in Go a few months ago, and I'd like to track my own progress in terms of the size of models I can beat. ELO scores are one thing, but I think it would be cooler to know how many parameters my own neural net has. 


### Architecture

- Python class that handles representation of the game, making moves, and scoring boards. 
- Several "agents" that are trained and pickled to play against. 
- A Flask backend that exposes game logic and agent access over APIs
- A React frontend for playing games in a GUI. 

- A selfplay program, which generates games played between two agents
- A training program, which reads those games and uses them to train a model. 

The representation of the game, the state tensor, is the same one used in the AlphaGo model:

- One board state is a pair of matrices, one for each player, with 1s as placed stones.
- The next player to move comes first, meaning the pairs flip their order each time a move is placed. 
- The complete state tensor holds the last 7 historical moves, for 16 total frames. 
- A 17th frame holds all 1s if black is next to move, and all 0s if white is next to move. 

So, after a move is played, the current player's stones are on top, and needs to add a stone to the board represented by the two top matrices. 

```python
self.game = Go(GAME_SIZE)   # B0, W0
self.game.place_stone(3, 3) # W1, B1, W0, B0
self.game.place_stone(4, 4) # B2, W2, B1, W1, B0, W0
self.game.place_stone(5, 5) # W3, B3, W2, B2, W1, B1, W0, B0
```

### Model Performance
Times to think ahead, as measured on my M1 macbook pro: 

9x9 Random:     ~0.003s per move
9x9 Minmax1:    ~0.003s per move
9x9 Minmax2:    ~0.1 per move

So far, from very basic local tests, minmax2 > minmax 1 > random. This makes sense, since minmax models pick randomly when there's no better move in the visible tree; so random + minmax(N) models will likely linearly outperform eachother. 