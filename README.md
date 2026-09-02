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

## How It Works

### Controller

Inputs are sent to the emulator through the `vgamepad` library. Since the library has no built-in way to do a fast click, I wrote my own function to emulate one.

### Screenshot

The screenshot module has two separate capture methods: one for Windows and one for Ubuntu. This is because I develop on my Windows laptop but run the bot on an Ubuntu VM hosted on a server.

### Telegram

A single function handles sending messages to the bot. If no config is specified, it falls back to the default one set up during installation.

### Image Processing

This is the core of the shiny detection logic, and it works in two main steps:

1. **Locate the Pokémon.** The bot looks for the Pokémon in the screenshot and, if found, crops it as precisely as possible. Right now this only works on the summary screen in FRLG — support for wild encounters is planned for later.
2. **Compare against a reference.** It computes the median color of both the cropped screenshot and the corresponding shiny sprite (sourced from [Bulbagarden Archives](https://archives.bulbagarden.net/wiki/Category:FireRed_and_LeafGreen_Shiny_sprites)), then measures the Euclidean distance between the two. If the distance exceeds a set threshold, the Pokémon is flagged as not shiny.

### Catching Loop

I wanted this part to be as simple as possible to configure, since nailing down exact timings by hand — especially for soft-reset hunts — is a huge pain. Instead, the loop reads commands from a CSV file, where each row maps a keyword to a button or a sequence of buttons. I'll likely need to expand this list once I move on to DS games, which are a lot more complex than the GBA.

## Future of the Bot
 
Whenever I find the time, here's what I'd like to tackle next:
 
1. Design a 3D-printable mount for my 3DS with a built-in webcam stand, so I don't have to keep repositioning it by hand.
2. Expand the set of routine commands to allow for more precise control.
3. Build a new crop function that works across all wild encounter dioramas — ideally one that can also tell the summary screen apart from a wild encounter, though that part could be solved in simpler ways too.
4. Track more metrics about each shiny found, like how long it took to find it.
5. Improve the Telegram bot so I can check its current state and see some stats from the last shiny encounter.
6. Still on the fence about whether the bot should attempt to catch wild Pokémon on its own — there are so many possible scenarios during a catch that I haven't settled on an approach yet.
7. And lastly, make it work for multiple istances of the game to speed things up