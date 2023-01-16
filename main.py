import pygame
import random
import os
import sys

# 一秒钟会更新60次画面
FPS = 60
# 窗口的宽度
WIDTH = 500
# 窗口的高度
HEIGHT = 600

# 窗口背景颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGERED = (255, 69, 0)
YELLOW = (255, 255, 0)
SKYBLUE = (0,191,255)
ORANGE = (255,218,185)
ROSE = (255,228,225)
PURPLE = (255,215,0)

# 游戏初始化
pygame.init()
# 初始化音效
pygame.mixer.init()
# 创建窗口，传入一个元组，画面的宽度和高度
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# 修改窗口标题
pygame.display.set_caption("拯救许晔晨")
# 创建一个物件，对时间进行管理和操控
clock = pygame.time.Clock()

# 加载图片
# os.path 代表现在python文件的位置
# .join会再往下去找img文件夹，再往下找background.png
# convert() 转换成pygame比较容易读取的格式
background_img1_trans = pygame.image.load(os.path.join("img", "xyc3.jpg")).convert()
background_img1 = pygame.transform.scale(background_img1_trans, (800, 600))
background_img2_trans = pygame.image.load(os.path.join("img", "xyc4.jpg")).convert()
background_img2 = pygame.transform.scale(background_img2_trans, (800, 600))
background_img3_trans = pygame.image.load(os.path.join("img", "xyc5.jpg")).convert()
background_img3 = pygame.transform.scale(background_img3_trans, (800, 600))
background_img4_trans = pygame.image.load(os.path.join("img", "xyc8.jpg")).convert()
background_img4 = pygame.transform.scale(background_img4_trans, (600, 800))
background_img5_trans = pygame.image.load(os.path.join("img", "xyc10.jpg")).convert()
background_img5 = pygame.transform.scale(background_img5_trans, (600, 800))
background_img6_trans = pygame.image.load(os.path.join("img", "xyc11.jpg")).convert()
background_img6 = pygame.transform.scale(background_img6_trans, (800, 600))
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
# 把飞船图片调小，用来显示生命条数
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
# 用一个列表存放载入的石头图片
rock_imgs = []
# 载入7张石头图片，放到rock_imgs列表中
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
# 用一个字典存储两种爆炸，大爆炸和小爆炸，和飞船的爆炸
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    # 引入大小爆炸照片
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    # 把黑色变透明
    expl_img.set_colorkey(BLACK)
    # 把图片的大小改变
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    # 引入飞船爆炸照片
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    # 把黑色变透明
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
# 存储宝物的字典
power_imgs = {}
# 盾牌
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
# 闪电
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()


# 加载音乐
# 引入射击声音
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
# 引入子弹吃到宝物的音效
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
# 引入死亡声音
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
# 爆炸的音效
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
# 背景音乐（要一直播放）所以引入方式有不同
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
# 调整背景音乐的音量
# 可传入一个参数，从0到1，代表声音的大小
pygame.mixer.music.set_volume(0.4)

# 引入微软正黑体
font_name = os.path.join("华文行楷.ttf")
# 把文字写到画面上的函数
# 第一个参数是要写到什么平面上
# 第二个参数是要写的文字
# 第三个参数是文字的大小
# 第四、五个参数是要写在哪里
def draw_text(surf, text, size, x, y, color):
    # 第一个参数是字体，第二个参数是文字的大小
    font = pygame.font.Font(font_name, size)
    # 把文字渲染出来
    # 第一个参数是文字，第二个参数是布尔值，要不要用anti_arials，第三个参数是文字的颜色
    text_surface = font.render(text, True, color)
    # 文字定位
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    # 画在传进来的平面上
    surf.blit(text_surface, text_rect)
# 加入新石头
def new_rock(round):
    rock = Rock()
    rock.speedy = random.randrange(round, 10 + round)
    all_sprites.add(rock)
    rocks.add(rock)
# 显示生命值
# 参数：画在什么平面，剩余血量，坐标
def draw_health(surf, hp, x, y):
    # 血量如果小于0，就设置成0
    if hp < 0:
        hp = 0
    # 生命条的长度和高度
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    # 把生命条填满多少
    fill = (hp / 100) * BAR_LENGTH
    # 生命条的外框
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    # 填满生命条的外框
    fill_rect = pygame.Rect(x, y, fill,BAR_HEIGHT)
    # 画外框，没有写第四个参数就会把它填满
    pygame.draw.rect(surf, GREEN, fill_rect)
    # 第四个参数：外框2像素
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
# 画生命条的函数
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        # 飞船生命数之间相隔32像素
        img_rect.x = x + 32 * i
        img_rect.y = y
        # 把图片画出来
        surf.blit(img, img_rect)
