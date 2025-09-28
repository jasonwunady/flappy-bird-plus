# Flappy Bird Plus

A feature-rich Python implementation of the classic Flappy Bird game built with Pygame, featuring multiple difficulty modes, customizable skins, particle effects, and a shop system.

## Features

- **Multiple Difficulty Modes**: Easy, Normal, and Hard with different pipe gaps and speeds
- **Customizable Bird Skins**: Unlock and use different bird appearances including default, blue, red, and golden
- **Background Themes**: Customizable background options
- **Particle Effects**: Visual effects to enhance gameplay
- **Shop System**: Earn coins and purchase new skins, backgrounds, and power-ups
- **High Score Tracking**: Individual high scores saved for each difficulty level
- **Save System**: Persistent game data including scores, coins, and unlocked items

## Installation

1. Ensure you have Python 3.x installed
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Clone this repository:
   ```bash
   git clone <repository-url>
   cd flappy-bird-plus
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. **Controls**:
   - Press `SPACE` or click to make the bird flap
   - Navigate menus with mouse clicks
   - Press `ESC` to return to previous screens

3. **Game Modes**:
   - **Easy**: Larger pipe gaps, slower speed
   - **Normal**: Standard gameplay
   - **Hard**: Smaller gaps, faster speed

4. **Shop System**:
   - Earn coins by playing the game
   - Visit the shop to purchase new bird skins, backgrounds, and particle effects
   - Customize your gameplay experience

## Game Structure

- `main.py` - Main game loop and core gameplay logic
- `bird.py` - Bird class with physics and animation
- `pipe.py` - Pipe obstacles management
- `particles.py` - Particle effect system
- `constants.py` - Game constants and configuration
- `assets/` - Game sprites and visual assets
- `sounds/` - Audio files
- `fonts/` - Custom fonts
- `save_data.json` - Persistent game data
- `high_score.json` - High score storage

## Game States

The game includes several states:
- **Home Screen**: Main menu with play and shop options
- **Playing**: Active gameplay
- **Game Over**: Score display and restart options
- **Shop**: Purchase new items and customize appearance
- **Background Shop**: Select background themes
- **Power Shop**: Purchase power-ups
- **Particles Shop**: Choose particle effects

## Data Persistence

Game progress is automatically saved, including:
- High scores for each difficulty level
- Collected coins
- Owned and equipped skins/backgrounds/particles
- Current customization settings

## Asset Creation

The project includes several utility scripts for asset generation:
- `create_assets.py` / `create_assets_new.py` - Generate game sprites
- `create_font.py` - Create custom fonts
- `create_sounds.py` / `create_sounds_new.py` - Generate audio assets
- `create_skins.py` - Create bird skin variations

## Requirements

- Python 3.x
- Pygame

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Enjoy playing Flappy Bird Plus!