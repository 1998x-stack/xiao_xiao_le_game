# config.py

"""
Configuration settings for the 消消乐 game.
"""

# Screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 800

# Grid settings
TILE_SIZE: int = 80
GRID_SIZE: int = SCREEN_WIDTH // TILE_SIZE

# Tile types (using color names for now, but can be expanded to other shapes or symbols)
TILES = ["red", "green", "blue", "yellow", "purple"]

# Scoring
MATCH_SCORE: int = 10
BONUS_SCORE: int = 50  # Bonus score for special tiles or long combos

# Target score to win
TARGET_SCORE: int = 1000

# Asset paths
ASSET_PATH: str = "assets/"
IMAGE_PATH: str = ASSET_PATH + "images/"
SOUND_PATH: str = ASSET_PATH + "sounds/"

# Sound files
BACKGROUND_MUSIC: str = SOUND_PATH + "background.mp3"
MATCH_SOUND: str = SOUND_PATH + "match.wav"
WIN_SOUND: str = SOUND_PATH + "win.wav"

MAX_MOVES: int = 20  # Limit the number of moves for each game