# 初始画面显示函数
def draw_init():
    # 游戏背景
    screen.blit(background_img1, (0, 0))
    # 游戏名
    draw_text(screen, '拯救许晔晨', 78, WIDTH/2, HEIGHT/4, WHITE)
    # 告诉玩家如何操控飞船
    draw_text(screen, '↑ ↓ ← → 移动飞船 空白键发射子弹~', 25, WIDTH/2, HEIGHT/2, WHITE)
    draw_text(screen, '按任意键开始游戏！', 25, WIDTH/2, HEIGHT*3/4, WHITE)
    draw_text(screen, '@Copyright 柠檬小帽', 22, WIDTH/2, HEIGHT - 30, SKYBLUE)
    # 显示出来
    pygame.display.update()
    # 等待键盘按下的事件
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得输入
        for event in pygame.event.get():
            # 事件的类型是否是退出
            if event.type == pygame.QUIT:
                # 把窗口关闭
                pygame.quit()
                sys.exit()
            # 键盘按下再松开后才开始
            elif event.type == pygame.KEYUP:
                waiting = False
def draw_end(round,score,record):
    # 游戏背景
    screen.blit(background_img1, (0, 0))
    if score > int(record):
        draw_text(screen, '新纪录：' + str(score) + "!", 30, WIDTH/2, HEIGHT/8, ORANGERED)
    draw_text(screen, "您成功闯到第" + str(round) + "关", 30, WIDTH/2, HEIGHT/4, ORANGE)
    draw_text(screen, "未能成功拯救许晔晨！", 30, WIDTH/2, HEIGHT* 1.5 /4, ORANGE)
    draw_text(screen, "您总共获得了 " + str(score) + " 分", 30, WIDTH/2, HEIGHT/2, ORANGE)
    draw_text(screen, '按空格键重新开始游戏！', 28, WIDTH/2, HEIGHT*3/4, WHITE)
    pygame.display.update()
    # 等待键盘按下的事件
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得输入
        for event in pygame.event.get():
            # 事件的类型是否是退出
            if event.type == pygame.QUIT:
                # 把窗口关闭
                pygame.quit()
                sys.exit()
            # 键盘按下空格键
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
def draw_victory(score, record):
    screen.blit(background_img6, (0, 0))
    if score > int(record):
        draw_text(screen, '新纪录：' + str(score) + "!", 50, WIDTH/2, HEIGHT/8, ORANGERED)
    draw_text(screen, "您成功坚持到了最后一关！", 38, WIDTH/2, HEIGHT/4, PURPLE)
    draw_text(screen, "您成功拯救了许氏集团的少爷：许晔晨!", 28, WIDTH/2, HEIGHT/2, PURPLE)
    draw_text(screen, "您将获得他的财产：" + str(score* 10) + " 元", 30, WIDTH/2, HEIGHT*2.5/4,ORANGERED)
    draw_text(screen, '按空格键重新开始游戏！', 28, WIDTH/2, HEIGHT*3/4, ROSE)
    pygame.display.update()
    # 等待键盘按下的事件
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得输入
        for event in pygame.event.get():
            # 事件的类型是否是退出
            if event.type == pygame.QUIT:
                # 把窗口关闭
                pygame.quit()
                return True
                # sys.exit()
            # 键盘按下空格键
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return False
def add_rock(round):
    for i in range(round - 1):
        new_rock(round)
def write_record(record):
    with open('record.txt','w') as f:   
        f.write(str(record)) 
def get_record():
    record = 0
    # 记录
    file_open = open("record.txt",encoding = "utf-8")
    for line in file_open.readlines(): # 依次读取每一行
        line = line.strip()    #去掉每行的头尾空白
        record = line
    file_open.close()
    return record
