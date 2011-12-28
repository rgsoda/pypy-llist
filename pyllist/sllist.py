#!/usr/bin/env python
# -*- coding: utf-8 -*-


class sllistnode(object):
    __slots__ = ('__next', '__value', '__owner')

    def __init__(self, value=None, next=None, owner=None):
        self.__next = next
        self.__value = value
        self.__owner = owner

    @property
    def next(self):
        return self.__next

    @property
    def value(self):
        return self.__value

    @property
    def owner(self):
        return self.__owner

    def __call__(self):
        return self.__value

    def __str__(self):
        return "sllistnode(%s)" % str(self.__value)

    def __repr__(self):
        return "<sllistnode(%s)>" % repr(self.__value)


class sllist(object):
    __slots__ = ('__first', '__last', '__size', )

    def __init__(self, iterable=None):
        self.__first = None
        self.__last = None
        self.__size = 0
        if iterable:
            self.__extend(iterable)

    @property
    def first(self):
        return self.__first

    @property
    def last(self):
        return self.__last

    @property
    def size(self):
        return self.__size

    def __extend(self, iterable):
        for item in iterable:
            self.appendright(item)

    def __delitem__(self, index):
        to_del = self.__getitem__(index)
        self.remove(to_del)

    def __getitem__(self, index):
        if abs(index) >= self.__size:
            raise IndexError("list index out of range")
        i = 0
        if index < 0:
            index = self.__size + index
        if not self.__first:
            raise IndexError("list index out of range")
        curr = self.__first
        while(curr != None and i < index):
            curr = curr.next
            i += 1
        return curr

    def __len__(self):
        return self.__size

    def __setitem__(self, index, value):
        node = self.__getitem__(index)
        if isinstance(value, sllistnode):
            value = value.value
        node.value = value

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
            return "sllist([%s])" % ', '.join((str(x) for x in self))
        else:
            return 'sllist()'

    def __repr__(self):
        if self.__first is not None:
            return "sllist([%s])" % ', '.join((repr(x) for x in self))
        else:
            return 'sllist()'

    def __iter__(self):
        current = self.__first
        while current is not None:
            yield current.value
            current = current.next

    def __get_prev(self, node):
        if not isinstance(node, sllistnode):
            raise TypeError("Object must be Node instance")
        if not self.__first:
            raise IndexError("List is empty")
        if self.__first == node:
            return None
        curr = self.__first
        prev = None
        while(curr and curr != node):
            prev = curr
            curr = curr.next
        return prev

    def appendleft(self, value):
        if isinstance(value, sllistnode):
            value = value.value
        new_node = sllistnode(value=value, next=self.__first, owner=self)
        self.__first = new_node
        self.__size += 1
        return new_node

    def insert(self, value, before=None):
        if before is None:
            return self.appendright(value)
        else:
            return self.insertbefore(before, value)

    def insertafter(self, node, value):
        if not isinstance(node, sllistnode):
            raise TypeError("node must be instance of sllistnode")
        if isinstance(value, sllistnode):
            value = value.value
        new_node = sllistnode(value=value, next=None, owner=self)
        new_node._sllistnode__next = node.next
        node._sllistnode__next = new_node
        self.__size += 1
        return new_node

    def insertbefore(self, node, value):
        if not isinstance(node, sllistnode):
            raise TypeError("node must be instance of sllistnode")
        if isinstance(value, sllistnode):
            value = value.value
        new_node = sllistnode(value=value, next=None, owner=self)
        prev = self.__get_prev(node)
        if prev:
            prev._sllistnode__next = new_node
            new_node._sllistnode__next = node
        else:
            new_node._sllistnode__next = node
            self.__first = new_node
        self.__size += 1
        return new_node

    def append(self, value):
        return self.appendright(value)

    def appendright(self, value):
        if isinstance(value, sllistnode):
            value = value.value
        new_node = sllistnode(value=value, next=None, owner=self)
        if not self.__first:
            self.__first = new_node
        else:
            self.__last._sllistnode__next = new_node
        self.__last = new_node
        self.__size += 1
        return new_node

    def popleft(self):
        if not self.__first:
            raise RuntimeError("List is empty")
        del_node = self.__first
        self.__first = del_node.next
        if self.__last == del_node:
            self.__last = None
        self.__size -= 1
        return del_node.value

    def pop(self):
        return self.popright()

    def popright(self):
        if not self.__first:
            raise RuntimeError("List is empty")
        del_node = self.__last
        if self.__first == del_node:
            self.__last = None
            self.__first = None
        else:
            prev = self.__get_prev(del_node)
            prev._sllistnode__next = None
            self.__last = prev
        self.__size -= 1
        return del_node.value

    def remove(self, node):
        if not isinstance(node, sllistnode):
            raise TypeError("node must be a sllistnode")
        if self.__first is None:
            raise RuntimeError("List is empty")
        if node.owner != self:
            raise RuntimeError("Node is not element of this list")
        prev = self.__get_prev(node)
        if not prev:
            self.popleft()
        else:
            prev._sllistnode__next = node.next
            self.__size -= 1
        return node.value
