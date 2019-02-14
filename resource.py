# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:45:00 2019

@author: marble_xu
"""
import pygame
from gameRole import *


shoot_img =  pygame.image.load('resource/image/shoot.png')

def initWeaponGroups():
	weapon_groups = []
	bullet1_surface = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))
	bullet_sound = pygame.mixer.Sound('resource/sound/bullet.wav')
	bullet_sound.set_volume(0.3)
	weapon_groups.append(WeaponGroup(bullet1_surface, bullet_sound, 1))
	
	bullet2_surface = shoot_img.subsurface(pygame.Rect(69, 78, 9, 21))
	weapon_groups.append(WeaponGroup(bullet2_surface, bullet_sound, 2))
	
	bomb_surface = shoot_img.subsurface(pygame.Rect(828, 691, 28, 57))
	bomb_sound = pygame.mixer.Sound('resource/sound/use_bomb.wav')
	bomb_sound.set_volume(0.3)
	weapon_groups.append(WeaponGroup(bomb_surface, bomb_sound, 9))
	
	return weapon_groups


def initHero():
	hero_surface = []
	hero_surface.append(shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)))
	hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)))

	hero_down_surface = []
	hero_down_surface.append(shoot_img.subsurface(pygame.Rect(165, 234, 102, 126)))
	hero_down_surface.append(shoot_img.subsurface(pygame.Rect(330, 624, 102, 126)))
	hero_down_surface.append(shoot_img.subsurface(pygame.Rect(330, 498, 102, 126)))
	hero_down_surface.append(shoot_img.subsurface(pygame.Rect(432, 624, 102, 126)))
	hero_pos = [200, 500]

	return Hero(hero_surface, hero_down_surface, hero_pos, initWeaponGroups(), 3)


def initEnemyGroups():
	enemy_groups = []
	enemy1_surface = []
	enemy1_surface.append(shoot_img.subsurface(pygame.Rect(534, 612, 57, 43)))
	enemy1_hit_surface = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))
	enemy1_down_surface = []
	enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
	enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
	enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
	enemy1_down_surface.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))
	enemy1_down_sound = pygame.mixer.Sound('resource/sound/enemy1_down.wav')
	enemy1_down_sound.set_volume(0.3)
	enemy_groups.append(EnemyGroup(enemy1_surface, enemy1_hit_surface, enemy1_down_surface, enemy1_down_sound, 1000, 1, 3))
	
	enemy2_surface = []
	enemy2_surface.append(shoot_img.subsurface(pygame.Rect(0, 0, 69, 99)))
	enemy2_hit_surface = shoot_img.subsurface(pygame.Rect(432, 525, 69, 99))
	enemy2_down_surface = []
	enemy2_down_surface.append(shoot_img.subsurface(pygame.Rect(534, 655, 69, 95)))
	enemy2_down_surface.append(shoot_img.subsurface(pygame.Rect(603, 655, 69, 95)))
	enemy2_down_surface.append(shoot_img.subsurface(pygame.Rect(672, 653, 69, 95)))
	enemy2_down_surface.append(shoot_img.subsurface(pygame.Rect(741, 653, 69, 95)))
	enemy2_down_sound = pygame.mixer.Sound('resource/sound/enemy2_down.wav')
	enemy2_down_sound.set_volume(0.3)
	enemy_groups.append(EnemyGroup(enemy2_surface, enemy2_hit_surface, enemy2_down_surface, enemy2_down_sound, 3000, 3, 2))
	
	enemy3_surface = []
	enemy3_surface.append(shoot_img.subsurface(pygame.Rect(335, 750, 169, 258)))
	enemy3_surface.append(shoot_img.subsurface(pygame.Rect(504, 750, 169, 258)))
	enemy3_hit_surface = shoot_img.subsurface(pygame.Rect(166, 750, 169, 258))
	enemy3_down_surface = []
	enemy3_down_surface.append(shoot_img.subsurface(pygame.Rect(0, 486, 165, 261)))
	enemy3_down_surface.append(shoot_img.subsurface(pygame.Rect(0, 255, 165, 261)))
	enemy3_down_surface.append(shoot_img.subsurface(pygame.Rect(839, 748, 165, 260)))
	enemy3_down_surface.append(shoot_img.subsurface(pygame.Rect(165, 486, 165, 261)))
	enemy3_down_surface.append(shoot_img.subsurface(pygame.Rect(673, 748, 166, 260)))
	enemy3_down_surface.append(shoot_img.subsurface(pygame.Rect(0, 747, 166, 261)))
	enemy3_down_sound = pygame.mixer.Sound('resource/sound/enemy3_down.wav')
	enemy3_down_sound.set_volume(0.3)
	enemy_groups.append(EnemyGroup(enemy3_surface, enemy3_hit_surface, enemy3_down_surface, enemy3_down_sound, 9000, 12, 1))
	
	return enemy_groups


def initGiftGroups():
	gift_groups = []
	gift1_surface = shoot_img.subsurface(pygame.Rect(101, 120, 60, 104))
	gift1_sound = pygame.mixer.Sound('resource/sound/get_bomb.wav')
	gift1_sound.set_volume(0.3)
	gift_groups.append(GiftGroup(gift1_surface, gift1_sound, 1, GameGift.Bomb))
	
	gift2_surface = shoot_img.subsurface(pygame.Rect(265, 400, 60, 85))
	gift_groups.append(GiftGroup(gift2_surface, gift1_sound, 1, GameGift.PowerBullet))
	
	return gift_groups


def initGame():
	pygame.mixer.music.load('resource/sound/game_music.wav')
	pygame.mixer.music.play(-1, 0.0)
	pygame.mixer.music.set_volume(0.2)

	background = pygame.image.load('resource/image/background.png')
	gameover = pygame.image.load('resource/image/gameover.png')

	game_over_sound = pygame.mixer.Sound('resource/sound/game_over.wav')
	game_over_sound.set_volume(0.3)	
	
	bomb_surface = pygame.transform.scale(shoot_img.subsurface(pygame.Rect(828, 691, 28, 57)), (19,40))
	plane_surface = pygame.transform.scale(shoot_img.subsurface(pygame.Rect(5, 99, 96, 96)), (36,36))
	return (background, gameover, game_over_sound, bomb_surface, plane_surface)
