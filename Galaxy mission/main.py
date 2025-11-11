import pgzrun
import os
import random
os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 720/1.2
HEIGHT = 1280/1.2

# Values
score = 0
bosssets = 0
bossdirection = 1

# Actors
ship = Actor("ship")
beam = Actor("beam")
boss = Actor("boss")

# positions
ship.x = WIDTH/2
ship.y = 1200/1.2
boss.x = WIDTH/2
boss.y = 80/1.2

# Lists
bossbullets = []
bugs1 = []
bullets = []

def bugs():
    for i in range(7):
        for j in range(7):
            bug = Actor("bug")
            bug.x = 45 + i * 100
            bug.y = 40 + j * 50
            bug.speed = random.uniform(0.6, 1.4)
            bugs1.append(bug)

def draw():
    screen.blit("space", (0,0))
    ship.draw()
    for b in bugs1:
        b.draw()

    for l in bullets:
        l.draw()

    if boss:
        boss.draw()
    screen.draw.text(f"Score: {score}", ((10/1.2), (10/1.2)), fontsize = 30)

def update():
    global score, bullets, bugs1, boss, bosssets, bossdirection
    if keyboard.a:
        ship.x -= 10
    if keyboard.d:
        ship.x += 10
        
# Boss Speed
    if boss:
        # boss.speed = 1
        # boss.y += boss.speed
        # boss.x += boss.speed
        boss.x += bossdirection * 4
        # boss.y += bossdirection * 4
        if boss.x >= WIDTH - 50 or boss.x <= 50:
            bossdirection *= -1

    for b in bugs1:
        b.y += b.speed
        for l in bullets:
            l.y -= 1
            if l.colliderect(b):
                bugs1.remove(b)
                bullets.remove(l)
                score += 1
    if boss:
        for l in bullets:
            l.y -= 1
            if l.colliderect(boss):
                bosssets += 1
                bullets.remove(l)
                if bosssets >= 20:
                    score += 10
                    boss = None
                    break

def on_key_down(key):
    global bullets
    if key == keys.W:
        beam = Actor("beam")
        beam.x = ship.x
        beam.y = ship.y
        bullets.append(beam)

bugs()
pgzrun.go()