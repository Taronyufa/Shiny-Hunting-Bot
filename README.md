# Shiny Hunting Bot

## Introduction

This project started with a simple goal: a full shiny living dex, from Gen 1 to Gen 7. Those are the only generations where this is actually achievable, since later generations fundamentally changed how wild Pokémon spawn in the overworld.

It's still very much a work in progress — I add things as I need them, rather than following a fixed roadmap.

Eventually, I'd like to build a website with a section dedicated to tracking my progress toward this goal.

## Requirements

Right now the bot runs on mGBA with a Fire Red ROM.

Down the line, I'd like to extend it to work with a webcam pointed at a DS, since DS games can't be captured through homebrew applications the way 3DS games can. Ideally, I'd eventually move to a 3DS with a capture card instead, since that would remove the noise a webcam introduces, but it's pricey T^T.

## Install

I use PyCharm, so I don't manage dependencies manually — it takes care of that for me. The one manual step is setting up the Telegram bot: run `telegram-send --configure` and follow the prompts.

On Linux, the gamepad library will raise a permissions-denied error unless you run `sudo chmod 666 /dev/uinput` first.

## How It Works

### Controller

Inputs are sent to the emulator through the `vgamepad` library. Since the library has no built-in way to do a fast click, I wrote my own function to emulate one.

### Screenshot

The screenshot module has two separate capture methods: one for Windows and one for Ubuntu. This is because I develop on my Windows laptop but run the bot on an Ubuntu VM hosted on a server.

### Telegram

There are two ways the bot talks back over Telegram, depending on the situation.

For simple cases — like stopping the bot when a shiny is found — there's a straightforward function built on the `telegram_send` library that just fires off a message, falling back to the default config set up during installation if none is specified.

For anything more involved, there's a separate function that pauses the main thread and hands control over to Telegram commands, letting you play the game remotely. The available commands are:

- `a` / `b`: press A / B
- `up` / `down` / `left` / `right`: directional movements
- `run`: flee the current encounter (useful for false positives)
- `screen`: send a screenshot of the game
- `resume`: stop listening for Telegram commands and let the main thread resume
- `stop`: stop the bot entirely

### Image Processing

### Image Processing

There's an important distinction between the summary check and the fight check — they work quite differently.

**Summary check.** This is the core of the shiny detection logic on the summary screen, and it works in two main steps:

1. **Locate the Pokémon.** The bot looks for the Pokémon in the screenshot and, if found, crops it as precisely as possible. Right now this only works on the summary screen in FRLG.
2. **Compare against a reference.** It computes the median color of both the cropped screenshot and the corresponding shiny sprite (sourced from [Bulbagarden Archives](https://archives.bulbagarden.net/wiki/Category:FireRed_and_LeafGreen_Shiny_sprites)), then measures the Euclidean distance between the two. If the distance exceeds a set threshold, the Pokémon is flagged as not shiny.

**Fight check.** This one works on a completely different principle. It first detects whether a battle is ongoing, and if so, takes a second screenshot timed to when the first sentence has fully appeared in the text box at the bottom. The idea is that a shiny Pokémon's star animation delays how long the text takes to fully show up. A mask is then applied to isolate the white pixels of the text, and those pixels are counted — if the count exceeds a threshold, it's flagged as shiny. Worth noting: the white pixel count can vary depending on resolution, so I'd recommend setting the threshold an order of magnitude below the typical pixel count you observe.

Since this check is time-based, it's not immune to hiccups on my end — every once in a while my computer lags for a moment and throws off the timing, which can cause a false positive. Not much I can do about that one.

### Catching Loop

I wanted this part to be as simple as possible to configure, since nailing down exact timings by hand — especially for soft-reset hunts — is a huge pain. Instead, the loop reads commands from a CSV file, where each row maps a keyword to a button or a sequence of buttons. I'll likely need to expand this list once I move on to DS games, which are a lot more complex than the GBA.

The available commands are:
- `a`: press A
- `b`: press B
- `up` / `down` / `left` / `right`: press the corresponding directional button
- `summary_n`: opens the summary menu, where `n` is the slot number of the Pokémon minus one
- `sleep_n`: pauses execution for `n` seconds
- `random_n`: pauses execution for `n` seconds plus a random extra delay between 0 and 1 second
- `reset`: performs a soft reset
- `fight_check`: checks whether a battle has started, and if so, checks whether the wild Pokémon is shiny
- `hold_b`: if it's the first command it holds B for the whole execution

For wild encounters, I'd advise sticking to only two of the four directions — ideally moving in a corner — since sometimes an input is too short for the game to register it, and the character ends up wandering off in the wrong direction.

## Future of the Bot
 
Whenever I find the time, here's what I'd like to tackle next:
 
1. Design a 3D-printable mount for my 3DS with a built-in webcam stand, so I don't have to keep repositioning it by hand.
2. Expand the set of routine commands to allow for more precise control.
3. Track more metrics about each shiny found, like how long it took to find it.
4. Improve the Telegram bot so I can check its current state and see some stats from the last shiny encounter.
5. Improve the battle-check function, since it occasionally throws false positives.
6. Turn the program into a CLI command for easier day-to-day use.
7. Create a script to download all the dependencies, ideally creating a venv.
8. Writing the ImageProcessing file on a faster language ( Either C or Rust )