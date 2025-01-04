import discord
from discord.ext import commands
import importlib.util
from dotenv import load_dotenv
import os
import random
import platform
import asyncio

# 加載 .env 文件
load_dotenv()

# 獲取環境變數
token = os.getenv("DISCORD_TOKEN")

# 初始化 Bot 實例
intents = discord.Intents.default()
intents.message_content = True  # 開啟訊息內容權限

# 使用 commands.Bot 創建 bot 實例
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'已登入為 {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # 防止機器人自己回覆自己
    
    
    # 處理「說」命令
    if message.content.startswith('說'):
        tmp = message.content.split(" ", 2)
        if len(tmp) == 1:
            await message.channel.send("你要我說什麼啦？")
        else:
            await message.channel.send(tmp[1])
    
    elif message.content.startswith('傻逼'):
        await message.channel.send("叫我幹嘛！")

    elif message.content.startswith('打瓦'):
        await message.channel.send(" <@&1324711416652894239> 上線")
        
    # 處理 !flood 命令，模擬洗版
    elif message.content.startswith('!f'):
        # 確保指令有設定要發送的次數
        try:
            parts = message.content.split()
            if len(parts) < 3:
                await message.channel.send("請提供有效的訊息內容和發送次數！例如：`!f 訊息 10`")
                return
            elif "@" in parts[1] or int(parts[2]) >= 5:
                await message.channel.send("想幹嘛？想屁吃！")
                return
            flood_message = parts[1]  # 訊息內容
            num_messages = int(parts[2])  # 發送次數

            # 確保 flood_message 的長度為 2000 字符
            flood_message = (flood_message * (2000 // len(flood_message)))[:2000]

            for i in range(num_messages):
                # 發送修改後的訊息
                await message.channel.send(flood_message)

        except ValueError:
            await message.channel.send("請提供有效的數字作為發送次數！")
    # 確保指令處理正常運作
    await client.process_commands(message)

spec = importlib.util.spec_from_file_location("data", r"vscode\bot\data.py")  # 請確保此路徑正確
data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_module)

# 吃指令
@client.command(name="吃")
async def eat(ctx):
    random_choice = random.choice(data_module.meals)  # 隨機選擇食物
    await ctx.send(f"隨機抽選的食物是：{random_choice}")

# 喝指令
@client.command(name="喝")
async def drink(ctx):
    random_choice = random.choice(data_module.drinks)  # 隨機選擇飲品
    await ctx.send(f"隨機抽選的飲品是：{random_choice}")



@client.command(name="av")
async def recommend(ctx):
    av_data = data_module.av_data  # 從檔案中獲取字典
    
    # 隨機選擇一位女優
    actress = random.choice(list(av_data.keys()))
    
    # 隨機選擇一部作品
    work = random.choice(av_data[actress])
    
    # 發送結果
    await ctx.send(f"推薦女優：**{actress}**\n推薦作品：**{work}**")

# 使用從 .env 文件中加載的 token
client.run(token)
