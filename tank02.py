
"""
v1.2 新增：
1.实现左上角剩余敌方坦克提示
    a.选一个字体
    b.使用指定的字体绘制文字
    c.将小画布贴到窗口中
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
        _display.set_caption("坦克大战v1.2")
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
