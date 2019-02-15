# PythonShootGame
A improved shoot game based on https://github.com/Kill-Console/PythonShootGame.
* add two types of enemy planes
* add two types of weapons (bomb, power bullet)
* improve plane collide check
* enemy plane can appear from left，right and top side
* enemy plane can shoot bullet
* provide config.py to modify game difficulty

# Introduce
This project only include four simple .py files:

* shooter.py: initialization and main loop of the game.
* gameRole.py: class of the game role and helper class to manage game role
* resource.py: image and music related initialization
* config.py: provide parameters to modify game difficulty

# Requirement
* Python 3.7
* Python-Pygame 1.9

# How To Start Game
$ python shooter.py

# How to Play
* use UP/DOWN/LEFT/RIGHT key to control plane
* use SPACE key to shoot bomb
* use z key to pause or resume game

# Demo
![screenshot](https://raw.githubusercontent.com/marblexu/PythonSimpleShoot/master/demo/screenshot1.png)
