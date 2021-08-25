# CUNY Tech Prep Hackathon, Team GECL’s Project: <Game Title>

This project is the fruit of Team GECL’s innovation. For the theme of CUNY Tech Prep’s 2021 hackathon, “back to in-person” we wanted to create an entertaining game related to social distancing and/or avoiding close contact. This game’s setting is a subway platform, and the objective is to avoid coming into contact with the random people milling about. There *is* a health counter, so many sure to keep it positive 😉 by keeping away from the COVID positives (the people with the green clouds hanging over their heads).

## How to Run

In order to run this game, you will need Python 3. This game also depends on [Pygame](https://www.pygame.org/), so install it first using the `pip` tool.

```
python3 -m pip install -U pygame --user
```

There are more detailed instructions on installing Pygame on [Pygame’s Getting Started page](https://www.pygame.org/wiki/GettingStarted).

But once that is set up, run the game by typing `python main.py`. Replace `main.py` with the [relative] path to the Python code.

## How to Play

So you’ve got it running? Here’s how to play:

1. The game will begin by spawning people randomly on the platform (including yourself).
2. Your objective it to keep your distance, so use the arrow keys to help your character navigate the platform.
    a. If you are touch by anyone, you lose a life.
    b. If you manage to dodge them, more will come.
3. Try to stay alive and rack up a high score. 🙂

Good luck!
