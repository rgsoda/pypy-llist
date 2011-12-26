#!/usr/bin/env python
# -*- coding: utf-8 -*-

class dllistnode(object):
    __slots__ = ('__prev', '__next', '__value', '__list')

    def __init__(self, value=None, prev=None, next=None, list=None):
        if isinstance(value, dllistnode):
            value = value.value

        self.__prev = prev
        self.__next = next
        self.__value = value
        self.__list = list

        if prev is not None:
            prev.__next = self 
        if next is not None:
            next.__prev = self

    @property
    def prev(self):
        return self.__prev

    @property
    def next(self):
        return self.__next

    @property
    def value(self):
        return self.__value

    @property
    def list(self):
        return self.__list

    def __call__(self):
        return self.__value

    def __str__(self):
        return 'dllistnode(' + str(self.__value) + ')'

    def __repr__(self):
        return '<dllistnode(' + repr(self.__value) + ')>'


class dllistiterator(object):
    __slots__ = ('__current_node',)

    def __init__(self, list):
        if not isinstance(list, dllist):
            raise TypeError('dllist argument expected')

        self.__current_node = list.first

    def next(self):
        if self.__current_node is None:
            raise StopIteration

        value = self.__current_node.value
        self.__current_node = self.__current_node.next

        return value

    def __iter__(self):
        return self


class dllist(object):
    __slots__ = ('__first', '__last', '__size',
                 '__last_access_node', '__last_access_idx')

    def __init__(self, sequence=None):
        self.__first = None
        self.__last = None
        self.__size = 0
        self.__last_access_node = None
        self.__last_access_idx = -1

        if sequence is None:
            return

        for value in sequence:
            node = dllistnode(value, self.__last, None, self)

            if self.__first is None:
                self.__first = node
            self.__last = node
            self.__size += 1

    @property
    def first(self):
        return self.__first

    @property
    def last(self):
        return self.__last

    @property
    def size(self):
        return self.__size

    def appendleft(self, x):
        node = dllistnode(x, None, self.__first, self)

        if self.__first is self.__last:
            self.__last = node
        self.__first = node
        self.__size += 1

        if self.__last_access_idx >= 0:
            self.__last_access_idx += 1
        return node

    def appendright(self, x):
        node = dllistnode(x, self.__last, None, self)

        if self.__first is self.__last:
            self.__first = node
        self.__last = node
        self.__size += 1

        return node

    def append(self, x):
        return self.appendright(x)

    def insert(self, x, before=None):
        if before is None:
            return self.appendright(x)

        if not isinstance(before, dllistnode):
            raise TypeError('before argument must be a dllistnode')

        if before.list is not self:
            raise ValueError('before argument belongs to another list')

        node = dllistnode(x, before.prev, before, self)

        if before is self.__first:
            self.__first = node
        self.__size += 1

        self.__last_access_node = None
        self.__last_access_idx = -1

        return node

    def popleft(self):
        if self.__first is None:
            raise ValueError('list is empty')

        node = self.__first
        self.__first = node.next
        if self.__last is node:
            self.__last = None
        self.__size -= 1

        if node.prev is not None:
            node.prev._dllistnode__next = node.next
        if node.next is not None:
            node.next._dllistnode__prev = node.prev

        if self.__last_access_node is not node:
            if self.__last_access_idx >= 0:
               self.__last_access_idx -= 1
        else:
            self.__last_access_node = None
            self.__last_access_idx = -1

        return node.value

    def popright(self):
        if self.__last is None:
            raise ValueError('list is empty')

        node = self.__last
        self.__last = node.prev
        if self.__first is node:
            self.__first = None
        self.__size -= 1

        if node.prev is not None:
            node.prev._dllistnode__next = node.next
        if node.next is not None:
            node.next._dllistnode__prev = node.prev

        if self.__last_access_node is node:
            self.__last_access_node = None
            self.__last_access_idx = -1

        return node.value

    def pop(self):
        return self.popright()

    def remove(self, node):
        if not isinstance(node, dllistnode):
            raise TypeError('node argument must be a dllistnode')

        if self.__first is None:
            raise ValueError('list is empty')

        if node.list is not self:
            raise ValueError('node argument belongs to another list')

        if self.__first is node:
            self.__first = node.next
        if self.__last is node:
            self.__last = node.prev
        self.__size -= 1

        if node.prev is not None:
            node.prev._dllistnode__next = node.next
        if node.next is not None:
            node.next._dllistnode__prev = node.prev

        self.__last_access_node = None
        self.__last_access_idx = -1

        return node.value

    def __len__(self):
        return self.__size

    def __cmp__(self, other):
        result = len(self) - len(other)
        if result < 0:
            return -1
        elif result > 0:
            return 1

        for sval, oval in zip(self, other):
            result = cmp(sval, oval)
            if result != 0:
                return result

        return 0

    def __str__(self):
        if self.__first is not None:
            return 'dllist([' + ', '.join((str(x) for x in self)) + '])'
        else:
            return 'dllist()'

    def __repr__(self):
        if self.__first is not None:
            return 'dllist([' + ', '.join((repr(x) for x in self)) + '])'
        else:
            return 'dllist()'

    def __iter__(self):
        return dllistiterator(self)

    def __getitem__(self, index):
        return self.__get_node_at(index)

    def __setitem__(self, index, value):
        self.__get_node_at(index).value = value

    def __delitem__(self, index):
        node = self.__get_node_at(index)
        self.remove(node)

        if node.prev is not None and index > 0:
            self.__last_access_node = node.prev
            self.__last_access_idx = index - 1

    def __get_node_at(self, index):
        if not isinstance(index, int):
            raise TypeError('invalid index type')

        if index < 0:
            index = self.__size + index

        if index < 0 or index >= self.__size:
            raise IndexError('index out of range')

        middle = index / 2
        if index <= middle:
            node = self.__first
            start_idx = 0
            reverse_dir = False
        else:
            node = self.__last
            start_idx = self.__size - 1
            reverse_dir = True

        if self.__last_access_node is not None and \
                self.__last_access_idx >= 0 and \
                abs(index - self.__last_access_idx) < middle:
            node = self.__last_access_node
            start_idx = self.__last_access_idx
            if index < start_idx:
                reverse_dir = True
            else:
                reverse_dir = False

        if not reverse_dir:
            while start_idx < index:
                node = node.next
                start_idx += 1
        else:
            while start_idx > index:
                node = node.prev
                start_idx -= 1

        self.__last_access_node = node
        self.__last_access_idx = index

        return node
