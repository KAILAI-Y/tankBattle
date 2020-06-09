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
"""
新增：
1. 解决点击关闭按钮， 程序未响应bug
2. 事件处理， 方向键控制，发射按键控制
"""
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
        _display.set_caption("坦克大战v1.1")
        while True:
            # 渲染背景
            MainGame.__window.fill(pygame.Color(0, 0, 255))

            # 调用事件处理的方法
            self.getEvent()

            # 刷新屏幕
            _display.update()

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
                elif event.key == pygame.K_RIGHT:
                    print("向右移动")
                elif event.key == pygame.K_UP:
                    print("向上移动")
                elif event.key == pygame.K_DOWN:
                    print("向下移动")
                elif event.key == pygame.K_SPACE:
                    print("攻击")

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
