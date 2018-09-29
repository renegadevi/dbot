#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from .ansi import ANSI
logger = logging.getLogger('discord')

class InterfaceDecorator:

    def __init__(self):
        self.tty_rows = 79

    def print_title(self, title):
        self.print_starline(start="\n")
        print(f"   {title.upper()}")
        self.print_starline(end="\n")

    def print_starline(self, start="", end=""):
        print(start, ANSI.fg_cyan + "*" * self.tty_rows + end + ANSI.reset)

    @staticmethod
    def print_success(string):
        print(ANSI.fg_green, '[ SUCCESS ]', ANSI.reset, string)

    @staticmethod
    def print_failed(string):
        print(ANSI.fg_red, '[ FAILED ]  ', string, ANSI.reset)

    def print_failed_subtitle(self, subtitle):
        print(f"{ANSI.fg_red}")
        print(subtitle, ANSI.reset)
        print("-"*self.tty_rows)
