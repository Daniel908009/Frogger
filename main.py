import pygame
import random
import tkinter as tk
import threading
from pygame import mixer

# functions
# reset function
def reset():
    global obstacle_group, log_group, backgrounds_group, score, end_screen_active, player
    # resetting the score
    score = 0
    # resetting the player
    player.rect.x = screen.get_width() / 2 - player.rect.width / 2
    player.rect.y = screen.get_height() - player.rect.height*2
    # resetting the obstacles
    obstacle_group.empty()
    # resetting the logs
    log_group.empty()
    # resetting the backgrounds
    backgrounds_group.empty()
    # starting the game again
    end_screen_active = False
    # spawning the beginning background
    background = Background("grass", 600-100, None)
    backgrounds_group.add(background)
    # resetting players attributes
    player.on_what = None
    player.direction = ""
    # reseting important variables
    global on_water, temp, change_in_y
    on_water = 0
    temp = False
    change_in_y = 0

    # starting the music again
    mixer.music.load('beethoven-sonata.mp3')
    mixer.music.play(-1)

# end screen function, currenlty very simple, will be updated later
def end_screen(death_type):
    global end_screen_active, score, start_screen_active
    end_screen_active = True
    end_screen = True
    # setting the end screen text based on the death type
    if death_type == "water":
        text1 = font.render("You drowned", True, (0, 0, 0))
        joke = "How does a blonde kill a fish? She drowns it ..." # later the jokes will be randomised from a file
    elif death_type == "car":
        text1 = font.render("You got hit by a car", True, (0, 0, 0))
        joke = "What do you call a Ford Fiesta that ran out of gas? A Ford Siesta." # later the jokes will be randomised from a file
    elif death_type == "left":
        text1 = font.render("You left the screen", True, (0, 0, 0))
        joke = "The circus lion decided to quit because he felt trapped in his job."# later the jokes will be randomised from a file
    
    # resizing the text so it always fits the screen
    joke_text = font.render(str(joke), True, (0, 0, 0))
    while joke_text.get_width() > screen.get_width():
        font1 = pygame.font.Font(None, font.size-1)
        joke_text = font1.render(str(joke), True, (0, 0, 0))

    # setting up the score text
    text = font.render("Score: "+str(score), True, (0, 0, 0))
    # stopping the music
    mixer.music.stop()
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    end_screen = False
                    reset()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # checking if the back arrow was clicked
                    if 0 < event.pos[0] < resized_back_arrow.get_width() and 0 < event.pos[1] < resized_back_arrow.get_height():
                        end_screen = False
                        start_screen_active = True
        # background color, and texts
        screen.fill((255, 255, 255))
        # displaying the score
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2 - text.get_height()/2))
        # displaying the death text
        screen.blit(text1, (screen.get_width()/2 - text1.get_width()/2, screen.get_height()/2 - text1.get_height()/2 - text.get_height()))
        # displaying the joke
        screen.blit(joke_text, (screen.get_width()/2 - joke_text.get_width()/2, screen.get_height()/2 - joke_text.get_height()/2 + text.get_height()))
        # displaying a back arrow
        screen.blit(resized_back_arrow, (0, 0))
        pygame.display.update()

