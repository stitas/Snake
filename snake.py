import pygame, random, time

#WIDTH AND HEIGHT OF WINDOW
WIDTH, HEIGHT = 601,551

#SNAKE HEAD STARTING POSITONS
POS_X=300
POS_Y=250

#CHANGE OF SNAKE HEADS POSITION
POS_X_CHANGE=0
POS_Y_CHANGE=0

#CREATES WINDOW
WIN=pygame.display.set_mode((WIDTH,HEIGHT))

#RENAMES GAME WINDOW
pygame.display.set_caption('Snake')

#COLORS
COLOR=(0,0,0)
COLOR1=(16,16,16)
SNAKE_COLOR=(0,255,0)
FOOD_COLOR=(255,0,0)

#POSITIONS OF DIFFERNT TEXTS
SCORE_POS_X,SCORE_POS_Y=0,521
LABEL_POS_X,LABEL_POS_Y=5,0
HIGH_SCORE_POS_X,HIGH_SCORE_POS_Y=254,521

#GRID DIAMETERS
POS_X_GRID=list(range(-10,601,10))
POS_Y_GRID=list(range(50,511,10))

#FPS
FPS=10

#SOUND EFFECTS
pygame.mixer.init()
GAME_OVER=pygame.mixer.Sound('GAME_OVER.mp3')
EAT=pygame.mixer.Sound('EAT.mp3')

#TEXT FONT
pygame.font.init()
FONT_SCORE=pygame.font.Font('font.ttf',25)
FONT_LABEL=pygame.font.Font('font.ttf',50)

#PROGRAM ICON
ICON=pygame.image.load('snake.png')
pygame.display.set_icon(ICON)

#DRAWS THE WINDOW OF PROGRAM
def draw_window():
    WIN.fill(COLOR)

#DRAWS THE GRID OF THE SNAKE
def draw_grid():
    for i in POS_X_GRID:
        for l in POS_Y_GRID:
            pygame.draw.rect(WIN,COLOR1,[i,l,1,10])
            pygame.draw.rect(WIN,COLOR1,[i,l,10,1])

#DRAWS SNAKE BODY
def snake():
    for i in SNAKE_LIST:
        pygame.draw.rect(WIN,SNAKE_COLOR,[i[0],i[1],10,10])

#DRAWS SCORE OF CURRENT GAME
def score(p_score):
    value=FONT_SCORE.render('SCORE:'+ str(p_score)+', ',True, SNAKE_COLOR)
    WIN.blit(value,[SCORE_POS_X,SCORE_POS_Y])

#DRAWS "<SNAKE GAME>"
def label():
    value=FONT_LABEL.render('<SNAKE GAME>',True,SNAKE_COLOR)
    WIN.blit(value,[LABEL_POS_X,LABEL_POS_Y])

#DRAWS HIGH SCORE
def high_score(SCORE):
    with open('high_score.txt','r+') as file:
        high_score=file.read()
        if int(high_score)<SCORE:
            file.seek(0)
            file.truncate()
            file.write(str(SCORE))
        file.close()

    value=FONT_SCORE.render('HIGH SCORE:'+str(high_score),True,SNAKE_COLOR)
    WIN.blit(value,[HIGH_SCORE_POS_X,HIGH_SCORE_POS_Y])

#SNAKES BODY
SNAKE_LIST = [[POS_X-10,POS_Y],[POS_X-20,POS_Y],[POS_X,POS_Y]]

#MAIN GAME LOOP
def main():
    clock=pygame.time.Clock()
    run=True
    FOOD_POS = (400,250)
    SNAKE_LENGTH = 3
    while run:
        global FPS
        global POS_X_CHANGE
        global POS_Y_CHANGE
        global POS_X
        global POS_Y

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #MOVEMENT KEYS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and POS_X%10==0 and SNAKE_LIST[-1][0]<=SNAKE_LIST[-2][0]:
                        POS_X_CHANGE = -10
                        POS_Y_CHANGE = 0

                if event.key == pygame.K_RIGHT and POS_X%10==0 and SNAKE_LIST[-1][0]>=SNAKE_LIST[-2][0]:
                        POS_X_CHANGE = 10
                        POS_Y_CHANGE = 0

                if event.key == pygame.K_UP and POS_Y%10==0 and SNAKE_LIST[-1][1]<=SNAKE_LIST[-2][1]:
                        POS_Y_CHANGE = -10
                        POS_X_CHANGE = 0

                if event.key == pygame.K_DOWN and POS_Y%10==0 and SNAKE_LIST[-1][1]>=SNAKE_LIST[-2][1]:
                        POS_Y_CHANGE = 10
                        POS_X_CHANGE = 0

        #CHANGES POSITION OF SNAKE HEAD
        POS_X += POS_X_CHANGE
        POS_Y += POS_Y_CHANGE

        #MAKES BOUNDRIES
        if POS_X == 600 or POS_X == -10:
            GAME_OVER.play()
            time.sleep(1.5)
            quit()

        if POS_Y == 520 or POS_Y == 40:
            GAME_OVER.play()
            time.sleep(1.5)
            quit()

        #CONNECTS SNAKE BODY TO SNAKE HEAD
        if POS_X_CHANGE == 10 or POS_X_CHANGE == -10 or POS_Y_CHANGE == 10 or POS_Y_CHANGE == -10:
            SNAKE_HEAD=[]
            SNAKE_HEAD.append(POS_X)
            SNAKE_HEAD.append(POS_Y)
            SNAKE_LIST.append(SNAKE_HEAD)

            if len(SNAKE_LIST)>SNAKE_LENGTH:
                del SNAKE_LIST[0]

            #IF THE SNAKE HITS IT SELF GAME ENDS
            for i in SNAKE_LIST[:-1]:
                if i == SNAKE_HEAD:
                    GAME_OVER.play()
                    time.sleep(1.5)
                    run=False

        draw_window()
        draw_grid()
        snake()

        SCORE = SNAKE_LENGTH - 3

        #DRAWS SNAKE HEAD
        pygame.draw.rect(WIN,SNAKE_COLOR,[POS_X,POS_Y,10,10])
        #DRAWS FOOD
        pygame.draw.rect(WIN,FOOD_COLOR,[FOOD_POS[0], FOOD_POS[1], 10, 10])

        #CHECKS IF THE SNAKE HAS EATEN HER FOOD AND IF SO MAKES THE SNAKE LONGER AND SPAWNS ANOTHER FOOD
        if POS_X == FOOD_POS[0] and POS_Y == FOOD_POS[1]:
            COLLISION = True
            while COLLISION:
                FOOD_POS = random.randrange(0,600,10),random.randrange(50,500,10)
                EAT.play()
                if list(FOOD_POS) in SNAKE_LIST[:-1]:
                    continue
                else:
                    COLLISION = False
            SNAKE_LENGTH += 1
            FPS += 0.2

        score(SNAKE_LENGTH - 3)
        high_score(SCORE)
        label()

        #UPDATES DISPLAY
        pygame.display.update()

    pygame.quit()

if __name__=='__main__':
    main()