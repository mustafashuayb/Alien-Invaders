import turtle
import random
import time

# -----------------------
# Screen
# -----------------------
wn = turtle.Screen()
wn.title("Alien Invaders")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# -----------------------
# Stars
# -----------------------
stars = []
for _ in range(40):
    s = turtle.Turtle()
    s.shape("circle")
    s.color("white")
    s.penup()
    s.shapesize(0.1, 0.1)
    s.goto(random.randint(-300, 300), random.randint(-300, 300))
    stars.append(s)

# -----------------------
# UI
# -----------------------
pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(0, 260)

def update_ui(score, lives, level):
    pen.clear()
    pen.write(f"Score: {score}   Lives: {lives}   Level: {level}",
              align="center", font=("Arial", 14, "normal"))

# -----------------------
# Player
# -----------------------
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.setheading(90)
player.goto(0, -250)
player_speed = 15

# -----------------------
# Bullet
# -----------------------
bullet = turtle.Turtle()
bullet.shape("triangle")
bullet.color("yellow")
bullet.penup()
bullet.setheading(90)
bullet.hideturtle()
bullet_speed = 12
bullet_state = "ready"

# -----------------------
# Aliens
# -----------------------
aliens = []
colors = ["red", "orange", "purple"]
alien_speed = 1.50

def clear_aliens():
    for alien in aliens:
        alien.hideturtle()
    aliens.clear()

def create_aliens(level):
    clear_aliens()
    if level % 5 != 0:
        for _ in range(3 + level):
            alien = turtle.Turtle()
            alien.shape("square")
            alien.color(random.choice(colors))
            alien.penup()
            alien.goto(random.randint(-250, 250), random.randint(100, 250))
            aliens.append(alien)


# Boss

boss = None
boss_hits_needed = 5
boss_direction = 1
boss_active = False
# Boss Health Bar
health_bar = turtle.Turtle()
health_bar.hideturtle()
health_bar.penup()
health_bar.goto(-50, 280)
health_bar.color("green")
health_bar.width(8)
# Boss Laser Setup
laser = turtle.Turtle()
laser.hideturtle()
laser.shape("square")
laser.color("red")
laser.penup()
laser_speed = 8
laser_active = False
laser.shapesize(stretch_wid=20, stretch_len=0.3)


def spawn_boss():
    global boss, boss_hits_needed, boss_direction, boss_active
    clear_aliens()  # remove all normal aliens
    boss = turtle.Turtle()
    boss.shape("square")
    boss.color("darkred")
    boss.shapesize(2, 2)
    boss.penup()
    boss.goto(0, 250)
    boss_hits_needed = 5
    boss_direction = 1
    boss_active = True
    laser.hideturtle()

def update_health_bar():
    health_bar.clear()
    health_bar.goto(-50, 280)
    health_bar.color("green")
    health_bar.forward(boss_hits_needed * 20)
    health_bar.setheading(0)


def boss_defeated_animation():
    bx, by = boss.xcor(), boss.ycor()
    boss.hideturtle()
    laser.hideturtle()

    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("darklime")
    msg.penup()
    msg.goto(0, 0)
    msg.write("BOSS DEFEATED!", align="center", font=("Arial", 40, "bold"))

    # Fireworks
    fireworks = []
    for _ in range(8):
        f = turtle.Turtle()
        f.shape("circle")
        f.color(random.choice(["yellow", "orange", "red", "white"]))
        f.penup()
        f.goto(bx, by)  # use stored position
        f.shapesize(1, 1)
        fireworks.append(f)

    for size in range(1, 6):
        for f in fireworks:
            f.shapesize(size, size)
        wn.update()
        time.sleep(0.05)
    for f in fireworks:
        f.hideturtle()

# -----------------------
# Controls
# -----------------------
def move_left():
    x = player.xcor() - player_speed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor() + player_speed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# -----------------------
# Pause
# -----------------------
paused = False
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pen.goto(0,0)
        pen.write("PAUSED", align="center", font=("Arial", 30, "bold"))
    else:
        pen.goto(0,260)
        update_ui(score, lives, level)

# -----------------------
# Collision
# -----------------------
def check_collision(t1, t2, distance=15):
    return t1.distance(t2) < 20

