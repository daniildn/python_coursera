import math
import random

import pygame

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y

    def _sub_(self, v):  # разность двух векторов
        return Vec2d(self.x - v.x, self.y - v.y)

    def _add_(self, v):  # сумма двух векторов
        return Vec2d(self.x + v[0], self.y + v[1])

    def _len_(self):  # длина вектора
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def _mul_(self, v):  # скалярное умножение векторов
        if isinstance(v, Vec2d):
            return Vec2d(self.x * v.x, self.y * v.y)
        elif isinstance(v, int) or isinstance(v, float):
            return Vec2d(self.x * v, self.y * v)

    @property
    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def addVec(self, point, speed):
        self.points.append(Vec2d(*point))
        self.speeds.append(Vec2d(*speed))

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p]._add_(self.speeds[p])
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])

        # "Отрисовка" точекec2d' object does not support indexing

    def draw_points(self, points=None, style="points", width=3, color=(255, 255, 255)):
        # points = points if points else self.points
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, points[p_n].int_pair, points[p_n + 1].int_pair, width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, p.int_pair, width)

        # Персчитывание координат опорных точек


class Knot(Polyline):
    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg]._mul_(alpha)._add_(self.get_point(points, alpha, deg - 1)._mul_((1 - alpha)))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(self.points[i]._add_(self.points[i + 1])._mul_(0.5))
            ptn.append(self.points[i + 1])
            ptn.append(self.points[i + 1]._add_(self.points[i + 2])._mul_(0.5))

            res.extend(self.get_points(ptn, count))
        return res

    def draw_knot(self, count, style, width, color):
        self.draw_points(self.get_knot(count), style, width, color)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

def display_help():
    pass
# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True
    knot = Knot()
    hue = 0
    color = pygame.Color(0)
    display_help()
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False

                if event.key == pygame.K_r:
                    knot = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.addVec(event.pos, (random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.draw_knot(steps, "line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
