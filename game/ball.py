import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Sound placeholders
        self.snd_paddle = None
        self.snd_wall = None

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.snd_wall:
                self.snd_wall.play()

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        
        # Collision with player paddle
        if ball_rect.colliderect(player.rect()) and self.velocity_x < 0:
            self.velocity_x *= -1
            self.x = player.rect().right
            if self.snd_paddle:
                self.snd_paddle.play()

        # Collision with AI paddle
        elif ball_rect.colliderect(ai.rect()) and self.velocity_x > 0:
            self.velocity_x *= -1
            self.x = ai.rect().left - self.width
            if self.snd_paddle:
                self.snd_paddle.play()


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
