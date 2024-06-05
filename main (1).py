import asyncio
from typing import Text
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.exceptions import AlreadyJoinedError
from yt_dlp import YoutubeDL
from urllib.parse import parse_qs
from pyrogram import Client, filters, types
from pyrogram.errors import FloodWait
import time
import requests
import datetime
import openai
from time import sleep
import random
import hashlib
from asyncio import sleep
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types.messages_and_media import message_entity
from background import keep_alive
from pyrogram import enums
from commands import *
from pyrogram.types import Message
from importlib import reload
import os
import importlib
import sys
import numpy as np
from PIL import Image

api_id = 24679387
api_hash = "ad9e119acbfc9de527e1da32fae2a866"
openai.api_key = "sk-proj-Ms4cZzsofgpZrhzu1iIIT3BlbkFJHKtXjAC3yWmaUNgLB9kF"
nevo_api_url = "https://ai.nevolution.team/nevo?apikey=akbarrdev&prompt="

plugins = dict(root="modules")

with Client("my_account", api_id=api_id, api_hash=api_hash,
            plugins=plugins) as app:
  app.send_message("me", 'бот включен')
  print('включен')
    # Daftar user ID yang diizinkan untuk menggunakan command !exec
ALLOWED_USERS = [7271527237, 5977658793]  # Ganti dengan user ID Telegram Anda

# Variabel untuk menyimpan waktu awal bot mulai
start_time = time.time()

# Mode default
mode = 2

@app.on_message(filters.command("http", prefixes="."))
def check_url(client, message):
    if len(message.command) < 2:
        message.reply("Usage: .http <URL>")
        return

    url_to_check = message.command[1]
    api_url = f"https://check-host.cc/?m=HTTP&target={url_to_check}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.text

        # Parsing the response
        lines = data.split('\n')
        results = []

        for line in lines:
            if line.startswith("🇷🇺") or line.startswith("🇦🇪") or line.startswith("🇹🇼") or line.startswith("🇳🇿") or line.startswith("🇩🇪") or line.startswith("🇹🇭") or line.startswith("🇳🇱") or line.startswith("🇮🇹") or line.startswith("🇫🇮") or line.startswith("🇦🇹"):
                results.append(line)
            elif "Check Online" in line or "Full Report" in line:
                results.append(line)

        if results:
            result_message = "```\n" + "\n".join(results) + "\n```"
            message.reply(result_message, parse_mode="markdown")
        else:
            message.reply("No results found.")
    except requests.exceptions.RequestException as e:
        message.reply(f"An error occurred: {e}")


# Daftar untuk menyimpan lagu yang akan dimainkan
playlist = []

# Fungsi untuk mengunduh audio dari YouTube
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
    return filename

# Command untuk memainkan lagu
@app.on_message(filters.command("play", prefixes="."))
async def play(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("❗ Mohon sertakan judul atau URL YouTube setelah perintah `.play`.")
        return
    
    query = message.text.split(None, 1)[1]
    await message.reply("🔍 Sedang mencari lagu...")
    
    ydl_opts = {'default_search': 'ytsearch', 'quiet': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)['entries'][0]
        url = info['webpage_url']
        title = info['title']
    
    filename = download_audio(url)
    playlist.append(filename)
    
    if len(playlist) == 1:
        chat_id = message.chat.id
        try:
            await pytgcalls.join_group_call(chat_id, InputAudioStream(filename))
        except AlreadyJoinedError:
            await pytgcalls.change_stream(chat_id, InputAudioStream(filename))
    
    await message.reply(f'🎵 Sedang memutar: **{title}**')

# Command untuk melewati lagu
@app.on_message(filters.command("skip", prefixes="."))
async def skip(client: Client, message: Message):
    if playlist:
        skipped_song = playlist.pop(0)
        if playlist:
            chat_id = message.chat.id
            await pytgcalls.change_stream(chat_id, InputAudioStream(playlist[0]))
            await message.reply('⏭ Lagu telah dilewati, memutar lagu berikutnya.')
            if os.path.exists(skipped_song):
                os.remove(skipped_song)
        else:
            await pytgcalls.leave_group_call(message.chat.id)
            await message.reply('⏹ Tidak ada lagi lagu dalam daftar putar.')
    else:
        await message.reply('⚠ Tidak ada lagu yang sedang diputar.')

# Command untuk mengakhiri VC
@app.on_message(filters.command("end", prefixes="."))
async def end(client: Client, message: Message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    playlist.clear()
    await message.reply('🔚 Voice chat telah diakhiri dan daftar putar dikosongkan.')

# Menangani peristiwa ketika aliran berakhi
            


# Daftar bendera dengan detail negara
flags = {
    "🇮🇩": "Indonesia",
    "🇺🇸": "Amerika Serikat",
    "🇯🇵": "Jepang",
    "🇫🇷": "Perancis",
    "🇧🇷": "Brasil",
    "🇬🇧": "Inggris",
    "🇨🇦": "Kanada",
    "🇮🇹": "Italia",
    "🇩🇪": "Jerman",
    "🇦🇺": "Australia",
    "🇪🇸": "Spanyol",
    "🇨🇳": "Cina",
    "🇷🇺": "Rusia",
    "🇰🇷": "Korea Selatan",
    "🇸🇦": "Arab Saudi",
    "🇲🇽": "Meksiko",
    "🇳🇱": "Belanda",
    "🇨🇭": "Swiss",
    "🇦🇷": "Argentina",
    "🇿🇦": "Afrika Selatan",
    "🇳🇴": "Norwegia",
    "🇸🇪": "Swedia",
    "🇮🇳": "India",
    "🇧🇪": "Belgia",
    "🇪🇬": "Mesir",
    "🇹🇷": "Turki",
    "🇵🇹": "Portugal",
    "🇮🇱": "Israel",
    "🇳🇬": "Nigeria",
    "🇦🇪": "Uni Emirat Arab",
    # Tambahkan lebih banyak bendera dan negara di sini jika diperlukan
}

@app.on_inline_query()
async def inline_tebak_bendera(client, inline_query):
    bendera, negara = random.choice(list(flags.items()))

    # Create a unique ID using hashlib
    result_id = hashlib.md5(bendera.encode()).hexdigest()

    # Generate an inline keyboard with the options for the user to guess
    options = list(flags.values())
    random.shuffle(options)

    keyboard = [[InlineKeyboardButton(option, callback_data=f"guess_{option}")] for option in options]

    results = [
        InlineQueryResultArticle(
            id=result_id,
            title="Tebak Bendera",
            input_message_content=InputTextMessageContent(f"Tebak bendera ini: {bendera}\nPilih jawabanmu dari tombol di bawah!"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            description="Klik untuk bermain tebak bendera",
        )
    ]

    await client.answer_inline_query(inline_query.id, results, cache_time=0)

@app.on_message(filters.command("tebakbendera"))
async def command_tebak_bendera(client, message):
    bendera, negara = random.choice(list(flags.items()))

    options = list(flags.values())
    random.shuffle(options)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(option, callback_data=f"guess_{option}")] for option in options]
    )

    await message.reply(
        f"Tebak bendera ini: {bendera}\nPilih jawabanmu dari tombol di bawah!",
        reply_markup=keyboard
    )

