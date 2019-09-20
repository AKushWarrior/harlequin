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
    for submission in subreddit.top('day', limit=30):
        if not (submission.stickied or submission in used):
            used.append(submission)
            return submission
    for submission in reddit.subreddit("MemeEconomy").top('day', limit=30):
        if not (submission.stickied or submission in used):
            used.append(submission)
            return submission


used = []
working = False
client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command(pass_context=True)
async def boot(ctx):
    global working
    working = True
    await ctx.send("Memes will send every minute...")
    while True:
        memeurl = fetchmeme().url
        async with aiohttp.ClientSession() as session:
            async with session.get(memeurl) as resp:
                if resp.status != 200:
                    await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                try:
                    await ctx.send(file=discord.File(data, 'meme.png'))
                except discord.errors.HTTPException:
                    await ctx.send("File too large to send...")
        time.sleep(60)

client.run('NjI0NDE1Nzg5MTA1MjgzMDgy.XYVf8g.6k29MjCDVMKOonKFunCelucEGLU')
