import discord
import asyncio
from discord.ext import commands, tasks


token = "Token Here"
delay = 1


bot = commands.Bot(command_prefix="[]", help_command=None, self_bot=True, case_insensitive=True)


@bot.event
async def on_ready():
    print("Orvix Auto Purge Ready")


def progress(channel):
    print(f"Total: {total}/{total_count} ({round((total/total_count), 2)}%)")
    print(f"{channel.recipient} {channel.recipient.id}")
    print(f"{current}/{current_count} ({round((current/current_count), 2)}%)\n")


async def purge(channel):
    global total
    global current
    global current_count
    history = await channel.history(limit=None).filter(lambda m: m.author == bot.user).flatten()
    current_count = len([message for message in history])
    for message in history:
        try:
            await message.delete()
            total += 1
            current += 1
            progress(channel)
            await asyncio.sleep(delay)
        except:
            pass
    current = 0


@tasks.loop(hours=24)
async def purge_loop():
    global channels
    channels = []
    global total
    total = 0
    global current
    current = 0
    global total_count
    total_count = 0
    await bot.wait_until_ready()
    await asyncio.sleep(1)
    for i in range(5, 0, -1):
        print(f'Starting purge in {i} seconds...')
        await asyncio.sleep(1)
    print("Getting messages...")
    with open('exclude ids.txt', 'r') as f:
        id_list = [int(line.strip()) for line in f]
    channels = [channel for channel in bot.private_channels if isinstance(channel, discord.channel.DMChannel)]
    for channel in channels:
        if channel.recipient.id not in id_list:
            total_count += len([message for message in await channel.history(limit=None).filter(lambda m: m.author == bot.user).flatten()])
    for channel in channels:
        if channel.recipient.id not in id_list:
            await purge(channel)
    print(f"Finished purging {total_count} messages in {len(channels)} DMs")


purge_loop.start()
bot.run(token, bot=False)
