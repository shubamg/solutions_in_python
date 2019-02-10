"""This problem was asked by Microsoft.
Given a dictionary of words and a string made up of those words (no spaces),
return the original sentence in a list.
If there is more than one possible reconstruction,
return any of them. If there is no possible reconstruction, then return null.
For example, given the set of words 'quick', 'brown', 'the', 'fox',
and the string "thequickbrownfox", you should return ['the', 'quick', 'brown', 'fox'].
Given the set of words 'bed', 'bath', 'bedbath', 'and', 'beyond',
and the string "bedbathandbeyond", return either ['bed', 'bath', 'and', 'beyond]
or ['bedbath', 'and', 'beyond']."""


def g(words, sentence):
    def f(sentence):
        if not len(sentence):
            return [True, []]
        for word in words:
            if str.startswith(sentence, word):
                res = f(sentence[len(word):])
                if res[0]:
                    res[1].append(word)
                return res
        return [False, []]

    res = f(sentence)
    res[1].reverse()
    return res


def g_optimal(words, sentence):
    longest_word_length = max(map(len, words))
    end_index_to_last_word_of_decomposition = {-1: ''}
    for curr_index in range(len(sentence)):
        for end_index in end_index_to_last_word_of_decomposition:
            if (curr_index - end_index) <= longest_word_length and sentence[end_index+1:curr_index+1] in words:
                end_index_to_last_word_of_decomposition[curr_index] = sentence[end_index+1:curr_index+1]
                break
    if (len(sentence)-1) not in end_index_to_last_word_of_decomposition:
        return [False, []]

    decomposition = []
    curr_index = len(sentence)-1
    while curr_index >= 0:
        word = end_index_to_last_word_of_decomposition[curr_index]
        curr_index -= len(word)
        decomposition.append(word)

    decomposition.reverse()
    return [True, decomposition]


print(g_optimal(['quick', 'brown', 'the', 'fox'], "thequickbrownfox"))
print(g_optimal(['bed', 'bath', 'and', 'beyond'], "bedbathandbeyond"))
print(g_optimal(['a', 'bcd' 'e'], "bceaebcad"))
