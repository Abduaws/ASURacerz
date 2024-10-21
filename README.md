# ASURacerz

## Overview
Welcome to the Car Racing Game! This project is a multiplayer car racing game developed using Pygame, featuring robust networking capabilities to ensure a smooth gaming experience. The game is designed to be played by multiple users, allowing them to race against each other in real-time. The architecture includes multiple servers for redundancy, ensuring that the game remains accessible and functional even in the event of server issues.

## Features
- **Multiplayer Gameplay**: Compete against friends or other players online.
- **Dynamic Game Environment**: Experience a vibrant racing atmosphere with various car models and obstacles.
- **Robust Networking**: The game utilizes socket.io for real-time communication between clients and servers, ensuring smooth gameplay.
- **Redundancy and Failover**: The architecture includes multiple servers to handle player connections and game state, providing fallback options in case of server failure.
- **Crash Handling**: The game includes a crash detection mechanism that resets player positions and notifies the server in case of collisions.
- **User -Friendly UI**: The game features a clean and intuitive user interface built using PyQt5, enhancing the overall user experience.

## Technologies Used
- **Pygame**: For rendering graphics and handling game mechanics.
- **Socket.IO**: For real-time communication between clients and servers.
- **PyQt5**: For creating the graphical user interface.
- **Python**: The primary programming language used for development.

## Installation
To set up the Car Racing Game on your local machine, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Abduaws/ASURacerz.git
   cd ASURacerz
   ```
2. **Install Dependencies**
   ```bash
   pip install pygame PyQt5 python-socketio requests
   ```
3. **Running Game**
   ```bash
   python main.py
   ```

## How to Play
1. **Launch the Game**: After running the game, you will be presented with a main menu.
2. **Enter Username**: Input your desired username to join the game.
3. **Select Cars**: Choose your car from the available options.
4. **Start the Game**: Once all players are ready, the game will begin.
5. **Controls**: Use the arrow keys to navigate your car. Avoid obstacles and try to reach the finish line first!

## Server Architecture
The game architecture consists of multiple servers to handle player connections and game state. The primary server handles the main game logic, while backup servers are available to take over in case of failures. This redundancy ensures that players can continue their gaming experience without interruptions.

### Connection Handling
- The game attempts to connect to the main server first. If the connection fails, it automatically switches to a backup server.
- Players are notified of their connection status and any changes in server availability.

## Youtube Demo Video
https://www.youtube.com/watch?v=KurSgbvI47Q
