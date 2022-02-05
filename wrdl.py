from string import ascii_uppercase
from statistics import mean
import pandas as pd
from collections import Counter
import wrdl_tools
from tqdm import tqdm


# Get all valid guesses and answers
with open("guesses.txt") as file:
    all_guesses = [line.strip() for line in file]

with open("answers.txt") as file:
    all_answers = [line.strip() for line in file]





d = {
    'guess': [],
    'greens': [],
    'yellows': [],
    'possible': []
}


for guess in tqdm(all_guesses):

    greens = []
    yellows = []
    possible = []

    for answer in all_answers:

        result = wrdl_tools.wordle(guess, answer)
        existing_info = wrdl_tools.update_information(guess, result)
        remaining = wrdl_tools.remaining_valid_answers(all_answers, existing_info)


        greens.append(result.count('G'))
        yellows.append(result.count('Y'))
        possible.append(len(remaining))


    d['guess'].append(guess)
    d['greens'].append(mean(greens))
    d['yellows'].append(mean(yellows))
    d['possible'].append(mean(possible))


    df = pd.DataFrame.from_dict(d)
    df.to_excel('first guesses.xlsx', index=False)