# 飞船
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # 内嵌的Sprite类的初始函数
        pygame.sprite.Sprite.__init__(self)
        # pygame.transform.scale() 把它的长宽重新定义
        self.image = pygame.transform.scale(player_img, (50, 38))
        # set_colorkey() 把黑色变透明
        self.image.set_colorkey(BLACK)
        # 定位图片，get_rect()把这张图片框起来，框起来后就可以对它设定属性
        self.rect = self.image.get_rect()
        # 飞船圆形半径
        self.radius = 20
        # 画出圆形
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # 绿色方块设定在画面的正中央
        self.rect.centerx = WIDTH / 2
        # 方块距离底部10px（飞船位置）
        self.rect.bottom = HEIGHT - 10
        # 方块的水平移动速度
        self.speedx = 8
        # 方块的垂直移动速度
        self.speedy = 8
        # 血量
        self.health = 100
        # 有几条命
        self.lives = 3
        # 判断飞船现在是否在隐藏中
        self.hidden = False
        # 飞船隐藏时间
        self.hide_time = 0
        # 子弹的等级
        self.gun = 1
        # 吃到闪电的时间
        self.gun_time = 0
        # 子弹射击的频率
        self.shoot_frequency = 0
    def update(self):
        # 现在的时间
        now = pygame.time.get_ticks()
        # 子弹等级过一段时间后就下降
        if self.gun > 1 and now - self.gun_time > 5000:
            # 等级下降
            self.gun -= 1
            # 时间设定为现在
            self.gun_time = now
        # 如果飞船在隐藏中，而且当update函数被呼叫时的时间减掉隐藏时间已经大于1秒钟
        if self.hidden and now - self.hide_time > 1000:
            # 让飞船显示回来
            self.hidden = False
            self.image = pygame.transform.scale(player_img, (50, 38))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            # 把飞船的位置定位回去
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        # pygame.key.get_pressed() 函数会回传一整串的布尔值 代表现在键盘的每一个按键有没有被按下
        key_pressed = pygame.key.get_pressed()
        # 判断右键有没有被按下，按下的话key_pressed[pygame.K_RIGHT]为true
        if key_pressed[pygame.K_RIGHT]: # K_d
            self.rect.x += self.speedx
        # 判断左键有没有被按下，按下的话key_pressed[pygame.K_LEFT]为true
        if key_pressed[pygame.K_LEFT]:  # K_a
            # 方块往左边动
            self.rect.x -= self.speedx
        # 判断上键有没有被按下，按下的话key_pressed[pygame.K_UP]为true
        if key_pressed[pygame.K_UP]: 
            self.rect.y -= self.speedy
        # 判断下键有没有被按下，按下的话key_pressed[pygame.K_DOWN]为true
        if key_pressed[pygame.K_DOWN]: 
            self.rect.y += self.speedy
        
        # 阻止方块跑出窗口
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    def shoot(self):
        # 没有隐藏中才让飞船发射子弹
        if not(self.hidden):
            # if self.shoot_frequency % 2 == 0:
                # 判断子弹的等级
                if self.gun == 1:
                    # 传入飞船的中心坐标，和飞船顶部
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    # 播放射击声音
                    shoot_sound.play()
                elif self.gun >= 2:
                    # 从飞船的两侧发射
                    bullet1 = Bullet(self.rect.left, self.rect.centery)
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    # 播放射击声音
                    shoot_sound.play()
            # self.shoot_frequency += 1
            # if self.shoot_frequency % 2 == 0:
            #     self.shoot_frequency = 0

    # 隐藏飞船
    def hide(self):
        self.hidden = True
        # 记录隐藏的时间
        self.hide_time = pygame.time.get_ticks()
        # 隐藏飞船（把飞船定位到飞船的外面）
        # 会在窗口下面500像素的位置
        self.image = pygame.transform.scale(player_img, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT + 500)
    def gunup(self):
        # 把等级加1
        self.gun += 1
        # 把时间设定成现在的时间
        self.gun_time = pygame.time.get_ticks()
