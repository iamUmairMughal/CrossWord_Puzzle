import csv
import re
import sre_yield

def read_csv(filename):
    crossboard = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            temp = {}
            for i in range(2, len(row), 2):
                temp[row[i]] = row[i+1]

            crossboard[row[0]] = {'word': row[1],
                                  'word_len': len(row[1]),
                                  'unknown_char': row[1].count('.'),
                                  'intersects': temp}
    return crossboard


def read_regex(filename):
    regex = []

    with open(filename, 'r') as file:
        reader = file.read()
        for row in reader.split('\n'):
            if row != '':
                regex.append(row)

    return regex

def get_all_strings(regEx):
    result={}
    for reg in regEx:
        strs = sre_yield.AllStrings(reg, max_count=5)
        result[reg] = list(strs)

    return result


def get_all_possible_words(crossboard_words, all_strings):
    possible_words = {}

    for key, val in crossboard_words.items():
        words = {}
        for k, v in all_strings.items():
            temp = []
            for s in v:
                if len(s) == val.get('word_len') and s not in temp:
                    temp.append(s)
            if len(temp) > 0:
                words[k] = temp

        possible_words[key] = words

    return possible_words
def _solve(W1_inters, key, word_W1, known_words, possible_words):

    for ik, ipos in W1_inters.items():
        W2 = crossboard_words.get(ik)
        W2_possible = possible_words.get(ik)
        W2_inters = W2.get('intersects').get(key)

        for rW2, word_W2 in W2_possible.items():
            for word in word_W2:
                # print(word, len(word))
                if word[int(W2_inters)] == word_W1[int(ipos)]:
                    print(key, 'W1:', word_W1)
                    print(ik, 'W2:', word)
                    known_words[ik] = word
    print(known_words)
    return known_words

def solve_puzzle(crossboard_words, possible_words):
    results = None
    known_words = {}
    for key, value in crossboard_words.items():
        if value.get('unknown_char') == 0:
            known_words[key] = value.get('word')

    while len(known_words) != len(crossboard_words):
            key = list(known_words.keys())[-1]
            W1 = crossboard_words.get(key)
            word_W1 = known_words.get(key)
            W1_inters = W1.get('intersects')
            known_words = _solve(W1_inters, key, word_W1, known_words, possible_words)

    return results


crossboard_words = read_csv('laughs.csv')
regEx = read_regex('laughs.txt')
print(crossboard_words)

all_strings = get_all_strings(regEx)
possible_words = get_all_possible_words(crossboard_words, all_strings)
print(possible_words)

print(solve_puzzle(crossboard_words, possible_words))



#
# def solve_puzzle(crossboard_words, possible_words):
#     results = None
#     for key, value in crossboard_words.items():
#         word = None
#         inter = value.get('intersects')
#         pos_words = possible_words.get(key)
#         for i, pos in inter.items():
#             inter_words = possible_words.get(i)
#             i_inter = crossboard_words.get(i).get('intersects').get(key)
#             for kr, kw in pos_words.items():
#                 for ir,iw in inter_words.items():
#                     for w1 in kw:
#                         for w2 in iw:
#                             if w1[int(i_inter)] == w2[int(pos)]:
#                                 print(key, (kr, w1))
#                                 print(i, (ir,w2))
#         break
#     return results