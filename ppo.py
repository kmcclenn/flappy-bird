import torch
from torch import nn
import torch.nn.functional as F
import numpy as np

class FeedForward(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(FeedForward, self).__init__()

        self.layers = [
            nn.Linear(in_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, out_dim),
            nn.ReLU()
        ]
        
        self.model = nn.Sequential(*self.layers)
        
    def forward(self, x):
        if isinstance(x, np.ndarray):
            x = torch.from_numpy(x).float()
        return self.model(x)

class PPO:
    
    def __init__(self, env):
        self.env = env
        self.actor = FeedForward(env.observation_space[0], env.action_space[0])
        self.critic = FeedForward(env.observation_space[0], 1) # the value function
    
    def learn(self, total_timesteps = 2000):
        t = 0
        while t < total_timesteps:
            
            
            t += 1
    
    