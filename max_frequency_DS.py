class Node:

    def __init__(self, frequency, element):
        self.elements = set([element])
        self.frequency = frequency
        self._prev = None
        self._next = None

    def set_neighbours(self, prev, _next):
        self._prev = prev
        self._next = _next

    def is_empty(self):
        return len(self.elements) == 0

    def remove_element(self, element):
        self.elements.remove(element)

    def add_element(self, element):
        self.elements.add(element)

    def set_next(self, _next):
        self._next = _next

    def set_prev(self, _prev):
        self._prev = _prev

    def get_next(self):
        return self._next

    def get_prev(self):
        return self._prev

    def get_frequency(self):
        return self.frequency

    def __str__(self):
        return 'Element(s) with frequency {} are: {}'.format(str(self.get_frequency()),
                                                             ', '.join(map(str, self.elements)))


class DoublyLinkedListIterator:

    def __init__(self, begin, end):
        self.current_position = begin
        self.end_position = end

    def next(self):
        if self.current_position == self.end_position:
            raise StopIteration
        else:
            self.current_position = self.current_position.get_next()
            return self.current_position.get_prev()


class DoublyLinkedList:
    INFINITY = 2**32

    def __init__(self):
        self.HEAD = Node(DoublyLinkedList.INFINITY, None)
        self.TAIL = self.HEAD
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def add_node(self, location, node):
        prev = location.get_prev()
        node.set_neighbours(prev, location)
        if prev:
            prev.set_next(node)
        else:
            self.HEAD = node
        location.set_prev(node)

    def remove_node(self, location):
        prev = location.get_prev()
        _next = location.get_next()
        if prev:
            prev.set_next(_next)
        else:
            self.HEAD = _next
        _next.set_prev(prev)

    def begin(self):
        return self.HEAD

    def end(self):
        return self.TAIL

    def print_max_freq(self):
        if self.begin() == self.end():
            print "Oops!! No element in the DS!! Hence no max frequency elements"
        else:
            print "Here are the elements with Max Frequency:"
            print self.end().get_prev(), '\n'

    def __iter__(self):
        return DoublyLinkedListIterator(self.begin(), self.end())

    def __str__(self):
        return '\n'.join((node.__str__() for node in self))+'\n'


class MaxFrequencyDS:
    def __init__(self):
        self.frequencies_to_elements = DoublyLinkedList()
        self.element_to_node = {}

    def __init__(self, initialliser_list):
        self.frequencies_to_elements = DoublyLinkedList()
        self.element_to_node = {}
        self.add_list(initialliser_list)

    def add_list(self, list_of_elements):
        for number in list_of_elements:
            self.add(number)

    def remove_list(self, list_of_elements):
        for number in list_of_elements:
            self.remove(number)

    def add(self, element):
        if element in self.element_to_node:
            old_node = self.element_to_node[element]
            new_freq = old_node.get_frequency() + 1
            next_node = old_node.get_next()

            if next_node == self.frequencies_to_elements.end() or \
                    next_node.get_frequency() > new_freq:
                self.element_to_node[element] = Node(element=element, frequency=new_freq)
                self.frequencies_to_elements.add_node(next_node, self.element_to_node[element])
            else:
                next_node.add_element(element)
                self.element_to_node[element] = next_node

            old_node.remove_element(element)
            if old_node.is_empty():
                self.frequencies_to_elements.remove_node(old_node)
        else:
            HEAD = self.frequencies_to_elements.begin()
            if HEAD.get_frequency() != 1:
                self.frequencies_to_elements.add_node(
                    HEAD, Node(frequency=1, element=element))
            else:
                HEAD.add_element(element)
            self.element_to_node[element] = self.frequencies_to_elements.begin()
        print "Added", element, ". State is:\n", self.frequencies_to_elements

    def remove(self, element):
        if element in self.element_to_node:
            current_node = self.element_to_node[element]
            new_freq = current_node.get_frequency() - 1
            new_node_with_element = None

            if new_freq:
                if current_node != self.frequencies_to_elements.begin():
                    prev_node = current_node.get_prev()
                    if prev_node.get_frequency() == new_freq:
                        prev_node.add_element(element)
                        new_node_with_element = prev_node

                if not new_node_with_element:
                    new_node_with_element = Node(frequency=new_freq, element=element)
                    self.element_to_node[element] = new_node_with_element
                    self.frequencies_to_elements.add_node(current_node, new_node_with_element)

                self.element_to_node[element] = new_node_with_element

            else:
                self.element_to_node.pop(element)

            current_node.remove_element(element)
            if current_node.is_empty():
                self.frequencies_to_elements.remove_node(current_node)
        else:
            raise Exception("Element {} does not exist in the data structure".format(element))
        print "Removed", element, ". State is:\n", self.frequencies_to_elements

    def print_max_freq(self):
        self.frequencies_to_elements.print_max_freq()


max_frequency_DS = MaxFrequencyDS([900, 456, 789, 23435354543])
max_frequency_DS.add(123)
max_frequency_DS.add(2345)
max_frequency_DS.add_list([123, 23435354543, 234])
max_frequency_DS.print_max_freq()
max_frequency_DS.remove_list([123, 23435354543])
max_frequency_DS.remove(23435354543)
max_frequency_DS.print_max_freq()
max_frequency_DS.remove(2)
