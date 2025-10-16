import pygame
from .paddle import Paddle
from .ball import Ball

# Initialize mixer before anything that uses sound
pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.winning_score = 5

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.snd_paddle = pygame.mixer.Sound("assets/sounds/paddle_hit.wav")
        self.snd_wall = pygame.mixer.Sound("assets/sounds/wall_bounce.wav")
        self.snd_score = pygame.mixer.Sound("assets/sounds/score.wav")
        self.ball.snd_paddle = self.snd_paddle
        self.ball.snd_wall = self.snd_wall

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # --- Move the ball first ---
        self.ball.move()

        # --- Collision check: right after moving the ball ---
        ball_rect = self.ball.rect()
        player_rect = self.player.rect()
        ai_rect = self.ai.rect()

        if ball_rect.colliderect(player_rect):
            self.ball.velocity_x *= -1
            # Snap ball outside paddle to prevent "sticking"
            self.ball.x = player_rect.right

        elif ball_rect.colliderect(ai_rect):
            self.ball.velocity_x *= -1
            self.ball.x = ai_rect.left - self.ball.width

        # --- Boundary / Scoring ---
        if self.ball.x <= 0:
            self.ai_score += 1
            self.snd_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.snd_score.play()
            self.ball.reset()

        # --- AI logic ---
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score == self.winning_score or self.ai_score == self.winning_score:
            winner_text = "Player Wins!" if self.player_score == self.winning_score else "AI Wins!"
            font = pygame.font.SysFont("Arial", 60)
            text_surface = font.render(winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

            pygame.time.delay(1000)  # Short pause before showing replay menu
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        font = pygame.font.SysFont("Arial", 30)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        waiting = True
        while waiting:
            screen.fill((0, 0, 0))
            title_font = pygame.font.SysFont("Arial", 50)
            title_surface = title_font.render("Play Again?", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
            screen.blit(title_surface, title_rect)

            # Display menu options
            for i, line in enumerate(options):
                text = font.render(line, True, (255, 255, 255))
                rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
                screen.blit(text, rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.start_new_game(3)
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.start_new_game(5)
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.start_new_game(7)
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

    def start_new_game(self, best_of):
        # Reset scores, ball, and winning target
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = best_of
        self.ball.reset()

