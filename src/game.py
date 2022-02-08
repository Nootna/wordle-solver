import words
class Game():
  def __init__(self, word):
    self.word_length = len(word)
    self.ans = word
    self.guesses = []
    self.results = []
  
  def guess(self, word):
    if word not in words.ALL_WORDS_SET:
      raise ValueError(f"Guess {word} is not a valid word")
    
    if not len(word) == self.word_length:
      raise ValueError(f"Guess {word} it not of correct length")

    result = ["GRAY" for _ in range(self.word_length)]
    available_letters = list(self.ans)
    # check for greens:
    for i, letter in enumerate(word):
      if letter == self.ans[i] and letter in available_letters:
        result[i] = "GREEN"
        available_letters.remove(letter)

    # check for yellows:
    for i, letter in enumerate(word):
      if letter in self.ans and letter in available_letters and not result[i] == "GREEN":
        result[i] = "YELLOW"
        available_letters.remove(letter)

    self.guesses.append(word)
    self.results.append(result)
    return result
  
  def __str__(self):
    ret_str = ""
    ret_str += f"Word to guess is: {self.ans}\n"
    for i, guess in enumerate(self.guesses):
      res = self.results[i]
      tiles = ""
      for letter in res:
        if letter == "GREEN":
          tiles += "G"
        elif letter == "YELLOW":
          tiles += "Y"
        else:
          tiles += "_"
      ret_str += f"Guessed {guess}\n"
      ret_str += f"{tiles}\n"
    return ret_str[:-1]