def explosion(x, y):
    boom = turtle.Turtle()
    boom.shape("circle")
    boom.color("yellow")
    boom.penup()
    boom.goto(x, y)
    for _ in range(3):
        boom.shapesize(2)
        wn.update()
        time.sleep(0.02)
        boom.shapesize(1)
    boom.hideturtle()

# -----------------------
# Game Variables
# -----------------------
score = 0
lives = 3
level = 1
game_over = True
first_start = True

# -----------------------
# Start/Restart Screen
# -----------------------
def start_game():
    global score, lives, level, game_over, alien_speed, bullet_state, first_start, boss_active
    game_over = False
    score = 0
    lives = 3
    level = 1
    alien_speed = 1.0
    bullet_state = "ready"
    boss_active = False
    if boss:
        boss.hideturtle()
    player.goto(0, -250)
    pen.goto(0,260)
    update_ui(score, lives, level)
    create_aliens(level)
    first_start = False

wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")
wn.onkeypress(toggle_pause, "p")
wn.onkeypress(start_game, "Return")

laser.shapesize(stretch_wid=1, stretch_len=0.3)  # thin vertical laser

# Main Game Loop
while True:
    wn.update()

    if game_over:
        pen.goto(0,50)
        pen.clear()
        if first_start:
            pen.write("ALIEN INVADERS", align="center", font=("Arial", 40, "bold"))
            pen.goto(0,-50)
            pen.write("Press Enter to Start", align="center", font=("Arial", 30, "bold"))
        else:
            pen.write("GAME OVER", align="center", font=("Arial", 40, "bold"))
            pen.goto(0,-50)
            pen.write("Press Enter to Restart", align="center", font=("Arial", 30, "bold"))
        time.sleep(0.1)
        continue

    if paused:
        continue

    # Move stars
    for s in stars:
        y = s.ycor() - 1
        if y < -300:
            y = 300
        s.sety(y)

    # Move bullet
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    # Move aliens (if boss not active)
    if not boss_active:
        for alien in aliens:
            alien.sety(alien.ycor() - alien_speed)

            if check_collision(bullet, alien):
                explosion(alien.xcor(), alien.ycor())
                bullet.hideturtle()
                bullet_state = "ready"
                alien.goto(random.randint(-250, 250), random.randint(100, 250))
                alien.color(random.choice(colors))
                score += 1

                # Level up every 10 points
                if score % 10 == 0:
                    level += 1
                    alien_speed += 0.3
                    lives = 3
                    if level % 5 == 0:
                        spawn_boss()
                    create_aliens(level)
                update_ui(score, lives, level)

            # Alien reaches bottom
            if alien.ycor() < -260:
                lives -= 1
                update_ui(score, lives, level)
                alien.goto(random.randint(-250, 250), random.randint(100, 250))

            # Alien hits player
            if check_collision(player, alien):
                lives -= 1
                update_ui(score, lives, level)
                alien.goto(random.randint(-250, 250), random.randint(100, 250))

            if lives <= 0:
                game_over = True
                pen.goto(0,0)

    # Boss movement and laser
    if boss_active and boss:
        # Move boss
        boss.setx(boss.xcor() + boss_direction * 2)
        if boss.xcor() > 250 or boss.xcor() < -250:
            boss_direction *= -1

        # Random laser shooting (~1 sec cooldown)
        if not laser_active and random.randint(0, 50) == 0:
            laser_active = True
            laser.goto(boss.xcor(), boss.ycor() - 30)
            laser.showturtle()

        # Move laser vertically
        if laser_active:
            laser.sety(laser.ycor() - laser_speed)
            if laser.ycor() < -260:
                laser.hideturtle()
                laser_active = False
            elif check_collision(laser, player, distance=15):
                lives -= 1
                laser.hideturtle()
                laser_active = False
                update_ui(score, lives, level)
                if lives <= 0:
                    game_over = True

        # Bullet hits boss
        if check_collision(bullet, boss):
            bullet.hideturtle()
            bullet_state = "ready"
            boss_hits_needed -= 1
            explosion(boss.xcor(), boss.ycor())
            update_health_bar()
            if boss_hits_needed <= 0:
                boss_defeated_animation()
                boss_active = False
                boss.hideturtle()
                lives = 3
                update_ui(score, lives, level)

    time.sleep(0.02)