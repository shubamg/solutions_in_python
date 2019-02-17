"""Good morning! Here's your coding interview problem for today.
This problem was asked by Quora.
Given a string, find the palindrome that can be made by inserting the fewest number
of characters as possible anywhere in the word. If there is more than one
palindrome of minimum length that can be made,
return the lexicographically earliest one (the first one alphabetically).
For example, given the string "race", you should return "ecarace",
since we can add three letters to it (which is the smallest amount to make a palindrome).
There are seven other palindromes that can be made from "race" by adding three letters,
but "ecarace" comes first alphabetically.
As another example, given the string "google", you should return "elgoogle"."""
from collections import deque


def f(input: str):
    N = len(input)
    lengths = [[N+1] * N for i in range(N+1)]

    for length in range(1, N+1):
        for begin in range(N- length + 1):
            end = begin + length - 1
            if length <= 1:
                lengths[length][begin] = length
            elif input[begin] == input[end]:
                lengths[length][begin] = lengths[length-2][begin+1] + 2
            else:
                lengths[length][begin] = min(lengths[length-2][begin+1], lengths[length-2][begin+1]) + 2

    def get_palindrome(begin, end):
        if begin > end:
            d = deque()
        elif begin == end:
            d = deque([input[begin]])
        elif input[begin] == input[end]:
            d = get_palindrome(begin+1, end-1)
            d.append(input[begin])
            d.appendleft(input[begin])
        else:
            l1 = lengths[end - begin][begin]
            l2 = lengths[end - begin][begin+1]
            if l1 == l2:
                if input[begin] < input[end]:
                    d = get_palindrome(begin+1, end)
                    d.appendleft(input[begin])
                    d.append(input[begin])
                else:
                    d = get_palindrome(begin, end-1)
                    d.appendleft(input[end])
                    d.append(input[end])
            elif l1 < l2:
                d = get_palindrome(begin, end - 1)
                d.appendleft(input[end])
                d.append(input[end])
            else:
                d = get_palindrome(begin + 1, end)
                d.appendleft(input[begin])
                d.append(input[begin])

        return d

    d = get_palindrome(0, N-1)
    return '{} of length {:d} --> {} of length {:d}'.format(input, len(input), ''.join(d), len(d))


print(f('race'))
print(f('google'))
print(f('quora'))
print(f('abcde'))
