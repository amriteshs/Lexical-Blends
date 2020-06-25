import re
import jellyfish as jf
from itertools import combinations
from datetime import datetime


def global_edit_distance(f, t):
    x = [[0] * (len(t) + 1)] * (len(f) + 1)

    for i in range(1, len(f) + 1):
        x[i][0] = -i

    for j in range(1, len(t) + 1):
        x[0][j] = -j

    for i in range(1, len(f) + 1):
        for j in range(1, len(t) + 1):
            x[i][j] = max(x[i][j - 1] - 1, x[i - 1][j] - 1, x[i - 1][j - 1] + (1 if f[i - 1] == t[j - 1] else -1))

    return x[len(f)][len(t)]


def jaro_winkler(f, t):
    return jf.jaro_winkler(f, t)


def levenshtein(f, t):
    return jf.levenshtein_distance(f, t)


def prefix_ranks(candidate, lexicon):
    words = {}

    for c in range(2, len(candidate) - 2):
        x = candidate[:c]

        for l in lexicon:
            if len(l) > c and l[:c] == x and l not in words:
                words[l] = jaro_winkler(l, candidate)

    return sorted([(k, v) for k, v in words.items()], key=lambda t: t[1], reverse=True)


def suffix_ranks(candidate, lexicon):
    words = {}

    for c in range(3, len(candidate) - 1):
        x = candidate[(len(candidate) - c):len(candidate)]

        for l in lexicon:
            if len(l) > c and l[(len(l) - c):len(l)] == x and l not in words:
                words[l] = jaro_winkler(l[::-1], candidate[::-1])

    return sorted([(k, v) for k, v in words.items()], key=lambda t: t[1], reverse=True)


def filter_data(data):
    filtered_data = []

    for i in range(len(data)):
        if len(data[i]) < 4:
            continue

        if len(data[i]) > 1:
            if data[i].endswith('s'):
                if data[i][:-1] in dictionary:
                    continue

        if len(data[i]) > 2:
            if data[i].endswith('ed'):
                if data[i][:-2] in dictionary:
                    continue

            if data[i].endswith('en'):
                if data[i][:-2] in dictionary:
                    continue

        if len(data[i]) > 3:
            if data[i].endswith('ing'):
                if data[i][:-3] in dictionary:
                    continue

            if data[i].endswith('in'):
                if data[i] + 'g' in dictionary:
                    continue

        if len(set([data[i][j] for j in range(len(data[i]))])) < 3:
            continue

        if re.findall(r'(.)\1\1', data[i]):
            continue

        flag = False
        subseqs = set([data[i][j:k] for j, k in combinations(range(len(data[i]) + 1), r=2) if k - j > 1])

        for j in subseqs:
            if j * 3 in data[i]:
                flag = True
                break

        if flag:
            continue

        filtered_data.append(data[i])

    return filtered_data


def read_data(filename):
    data = []

    with open(filename) as file:
        for line in file:
            if not line.isspace():
                data.append(line.split('\n')[0].split()[0])

    return data


if __name__ == '__main__':
    ti = datetime.now()

    dictionary = read_data('dict.txt')
    candidates = read_data('candidates.txt')
    true_blends = read_data('blends.txt')

    candidates = filter_data(candidates)

    detected_blends = []
    threshold = 0.935

    for i in candidates:
        p = prefix_ranks(i, dictionary)
        s = suffix_ranks(i, dictionary)

        if not p or not s:
            continue

        x = False
        y = False

        for j in p:
            flag = False

            for k in s:
                if len(j[0]) + len(k[0]) >= len(i) and j[0] != k[0]:
                    x = j
                    y = k
                    flag = True
                    break

            if flag:
                break

        if not x or not y:
            continue

        if x[1] > threshold and y[1] > threshold:
            detected_blends.append(i)

    accuracy = 100 * (len([i for i in detected_blends if i in true_blends]) + len([i for i in candidates if i not in detected_blends and i not in true_blends])) / len(candidates)
    precision = 100 * len([i for i in detected_blends if i in true_blends]) / len(detected_blends)

    print(f'Accuracy: {accuracy:.2f}%')
    print(f'Precision: {precision:.2f}%')

    tf = datetime.now()
    tdiff = (tf - ti).total_seconds()
    print(f'\nTime taken for execution: {int(tdiff // 60)}min{int(tdiff % 60)}sec')
