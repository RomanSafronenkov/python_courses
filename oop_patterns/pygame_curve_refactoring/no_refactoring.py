import pygame
import random


class Vec2d:
    """
    An object of type vector has two coordinates,
    methods for adding subtraction and multiplying vectors.
    """

    def __init__(self, *args):
        """
        Vector initialization, passed parameters:
        no parameters, or
        Vec2d, or
        int | float, int | float.
        """
        self.x = 0
        self.y = 0
        if len(args) == 1:
            if not isinstance(args[0], Vec2d):
                raise TypeError('The parameter must be of type Vec2d!')
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            if not((isinstance(args[0], int) or isinstance(args[0], float)) and
                   (isinstance(args[1], int) or isinstance(args[1], float))
                   ):
                raise TypeError('Parameters must be int or float!')
            self.x = args[0]
            self.y = args[1]
        elif len(args) > 2:
            raise TypeError(
                f'input expected at most 0, 1 or 2 arguments, got {len(args)}.')

    def __str__(self):
        return f'Vec2d({self.x}, {self.y})'

    def __add__(self, other):
        """
        Returns an object of type Vec2d summed with another object of type Vec2d.
        """
        if not isinstance(other, Vec2d):
            raise TypeError(
                'Addition is possible only with an object of type Vec2d!')
        result = Vec2d(self.x, self.y)
        result.x += other.x
        result.y += other.y
        return result

    def __iadd__(self, other):
        """
        Summed with another object of type Vec2d.
        """
        if not isinstance(other, Vec2d):
            raise TypeError(
                'Addition is possible only with an object of type Vec2d!')
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        """
        Returns an object of type Vec2d,
        the result of subtraction with another object of type Vec2d.
        """
        if not isinstance(other, Vec2d):
            raise TypeError(
                'Subtraction is possible only with an object of type Vec2d!')
        result = Vec2d(self.x, self.y)
        result.x -= other.x
        result.y -= other.y
        return result

    def __isub__(self, other):
        """
        The result of subtraction with another object of type Vec2d.
        """
        if not isinstance(other, Vec2d):
            raise TypeError(
                'Subtraction is possible only with an object of type Vec2d!')
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, multiplier):
        """
        Returns an object of type Vec2d,
        the result of multiplication with number.
        """
        result = Vec2d(self.x, self.y)
        if not (isinstance(multiplier, int) or isinstance(multiplier, float)):
            raise TypeError(
                'Multiplication is possible only with an object of type int or float!')
        result.x *= multiplier
        result.y *= multiplier
        return result

    def __imul__(self, multiplier):
        """
        Returns an object of type Vec2d,
        the result of multiplication with number.
        """
        if not (isinstance(multiplier, int) or isinstance(multiplier, float)):
            raise TypeError(
                'Multiplication is possible only with an object of type int or float!')
        self.x *= multiplier
        self.y *= multiplier
        return self

    def __len__(self):
        """
        Returns the scalar length of an object of type Vec2d.
        """
        return (self.x*self.x + self.y*self.y)**0.5

    def int_pair(self):
        """
        Returns the current coordinates of the vector.
        """
        return (int(self.x), int(self.y))


