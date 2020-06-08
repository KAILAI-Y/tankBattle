# 游戏业务（面向对象的思想分析游戏）
# 坦克大战
#     主逻辑类：
#
#     坦克类：（我方坦克，敌方坦克）
#
#     子弹类：
#
#     爆炸类：
#
#     音效类：
import pygame
_display = pygame.display


class MainGame():
    __SCREEN_WIDTH = 800
    __SCREEN_HEIGHT = 600
    # 窗口对象
    __window = None

    # 开始游戏
    def startGame(self):
        pygame.display.init()
        # 加载游戏窗口
        MainGame.__window = _display.set_mode([MainGame.__SCREEN_WIDTH, MainGame.__SCREEN_HEIGHT])
        # 设置游戏标题
        _display.set_caption("坦克大站v1.0")
        while True:
            MainGame.__window.fill(pygame.Color(0, 0, 0))
            # 刷新屏幕
            _display.update()

    def gameOver(self):
        exit()


class Tank():
    pass


class MyTank(Tank):
    pass


class EnemyTank(Tank):
    pass


class Bullet():
    pass


class Explode():
    pass


class Music():
    pass


game = MainGame()
game.startGame()