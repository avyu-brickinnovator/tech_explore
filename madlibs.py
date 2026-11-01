"""
Mad Libs Generator
------------------
A beginner Python project. The player types in words,
and the program drops them into a silly story, with the
player's words in bright colors.

Concepts practiced: input(), variables, strings, lists,
dictionaries, functions, loops, and simple input checks.
"""

import hashlib
import os
import random
import time

# The longest word (or words) a player can type for one blank.
MAX_LENGTH = 20

# Besides letters, these are the only characters allowed in a word.
# They let players type things like "ice cream", "T-rex", or "Jack's".
ALLOWED_EXTRAS = " -'"


# The blocked words are saved as hashes, so nobody can read them.
# A hash turns a word into a jumble of letters and numbers that can't
# be turned back. To check a word, we hash it and look for that hash.
# This must match HASH_SALT in the script that made the file.
HASH_SALT = "madlibs-blocklist-v1:"


def hash_word(text):
    """Turn a word or phrase into a hash, the same way the list was made."""
    return hashlib.sha256((HASH_SALT + text).encode("utf-8")).hexdigest()


def load_blocked_hashes():
    """Read the hashes of words the game won't accept."""
    # The list lives in a separate file next to this one.
    try:
        folder = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Some online Python sites don't tell us where this file is,
        # so look in the current folder instead.
        folder = os.getcwd()
    path = os.path.join(folder, "blocked_words.txt")
    blocked = set()
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    blocked.add(line)
    except FileNotFoundError:
        print("(Note: blocked_words.txt is missing, so no words are blocked.)")
    return blocked


BLOCKED_HASHES = load_blocked_hashes()

# Your words show up in color. If you see weird symbols like [1;33m
# instead of colors, change this to False. Your words will show up
# like *THIS* instead.
USE_COLOR = True

# Color codes. These special codes tell the screen to change color.
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
NORMAL = "\033[0m"

# Each of your words gets the next color in this list.
COLORS = [YELLOW, CYAN, MAGENTA, GREEN, RED]

# Each story has a title, a dictionary of blanks, and a template.
# In the blanks dictionary, each key is the placeholder name and
# each value is what to ask the player.
# The placeholder names in {curly braces} must match the blank names.
STORIES = [
    {
        "title": "The Zoo Trip",
        "blanks": {
            "adj": "an adjective",
            "animal": "an animal",
            "verb_ing": "a verb ending in -ing",
            "number": "a number",
            "food": "a food (plural)",
            "exclaim": "an exclamation (like Wow or Yikes)",
        },
        "template": (
            "Yesterday our class went on a {adj} trip to the zoo. "
            "The first thing we saw was a giant {animal} {verb_ing} "
            "on top of its cage! The zookeeper fed it {number} bowls "
            "of {food}. When it finished, it shouted \"{exclaim}!\" "
            "and everyone clapped."
        ),
    },
    {
        "title": "My Robot Teacher",
        "blanks": {
            "adj": "an adjective",
            "name": "a silly name",
            "number": "a number",
            "body_part": "a body part",
            "noun_plural": "a plural noun",
            "verb_past": "a verb in past tense (like jumped)",
        },
        "template": (
            "On Monday, our teacher was replaced by a {adj} robot "
            "named {name}. It had {number} arms and a {body_part} made "
            "of shiny metal. Instead of homework, it gave everyone "
            "{noun_plural}. When the principal walked in, the robot "
            "{verb_past} right out the window!"
        ),
    },
    {
        "title": "The Worst Pizza Ever",
        "blanks": {
            "adj": "an adjective",
            "food": "a food",
            "liquid": "a liquid",
            "animal": "an animal",
            "adverb": "an adverb (ends in -ly)",
            "place": "a place",
        },
        "template": (
            "Last night I ordered the most {adj} pizza in town. "
            "It was topped with {food} and covered in {liquid} instead "
            "of cheese. When I opened the box, a tiny {animal} jumped "
            "out and ran {adverb} to the {place}. I think I'll order "
            "tacos next time."
        ),
    },
]


def has_only_letters(word):
    """Return True if the word has only letters and a few allowed extras."""
    for character in word:
        if not character.isalpha() and character not in ALLOWED_EXTRAS:
            return False
    return True


def is_blocked(word):
    """Return True if the answer has a blocked word or phrase in it."""
    # Check whole words only, so "class" or "grass" are never blocked.
    # Hyphens count as spaces, so "T-rex" is checked as "t" and "rex".
    parts = word.lower().replace("-", " ").split()

    # Check every group of words that sit next to each other, because
    # some entries are phrases. For "big red dog" we check "big",
    # "big red", "big red dog", "red", "red dog", and "dog".
    for start in range(len(parts)):
        for end in range(start + 1, len(parts) + 1):
            group = " ".join(parts[start:end])
            if hash_word(group) in BLOCKED_HASHES:
                return True

    # Also catch plurals, like "words" when "word" is on the list.
    for part in parts:
        if part.endswith("s") and hash_word(part[:-1]) in BLOCKED_HASHES:
            return True
    return False


def ask_for_word(name, description):
    """Keep asking until the player types a valid word."""
    while True:
        word = input(f"Give me {description}: ").strip()
        if word == "":
            print("  Oops, you didn't type anything. Try again!")
        elif len(word) > MAX_LENGTH:
            print(f"  That's too long! Use {MAX_LENGTH} letters or fewer.")
        elif name == "number":
            if word.isdigit():
                return word
            print("  That needs to be a number, like 7 or 42.")
        elif not has_only_letters(word):
            print("  Please use letters only, no numbers or symbols.")
        elif is_blocked(word):
            print("  Let's keep it school-friendly! Try another word.")
        else:
            return word


def choose_story():
    """Show the menu and return the story the player picks."""
    print("\nPick a story:")
    for i, story in enumerate(STORIES, start=1):
        print(f"  {i}. {story['title']}")
    print("  R. Surprise me!")

    while True:
        choice = input("Your choice: ").strip().lower()
        if choice == "r":
            return random.choice(STORIES)
        if choice.isdigit() and 1 <= int(choice) <= len(STORIES):
            return STORIES[int(choice) - 1]
        print("  Please type a story number or R.")


def highlight(word, number):
    """Make one of the player's words stand out. number picks the color."""
    if not USE_COLOR:
        return "*" + word.upper() + "*"
    color = COLORS[number % len(COLORS)]
    return color + word.upper() + NORMAL


def play_round():
    """Play one game: pick a story, collect words, show the result."""
    story = choose_story()
    print("\nFill in the blanks. No peeking at the story!\n")

    answers = {}
    number = 0
    for name in story["blanks"]:
        description = story["blanks"][name]
        word = ask_for_word(name, description)
        answers[name] = highlight(word, number)
        number += 1

    finished = story["template"].format_map(answers)

    print("\nYour story is ready...")
    for count in ["3", "2", "1"]:
        time.sleep(0.7)
        print(f"  {count}...")

    print("\n" + "=" * 60)
    print(story["title"].upper())
    print("=" * 60)
    # One sentence per line, so the story is easy to read.
    print(finished.replace(". ", ".\n").replace("! ", "!\n"))
    print("=" * 60)


def main():
    print("Welcome to MAD LIBS!")
    while True:
        play_round()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

main()