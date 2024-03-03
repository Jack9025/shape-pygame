import pygame
import tkinter as tk

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
    """Determines if there is an overlap in the box"""
    return corner[0] - PADDING <= p[0] <= corner[0] + PADDING and corner[1] - PADDING <= p[1] <= corner[1] + PADDING


def line_seg_intersection(p1, p2, p3, p4):
    """Check if line segments l1 (points p1 and p2) and l2 (points p3 and p4) intersect"""
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
    """Calculate area of shape using shoelace formula"""
    a = 0
    for i, c in enumerate(vertices):
        n_c = vertices[(i + 1) % len(vertices)]
        a += c[0] * n_c[1] - n_c[0] * c[1]
    return a / 2 / (UNIT ** 2)


def check_guess():
    """Checks the guess submitted by the user"""
    global root
    number = -1
    try:
        number = float(entry.get())
    except ValueError:
        pass

    if number >= 0:
        root.destroy()
        root = tk.Tk()
        root.title("Outcome of your guess.")
        text_label = tk.Label(root, text=f"You guessed {number} and the actual area was {round(calc_size(), 2)}")
        text_label.pack()
        root.geometry("450x80")


def add_vertex():
    """Adds vertex to shape if allowed"""
    global is_shape_finished, m, n

    pos = pygame.mouse.get_pos()
    if len(vertices) == 0:
        vertices.append(pos)
    elif len(vertices) == 1:
        if pos != vertices and not overlap(pos, vertices[0]):
            vertices.append(pos)
    else:
        num_overlap = len(set(x for x in vertices if overlap(pos, x)))
        if len(set(x for x in vertices if overlap(pos, x))) == 1:
            if overlap(pos, vertices[0]):
                is_shape_finished = True
        elif not is_shape_finished:
            m = None
            n = None
            has_overlap = False
            for i in range(len(vertices) - 2):
                if line_seg_intersection(vertices[-1], pos, vertices[i], vertices[i + 1]):
                    m = vertices[i]
                    n = vertices[i + 1]
                    has_overlap = True
                    break
            if not has_overlap:
                vertices.append(pos)


vertices = []
guessed = False

m = None
n = None

# Guess window
root = tk.Tk()
root.title("Guess the area of the shape you have drawn.")
entry = tk.Entry(root)
entry.pack(pady=10)
button = tk.Button(root, text="Submit guess", command=check_guess)
button.pack()
root.geometry("450x80")
root.withdraw()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONDOWN:
                add_vertex()

    # Draw background
    screen.fill((255, 255, 255))

    # Draw grid lines vertically
    for x in range(WIDTH // UNIT):
        pygame.draw.line(screen, (0, 0, 0), (x * 25, 0), (x * 25, HEIGHT), 1)

    # Draw grid lines horizontally
    for y in range(HEIGHT // UNIT):
        pygame.draw.line(screen, (0, 0, 0), (0, y * 25), (WIDTH, y * 25), 1)

    # Draw vertices
    for i, (x, y) in enumerate(vertices):
        pygame.draw.rect(screen, (255 if i == 0 else 125, 0 if i == 0 else 125, 0 if i == 0 else 125),
                         (x - PADDING, y - PADDING, PADDING * 2, PADDING * 2))

    # Draw lines between vertices
    for i, (x, y) in enumerate(vertices):
        if not is_shape_finished and i == len(vertices) - 1:
            continue
        pygame.draw.line(screen, (0, 0, 255), (x, y), vertices[(i + 1) % len(vertices)])

    # Draw line of where vertex selected by user is intercepting the two other points
    if m:
        pygame.draw.line(screen, (255, 0, 255), m, n)

    pygame.display.flip()

    # Show guess window if shape is completed
    if is_shape_finished and not guessed:
        root.deiconify()
        guessed = True

    root.update()

pygame.quit()
