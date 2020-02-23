import pygame
from pygame.locals import *
import random

def apply_scale(orig_image, factor):
    '''
    Returns a copy of <orig_image> scaled by <factor> as well as the new
    dimensions of the scaled image.
    '''
    orig_dims = orig_image.get_size()
    new_dims = (int(orig_dims[0] * factor), int(orig_dims[1] * factor))
    image = pygame.transform.smoothscale(orig_image, new_dims)

    return image, new_dims

def adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos):
    return [
        -(mouse_pos[0] - SCREEN_DIMS[0] * 0.5 - map_pos[0] * old_dims[0]) / old_dims[0] - (SCREEN_DIMS[0] * 0.5 - mouse_pos[0]) / scaled_dims[0],
        -(mouse_pos[1] - SCREEN_DIMS[1] * 0.5 - map_pos[1] * old_dims[1]) / old_dims[1] - (SCREEN_DIMS[1] * 0.5 - mouse_pos[1]) / scaled_dims[1]
    ]


def display_map(screen, image, pos):
    image_dims = image.get_size()

    image_x = SCREEN_DIMS[0] * 0.5 - map_pos[0] * scaled_dims[0]
    image_y = SCREEN_DIMS[1] * 0.5 - map_pos[1] * scaled_dims[1]

    screen.blit(scaled_image, (image_x, image_y))


def generate_locations():
    return [(random.random(), random.random()) for _ in range(30)]


def map_to_pix(scaled_dims, map_pos, pos):
    return [
        int(SCREEN_DIMS[0] * 0.5 - map_pos[0] * scaled_dims[0] + pos[0] * scaled_dims[0]),
        int(SCREEN_DIMS[1] * 0.5 - map_pos[1] * scaled_dims[1] + pos[1] * scaled_dims[1]),
    ]


def draw_locations(screen, scaled_dims, map_pos, locations):
    for loc in locations:
        coords = map_to_pix(scaled_dims, map_pos, loc)
        pygame.draw.circle(screen, (255, 0, 0), coords, 10)


def load_images():
    images = []
    for i in range(1, 100):
        print("Loading {}...".format(i))
        images.append(pygame.image.load("/Users/nicholas_schweitzer/OneDrive - Munich International School/school/10B/Design/program/scaled-maps/{}.png".format(i)))

    return images


def create_icon():
    font = pygame.font.Font(pygame.font.get_default_font(), 32)

    return font.render("F", True, (0, 0, 0))


def icon_at(coords):
    SCREEN.blit(ICON_SURFACE, (coords[0] - ICON_SURFACE.get_width() // 2, coords[1] - ICON_SURFACE.get_height())


pygame.init()
SCREEN_DIMS = (1440, 900)
screen = pygame.display.set_mode(SCREEN_DIMS)
done = False

ICON_SURFACE = create_icon()

image = pygame.image.load("/Users/nicholas_schweitzer/OneDrive - Munich International School/school/10B/Design/germany-map.png")

map_pos = [0.0, 0.0]

images = load_images()

cur_scale = 20

scaled_image = images[cur_scale]
scaled_dims = scaled_image.get_size()

interesting_locations = generate_locations()

while not done:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (1440 - mouse_pos[0], 900 - mouse_pos[1])

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

            if event.key == K_e:
                cur_scale += 1

                if cur_scale >= len(images):
                    cur_scale = len(images) - 1

                scaled_image = images[cur_scale]
                old_dims = scaled_dims
                scaled_dims = scaled_image.get_size()

                map_pos = adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos)

            if event.key == K_r:
                cur_scale -= 1

                if cur_scale < 0:
                    cur_scale = 0

                scaled_image = images[cur_scale]
                old_dims = scaled_dims
                scaled_dims = scaled_image.get_size()

                map_pos = adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos)

        if event.type == MOUSEMOTION:
            if event.buttons == (1, 0, 0):
                map_pos[0] -= event.rel[0] / scaled_dims[0]
                map_pos[1] -= event.rel[1] / scaled_dims[1]

        if event.type == MOUSEWHEEL:
            cur_scale += event.y

            if cur_scale >= len(images):
                cur_scale = len(images) - 1
            elif cur_scale < 0:
                cur_scale = 0

            scaled_image = images[cur_scale]
            old_dims = scaled_dims
            scaled_dims = scaled_image.get_size()

            map_pos = adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos)


    screen.fill((255, 0, 0))

    display_map(screen, scaled_image, map_pos)
    draw_locations(screen, scaled_dims, map_pos, interesting_locations)

    pygame.display.flip()
