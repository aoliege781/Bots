# Lexico Bot


This telegram bot is a great way to increase your vocabulary while playing!



## Discription

The game is designed for two people (in the future I plan to increase the number of players) HOST and GUEST.

To **start** the game, you should message bot with '/start'.

After that, you will be prompted to **create** a room, or **enter** an existing one.

If you choose **"Create" (Создать комнату)**, then you automatically become a **HOST**.
If you choose **"Enter the room" (Войти в комнату)**, then you automatically become a **GUEST**.

After room is created and **GUEST** entered it, **HOST** will be asked to choose five topics for the game.
Total topics - 52.

After that the **game starts**. The bot sends a word to the player, reads the translation, and then sends
next word to another player. So until the words run out. At the end of the game, players will
be sent messages with correct and incorrect answers.

## How does it work?

We have a few files and few folders here. All of them are necessary. Let's start with the modules used.

### Modules

- telebot
- random
- string
- os
- main - main.py file
- cfg - cfg.py file not necessary, you can paste your **TOKEN** right in *"bot = telebot.TeleBot()"*. 

### Folders

#### Rooms

The Rooms folder is containing folders named with codes of rooms. Then user press **"Create" (Создать комнату)**
a folder named **XXXXX** (room) is created.\
**Room** contains two files **pl1.txt** and **pl2.txt**. Both are for storing information about the player, such as:
- player id, player status (0 or 1)
- current words (**eng*rus**) - the word the player must guess
- done words - words that the player guessed correctly
- undone words - words that the player guessed incorrectly

#### Themes

The Themes folder is containing *.txt files. Each file contains words related to a specific theme. Except 'темы.txt' file which contains all the themes. 

### Files

#### log.txt

This file is for collecting info about players. If player press **"Create" (Создать комнату)** button - then **"id\*room name\*HOST"** line will be written. If player press **"Enter the room" (Войти в комнату)** button - then **"id\*room name\*GUEST"** line will be written.

#### main.py

This file contains functions for creating, reading, rewriting and changing files.

#### table.py

Basically it's a bot. All ways of interacting with the user are registered here. **To start the bot, you should start this file.**
