import pygame
from constants import Constants
import random
import datetime
import numpy as np

class Game:

    def __init__(self, draw = True, policy = None):
        self.clock = pygame.time.Clock()
        self.running = True
        self.draw = draw
        self.policy = policy # a funciton that returns whether or not the agent should jump

    def run(self):
        if self.draw:
            self.screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
        
        if self.draw:
            pygame.init()

        while self.running:  

            self.reset_game()

            while self.current_game:
                obs, reward, done = self.step()


        if self.draw:
            pygame.quit()
    
    def get_rollout(self):
        self.draw = False
        self.reset_game()
        out = []
        done = False
        while not done:
            obs, reward, done = self.step()
            out.append((obs, reward))
        return out

    def step(self):
    
        self.move_player()
        
        self.move_pipes()
        
        self.player_jump()

        self.dt = self.clock.tick(60) / 1000
        
        self.render()
        
        return self.observation(), self.reward(), self.done()
    
    def done(self):
        return not self.current_game or self.score > 1000
    
    def reward(self):
        return self.score
    
    def player_jump(self):
        
        # player jump
        if not self.policy:
            keys = pygame.key.get_pressed()
            if (
                keys[pygame.K_SPACE]
                and pygame.time.get_ticks() - self.previous_space > Constants.SPACE_RESET
            ):
                self.previous_space = pygame.time.get_ticks()
                self.jump()
        else:
            if self.policy(self.observation()):
                self.jump()
    
    
    def render(self):
        if self.draw:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(Constants.BACKGROUND)
            
            # draw text
            font = pygame.font.SysFont('Arial', 48)
            text = font.render(str(self.score), True, "black")
            textRect = text.get_rect()
            textRect.center = (10 + textRect.width // 2, 10 + textRect.height // 2)
            self.screen.blit(text, textRect)
            
            # draw player
            pygame.draw.circle(self.screen, "black", self.player_pos, Constants.PLAYER_SIZE)
            
            # draw pipes
            for i in range(Constants.PIPES_PER_TIME):
                pygame.draw.rect(
                    self.screen,
                    "black",
                    pygame.Rect(
                        self.obstacle_pos[i], 0, Constants.PIPE_WIDTH, self.gap_start[i]
                    ),
                )
                pygame.draw.rect(
                    self.screen,
                    "black",
                    pygame.Rect(
                        self.obstacle_pos[i],
                        self.gap_start[i] + Constants.PIPE_GAP,
                        Constants.PIPE_WIDTH,
                        Constants.SCREEN_SIZE[0] - (self.gap_start[i] + Constants.PIPE_GAP),
                    ),
                )

            pygame.display.flip()

    def reset_game(self):
        self.start_time = datetime.datetime.now()
        self.score = 0
        self.player_pos = pygame.Vector2(
            Constants.SCREEN_SIZE[0] / 2, Constants.SCREEN_SIZE[1] / 2
        )
        self.player_velocity = pygame.Vector2(0, 0)
        self.dt = 0
        self.previous_space = 0
        self.obstacle_pos = [
            Constants.SCREEN_SIZE[0] - Constants.PIPE_WIDTH,
            Constants.SCREEN_SIZE[0] * 1.5 - Constants.PIPE_WIDTH,
        ] # the x positions of the two obstacles
        self.gap_start = [
            random.randint(200, Constants.SCREEN_SIZE[1] - 200)
            for _ in range(Constants.PIPES_PER_TIME)
        ]
        self.background_speed = Constants.PIPE_SPEED
        self.current_game = True

    def move_player(self): 

        # falling
        self.player_velocity.y += Constants.GRAVITY * self.dt
        self.player_pos.y += self.player_velocity.y
        
        if self.player_pos.y > Constants.SCREEN_SIZE[1] + Constants.PLAYER_SIZE or self.player_pos.y < -Constants.PLAYER_SIZE:
            self.current_game = False
            
    def _agent_in_bounds_of_pipe(self, i):
        return self.obstacle_pos[
                i
            ] - Constants.PLAYER_SIZE < self.player_pos.x < self.obstacle_pos[
                i
            ] + Constants.PLAYER_SIZE + Constants.PIPE_WIDTH
        
    def move_pipes(self):
        self.background_speed += Constants.PIPE_ACCELERATION
        # obstacles
        for i in range(Constants.PIPES_PER_TIME):
            
            # check for agent passing through
            agent_in_bounds = self._agent_in_bounds_of_pipe(i)

            # draw obstacles
            self.obstacle_pos[i] -= self.dt * self.background_speed
            
            agent_in_bounds_after_move = self._agent_in_bounds_of_pipe(i)



            # reset pipe to start
            if self.obstacle_pos[i] < -Constants.PIPE_WIDTH:
                self.gap_start[i] = random.randint(200, Constants.SCREEN_SIZE[1] - 200)
                self.obstacle_pos[i] = Constants.SCREEN_SIZE[0]

            # check for collision
            if self._agent_in_bounds_of_pipe(i) and (
                self.player_pos.y < self.gap_start[i] + Constants.PLAYER_SIZE
                or self.player_pos.y
                > self.gap_start[i] + Constants.PIPE_GAP - Constants.PLAYER_SIZE
            ):
                self.current_game = False
                
                        
            if agent_in_bounds and not agent_in_bounds_after_move:
                # moved through the gap!
                self.score += 1
                
    def jump(self):
        self.player_velocity.y = Constants.JUMP
        
    def observation(self):
        '''
        Returns observation in the form:
        
        [
            player_pos.x, # player x position
            player_pos.y, # player y position
            obstacle_pos[0], # obstacle 1 x position
            obstacle_pos[1], # obstacle 2 x position
            gap_start[0], # gap start position for obstacle 1
            gap_start[1], # gap start position for obstacle 2
            background_speed, # background speed
            start_time # start time
        ]
            player_pos.y, obstacle_pos[0], obstacle_pos[1], gap_start, background_speed, start_time]
        
        '''
        return np.array([
            self.player_pos.x,
            self.player_pos.y,
            self.obstacle_pos[0],
            self.obstacle_pos[1],
            self.gap_start[0],
            self.gap_start[1],
            self.background_speed,
            self.start_time.timestamp()
        ])
        
    def observation_space(self):
        '''
        Returns observation space dimensions.
        '''
        return [2 + 2*Constants.PIPES_PER_TIME + 2]
    
    def action_space(self):
        '''
        Returns action space dimensions
        '''
        return [1] # either jump or not