# start screen function
def start_screen():
    global running, start_screen_active
    start_screen_font = pygame.font.Font(None, 100)
    # starting the music
    mixer.music.load('main_menu_music.mp3')
    mixer.music.play(-1)
    # start screen loop
    while start_screen_active and running:
        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_screen_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # checking play button
                    if screen.get_width()/2 - resized_play_button.get_width()/2 < event.pos[0] < screen.get_width()/2 + resized_play_button.get_width()/2 and screen.get_height()/2 - resized_play_button.get_height()/2 < event.pos[1] < screen.get_height()/2 + resized_play_button.get_height()/2:
                        mixer.music.stop()
                        mixer.music.load('beethoven-sonata.mp3')
                        mixer.music.play(-1)
                        start_screen_active = False
                        reset()
                    # checking scores button
                    elif screen.get_width()/2 - resized_scores_button.get_width()/2 < event.pos[0] < screen.get_width()/2 + resized_scores_button.get_width()/2 and screen.get_height()/2 - resized_scores_button.get_height()/2 + resized_play_button.get_height() < event.pos[1] < screen.get_height()/2 + resized_scores_button.get_height()/2 + resized_play_button.get_height():
                        scores_screen()
                    # checking exit button
                    elif screen.get_width()/2 - resized_end_game_button.get_width()/2 < event.pos[0] < screen.get_width()/2 + resized_end_game_button.get_width()/2 and screen.get_height()/2 - resized_end_game_button.get_height()/2 + resized_play_button.get_height() + resized_scores_button.get_height() < event.pos[1] < screen.get_height()/2 + resized_end_game_button.get_height()/2 + resized_play_button.get_height() + resized_scores_button.get_height():
                        running = False
                        start_screen_active = False
        # background color
        screen.fill((255, 255, 255))

        # main label
        text = start_screen_font.render("Frogger", True, (0, 0, 0))
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, text.get_height()))
        # play button
        screen.blit(resized_play_button, (screen.get_width()/2 - resized_play_button.get_width()/2, screen.get_height()/2 - resized_play_button.get_height()/2))
        # scores button
        screen.blit(resized_scores_button, (screen.get_width()/2 - resized_scores_button.get_width()/2, screen.get_height()/2 - resized_scores_button.get_height()/2 + resized_play_button.get_height()))
        # exit button
        screen.blit(resized_end_game_button, (screen.get_width()/2 - resized_end_game_button.get_width()/2, screen.get_height()/2 - resized_end_game_button.get_height()/2 + resized_play_button.get_height() + resized_scores_button.get_height()))
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

# function to show the top scores
def scores_screen():
    global running, start_screen_active
    # setting the font
    score_font = pygame.font.Font(None, 40)
    # label font
    label_font = pygame.font.Font(None, 60)
    # scores screen loop
    while running:
        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_screen_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # checking if the back arrow was clicked
                    if 0 < event.pos[0] < resized_back_arrow.get_width() and 0 < event.pos[1] < resized_back_arrow.get_height():
                        return
        # background color
        screen.fill((255, 255, 255))
        # reading the scores from the file
        try:
            with open("scores.txt", "r") as file:
                scores = file.readlines()
            file.close()
        except:
            scores = []
        # removing the \n from the scores
        for i in range(len(scores)):
            scores[i] = scores[i].replace("\n", "")
        # main label
        text = label_font.render("Top scores", True, (0, 0, 0))
        screen.blit(text, (screen.get_width()/2 - text.get_width()/2, text.get_height()))
        # back arrow
        screen.blit(resized_back_arrow, (0, 0))
        # displaying the first ten scores
        for i in range(10):
            try:
                text1 = score_font.render(str(i+1)+". "+scores[i], True, (0, 0, 0))
                screen.blit(text1, (screen.get_width()/2 - text1.get_width()/2, text.get_height()*2 + text1.get_height() + i*text1.get_height()))
            except:
                pass
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
        if running:
            clock.tick(0.2)
    quited = True