class Polyline():
    """
    The object is a closed polygon,
    has a list of dictionaries containing
    the coordinate and speed of the reference point,
    methods for adding and deleting points,
    and methods for calculating and drawing points.
    """

    def __init__(self, width, height, speed):
        """
        Initializing a closed polygon,
        takes the width and height parameters of the drawing area.
        """
        self.polyline = []
        self.width = width
        self.height = height
        self.speed = speed

    def __str__(self):
        result = ''
        if len(self.polyline) > 0:
            result = map(lambda x: '(position: {0}, speed: {1})'.
                         format(x['position'],  x['speed']),
                         self.polyline)
            result = ',\n'.join(result)
        return f"Polyline[\n{result}\n]"

    def add(self, point, speed):
        """
        Adds an anchor point to the curve.
        """
        self.polyline.append({'position': point, 'speed': speed})

    def remove(self):
        """
        Deletes the last added point from the curve.
        """
        self.polyline.pop()

    def set_speed(self, speed):
        self.speed = speed

    def set_points(self):
        """
        Recalculates the coordinates of points.
        """
        for i in range(len(self.polyline)):
            self.polyline[i]['position'] += self.polyline[i]['speed'] * self.speed
            x, y = self.polyline[i]['position'].int_pair()
            if x < 0 or x > self.width:
                self.flip_speed(i, 'x')
            if y < 0 or y > self.height:
                self.flip_speed(i, 'y')

    def draw_points(self, display, color, line_width):
        """
        Drawing points in the drawing area.
        """
        for point in self.polyline:
            pygame.draw.circle(
                display, color, point['position'].int_pair(), line_width)

    def flip_speed(self, i, key):
        """
        Inverts the speed.
        """
        if key == 'x':
            self.polyline[i]['speed'].x = -self.polyline[i]['speed'].x
        elif key == 'y':
            self.polyline[i]['speed'].y = -self.polyline[i]['speed'].y


class Knot(Polyline):
    """
    A closed curve object that calculates
    curve points based on control points.
    """

    def __init__(self, width, height, speed, steps):
        super().__init__(width, height, speed)
        self.curve = []
        self.steps = steps

    def add(self, point, speed):
        """
        Adds an anchor point to the polyline.
        """
        super().add(point, speed)
        self.get_knot()

    def remove(self):
        """
        Deletes the last added point from the polyline.
        """
        super().remove()
        self.get_knot()

    def set_steps(self, steps):
        """
        Sets the number of smoothing steps.
        """
        self.steps = steps
        self.get_knot()

    def set_points(self):
        """
        Recalculates the coordinates of polyline points.
        """
        super().set_points()
        self.get_knot()

    def get_knot(self):
        """
        Calculated the coordinates of curve points.
        """
        self.curve = []
        if len(self.polyline) >= 3:
            count = len(self.polyline)
            accessory = [Vec2d() for _ in range(count)]
            deltas = [Vec2d() for _ in range(count)]
            for i in range(-1, count - 1):  # Preparation of supporting data.
                point1 = self.polyline[i]['position']
                point2 = self.polyline[i + 1]['position']
                accessory[i + 1] = (point1 + point2) * 0.5
                deltas[i + 1] = (point2 - point1) * (1/(2 * self.steps))
            for i in range(count):
                point1 = accessory[i - 1]
                point2 = self.polyline[i - 1]['position']
                delta1 = deltas[i - 1]
                delta2 = deltas[i]
                for j in range(self.steps):  # Calculation of the Bezier curve.
                    start = point1 + delta1 * j
                    end = point2 + delta2 * j
                    delta = (end - start) * (1/self.steps)
                    self.curve.append(start + delta * j)

    def draw_points(self, display, color, line_width):
        """
        Drawing points and curve in the drawing area.
        """
        super().draw_points(display, color, line_width)
        if len(self.polyline) >= 3:
            for i in range(len(self.curve)):
                start = self.curve[i - 1].int_pair()
                end = self.curve[i].int_pair()
                pygame.draw.line(display, color, start, end, line_width)


