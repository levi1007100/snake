#made by leo pantar
#use arrows to control
#don't bump into black
#eat red
#don't bump into wall

import pygame,sys,random,os,time

clock=pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption("snake")

WINDOW_SIZE=(800,800)
screen=pygame.display.set_mode(WINDOW_SIZE,0,32)




def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_map(path):
    f=open(path+".txt","r")
    data=f.read()
    f.close()
    data=data.split("\n")
    game_map=[]
    for row in data:
        game_map.append(list(row))
    return game_map


def define_snake_body():
    row,column=find_snake()
    return [[row,column+1,"east"],[row,column]]

def find_snake():
    for row in range(0,row_length,1):
        for column in range(0,column_length,1):
            if(field[row][column]=="X"):
                return row,column

def render_field():
    for row in range(0,row_length,1):

        for column in range(0,column_length,1):
            if(field[row][column]=="."):
                color=(144,144,144)
            if(field[row][column]=="X"):
                color=(0,200,0)
            if(field[row][column]=="#"):
                color=(0,0,0)
            if(field[row][column]=="*"):
                color=fruit_color
            pygame.draw.rect(screen,color,pygame.Rect(WINDOW_SIZE[1]/column_length*column,
            WINDOW_SIZE[0]/row_length*row,WINDOW_SIZE[1]/column_length,
            WINDOW_SIZE[0]/row_length))




def make_field_without_snake():
    for row in range(0,row_length,1):
        for column in range(0,column_length,1):
            if(field[row][column]=="X"):
                field[row][column]="."

def move_snake():
    for ind in range(len(snake_body)-1,0,-1):
        snake_body[ind][0]=snake_body[ind-1][0]
        snake_body[ind][1]=snake_body[ind-1][1]

def insert_snake():
    for ind in range(len(snake_body)-1,0,-1):
        field[snake_body[ind][0]][snake_body[ind][1]]="X"

def change_where_snake_is_going(direction):
    if(direction=="north"):
        snake_body[0][0],snake_body[0][1]=snake_body[1][0]-1,snake_body[1][1]
    if(direction=="east"):
        snake_body[0][0],snake_body[0][1]=snake_body[1][0],snake_body[1][1]+1
    if(direction=="south"):
        snake_body[0][0],snake_body[0][1]=snake_body[1][0]+1,snake_body[1][1]
    if(direction=="west"):
        snake_body[0][0],snake_body[0][1]=snake_body[1][0],snake_body[1][1]-1

def check_for_collisions():

    if(snake_body[0][0]>row_length-1 or snake_body[0][0]<0):
        return True
    if(snake_body[0][1]>column_length-1 or snake_body[0][1]<0):
        return True
    if(field[snake_body[0][0]][snake_body[0][1]]!="." ):
        if(field[snake_body[0][0]][snake_body[0][1]]=="*" ):
            grow_snake()
            generate_fruit()
            return False
        return True

    return False

def grow_snake():
    global score
    snake_body.append([0,0])
    score+=1

def generate_fruit():
    global fruit_color
    row=random.randint(0,row_length-1)
    column=random.randint(0,column_length-1)
    while field[row][column]!=".":
        row=random.randint(0,row_length-1)
        column=random.randint(0,column_length-1)

    fruit_color=(random.randint(200,255),0,0)
    field[row][column]="*"

def determine_heading():
    if(arrow_value=="north"):
        if(snake_body[0][2]!="south"):
            snake_body[0][2]=arrow_value
    if(arrow_value=="east"):
        if(snake_body[0][2]!="west"):
            snake_body[0][2]=arrow_value
    if(arrow_value=="south"):
        if(snake_body[0][2]!="north"):
            snake_body[0][2]=arrow_value
    if(arrow_value=="west"):
        if(snake_body[0][2]!="east"):
            snake_body[0][2]=arrow_value

fruit_color=(255,0,0)
arrow_value="east"
field=load_map(r"C:\homemade_games\Snake\field")
row_length=len(field)
column_length=len(field[0])
snake_body=define_snake_body()

score = 0
font = pygame.font.SysFont(None, 100)


while 1:
    screen.fill((0,0,0))


    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:

            if event.key==K_RIGHT:
                arrow_value="east"
            if event.key==K_LEFT:
                arrow_value="west"
            if event.key==K_UP:
                arrow_value="north"
            if event.key==K_DOWN:
                arrow_value="south"

    determine_heading()
    change_where_snake_is_going(snake_body[0][2])
    if(check_for_collisions()):
        break


    move_snake()
    make_field_without_snake()
    insert_snake()
    render_field()
    pygame.display.update()
    clock.tick(9)
fill_collor=[255-score*4,255-score*4,255-score*4]

score_collor=[255/(score+1),16*score,16*score]
for ind in range(0,3,1):
    if(score_collor[ind]>255):
        score_collor[ind]=255
    if(score_collor[ind]<1):
        score_collor[ind]=1
    if(fill_collor[ind]>255):
        fill_collor[ind]=255
    if(fill_collor[ind]<1):
        fill_collor[ind]=1
screen.fill(fill_collor)
img = font.render('SCORE : '+str(score), True,(score_collor) )
screen.blit(img, (300, 300))

pygame.display.update()

time.sleep(1.5)
