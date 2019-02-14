import heapq as h


def get_median_of_stream(input):
    lower_nos = []
    higher_nos = []

    def push_and_get_median(x):
        if len(lower_nos) == len(higher_nos):
            if len(lower_nos) and x > -lower_nos[0]:
                h.heappush(higher_nos, x)
                return higher_nos[0]
            else:
                h.heappush(lower_nos, -x)
                return -lower_nos[0]
        else:
            if len(lower_nos) > len(higher_nos):
                y = -h.heappushpop(lower_nos, -x)
                h.heappush(higher_nos, y)
                y1 = -lower_nos[0]
            else:
                y = h.heappushpop(higher_nos, x)
                h.heappush(lower_nos, -y)
                y1 = higher_nos[0]
            return (y + y1)/2;

    return [push_and_get_median(x) for x in input]


input = [201.2, 1, 5, 7, 600, 2, 0, 5]
print(get_median_of_stream(input))
