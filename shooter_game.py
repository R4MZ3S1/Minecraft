#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer

#музыка
mixer.init()


random = randint(1, 6)
random_x = (1, 700)
randomdom = (1, 2)



if random == 1:
    randomdom = 'ender.png'

if random == 1:
    randomdom = 'ender2.png'



print(randint)
if random == 1:
    mixer.music.load('Scopin.mp3')
    mixer.music.play()
    
if random == 2:
    mixer.music.load('Haggstrom.mp3')
    mixer.music.play()

if random == 3:
    mixer.music.load('Key.mp3')
    mixer.music.play()

if random == 4:
    mixer.music.load('Minecraft.mp3')
    mixer.music.play()

if random == 5:
    mixer.music.load('Mutation.mp3')
    mixer.music.play()

if random == 6:
    mixer.music.load('Subwoofer.mp3')
    mixer.music.play()


fire_sound = mixer.Sound("piu.mp3")

img_hero = 'steve.png'
img_hero1 = 'alex.png'
img_back = 'minecraft.webp'
img_enemy = 'ender.png'
img_bullet = 'strela.png'
img_zar = 'enderzariad.png'


score = 0
lost = 0
max_lost = 2


font.init()
font1 = font.SysFont("Arial", 30)
win = font1.render('YOU Win о_О', True, (0, 255, 0))
lose = font1.render('You Lose :-D', True, (255, 0, 0))
cel = 10

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,
        15, 20, -7)
        bullets.add(bullet)

#класс-наследник для спрайта-врага (перемещается сам)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Counter-Strike 7")
background = transform.scale(image.load(img_back),
(win_width, win_height))


bullets = sprite.Group()
player = Player(img_hero, 300, 400, 85, 100, 8)
player2 = Player(img_hero1, 370, 400, 70, 90, 8)


monsters = sprite.Group()
for i in range (1, 10):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 1, 85, 100, randint(1, 2))
    monsters.add(monster)

enderzariads = sprite.Group()
for i in range (1, 10):
    enderzariad = Enemy(img_zar, randint(30, win_width - 80), -40, 25, 25, randint(1, 3))
    enderzariads.add(enderzariad)


finish = False
run = True
reload = False
num_fire = 0

while run:
    for knopka in event.get():
        if knopka.type == QUIT:
            run = False
        if knopka.type == KEYDOWN:
            if knopka.key == K_SPACE:
                if num_fire < 5 and reload == False:
                    fire_sound.play()
                    player.fire()
                    player2.fire()
                    num_fire += 1
                if num_fire >= 5 and reload == False:
                    shoot_time = timer()
                    reload = True



    if not finish:
        window.blit(background, (0,0))
        text = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        player.update()
        player.reset()
        player2.update()
        player2.reset()
        monsters.update()
        enderzariads.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        enderzariads.draw(window)
        if reload == True:
            now_time = timer()
            if now_time - shoot_time <3:
                reload1 = font1.render('Перезарядка....',
                                       1, (150, 0, 0))
                window.blit(reload1, (260, 460))
            else:
                num_fire = 0
                reload = False 


        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80),
            -40, 105, 80, randint(1, 2))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, enderzariads, False)or lost >= max_lost:
            finish = True
            window.blit(lose, (250, 200))
        if score >= cel:
            finish = True
            window.blit(win, (250, 200))
        display.update()


    time.delay(50)