# 石头
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        # 内嵌的Sprite类的初始函数
        pygame.sprite.Sprite.__init__(self)
        # 存放没有失真的图片
        # 从石头列表中随机抽一种石头图片出来
        self.image_ori = random.choice(rock_imgs)
        # 把黑色的部分去掉
        self.image_ori.set_colorkey(BLACK)
        # 存放转动后失真的图片
        self.image = self.image_ori.copy()
        # 定位图片，get_rect()把这张图片框起来，框起来后就可以对它设定属性
        self.rect = self.image.get_rect()
        # 石头圆形半径（因为不知道石头的宽度） 转为整数 -> 最后算分数看起来干净
        self.radius = int(self.rect.width * 0.85 / 2)
        # 画出圆形
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # 把石头的位置设为随机
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        # -100，-40为窗口上面看不到的地方，随机掉下来
        self.rect.y = random.randrange(-180, -100)
        # 石头的水平移动速度
        self.speedx = random.randrange(-3, 3)
        # 石头的垂直移动速度，掉下来的速度也是随机的
        self.speedy = random.randrange(2, 10)
        self.total_degree = 0
        # 让石头转动的度数随机
        self.rot_degree = random.randrange(-3, 3)
    
    def rotate(self):
        self.total_degree += self.rot_degree
        # 不要超过360度
        self.total_degree = self.total_degree % 360
        # 石头图片的旋转
        # pygame.transform.rotate() 第一个参数是要转动的图片，第二个参数是要转动几度
        # 转动会有一点点的失真
        # 解决方法：创建一个完全没有转动过的图片，每次的转动都是对这张图片做转动
        # 但不可能每次都对这张图片只转动3度，因为这样还是静止的
        # 所以每次转动的度数要叠加上去，第一次转动3度，第二次就转6度....
        # 加超过360度，就对360取余，不超过1圈
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # 但是石头还是会抽动
        # 解决方法：要在每一次的转动过后重新定位，而且都是把它定位在以前的中心点
        # 原先定位的中心点
        center = self.rect.center
        # 现在的self.image是转动过后的图片，get_rect()就是重新定位
        self.rect = self.image.get_rect()
        # 把转动后图片的中心点设为原先的中心点
        self.rect.center = center
    def update(self):
        self.rotate()
        # 让石头左右移动
        self.rect.x += self.speedx
        # 让石头掉下来
        self.rect.y += self.speedy
        # 石头的顶部大于窗口的高度，或者石头出了两边的边界
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            # 所有的属性重置，重新给值
            # 把石头的位置设为随机
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            # -100，-40为窗口上面看不到的地方，随机掉下来
            self.rect.y = random.randrange(-100, -40)
            # 石头的水平移动速度
            self.speedx = random.randrange(-3, 3)
            # 石头的垂直移动速度，掉下来的速度也是随机的
            self.speedy = random.randrange(2, 10)

# 子弹
class Bullet(pygame.sprite.Sprite):
    # 要传入飞船的位置
    def __init__(self, x, y):
        # 内嵌的Sprite类的初始函数
        pygame.sprite.Sprite.__init__(self)
        # 表示显示的图片，创建了一个Pygame的平面，宽度是10，高度是20
        self.image = bullet_img
        # set_colorkey() 把黑色变透明 
        self.image.set_colorkey(BLACK)
        # 定位图片，get_rect()把这张图片框起来，框起来后就可以对它设定属性
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # 子弹向上射击
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        # 判断子弹的底部如果小于0，表示出了窗口的上面
        if self.rect.bottom < 0:
            # kill()将子弹从所有的群组里删掉
            self.kill()

# 爆炸
class Explosion(pygame.sprite.Sprite):
    # 要传入爆炸的中心点，大爆炸还是小爆炸
    def __init__(self, center, size):
        # 内嵌的Sprite类的初始函数
        pygame.sprite.Sprite.__init__(self)
        # 爆炸的大小
        self.size = size
        # 爆炸的第一张图片
        self.image = expl_anim[self.size][0]
        # 定位图片，get_rect()把这张图片框起来，框起来后就可以对它设定属性
        self.rect = self.image.get_rect()
        self.rect.center = center
        # 代表现在更新到第几张图片
        self.frame = 0
        """
        为什么需要下面两个属性？
            如果用update来更新图片的话会更新得太快
            写一个frame属性判断上一次图片更新的时间和这一次是不是已经过了50毫秒
        """
        # 最后一张图片更新的时间（从初始化到现在经过的毫秒数）
        self.last_update = pygame.time.get_ticks()
        # 至少要经过几毫秒才会更新到下一张图片
        self.frame_rate = 50
    def update(self):
        # 现在图片更新的时间
        now = pygame.time.get_ticks()   
        if now - self.last_update > self.frame_rate:
            # 把最后一次的更新时间改为现在
            self.last_update = now
            # 更新到下一张图片
            self.frame += 1         
            # 判断图片有没有到最后一张了
            if self.frame == len(expl_anim[self.size]):
                # 把它删掉
                self.kill()
            else:
                # 更新到下一张图片
                self.image = expl_anim[self.size][self.frame]
                # 对图片做重新定位
                center = self.rect.center
                # 把爆炸的图片做重新定位
                self.rect = self.image.get_rect()
                # 定位在原先的中心点
                self.rect.center = center

