import pygame
import random
import numpy as np
import bullet
from enemy import *
from myplane import *
from supply import *

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, player_pos, enemy_positions, bullet_positions):
        return (player_pos, tuple(enemy_positions), tuple(bullet_positions))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon or state not in self.q_table:
            return random.choice(self.actions)
        else:
            return max(self.q_table[state], key=self.q_table[state].get)

    def learn(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in self.actions}
        
        q_predict = self.q_table[state][action]
        q_target = reward + self.gamma * max(self.q_table[next_state].values())
        self.q_table[state][action] += self.alpha * (q_target - q_predict)

# 初始化游戏
pygame.init()
bg_size = (480, 700)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Plane Battle")

# 定义玩家、敌人、子弹和智能体
player = MyPlane(bg_size)
enemies = pygame.sprite.Group(SmallEnemy(bg_size), MidEnemy(bg_size), BigEnemy(bg_size))
bullets = pygame.sprite.Group()
actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
agent = QLearningAgent(actions)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取当前状态
    player_position = (player.rect.left, player.rect.top)
    enemy_positions = [(enemy.rect.left, enemy.rect.top) for enemy in enemies]
    bullet_positions = [(bullet.rect.left, bullet.rect.top) for bullet in bullets]
    state = agent.get_state(player_position, enemy_positions, bullet_positions)

    # 选择动作
    action = agent.choose_action(state)
    if action == 'UP':
        player.moveUp()
    elif action == 'DOWN':
        player.moveDown()
    elif action == 'LEFT':
        player.moveLeft()
    elif action == 'RIGHT':
        player.moveRight()

    # 更新游戏状态
    for enemy in enemies:
        enemy.move()
    for bullet in bullets:
        bullet.move()

    # 碰撞检测和奖励计算
    reward = 0
    if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
        reward -= 1  # 撞击敌人扣分

    # 获取下一个状态
    next_player_position = (player.rect.left, player.rect.top)
    next_enemy_positions = [(enemy.rect.left, enemy.rect.top) for enemy in enemies]
    next_bullet_positions = [(bullet.rect.left, bullet.rect.top) for bullet in bullets]
    next_state = agent.get_state(next_player_position, next_enemy_positions, next_bullet_positions)

    # 学习
    agent.learn(state, action, reward, next_state)

    # 绘制游戏元素
    screen.fill((0, 0, 0))
    screen.blit(player.image1, player.rect)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
