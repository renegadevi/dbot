#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Dbot - Discord command bot
    Version 0.1

    Copyright 2016-2018 (c) Philip Andersen <philip.andersen@codeofmagi.net>
"""

# Load required modules
import sys
import logging
import asyncio
import datetime
import os
import importlib.util as imp
from collections import Counter
from core.ui import InterfaceDecorator as TUI

try:
    import toml
    import discord
    from discord.ext import commands
except ImportError as e:
    print("There was issues with loading modues.\n" +
          str(e) +
          "\nDid you try to install the required modules with "
          "`pip install -r requirements.txt`? \n"
          )
    sys.exit(1)


# Read configuration file
try:
    with open("config.toml") as config_file:
        config = toml.loads(config_file.read())
except FileNotFoundError as e:
    print("ERROR: Your config.toml cannot be found.\n" + str(e))
    sys.exit(1)
except toml.TomlDecodeError as e:
    print("ERROR: Your config.toml cannot be loaded: " + str(e))
    sys.exit(1)
for extension in config['bot']['extensions']:
    if "'" in str(extension):
        print("ERROR: Your config.toml is missing a comma")
        sys.exit(1)


# Initialize Logging
logger = logging.getLogger('discord')
if config['dev']['debug'] == 'True':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)
handler_log_file = config['logging']['filename']
handler_log = logging.FileHandler(filename=handler_log_file, mode='w')
handler_log.setFormatter(logging.Formatter(config['logging']['format']))
logger.addHandler(handler_log)
handler_term = logging.StreamHandler(sys.stdout)
handler_term.setFormatter(logging.Formatter(config['logging']['format']))
logger.addHandler(handler_term)


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.counter = Counter()
        self.uptime = datetime.datetime.now()
        self.oauth_url = config['discord']['oauth_url']
        self.prefix = config['bot']['prefix']
        super().__init__(*args, command_prefix=self.prefix, **kwargs)

    @asyncio.coroutine
    def send_cmd_help(self, ctx):
        cmd = ctx.invoked_subcommand if ctx.invoked_subcommand else ctx.command
        for page in self.formatter.format_help_for(ctx, cmd):
            yield from self.send_message(ctx.message.channel, page)


class Main():

    def __init__(self, *args, **kwargs):
        self.ui = TUI()
        self.loop = asyncio.get_event_loop()
        self.bot = Bot()
        self.load_extensions()
        self.run()

    def run(self):
        """ Run the bot """
        try:
            self.ui.print_title('Logging')
            print('DBot is now running...\n')
            running_token = config['discord']['token']
            self.loop.run_until_complete(self.bot.run(running_token))

        except KeyboardInterrupt:
            self.loop.run_until_complete(self.bot.logout())

        finally:
            self.loop.close()
            sys.exit(0)

    @staticmethod
    def input_continue(string="Do you want to continue?", kill=True):
        """ Prompt the user to being forced to answer yes/no """
        while True:
            question = input(string + " (y/n) ").lower()
            if question == 'y':
                return True
            elif question == 'n':
                return False if kill is False else sys.exit(0)
            else:
                pass

    def load_extensions(self):
        # Print information to the user
        self.ui.print_title('initializing bot extensions')

        # Prepare a list of errors
        errors = []
        try:
            # Loop each extension in the config-list
            for extension in config['bot']['extensions']:
                extension = str(extension)
                ext_path = "extensions/" + extension + '.py'

                # Importing module
                try:
                    # Load module
                    spec = imp.spec_from_file_location(extension, ext_path)
                    module = imp.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    methodToCall = getattr(module, str(extension).title())

                    # Add the functionallity to the bot
                    self.bot.add_cog(methodToCall(self.bot))

                    # Print success message
                    self.ui.print_success(extension.title())

                except FileNotFoundError as e:
                    # Print fail message
                    self.ui.print_failed(extension.title())

                    # Send the error to the logger and list of errors
                    errors.append(e)
                    logger.warning(e)

                except AttributeError as e:
                    # Print fail message
                    self.ui.print_failed(extension.title())

                    # Send the error to the logger and list of errors
                    errors.append(str(e) + " - Typo in the class name")
                    logger.warning(e)

        except ImportError as e:
            # Print fail message
            self.ui.print_failed(e)

            # Send the error to the logger and list of errors
            logger.warning(e)
            errors.append(str(e) + " - Import error")

        except KeyError as e:
            # Print fail message
            self.ui.print_failed(e)

            # Send the error to the logger and list of errors
            logger.warning(e)
            errors.append(str(e) + " - Key error of 'extensions' in TOML file")

        if errors:
            # Get total errors
            total_errors = str(len(errors))

            # Error title
            subtitle = "There was issue with " + total_errors + " extensions."
            self.ui.print_failed_subtitle(subtitle)

            # Loop trough errors
            for idx, e in enumerate(errors):
                print(str(idx+1) + ":", e)
            print("-" * self.ui.tty_rows)

            # Ask the user if they want to continue anyway
            self.input_continue()


if __name__ == '__main__':
    Main()
