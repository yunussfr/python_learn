import gymnasium as gym
from gymnasium.wrappers import TimeLimit
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import pygame
import time

# ======================
# NEURAL NETWORK
# ======================
class DQN(nn.Module):
    def __init__(self, obs_size, action_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_size, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_size)
        )

    def forward(self, x):
        return self.net(x)

# ======================
# HYPERPARAMETERS
# ======================
GAMMA = 0.99
LR = 0.0005

BATCH_SIZE = 128
MEMORY_SIZE = 50_000

EPSILON_START = 1.0
EPSILON_END = 0.02
EPSILON_DECAY = 0.99888  # 👈 SENİN SEÇİMİN

MAX_EPISODES = 2000
MAX_STEPS = 500

# ======================
# ENVIRONMENT (LIMIT KALDIRILMIŞ)
# ======================
env = gym.make("MountainCar-v0", render_mode="human")
env = TimeLimit(env, max_episode_steps=MAX_STEPS)

obs_size = env.observation_space.shape[0]
action_size = env.action_space.n

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

policy_net = DQN(obs_size, action_size).to(device)
target_net = DQN(obs_size, action_size).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
loss_fn = nn.MSELoss()

memory = deque(maxlen=MEMORY_SIZE)
epsilon = EPSILON_START

# ======================
# PYGAME TEXT
# ======================
pygame.init()
font = pygame.font.SysFont("Arial", 18)

# ======================
# TRAINING LOOP
# ======================
print("🚗 Eğitim başladı...")

for episode in range(1, MAX_EPISODES + 1):
    obs, _ = env.reset(seed=random.randint(0, 9999))
    obs = torch.tensor(obs, dtype=torch.float32).to(device)

    total_reward = 0

    for step in range(1, MAX_STEPS + 1):

        # ---- ACTION ----
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            with torch.no_grad():
                action = torch.argmax(policy_net(obs)).item()

        next_obs, reward, terminated, truncated, _ = env.step(action)
        next_obs_t = torch.tensor(next_obs, dtype=torch.float32).to(device)

        memory.append((obs, action, reward, next_obs_t, terminated))
        obs = next_obs_t
        total_reward += reward

        # ---- TRAIN ----
        if len(memory) >= BATCH_SIZE:
            batch = random.sample(memory, BATCH_SIZE)
            obs_b, act_b, rew_b, next_obs_b, done_b = zip(*batch)

            obs_b = torch.stack(obs_b)
            act_b = torch.tensor(act_b).to(device)
            rew_b = torch.tensor(rew_b, dtype=torch.float32).to(device)
            next_obs_b = torch.stack(next_obs_b)
            done_b = torch.tensor(done_b, dtype=torch.float32).to(device)

            q_vals = policy_net(obs_b).gather(1, act_b.unsqueeze(1)).squeeze()

            with torch.no_grad():
                max_next_q = target_net(next_obs_b).max(1)[0]
                target_q = rew_b + GAMMA * max_next_q * (1 - done_b)

            loss = loss_fn(q_vals, target_q)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # ---- TARGET NET UPDATE ----
        if step % 50 == 0:
            target_net.load_state_dict(policy_net.state_dict())

        # ---- SCREEN TEXT ----
        surface = pygame.display.get_surface()
        if surface:
            surface.fill((255, 255, 255), (0, 0, 520, 40))
            text = font.render(
                f"Episode: {episode} | Step: {step}/{MAX_STEPS} | "
                f"Remaining: {MAX_STEPS-step} | Epsilon: {epsilon:.3f}",
                True,
                (0, 0, 0)
            )
            surface.blit(text, (10, 10))
            pygame.display.update()

        time.sleep(0.0002)

        # ---- SUCCESS ----
        if next_obs[0] >= 0.5:
            print(f"\n🎉 BAŞARI! Episode {episode}, Step {step}")
            time.sleep(2)
            env.close()
            pygame.quit()
            exit()

        if terminated:
            break

    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    print(
        f"Episode {episode} | "
        f"Reward: {total_reward} | "
        f"Epsilon: {epsilon:.4f}"
    )

env.close()
pygame.quit()