# 宝物
class Power(pygame.sprite.Sprite):
    # 要传入飞船的位置
    def __init__(self, center):
        # 内嵌的Sprite类的初始函数
        pygame.sprite.Sprite.__init__(self)
        # type属性代表现在是哪种宝物，掉落是随机的
        self.type = random.choice(['shield', 'gun'])
        # 图片随机选一个，根据刚才的type
        self.image = power_imgs[self.type]
        # set_colorkey() 把黑色变透明 
        self.image.set_colorkey(BLACK)
        # 定位图片，get_rect()把这张图片框起来，框起来后就可以对它设定属性
        self.rect = self.image.get_rect()
        self.rect.center = center
        # 宝物是向下掉的，所以是正数
        self.speedy = 3
    def update(self):
        self.rect.y += self.speedy
        # 判断子弹的底部如果小于0，表示出了窗口的上面
        if self.rect.bottom > HEIGHT:
            # kill()将子弹从所有的群组里删掉
            self.kill()

# 播放背景音乐
# 传入参数：音乐要播放几次 -1代表无限重复播放
pygame.mixer.music.play(-1)
# 游戏初始画面是否显示
show_init = True
# 游戏是否继续
running = True
# 关卡数是否增加，是否增加石头
is_add_rock = True


# 游戏循环
while running:
    # 初始画面显示
    if show_init:
        close= draw_init()
        if close:
            break
        show_init = False
        # 创建一个Sprite的群组
        all_sprites = pygame.sprite.Group()
        # 石头群组
        rocks = pygame.sprite.Group()
        # 子弹群组
        bullets = pygame.sprite.Group()
        # 宝物群组
        powers = pygame.sprite.Group()
        # 创建一个Player
        player = Player()
        # 把player加到群组里
        all_sprites.add(player)
        # 创建8颗石头
        for i in range(8):
            new_rock(1)
        score = 0
        # 关卡数
        round = 1
        # 关卡数中文
        roundChi = '一'
        # 记录
        record = get_record()
    # if is_add_rock:
    #     if (500 < score < 1000) or (1500 < score < 2000):
    #         add_rock(round)
    #         print(rocks)
    #         is_add_rock = False
    # if not is_add_rock:
    #     if (1000 < score < 1500) or score > 2000:
    #         add_rock(round)
    #         print(rocks)
    #         is_add_rock = True
    if is_add_rock:
        if 500 < score < 1000:
            round = 2
            add_rock(round)
            roundChi = '二'
            is_add_rock = False
        elif 1500 < score < 2500:
            round = 4
            add_rock(round)
            roundChi = '四'
            is_add_rock = False
        elif 3500 < score < 5000:
            round = 6
            add_rock(round)
            roundChi = '六'
            is_add_rock = False
        elif 6500 < score < 8500:
            round = 8
            add_rock(round)
            roundChi = '八'
            is_add_rock = False
        elif score > 10500:
            round = 10
            add_rock(round+7)
            roundChi = '十'
            is_add_rock = False

    if not is_add_rock:
        if 1000 < score < 1500:
            round = 3
            add_rock(round)
            roundChi = '三'
            is_add_rock = True
        elif 2500 < score < 3500:
            round = 5
            add_rock(round)
            roundChi = '五'
            is_add_rock = True
        elif 5000 < score < 6500:
            round = 7
            add_rock(round)
            roundChi = '七'
            is_add_rock = True
        elif 8500 < score < 10500:
            round = 9
            add_rock(round+5)
            roundChi = '九'
            is_add_rock = True
    # 在一秒钟之内最多只能被执行FPS（Frames Per Second）次 
    clock.tick(FPS)
    # 取得输入
    # pygame.event.get() 回传现在发生的所有事件 像鼠标和键盘的事件 回传的是一个列表（同时发生多个事件）
    # for循环把每一个事件一一的拿出来
    for event in pygame.event.get():
        # 事件的类型是否是退出
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 如果按下空白键
            if event.key == pygame.K_SPACE:
                # 飞船射击子弹
                player.shoot()
    # 更新游戏
    # 去执行all_sprites群组里每个物件的update函数
    all_sprites.update()
    # 判断石头和子弹是否碰撞，后面还可以传入两个布尔值
    # 表示碰撞到后，石头是否要删掉，子弹是否要删掉
    # 会返回一个字典，里面是碰撞到的石头和子弹
    # key是碰撞到的石头，value是碰撞到的子弹
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        # 随机选择一个爆炸声音播放
        random.choice(expl_sounds).play()
        # 把石头的半径加到分数上
        score += hit.radius
        # 子弹射到石头是大爆炸
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        # 子弹和石头碰撞时有几率产生宝物
        # random.random() 会随机产生一个0到1的数
        if random.random() > 0.9:
            pow = Power(hit.rect.center) 
            all_sprites.add(pow)
            # 因为之后还要判断宝物和飞船是否碰撞到，碰撞到要让飞船吃下去，所以要创建宝物的群组
            powers.add(pow)
        # 只要每碰撞到一次，就补一颗石头
        new_rock(round)
    
    # 判断飞船和石头是否碰撞，后面还可以传入一个布尔值
    # 表示当飞船和石头碰撞时要不要把石头删掉
    # 会返回一个列表，里面是碰撞到的飞船的石头
    # 第四个参数：将预设的矩形碰撞改为圆形，同样还要给飞船和石头一个属性：半径
    # 此处False改为True，当初写False是因为飞船和石头撞到游戏就结束，此时石头是否删除影响不大
    # 现在飞船撞到石头游戏还要继续进行，所以要把石头删掉
    # 撞到之后石头会减少，因为改为True后把石头删掉了
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    # 回传的hits是一个列表，这个列表里面是撞到飞船的所有石头
    for hit in hits:
        # 此处需要把石头加回来，因为pygame.sprite.spritecollide的第三个参数传了True
        new_rock(round)
        # 以撞到石头的大小来扣血
        player.health -= hit.radius + 20
        # 石头碰到飞船是小爆炸
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        # 如果血量小于等于0，游戏结束
        if player.health <= 0 and player.lives >= 0:
            # 飞船爆炸
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            # 播放死亡音乐
            die_sound.play()
            # 生命数-1
            player.lives -= 1
            # 恢复满血
            player.health = 100
            # 死亡到复活的缓冲时间
            player.hide()
    
    # 判断宝物和飞船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        # 吃到盾牌后
        if hit.type == 'shield':
            player.health += 20
            # 血量不能超过100
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            # 吃到闪电后要做的事情
            player.gunup()
            gun_sound.play()
    # 生命数为0，die这个物件不存在了，才游戏结束
    if player.lives <= 0 and not(death_expl.alive()):
        if score > int(record):
            write_record(score)
        if round == 10:
            draw_victory(score, record)
        else:
            draw_end(roundChi,score,record)
        # 游戏结束后显示初始画面
        show_init = True

    # 画面显示
    screen.fill(BLACK)
    # 画在窗口的左上角
    # blit() 画到画面上 (0,0) 画在画面的左上角
    if score > 8500:
        screen.blit(background_img5,(0, 0))
    elif score > 5000:
        screen.blit(background_img4,(0, 0))
    elif score > 2500:
        screen.blit(background_img3,(0, 0))
    elif score > 1000:
        screen.blit(background_img2,(0, 0))
    else:
        screen.blit(background_img1, (0, 0))
    # screen.blit(background_img1, (0, 0))
    # 把all_sprites里面的东西全部都画到画面上
    all_sprites.draw(screen)
    # 第一个参数：要写在什么平面
    # 第二个参数：文字
    # 第三个参数：文字的大小
    # 第四个参数：文字的位置
    draw_text(screen, str(score), 22, WIDTH / 2, 10, WHITE)
    draw_text(screen, "第" + roundChi + "关", 22, WIDTH / 3, 10, WHITE)
    draw_text(screen, "记录: " + str(record), 22, WIDTH * 2.75 / 4, 10, WHITE)
    # 画出生命条
    draw_health(screen, player.health, 5, 15)
    # 画出还剩几条命
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    # 画面更新
    pygame.display.update()

# 关闭pygame的窗口
pygame.quit()