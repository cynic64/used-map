import pygame
from pygame.locals import *
import random

import os
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

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


def display_map(image, pos):
    image_dims = image.get_size()

    image_x = int(SCREEN_DIMS[0] * 0.5 - map_pos[0] * scaled_dims[0])
    image_y = int(SCREEN_DIMS[1] * 0.5 - map_pos[1] * scaled_dims[1])

    SCREEN.blit(scaled_image, (image_x, image_y))


def read_locations():
    locations = []

    path = "database.txt"

    f = open(path, "r")
    lines = f.read().split("\n")[:-1]

    for line in lines:
        chunks = line.split(", ")
        x = float(chunks[0])
        y = float(chunks[1])
        name = chunks[2]

        locations.append((x, y, name))

    return locations


def map_to_pix(scaled_dims, map_pos, pos):
    return [
        int(SCREEN_DIMS[0] * 0.5 - map_pos[0] * scaled_dims[0] + pos[0] * scaled_dims[0]),
        int(SCREEN_DIMS[1] * 0.5 - map_pos[1] * scaled_dims[1] + pos[1] * scaled_dims[1]),
    ]


def draw_locations(scaled_dims, map_pos, locations):
    for loc in locations:
        coords = map_to_pix(scaled_dims, map_pos, (loc[0], loc[1]))
        icon_at(coords, loc[2])


def draw_key():

    pygame.draw.rect(SCREEN, (180, 180, 180), (3, 20, 150, 230))
    pygame.draw.rect(SCREEN, (0, 0, 0), (3, 20, 150, 230), 2)
    y = 50
    for key in list("FTECIO"):
        icon_at((20, y), key)

        surf = KEY_SURFACES[key]
        SCREEN.blit(surf, (40, y - surf.get_height() // 2))
        y += 30


def load_images():
    images = []
    for i in range(1, 70):
        print("Loading {}...".format(i))
        images.append(pygame.image.load("{}/scaled-maps/{}.png".format(BASE_PATH, i)))

    return images


def create_icons():
    font = pygame.font.Font(pygame.font.get_default_font(), 16)

    icons = {}

    for text in list("FTECIO"):
        icons[text] = font.render(text, True, (0, 0, 0))

    return icons


def create_key_surfaces():
    font = pygame.font.Font(pygame.font.get_default_font(), 16)

    surfaces = {}

    for text in list("FTECIO"):
        surfaces[text] = font.render(ICON_KEYS[text], True, (0, 0, 0))

    return surfaces


def icon_at(coords, key):
    pygame.draw.circle(SCREEN, ICON_COLORS[key], coords, 13)
    surface = ICONS[key]
    SCREEN.blit(surface, (coords[0] - surface.get_width() // 2, coords[1] - surface.get_height() // 2))


def display_detail():
    pygame.draw.rect(SCREEN, (180, 180, 180), (1440-400, 450-240, 380, 330))
    pygame.draw.rect(SCREEN, (0, 0, 0), (1440-400, 450-240, 380, 330), 2)

    title_font = pygame.font.Font(pygame.font.get_default_font(), 30)

    title_surf = title_font.render("Ikea Sofa Bed (Navy Blue)", True, (0, 0, 0))
    SCREEN.blit(title_surf, (1440-400+5, 450-240+5))

    address_font = pygame.font.Font(pygame.font.get_default_font(), 10)
    address_surf = address_font.render("Sundgauallee, 46,  79110 Baden-Württemberg - Freiburg", True, (64, 64, 64))
    SCREEN.blit(address_surf, (1440-400+5, 450-240+170))

    t = """
Top Zustand
Kissen sind versetzbar
Maße: Höhe 46 cm , Tiefe 111cm , Breite 200cm
Bitte Selbstabholung
Originalpreis: 2400€
"""

    y = 450-240+170+10

    for line in t.split("\n"):
        surf = address_font.render(line, True, (0, 0, 0))

        SCREEN.blit(surf, (1440-400+5, y))

        y += 20

    SCREEN.blit(SOFA, (1440-400+5, 450-240+40))


pygame.init()
SCREEN_DIMS = (1440, 900)
SCREEN = pygame.display.set_mode(SCREEN_DIMS)
done = False

ICONS = create_icons()
ICON_COLORS = {
    "F": (200, 140, 80),
    "T": (127, 127, 127),
    "E": (170, 250, 30),
    "C": (100, 200, 90),
    "I": (230, 230, 100),
    "O": (230, 230, 230),
}

image = pygame.image.load("{}/scaled-maps/100.png".format(BASE_PATH))
map_pos = [0.0, 0.0]

images = load_images()

cur_scale = 9

scaled_image = images[cur_scale]
scaled_dims = scaled_image.get_size()

interesting_locations = read_locations()

overlay = pygame.image.load("{}/icons/overlay.png".format(BASE_PATH))

SOFA = pygame.image.load("icons/sofa.jpg")

ICON_KEYS = {
    "F": "Furniture",
    "T": "Tools",
    "E": "Electronics",
    "C": "Clothing",
    "I": "Instruments",
    "O": "Other",
}
KEY_SURFACES = create_key_surfaces()

detail = False

while not done:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (1440 - mouse_pos[0], 900 - mouse_pos[1])

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

            elif event.key == K_SPACE:
                map_tl = (
                    SCREEN_DIMS[0] * 0.5 - map_pos[0] * scaled_dims[0],
                    SCREEN_DIMS[1] * 0.5 - map_pos[1] * scaled_dims[1]
                )
                mp_t = (1440 - mouse_pos[0], 900 - mouse_pos[1])
                mouse_rel = (mp_t[0] - map_tl[0], mp_t[1] - map_tl[1])
                print("{}, {}".format(mouse_rel[0] / scaled_dims[0], mouse_rel[1] / scaled_dims[1]))

            elif event.key == K_x:
                detail = not detail

        elif event.type == MOUSEMOTION:
            if event.buttons == (1, 0, 0):
                map_pos[0] -= event.rel[0] / scaled_dims[0]
                map_pos[1] -= event.rel[1] / scaled_dims[1]

        elif event.type == MOUSEWHEEL:
            cur_scale += event.y

            if cur_scale >= len(images):
                cur_scale = len(images) - 1
            elif cur_scale < 0:
                cur_scale = 0

            scaled_image = images[cur_scale]
            old_dims = scaled_dims
            scaled_dims = scaled_image.get_size()

            map_pos = adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos)

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 5:
                cur_scale -= 1

                if cur_scale < 0:
                    cur_scale = 0

                scaled_image = images[cur_scale]
                old_dims = scaled_dims
                scaled_dims = scaled_image.get_size()

                map_pos = adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos)

            elif event.button == 4:
                cur_scale += 1

                if cur_scale >= len(images):
                    cur_scale = len(images) - 1

                scaled_image = images[cur_scale]
                old_dims = scaled_dims
                scaled_dims = scaled_image.get_size()

                map_pos = adjust_pos(SCREEN_DIMS, old_dims, scaled_dims, mouse_pos)


    SCREEN.fill((200, 200, 200))

    display_map(scaled_image, map_pos)
    draw_locations(scaled_dims, map_pos, interesting_locations)
    draw_key()

    if detail:
        display_detail()

    SCREEN.blit(overlay, (1440 - overlay.get_width(), 0))

    pygame.display.flip()
