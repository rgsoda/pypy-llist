#!/usr/bin/env python
# -*- coding: utf-8 -*-
from weakref import ref


class SLLNode:
    """ Node model """
    __slots__ = ['next', 'value', 'weakref']

    def __init__(self, value=None, next=None, weakref=None):
        self.next = next
        self.value = value
        self.weakref = weakref

    def __call__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class SLList:
    """ SLList model """
    __slots__ = ['first', 'last', 'size']

    def __init__(self, iterable=None):
        self.first = None
        self.last = None
        self.size = 0
        if iterable:
            self.__extend(iterable)

    def __extend(self, iterable):
        for item in iterable:
            self.appendright(item)

    def __iter__(self):
        curr = self.first
        while curr:
            yield curr
            curr = curr.next

    def __str__(self):
        return str(list(self))

    def __getitem__(self, index):
        i = 0
        if index < 0 and index > self.size:
            raise IndexError("Not such index")
        curr = self.first
        while(curr != None and i < index):
            curr = curr.next
            i += 1
        return curr

    def __setitem__(self, index, value):
        node = self.__getitem__(index)
        if isinstance(value, SLLNode):
            value = value.value
        node.value = value

    def __get_prev(self, node):
        if not isinstance(node, SLLNode):
            raise TypeError("Object must be Node instance")
        if not self.first:
            raise TypeError("List is empty")
        if self.first == node:
            return None
        curr = self.first
        prev = None
        while(curr and curr != node):
            prev = curr
            curr = curr.next
        del curr
        return prev

    def appendleft(self, value):
        if isinstance(value, SLLNode):
            value = value.value

        head = self.first
        new_node = SLLNode(value=value, next=head, weakref=ref(self))
        self.first = new_node
        return new_node

    def append(self, value):
        return self.appendright(value)

    def appendright(self, value):
        if isinstance(value, SLLNode):
            value = value.value

        new_node = SLLNode(value=value, next=None, weakref=ref(self))
        if not self.first:
            self.first = new_node
        else:
            self.last.next = new_node
        self.last = new_node
        self.size += 1
        return new_node

    def popleft(self):
        if not self.first:
            raise RuntimeError("List is empty")
        del_node = self.first
        self.first = del_node.next
        if self.last == del_node:
            self.last = None
        self.size -= 1
        rval = del_node.value
        del del_node
        return rval

    def pop(self):
        return self.popright()

    def popright(self):
        if not self.first:
            raise RuntimeError("List is empty")
        del_node = self.last
        if self.first == del_node:
            self.last = None
            self.first = None
        else:
            prev = self.__get_prev(del_node)
            prev.next = None
            self.last = prev
        self.size -= 1
        rval = del_node.value
        del del_node
        return rval

    def remove(self, node):
        if not node.weakref == ref(self):
            raise RuntimeError("Node is not element of this list")
        prev = self.__get_prev(node)
        if not prev:
            self.popleft()
        else:
            prev.next = node.next
        rval = node.value
        del node
        return rval

if __name__ == '__main__':
    l = SLList(range(100, 115))
    print "Initialized list", l
    for i in range(0, 10):
        l.appendleft(i)
    print "After append left", l
    for i in range(0, 10):
        l.appendright(i)
    print "After append right", l
    for i in range(0, 10):
        l.popleft()
    print "After pop left", l
    for i in range(0, 10):
        l.popright()
    print "After pop right", l
