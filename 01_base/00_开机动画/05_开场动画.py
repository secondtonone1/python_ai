#!/usr/bin/env python3
"""
Digital Rain - 全屏数字雨 + 空格触发风暴汇聚标题
"""

import pygame
import random
import math
import sys
import ctypes

# DPI感知，防止缩放问题
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

FPS = 60
FONT_SIZE = 22

# ============ 配置标题 ============
TITLE_TEXT = "Python进阶"
SUBTITLE_TEXT = "封装继承多态"
HOLD_SECONDS = 4
# ==================================


class DigitalRain:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        pygame.display.set_caption("Digital Rain")
        self.clock = pygame.time.Clock()

        self.font = self._load_font(FONT_SIZE)
        self.title_font = self._load_font(120)
        self.subtitle_font = self._load_font(52)
        self.char_height = FONT_SIZE

        # 列数和行数
        self.col_count = self.width // FONT_SIZE + 1
        self.row_count = self.height // self.char_height + 2

        # 每列状态
        self.columns = []
        for i in range(self.col_count):
            self._init_column(i, randomize_start=True)

        # 字符网格
        self.grid = [[self._random_char() for _ in range(self.row_count)] for _ in range(self.col_count)]
        self.grid_timer = [[random.randint(3, 30) for _ in range(self.row_count)] for _ in range(self.col_count)]

        # 字符缓存
        self.char_cache = {}

        # 风暴粒子
        self.storm_particles = []

        # 状态
        self.state = "rain"
        self.state_timer = 0
        self.rain_dim = 1.0
        self.flash_alpha = 0

        # 标题区域
        self.title_rect = None
        self.subtitle_rect = None

    def _load_font(self, size):
        font_names = [
            "SimHei", "Microsoft YaHei", "STHeiti",
            "PingFang SC", "Noto Sans CJK SC",
            "WenQuanYi Micro Hei", "Hiragino Sans GB",
        ]
        for name in font_names:
            try:
                font = pygame.font.SysFont(name, size, bold=False)
                test = font.render("测试", True, (255, 255, 255))
                if test.get_width() > size:
                    return font
            except Exception:
                continue
        return pygame.font.Font(None, size)

    @staticmethod
    def _random_char():
        r = random.random()
        if r < 0.5:
            return chr(random.randint(0x0030, 0x0039))
        else:
            return chr(random.randint(0x0041, 0x005A))

    def _init_column(self, idx, randomize_start=False):
        speed = random.uniform(0.3, 1.2)
        length = random.randint(8, 35)
        if randomize_start:
            head = random.uniform(-self.row_count, self.row_count)
        else:
            head = random.uniform(-length - 10, -1)

        data = {"head": head, "speed": speed, "length": length}
        if idx < len(self.columns):
            self.columns[idx] = data
        else:
            self.columns.append(data)

    def _get_char_surface(self, char, color):
        key = (char, color)
        if key not in self.char_cache:
            surf = self.font.render(char, True, color)
            self.char_cache[key] = surf
            if len(self.char_cache) > 8000:
                keys = list(self.char_cache.keys())
                for k in keys[:4000]:
                    del self.char_cache[k]
        return self.char_cache[key]

    def _text_to_char_positions(self, text, font, offset_y=0):
        surface = font.render(text, True, (255, 255, 255))
        w, h = surface.get_size()
        ox = (self.width - w) // 2
        oy = (self.height - h) // 2 + offset_y

        positions = []
        step_x = FONT_SIZE
        step_y = FONT_SIZE
        for y in range(0, h, step_y):
            for x in range(0, w, step_x):
                try:
                    c = surface.get_at((x, y))
                    if c[0] > 80:
                        positions.append((ox + x, oy + y))
                except IndexError:
                    continue
        return positions

    def _get_title_rects(self):
        title_surf = self.title_font.render(TITLE_TEXT, True, (255, 255, 255))
        tw, th = title_surf.get_size()
        tx = (self.width - tw) // 2
        ty = (self.height - th) // 2 - 50
        self.title_rect = pygame.Rect(tx - 20, ty - 10, tw + 40, th + 20)

        if SUBTITLE_TEXT:
            sub_surf = self.subtitle_font.render(SUBTITLE_TEXT, True, (255, 255, 255))
            sw, sh = sub_surf.get_size()
            sx = (self.width - sw) // 2
            sy = (self.height - sh) // 2 + 60
            self.subtitle_rect = pygame.Rect(sx - 20, sy - 10, sw + 40, sh + 20)

    def _is_in_title_area(self, x, y):
        if self.title_rect and self.title_rect.collidepoint(x, y):
            return True
        if self.subtitle_rect and self.subtitle_rect.collidepoint(x, y):
            return True
        return False

    def trigger_title(self):
        if self.state != "rain":
            return

        self.state = "storm"
        self.state_timer = 0
        self.storm_particles = []
        self._get_title_rects()

        # 主标题
        positions = self._text_to_char_positions(TITLE_TEXT, self.title_font, offset_y=-50)
        for tx, ty in positions:
            p = StormParticle(tx, ty, self.width, self.height, is_subtitle=False)
            self.storm_particles.append(p)

        # 副标题
        if SUBTITLE_TEXT:
            sub_positions = self._text_to_char_positions(SUBTITLE_TEXT, self.subtitle_font, offset_y=80)
            for tx, ty in sub_positions:
                p = StormParticle(tx, ty, self.width, self.height, is_subtitle=True)
                self.storm_particles.append(p)

    def update(self):
        self.state_timer += 1

        # 数字雨始终更新
        for i, col in enumerate(self.columns):
            col["head"] += col["speed"]
            tail = col["head"] - col["length"]
            if tail > self.row_count:
                self._init_column(i, randomize_start=False)

        # 字符闪烁
        for ci in range(self.col_count):
            for ri in range(self.row_count):
                self.grid_timer[ci][ri] -= 1
                if self.grid_timer[ci][ri] <= 0:
                    self.grid[ci][ri] = self._random_char()
                    self.grid_timer[ci][ri] = random.randint(5, 40)

        if self.state == "rain":
            self.rain_dim = min(1.0, self.rain_dim + 0.01)

        elif self.state == "storm":
            self.rain_dim = max(0.2, self.rain_dim - 0.015)

            all_arrived = True
            for p in self.storm_particles:
                p.update()
                if p.state == "moving":
                    all_arrived = False

            if all_arrived:
                self.state = "hold"
                self.state_timer = 0
                self.flash_alpha = 150

        elif self.state == "hold":
            for p in self.storm_particles:
                p.update()

            if self.state_timer > HOLD_SECONDS * FPS:
                self.state = "explode"
                self.state_timer = 0
                self.flash_alpha = 180
                for p in self.storm_particles:
                    p.start_explode()

        elif self.state == "explode":
            for p in self.storm_particles:
                p.update()

            alive = any(p.state != "dead" for p in self.storm_particles)
            if not alive or self.state_timer > 300:
                self.state = "fade_back"
                self.state_timer = 0
                self.title_rect = None
                self.subtitle_rect = None

        elif self.state == "fade_back":
            self.rain_dim = min(1.0, self.rain_dim + 0.008)
            if self.rain_dim >= 1.0:
                self.state = "rain"
                self.storm_particles = []

        self.flash_alpha = max(0, self.flash_alpha - 5)

    def draw(self):
        self.screen.fill((0, 0, 0))

        block_rain = self.state == "hold"

        # 数字雨
        for ci, col in enumerate(self.columns):
            head = col["head"]
            length = col["length"]
            x = ci * FONT_SIZE

            start_row = max(0, int(head - length))
            end_row = min(self.row_count - 1, int(head))

            for ri in range(start_row, end_row + 1):
                y = ri * self.char_height

                if block_rain and self._is_in_title_area(x, y):
                    continue

                dist_from_head = head - ri
                ratio = 1.0 - (dist_from_head / length)
                ratio = max(0.0, min(1.0, ratio))

                if ri == int(head):
                    color = (200, 255, 200)
                elif ratio > 0.85:
                    g = int(200 + 55 * ratio)
                    color = (int(80 * ratio), min(255, g), int(80 * ratio))
                else:
                    g = int(60 + 160 * ratio)
                    color = (0, g, 0)

                color = (
                    int(color[0] * self.rain_dim),
                    int(color[1] * self.rain_dim),
                    int(color[2] * self.rain_dim),
                )

                char = self.grid[ci][ri]
                char_surf = self._get_char_surface(char, color)
                self.screen.blit(char_surf, (x, y))

        # 风暴粒子
        if self.state in ("storm", "explode"):
            for p in self.storm_particles:
                if p.state == "dead" or p.alpha <= 0:
                    continue
                brightness = p.alpha / 255.0
                color = (
                    int(p.color[0] * brightness),
                    int(p.color[1] * brightness),
                    int(p.color[2] * brightness),
                )
                char_surf = self.font.render(p.char, True, color)
                self.screen.blit(char_surf, (int(p.x), int(p.y)))

        # 标题文字
        if self.state == "hold":
            title_surf = self.title_font.render(TITLE_TEXT, True, (220, 255, 220))
            tw, th = title_surf.get_size()
            self.screen.blit(title_surf, ((self.width - tw) // 2, (self.height - th) // 2 - 50))

            if SUBTITLE_TEXT:
                sub_surf = self.subtitle_font.render(SUBTITLE_TEXT, True, (150, 255, 180))
                sw, sh = sub_surf.get_size()
                self.screen.blit(sub_surf, ((self.width - sw) // 2, (self.height - sh) // 2 + 60))

        # 闪光
        if self.flash_alpha > 0:
            flash = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            flash.fill((150, 255, 180, self.flash_alpha))
            self.screen.blit(flash, (0, 0))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.trigger_title()
                    elif event.key == pygame.K_r:
                        self.state = "rain"
                        self.rain_dim = 1.0
                        self.storm_particles = []
                        self.title_rect = None
                        self.subtitle_rect = None

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


class StormParticle:
    """风暴粒子 - 从屏幕边缘螺旋汇聚"""

    def __init__(self, target_x, target_y, screen_w, screen_h, is_subtitle=False):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            self.x = random.uniform(0, screen_w)
            self.y = random.uniform(-100, -20)
        elif edge == "bottom":
            self.x = random.uniform(0, screen_w)
            self.y = random.uniform(screen_h + 20, screen_h + 100)
        elif edge == "left":
            self.x = random.uniform(-100, -20)
            self.y = random.uniform(0, screen_h)
        else:
            self.x = random.uniform(screen_w + 20, screen_w + 100)
            self.y = random.uniform(0, screen_h)

        self.start_x = self.x
        self.start_y = self.y
        self.target_x = target_x
        self.target_y = target_y

        self.char = self._random_char()
        self.progress = 0.0
        base_speed = 0.015 if not is_subtitle else 0.010
        self.converge_speed = random.uniform(base_speed * 0.7, base_speed * 1.5)
        self.state = "moving"
        self.alpha = 0
        self.color = (0, 255, 70)

        self.spiral_radius = random.uniform(50, 200)
        self.spiral_angle = random.uniform(0, 2 * math.pi)
        self.spiral_speed = random.uniform(3, 8) * random.choice([-1, 1])

        self.vel_x = 0.0
        self.vel_y = 0.0
        self.char_timer = random.randint(2, 10)

    @staticmethod
    def _random_char():
        r = random.random()
        if r < 0.5:
            return chr(random.randint(0x0030, 0x0039))
        else:
            return chr(random.randint(0x0041, 0x005A))

    def start_explode(self):
        self.state = "explode"
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(8, 25)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.color = random.choice([
            (0, 255, 70), (0, 200, 255), (150, 255, 100),
            (255, 255, 255), (0, 255, 180),
        ])

    def update(self):
        self.char_timer -= 1
        if self.char_timer <= 0:
            self.char = self._random_char()
            self.char_timer = random.randint(3, 15)

        if self.state == "moving":
            self.progress += self.converge_speed
            if self.progress >= 1.0:
                self.progress = 1.0
                self.state = "hold"
                self.x = self.target_x
                self.y = self.target_y
                self.alpha = 255
                return

            if self.progress < 0.5:
                t = 4 * self.progress ** 3
            else:
                t = 1 - (-2 * self.progress + 2) ** 3 / 2

            base_x = self.start_x + (self.target_x - self.start_x) * t
            base_y = self.start_y + (self.target_y - self.start_y) * t

            spiral_factor = (1 - t) ** 2
            self.spiral_angle += self.spiral_speed * 0.02
            offset_x = math.cos(self.spiral_angle) * self.spiral_radius * spiral_factor
            offset_y = math.sin(self.spiral_angle) * self.spiral_radius * spiral_factor

            self.x = base_x + offset_x
            self.y = base_y + offset_y
            self.alpha = min(255, int(self.progress * 400))

        elif self.state == "hold":
            self.alpha = 255

        elif self.state == "explode":
            self.x += self.vel_x
            self.y += self.vel_y
            self.vel_y += 0.3
            self.vel_x *= 0.97
            self.alpha = max(0, self.alpha - 4)
            if self.alpha <= 0:
                self.state = "dead"


if __name__ == "__main__":
    app = DigitalRain()
    app.run()