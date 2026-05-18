# 🦇 EchoLocation

**EchoLocation** is a high-performance, minimalistic 2D top-down horror-stealth game built with Python and Pygame. Trapped in a world of absolute pitch blackness, you possess no natural sight. You must rely entirely on acoustic sonar rings to map out your surroundings, avoid lethal blind predators, and hunt for the path to safety.

---

## 🛠 Advanced Features

* **Acoustic Radar Masking:** The entire world is covered by a hardware-accelerated dark mask using custom alpha-blending math (`pygame.BLEND_MULT`). Emitting a sound wave physically burns visibility holes into the dark, revealing walls, objects, and threats frame-by-frame.
* **Echo Trails (Visual Memory System):** Illuminated structural layouts do not instantly disappear. Walls fade through stepped alpha intervals, leaving a faint, decaying cyan "ghost trace" radar outline that stays visible for several seconds to allow for active path planning.
* **Sonic Wave-Surfing Mechanic:** Timing is everything. Stepping exactly onto the expanding crest of your own sound pulse grants a snappy **50% momentum velocity boost**. Master the rhythm to sprint through narrow corridors and escape tight corners.
* **Acoustic Chime Walls:** Interacting with specialized Chime Walls causes them to ripple and emit localized ambient sound vectors when struck by a sonar wave. This provides strategic auditory landmarks or distraction points to misdirect hunting predators.
* **State-Throttled Enemy:** "Hearer" predators track targets using physical sound-vector listening. The code enforces state-guard overrides and audio cooldown thresholds to make sure enemies hunt seamlessly across map boundaries without overloading audio buffers.
* **Data-Driven Architecture:** Maps are read, tokenized, and parsed directly from simple plaintext matrix configurations (`.txt` files), supporting complex custom layouts, mechanical chime walls, and progressive layouts.
* **Procedural Maze Generation:** Levels can transition into infinitely scaling, runtime-generated structural challenges via a recursive backtracker matrix algorithm, augmenting the static file parser for endless replayability.

---

## 🎮 Game Controls & Objectives

### Controls
* **`SPACEBAR`** — Emit Sonar Pulse (Reveals the maze but alerts nearby Hearers to your origin coordinates)
* **`W` / `A` / `S` / `D`** — Move (Stepping in sync with an active pulse edge triggers the **Sonic Wave-Surf Boost**)

### The Mission Vector
1. **Ping the Dark:** Send out echo waves to read the architecture around you.
2. **Secure the Objective:** Navigate the maze to locate the **Neon Gold Key**.
3. **Ride the Wave:** Dodge or outrun the blind predators patrolling the corridors.
4. **Breach the Perimeter:** Reach the **Green Exit Gate** with the key in your inventory to advance to the next floor.

---

## 🚀 Installation & Launch

### System Requirements
* Python 3.10 or higher
* Pygame 2.x

### Deployment Steps
1. **Clone the repository architecture:**
   ```bash
   git clone https://github.com/karbeto/EchoLocation.git
   cd echo-location
   ```

2. **Install the dependencies:**
   ```bash
   pip install pygame
   ```

3. **Initialize the engine loop:**
   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```text
echo-location/
├── main.py              # Engine core, clock ticking, event distribution, and app state loop
├── requirements.txt     # List of external Python dependencies (pygame)
├── assets/
│   └── audio/           # Sound repository (.wav and .flac channels)
│
├── levels/              # Plaintext structural layout configurations
│   ├── level1.txt       
│   ├── level2.txt       
│   └── level3.txt  
│  
└── src/               
    ├── __init__.py      # Marks directory as a regular Python package
    ├── audio_manager.py # Controls multi-channel mixers, sound effects, and spatial volumes
    ├── camera.py        # Vector translation offset tracking relative to player position
    ├── enemy.py         # Hearing state machines, listening math, and pathing velocity
    ├── game_renderer.py # Blend-multiplied surface masks, fade overlays, and layer blitting
    ├── level.py         # Map layout parsing, wall group grouping, and tile coordinate maps
    ├── maze_generator.py# Procedural layout generator for continuous/infinite level mapping
    ├── player.py        # Physics mechanics, input tracking, and Soundwave emission vectors
    ├── settings.py      # Core architectural constants (Colors, FPS, Audio configurations)
    ├── shop.py          # Upgrade modifier states (Radius improvements, cooldown scaling)
    ├── ui_renderer.py   # HUD layers, overlay drawings for menus, shop windows, and victory frames
    └── utils.py         # Auxiliary calculation assets (Pulse tracking classes, dimensions)
```

---

## 📝 Custom Level Blueprint Creation

You can engineer custom level profiles directly inside the `levels/` folder by modifying or creating `.txt` matrices. Use the following design tokens to construct your grid map:

* `W` — **Solid Wall** (Impassable blocking collider)
* `C` — **Chime Wall** (Acoustic resonance barrier that rings when pinged)
* `P` — **Player Spawn Point** (Initial player frame placement coordinates)
* `E` — **Enemy Spawn Point** (Initial Hearer entity patrol placement coordinates)
* `K` — **The Neon Gold Key** (Required to clear exit validation flags)
* `G` — **The Exit Goal Gate** (Triggers level advancement if key validation passes)
* `.` — **Empty Corridors / Open Air Space**

*Every grid cell maps to an explicit index layout, making it entirely open-source and easy to customize.*
