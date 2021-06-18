import random
import math

import pygame


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2d(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2d(x, y)

    def __mul__(self, k):
        x = self.x * k
        y = self.y * k
        return Vec2d(x, y)

    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    def int_pair(self):
        return self.x, self.y


class Polyline:
    def __init__(self, display, steps, screen_dim):
        self.display = display
        self.steps = steps
        self.screen_dim = screen_dim

    def set_points(self, points, speeds):
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]
            if points[p].x > self.screen_dim[0] or points[p].x < 0:
                speeds[p] = Vec2d(-speeds[p].x, speeds[p].y)
            if points[p].y > self.screen_dim[1] or points[p].y < 0:
                speeds[p] = Vec2d(speeds[p].x, -speeds[p].y)

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.display, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.display, color,
                                   (int(p.x), int(p.y)), width)

    def draw_help(self):
        self.display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [
            ["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["Q", "Speed up"],
            ["E", "Slow down"],
            ["LEFT_MOUSE_BUTTON", "Add point"],
            ["RIGHT_MOUSE_BUTTON", "Delete last point"],
            ["", ""],
            [str(self.steps), "Current points"]
        ]

        pygame.draw.lines(self.display, (255, 50, 50, 255), True, [
            (0, 0), (self.screen_dim[0], 0), (self.screen_dim[0], self.screen_dim[1]), (0, self.screen_dim[1])], 5)
        for i, text in enumerate(data):
            self.display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.display.blit(font2.render(
                text[1], True, (128, 128, 255)), (400, 100 + 30 * i))


class Knot(Polyline):

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, points):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = [
                (points[i] + points[i + 1]) * 0.5,
                points[i + 1],
                (points[i + 1] + points[i + 2]) * 0.5
            ]

            res.extend(self.get_points(ptn, self.steps))
        return res


class Play:
    def __init__(self, screen_dim):
        self.SCREEN_DIM = screen_dim
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = True
        self.hue = 0
        self.color = pygame.Color(0)

        pygame.init()
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")
        self.knot = Knot(display=self.gameDisplay, steps=50, screen_dim=self.SCREEN_DIM)

    def play(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.points = []
                        self.speeds = []
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.knot.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.knot.steps -= 1 if self.knot.steps > 1 else 0
                    if event.key == pygame.K_q:
                        if len(self.speeds):
                            for i in range(len(self.speeds)):
                                self.speeds[i] = self.speeds[i] * 1.5
                    if event.key == pygame.K_e:
                        if len(self.speeds):                  
                            for i in range(len(self.speeds)):
                                self.speeds[i] = self.speeds[i] * 0.5

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.points.append(Vec2d(*event.pos))
                        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))
                    elif event.button == 3:
                        if len(self.points) != 0:
                            del self.points[-1]
                            del self.speeds[-1]

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            self.knot.draw_points(self.points, style="points")
            self.knot.draw_points(self.knot.get_knot(self.points), style="line", color=self.color)
            if not self.pause:
                self.knot.set_points(self.points, self.speeds)
            if self.show_help:
                self.knot.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    play = Play((900, 600))
    play.play()
