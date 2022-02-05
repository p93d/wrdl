


def wordle(guess, answer):

    out = ['_', '_', '_', '_', '_']

    remaining_answer_letters = []
    remaining_guess_indices = []


    for i in range(5):

        if guess[i] == answer[i]:
            out[i] = 'G'
        else:
            remaining_answer_letters.append(answer[i])
            remaining_guess_indices.append(i)


    for i in remaining_guess_indices:

        if guess[i] in remaining_answer_letters:

            out[i] = 'Y'
            remaining_answer_letters.remove(guess[i])

    return out
        

"""
logic for determining what the guess and subsequent
tells us

We want to know any KNOWN letters, then any letters
that we know are IN the word and their possible locations

Then we want to be able to exclude letters from various
positions in the word
"""
def update_information(guess, result, existing_info={}):

    # Initialize the information dict if this is the
    # first guess
    if len(existing_info) == 0:
        existing_info = {
            'known': ['', '', '', '', ''],
            'missing': {},
            'exclude': [[], [], [], [], []]
        }



    # list of indices where we don't know the letter
    unknown_indices = [x for x in range(5)]
    
    

    # Check for greens.  If it's green, mark it as known,
    # and remove that from unknowns
    for i in range(5):

        if result[i] == "G":
            existing_info['known'][i] = guess[i]
            unknown_indices.remove(i)


    excluded_letters = []

    for i in range(5):

        if result[i] == "_":
            if guess[i] not in excluded_letters:
                excluded_letters.append(guess[i])
            

    # Then check the yellows and blanks
    for i in range(5):

        # YELLOWS:
        # If it's not in the existing list of known missing
        # letters, then add it.  Since we know it isn't in
        # THIS position, we can remove current index from 
        # possible locations, and we can add it to the list
        # of excluded letters for that position
        if result[i] == 'Y':

            if guess[i] not in existing_info['missing']:

                existing_info['missing'][guess[i]] = unknown_indices.copy()
                

            if i in existing_info['missing'][guess[i]]:
    
                existing_info['missing'][guess[i]].remove(i)


            if guess[i] not in existing_info['exclude'][i]:

                existing_info['exclude'][i].append(guess[i])


        # BLACKS:
        # If this letter is in the list of missing letters
        # it still could be in the word, so we just remove
        # the current index from the list of possibilities
        # Then we add this letter to the list of 
        elif result[i] == "_":

            if guess[i] in existing_info['missing']:

                if i in existing_info['missing'][guess[i]]:
                    existing_info['missing'][guess[i]].remove(i)

            else:
                for j in range(5):

                    existing_info['exclude'][j].append(guess[i])

            existing_info['exclude'][i].extend(excluded_letters)

    for x in range(5):

        existing_info['exclude'][x] = list(set(existing_info['exclude'][x]))

    
    # Check for greens.  If it's green, mark it as known,
    # and remove that from unknowns
    for i in range(5):

        if result[i] == "G":
            existing_info['missing'][guess[i]] = [i]
            
    
    return existing_info



def check_index_for_letter(word, letter, indices):

    if len(indices) == 0: return False

    for letter in indices:

        for i in indices[letter]:

            if word[i] == letter:
                return True
        else:
            return False





def check_for_excluded_letters(word, indices):

    for i in range(5):

        if word[i] in indices[i]:

            return False
    
    else:
        return True



    
def check_for_known_letters(word, known):

    for i in range(5):

        if known[i] != '':

            if word[i] != known[i]:

                return False
    else:

        return True


def check_for_missing_letters(word, missing):

    for ltr in missing:

        if word.find(ltr) not in missing[ltr]:
            return False
    
    else:
        return True





def remaining_valid_answers(answers, existing_info):

    possible_words = answers.copy()


    possible_words[:] = [wrd for wrd in possible_words if check_for_missing_letters(
            wrd, existing_info['missing']
            )]


    possible_words[:] = [wrd for wrd in possible_words if check_for_excluded_letters(
            wrd, existing_info['exclude']
    )]


    possible_words[:] = [wrd for wrd in possible_words if check_for_known_letters(
            wrd, existing_info['known']
    )]

    
    
    



    return possible_words   



