# EchoLocation

**EchoLocation** is a minimalistic 2D top-down horror-stealth game built with Python and Pygame. You are trapped in total darkness and must navigate using sound pulses to reveal your environment, avoid "Hearer" predators, and find the key to escape.

## 🛠 Features

*   **Acoustic Navigation:** The world is pitch black. You must send out pulses that briefly reveal walls, enemies, and objectives.
*   **State-Based Predator AI:** Enemies (Hearers) patrol the darkness and will pivot to hunting mode if they "hear" your pulses or see you within a specific radius.
*   **Data-Driven Level Design:** Levels are parsed from simple `.txt` files, allowing for easy expansion and map creation.
*   **Objective-Based Gameplay:** Players must locate a hidden key before the exit gate (Goal) will unlock.

## 🚀 Getting Started

### Prerequisites
*   Python 3.10 or higher
*   Pygame library

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/karbeto/EchoLocation.git
    cd echo-location

2. **Install dependencies:**
    ```bash
    pip install pygame

### Running the Game

Launch the game by executing the `main.py` file from the root directory:
    ```bash
    python main.py


# 🎮 How to Play

* **Pulse (Echolocation)**: Press the Spacebar to emit a sound pulse. This reveals your surroundings but alerts nearby enemies to your exact position
* **Move:** Use the Arrow Keys or WASD to navigate through the darkness.

* **The Objective:**

1. Explore the map to find the **Gold Key (K).**
2. Once acquired, the UI will update to **"KEY: ACQUIRED".**
3. Reach the **Exit (G)** to advance to the next level.
**Avoid the Hearers:** If an enemy touches you, the game is over. Watch their movement patterns to sneak past.


# 📁 Project Structure
    echo-location/
    ├── main.py            # Entry point and Game State Manager
    ├── levels/            # Directory containing .txt map files
    │   ├── level1.txt
    │   └── level2.txt
    └── src/               # Source code
        ├── settings.py    # Game constants (colors, speeds, states)
        ├── player.py      # Player logic and pulse mechanics
        ├── enemy.py       # Predator AI and FSM (Finite State Machine)
        └── level.py       # Map parsing and rendering logic


# 📝 Level Creation
You can design your own levels in the **levels/** folder using the following characters:

**W**: Wall

**P**: Player Spawn

**E**: Enemy Spawn

**K**: Key

**G**: Goal (Exit)

**.**: Empty Space