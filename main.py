import pygame
import random
import tkinter as tk
import threading

# functions
# reset function
def reset():
    pass

# end screen function, currenlty very simple, will be updated later
def end_screen():
    end_screen = True
    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                end_screen = False
        screen.fill((255, 255, 255))
        text = font.render("Score: "+str(score), True, (0, 0, 0))
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2))
        text1 = font.render("You lost", True, (0, 0, 0))
        screen.blit(text1, (screen.get_width()/2 - text1.get_width()/2, screen.get_height()/2 - text1.get_height()/2 - text.get_height()))
        pygame.display.update()

# start screen function
def start_screen():
    pass

# spawn function for the obstacles and logs
def spawn_func():
    global running, obstacle_group, log_group, backgrounds_group
    clock = pygame.time.Clock()
    while running:                                          # first attempt failed
                                                     #    copy_obstacle_group = obstacle_group.copy()
                                                     #    copy_log_group = log_group.copy()
                                                     #    #print(len(obstacle_group))
                                                     #    print(len(log_group))
                                                     #    # for every row of obstacles, logs spawns another obstacle or log
                                                     #    for log in copy_log_group:
                                                     #        #print("log loop")
                                                     #        # spawns a new log if there is less than 50 logs on the screen
                                                     #        if len(log_group) < 50:
                                                     #            new_log = Log(log.rect.y, log.direction, log.speed, log.initial_x)
                                                     #            log_group.add(new_log)
                                                     #            #print("spawned log")
                                                     #    for obstacle in copy_obstacle_group:
                                                     #        # spawns a new obstacle if there is less than 50 obstacles on the screen
                                                     #        if len(obstacle_group) < 50:
                                                     #            new_obstacle = Obstacle(obstacle.rect.y, obstacle.direction, obstacle.speed, obstacle.initial_x)
                                                     #            obstacle_group.add(new_obstacle)
                                                     #            #print("spawned obstacle")
                                                                # spawns new obstacles and logs every couple of seconds
                                                            #print("spawned check")

    # I added coordinates to the background class, so that I can spawn obstacles and logs on the right place(hopefully this works)
    # it does work, but it is not perfect, and can cause errors, however I have a solution for this(will be implemented later)
        for background in backgrounds_group:
            temp = 0
            for i in background.coordinates:
                if background.type == "road":
                    if temp % 2 == 0:
                        if len(obstacle_group) < 30:
                            new_obstacle = Obstacle(i, "left", None, None)
                            obstacle_group.add(new_obstacle)
                    else:
                        if len(obstacle_group) < 30:
                            new_obstacle = Obstacle(i, "right", None, None)
                            obstacle_group.add(new_obstacle)
                elif background.type == "water":
                    if temp % 2 == 0:
                        if len(log_group) < 30:
                            new_log = Log(i, "left", None, None)
                            log_group.add(new_log)
                    else:
                        if len(log_group) < 30:
                            new_log = Log(i, "right", None, None)
                            log_group.add(new_log)
                temp += 1



        clock.tick(0.2)


# settings screen function
def settings_screen():
    window = tk.Tk()
    window.title("Settings")
    window.geometry("300x300")
    window.resizable(False, False)
    window.iconbitmap("settings.ico")
    # creating a label
    label = tk.Label(window, text="Settings", font=("Arial", 20))
    label.pack()
    # creating a frame for the settings
    frame = tk.Frame(window)
    frame.pack()
    # creating a label for the first setting
    label1 = tk.Label(frame, text="Setting 1")
    label1.grid(row=0, column=0)
    # creating a checkbutton for the first setting
    checkbutton1 = tk.Checkbutton(frame)
    checkbutton1.grid(row=0, column=1)

    # creating a apply button
    apply_button = tk.Button(window, text="Apply", command=lambda: window.destroy())# later this will call a function to apply the settings
    apply_button.pack(side="bottom")

    window.mainloop()

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

# obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y, direction, speed, x):
        super().__init__()
        self.image = resized_obstacle
        self.rect = self.image.get_rect()
        self.rect.y = y
        if speed == None:
            self.speed = 1 # later this will be random maybe
        else:
            self.speed = speed
        self.direction = direction
        if x == None:
            if self.direction == "left":
                self.rect.x = screen.get_width()+random.randint(0, obstacle_image.get_width())
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.direction == "right":
                self.rect.x = 0 - self.rect.width - random.randint(0, obstacle_image.get_width())
        else:
            self.rect.x = x
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.direction == "right":
                pass
        self.initial_x = self.rect.x

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        self.rect.y = self.rect.y + change_in_y
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# log class
class Log(pygame.sprite.Sprite):
    def __init__(self, y, direction, speed ,x):
        super().__init__()
        self.image = resized_log
        self.rect = self.image.get_rect()
        self.rect.y = y
        if speed == None:
            self.speed = 1 # again will be random later maybe
        else:
            self.speed = speed
        self.direction = direction
        if x == None:
            if self.direction == "left":
                self.rect.x = screen.get_width()+random.randint(0, log_image.get_width())
            elif self.direction == "right":
                self.rect.x = 0 - self.rect.width - random.randint(0, log_image.get_width())
        else:
            self.rect.x = x
        self.has_player = False
        self.initial_x = self.rect.x

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
    def __init__(self, type, y, height):
        super().__init__()
        if type == None:
            self.type = random.choice(["road", "water", "grass"])
        else:
            self.type = type
        if height != None:
            self.image = pygame.transform.scale(pygame.image.load('grass.png'), (800, height))
        else:
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
        self.coordinates = []
        # getting all the coordinates for placing the obstacles
        for i in range(self.rect.y, self.rect.y+ self.image.get_height(), 50):
            self.coordinates.append(i)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def move(self):
        self.rect.y = self.rect.y + change_in_y
    
    def update(self):
        self.coordinates.clear()
        for i in range(self.rect.y, self.rect.y+ self.image.get_height(), 50):
            self.coordinates.append(i)

