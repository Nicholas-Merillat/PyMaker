import pygame, math, numpy, sys, ctypes, pygame_gui, os, ast, json

# User settings
WINDOW_RESOLUTION = (1280, 720)
MAX_FPS = 150 # If 0, framerate is uncapped
VSYNC = True

# ENGINE SETTINGS BELOW DO NOT EDIT!

# Game settings
VIEWPORT_RESOLUTION = (640, 360) # 960, 540
ASPECT_SCALE_FACTOR = VIEWPORT_RESOLUTION[0] / VIEWPORT_RESOLUTION[1]
PHYSICS_FPS = 60

# Tilemap settings
TILE_SIZE = 16
TILEMAP_SIZE = (200, 75)

# Math functions for stuff

def easeInQuad(t):
    return t * t

def easeOutQuad(t):
    return -t * (t - 2)