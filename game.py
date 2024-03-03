import pygame

pygame.init()
WIDTH = 600
HEIGHT = 600
UNIT = 25
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Draw a shape")

PADDING = 8

is_shape_finished = False


def overlap(p, corner):
    return corner[0] - PADDING <= p[0] <= corner[0] + PADDING and corner[1] - PADDING <= p[1] <= corner[1] + PADDING


def line_line_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if denom == 0:
        return False
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    return 0 <= t <= 1 and 0 <= u <= 1


def calc_size():
    a = 0
    for i, c in enumerate(corners):
        n_c = corners[(i + 1) % len(corners)]
        a += c[0] * n_c[1] - n_c[0] * c[1]
    return a / 2 / (UNIT ** 2)


corners = []

m = None
n = None

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if len(corners) == 0:
                    corners.append(pos)
                elif len(corners) == 1:
                    if pos != corners and not overlap(pos, corners[0]):
                        corners.append(pos)
                else:
                    num_overlap = len(set(x for x in corners if overlap(pos, x)))
                    if len(set(x for x in corners if overlap(pos, x))) == 1:
                        if overlap(pos, corners[0]):
                            print(calc_size())
                            is_shape_finished = True
                    elif not is_shape_finished:
                        m = None
                        n = None
                        has_overlap = False
                        for i in range(len(corners) - 2):
                            if line_line_intersection(corners[-1], pos, corners[i], corners[i + 1]):
                                m = corners[i]
                                n = corners[i + 1]
                                has_overlap = True
                                break
                        if not has_overlap:
                            corners.append(pos)

    screen.fill((255, 255, 255))

    for x in range(WIDTH // UNIT):
        pygame.draw.line(screen, (0, 0, 0), (x * 25, 0), (x * 25, HEIGHT), 1)

    for y in range(HEIGHT // UNIT):
        pygame.draw.line(screen, (0, 0, 0), (0, y * 25), (WIDTH, y * 25), 1)

    for i, (x, y) in enumerate(corners):
        pygame.draw.rect(screen, (255 if i == 0 else 125, 0 if i == 0 else 125, 0 if i == 0 else 125),
                         (x - PADDING, y - PADDING, PADDING * 2, PADDING * 2))

    for i, (x, y) in enumerate(corners):
        if not is_shape_finished and i == len(corners) - 1:
            continue
        pygame.draw.line(screen, (0, 0, 255), (x, y), corners[(i + 1) % len(corners)])

    if m:
        pygame.draw.line(screen, (255, 0, 255), m, n)

    pygame.display.flip()

pygame.quit()