# Initializing the pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Frogger")
icon = pygame.image.load('frog.png')
pygame.display.set_icon(icon)

# creating the backgrounds
backgrounds_group = pygame.sprite.Group()
background = Background("grass", 600-100, None)
backgrounds_group.add(background)

# creating a settings button
settings_button = pygame.image.load('settings.png')
resized_settings_button = pygame.transform.scale(settings_button, (50, 50))

# creating the player
player_image = pygame.image.load('frog.png')
resized_player = pygame.transform.scale(player_image, (35, 35))
player = Player()

# creating a test obstacle
obstacle_image = pygame.image.load('temporary_obstacle.png')
resized_obstacle = pygame.transform.scale(obstacle_image, (100, 50))
obstacle_group = pygame.sprite.Group()

# creating a test log
log_image = pygame.image.load('log_temporary.png')
resized_log = pygame.transform.scale(log_image, (100, 50))
log_group = pygame.sprite.Group()

# setting up a thread for the spawning of obstacles and logs
spawn_thread = threading.Thread(target=spawn_func)

# special settings
invincible = True

# main loop
running = True
change_in_y = 0
clock = pygame.time.Clock()
coordinates = []
score = 0
# score font
font = pygame.font.Font(None, 36)
while running:
    # starting the thread for the spawning of obstacles and logs
    if not spawn_thread.is_alive():
        spawn_thread.start()

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
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_s or event.key == pygame.K_DOWN or event.key == pygame.K_a or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.change_direction("")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # checking if the settings button was clicked
                if screen.get_width()-resized_settings_button.get_width() < event.pos[0] < screen.get_width() and 0 < event.pos[1] < resized_settings_button.get_height():
                    settings_screen()
    
    # checking if at least one background has y lower or equal to 0, if not, adding a new background
    temp = False
    back = None
    for background in backgrounds_group:
        if background.rect.y <= 0:
            temp = True
        else:
            back = background

    if not temp and back != None:
        if back.type == "grass":
            if back.image.get_height() == 200:
                background1 = Background(None, back.rect.y - 600, None)
            else:
                background1 = Background(None, back.rect.y - back.image.get_height(), None)
        else:
            background1 = Background("grass", back.rect.y - 200, 200)
        backgrounds_group.add(background1)
    
    # removing backgrounds that are out of the screen
    for background in backgrounds_group:
        if background.rect.y - screen.get_height() > screen.get_height():
            backgrounds_group.remove(background)

    # removing obstacles that are out of the screen
    for obstacle in obstacle_group:
        if obstacle.rect.x < screen.get_width()*-2 or obstacle.rect.x > screen.get_width()*2:
            obstacle_group.remove(obstacle)
            #print("removed obstacle")
    # removing logs that are out of the screen
    for log in log_group:
        if log.rect.x < screen.get_width()*-2 or log.rect.x > screen.get_width()*2:
            log_group.remove(log)
            #print("removed log")
    
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
    
    # increasing the score
    score += change_in_y
    
    # resetting the change_in_y(if this is not done, the logs would never stop moving)
    change_in_y = 0

    # background types drawing
    backgrounds_group.draw(screen)

                # drawing everything
    try:
        # drawing the obstacles
        obstacle_group.draw(screen)

        # drawing the logs
        log_group.draw(screen)
    except:
        print("We hebben een serieus probleem")
    # drawing the player
    player.draw(screen)

    # drawing a settings button
    screen.blit(resized_settings_button, (screen.get_width()-resized_settings_button.get_width(), 0))

    # drawing the score in the top left corner
    text = font.render("Score: "+str(score), True, (255, 255, 255))
    screen.blit(text, (0, 0))

    # checking if player is on a log
    if not any(log.has_player for log in log_group):
        for log in log_group:
            if player.rect.x+player.rect.width < log.rect.x + log.rect.width and player.rect.x > log.rect.x:
                if player.rect.y < log.rect.y + log.rect.height and player.rect.y + player.rect.height > log.rect.y:
                    log.add_player()
                else:
                    log.has_player = False
            else:
                log.has_player = False
    else:
        for log in log_group:
            if log.has_player:
                if player.rect.x+player.rect.width < log.rect.x + log.rect.width and player.rect.x > log.rect.x:
                    if player.rect.y < log.rect.y + log.rect.height and player.rect.y + player.rect.height > log.rect.y:
                        pass
                    else:
                        log.has_player = False
                else:
                    log.has_player = False
        
    # checking if player is on a water background and not on a log
    if player.on_what == "water":
        temp = False
        for log in log_group:
            if log.has_player:
                temp = True
                break
        if not temp and not invincible:
            end_screen()

    # checking for collisions between player and obstacles
    if pygame.sprite.spritecollide(player, obstacle_group, False) and not invincible:
        end_screen()

    # checking if player left the screen
    if player.rect.x < 0 - resized_player.get_width() or player.rect.x > screen.get_width() and not invincible:
        end_screen()

    # updating the player(checking if the player is on a water background)
    player.update()

    # updating the backgrounds
    backgrounds_group.update()

    # just for testing
    # displaying fps
    fps = font.render(str(int(clock.get_fps())), True, (0, 0, 0))
    screen.blit(fps, (screen.get_width()-fps.get_width(), screen.get_height()-fps.get_height()))

    # updating the screen and setting the frames per second
    clock.tick(60)
    pygame.display.update()

pygame.quit()