class Screen():
    """
    A class with a main application event loop.
    """

    def __init__(self, width, height):
        """
        Initialization of the application.
        """
        self.width = width
        self.height = height

        self.steps = 10
        self.speed = 1.0

        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("MyScreenSaver")

        self.hue = 0
        self.color = pygame.Color(0)
        self.line_width = 3

        self.help = Help(self.width, self.height, self.speed, self.steps)

        self.knots = []
        self.knots.append(
            Knot(self.width, self.height, self.speed, self.steps))

        self.working = True
        self.show_help = False
        self.pause = True

    def run(self):
        """
        Launching the main application loop.
        """
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousedown(event)

            self.redraw()

        pygame.display.quit()
        pygame.quit()

    def keydown(self, event):
        """
        The function of handling the keypress event.
        """
        if event.key == pygame.K_ESCAPE:
            self.working = False
        if event.key == pygame.K_r:
            self.knots = []
            self.knots.append(Knot(self.width,
                                    self.height,
                                    self.speed,
                                    self.steps))
        if event.key == pygame.K_p:
            self.pause = not self.pause
        if event.key == pygame.K_KP_PLUS:
            self.steps += 1
            self.help.set_steps(self.steps)
            for item in self.knots:
                item.set_steps(self.steps)
        if event.key == pygame.K_KP_MINUS:
            self.steps -= 1 if self.steps > 1 else 0
            self.help.set_steps(self.steps)
            for item in self.knots:
                item.set_steps(self.steps)
        if event.key == pygame.K_F1:
            self.show_help = not self.show_help
        if event.key == pygame.K_PAGEUP:
            self.speed += 0.1
            self.speed = round(self.speed, 1)
            self.help.set_speed(self.speed)
            for item in self.knots:
                item.set_speed(self.speed)
        if event.key == pygame.K_PAGEDOWN:
            self.speed -= 0.1 if self.speed > 0.101 else 0
            self.speed = round(self.speed, 1)
            self.help.set_speed(self.speed)
            for item in self.knots:
                item.set_speed(self.speed)

    def mousedown(self, event):
        """
        Function for handling mouse click events.
        """
        if event.button == 1:
            point = Vec2d(*event.pos)
            speed = Vec2d((random.random() - 0.5) * 2,
                          (random.random() - 0.5) * 2)
            self.knots[-1].add(point, speed)
        if event.button == 2:
            if len(self.knots[-1].polyline) != 0:
                self.knots.append(Knot(self.width,
                                       self.height,
                                       self.speed,
                                       self.steps))
        if event.button == 3:
            try:
                self.knots[-1].remove()
            except IndexError:
                if len(self.knots) > 1:
                    self.knots.pop()

    def redraw(self):
        """
        Screen redraw function.
        """
        self.display.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

        for item in self.knots:
            item.draw_points(self.display, self.color, self.line_width)
        if not self.pause:
            for item in self.knots:
                item.set_points()
        if self.show_help:
            self.help.show_help(self.display)

        pygame.display.flip()


class Help():
    """
    Class to display help.
    """

    def __init__(self, width, height, speed, steps):
        """
        Help initialization.
        """
        self.width = width
        self.height = height

        self.data = []
        self.data.append(["F1", "Show Help"])
        self.data.append(["R", "Restart"])
        self.data.append(["P", "Pause/Play"])
        self.data.append(["Num+", "More smoothing steps"])
        self.data.append(["Num-", "Less smoothing steps"])
        self.data.append(["PgUp", "More speed"])
        self.data.append(["PgDown", "Less speed"])
        self.data.append(["LMB", "Add point"])
        self.data.append(["MMB", "Add curve"])
        self.data.append(["RMB", "Delete point"])
        self.data.append(["", ""])
        self.data.append([str(steps), "Current points"])
        self.data.append([str(speed), "Current speed"])

        self.frame_color = (255, 50, 50, 255)
        self.frame_width = 5
        self.head = height // 6
        self.column1 = width // 8
        self.column2 = width // 2
        self.line_height = 30

        self.font1 = pygame.font.SysFont("courier", 24)
        self.font2 = pygame.font.SysFont("serif", 24)
        self.font_color = (128, 128, 255)

    def set_steps(self, key):
        """
        Updating the up-step counter.
        """
        self.data[-2][0] = str(key)

    def set_speed(self, key):
        """
        Updating the speed counter.
        """
        self.data[-1][0] = str(key)

    def show_help(self, display):
        """
        Display help content in the drawing area.
        """
        pygame.draw.lines(display,
                          self.font_color,
                          True,
                          [(0, 0), (self.width, 0),
                           (self.width, self.height), (0, self.height)],
                          self.frame_width)
        for i, text in enumerate(self.data):
            display.blit(self.font1.render(
                text[0],
                True,
                self.font_color), (self.column1, self.head + self.line_height * i))
            display.blit(self.font2.render(
                text[1],
                True,
                self.font_color), (self.column2, self.head + self.line_height * i))


if __name__ == "__main__":
    game = Screen(800, 600)
    game.run()