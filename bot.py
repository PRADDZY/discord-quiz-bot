import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction
from discord.ui import Button, View
import asyncio
import motor.motor_asyncio
import matplotlib.pyplot as plt
import datetime
import json
import time
import os

# JSON
try:
    with open('level1_questions.json', 'r') as file:
        level1_questions = json.load(file)
    with open('level2_questions.json', 'r') as file:
        level2_questions = json.load(file)
    with open('level3_questions.json', 'r') as file:
        level3_questions = json.load(file)
except json.JSONDecodeError as e:
    print(f"Error loading JSON files: {e}")
    level1_questions, level2_questions, level3_questions = [], [], []

# Mongodb
mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017") # REPLACE!!
db = mongo_client["quiz_bot"]
user_scores = db["user_scores"]


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

AUTHORIZED_ROLE_ID = 1279085011944865813  # REPLACE!!

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


async def update_score(user: discord.User, points: int):
    await user_scores.update_one({"username": user.name}, {"$inc": {"points": points}}, upsert=True)

def plot_scores(data):
    usernames = [item['username'] for item in data]
    scores = [item['points'] for item in data]
    plt.bar(usernames, scores, color='skyblue')
    for i, v in enumerate(scores):
        plt.text(i, v + 0.5, str(v), ha='center')
    plt.xlabel('Users')
    plt.ylabel('Points')
    plt.title('Quiz Points')
    plt.xticks(rotation=45)
    plt.tight_layout()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'scores_{timestamp}.png'
    plt.savefig(filename)
    plt.close()
    return filename

async def show_graph(ctx):
    await ctx.send("The results are in! 🎉 Let’s see how everyone did... generating graph...")
    data = await user_scores.find().to_list(length=100)
    filename = plot_scores(data)
    await ctx.send(file=discord.File(filename))

def is_authorized():
    async def predicate(ctx):
        return any(role.id == AUTHORIZED_ROLE_ID for role in ctx.author.roles)
    return commands.check(predicate)

@bot.command()
@is_authorized()
async def startlevel(ctx, level: int):
    if level == 1:
        questions = level1_questions
        duration = 10
    elif level == 2:
        questions = level2_questions
        duration = 15
    elif level == 3:
        questions = level3_questions
        duration = 20
    else:
        await ctx.send("Invalid level. Choose 1, 2, or 3.")
        return

    await ctx.send(f"Starting Level {level}!")
    for idx, q in enumerate(questions):
        await ask_question(ctx, level, q, duration)
        if idx != len(questions) - 1:
            await countdown(ctx, 15)
    await show_graph(ctx)

async def ask_question(ctx, level, q, duration):
    view = View(timeout=duration)
    correct_answer = q['answer']
    answered_users = {}
    correct_users = []

    button_styles = [ButtonStyle.primary, ButtonStyle.success, ButtonStyle.danger, ButtonStyle.secondary]
    start_time = time.time()

   
    file_to_send = None
    if level == 2 and 'audio' in q and q['audio']:
        file_path = q['audio']
        print(f"DEBUG: Level 2 question - checking audio file at: {file_path}")
        if os.path.exists(file_path):
            print("DEBUG: Audio file found.")
            file_to_send = discord.File(file_path)
        else:
            print("DEBUG: Audio file not found!")
    elif level == 3 and 'image' in q and q['image']:
        file_path = q['image']
        print(f"DEBUG: Level 3 question - checking image file at: {file_path}")
        if os.path.exists(file_path):
            print("DEBUG: Image file found.")
            file_to_send = discord.File(file_path)
        else:
            print("DEBUG: Image file not found!")

    for i, option in enumerate(q['options']):
        button = Button(label=option, style=button_styles[i % len(button_styles)])
        async def button_callback(interaction: Interaction, option=option):
            if interaction.user.id in answered_users:
                await interaction.response.send_message("You have already answered!", ephemeral=True)
                return
            answer_time = round(time.time() - start_time, 2)
            answered_users[interaction.user.id] = (interaction.user.name, option, answer_time)
            await interaction.response.send_message(f"Answer recorded! You answered in {answer_time} seconds.", ephemeral=True)
        button.callback = button_callback
        view.add_item(button)

    content = q['question'] + f"\n\nYou have <t:{int(start_time) + duration}:R> to answer."
    if file_to_send:
        print("DEBUG: Sending message with attached file.")
        message = await ctx.send(content, file=file_to_send, view=view)
    else:
        print("DEBUG: Sending message without attached file.")
        message = await ctx.send(content, view=view)

    await asyncio.sleep(duration)
    for item in view.children:
        item.disabled = True
    await message.edit(view=view)

    sorted_answers = sorted(
        [(uid, data) for uid, data in answered_users.items() if data[1] == correct_answer],
        key=lambda x: x[1][2]
    )

    points = 10
    result_embed = discord.Embed(title="Results", color=discord.Color.blue())
    for user_id, (username, answer, answer_time) in sorted_answers:
        user = await bot.fetch_user(user_id)
        await update_score(user, points)
        result_embed.add_field(name=username, value=f"Answered in {answer_time}s | +{points} points", inline=False)
        points = max(points - 1, 1)
        correct_users.append(username)

    incorrect_users = [name for user_id, (name, answer, _) in answered_users.items() if answer != correct_answer]

    if correct_users:
        result_embed.add_field(name="Correct Answers", value=", ".join(correct_users), inline=False)
    if incorrect_users:
        result_embed.add_field(name="Incorrect Answers", value=", ".join(incorrect_users), inline=False)

    await ctx.send(embed=result_embed)

async def countdown(ctx, duration):
    end_time = int(time.time()) + duration
    await ctx.send(f"NEXT QUESTION IN <t:{end_time}:R>")
    await asyncio.sleep(duration)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run('your-actual-token-here') #REPLACE!!
