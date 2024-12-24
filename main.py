import random
import pygame

# Initialize pygame
pygame.init()

# Screen Creation
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

# Load assets
bg = pygame.image.load('bg.png')
bg = pygame.transform.scale(bg, (1000, 1000))
player = pygame.image.load("spaceship.png")
enemy = pygame.image.load("ufo.png")
icon = pygame.image.load('startup.png')
bullet_image = pygame.image.load("bullet_img.png")

# Display and Icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)
overlay = pygame.Surface((1000, 1000), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 255 * 0.75))

# Player and Enemy Collision Box
player_rect = player.get_rect()
enemy_width = enemy.get_width()

# Player Positioning
player_x = (1000 - player.get_width()) // 2
player_y = 900
player_rect.topleft = (player_x, player_y)

# Bullet setup for player
bullet_speed = 20
bullets = []  # List to store active bullets
bullet_cooldown = 200  # milliseconds
last_shot_time_player = 0

# Bullet setup for Enemy
bullet_enemy = pygame.transform.rotate(bullet_image, 180)
bullet_enemy_speed = 20
bullets_enemy = []  # List to store active bullets
bullet_cooldown_enemy = 1500  # milliseconds
last_shot_time_enemy = 0

# Speed
player_speed = 15

# Fonts
font = pygame.font.Font(None, 74)

title_font=pygame.font.Font('AwakenningPersonalUse-DOLPD.ttf', 120)
font_Score = pygame.font.Font(None, 56)
menu_font = pygame.font.Font(None, 48)
matched_font = pygame.font.match_font("arial", bold=True)
player_font = pygame.font.Font(matched_font, 36)
font_dead_message = pygame.font.Font(None, 30)

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

#Score Board
Score=0
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def display_start_screen():
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        screen.blit(overlay, (0, 0))

        draw_text("SPACE  INVADERS", title_font, YELLOW, screen, 500, 400)
        draw_text("Press ENTER to Start", menu_font, WHITE, screen, 500, 550)
        draw_text("Press ESC to Quit", menu_font, WHITE, screen, 500, 600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        pygame.display.update()


def save_name_and_score(name, score):
    scores = []

    # Read existing scores from the file
    try:
        with open(high_score_file, "r") as file:
            for line in file:
                existing_name, existing_score = line.strip().split(":")
                scores.append((existing_name, int(existing_score)))
    except FileNotFoundError:
        pass

    # Add the new score
    scores.append((name, score))

    # Sort scores in descending order and keep only the top 10
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:10]

    # Write updated scores back to the file
    with open(high_score_file, "w") as file:
        for player_name, player_score in scores:
            file.write(f"{player_name}:{player_score}\n")

    print(f"Score saved! {name}: {score}")


#assigning file name
high_score_file='high_score_file.txt'
def get_max_value_from_file(high_score_file):
    scores = {}

    try:
        # Read the existing high scores from the file
        with open(high_score_file, "r") as file:
            for line in file:
                name, score = line.strip().split(":")
                scores[name] = int(score)
    except FileNotFoundError:
        return "No high score found", 0  # If file doesn't exist, return a default value

    # Find the player with the maximum score
    if scores:
        max_name = max(scores, key=scores.get)
        max_score = scores[max_name]
        return max_name, max_score
    else:
        return "No high score", 0  # Return a default if no scores exist

# Initialize multiple enemies
num_enemies = 3
enemies = []  # List to store enemies
for i in range(num_enemies):
    enemy_rect = enemy.get_rect()
    enemy_rect.topleft = (random.randint(0, 1000 - enemy.get_width()), random.randint(0, 500))
    enemy_speed = random.choice([-5, 5])  # Random initial direction
    bullet_cooldown_enemy = random.randint(1000, 2000)
    enemies.append({"rect": enemy_rect, "speed": enemy_speed, "bullets": [], "last_shot_time": bullet_cooldown_enemy})



