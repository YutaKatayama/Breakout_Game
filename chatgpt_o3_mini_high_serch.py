import pygame
import sys
import random

# Pygame の初期化
pygame.init()

# 画面サイズの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ブロック崩しゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# FPS の設定
clock = pygame.time.Clock()
FPS = 60

# パドルクラス
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 画面外に出ないように制限
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# ボールクラス
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10
        # アルファチャンネル付きの Surface を作成し、円を描画
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 壁との衝突処理（左右と上）
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

# ブロッククラス
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

# ブロック群を生成する関数
def create_bricks(rows, cols):
    brick_group = pygame.sprite.Group()
    padding = 5  # ブロック間の隙間
    # 各ブロックの幅を計算
    brick_width = (SCREEN_WIDTH - (cols + 1) * padding) // cols
    brick_height = 20
    for row in range(rows):
        for col in range(cols):
            x = padding + col * (brick_width + padding)
            y = padding + row * (brick_height + padding) + 50  # 画面上部からのオフセット
            color = random.choice([GREEN, YELLOW, BLUE])
            brick = Brick(x, y, brick_width, brick_height, color)
            brick_group.add(brick)
    return brick_group

def main():
    # パドル、ボール、ブロック群の生成
    paddle = Paddle()
    ball = Ball()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    bricks = create_bricks(5, 10)  # 5行 x 10列のブロック

    score = 0
    font = pygame.font.SysFont("Arial", 24)
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # 各スプライトの更新
            all_sprites.update()

            # ボールとパドルの衝突判定
            if pygame.sprite.collide_rect(ball, paddle):
                # 衝突位置に応じてボールの反射角を調整
                offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.width / 2)
                ball.speed_x = 4 * offset
                ball.speed_y = -abs(ball.speed_y)

            # ボールとブロックの衝突判定（衝突したブロックは削除）
            hit_bricks = pygame.sprite.spritecollide(ball, bricks, True)
            if hit_bricks:
                ball.speed_y = -ball.speed_y
                score += len(hit_bricks) * 10

            # ボールが画面下部に落ちた場合 → ゲームオーバー
            if ball.rect.top > SCREEN_HEIGHT:
                game_over = True

            # 全ブロックを破壊したらクリア
            if len(bricks) == 0:
                game_over = True

        # 画面の描画
        screen.fill(BLACK)
        all_sprites.draw(screen)
        bricks.draw(screen)

        # スコアの表示
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

        if game_over:
            # ゲーム終了時のメッセージ表示
            msg = "CLEAR!" if len(bricks) == 0 else "GAME OVER"
            msg_text = font.render(msg, True, WHITE)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(msg_text, msg_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