@app.on_callback_query()
async def handle_guess(client, callback_query):
    guess = callback_query.data.split("_")[1]
    correct_flag = next((flag for flag, country in flags.items() if country == guess), None)

    if correct_flag:
        await callback_query.answer(f"Selamat! Jawabanmu benar. Bendera ini adalah {guess}.", show_alert=True)
    else:
        await callback_query.answer("Jawaban salah. Coba lagi!", show_alert=True)


games = {}

def get_board_markup(board):
    buttons = []
    for row in range(3):
        button_row = []
        for col in range(3):
            button_text = board[row][col]
            button_data = f"{row}{col}"
            button_row.append(InlineKeyboardButton(button_text, callback_data=button_data))
        buttons.append(button_row)
    return InlineKeyboardMarkup(buttons)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

def is_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

@app.on_message(filters.command("tictactoe", prefixes="."))
async def start_tictactoe(client, message):
    chat_id = message.chat.id
    games[chat_id] = {
        "board": [[" " for _ in range(3)] for _ in range(3)],
        "turn": "X"
    }
    await message.reply("Tic-Tac-Toe game started!\nPlayer X's turn.", reply_markup=get_board_markup(games[chat_id]["board"]))

@app.on_callback_query()
async def handle_turn(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in games:
        await callback_query.answer("No game in progress.", show_alert=True)
        return

    game = games[chat_id]
    board = game["board"]
    turn = game["turn"]

    row, col = int(callback_query.data[0]), int(callback_query.data[1])

    if board[row][col] != " ":
        await callback_query.answer("Invalid move! Cell already taken.", show_alert=True)
        return

    board[row][col] = turn
    winner = check_winner(board)
    if winner:
        await callback_query.message.edit_text(f"Player {winner} wins!", reply_markup=get_board_markup(board))
        del games[chat_id]
    elif is_full(board):
        await callback_query.message.edit_text("It's a draw!", reply_markup=get_board_markup(board))
        del games[chat_id]
    else:
        game["turn"] = "O" if turn == "X" else "X"
        await callback_query.message.edit_text(f"Player {game['turn']}'s turn.", reply_markup=get_board_markup(board))

    await callback_query.answer()

def is_allowed(user_id):
    return user_id in ALLOWED_USERS

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(client, message):
    if not is_allowed(message.from_user.id):
        await message.reply_text("You are not authorized to use this command.")
        return

    start = time.time()
    msg = await message.reply_text("Pong!")
    end = time.time()
    await msg.edit_text(f"Pong! {round((end - start) * 1000)}ms")

# Fungsi untuk memanggil API Nevolution
def get_ai_response(prompt):
    url = "https://ai.nevolution.team/nevo"
    params = {
        "apikey": "akbarrdev",
        "prompt": prompt
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("response")
    else:
        return "Terjadi kesalahan saat memproses permintaan."

# Handler untuk command .ai
@app.on_message(filters.command("ai", prefixes="."))
def handle_ai_command(client, message):
    if len(message.command) < 2:
        message.reply_text("Silakan masukkan prompt setelah command .ai")
        return
    prompt = " ".join(message.command[1:])
    response = get_ai_response(prompt)
    message.reply_text(response)
    
@app.on_message(filters.command("alive", prefixes=".") & filters.me)
async def alive(client, message):
    if not is_allowed(message.from_user.id):
        await message.reply_text("You are not authorized to use this command.")
        return

    uptime = time.time() - start_time
    uptime_str = str(datetime.timedelta(seconds=int(uptime)))
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    await message.reply_text(f"Bot has been running for: {uptime_str}\nStarted at: {start_time_str}")

@app.on_message(filters.command("mode", prefixes=".") & filters.group & filters.me)
async def set_mode(client, message):
    if not is_allowed(message.from_user.id):
        await message.reply_text("You are not authorized to use this command.")
        return

    try:
        new_mode = int(message.text.split(" ", 1)[1])
        global mode

        if new_mode in [1, 2]:
            mode = new_mode
            if mode == 1:
                await client.set_chat_description(message.chat.id, "ISeven playing a game!")
            else:
                await client.set_chat_description(message.chat.id, "")
            await message.reply_text(f"Mode has been set to: {mode}")
        else:
            await message.reply_text("Invalid mode! Please choose between 1 and 2.")
    except (IndexError, ValueError):
        await message.reply_text("Invalid mode! Please choose between 1 and 2.")


@app.on_message(filters.command("exec", prefixes="."))
async def exec_shell_command(client, message):
    # Memeriksa apakah user ID pengirim ada dalam daftar yang diizinkan
    if message.from_user.id not in ALLOWED_USERS:
        await message.reply_text("You are not authorized to use this command.")
        return

    try:
        # Mendapatkan perintah dari pesan (menghilangkan prefix dan command)
        command = message.text.split(" ", 1)[1]

        # Menjalankan perintah shell
        result = os.popen(command).read()

        # Mengirimkan hasil eksekusi kembali ke chat dengan Markdown
        await message.reply_text(f"**Command:**\n```\n{command}\n```\n\n**Result:**\n```\n{result}\n```")
    except IndexError:
        await message.reply_text("Please provide a command to execute.")
    except Exception as e:
        await message.reply_text(f"An error occurred: ```\n{e}\n```")

@app.on_message(filters.command('run', prefixes=['.', '/', '!']) & filters.me)
def run(client, message):
  expression = message.text.split(None, 1)[1]
  try:
    result = eval(expression)
  except Exception as e:
    message.reply_text(f"Ошибка выполнения:\n{e}")


def rgb_to_hex(r, g, b):
  hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
  return hex_color


@app.on_message(filters.command('colorhex') & filters.me)
async def colorhex(_, msg):
  r = random.randint(0, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  width, height = 256, 256
  colorHex = rgb_to_hex(r, g, b)
  color = r, g, b
  color_image = Image.new('RGB', (width, height), color)
  color_image.save('color_image.jpg')
  await app.send_photo(msg.chat.id,
                       'color_image.jpg',
                       caption=f'<code>{colorHex}</code>')


@app.on_message(filters.command('color') & filters.me)
async def color(_, msg):
  r = random.randint(0, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  width, height = 256, 256
  color = r, g, b
  color_image = Image.new('RGB', (width, height), color)
  color_image.save('color_image.jpg')
  await app.send_photo(msg.chat.id,
                       'color_image.jpg',
                       caption=f'<code>{r}, {g}, {b}</code>')
  os.remove('color_image.jpg')
  print(generate_hex_color())


@app.on_message(filters.command('random_member', prefixes=['/', '.']))
async def rand(_, message):
  сhat_members = app.get_chat_members(message.chat.id)
  random_user = сhat_members.random()
  print(f'Имя пользователя: {random_user.user.first_name}')
  print(f'ID пользователя: {random_user.user.id}')


@app.on_message(filters.command("t1", ".") & filters.me)
async def type1(_, msg):
    orig_text = msg.text.split(".t1 ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "▒"

    while(tbp != orig_text):
        try:
            await msg.edit(tbp + typing_symbol)
            await sleep(0.05)

            tbp = tbp + text[0]
            text = text[1:]

            await msg.edit(tbp)
            await sleep(0.05)
            
        except FloodWait as e:
             await sleep(e.x)
            
@app.on_message(filters.command("t2", prefixes=".") & filters.me)
async def type2(_, msg):
    orig_text = msg.text.split(".t2 ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "❤️"

    while(tbp != orig_text):
        try:
            await msg.edit(tbp + typing_symbol)
            await sleep(0.05)

            tbp = tbp + text[0]
            text = text[1:]

            await msg.edit(tbp)
            await sleep(0.05)
            
        except FloodWait as e: 
            await sleep(e.x)

keep_alive()

app.run()
