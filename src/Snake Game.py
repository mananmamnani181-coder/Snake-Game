import pygame
import random
import os
import sys
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
screen_width=900
screen_height=600
pygame.init()
def resource_path(filename):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)
def highscore_path():
    if getattr(sys, "frozen", False):
        base_path = os.path.join(os.environ["LOCALAPPDATA"], "SnakeGame")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, "highscore.txt")
bgmig = pygame.image.load(resource_path("background.jpg"))
gameWin = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()
font = pygame.font.SysFont(None,55)
if not os.path.exists(highscore_path()):
    with open(highscore_path(), 'w') as f:
        f.write("0")
with open(highscore_path(), "r") as f:
    highscore = f.read()
clock=pygame.time.Clock()
def screen_score(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWin.blit(screen_text,[x,y])  
def plot_snake(gameWin, color,snk_list,snake_size):
 for x,y in snk_list:
   pygame.draw.rect(gameWin, color, [x, y, snake_size, snake_size])
def welcome():
    global bgmig
    bgmig = pygame.transform.scale(bgmig,(screen_width,screen_height)).convert_alpha()
    exit_game = False
    while not exit_game:
        gameWin.fill(white)
        screen_score("Welcome to Snakes",black,260,250)
        screen_score("Press Spacebar to play",black,232,290)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(resource_path("back.mp3"))
                    pygame.mixer.music.play()
                    gameloop()               
        pygame.display.update()
        clock.tick(60)
def gameloop():
    global bgmig
    global highscore
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocityx=0
    velocityY=0
    score =0
    foodX=random.randint(20,screen_width//2)
    foodY=random.randint(20,screen_height//2)
    snake_size = 30
    init_velocity = 5
    snk_list =[]
    snk_length = 1
    fps = 60
    while not exit_game:
        bgmig = pygame.transform.scale(bgmig,(screen_width,screen_height)).convert_alpha()
        if game_over:
            with open(highscore_path(),"w") as f:
             f.write(str(highscore))
            gameWin.fill(white)
            screen_score("Game Over! Press Enter to continue",red,100,250)
            for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                    exit_game = True
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                   welcome() 
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        exit_game = True
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                        snake_x+=10
                        velocityx =init_velocity
                        velocityY=0
                    if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                        snake_x-=10
                        velocityx = -init_velocity
                        velocityY=0
                    if event.key == pygame.K_UP or event.key==pygame.K_w:
                        snake_y-=10
                        velocityY=-init_velocity
                        velocityx=0
                    if event.key == pygame.K_DOWN or event.key==pygame.K_s:
                        snake_y+=10
                        velocityY=init_velocity
                        velocityx=0
                    if event.key == pygame.K_q:
                        score+=10
                        
            snake_x+=velocityx
            snake_y+=velocityY
            if abs(snake_x-foodX)<10 and abs(snake_y-foodY)<10:
                score+=10
                foodX=random.randint(20,screen_width//2)
                foodY=random.randint(20,screen_height//2)
                snk_length+=5
                if score>int(highscore):
                    highscore = score
            gameWin.fill(white)  
            gameWin.blit(bgmig,(0,0)) 
            screen_score("Score: "+str(score)+"  Highscore: "+str(highscore),red,5,5)  
            pygame.draw.rect(gameWin,black,[snake_x,snake_y,snake_size,snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if len(snk_list)>snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over=True
                pygame.mixer.music.load(resource_path('Gameover.mp3'))
                pygame.mixer.music.play()
            pygame.draw.rect(gameWin,red,[foodX,foodY,snake_size,snake_size])
            plot_snake(gameWin,black,snk_list,snake_size)
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over =True
                pygame.mixer.music.load(resource_path('Gameover.mp3'))
                pygame.mixer.music.play()
        pygame.display.update() 
        clock.tick(fps)  
    pygame.quit()
    sys.exit()
welcome()
