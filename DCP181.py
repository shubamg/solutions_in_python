"""This problem was asked by Google.
Given a string, split it into as few strings as possible such that each string is a palindrome.
For example, given the input string racecarannakayak, return ["racecar", "anna", "kayak"].
Given the input string abc, return ["a", "b", "c"]."""

from collections import defaultdict
"""O(n2) space and time algorithm"""


def get_all_palindromic_substrings(s):
    length_of_palindromes_with_given_end_point = defaultdict(list)

    # calculate odd length palindromes
    for i in range(len(s)):
        j=0
        while i+j < len(s) and i-j >=0 and s[i+j]==s[i-j]:
            length_of_palindromes_with_given_end_point[i+j].append((j<<1) + 1)
            j += 1

    # calculate even length palindromes [i-1-j, i+j]
    for i in range(1, len(s)):
        j = 0
        while i + j < len(s) and i - j -1 >= 0 and s[i + j] == s[i - j - 1]:
            length_of_palindromes_with_given_end_point[i + j].append((j << 1) + 2)
            j += 1

    return length_of_palindromes_with_given_end_point


def get_min_palindromic_partition(s):
    INF = len(s) + 1
    min_partition_dp = [(INF, 0)] * (len(s) + 1)
    min_partition_dp[0] = (0, 0)
    length_of_palindromes_with_given_end_point = get_all_palindromic_substrings(s)
    for i in range(len(s)):
        for j in length_of_palindromes_with_given_end_point[i]:
            if min_partition_dp[i+1][0] > 1 + min_partition_dp[i-j+1][0]:
                min_partition_dp[i+1] = (min_partition_dp[i-j+1][0]+1, j)

    palindromic_breakup = []
    i=len(s)-1
    while i >= 0:
        palindromic_breakup.append(s[i-min_partition_dp[i+1][1]+1:i+1])
        i -= min_partition_dp[i+1][1]
    palindromic_breakup.reverse()
    return s, palindromic_breakup


print(get_min_palindromic_partition("racecarannakayak"))
