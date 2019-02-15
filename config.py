# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:45:00 2019

@author: marble_xu
"""

# screen size 
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

FRAME_RATE = 60
# enemy or hero image change frequency of tick unit
ANIMATE_CYCLE = 30

######### Game Difficulty Setting #########

# enemy plane appear in y range (0, ENEMY_APPEAR_HEIGHT) when come from left or right side
# easy:SCREEN_HEIGHT//3, hard:SCREEN_HEIGHT//2, dead:(SCREEN_HEIGHT*2//3)
ENEMY_APPEAR_HEIGHT = (SCREEN_HEIGHT//3)

# create enemy and gift frequency of tick unit
# easy:60, hard:30
CREATE_CYCLE = 60

# hero shoot frequency of tick unit
# easy:10, hard:15, dead:30
SHOOT_CYCLE = 15
# easy <= 5, hard: (6,8)
SHOOT_SPEED = 8

# enemy shoot frequency of tick unit
# easy:120, hard:90, dead:60
ENEMY_SHOOT_CYCLE = 120
# ENEMY_SHOOT_SPEED easy:1, hard:2, dead = 3
ENEMY_SHOOT_SPEED = 2

######### End of Game Difficulty Setting #########