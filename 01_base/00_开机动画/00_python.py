#!/usr/bin/env python3
"""
Love Storm - 持续循环动画
阶段：汇聚 → 心跳 → 爆裂(红→紫渐变) → 全部落地 → 重新汇聚
"""

import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Storm")
clock = pygame.time.Clock()

BG_COLOR = (10, 5, 20)


def heart_function(t, scale=10):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    x *= scale
    y *= scale
    return x, y


def generate_heart_points(num_points, scale=10, center_x=None, center_y=None):
    if center_x is None:
        center_x = WIDTH // 2
    if center_y is None:
        center_y = HEIGHT // 2 - 40

    points = []
    for _ in range(num_points):
        t = random.uniform(0, 2 * math.pi)
        x, y = heart_function(t, scale)
        if random.random() < 0.7:
            ratio = random.random() ** 0.5
            x *= ratio
            y *= ratio
        points.append((center_x + x, center_y + y))
    return points


class Particle:
    def __init__(self, target_x, target_y):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(HEIGHT + 20, HEIGHT + 200)
        self.start_x = self.x
        self.start_y = self.y

        self.target_x = target_x
        self.target_y = target_y

        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-8, -3)

        self.state = 'rising'
        self.progress = 0

        self.size = random.uniform(1.5, 3.5)
        self.base_size = self.size
        self.alpha = random.randint(150, 255)

        self.color_type = random.choice(['pink', 'red', 'magenta', 'rose', 'coral'])
        self.base_color = self._get_color()
        self.current_color = self.base_color

        self.wind_offset = random.uniform(0, math.pi * 2)
        self.wind_strength = random.uniform(0.5, 2.0)

        self.trail = []
        self.max_trail = random.randint(5, 12)

        self.twinkle_speed = random.uniform(0.05, 0.15)
        self.twinkle_phase = random.uniform(0, math.pi * 2)

        self.delay = random.uniform(0, 2.5)
        self.time = 0

        self.float_offset_x = random.uniform(-2, 2)
        self.float_offset_y = random.uniform(-2, 2)
        self.float_speed = random.uniform(0.02, 0.05)

        # 爆炸用
        self.explode_vx = 0
        self.explode_vy = 0
        self.gravity = 0.3
        self.life = 1.0
        self.decay = random.uniform(0.005, 0.015)

        # 落地标记
        self.landed = False

    def _get_color(self):
        colors = {
            'pink': (255, 105, 180),
            'red': (255, 50, 80),
            'magenta': (255, 0, 144),
            'rose': (255, 80, 120),
            'coral': (255, 127, 100),
        }
        return colors[self.color_type]

    def reset_for_converge(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(HEIGHT + 20, HEIGHT + 200)
        self.start_x = self.x
        self.start_y = self.y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-8, -3)
        self.state = 'rising'
        self.progress = 0
        self.delay = random.uniform(0, 2.5)
        self.time = 0
        self.trail = []
        self.life = 1.0
        self.size = self.base_size
        self.landed = False

    def reset_from_landed(self):
        self.start_x = self.x
        self.start_y = self.y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-5, -2)
        self.state = 'rising'
        self.progress = 0
        self.delay = random.uniform(0, 1.5)
        self.time = 0
        self.trail = []
        self.life = 1.0
        self.size = self.base_size
        self.landed = False

    def start_explode(self, center_x, center_y):
        self.state = 'exploding'
        dx = self.x - center_x
        dy = self.y - center_y
        dist = math.sqrt(dx * dx + dy * dy) + 1
        speed = random.uniform(5, 15)
        self.explode_vx = (dx / dist) * speed + random.uniform(-3, 3)
        self.explode_vy = (dy / dist) * speed + random.uniform(-5, -1)
        self.life = 1.0
        self.trail = []
        self.size = self.base_size * random.uniform(2.5, 4.0)
        self.landed = False
        # 爆炸时设为红色
        self.current_color = (255, 50, 50)

    def update(self, dt, global_time, heartbeat_scale=1.0):
        self.time += dt

        if self.state == 'rising':
            if self.time < self.delay:
                return

            active_time = self.time - self.delay
            wind = math.sin(global_time * 2 + self.wind_offset) * self.wind_strength
            self.vx += wind * 0.02
            self.vy += 0.05
            self.x += self.vx
            self.y += self.vy

            if self.y < HEIGHT * 0.7 or active_time > 2.0:
                self.state = 'forming'
                self.progress = 0

        elif self.state == 'forming':
            self.progress += 0.008 + random.uniform(0, 0.005)
            if self.progress > 1.0:
                self.progress = 1.0
                self.state = 'done'

            t = self.progress
            ease = t * t * (3 - 2 * t)

            spiral_angle = (1 - t) * math.pi * 4 + self.wind_offset
            spiral_radius = (1 - ease) * 80

            target_x = self.target_x + math.cos(spiral_angle) * spiral_radius
            target_y = self.target_y + math.sin(spiral_angle) * spiral_radius

            self.x = self.x + (target_x - self.x) * 0.03
            self.y = self.y + (target_y - self.y) * 0.03

        elif self.state == 'done':
            center_x = WIDTH // 2
            center_y = HEIGHT // 2 - 40
            dx = self.target_x - center_x
            dy = self.target_y - center_y
            self.x = center_x + dx * heartbeat_scale
            self.y = center_y + dy * heartbeat_scale

            float_x = math.sin(global_time * self.float_speed * 60 + self.wind_offset) * self.float_offset_x
            float_y = math.cos(global_time * self.float_speed * 60 + self.wind_offset) * self.float_offset_y
            self.x += float_x
            self.y += float_y

        elif self.state == 'exploding':
            self.x += self.explode_vx
            self.y += self.explode_vy
            self.explode_vy += self.gravity
            self.explode_vx *= 0.98

            # 红色渐变到紫色
            r, g, b = self.current_color
            target_purple = (180, 50, 255)
            self.current_color = (
                int(r + (target_purple[0] - r) * 0.02),
                int(g + (target_purple[1] - g) * 0.02),
                int(b + (target_purple[2] - b) * 0.02),
            )

            self.size = self.base_size * 2.5

            # 检测落地（到达屏幕底部）
            if self.y >= HEIGHT - 20:
                self.y = HEIGHT - 20
                self.x = max(0, min(WIDTH, self.x))
                self.landed = True
                self.state = 'landed'
                self.trail = []

        elif self.state == 'landed':
            # 停在原地等待汇聚指令
            pass

        # 拖尾
        if self.state in ('rising', 'forming', 'exploding'):
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.max_trail:
                self.trail.pop(0)
        elif self.state == 'done':
            if self.trail:
                self.trail.pop(0)

    def draw(self, surface, global_time):
        if self.state == 'rising' and self.time < self.delay:
            return
        if self.state == 'landed':
            # 落地后画一个小光点
            r, g, b = self.current_color
            twinkle = 0.6 + 0.4 * math.sin(global_time * 5 + self.twinkle_phase)
            alpha = int(180 * twinkle)
            size = max(1, int(self.base_size * 1.5))
            glow_size = size * 3
            s = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (r, g, b, int(alpha * 0.3)), (glow_size, glow_size), glow_size)
            pygame.draw.circle(s, (r, g, b, alpha), (glow_size, glow_size), size)
            surface.blit(s, (self.x - glow_size, self.y - glow_size))
            return

        if self.life <= 0:
            return

        twinkle = 0.7 + 0.3 * math.sin(global_time * 10 * self.twinkle_speed + self.twinkle_phase)
        r, g, b = self.current_color
        alpha = int(self.alpha * twinkle * min(1.0, self.life))

        if alpha <= 0:
            return

        # 拖尾
        for i, (tx, ty) in enumerate(self.trail):
            trail_ratio = (i + 1) / len(self.trail)
            trail_alpha = int(alpha * trail_ratio * 0.4)
            trail_size = max(1, int(self.size * trail_ratio * 0.6))
            if trail_alpha > 0:
                s = pygame.Surface((trail_size * 4, trail_size * 4), pygame.SRCALPHA)
                pygame.draw.circle(s, (r, g, b, trail_alpha), (trail_size * 2, trail_size * 2), trail_size)
                surface.blit(s, (tx - trail_size * 2, ty - trail_size * 2))

        # 本体
        glow_size = max(2, int(self.size * 4))
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (r, g, b, int(alpha * 0.2)), (glow_size, glow_size), glow_size)
        pygame.draw.circle(glow_surf, (r, g, b, alpha), (glow_size, glow_size), max(1, int(self.size)))
        pygame.draw.circle(glow_surf, (255, 255, 255, int(alpha * 0.8)), (glow_size, glow_size), max(1, int(self.size * 0.4)))
        surface.blit(glow_surf, (self.x - glow_size, self.y - glow_size))


