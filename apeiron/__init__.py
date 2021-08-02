# coding: utf-8

__import__('os').environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from .core import trans
from .core.state import State, StateManager
from .core.context import Context, ContextBuilder

from .graphics import draw