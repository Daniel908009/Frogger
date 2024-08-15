import pygame
import random

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
    pass

# Classes
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = resized_player
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2 - self.rect.width / 2
        self.rect.y = screen.get_height() - self.rect.height
        self.speed = 5
        self.direction = ""
    
    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        global change_in_y
        #print("moving")
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
    def __init__(self):
        print("log created")
        super().__init__()
        self.image = resized_log
        self.rect = self.image.get_rect()
        self.rect.x = 200 # later this will be random
        self.rect.y = 200 # later this will be random
        self.speed = 1 # also will later be randomized
        self.direction = random.choice(["left","right"])
        self.has_player = False

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        if self.has_player:
            player.rect.x += self.speed
        self.rect.y = self.rect.y + change_in_y
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def add_player(self):
        self.has_player = True

# Initializing the pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Frogger")
icon = pygame.image.load('frog.png')
pygame.display.set_icon(icon)

# creating the player
player_image = pygame.image.load('frog.png')
resized_player = pygame.transform.scale(player_image, (50, 50))
player = Player()

# creating a test obstacle
#obstacle_image = pygame.image.load('obstacle.png')
#resized_obstacle = pygame.transform.scale(obstacle_image, (50, 50))
#obstacle = Obstacle()
#obstacle_group = pygame.sprite.Group()
#obstacle_group.add(obstacle)

# creating a test log
log_image = pygame.image.load('log_temporary.png')
resized_log = pygame.transform.scale(log_image, (100, 50))
log = Log()
log_group = pygame.sprite.Group()
log_group.add(log)

# main loop
running = True
change_in_y = 0
clock = pygame.time.Clock()
while running:

    # background
    screen.fill((255, 255, 255))

    # event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                print("forward")
                player.change_direction("forward")
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                print("backward")
                player.change_direction("backward")
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                print("left")
                player.change_direction("left")
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print("right")
                player.change_direction("right")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                print("forward stop")
                player.change_direction("")
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                print("backward stop")
                player.change_direction("")
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                print("left stop")
                player.change_direction("")
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print("right stop")
                player.change_direction("")
    
    # removing obstacles that are out of the screen
    #for obstacle in obstacle_group:
    #    if obstacle.rect.x < -obstacle.rect.width or obstacle.rect.x > screen.get_width():
    #        obstacle_group.remove(obstacle)
    #        obstacle = Obstacle()
    #        obstacle_group.add(obstacle)

    # removing logs that are out of the screen
    for log in log_group:
        if log.rect.x < -log.rect.width or log.rect.x > screen.get_width():
            log_group.remove(log)
            log = Log()
            log_group.add(log)
    
    # moving the player
    player.move()

    # moving the obstacles
    #obstacle_group.move()

    # moving the logs
    for log in log_group:
        log.move()
    
    # resetting the change_in_y(if this is not done, the logs would never stop moving)
    change_in_y = 0

                # drawing everything
    # drawing the obstacles
    #obstacle_group.draw(screen)

    # drawing the logs
    log_group.draw(screen)

    # drawing the player
    player.draw(screen)

    # testing if the player is on a log works
    #for log in log_group:
        #log.add_player()

    # checking for collisions between player and obstacles
    #if pygame.sprite.spritecollide(player, obstacle_group, False):
    #    print("collision")

    # checking if player left the screen
    if player.rect.x < 0 - resized_player.get_width() or player.rect.x > screen.get_width():
        print("player left the screen") # later this will trigger the end screen

    clock.tick(60)
    pygame.display.update()

pygame.quit()