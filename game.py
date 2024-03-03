import pygame

pygame.init()
size = (600, 600)
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
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    return 0 <= t <= 1 and 0 <= u <= 1


corners = []

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
                            is_shape_finished = True
                    elif not is_shape_finished:
                        has_overlap = False
                        for i in range(len(corners) - 1):
                            if line_line_intersection(corners[-1], pos, corners[i], corners[i + 1]):
                                has_overlap = True
                                break
                        if not has_overlap:
                            corners.append(pos)

    screen.fill((0, 0, 0))

    for i, (x, y) in enumerate(corners):
        pygame.draw.rect(screen, (255 if i == 0 else 50, 255 if i == 1 else 50, 255 if i == 2 else 50), (x - PADDING, y - PADDING, PADDING * 2, PADDING * 2))

    for i, (x, y) in enumerate(corners):
        if not is_shape_finished and i == len(corners) - 1:
            continue
        pygame.draw.line(screen, (0, 0, 255), (x, y), corners[(i + 1) % len(corners)])

    pygame.display.flip()

pygame.quit()
