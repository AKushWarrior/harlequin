import praw
import discord
import time
from random import randint
import io
import aiohttp

client = discord.Client()


reddit = praw.Reddit(client_id= 'p1txnzMS8WzQMg',
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

used = []

working = False

@client.event
async def on_ready():
    print('Harlequin is booted up and providing memes...')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$boot'):
        global working
        working = True
        while working:
            memeurl = fetchmeme().url
            async with aiohttp.ClientSession() as session:
                async with session.get(memeurl) as resp:
                    if resp.status != 200:
                        return await message.channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, 'meme.png'))
            time.sleep(300)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$shut'):
        global working
        working = False


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


client.run('NjI0NDE1Nzg5MTA1MjgzMDgy.XYQq4Q.Vn92tsvgdc1jOivX190yO1z8_cs')
