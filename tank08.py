"""
v1.8 新增功能：
    1. 完善子弹类
    2. 我方坦克中新增射击方法（射击之后，产生子弹）
"""

import pygame, time, random

_display = pygame.display
version = "V1.8"


class MainGame():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    # 窗口对象
    window = None
    P1_TANK = None
    # 敌方坦克列表， 用来存储所有的敌方坦克
    enemy_tank_list = []
    enemy_tank_count = 5

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
            MainGame.window.blit(self.drawText('剩余敌方坦克%d辆' % 5), (5, 5))
            # 加载我方坦克
            MainGame.P1_TANK.display_tank()
            # 遍历敌方坦克加入到窗口中
            for eTank in MainGame.enemy_tank_list:
                eTank.display_enemy_tank()
                # 移动方式更新
                eTank.random_move()
            # 调用我方坦克的移动方法
            if not MainGame.P1_TANK.stop:
                MainGame.P1_TANK.move()
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

            # 按键松开事件处理
            if event.type == pygame.KEYUP:
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
            'R': pygame.image.load('img/p1tankR.gif'),
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5

        # stop变量， 用来控制坦克是否应该移动的开关
        self.stop = True

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


class MyTank(Tank):
    pass


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 图片集
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif'),
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

    def display_enemy_tank(self):
        # 重新设置图片
        self.image = self.images[self.direction]
        # 将坦克加入到窗口中
        MainGame.window.blit(self.image, self.rect)
        # super().display_tank()


class Bullet(BaseItem):
    pass


class Explode():
    pass


class Music():
    pass


game = MainGame()
game.startGame()
# game.drawText('a')