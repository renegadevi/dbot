#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('discord')

class ANSI:
    """ Some basic ANSI colors for terminal output """

    reset = '\033[0m'
    bold = '\033[1m'

    fg_black = '\033[0;30m'
    fg_boldblack = '\033[1;30m'

    fg_red = '\033[0;31m'
    fg_boldred = '\033[1;31m'

    fg_green = '\033[0;32m'
    fg_boldgreen = '\033[1;32m'

    fg_brown = '\033[0;33m'
    fg_boldbrown = '\033[1;33m'

    fg_blue = '\033[0;34m'
    fg_boldblue = '\033[1;34m'

    fg_purple = '\033[0;35m'
    fg_boldpurple = '\033[1;35m'

    fg_cyan = '\033[0;36m'
    fg_boldcyan = '\033[1;36m'

    fg_white = '\033[0;37m'
    fg_boldwhite = '\033[1;37m'
