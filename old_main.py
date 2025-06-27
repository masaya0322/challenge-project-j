import pygame
import pygame_gui
import sys

# --- 定数の設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (240, 240, 240)

BUTTON1_TEXT = "おもちゃであそぶ"
BUTTON2_TEXT = "いますぐかたづける"

def main():
    """ メインのゲーム関数 """
    pygame.init()

    # 画面の設定
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Duolingo風UI")
    width, height = screen.get_size()

    # pygame_guiマネージャーの作成
    manager = pygame_gui.UIManager((width, height), 'theme.json')

    # ボタンの作成
    button1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width // 2 - 150, height // 2 - 60), (300, 50)),
        text=BUTTON1_TEXT,
        manager=manager
    )
    button2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width // 2 - 150, height // 2 + 10), (300, 50)),
        text=BUTTON2_TEXT,
        manager=manager
    )

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(BACKGROUND_COLOR)
        manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