class PulseRing:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 10
        self.max_radius = 250
        self.speed = 4
        self.life = 1.0
        self.color = color

    def update(self):
        self.radius += self.speed
        self.life = 1.0 - (self.radius / self.max_radius)
        return self.life > 0

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(120 * self.life)
        r, g, b = self.color
        width = max(1, int(3 * self.life))
        s = pygame.Surface((self.max_radius * 2 + 20, self.max_radius * 2 + 20), pygame.SRCALPHA)
        center = self.max_radius + 10
        pygame.draw.circle(s, (r, g, b, alpha), (center, center), int(self.radius), width)
        surface.blit(s, (self.x - center, self.y - center))


class StarParticle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.size = random.uniform(0.5, 2)
        self.twinkle_speed = random.uniform(0.5, 3)
        self.phase = random.uniform(0, math.pi * 2)
        self.brightness = random.uniform(0.3, 1.0)

    def draw(self, surface, global_time):
        b = self.brightness * (0.5 + 0.5 * math.sin(global_time * self.twinkle_speed + self.phase))
        alpha = int(255 * b * 0.4)
        if alpha < 10:
            return
        color = (200, 200, 255, alpha)
        size = max(1, int(self.size * b * 2))
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (size, size), size)
        surface.blit(s, (self.x - size, self.y - size))


