import pygame
from constants import Constants
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_velocity = pygame.Vector2(0, 0)
    dt = 0
    previous_space = 0

    obstacle_pos = [screen.get_width() - Constants.PIPE_WIDTH, screen.get_width() * 1.5 - Constants.PIPE_WIDTH]
    gap_start = [random.randint(200, screen.get_height() - 200) for _ in range(Constants.PIPES_PER_TIME)]
    background_speed = Constants.PIPE_SPEED
    current_game = True

    while current_game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(Constants.BACKGROUND)
        
        # draw player
        pygame.draw.circle(screen, "black", player_pos, Constants.PLAYER_SIZE)
        
        # falling
        player_velocity.y += Constants.GRAVITY * dt
        player_pos.y += player_velocity.y
        
        background_speed += Constants.PIPE_ACCELERATION
        
        # obstacles
        for i in range(Constants.PIPES_PER_TIME):
            
            obstacle_pos[i] -= dt * background_speed
            pygame.draw.rect(screen, "black", pygame.Rect(obstacle_pos[i], 0, Constants.PIPE_WIDTH, gap_start[i]))
            pygame.draw.rect(screen, "black", pygame.Rect(obstacle_pos[i], gap_start[i] + Constants.PIPE_GAP, Constants.PIPE_WIDTH, screen.get_width() - (gap_start[i] + Constants.PIPE_GAP)))
            
            if obstacle_pos[i] < -Constants.PIPE_WIDTH:
                gap_start[i] = random.randint(200, screen.get_height() - 200)
                obstacle_pos[i] = screen.get_width()
                
            if obstacle_pos[i] - Constants.PLAYER_SIZE < player_pos.x < obstacle_pos[i] + Constants.PLAYER_SIZE + Constants.PIPE_WIDTH and (player_pos.y < gap_start[i] + Constants.PLAYER_SIZE or player_pos.y > gap_start[i] + Constants.PIPE_GAP - Constants.PLAYER_SIZE):
                current_game = False
            
        
        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - previous_space > Constants.SPACE_RESET:
            previous_space = pygame.time.get_ticks()
            player_velocity.y = Constants.JUMP
            
        if player_pos.y > screen.get_height() + Constants.PLAYER_SIZE:
            current_game = False
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000

pygame.quit()
