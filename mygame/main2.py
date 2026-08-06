import pyxel
import os

WIDTH = 160
HEIGHT = 120

POINT_CENTER_X = WIDTH // 2
POINT_CENTER_Y = HEIGHT // 2

FRAME = 30
STONE_INTERVAL = FRAME
START_SCENE = "start"
PLAY_SCENE = "play"


class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < HEIGHT:
            self.y += 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)


class App:
    def __init__(self):
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT * 4 // 5
        self.stones = []
        self.is_collision = False
        self.current_scene = START_SCENE
        self.game_over_display_time = 2 * FRAME
        font_path = os.path.join(os.path.dirname(__file__), "umplus_j10r.bdf")
        self.jp_font = pyxel.Font(font_path)

        pyxel.init(WIDTH, HEIGHT, title="アルカディアの冒険")
        pyxel.mouse(True)
        pyxel.load("./my_resource.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT * 4 // 5
        self.stones = []
        self.is_collision = False
        self.game_over_display_time = 2 * FRAME

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

    def update_play_scene(self):
        # ゲームオーバー
        if self.is_collision:
            if self.game_over_display_time > 0:
                self.game_over_display_time -= 1
            else:
                self.current_scene = START_SCENE
            return

        # 石の生成
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, WIDTH - 8), 0))

        # 石の落下
        for stone in self.stones.copy():
            stone.update()

            # 衝突判定
            if (
                self.player_x <= stone.x <= self.player_x + 16
                and self.player_y <= stone.y <= self.player_y + 16
            ):
                self.is_collision = True

            # 石が画面外に出たら削除
            if stone.y > HEIGHT:
                self.stones.remove(stone)

        # プレイヤーの移動
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < WIDTH - 12:
            self.player_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > -4:
            self.player_x -= 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(
            WIDTH // 10, HEIGHT // 10, "クリックしてね", pyxel.COLOR_PINK, self.jp_font
        )

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)

        # 石
        for stone in self.stones:
            stone.draw()

        # プレイヤー
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)

        if self.is_collision:
            pyxel.text(
                POINT_CENTER_X,
                POINT_CENTER_Y,
                "ゲームオーバー",
                pyxel.COLOR_RED,
                self.jp_font,
            )

    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()


App()
