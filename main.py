from turtle import Screen, Turtle, register_shape, listen, onkey
import random
import math
import winsound

ws = Screen()
ws.bgcolor('black')
ws.bgpic('background.gif')
ws.title('Space Invaders')
ws.setup(600, 700)

border = Turtle()
border.color('white')
border.hideturtle()

register_shape('invader1.gif')
register_shape('invader2.gif')
register_shape('invader3.gif')
register_shape('invader4.gif')
register_shape('player.gif')

ws.tracer(0)
bullet = Turtle()
bullet.hideturtle()
bullet.color('blue')
bullet.shape('triangle')
bullet.turtlesize(0.7)
bullet.setheading(90)
bullet.penup()
bullet.setposition(0, -300)

player = Turtle()
player.shape('player.gif')
player.penup()
player.setposition(0, -300)

writer = Turtle()
writer.hideturtle()
writer.color('white')
writer.penup()
ws.tracer(1)

invaders_speed = 10
list_invaders = []

bullet_status = 'ready'

score = 0


def start_fire():
    global bullet_status
    if bullet_status == 'ready':
        winsound.PlaySound('lazer.wav', winsound.SND_ASYNC)
        bullet_status = 'fire'
        bullet.setposition(player.xcor(), player.ycor() + 30)
        bullet.showturtle()


def create_border():
    ws.tracer(0)
    border.penup()
    border.goto(300, 0)
    border.goto(300, -350)
    border.pendown()
    for i in range(4):
        border.left(90)
        if i % 2 == 0:
            border.forward(700)
        else:
            border.forward(600)
    ws.tracer(1)


def write_score():
    ws.tracer(0)
    writer.goto(-290, 300)
    writer.pendown()
    writer.write(f'Score: {score}', font=('Arial', 20, 'normal'))
    writer.penup()
    ws.tracer(1)


def invaders():
    global list_invaders
    ws.tracer(0)
    for i in range(5):
        invader = Turtle()
        invader.penup()
        invader.shape(f'invader{random.randint(1, 4)}.gif')
        invader.goto(random.randint(-260, 260), random.randint(0, 300))
        list_invaders.append(invader)
    ws.tracer(1)


def collision(object1, object2):
    distance = math.sqrt(math.pow(object1.xcor() - object2.xcor(), 2) + math.pow(object1.ycor() - object2.ycor(), 2))
    if distance < 30:
        return True
    else:
        return False


def move_left():
    x = player.xcor()
    x -= 20
    if x < -260:
        x = -260
    player.setx(x)


def move_right():
    x = player.xcor()
    x += 20
    if x > 260:
        x = 260
    player.setx(x)


create_border()
invaders()

ws.listen()
ws.onkey(move_left, 'Left')
ws.onkey(move_right, 'Right')
ws.onkey(start_fire, 'space')

write_score()

while True:
    for i1 in range(len(list_invaders)):
        x = list_invaders[i1].xcor() + invaders_speed
        list_invaders[i1].setx(x)
        if list_invaders[i1].xcor() > 260:
            for i in list_invaders:
                y = i.ycor()
                y -= 30
                i.sety(y)
            invaders_speed *= -1
        if list_invaders[i1].xcor() < -260:
            for i in list_invaders:
                y = i.ycor()
                y -= 30
                i.sety(y)
            invaders_speed *= -1
        if list_invaders[i1].ycor() < -350:
            list_invaders[i1].hideturtle()
            del list_invaders[i1]
            ws.tracer(0)
            invader = Turtle()
            invader.penup()
            invader.shape(f'invader{random.randint(1, 4)}.gif')
            invader.goto(random.randint(-260, 260), random.randint(300, 350))
            list_invaders.append(invader)
            ws.tracer(1)
        if collision(list_invaders[i1], bullet):
            winsound.PlaySound('explosion.wav', winsound.SND_ASYNC)
            score += 10
            writer.clear()
            write_score()
            bullet.hideturtle()
            bullet_status = 'ready'
            bullet.setposition(0, -300)
            list_invaders[i1].hideturtle()
            del list_invaders[i1]
            ws.tracer(0)
            invader = Turtle()
            invader.penup()
            invader.shape(f'invader{random.randint(1, 4)}.gif')
            invader.goto(random.randint(-260, 260), random.randint(300, 350))
            list_invaders.append(invader)
            ws.tracer(1)
    if bullet_status == 'fire':
        y = bullet.ycor() + 50
        bullet.sety(y)
    if bullet.ycor() > 350:
        bullet.hideturtle()
        bullet_status = 'ready'
