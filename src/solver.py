import random
import numpy as np
from tqdm import tqdm

from game import Game
import words

MAX_GUESSES = 1000
class Solver():
  def __init__(self):
    pass

  def bench(self):
    nr_guesses = []
    for word in tqdm(words.CORRECT_WORDS):
      game = Game(word)
      nr_guesses.append(self.play_single_game(game))
    print(f"Mean: {np.mean(nr_guesses)}\nMedian: {np.median(nr_guesses)}")

  def play_random_game(self):
    sol = random.choice(words.CORRECT_WORDS)
    game = Game(sol)
    self.play_single_game(game)
    print(game)

  def play_single_game(self, game):
    words_left = words.ALL_WORDS
    #words_left = words.CORRECT_WORDS
    res = []
    num_guesses = 0
    t = ["GREEN" for _ in range(game.word_length)]
    while not res == t and num_guesses < MAX_GUESSES:
      word_to_guess = random.choice(words_left)
      res = game.guess(word_to_guess)


      words_left = self.get_possible_words(game, words_left)

      if game.ans not in words_left:
        self.word_uses_all_hints(game, game.ans, True)
        raise Exception("Word no longer guessable, something went wrong with the latest guess")

      num_guesses += 1
    return num_guesses

  
  def get_possible_words(self, game, word_list):
    possible_words = []
    for word in word_list:
      if self.word_uses_all_hints(game, word):
        possible_words.append(word)

    return possible_words
  
  def word_uses_all_hints(self, game, word, debug=False):
    # CHECK FOR GREENS

    # loop through all guesses that have been made in the game
    for guess_nr in range(len(game.guesses)):
      # find which positions we have a green letter for
      for letter_pos, letter_col in enumerate(game.results[guess_nr]):
        if letter_col == "GREEN":
          green_letter = game.guesses[guess_nr][letter_pos]
          # if a guess has a green letter, and the word does not use that letter
          # at that pos, return false
          if not word[letter_pos] == green_letter:
            if debug:
              print("Return false because of green")
            return False
    
    # CHECK FOR YELLOWS
    for guess_nr in range(len(game.guesses)):
      # find which positions we have a yellow letter for
      for letter_pos, letter_col in enumerate(game.results[guess_nr]):
        if letter_col == "YELLOW":
          yellow_letter = game.guesses[guess_nr][letter_pos]

          # if yellow letter not used return false
          if not yellow_letter in word:
            if debug:
              print("Return false because of yellow1")
            return False

          # if yellow letter is used as a green letter return false
          if word[letter_pos] == yellow_letter:
            if debug:
              print("Return false because of yellow2")
            return False
    
    min_occurrences = {}
    # CHECK NUM OF OCCURRENCES WE KNOW OF FOR A LETTER
    for guess_nr in range(len(game.guesses)):
      curr_occurrences = {}
      for letter_pos, letter_col in enumerate(game.results[guess_nr]):
        if letter_col == "YELLOW" or letter_col == "GREEN":
          letter = game.guesses[guess_nr][letter_pos]
          
          if letter not in curr_occurrences:
            curr_occurrences[letter] = 1
          else:
            curr_occurrences[letter] += 1

      for letter in curr_occurrences:
        if letter not in min_occurrences:
          min_occurrences[letter] = 0
          
        min_occurrences[letter] = max(min_occurrences[letter], curr_occurrences[letter])

    # CHECK FOR GRAYS
    for guess_nr in range(len(game.guesses)):
      # find which positions we have a gray letter for
      for letter_pos, letter_col in enumerate(game.results[guess_nr]):
        if letter_col == "GRAY":
          gray_letter = game.guesses[guess_nr][letter_pos]

          # if gray letter is used in word return false
          if gray_letter not in min_occurrences:
            min_occurrences[gray_letter] = 0
          if word.count(gray_letter) < min_occurrences[gray_letter]:
            if debug:
              print("Return false because of gray")
            return False

    return True



