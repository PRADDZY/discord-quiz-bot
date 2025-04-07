# 🧠 Discord Quiz Bot

A feature-rich, interactive Discord Quiz Bot built with Python!  
Supports image/audio-based questions, multiple levels, MongoDB scoring, dynamic buttons, and real-time result tracking.  
Perfect for educational servers, community games, and more.

---

## 📸 Preview

> 🧠 Sends a question with a timer and optional media  
> 🏆 Tracks scores and displays a leaderboard  
> 🎯 Buttons for quick interaction  
> 🎧 Supports audio/image questions in Level 2 & 3

---

## 🚀 Features

- 🎮 Multi-level quiz system (Level 1, 2, and 3)
- ⏱️ Question timer with live countdown
- 📂 File support: 
  - Level 1: Text-only
  - Level 2: Audio (MP3)
  - Level 3: Images (PNG/JPEG)
- 🔘 Interactive multiple-choice buttons
- 🏆 MongoDB-based scoring and leaderboard
- 📊 Auto-generated result graphs using `matplotlib`
- 🔐 Restricted quiz control to authorized roles
- ⚙️ Easy to host 

---

## 🧩 Setup Guide

### 1. Clone the Repo
```bash
git clone https://github.com/PRADDZY/discord-quiz-bot.git
cd discord-quiz-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Required Python Libraries
- `discord.py`
- `motor`
- `matplotlib`
- `asyncio`
- `pymongo`

Install with:
```bash
pip install discord.py motor matplotlib
```
### 4. Set up your folders:
   - Place audio files in the `audio/` folder.
   - Place image files in the `image/` folder.
   - Ensure filenames match the question number (e.g., `1.mp3`, `1.png`).
### 5. **Replace your bot token**:
   - Open `bot.py`
   - Replace `'YOUR_BOT_TOKEN'` with your actual Discord bot token:
     ```python
     bot.run('your-actual-token-here')
     ```
### 6. Run the bot:
   ```bash
   python3 bot.py
   ```

---

---

## 🧠 Example JSON Format

### `level1_questions.json`
```json
[
  {
    "question": "What is the capital of India?",
    "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
    "answer": "New Delhi"
  }
]
```

### `level2_questions.json`
```json
[
  {
    "question": "Identify this sound:",
    "options": ["Train", "Airplane", "Car", "Ship"],
    "answer": "Train",
    "file": "1.mp3"
  }
]
```

### `level3_questions.json`
```json
[
  {
    "question": "Which monument is shown in this image?",
    "options": ["Taj Mahal", "Qutub Minar", "Red Fort", "Gateway of India"],
    "answer": "Taj Mahal",
    "file": "1.png"
  }
]
```

---

## 🛠 Commands

| Command        | Description                      |
|----------------|----------------------------------|
| `!startlevel 1`| Start Level 1 quiz              |
| `!startlevel 2`| Start Level 2 quiz (audio)      |
| `!startlevel 3`| Start Level 3 quiz (image)      |
| `!ping`        | Check if bot is alive           |

---

## 👤 Role Restriction

Only users with the specified role ID can run quiz commands.

Set your role ID here:
```python
AUTHORIZED_ROLE_ID = 123456789012345678
```

---

## 🖼️ Result Graph

- After every level, a bar graph of user scores is generated and shared in the channel.
- Saves graph with timestamp automatically.

---

## 👨‍💻 Author

Made with ❤️ by **PRADDZY**  
Feel free to fork, modify, and contribute!

---

## 📄 License

This project is open-source under the MIT License.
