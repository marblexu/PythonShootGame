# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:45:00 2019

@author: marble_xu
"""
import pygame
from random import randint
from enum import Enum
from config import *

class GameGift(Enum):
	Bomb = 0
	PowerBullet = 1
	Laser = 2

class BulletType(Enum):
	OneWay = 0
	TwoWay = 1
	ThreeWay = 2

class EnemyType(Enum):
	EnemyType1 = 1
	EnemyType2 = 2
	EnemyType3 = 3


bullet_type = [BulletType.OneWay, BulletType.TwoWay, BulletType.ThreeWay]

class Weapon(pygame.sprite.Sprite):
	def __init__(self, weapon_surface, weapon_init_pos, direction):
		pygame.sprite.Sprite.__init__(self)
		self.image = weapon_surface
		self.rect = self.image.get_rect()
		self.rect.topleft = weapon_init_pos
		self.direction = direction
	
	def update(self):
		#direction[0]:x , direction[1]:y
		if self.direction[0] == 0:
			self.rect.y += self.direction[1]
			if self.direction[1] > 0:				
				if self.rect.y > SCREEN_HEIGHT:
					self.kill()				
			else:
				if self.rect.y < -self.rect.height:
					self.kill()
		else:
			self.rect.x += self.direction[0]
			if self.direction[0] > 0:
				if self.rect.x > SCREEN_WIDTH:
					self.kill()	
			else:
				if self.rect.x < -self.rect.width:
					self.kill()
				
class Enemy(pygame.sprite.Sprite):
	def __init__(self, enemy_surface, enemy_init_pos, direction, weapon_group):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_surface
		self.rect = self.image.get_rect()
		self.rect.topleft = enemy_init_pos
		self.direction = direction
		self.down_index = 0
		self.damage = 0
		self.is_down = 0
		self.is_hit = 0
		self.ticks = 0
		self.weapon_group = weapon_group

	def update(self, enemy_surface, hit_surface=0):
		def shootWeapon(weapon_group, position, direction):
			weapon_group.shootWeapon(position, direction)
			
		#direction[0]:x , direction[1]:y
		should_kill = False
		self.rect.x += self.direction[0]
		self.rect.y += self.direction[1]
		if self.rect.x > SCREEN_WIDTH or self.rect.x < -self.image.get_width():
			should_kill = True
		if self.rect.y > SCREEN_HEIGHT or self.rect.y < -self.image.get_height():
			should_kill = True
				
		if should_kill:
			self.kill()
		else:
			if len(enemy_surface) >= 2:
				if self.ticks >= ENEMY_SHOOT_CYCLE:
					self.ticks = 0
				
				if self.is_hit:
					self.is_hit -= 1
					self.image = hit_surface
				else:
					self.image = enemy_surface[self.ticks//(ENEMY_SHOOT_CYCLE//2)]
			
			self.ticks += 1
			if self.weapon_group is not None:
				if self.ticks % ENEMY_SHOOT_CYCLE == 0:
					shootWeapon(self.weapon_group, [self.rect.centerx, self.rect.y + self.image.get_height()], [0, ENEMY_SHOOT_SPEED])

class Gift(pygame.sprite.Sprite):
	def __init__(self, gift_surface, gift_init_pos, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = gift_surface
		self.rect = self.image.get_rect()
		self.rect.topleft = gift_init_pos
		self.speed = speed

	def update(self):	
		self.rect.top += self.speed
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()
	
class Hero(pygame.sprite.Sprite):
	def __init__(self, hero_surface, hero_down_surface, hero_init_pos, weapon_groups, life):
		pygame.sprite.Sprite.__init__(self)
		self.surface = hero_surface
		self.down_surface = hero_down_surface
		self.image = hero_surface[0]
		self.rect = self.image.get_rect()
		self.rect.topleft = hero_init_pos
		self.hero_init_pos = hero_init_pos
		self.weapon_groups = weapon_groups
		self.life = life
		self.reset()
		
	def reset(self):
		self.ticks = 0
		self.is_hit = False
		self.down_index = 0
		self.bullet_type_index = 0
		self.bomb_num = 0
		self.use_bomb = 0
		self.immune_ticks = 0
		
	def move(self, offset):
		x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
		y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
		if x < 0:
			self.rect.left = 0
		elif x > SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH - self.rect.width
		else:
			self.rect.left = x
		
		if y < 0:
			self.rect.top = 0
		elif y > SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT - self.rect.height
		else:
			self.rect.top = y	
	
	def useBomb(self):
		if self.bomb_num:
			self.use_bomb = 1
	
	def getBombNum(self):
		return self.bomb_num
	
	def addGift(self, type):
		if type == GameGift.Bomb:
			self.bomb_num += 3
		elif type == GameGift.PowerBullet:
			self.bullet_type_index = self.bullet_type_index + 1 if self.bullet_type_index < (len(bullet_type)-1) else self.bullet_type_index
		#elif type == GameGift.Laser:
	
	def isHeroCrash(self):
		if self.immune_ticks <= 0 and not self.is_hit:
			self.is_hit = True
			self.life -= 1
			return 1
		else:
			return 0
		
	def restart(self):
		self.reset()
		self.immune_ticks = 180
		self.rect.topleft = self.hero_init_pos
		
	def play(self):
		def getBulletPosition(rect, position_type):
			if position_type == 0:
				return [rect.centerx - 3, rect.centery]
			elif position_type == 1:
				return [rect.x + 10, rect.centery]
			else:
				return [rect.x + rect.width - 20, rect.centery]
		
		def shootWeapon(type, rect, weapon_groups):
			weapon_index = 0
			weapon_direction = [[0, -SHOOT_SPEED],[-SHOOT_SPEED, 0], [SHOOT_SPEED, 0]]
			if type == BulletType.OneWay:
				weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 0), weapon_direction[0])
			elif type == BulletType.TwoWay:
				weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 1), weapon_direction[0])
				weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 2), weapon_direction[0])
			elif type == BulletType.ThreeWay:
				weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 0), weapon_direction[0])
				weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 1), weapon_direction[0])
				weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 2), weapon_direction[0])
				
		if self.immune_ticks > 0:
			self.immune_ticks -= 1
		if not self.is_hit:
			if self.use_bomb:
				self.use_bomb = 0
				if self.bomb_num > 0:
					self.bomb_num -= 1
					self.weapon_groups[2].shootWeapon(self.rect.midtop, [0, -SHOOT_SPEED])
			elif self.ticks % SHOOT_CYCLE == 0:
				shootWeapon(bullet_type[self.bullet_type_index], self.rect, self.weapon_groups)
					
		for weapon_group in self.weapon_groups:
			weapon_group.update()

		if self.ticks >= ANIMATE_CYCLE:
			self.ticks = 0
		if self.is_hit:
			assert self.down_index < len(self.down_surface)
			self.image = self.down_surface[self.down_index]
			if self.ticks % (ANIMATE_CYCLE//2) == 0:
				self.down_index += 1
		else:
			self.image = self.surface[self.ticks//(ANIMATE_CYCLE//2)]
		self.ticks += 1

class EnemyGroup():
	def __init__(self, surface, hit_surface, down_surface, down_sound, score, health, speed, enemy_type, weapon_group):
		self.surface = surface
		self.hit_surface = hit_surface
		self.down_surface = down_surface
		self.group = pygame.sprite.Group()
		self.down_group = pygame.sprite.Group()
		self.down_sound = down_sound
		self.score = score
		self.health = health
		self.speed = speed
		self.enemy_type = enemy_type
		self.weapon_group = weapon_group
	
	def createEnemy(self):
		def getDirection(surface, speed, enemy_type):
			if enemy_type == EnemyType.EnemyType3:
				enemy_init_pos = [randint(0, SCREEN_WIDTH - surface.get_width()), -surface.get_height()]
				direction = [0, speed]
			else:
				# enemy can appear from top side, left side,  and right side
				appearSide = randint(0, 2)
				if appearSide == 0: # from top side
					enemy_init_pos = [randint(0, SCREEN_WIDTH - surface.get_width()), -surface.get_height()]
					direction = [0, speed]
				elif appearSide == 1: # from left side
					enemy_init_pos = [-surface.get_width(), randint(0, (ENEMY_APPEAR_HEIGHT - surface.get_height()))]
					direction = [randint(1, speed), randint(1, speed)]
				elif appearSide == 2: # from right side
					enemy_init_pos = [SCREEN_WIDTH, randint(0, (ENEMY_APPEAR_HEIGHT - surface.get_height()))]
					direction = [randint(-speed, -1), randint(1, speed)]
			return (enemy_init_pos, direction)
		
		(enemy_init_pos, direction)	= getDirection(self.surface[0], self.speed, self.enemy_type)
		enemy = Enemy(self.surface[0], enemy_init_pos, direction, self.weapon_group)
		self.group.add(enemy)
		
	def update(self):
		self.group.update(self.surface, self.hit_surface)
		if self.weapon_group is not None:
			self.weapon_group.update()
	
	def draw(self, screen):
		self.group.draw(screen)
		if self.weapon_group is not None:
			self.weapon_group.draw(screen)
	
	def checkBulletCollide(self, bullets, screen, ticks):
		score = 0
		self.down_group.add(pygame.sprite.groupcollide(self.group, bullets.group, False, True))
		for enemy_down in self.down_group:
			if enemy_down.is_down:
				screen.blit(self.down_surface[enemy_down.down_index], enemy_down.rect)
				if ticks % (ANIMATE_CYCLE//2) == 0:
					if enemy_down.down_index < (len(self.down_surface)-1):
						if enemy_down.down_index == 0:
							self.down_sound.play()
						enemy_down.down_index += 1
					else:
						self.down_group.remove(enemy_down)
						score += self.score
			else:
				enemy_down.damage += bullets.damage
				enemy_down.is_hit = 8
				if enemy_down.damage >= self.health:
					enemy_down.is_down = 1
					self.group.remove(enemy_down)
				else:
					self.down_group.remove(enemy_down)
		return score

	def checkHeroCollide(self, hero):
		enemy_down_list = pygame.sprite.spritecollide(hero, self.group, False)
		collide = False
		if len(enemy_down_list) > 0:
			for enemy_down in enemy_down_list:
				if pygame.sprite.collide_circle_ratio(0.7)(enemy_down, hero):
					self.group.remove(enemy_down)
					self.down_group.add(enemy_down)
					enemy_down.is_down = 1
					collide = True
		
		if not collide and self.weapon_group is not None:
			bullet_hit_list = pygame.sprite.spritecollide(hero, self.weapon_group.group, False)
			if len(bullet_hit_list) > 0:
				for bullet_hit in bullet_hit_list:
					if pygame.sprite.collide_circle_ratio(0.7)(bullet_hit, hero):
						self.weapon_group.group.remove(bullet_hit)
						collide = True
			
		return collide

class GiftGroup():
	def __init__(self, surface, gift_sound, speed, type):
		self.surface = surface
		self.group = pygame.sprite.Group()
		self.gift_sound = gift_sound
		self.speed = speed
		self.type = type
		
	def update(self):
		self.group.update()

	def draw(self, screen):
		self.group.draw(screen)
		
	def createGift(self):
		gift = Gift(self.surface, [randint(0, SCREEN_WIDTH - self.surface.get_width()), -self.surface.get_height()], self.speed)
		self.group.add(gift)
	
	def checkHeroCollide(self, hero):
		gift_hit_list = pygame.sprite.spritecollide(hero, self.group, False)
		if len(gift_hit_list) > 0:
			for gift in gift_hit_list:
				if pygame.sprite.collide_circle_ratio(0.8)(gift, hero):
					self.group.remove(gift)
					self.gift_sound.play()
					hero.addGift(self.type)
					
class WeaponGroup():
	def __init__(self, weapon_surface, weapon_sound, damage):
		self.surface = weapon_surface
		self.group = pygame.sprite.Group()
		self.weapon_sound = weapon_sound
		self.damage = damage
	
	def shootWeapon(self, position, direction):
		weapon = Weapon(self.surface, position, direction)
		self.group.add(weapon)
		self.weapon_sound.play()

	def update(self):
		self.group.update()
	
	def draw(self, screen):
		self.group.draw(screen)

class EnemyWeaponGroup():
	def __init__(self, weapon_surface, weapon_sound, damage):
		self.surface = weapon_surface
		self.group = pygame.sprite.Group()
		self.weapon_sound = weapon_sound
		self.damage = damage
	
	def shootWeapon(self, position, direction):
		assert (direction[0] != 0) or (direction[1] != 0)
		weapon = Weapon(self.surface, position, direction)
		self.group.add(weapon)
		self.weapon_sound.play()

	def update(self):
		self.group.update()
	
	def draw(self, screen):
		self.group.draw(screen)
