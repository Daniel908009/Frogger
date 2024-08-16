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
    global end_screen_active, score
    end_screen_active = True
    end_screen = True
    # writing the score to a file
    write_score()
    # end screen loop
    while end_screen:
        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                end_screen = False
        # background color, and texts
        screen.fill((255, 255, 255))
        text = font.render("Score: "+str(score), True, (0, 0, 0))
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2))
        text1 = font.render("You lost", True, (0, 0, 0))
        screen.blit(text1, (screen.get_width()/2 - text1.get_width()/2, screen.get_height()/2 - text1.get_height()/2 - text.get_height()))
        pygame.display.update()

# start screen function
def start_screen():
    global running, start_screen_active
    start_screen_font = pygame.font.Font(None, 100)
    # start screen loop
    while start_screen_active and running:
        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_screen_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if screen.get_width()/2 - resized_play_button.get_width()/2 < event.pos[0] < screen.get_width()/2 + resized_play_button.get_width()/2 and screen.get_height()/2 - resized_play_button.get_height()/2 < event.pos[1] < screen.get_height()/2 + resized_play_button.get_height()/2:
                        start_screen_active = False
        # background color
        screen.fill((255, 255, 255))

        # main label
        text = start_screen_font.render("Frogger", True, (0, 0, 0))
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, text.get_height()))
        # play button
        screen.blit(resized_play_button, (screen.get_width()/2 - resized_play_button.get_width()/2, screen.get_height()/2 - resized_play_button.get_height()/2))
        # updating the screen
        pygame.display.update()

# pause screen function
def pause_screen():
    global running, pause_screen_active
    pause_screen_active = True
    while pause_screen_active:
        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pause_screen_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_q or event.key == pygame.K_m:
                    pause_screen_active = False
                elif event.key == pygame.K_r:
                    pause_screen_active = False
                    reset()
        # background color
        screen.fill((255, 255, 255))
        # pause text
        text = font.render("Paused", True, (0, 0, 0))
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2))
        # help text
        text1 = font.render("Press 'm' or 'p' or 'q' to continue", True, (0, 0, 0))
        screen.blit(text1, (screen.get_width()/2 - text1.get_width()/2, screen.get_height()/2 - text.get_height()/2 + text1.get_height()))
        # updating the screen
        pygame.display.update()

# spawn function for the obstacles and logs
def spawn_func():
    global running, obstacle_group, log_group, backgrounds_group, logs_to_spawn, obstacles_to_spawn, spawn_logs, spawn_obstacles, settings_window, pause_screen_active, quited
    clock = pygame.time.Clock()
    while running:
        # checking if the end screen is active or if the start screen is active
        while end_screen_active and running or start_screen_active and running or settings_window and running or pause_screen_active and running:
            clock.tick(10)
        # I added coordinates to the background class, so that I can spawn obstacles and logs on the right place(works)
        for background in backgrounds_group:
            temp = 0
            # the actual spawning of the obstacles and logs is done in the main loop, this is to prevent a drawing error
            for i in background.coordinates:
                if background.type == "road" and background.rect.y < 600:
                    if temp % 2 == 0:
                        if len(obstacle_group) < 30:
                            obstacles_to_spawn.append(Obstacle(i, "left", None, None))
                            spawn_obstacles = True
                    else:
                        if len(obstacle_group) < 30:
                            obstacles_to_spawn.append(Obstacle(i, "right", None, None))
                            spawn_obstacles = True
                elif background.type == "water" and background.rect.y < 600:
                    #print(background.coordinates)
                    if temp % 2 == 0:
                        if len(log_group) < 30:
                            logs_to_spawn.append(Log(i, "left", None, None))
                            spawn_logs = True
                    else:
                        if len(log_group) < 30:
                            logs_to_spawn.append(Log(i, "right", None, None))
                            spawn_logs = True
                temp += 1
        clock.tick(0.2)
    quited = True


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

# function to write the score to a file, later will be used for highscores window
def write_score():
    global player_name, score
    # first reading the file
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
        file.close()
    except:
        scores = []
    # rearranging the scores from highest to lowest
    scores.append(player_name+","+str(score)+"\n")
    scores = sorted(scores, key=lambda x: int(x.split(",")[1]), reverse=True)
    # writing the scores to the file
    with open("scores.txt", "w") as file:
        for i in scores:
            file.write(i)
    # closing the file
    file.close()

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
        self.image = random.choice(resized_obstacles)
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

