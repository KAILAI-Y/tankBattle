"""
v1.11 新增功能：
    1.优化主逻辑中业务代码
    2.新增我方子弹与敌方坦克的碰撞
        子弹新增方法 hit_tank()
"""

import pygame
import random
import time

_display = pygame.display
version = "V1.11"


class MainGame():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    # 窗口对象
    window = None
    P1_TANK = None
    # 敌方坦克列表， 用来存储所有的敌方坦克
    enemy_tank_list = []
    enemy_tank_count = 5

    # 新增存储敌方子弹的列表
    enemy_bullet_list = []

    # 新增我方子弹列表
    bullet_list = []

    # 开始游戏
    def startGame(self):
        pygame.display.init()
        # 加载游戏窗口
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 设置游戏标题
        _display.set_caption("坦克大战" + version)
        # 创建一个坦克
        MainGame.P1_TANK = Tank(375, 250)
        # 创建敌方坦克
        self.creatEnemyTank()
        while True:
            # 渲染背景
            MainGame.window.fill(pygame.Color(0, 0, 255))
            # 调用事件处理的方法
            self.getEvent()
            # 将带有文字的Surface绘制到窗口中
            MainGame.window.blit(self.drawText('剩余敌方坦克%d辆' % len(MainGame.enemy_tank_list)), (5, 5))
            # 调用展示我方坦克的方法
            self.show_P1_TANK()
            # 调用展示敌方坦克的方法
            self.show_enemy_tank()
            # 调用展示我方坦克的方法
            self.show_bullet()
            # 调用展示敌方坦克的方法
            self.show_enemey_bullet()


            # 刷新屏幕
            _display.update()
            # 主逻辑休眠
            time.sleep(0.01)

    # 新增创建敌方坦克的方法
    def creatEnemyTank(self):
        # 创建敌方坦克
        for i in range(MainGame.enemy_tank_count):
            random_left = random.randint(0, 8)
            random_speed = random.randint(5, 10)
            # 创建敌方坦克
            enemy_tank = EnemyTank(random_left*100, 150, random_speed)
            MainGame.enemy_tank_list.append(enemy_tank)

    # 优化我方坦克展示
    def show_P1_TANK(self):
        # 加载我方坦克
        MainGame.P1_TANK.display_tank()
        # 调用我方坦克的移动方法
        if not MainGame.P1_TANK.stop:
            MainGame.P1_TANK.move()

    # 优化敌方坦克展示
    def show_enemy_tank(self):
        # 遍历敌方坦克加入到窗口中
        for eTank in MainGame.enemy_tank_list:
            # 移动方式更新
            eTank.random_move()
            # 根绝live判断坦克是否应该渲染
            if eTank.live:
                eTank.display_enemy_tank()
            else:
                MainGame.enemy_tank_list.remove(eTank)
            # 敌方坦克调用射击方法
            eBullet = eTank.random_fire()
            # 在random_fire()返回值可能为None， 保证不是None再将子弹存储起来
            if eBullet:
                MainGame.enemy_bullet_list.append(eBullet)

    # 优化我方子弹展示
    def show_bullet(self):
        # 新增子弹在屏幕上完成绘制
        for bullet in MainGame.bullet_list:
            # 新增调用子弹移动
            bullet.bullet_move()
            if bullet.live:
                bullet.display_bullet()
                # 调用子弹碰撞方法
                bullet.hit_tank()
            else:
                # 删除子弹
                MainGame.bullet_list.remove(bullet)

    # 优化敌方子弹展示
    def show_enemey_bullet(self):
        # 新增敌方子弹的渲染
        for eBullet in MainGame.enemy_bullet_list:
            # 新增调用子弹移动
            eBullet.bullet_move()
            if eBullet.live:
                eBullet.display_bullet()
            else:
                # 删除子弹
                MainGame.enemy_bullet_list.remove(eBullet)

    # 事件处理方法
    def getEvent(self):
        # 获取所有事件
        eventList = pygame.event.get()
        for event in eventList:
            # type属性
            if event.type == pygame.QUIT:
                print("退出游戏")
                self.gameOver()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("向左移动")
                    MainGame.P1_TANK.direction = 'L'
                    # MainGame.P1_TANK.move()
                    # 坦克移动的开关控制
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_RIGHT:
                    print("向右移动")
                    MainGame.P1_TANK.direction = 'R'
                    # MainGame.P1_TANK.move()
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_UP:
                    print("向上移动")
                    MainGame.P1_TANK.direction = 'U'
                    # MainGame.P1_TANK.move()
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_DOWN:
                    print("向下移动")
                    MainGame.P1_TANK.direction = 'D'
                    # MainGame.P1_TANK.move()
                    MainGame.P1_TANK.stop = False
                elif event.key == pygame.K_SPACE:
                    print("攻击")
                    # 我方坦克发射子弹
                    # MainGame.P1_TANK.fire()
                    # 新增我方坦克发射子弹的数量控制
                    if len(MainGame.bullet_list) < 3:
                        bullet = MainGame.P1_TANK.fire()
                        MainGame.bullet_list.append(bullet)

            # 按键松开事件处理
            if event.type == pygame.KEYUP:
                # MainGame.P1_TANK.stop = True
                # 弹出的不是空格键再停止
                if event.key != pygame.K_SPACE:
                    MainGame.P1_TANK.stop = True

    # 给一个字符串，返回一个包含字符串内容的表面(surface)
    def drawText(self, content):
        # 字体模块初始化
        pygame.font.init()

        # 创建字体对象
        font = pygame.font.Font('FangZhengFangSongFanTi-1.ttf', 16)
        # fonts_list = pygame.font.get_fonts()
        # print(fonts_list)

        # 使用字体渲染内容
        text_sf = font.render(content, True, pygame.Color(0, 255, 0))

        # 返回包含内容的Surface
        return text_sf

    def gameOver(self):
        exit()


