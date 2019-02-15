# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:45:00 2019

@author: marble_xu
"""
import pygame
from pygame.locals import *
from sys import exit
from random import randint
from config import *
from gameRole import *
from resource import *

# display information like score, bomb number		
class ScreenInfo():
	def __init__(self, bomb_surface, plane_surface):
		self.score = 0
		self.bomb_surface = bomb_surface
		self.plane_surface = plane_surface
		self.latest_score = 0
		
	def addScore(self, score):
		self.score += score
		self.latest_score += score
		
	def getScore(self):
		return self.score
	
	def shouldCreateGift(self):
		if self.latest_score > 20000:
			self.latest_score -= 20000
			return True
		return False
		
	def displayInfo(self, screen, game_over, bomb_num, plane_life):
		def displayScore(screen, score):
			score_font = pygame.font.Font(None, 36)
			score_text = score_font.render(str(score), True, (128,128,128))
			text_rect = score_text.get_rect()
			text_rect.topleft = [SCREEN_WIDTH//2-35, 10]
			screen.blit(score_text, text_rect)
			
		displayScore(screen, self.score)
		if not game_over:
			bomb_rect = self.bomb_surface.get_rect()
			bomb_rect.topleft = [10, 0]
			screen.blit(self.bomb_surface, bomb_rect)
			
			bomb_font = pygame.font.Font(None, 36)
			bomb_text = bomb_font.render(" : "+str(bomb_num), True, (128,128,128))
			text_rect = bomb_text.get_rect()
			text_rect.topleft = [30, 10]
			screen.blit(bomb_text, text_rect)
			
			for i in range(plane_life):
				plane_rect = self.plane_surface.get_rect()
				plane_rect.topleft = [SCREEN_WIDTH - 120 + (i * 40), 0]
				screen.blit(self.plane_surface, plane_rect)

class Game():
	def __init__(self, caption, hero, screen_info):
		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pygame.display.set_caption(caption)
		self.hero = hero
		self.clock = pygame.time.Clock()
		self.screen_info = screen_info
		self.ticks = 0
		self.pause = False
	
	# create a new enemy if match condition
	def createEnemy(self, enemy_groups, ticks, score):
		# limit enemy2 and enemy3 numbers
		def getEnemyIndex(enemy_groups, enemy_range):
			index = randint(0, enemy_range)
			if index == 2:
				if len(enemy_groups[index].group) > 0:
					index = 0
			elif index == 1:
				if len(enemy_groups[index].group) > 2:
					index = 0
			return index
			
		if ticks % CREATE_CYCLE == 0:
			if score < 10000:
				enemy_range = 0
			elif score < 20000:
				enemy_range = 1
			else:
				enemy_range = 2
			
			index = getEnemyIndex(enemy_groups, enemy_range)
			enemy_groups[index].createEnemy()
	
	# create a new gift if match condition
	def createGift(self, gift_groups, ticks, screen_info):
		if ticks % CREATE_CYCLE == 0 and screen_info.shouldCreateGift():
			score = screen_info.getScore()
			if score < 20000:
				gift_range = 0
			elif score < 40000:
				gift_range = 1
			else:
				gift_range = 1
				
			gift_size = 0
			for group in gift_groups:
				gift_size += len(group.group)
			if gift_size == 0:
				if self.hero.bomb_num >= 3:
					index = randint(1, gift_range)
				else:
					index = randint(0, gift_range)
				gift_groups[index].createGift()

	def play(self, enemy_groups, gift_groups):
		def checkBulletCollide(enemy_group, bullets_group, screen, ticks):
			score = 0
			for group in enemy_group:
				for bullet_group in bullets_group:
					score += group.checkBulletCollide(bullet_group, screen, ticks) 
			return score

		def checkHeroCollide(hero, enemy_group):
			collide = False
			for group in enemy_group:
				if group.checkHeroCollide(hero):
					collide = True
					break;
			return collide
		
		self.clock.tick(FRAME_RATE)
		self.screen.blit(background, (0,0))
		
		if self.ticks >= FRAME_RATE:
			self.ticks = 0
			
		self.hero.play()
		
		self.createEnemy(enemy_groups, self.ticks, self.screen_info.getScore())
		self.createGift(gift_groups, self.ticks, self.screen_info)
		
		self.screen_info.addScore(checkBulletCollide(enemy_groups, self.hero.weapon_groups, self.screen, self.ticks))
		
		if checkHeroCollide(self.hero, enemy_groups):
			if self.hero.isHeroCrash():
				game_over_sound.play()
		
		for gift_group in gift_groups:
			gift_group.checkHeroCollide(self.hero)

		for weapon_group in self.hero.weapon_groups:
			weapon_group.draw(self.screen)
			
		for enemy_group in enemy_groups:
			enemy_group.update()
			enemy_group.draw(self.screen)

		for gift_group in gift_groups:
			gift_group.update()
			gift_group.draw(self.screen)
			
		self.screen.blit(self.hero.image, self.hero.rect)
		self.ticks += 1
		
		self.screen_info.displayInfo(self.screen, 0, self.hero.bomb_num, self.hero.life)
	
	def isGameOver(self):
		if self.hero.down_index >= len(self.hero.down_surface):
			if self.hero.life <= 0:
				return 1
			else:
				self.hero.restart()
		return 0

	def showGameOver(self):
		self.screen.blit(gameover, (0,0))
		self.screen_info.displayInfo(self.screen, 1, self.hero.bomb_num, self.hero.life)
		
	def setPause(self):
		self.pause = not self.pause
		
	def isPause(self):
		return self.pause


offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}

pygame.init()

(background, gameover, game_over_sound, bomb_surface, plane_surface) = initGame()
screen_info = ScreenInfo(bomb_surface, plane_surface)
myGame = Game('Air Craft Shooter!', initHero(), screen_info)
enemy_groups = initEnemyGroups()
gift_groups = initGiftGroups()

while True:
	if myGame.isGameOver():
		myGame.showGameOver()
	elif not myGame.isPause():
		myGame.play(enemy_groups, gift_groups)
		
	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# get keyboard input
		if event.type == pygame.KEYDOWN:
			if event.key in offset:
				offset[event.key] = 3
			elif event.key == pygame.K_SPACE:
				myGame.hero.useBomb()
			# press z to pause or resume game
			elif event.key == pygame.K_z:
				myGame.setPause()
		elif event.type == pygame.KEYUP:
			if event.key in offset:
				offset[event.key] = 0

	if not myGame.hero.is_hit:
		myGame.hero.move(offset)
		
