# Monopoly Go! Bot

This thing plays the mobile game "Monopoly Go!" non-stop by clicking on the Bluestacks window. It restarts itself every once in a while (to avoid getting stuck, if it ever does), and sends screenshots to a Discord webhook so that you can know what went wrong if it gets stuck.

## Instructions

1) Install Python 3.10 or higher
2) Edit the first few lines of main.py in order to specificy your webhook url (you can leave it blank) and the restart internal.
3) Lunch `run.cmd`

## TODO

### IMPORTANT
- Automate mini-games (such as the one with the balls, or the sweeper, etc)

### USEFUL
- Use locateAllOnScreen to find all heist vaults and click them all faster
- Improve building destruction coordinates range (make it more accurate)


## Good to know (if you wanna maintain) 

- the free gift is available every 8 hours
- If for whatever using a click on close_*.png doesn't work anymore, sending the "ESC" key signal works to close menus/ads

## THANKS TO

### These repos that I got inspiration from:
- https://github.com/lewisgibson/monopoly-go-bot
- https://github.com/mohammadafshar06/monopoly-go-bot
- https://github.com/ethanriverpage/monopolygobot

#### SweeZ cuz he my bro fr 🥺