# function to apply the settings
def apply_settings(window, setting1,setting2, setting3):
    global invincible
    invincible = setting1
    global back_wards_movement
    back_wards_movement = setting2
    global show_fps
    show_fps = setting3
    window.destroy()

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
    # creating a label for the invincible setting
    label1 = tk.Label(frame, text="Invincible")
    label1.grid(row=0, column=0)
    # creating a checkbutton for the invincible setting
    e1 = tk.BooleanVar()
    e1.set(invincible)
    checkbutton1 = tk.Checkbutton(frame, variable=e1)
    checkbutton1.grid(row=0, column=1)
    # label for the back_wards_movement setting
    label2 = tk.Label(frame, text="Backwards movement")
    label2.grid(row=1, column=0)
    # checkbutton for the back_wards_movement setting
    e2 = tk.BooleanVar()
    e2.set(back_wards_movement)
    checkbutton2 = tk.Checkbutton(frame, variable=e2)
    checkbutton2.grid(row=1, column=1)
    # label for the show_fps setting
    label3 = tk.Label(frame, text="Show fps")
    label3.grid(row=2, column=0)
    # checkbutton for the show_fps setting
    e3 = tk.BooleanVar()
    e3.set(show_fps)
    checkbutton3 = tk.Checkbutton(frame, variable=e3)
    checkbutton3.grid(row=2, column=1)

    # creating a apply button
    apply_button = tk.Button(window, text="Apply", width=10,height=2, command=lambda: apply_settings(window, e1.get(), e2.get(), e3.get()))
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
        self.an_images = [resized_an_player1, resized_an_player2]
        self.index = 0
        # finding out on what is the player standing on
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
        elif self.direction == "backward" and back_wards_movement:
            change_in_y = -self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
    
    def draw(self, screen):
        global change_in_y
        self.index +=0.1
        if self.index >= 1.1:
            self.index = 0
        if change_in_y == 0:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.an_images[round(self.index)], (self.rect.x, self.rect.y))

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
        rand = random.randint(0, 5)
        if rand == 0:
            self.image = water_images[1]
        else:
            self.image = water_images[0]
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

# setting up sounds
splash_sound = mixer.Sound('splash_sound.mp3')
game_over_sound = mixer.Sound('game_over_sound.mp3')
power_up_pickup_sound = mixer.Sound('powerup_pickedup.mp3')
car_horn_sound = mixer.Sound('car_horn.mp3')

# creating the backgrounds group
backgrounds_group = pygame.sprite.Group()

# creating a settings button
settings_button = pygame.image.load('settings.png')
resized_settings_button = pygame.transform.scale(settings_button, (50, 50))

# creating the player
player_image = pygame.image.load('frog.png')
resized_player = pygame.transform.scale(player_image, (38, 38))
an_player1 = pygame.image.load('frog1.png')
resized_an_player1 = pygame.transform.scale(an_player1, (38,38))
an_player2 = pygame.image.load('frog2.png')
resized_an_player2 = pygame.transform.scale(an_player2, (38, 38))
player = Player()

# obstacle image
obstacle_image = pygame.image.load('temporary_obstacle.png')
obstacle_image_red = pygame.image.load('temporary_obstacle_red.png')
obstacle_image_yellow = pygame.image.load('temporary_obstacle_yellow.png')
obstacle_image_purple = pygame.image.load('temporary_obstacle_purple.png')
obstacle_image_pink = pygame.image.load('temporary_obstacle_pink.png')
obstacle_image_blue = pygame.image.load('temporary_obstacle_blue.png')
obstacle_image_green = pygame.image.load('temporary_obstacle_green.png')
resized_obstacles = [pygame.transform.scale(obstacle_image, (100, 50)), 
                     pygame.transform.scale(obstacle_image_red, (100, 50)), 
                     pygame.transform.scale(obstacle_image_yellow, (100, 50)), 
                     pygame.transform.scale(obstacle_image_purple, (100, 50)), 
                     pygame.transform.scale(obstacle_image_pink, (100, 50)), 
                     pygame.transform.scale(obstacle_image_blue, (100, 50)), 
                     pygame.transform.scale(obstacle_image_green, (100, 50))]
obstacle_group = pygame.sprite.Group()

# log image
log_image = pygame.image.load('log.png')
resized_log = pygame.transform.scale(log_image, (100, 50))
lilypad_image = pygame.image.load('waterlily.png')
resized_lilypad = pygame.transform.scale(lilypad_image, (50, 50))
water_images = [resized_log, resized_lilypad]
log_group = pygame.sprite.Group()

