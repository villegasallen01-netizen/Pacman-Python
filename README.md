# Pac-Man Python Game Engine

A full 2D arcade Pac-Man clone built from scratch in Python using Pygame. Features real-time game loops, tile-map collision detection, ghost AI pathfinding, and procedurally synthesized retro audio.

## Features
- **Ghost AI:** Implements dynamic targeting and frightened state movement using Euclidean distance formulas (`math.hypot`).
- **Retro Sound Synthesizer:** Generates pure audio sound effects (waka-waka, power pellets, ghost consumption) on the fly using Pygame sound buffers—no external `.wav` or `.mp3` files required!
- **Object-Oriented Design:** Clean OOP structure separating game loop management, Pac-Man player state, ghost behaviors, and maze rendering.
- **Classic Gameplay:** Complete with 28x31 tile maze grid matrix, score tracking, lives, warp tunnels, and pulsing power pellets.

## Tech Stack
- **Language:** Python 3
- **Library:** Pygame
- **Concepts:** Object-Oriented Programming (OOP), Discrete Mathematics, Tile-Map Collision Algorithms

## How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/villegasallen01-netizen/Pacman-Python.git](https://github.com/villegasallen01-netizen/Pacman-Python.git)
   cd Pacman-Python
