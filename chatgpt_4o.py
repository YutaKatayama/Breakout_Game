import pygame
import random

# ゲームの初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# パドルの設定
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 50, paddle_width, paddle_height)
paddle_speed = 6

# ボールの設定
ball_radius = 8
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
ball_dx, ball_dy = 4 * random.choice((1, -1)), -4

# ブロックの設定
block_rows = 5
block_cols = 8
block_width = WIDTH // block_cols
block_height = 30
blocks = [pygame.Rect(col * block_width, row * block_height, block_width, block_height) 
          for row in range(block_rows) for col in range(block_cols)]

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)
    
    # ボールの移動
    ball.move_ip(ball_dx, ball_dy)
    
    # 壁との衝突
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy
    
    # パドルとの衝突
    if ball.colliderect(paddle):
        ball_dy = -ball_dy
    
    # ブロックとの衝突
    for block in blocks[:]:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_dy = -ball_dy
            break
    
    # ボールが下に落ちたらゲームオーバー
    if ball.bottom >= HEIGHT:
        running = False
    
    # 描画
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
