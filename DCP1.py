"""This problem was recently asked by Google.
Given a list of numbers and a number k, return whether any two numbers from the list add up to k.
For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.
Bonus: Can you do this in one pass?"""


def f(number_list, k):
    number_set = set()
    for number in number_list:
        complement = k - number
        if complement in number_set:
            return True
        number_set.add(complement)
    return False


if __name__ == "__main__":
    input_list = [([1,2,3,4,5,5], 10),
                  ([47, -94, 85, 53], 100)]
    input_numbers, Ks =  zip(*input_list)
    answer = map(f, input_numbers, Ks)
    print answer