# AI Agent for *Game of Thrones: Hand of the King*

## Overview

This project implements an AI agent to play *Hand of the King*, leveraging **MiniMax with Alpha-Beta pruning** and a **learning-based approach** for improved decision-making. We built upon the repository [Hand-of-the-King](https://github.com/Mohammad-Momeni/Hand-of-the-King), enhancing it with AI techniques.

![Screenshot from 2025-02-08 15-20-10](https://github.com/user-attachments/assets/5e30fcda-8390-4516-86f4-ccb5f0522918)


The project consists of two phases:
1. **Phase 1:** Implementing the MiniMax algorithm with Alpha-Beta pruning and heuristic evaluation.
2. **Phase 2:** Training the AI to refine its strategy dynamically.

## Features and Approach

### Phase 1: MiniMax with Alpha-Beta Pruning

- **MiniMax Algorithm:**  
  - The agent simulates **all possible scenarios**, assuming an optimal opponent.
  - Given the game’s branching factor (up to 35 initial moves), searching the entire game tree is infeasible.
  - To **optimize performance**, we employ **Alpha-Beta pruning** to eliminate unnecessary calculations.

- **Time-Constrained Search:**  
  - If the algorithm exceeds **10 seconds**, it returns the best move based on **heuristic evaluation**.
  - Some branches are **searched to depth 6**, while others **extend to depth 7** based on time availability.

- **Heuristic Function:**  
  - The evaluation function scores board states based on:
    - **Captured banners** (higher score for more banners).
    - **House control** (owning more than half of a house’s cards ensures its banner).
    - **Opponent restriction** (limiting the opponent’s moves improves evaluation).

- **MiniMax Implementation (Key Logic):**  
  - Generates **valid moves** and recursively simulates game states.
  - Uses **Alpha-Beta pruning** to improve efficiency.
  - Returns the **best move** based on the evaluation function.

### Phase 2: Training for Improved Decision-Making (Reinforcement Learning-Inspired Approach)

- **Dynamic Weight Adjustment:**  
  - If the agent **wins**, it retains the weights and focuses on restricting the opponent.
  - If the agent **loses**, it increases the weights of houses it failed to control and decreases the weights of houses it dominated.

- **Reinforcement Learning (RL) Perspective:**  
  - The approach is **not a traditional RL model** but shares **policy improvement principles**.
  - The agent **learns from game outcomes**, adapting weights based on rewards and penalties.
  - Over multiple iterations, it **self-tunes** to optimize its decision-making.

- **Machine Learning-Inspired Techniques:**
  - Concepts from **Simulated Annealing**, **Genetic Algorithms**, and **Gradient Descent** were explored.
  - Since **Gradient Descent** requires a differentiable function (which the game lacks), a **genetic algorithm-like approach** was used.
  - The AI **starts with random weights** and refines them through gameplay.

- **Training and Optimization:**
  - The AI played against itself, refining its strategy over time.
  - **Initial weights were randomized**, and the `evaluate_fitness` function **ran 100 times** to optimize decisions.
  - After training, the agent won **80% of matches** against its untrained version.
  - It successfully **learned to win on 7-8 different board configurations**.

## Implementation Details

### Key Functions

#### `minimax()`
- Implements MiniMax with Alpha-Beta pruning, limiting depth based on execution time.

#### `right_minimax()`
- Evaluates all possible moves for **companion cards**, calling MiniMax to decide the best move.

#### `apply()`
- A helper function that applies a move to update the game state efficiently.

#### `evaluate_board()`
- The heuristic function that scores board states based on banners, house control, and opponent restriction.

#### `evaluate_fitness()`
- Determines the effectiveness of a given weight configuration.
- If successful across multiple games, it refines its approach.

### Data Storage
- Game results, including inputs and outputs, are logged for further training and analysis.

## Acknowledgments

This project was inspired by and extends the work of [Hand-of-the-King](https://github.com/Mohammad-Momeni/Hand-of-the-King).  
Special thanks to **Dr. Salimi Badr** for guidance in the **Fundamentals of AI course**.

## Team

**AI Rebels**  
- **Nila Chenari**  
- **Mehdi Rezaei**

## Usage

### Requirements

- Python 3.x
- Pygame (for game display)

You can clone the repository and set up the project by running:

```bash
git clone https://github.com/your-repo/Hand-of-the-King-AI.git
cd Hand-of-the-King-AI
pip install -r requirements.txt
```

### Running the Game
To run the game, use the following command line syntax:

```bash 
python main.py --player1 <player1_type> --player2 <player2_type> -l <load_file>
 ```

- `--player1`, `--player2` : Choose the players. Options:
  - `"human"`:  Play manually
  - `"<AI file>"`: Select a specific AI (e.g., rebel_agent, random_agent).
  - 
**Playing Manually**
```bash
python main.py --player1 rebel_agent --player2 human
```
