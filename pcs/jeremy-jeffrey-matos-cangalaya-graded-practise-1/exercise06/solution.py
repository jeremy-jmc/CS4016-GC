import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import numpy as np
random.seed(123)

WIDTH, HEIGHT = 1280, 720

def get_random_color() -> tuple:
    """Generate a random color"""
    return tuple(random.randint(0, 255) for _ in range(3))

class Circle:

    def __init__(self, x: int, y: int, r: int, color: tuple = None):
        if color is None:
            color = get_random_color()
        self.x = x
        self.y = y
        self.r = r
        self.dx = (1 if random.randint(0, 1) == 1 else -1) * 2
        self.dy = (1 if random.randint(0, 1) == 1 else -1) * 2
        self.color = color

    def draw(self, img: np.ndarray):
        """Draw the circle on the image"""
        cv2.circle(img, (self.x, self.y), self.r, self.color, -1)

    def move(self):
        """Move the circle and change direction if it hits the border"""
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.dx *= -1
            self.x = WIDTH - self.r if self.x + self.r >= WIDTH else self.x

        if self.y + self.r >= HEIGHT or self.y - self.r <= 0:
            self.dy *= -1
            self.y = HEIGHT - self.r if self.y + self.r >= HEIGHT else self.y

        self.x += self.dx
        self.y += self.dy


def collides(c1: Circle, c2: Circle) -> bool:
    return (c1.x - c2.x)**2 + (c1.y - c2.y)**2 < (c1.r + c2.r)**2


if __name__ == '__main__':
    N = 100
    circles = [Circle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 10) for _ in range(N)]

    while True:
        img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

        for i in circles:
            i.move()
            for j in circles:
                # manage collisions
                if i != j and collides(i, j):
                    i.dx *= -1
                    i.dy *= -1
                    j.dx *= -1
                    j.dy *= -1
                    j.move()
                    i.move()

                    j.draw(img)
            i.draw(img)

        cv2.imshow('Visualizador', img)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()
