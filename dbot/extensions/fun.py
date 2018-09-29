#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import asyncio
import logging
from discord.ext import commands
from random import choice
logger = logging.getLogger('discord')

class Fun:
    """ Fun commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def cointoss(self):
        """ Flip a coin """
        if choice([True, False]):
            message = "(╯°□°）╯︵ O \n \n It's heads!"
        else:
            message = "(╯°□°）╯︵ O \n \n It's tails!"
        yield from self.bot.say(message)

    @commands.command()
    @asyncio.coroutine
    def ball(self):
        """ 8Ball game

        Type !ball and it will give you a one of all 20 possible outcomes.
        """
        answers = [
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes definitely',
            'You may rely on it',
            'As I see it, yes',
            'Most likely',
            'Outlook good',
            'Yes',
            'Signs point to yes',
            'Reply hazy try again',
            'Ask again later',
            'Better not tell you now',
            'Cannot predict now',
            'Concentrate and ask again',
            "Don't count on it",
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful'
        ]
        yield from self.bot.say(choice(answers))
