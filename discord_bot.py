import os
from flask import Flask
import discord
from discord.ext import commands
from gemini_bot import GeminiBot 
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

DISCORD_KEY = os.getenv('DISCORD_KEY')

app = Flask(__name__)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents = intents)
gemini = GeminiBot()

@bot.event
async def on_ready():
    print(f'Bot已登入，名稱：{bot.user.name}，ID：{bot.user.id}')

@bot.command(name='hello', help='回應一個簡單的招呼')
async def hello(ctx):
    await ctx.send(f'你好，{ctx.author.mention}!')

@bot.command(name='bowwow', help='你想說什麼')
async def bowwow(ctx):
    user_message = ctx.message.content[len('!bowwow '):] 
    reply_text = gemini.handle_text_message("(zh-tw) {}".format(user_message))
    await ctx.send(reply_text)

@bot.command(name='photo', help='這是啥圖')
async def photo(ctx):
    user_message = ctx.message.content[len('!photo '):] 
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url
        reply_text = gemini.handle_image_message(image_url)
    else:
        reply_text = gemini.handle_text_message("(zh-tw) {}".format(user_message))
    await ctx.send(reply_text)


if __name__ == '__main__':
    bot.run(DISCORD_KEY)

    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