# setting up a play button
play_button = pygame.image.load('play_button.png')
resized_play_button = pygame.transform.scale(play_button, (300, 100))
scores_button = pygame.image.load('scores_button.png')
resized_scores_button = pygame.transform.scale(scores_button, (300, 100))
back_arrow = pygame.image.load('back_arrow.png')
resized_back_arrow = pygame.transform.scale(back_arrow, (50, 50))
end_game_button = pygame.image.load('exit_button.png')
resized_end_game_button = pygame.transform.scale(end_game_button, (300, 100))
home_button = pygame.image.load('home_button.png')
resized_home_button = pygame.transform.scale(home_button, (50, 50))

# setting up a thread for the spawning of obstacles and logs
spawn_thread = threading.Thread(target=spawn_func)

# special settings
invincible = False
back_wards_movement = True
show_fps = True

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
                # checking if the home button was clicked
                elif screen.get_width()-resized_home_button.get_width() < event.pos[0] < screen.get_width() and resized_settings_button.get_height() < event.pos[1] < resized_settings_button.get_height() + resized_home_button.get_height():
                    start_screen_active = True
    
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

    # background types drawing
    backgrounds_group.draw(screen)

                # drawing everything
    try:
        # drawing the obstacles
        obstacle_group.draw(screen)

        # drawing the logs
        log_group.draw(screen)
    except:
        # weirdly enough, this still sometimes happen, maybe when there is too much sprites?
        print("We hebben een serieus probleem")

    # drawing the player
    player.draw(screen)

    # resetting the change_in_y(if this is not done, the logs would never stop moving)
    # this has to be done after drawing the player, since player.draw uses it
    change_in_y = 0

    # drawing a settings button
    screen.blit(resized_settings_button, (screen.get_width()-resized_settings_button.get_width(), 0))

    # drawing a home button
    screen.blit(resized_home_button, (screen.get_width()-resized_home_button.get_width(), resized_settings_button.get_height()))

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
                pass
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
        if on_water == 2 and not invincible and not temp:
            splash_sound.play()
            end_screen("water")

    # checking for collisions between player and obstacles
    if pygame.sprite.spritecollide(player, obstacle_group, False) and not invincible:
        car_horn_sound.play()
        end_screen("car")

    # checking if player left the screen
    if player.rect.x < 0 - resized_player.get_width() and not invincible or player.rect.x > screen.get_width() and not invincible:
        game_over_sound.play()
        end_screen("left")

    # updating the player(checking if the player is on a water background)
    player.update()

    # updating the backgrounds
    backgrounds_group.update()

    # displaying fps
    if show_fps:
        fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
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
    
    # checking if a log or obstacle is touching another log or obstacle(this prevents a bug where the player could move twice as fast to the side by sitting on two logs at the same time)
    # also this makes the game more playable
    # they also have to check only the logs and obstacles on a similar y coordinate
    for log in log_group:
        for log1 in log_group:
            if log != log1:
                # probably not the best way to do this, but hopefully it works(there is no simple way to check, however I think it makes sense)
                tmp = False
                if abs(log.rect.y - log1.rect.y) < 48:
                    tmp = True
                # currently it also checks if they have the same direction, because otherwise its deleting just about every second log
                if pygame.sprite.collide_rect(log, log1) and tmp and log.direction == log1.direction:
                    log_group.remove(log)
            else:
                pass
    # the same goes for the obstacles
    for obstacle in obstacle_group:
        for obstacle1 in obstacle_group:
            if obstacle != obstacle1:
                tmp = False
                if abs(obstacle.rect.y - obstacle1.rect.y) < 48:
                    tmp = True
                if pygame.sprite.collide_rect(obstacle, obstacle1) and tmp and obstacle.direction == obstacle1.direction:
                    obstacle_group.remove(obstacle)

    # updating the screen and setting the frames per second
    clock.tick(60)
    pygame.display.update()

# waiting for the thread to finish(this prevents an error when the code tryes to spawn an obstacle or log on a non existing window)
while not quited:
    pass
pygame.quit()