import pygame
import random
import tkinter as tk

# functions
# reset function
def reset():
    pass

# end screen function
def end_screen():
    pass

# start screen function
def start_screen():
    pass

# settings screen function
def settings_screen():
    window = tk.Tk()
    window.title("Settings")
    window.geometry("300x300")
    window.mainloop()

# fill background function(adding obstacles or logs to the background)
def fill_background(background):
    # getting all the coordinates for placing the obstacles
    coordinates = []
    for i in range(background.rect.y, background.rect.y+ background.image.get_height(), 50):
        coordinates.append(i)
        print(coordinates)
    # for now only adding logs to everything
    temp= 0
    for i in coordinates:
        temp += 1
        if temp % 2 == 0:
            direction = "left"
        else:
            direction = "right"
        log = Log(i, direction)
        log_group.add(log)

# Classes
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = resized_player
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2 - self.rect.width / 2
        self.rect.y = screen.get_height() - self.rect.height*2
        self.speed = 5
        self.direction = ""
        # finding out on what is the player standing
        self.on_what = None
        for background in backgrounds_group:
            if pygame.sprite.collide_rect(self, background):
                self.on_what = background.type
    
    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        global change_in_y
        if self.direction == "forward":
            change_in_y = self.speed
        elif self.direction == "backward":
            change_in_y = -self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        for background in backgrounds_group:
            if pygame.sprite.collide_rect(self, background):
                self.on_what = background.type
        #print(self.on_what)

# obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(0, 600)
        self.speed = random.randint(1, 5)

    def move(self):
        self.rect.x -= self.speed
        self.rect.y = self.rect.y + change_in_y
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# log class
class Log(pygame.sprite.Sprite):
    def __init__(self, y, direction):
        super().__init__()
        self.image = resized_log
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.speed = 1 # also will later be randomized
        self.direction = direction
        if self.direction == "left":
            self.rect.x = screen.get_width()+random.randint(0, log_image.get_width()*2)
        elif self.direction == "right":
            self.rect.x = 0 - self.rect.width - random.randint(0, log_image.get_width()*2)
        self.has_player = False

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        if self.has_player:
            if self.direction == "left":
                player.rect.x -= self.speed
            elif self.direction == "right":
                player.rect.x += self.speed
        self.rect.y = self.rect.y + change_in_y
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def add_player(self):
        self.has_player = True

# background class
class Background(pygame.sprite.Sprite):
    def __init__(self, type, y):
        super().__init__()
        if type == None:
            self.type = random.choice(["road", "water", "grass"])
        else:
            self.type = type
        if self.type == "road":
            self.image = pygame.transform.scale(pygame.image.load('road.png'), (800, 600))
        elif self.type == "water":
            self.image = pygame.transform.scale(pygame.image.load('water.png'), (800, 600))
        elif self.type == "grass":
            self.image = pygame.transform.scale(pygame.image.load('grass.png'), (800, 600))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        if y != None:
            self.rect.y = y
        else:
            self.rect.y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def move(self):
        self.rect.y = self.rect.y + change_in_y

# Initializing the pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Frogger")
icon = pygame.image.load('frog.png')
pygame.display.set_icon(icon)

# creating the backgrounds
backgrounds_group = pygame.sprite.Group()
background = Background("grass", 600-100)
backgrounds_group.add(background)

# creating the player
player_image = pygame.image.load('frog.png')
resized_player = pygame.transform.scale(player_image, (30, 30))
player = Player()

# creating a test obstacle
#obstacle_image = pygame.image.load('obstacle.png')
#resized_obstacle = pygame.transform.scale(obstacle_image, (50, 50))
obstacle_group = pygame.sprite.Group()

# creating a test log
log_image = pygame.image.load('log_temporary.png')
resized_log = pygame.transform.scale(log_image, (100, 50))
log_group = pygame.sprite.Group()

# main loop
running = True
change_in_y = 0
clock = pygame.time.Clock()
while running:

    # background color
    screen.fill((255, 255, 255))

    # event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.change_direction("forward")
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.change_direction("backward")
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.change_direction("left")
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.change_direction("right")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.change_direction("")
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.change_direction("")
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.change_direction("")
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.change_direction("")
    
    # checking if at least one background has y lower or equal to 0, if not, adding a new background
    temp = False
    back = None
    for background in backgrounds_group:
        if background.rect.y <= 0:
            temp = True
        else:
            back = background
    #print(temp, back)
    if not temp and back != None:
        background = Background(None, back.rect.y - screen.get_height())
        backgrounds_group.add(background)
        # filling the background with obstacles or logs
        fill_background(background)
    
    # removing backgrounds that are out of the screen
    for background in backgrounds_group:
        if background.rect.y - screen.get_height() > screen.get_height():
            backgrounds_group.remove(background)

    # removing obstacles that are out of the screen
    for obstacle in obstacle_group:
        if obstacle.rect.x < -obstacle.rect.width or obstacle.rect.x > screen.get_width():
            obstacle_group.remove(obstacle)
            obstacle = Obstacle()
            obstacle_group.add(obstacle)

    # removing logs that are out of the screen
    for log in log_group:
        if log.rect.x < -log.rect.width or log.rect.x > screen.get_width():
            new_log = Log(log.rect.y, log.direction)
            log_group.remove(log)
            log_group.add(new_log)
    
    # moving the player
    player.move()

    # moving the obstacles
    for obstacle in obstacle_group:
        obstacle.move()

    # moving the logs
    for log in log_group:
        log.move()

    # moving the backgrounds
    for background in backgrounds_group:
        background.move()
    
    # resetting the change_in_y(if this is not done, the logs would never stop moving)
    change_in_y = 0

    # background types drawing
    backgrounds_group.draw(screen)

                # drawing everything
    # drawing the obstacles
    obstacle_group.draw(screen)

    # drawing the logs
    log_group.draw(screen)

    # drawing the player
    player.draw(screen)

    # checking if player is on a log
    for log in log_group:
        if player.rect.x+player.rect.width < log.rect.x + log.rect.width and player.rect.x > log.rect.x:
            if player.rect.y < log.rect.y + log.rect.height and player.rect.y + player.rect.height > log.rect.y:
                log.add_player()
            else:
                log.has_player = False
        else:
            log.has_player = False

    # checking for collisions between player and obstacles
    if pygame.sprite.spritecollide(player, obstacle_group, False):
        print("collision")

    # checking if player left the screen
    if player.rect.x < 0 - resized_player.get_width() or player.rect.x > screen.get_width():
        print("player left the screen") # later this will trigger the end screen

    player.update()

    clock.tick(60)
    pygame.display.update()

pygame.quit()