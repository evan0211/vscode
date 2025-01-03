import discord
from dotenv import load_dotenv
import os

# 加載 .env 文件
load_dotenv()

# 獲取環境變量
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # 開啟消息內容權限

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content == '!ping':
        await message.channel.send('Pong!')

# 使用從 .env 文件中加載的 token
client.run(token)