# obstacle image
obstacle_image = pygame.image.load('temporary_obstacle.png')
obstacle_image_red = pygame.image.load('temporary_obstacle_red.png')
obstacle_image_yellow = pygame.image.load('temporary_obstacle_yellow.png')
obstacle_image_purple = pygame.image.load('temporary_obstacle_purple.png')
obstacle_image_pink = pygame.image.load('temporary_obstacle_pink.png')
obstacle_image_blue = pygame.image.load('temporary_obstacle_blue.png')
resized_obstacles = [pygame.transform.scale(obstacle_image, (100, 50)), pygame.transform.scale(obstacle_image_red, (100, 50)), pygame.transform.scale(obstacle_image_yellow, (100, 50)), pygame.transform.scale(obstacle_image_purple, (100, 50)), pygame.transform.scale(obstacle_image_pink, (100, 50)), pygame.transform.scale(obstacle_image_blue, (100, 50))]
obstacle_group = pygame.sprite.Group()

# log image
log_image = pygame.image.load('log_temporary.png')
resized_log = pygame.transform.scale(log_image, (100, 50))
log_group = pygame.sprite.Group()

# setting up a play button
play_button = pygame.image.load('play_button.png')
resized_play_button = pygame.transform.scale(play_button, (300, 100))

# setting up a thread for the spawning of obstacles and logs
spawn_thread = threading.Thread(target=spawn_func)

# special settings
invincible = False

# main loop
running = True
quited = False
change_in_y = 0
clock = pygame.time.Clock()
coordinates = []
score = 0
spawn_logs, spawn_obstacles = False, False
logs_to_spawn, obstacles_to_spawn = [], []
on_water = 0
end_screen_active, start_screen_active, settings_window, pause_screen_active = False, True, False, False
player_name = "Player"
# score font
font = pygame.font.Font(None, 36)
while running:

    # showing the start screen
    while start_screen_active:
        start_screen()

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
            elif event.key == pygame.K_r:
                reset()
            elif event.key == pygame.K_p or event.key == pygame.K_q or event.key == pygame.K_m:
                pause_screen()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_s or event.key == pygame.K_DOWN or event.key == pygame.K_a or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.change_direction("")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # checking if the settings button was clicked
                if screen.get_width()-resized_settings_button.get_width() < event.pos[0] < screen.get_width() and 0 < event.pos[1] < resized_settings_button.get_height():
                    settings_window = True
                    settings_screen()
    
    # if the code reaches this point, the settings window must be closed
    settings_window = False

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
        if obstacle.rect.x < screen.get_width()*-2 or obstacle.rect.x > screen.get_width()*2 or obstacle.rect.y > screen.get_height()+obstacle.rect.height:
            obstacle_group.remove(obstacle)
    # removing logs that are out of the screen
    for log in log_group:
        if log.rect.x < screen.get_width()*-2 or log.rect.x > screen.get_width()*2 or log.rect.y > screen.get_height()+log.rect.height:
            log_group.remove(log)
    
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
        # checking for collisions between player and logs is now done through colission(its less buggy)
        for log in log_group:
            if pygame.sprite.collide_rect(player, log):
                log.has_player = True
            else:
                log.has_player = False
    else:
        for log in log_group:
            if pygame.sprite.collide_rect(player, log):
                print("player is on a log")
            else:
                log.has_player = False

    # checking if player is on a water background and not on a log
    if player.on_what == "water":
        temp = False
        for log in log_group:
            if log.has_player:
                temp = True
                break
        # I complexified this, because this was the original solution, but it was buggy, however it can stay now as a double check
        if temp:
            on_water = 0
        else:
            on_water += 1
        #print(on_water, temp)
        if on_water == 2 and not invincible and not temp:
            end_screen()

    # checking for collisions between player and obstacles
    if pygame.sprite.spritecollide(player, obstacle_group, False) and not invincible:
        end_screen()

    # checking if player left the screen
    if player.rect.x < 0 - resized_player.get_width() and not invincible or player.rect.x > screen.get_width() and not invincible:
        end_screen()

    # updating the player(checking if the player is on a water background)
    player.update()

    # updating the backgrounds
    backgrounds_group.update()

    # just for testing
    # displaying fps
    fps = font.render(str(int(clock.get_fps())), True, (0, 0, 0))
    screen.blit(fps, (screen.get_width()-fps.get_width(), screen.get_height()-fps.get_height()))

    # spawning the new obstacles and logs
    if spawn_logs:
        for log in logs_to_spawn:
            log_group.add(log)
        logs_to_spawn.clear()
        spawn_logs = False
    if spawn_obstacles:
        for obstacle in obstacles_to_spawn:
            obstacle_group.add(obstacle)
        obstacles_to_spawn.clear()
        spawn_obstacles = False

    # updating the screen and setting the frames per second
    clock.tick(60)
    pygame.display.update()

# waiting for the thread to finish(this prevents an error when the code tryes to spawn an obstacle or log on a non existing window)
while not quited:
    pass
pygame.quit()