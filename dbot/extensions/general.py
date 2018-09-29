#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
import datetime
import asyncio
import logging
from discord.ext import commands
logger = logging.getLogger('discord')


class General:
    """General commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @asyncio.coroutine
    def uptime(self):
        """ Shows uptime of the bot """
        uptime = datetime.datetime.now() - self.bot.uptime
        def humanize_deltatime(delta):
            """ Humanize deltatime """

            days = delta.days
            hours, r = divmod(delta.seconds, 3600)
            minutes, sec = divmod(r, 60)

            # Check for single minutes/seconds
            if minutes == 1 and sec == 1:
                time = "{0} days, {1} hours, {2} minute and {3} second."
            elif minutes > 1 and sec == 1:
                time = '{0} days, {1} hours, {2} minutes and {3} second.'
            elif minutes == 1 and sec > 1:
                time = '{0} days, {1} hours, {2} minute and {3} seconds.'
            else:
                time = '{0} days, {1} hours, {2} minutes and {3} seconds.'

            return time.format(days, hours, minutes, sec)

        yield from self.bot.say(humanize_deltatime(uptime))


    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def userinfo(self, ctx, *, user: discord.Member=None,
                 date_format="%d %b %Y %H:%M"):
        """ Shows information about a user """

        server = ctx.message.server
        if not user:
            user = ctx.message.author

        # User status
        if user.game is None:
            game = f"Chilling in {user.status} status"
        elif user.game.url is None:
            game = f"Playing {user.game}"
        else:
            game = f"Streaming: [{user.game}]({user.game.url})"

        # Joined Discord date
        created_date = user.created_at.strftime(date_format)
        created_on = f"{created_date}"

        # Joined Server date
        joined_date = user.joined_at.strftime(date_format)
        joined_on = f"{joined_date}"

        # User
        name = " ~ ".join((str(user), user.nick)) if user.nick else str(user)

        # Roles
        roles = [x.name for x in user.roles if x.name != "@everyone"]
        key = [x.name for x in server.role_hierarchy if x.name != "@everyone"]
        total_roles = "{}: ".format(len(user.roles) - 1)
        if roles:
            roles = total_roles + ", ".join(sorted(roles, key=key.index))
        else:
            roles = "None"

        # Member ID
        member_id = sorted(server.members, key=lambda m: m.joined_at)
        member_id = member_id.index(user) + 1

        #  Add fields
        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Member ID", value=member_id)
        data.add_field(name="User ID", value=user.id)
        data.add_field(name="Roles", value=roles, inline=False)
        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        # Show the embed
        try:
            yield from self.bot.say(embed=data)
        except discord.HTTPException:
            yield from self.bot.say("No `Embed links` permission")

    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def serverinfo(self, ctx, date_format="%d %b %Y %H:%M"):
        """ Shows information about the server"""
        server = ctx.message.server

        # Server creation information
        server_created_date = server.created_at.strftime(date_format)

        # Region
        server_region = str(server.region)

        # Users
        online = [m.status for m in server.members if m.status ==
                  discord.Status.online or m.status == discord.Status.idle]
        total_online = len(online)
        total_users = len(server.members)
        server_users = f"{total_online}/{total_users}"

        # Text channels
        server_text_channels = len(
            [x for x in server.channels if x.type == discord.ChannelType.text])

        # Voice channels
        server_voice_channels = len(server.channels) - server_text_channels

        # Roles
        server_roles = len(server.roles)

        # Owner
        server_owner = str(server.owner)

        # Mods
        mods = ""
        for member in ctx.message.server.members:
            for role in member.roles:
                if str(role).lower() == "Mod" or str(role).lower() == "mod":
                    mods = mods + "".join(str(member)) + "\n"
        server_mods = ''.join(mods)

        # Verification level
        server_verification = str(server.verification_level)

        # Server ID
        server_id = str(server.id)

        # Total bots
        total_bots = len(set(filter(lambda m: m.bot, server.members)))

        #  Add fields
        data = discord.Embed(description="Server information")
        data.add_field(name="Region", value=server_region)
        data.add_field(name="Users", value=server_users)
        data.add_field(name="Text Channels", value=server_text_channels)
        data.add_field(name="Voice Channels", value=server_voice_channels)
        data.add_field(name="Roles", value=server_roles)
        data.add_field(name="Owner", value=server_owner)
        data.add_field(name='Verification Level', value=server_verification)
        data.add_field(name="Total Bots", value=str(total_bots))
        data.add_field(name="Server ID: ", value=server_id)
        data.add_field(name="Creation date", value=server_created_date)
        data.add_field(name="Mods", value=server_mods)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        # Show the embed
        try:
            yield from self.bot.say(embed=data)
        except discord.HTTPException:
            yield from self.bot.say("No `Embed links` permission")

    @commands.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def mods(self, ctx, date_format="%d %b %Y %H:%M"):
        """ Shows a list of mods """
        for member in ctx.message.server.members:
            for role in member.roles:
                if str(role).lower() == "Mod" or str(role).lower() == "mod":

                    # User status
                    if member.game is None:
                        game = f"Chilling..."
                    elif member.game.url is None:
                        game = f"Playing {member.game}"
                    else:
                        game = f"Streaming: [{member.game}]({member.game.url})"

                    # Create embed form
                    data = discord.Embed(
                        description=game, colour=member.colour)
                    data.add_field(name="Current status:",
                                   value=str(member.status).upper())

                    # Get the users avatar
                    if member.avatar_url:
                        data.set_author(name=member, url=member.avatar_url)
                        data.set_thumbnail(url=member.avatar_url)
                    else:
                        data.set_author(name=member)

                    # Show embed
                    try:
                        yield from self.bot.say(embed=data)
                    except discord.HTTPException:
                        yield from self.bot.say("No `Embed links` permission")
