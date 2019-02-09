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


print(g(['quick', 'brown', 'the', 'fox'], "thequickbrownfox"))
print(g(['bed', 'bath', 'and', 'beyond'], "bedbathandbeyond"))
print(g(['a', 'bcd' 'e'], "bceaebcad"))
