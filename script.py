import praw
import discord
from discord.ext import commands
import time
from random import randint
import io
import aiohttp


reddit = praw.Reddit(client_id='p1txnzMS8WzQMg',
                     client_secret='I4eujCIMd_qxTKEaTLlP15eVxPw',
                     user_agent='Harlequin for Discord v1.0.0')

memeReddits = [
    'memes',
    'dankmemes',
    'MemeEconomy',
    'HistoryMemes',
    'meme',
    'dank_meme'
]


def fetchmeme():
    global used
    subreddit = reddit.subreddit(memeReddits[randint(0,len(memeReddits)-1)])
    for submission in subreddit.top(limit=20):
        if not (submission.stickied or submission in used):
            used.append(submission)
            return submission
    for submission in reddit.subreddit("MemeEconomy").top(limit=30):
        if not (submission.stickied or submission in used):
            used.append(submission)
            return submission


used = []
working = False
client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print('Harlequin is booted up and providing memes...')


@client.command(pass_context=True)
async def boot(ctx):
    global working
    working = True
    await ctx.send("Memes will send every 5 minutes...")
    while working:
        memeurl = fetchmeme().url
        async with aiohttp.ClientSession() as session:
            async with session.get(memeurl) as resp:
                if resp.status != 200:
                    await ctx.message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'meme.png'))
        time.sleep(300)


@client.command(pass_context=True)
async def shut(ctx):
    global working
    working = False
    await ctx.send("Memes will no longer send...")
    return

while True:
    client.run('NjI0NDE1Nzg5MTA1MjgzMDgy.XYQz0A.lyomi3gHRyrlnJIneclXjfaLvfA')
