#create a Maze game!
from pygame import *

#game scene
win_width = 700
win_height = 500

class GameSprite(sprite.Sprite):
  def __init__(self, player_image, player_x, player_y, player_speed):
    super().__init__()
    
    self.image = transform.scale(image.load(player_image), (65, 65))
    self.speed = player_speed
    self.rect = self.image.get_rect()
    self.rect.x = player_x
    self.rect.y = player_y
    
  def reset(self):
    window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite): 
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect. y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed / 2
        else:
            self.rect.x += self.speed / 2

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#object
player = Player('hero.png', 10, 10, 10)
enemy = Enemy('cyborg.png', win_width - 125, win_height - 250, 10)
treasure = GameSprite('treasure.png', win_width - 125, win_height - 125, 10)
wall_1 = Wall(51, 196, 61, 100, 100, 450, 10)


window = display.set_mode((win_width, win_height))
display.set_caption("Maze")

background = transform.scale(image.load("background.jpg"), (win_width, win_height))

#music
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

clock = time.Clock()
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background,(0, 0))
    enemy.update()
    player.update()
    player.reset()
    enemy.reset()
    treasure.reset()
    wall_1.reset()

    display.update()
    clock.tick(60)
