import turtle
import math
import random

# window setup
wn = turtle.Screen()
wn.title("Space Defense")
wn.setup(width=800, height=800)
wn.bgcolor("black")
wn.tracer(0)

player_vertices = ((0, 15), (-15, 0), (-18, 5), (-18, -5), (0, 0), (18, -5), (18, 5), (15, 0))
wn.register_shape("player", player_vertices)


class Sprite(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()


def get_heading_to(t1, t2):
    x1 = t1.xcor()
    y1 = t1.ycor()

    x2 = t2.xcor()
    y2 = t2.ycor()

    heading = math.atan2(y1 - y2, x1 - x2)
    heading = heading * 180.0 / math.pi

    return heading


player = Sprite()
player.color("white")
player.shape("player")
player.score = 0

missile = Sprite()
missile.color("red")
missile.shape("arrow")
missile.speed = 7
missile.state = "ready"
missile.hideturtle()

pen = Sprite()
pen.color("white")
pen.hideturtle()
pen.goto(0, 350)
pen.write("Score: 0", False, align="center", font=("Arial", 24, "normal"))


asteroids = []

for _ in range(5):
    asteroid = Sprite()
    asteroid.color("yellow")
    asteroid.shape("circle")
    asteroid.speed = 0.3
    asteroid.goto(0, 0)
    heading = random.randint(0, 360)
    distance = random.randint(400, 600)
    asteroid.setheading(heading)
    asteroid.fd(distance)
    asteroid.setheading(get_heading_to(player, asteroid))
    asteroids.append(asteroid)


def rotate_left():
    player.lt(10)


def rotate_right():
    player.rt(10)


def fire_missile():
    if missile.state == "ready":
        missile.goto(0, 0)
        missile.showturtle()
        missile.setheading(player.heading())
        missile.state = "fire"


# keyboard binding
wn.listen()
wn.onkey(rotate_left, "Left")
wn.onkey(rotate_right, "Right")
wn.onkey(fire_missile, "space")

# main game loop
while True:
    wn.update()
    player.goto(0, 0)

    # move missile
    if missile.state == "fire":
        missile.fd(missile.speed)

    # boarder checking
    if missile.xcor() > 400 or missile.xcor() < -400 or missile.ycor() > 400 or missile.ycor() < -400:
        missile.hideturtle()
        missile.state = "ready"

    # iterate through asteroids
    for asteroid in asteroids:

        # move asteroid
        asteroid.fd(asteroid.speed)

        # check for collision
        # asteroid and missile
        if asteroid.distance(missile) < 20:
            # reset asteroid
            heading = random.randint(0, 360)
            distance = random.randint(800, 1000)
            asteroid.setheading(heading)
            asteroid.fd(distance)
            asteroid.setheading(get_heading_to(player, asteroid))
            asteroid.speed += 0.07

            # reset missile
            missile.goto(1000, 1000)
            missile.hideturtle()
            missile.state = "ready"

            # increase score
            player.score += 10
            pen.clear()
            pen.write("Score: {}".format(player.score), False, align="center", font=("Arial", 24, "normal"))

        if asteroid.distance(player) < 20:
            # reset asteroid
            heading = random.randint(0, 360)
            distance = random.randint(800, 1000)
            asteroid.setheading(heading)
            asteroid.fd(distance)
            asteroid.setheading(get_heading_to(player, asteroid))
            asteroid.speed += 0.5
            print("You were killed!")
            player.score -= 50
            pen.clear()
            pen.write("Score: {}".format(player.score), False, align="center", font=("Arial", 24, "normal"))

# wn.mainloop()
