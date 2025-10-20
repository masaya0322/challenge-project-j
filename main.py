import pygame
import sys

# --- 定数の設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_COLOR = (255, 100, 100)
PLATFORM_COLOR = (100, 200, 100)
BACKGROUND_COLOR = (50, 50, 150)

GRAVITY = 0.5
PLAYER_JUMP_STRENGTH = -12
PLAYER_SPEED = 5

class Player(pygame.sprite.Sprite):
    """ プレイヤーキャラクターを管理するクラス """
    def __init__(self):
        super().__init__()
        # プレイヤーの画像（矩形）を作成
        self.image = pygame.Surface([40, 50])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()

        # プレイヤーの速度ベクトル
        self.change_x = 0
        self.change_y = 0

        # プレイヤーが立っているプラットフォーム
        self.platform = None

    def update(self):
        """ プレイヤーの動きを毎フレーム更新する """
        # 重力を適用
        self.calc_gravity()

        # X方向（横）に移動
        self.rect.x += self.change_x

        # X方向の衝突判定
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_x > 0: # 右に移動中
                self.rect.right = block.rect.left
            elif self.change_x < 0: # 左に移動中
                self.rect.left = block.rect.right
        
        # Y方向（縦）に移動
        self.rect.y += self.change_y

        # Y方向の衝突判定
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0: # 下に落下中
                self.rect.bottom = block.rect.top
                self.change_y = 0 # 落下を止める
            elif self.change_y < 0: # ジャンプ中
                self.rect.top = block.rect.bottom
                self.change_y = 0 # 上昇を止める

        # 画面外に出ないようにする
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def calc_gravity(self):
        """ 重力の影響を計算する """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

        # 地面にいるかチェック
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ プレイヤーをジャンプさせる """
        # 地面についているか、またはプラットフォームの上に乗っているか確認
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2
        
        # y座標が画面の下端にあるか、またはプラットフォームリストが空でない場合ジャンプできる
        if self.rect.bottom >= SCREEN_HEIGHT or len(platform_hit_list) > 0:
            self.change_y = PLAYER_JUMP_STRENGTH

    # プレイヤーの移動
    def go_left(self):
        self.change_x = -PLAYER_SPEED

    def go_right(self):
        self.change_x = PLAYER_SPEED

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    """ 地面やブロックなどのプラットフォーム """
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()


def main():
    """ メインのゲーム関数 """
    pygame.init()

    # 画面の設定
    # size = [SCREEN_WIDTH, SCREEN_HEIGHT] # フルスクリーン時は (0,0) または解像度指定
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("2D横スクロールゲーム")

    # スプライトリストの作成
    all_sprites_list = pygame.sprite.Group()
    platform_list = pygame.sprite.Group()

    # プレイヤーの作成
    player = Player()
    all_sprites_list.add(player)

    # 地面の作成
    ground = Platform(SCREEN_WIDTH, 20)
    ground.rect.x = 0
    ground.rect.y = SCREEN_HEIGHT - 20
    platform_list.add(ground)
    all_sprites_list.add(ground)

    # ブロックの配置
    block_positions = [
        [200, 450, 150, 20],
        [450, 350, 120, 20],
        [600, 250, 100, 20],
    ]

    for pos in block_positions:
        block = Platform(pos[2], pos[3])
        block.rect.x = pos[0]
        block.rect.y = pos[1]
        platform_list.add(block)
        all_sprites_list.add(block)

    player.platforms = platform_list

    # ループのフラグと時計
    done = False
    clock = pygame.time.Clock()

    # --- メインゲームループ ---
    while not done:
        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # --- ゲームロジック ---
        all_sprites_list.update()

        # --- 描画処理 ---
        screen.fill(BACKGROUND_COLOR)
        all_sprites_list.draw(screen)

        # --- 画面更新 ---
        pygame.display.flip()

        # --- フレームレート制御 ---
        clock.tick(60)

    # --- 終了処理 ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
