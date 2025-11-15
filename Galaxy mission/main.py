import pgzrun
import os
import random
os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 720/1.2
HEIGHT = 1280/1.2

score = 0
bosssets = 0
bossdirection = 1
game_over = False

ship = Actor("ship")
beam = Actor("beam")
boss = Actor("boss")

ship.x = WIDTH/2
ship.y = 1200/1.2
boss.x = WIDTH/2
boss.y = 80/1.2

# Lists
bossbullets = []
bugs1 = []
bullets = []

boss_shoot_timer = 0
BOSS_SHOOT_DELAY = 30

def bugs():
    for i in range(7):
        for j in range(7):
            bug = Actor("bug")
            bug.x = 45 + i * 100
            bug.y = 40 + j * 50
            bug.speed = random.uniform(0.6, 2)
            bugs1.append(bug)

def draw():
    screen.blit("space", (0,0))
    ship.draw()
    for b in bugs1:
        b.draw()

    for l in bullets:
        l.draw()

    for b in bossbullets:
        b.draw()

    if boss:
        boss.draw()

    if game_over:
        screen.draw.text("GAME OVER", center = (WIDTH/2, HEIGHT/2), fontsize = 50, fontname = "myfont", color = "red")

    screen.draw.text(f"Score: {score}", (10/1.2, 10/1.2), fontsize = 30, fontname = "myfont", color = "blue")

def update():
    global score, bullets, bugs1, boss, bosssets, bossdirection, boss_shoot_timer, game_over

    if not game_over:
        if keyboard.a:
            ship.x -= 10
        if keyboard.d:
            ship.x += 10 

        if boss:
            boss.x += bossdirection * 4
            if boss.x >= WIDTH - 50 or boss.x <= 50:
                bossdirection *= -1

        for b in bugs1:
            b.y += b.speed
            for l in bullets[:]:
                l.y -= 1
                if l.colliderect(b):
                    bugs1.remove(b)
                    bullets.remove(l)
                    score += 1

        if boss:
            for l in bullets[:]:
                l.y -= 1
                if l.colliderect(boss):
                    bosssets += 1
                    bullets.remove(l)
                    if bosssets >= 20:
                        score += 10
                        boss = None
                        break

        boss_shoot_timer += 1
        if boss and boss_shoot_timer >= BOSS_SHOOT_DELAY:
            beam = Actor("beam")
            beam.x = boss.x
            beam.y = boss.y
            bossbullets.append(beam)
            boss_shoot_timer = 0

        for b in bossbullets:
            b.y += 5
            if b.colliderect(ship):
                game_over = True
            elif b.y > HEIGHT:
                bossbullets.remove(b)

def on_key_down(key):
    global bullets
    if key == keys.W:
        beam = Actor("beam")
        beam.x = ship.x
        beam.y = ship.y
        bullets.append(beam)

bugs()
pgzrun.go()