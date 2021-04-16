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

def _solve(key, W1_inter, W2_inter,intersect_key_1, intersect_key_2, possible_words):

    final_words = {}
    for regW1, W1list in possible_words.get(key).items():
        for Word_1 in W1list:
            for regW2, W2list in possible_words.get(W1_inter).items():
                for Word_2 in W2list:
                    for regW3, W3list in possible_words.get(W2_inter).items():
                        for Word_3 in W3list:
                            if Word_1[int(intersect_key_1[0])] == Word_2[int(intersect_key_1[1])]:
                                if Word_2[int(intersect_key_2[0])] == Word_3[int(intersect_key_2[1])]:
                                    if [Word_1] not in final_words.values():
                                        final_words[regW1] = [Word_1]


    return final_words

def solve_puzzle(crossboard_words, possible_words):
    results = None
    known_words = {}
    for key_1, value_1 in crossboard_words.items():
        intersect_1 = value_1.get('intersects')
        for key_2, value_2 in intersect_1.items():
            intersect_2 = crossboard_words.get(key_2).get('intersects')
            intersect_key_1 = (intersect_2.get(key_1), value_2)
            for key_3, value_3 in intersect_2.items():
                if key_3 is not key_1:
                    intersect_3 = crossboard_words.get(key_3).get('intersects')
                    intersect_key_2 = (intersect_3.get(key_2), value_3)
                    known_words[key_1] = _solve(key_1, key_2, key_3, intersect_key_1, intersect_key_2, possible_words)

    print(known_words)
    #
    # print('HAHAAA' in known_words.get('0').get('HAHA*'))
    # print('HEHEHE' in known_words.get('1').get('HE(HE)+'))
    # print('HOHO' in known_words.get('2').get('(HO)+'))
    # print('HAA' in known_words.get('3').get('HA+'))
    # print('TEHEHEHE' in known_words.get('4').get('TE(HE+)+'))
    # print('LOOL' in known_words.get('5').get('LO+L'))
    # print('LOLOLOL' in known_words.get('6').get('L(OL)+'))
    # print('LULZ' in known_words.get('7').get('LULZ'))
    # print('KEKE' in known_words.get('8').get('K(EK)*E'))
    # print('ROTFL' in known_words.get('9').get('ROT?FL'))
    # print('MWAHA' in known_words.get('10').get('MWA(HA)+'))
    # print('LAWL' in known_words.get('11').get('LAW*L'))
    # print('HEH' in known_words.get('12').get('H(EH)+'))
    # print('HARRHARR' in known_words.get('13').get('(HAR+)+'))
    # print('JAJAJAJAJA' in known_words.get('14').get('(JA)+'))
    # print('AHAHA' in known_words.get('15').get('(AH)+A+'))

    return results


crossboard_words = read_csv('laughs.csv')
regEx = read_regex('laughs.txt')
print(crossboard_words)

all_strings = get_all_strings(regEx)
possible_words = get_all_possible_words(crossboard_words, all_strings)
print(possible_words)

print(solve_puzzle(crossboard_words, possible_words))