class SparkParticle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(HEIGHT + 10, HEIGHT + 50)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-3, -0.5)
        self.life = 1.0
        self.decay = random.uniform(0.003, 0.01)
        self.size = random.uniform(0.5, 2)
        self.color = random.choice([
            (255, 200, 200), (255, 150, 180), (255, 100, 150),
            (200, 100, 255), (255, 220, 180),
        ])

    def update(self, global_time):
        self.x += self.vx + math.sin(global_time * 3 + self.x * 0.01) * 0.5
        self.y += self.vy
        self.life -= self.decay
        if self.life <= 0 or self.y < -10:
            self.reset()

    def draw(self, surface):
        alpha = int(255 * self.life * 0.6)
        if alpha <= 0:
            return
        r, g, b = self.color
        size = max(1, int(self.size * self.life * 2) + 1)
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (r, g, b, alpha), (size, size), size)
        surface.blit(s, (self.x - size, self.y - size))


class LoveStorm:
    def __init__(self):
        self.num_particles = 800
        self.heart_targets = generate_heart_points(self.num_particles, scale=12)

        self.particles = []
        for tx, ty in self.heart_targets:
            self.particles.append(Particle(tx, ty))

        self.sparks = [SparkParticle() for _ in range(100)]
        self.stars = [StarParticle() for _ in range(80)]
        self.pulse_rings = []

        self.global_time = 0

        # 阶段控制
        self.phase = 'converge'
        self.phase_time = 0
        self.phase_durations = {
            'converge': 8.0,
            'heartbeat': 3.0,
            'reconverge': 8.0,
        }

        # 心跳
        self.heartbeat_scale = 1.0
        self.heartbeat_count = 0
        self.last_beat_time = 0

        # 屏幕震动
        self.shake_x = 0
        self.shake_y = 0
        self.shake_intensity = 0

        # 闪光
        self.flash_alpha = 0

        # 文字
        self.show_text = False
        self.text_alpha = 0

        # 字体
        self.font_large = pygame.font.SysFont("Microsoft YaHei", 40, bold=True)
        self.font_small = pygame.font.SysFont("Microsoft YaHei", 20)

    def _get_phase_color(self):
        if self.phase in ('converge', 'reconverge'):
            return (255, 105, 180)
        elif self.phase == 'heartbeat':
            return (255, 50, 80)
        elif self.phase == 'explode':
            return (255, 80, 120)
        return (255, 105, 180)

    def _lerp_color(self, c1, c2, t):
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )

    def _transition_to(self, new_phase):
        self.phase = new_phase
        self.phase_time = 0

        if new_phase == 'heartbeat':
            self.heartbeat_count = 0
            self.last_beat_time = 0
            self.show_text = True

        elif new_phase == 'explode':
            self.flash_alpha = 100
            self.shake_intensity = 15
            center_x = WIDTH // 2
            center_y = HEIGHT // 2 - 40
            for p in self.particles:
                p.start_explode(center_x, center_y)
            self.show_text = False

        elif new_phase == 'reconverge':
            self.heart_targets = generate_heart_points(self.num_particles, scale=12)
            for i, p in enumerate(self.particles):
                p.target_x = self.heart_targets[i][0]
                p.target_y = self.heart_targets[i][1]
                p.reset_from_landed()

    def update(self):
        dt = 1 / 30
        self.global_time += dt
        self.phase_time += dt

        # 颜色渐变（非爆炸阶段）
        if self.phase not in ('explode',):
            target_color = self._get_phase_color()
            for p in self.particles:
                if p.state not in ('exploding', 'landed'):
                    p.current_color = self._lerp_color(p.current_color, target_color, 0.02)

        # 震动衰减
        if self.shake_intensity > 0:
            self.shake_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_y = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity *= 0.9
            if self.shake_intensity < 0.5:
                self.shake_intensity = 0
                self.shake_x = 0
                self.shake_y = 0

        # 闪光衰减
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 5)

        # 阶段逻辑
        if self.phase == 'converge':
            formed = sum(1 for p in self.particles if p.state == 'done')
            for p in self.particles:
                p.update(dt, self.global_time)
            if formed > self.num_particles * 0.85 or self.phase_time > self.phase_durations['converge']:
                self._transition_to('heartbeat')

        elif self.phase == 'heartbeat':
            beat_interval = 0.8
            time_in_beat = (self.phase_time - self.last_beat_time)

            if time_in_beat > beat_interval and self.heartbeat_count < 3:
                self.last_beat_time = self.phase_time
                self.heartbeat_count += 1
                self.pulse_rings.append(PulseRing(WIDTH // 2, HEIGHT // 2 - 40, self._get_phase_color()))
                self.shake_intensity = 3

            t = (self.phase_time % beat_interval) / beat_interval
            if t < 0.15:
                self.heartbeat_scale = 1.0 + 0.12 * math.sin(t / 0.15 * math.pi)
            elif t < 0.3:
                self.heartbeat_scale = 1.0 + 0.06 * math.sin((t - 0.15) / 0.15 * math.pi)
            else:
                self.heartbeat_scale = 1.0

            for p in self.particles:
                p.update(dt, self.global_time, self.heartbeat_scale)

            if self.phase_time > self.phase_durations['heartbeat']:
                self._transition_to('explode')

        elif self.phase == 'explode':
            for p in self.particles:
                p.update(dt, self.global_time)

            # 等全部粒子落地后才进入汇聚
            landed_count = sum(1 for p in self.particles if p.landed)
            if landed_count >= self.num_particles:
                self._transition_to('reconverge')

        elif self.phase == 'reconverge':
            formed = sum(1 for p in self.particles if p.state == 'done')
            for p in self.particles:
                p.update(dt, self.global_time)
            if formed > self.num_particles * 0.85 or self.phase_time > self.phase_durations['reconverge']:
                self._transition_to('heartbeat')

        # 脉冲光环
        self.pulse_rings = [ring for ring in self.pulse_rings if ring.update()]

        # 火花
        for spark in self.sparks:
            spark.update(self.global_time)

        # 文字淡入淡出
        if self.show_text and self.text_alpha < 255:
            self.text_alpha = min(255, self.text_alpha + 4)
        elif not self.show_text and self.text_alpha > 0:
            self.text_alpha = max(0, self.text_alpha - 6)

    def draw(self):
        # 拖影
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill(BG_COLOR)
        fade_surface.set_alpha(50)
        screen.blit(fade_surface, (int(self.shake_x), int(self.shake_y)))

        # 星空
        for star in self.stars:
            star.draw(screen, self.global_time)

        # 火花
        for spark in self.sparks:
            spark.draw(screen)

        # 脉冲光环
        for ring in self.pulse_rings:
            ring.draw(screen)

        # 粒子
        for p in self.particles:
            p.draw(screen, self.global_time)

        # 闪光
        if self.flash_alpha > 0:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 220, 255, self.flash_alpha))
            screen.blit(flash, (0, 0))

        # 文字
        if self.text_alpha > 0:
            text_surf = self.font_large.render("恋恋风辰zack", True, (255, 180, 200))
            text_surf.set_alpha(self.text_alpha)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
            screen.blit(text_surf, text_rect)

            sub_text = self.font_small.render("每一颗粒子都是我对你的爱", True, (255, 150, 180))
            sub_text.set_alpha(int(self.text_alpha * 0.7))
            sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
            screen.blit(sub_text, sub_rect)

        pygame.display.flip()


def main():
    storm = LoveStorm()
    screen.fill(BG_COLOR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    storm = LoveStorm()
                    screen.fill(BG_COLOR)

        storm.update()
        storm.draw()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()