import pygame
import random

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2d(self.x * other, self.y * other)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def int_pair(self):
        return tuple([int(self.x), int(self.y)])


class Polyline:

    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, self.points[p_n].int_pair,
                                 self.points[p_n + 1].int_pair, width)
        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, p.int_pair, width)

    def del_point(self):
        if len(self.points) != 0:
            self.points.pop()

    def change_speed(self, coef):
        self.speeds = [Vec2d(vector.x * coef, vector.y * coef) for vector in self.speeds]


class Knot(Polyline):

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self._get_point(points, alpha, deg - 1) * (1 - alpha)

    def _get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self._get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [
                (self.points[i] + self.points[i + 1]) * 0.5,
                self.points[i + 1],
                (self.points[i + 1] + self.points[i + 2]) * 0.5
            ]
            res.extend(self._get_points(ptn, count))

        for p_n in range(-1, len(res) - 1):
            pygame.draw.line(gameDisplay, color, res[p_n].int_pair,
                             res[p_n + 1].int_pair, 3)


# ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [
        ["F1", "Show Help"],
        ["R", "Restart"],
        ["P", "Pause/Play"],
        ["Num+", "More points"],
        ["Num-", "Less points"],
        ["D", "Remove point"],
        ["â†‘ Up", "Increase speed x2"],
        ["â†“ Down", "Decrease speed x0.5"],
        ["", ""],
        ["Switch between lines (max - 3):", ""],
        ["1,2,3", "Line â„– 1, 2, 3"]
    ]
    data2 = [
        ["Current points:", str(steps)],
        ["Current line:", str(line_num)],
        ["Acceleration:", str('%.2E' % accel) + 'x']
    ]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 50 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 50 + 30 * i))

    for i, text in enumerate(data2):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * (i + len(data))))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (350, 100 + 30 * (i + len(data))))


# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    accel = 1.
    working = True
    line_key = pygame.K_1
    line_num = line_key - 48
    lines = {line_key: Knot()}
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    for key in lines:
                        lines[key].points = []
                        lines[key].speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_d:
                    lines[line_key].del_point()
                if event.key == pygame.K_UP:
                    accel = accel * 2
                    for key in lines:
                        lines[key].change_speed(2)
                if event.key == pygame.K_DOWN:
                    accel = accel * 0.5
                    for key in lines:
                        lines[key].change_speed(0.5)
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    line_key = event.key
                    line_num = line_key - 48
                    if line_key not in lines.keys():
                        lines[line_key] = Knot()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0], event.pos[1]
                lines[line_key].add_point(Vec2d(x, y), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for key in lines:
            lines[key].draw_points("points")
            lines[key].get_knot(steps)
        if not pause:
            for key in lines:
                lines[key].set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)