def display_game_over_screen():
    global Score,death_message
    game_over_running = True
    player_name = ""

    while game_over_running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        screen.blit(overlay, (0, 0))

        draw_text("GAME OVER", font, RED, screen, 500, 300)
        draw_text(f"Score: {Score}", menu_font, YELLOW, screen, 500, 400)

        # Get and display the high score
        high_score_name, high_score_value = get_max_value_from_file(high_score_file)
        draw_text(f"High Score: {high_score_name} - {high_score_value}", menu_font, WHITE, screen, 500, 450)

        draw_text("Enter Your Name:", menu_font, WHITE, screen, 500, 500)
        draw_text(player_name, player_font, YELLOW, screen, 500, 550)

        draw_text("Press ENTER to Submit", menu_font, WHITE, screen, 500, 650)
        draw_text("Press ESC to Quit", menu_font, WHITE, screen, 500, 700)
        draw_text(death_message, font_dead_message, RED, screen, 500, 340)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name.strip():  # Ensure a valid name is entered
                        save_name_and_score(player_name.strip(), Score)
                        Score=0
                        death_message = ""  # Reset death message after submitting
                        return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Remove the last character
                elif len(player_name) < 15:  # Limit name length
                    player_name += event.unicode  # Saving typed character

        pygame.display.update()



# Game Over flag
game_over = False



# Start screen
display_start_screen()

# Main game loop

running = True


# Global variable for death message
death_message = ""

while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    screen.blit(overlay, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        if display_game_over_screen():
            # Reset the game state
            game_over = False
            player_rect.topleft = (player_x, player_y)
            bullets.clear()
            enemies = []
            for i in range(num_enemies):
                enemy_rect = enemy.get_rect()
                enemy_rect.topleft = (random.randint(0, 1000 - enemy.get_width()), random.randint(0, 500))
                enemy_speed = random.choice([-5, 5])
                bullet_cooldown_enemy = random.randint(1000, 2000)
                enemies.append({"rect": enemy_rect, "speed": enemy_speed, "bullets": [], "last_shot_time": bullet_cooldown_enemy})

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += player_speed

        # Enforce player boundaries
        player_rect.x = max(0, min(player_rect.x, 1000 - player.get_width()))
        player_rect.y = max(0, min(player_rect.y, 1000 - player.get_height()))

        # Update enemies
        for enemy_obj in enemies:
            enemy_rect = enemy_obj["rect"]
            enemy_speed = enemy_obj["speed"]

            # Enemy movement
            enemy_rect.x += enemy_speed
            if enemy_rect.x <= 0 or enemy_rect.x >= 1000 - enemy_width:
                enemy_obj["speed"] = -enemy_speed
                enemy_rect.y += 20

            # Firing bullets for enemy
            current_time = pygame.time.get_ticks()
            if current_time - enemy_obj["last_shot_time"] > bullet_cooldown_enemy:
                bullet_enemy_rect = bullet_enemy.get_rect(center=(enemy_rect.centerx, enemy_rect.bottom))
                enemy_obj["bullets"].append(bullet_enemy_rect)
                enemy_obj["last_shot_time"] = current_time

            # Update enemy bullets
            for bullet in enemy_obj["bullets"][:]:
                bullet.y += bullet_enemy_speed
                if bullet.top > 1000:
                    enemy_obj["bullets"].remove(bullet)
                if bullet.colliderect(player_rect):
                    game_over = True
                    death_message="Killed by Enemy Bullet!"

            # Draw enemy and its bullets
            screen.blit(enemy, enemy_rect)
            for bullet in enemy_obj["bullets"]:
                screen.blit(bullet_enemy, bullet)

        # Firing bullets for player
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time_player > bullet_cooldown:
                bullet_rect = bullet_image.get_rect(center=(player_rect.centerx, player_rect.top))
                bullets.append(bullet_rect)
                last_shot_time_player = current_time

        # Update player bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)
            for enemy_obj in enemies:
                if bullet.colliderect(enemy_obj["rect"]):
                    bullets.remove(bullet)
                    Score+=1
                    enemy_obj["rect"].topleft = (random.randint(0, 1000 - enemy_obj["rect"].width), random.randint(0, 500))

        # Draw player and player bullets
        screen.blit(player, player_rect)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)

        # Check collision with player and any enemy
        for enemy_obj in enemies:
            if player_rect.colliderect(enemy_obj["rect"]):
                game_over = True
                death_message = "You were hit by an enemy!"
    draw_text(f'Score:{Score}', font_Score, YELLOW, screen,900, 50)
    pygame.display.update()
    clock.tick(60)