# 继承精灵类的类， 供其他类继承
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
    def __init__(self, left, top):
        self.images = {
            'U': pygame.image.load('img/p1tankU.gif'),
            'D': pygame.image.load('img/p1tankD.gif'),
            'L': pygame.image.load('img/p1tankL.gif'),
            'R': pygame.image.load('img/p1tankR.gif')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 10

        # stop变量， 用来控制坦克是否应该移动的开关
        self.stop = True
        # 新增属性live用来判断坦克是否还在
        self.live = True

    # 展示坦克
    def display_tank(self):
        # 设置坦克图片
        self.image = self.images[self.direction]
        # 将坦克加入到窗口中
        MainGame.window.blit(self.image, self.rect)

    # 坦克移动方向
    def move(self):
        # 修改tank的坐标：取决于坦克的方向
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - MainGame.P1_TANK.rect.height:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - MainGame.P1_TANK.rect.width:
                self.rect.left += self.speed

    # 新增射击方法
    def fire(self):
        # 创建子弹对象
        bullet = Bullet(self)
        # 加入到列表
        # MainGame.bullet_list.append(bullet)
        return bullet


class MyTank(Tank):
    pass


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 图片集
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }
        # 初始方向（随机）
        self.direction = self.random_direction()
        self.image = self.images[self.direction]
        # 坦克的图片
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = speed
        # stop变量， 用来控制坦克是否应该移动的开关
        self.stop = False

        # 步数控制
        self.step = 10
        self.live = True

    def random_direction(self):
        num = random.randint(1, 4)
        if num == 1:
            self.direction = 'U'
        elif num == 2:
            self.direction = 'D'
        elif num == 3:
            self.direction = 'L'
        elif num == 4:
            self.direction = 'R'
        return self.direction

    # 随机移动方法
    def random_move(self):
        if self.step == 0:
            self.random_direction()
            # 如果将step复位到10
            self.step = 10
        else:
            self.move()
            self.step -= 1

    # 新增随机射击方法
    def random_fire(self):
        num = random.randint(1, 50)
        if num < 3:
            eBullet = self.fire()
            return eBullet

    def display_enemy_tank(self):
        # 重新设置图片
        self.image = self.images[self.direction]
        # 将坦克加入到窗口中
        MainGame.window.blit(self.image, self.rect)
        # super().display_tank()


class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('img/bullet.gif')
        self.direction = tank.direction
        self.speed = MainGame.P1_TANK.speed * 1.5
        # self.rect = tank.rect
        self.rect = self.image.get_rect()
        # 子弹初始化位置要根据坦克的的方向进行调整
        if self.direction == 'U':
            self.rect.left += tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - tank.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        # 新增记录子弹是否碰撞到墙壁或者坦克
        self.live = True

    # 新增子弹的移动方法
    def bullet_move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False

    # 新增子弹与坦克的逻辑方法
    def hit_tank(self):
        for eTank in MainGame.enemy_tank_list:
            result = pygame.sprite.collide_rect(eTank, self)
            if result:
                self.live = False
                eTank.live = False

    # 将子弹加入到窗口中
    def display_bullet(self):
        MainGame.window.blit(self.image, self.rect)


class Explode():
    pass


class Music():
    pass


game = MainGame()
game.startGame()
