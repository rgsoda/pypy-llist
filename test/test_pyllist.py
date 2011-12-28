#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pyllist import sllist
from pyllist import sllistnode
from pyllist import dllist
from pyllist import dllistnode


class testdllist(unittest.TestCase):

    def test_init_empty(self):
        ll = dllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)

    def test_init_with_non_sequence(self):
        self.assertRaises(TypeError, dllist, 1)
        self.assertRaises(TypeError, dllist, 1.5)

    def test_str(self):
        a = dllist([])
        self.assertEqual(str(a), 'dllist()')
        b = dllist([None, 1, 'abc'])
        self.assertEqual(str(b), 'dllist([None, 1, abc])')

    def test_repr(self):
        a = dllist([])
        self.assertEqual(repr(a), 'dllist()')
        b = dllist([None, 1, 'abc'])
        self.assertEqual(repr(b), 'dllist([None, 1, \'abc\'])')

    def test_node_str(self):
        a = dllist([None, None]).first
        self.assertEqual(str(a), 'dllistnode(None)')
        b = dllist([1, None]).first
        self.assertEqual(str(b), 'dllistnode(1)')
        c = dllist(['abc', None]).first
        self.assertEqual(str(c), 'dllistnode(abc)')
        pass

    def test_node_repr(self):
        a = dllist([None]).first
        self.assertEqual(repr(a), '<dllistnode(None)>')
        b = dllist([1, None]).first
        self.assertEqual(repr(b), '<dllistnode(1)>')
        c = dllist(['abc', None]).first
        self.assertEqual(repr(c), '<dllistnode(\'abc\')>')
        pass

    def test_cmp(self):
        a = dllist(xrange(0, 1100))
        b = dllist(xrange(0, 1101))
        c = [xrange(0, 1100)]
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(a, c), 1)
        self.assertEqual(cmp(c, a), -1)
        self.assertEqual(cmp([], []), 0)
        self.assertEqual(cmp([], a), -1)
        self.assertEqual(cmp(a, []), 1)

    def test_iter(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        idx = 0
        for val in ll:
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iter_empty(self):
        ll = dllist()
        count = 0
        for val in ll:
            count += 1
        self.assertEqual(count, 0)

    def test_insert_value(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, ll[-2])
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_value_before(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 10, 2, 3])
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, ll[2])
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, ll[1])
        self.assertEqual(new_node.next, ll[3])
        self.assertEqual(ll[1].next, new_node)
        self.assertEqual(ll[3].prev, new_node)
        self.assertEqual(ll, ref)

    def test_insert_invalid_ref(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.insert, 10, 1)
        self.assertRaises(TypeError, ll.insert, 10, 'abc')
        self.assertRaises(TypeError, ll.insert, 10, [])

    def test_append(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        arg_node = dllistnode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, ll[-2])
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_appendleft(self):
        ll = dllist(xrange(4))
        ref = dllist([10, 0, 1, 2, 3])
        arg_node = dllistnode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, ll[1])
        self.assertEqual(ll[1].prev, new_node)
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_appendright(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        arg_node = dllistnode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, ll[-2])
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.pop()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_del(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        del ll[0]
        del ref[0]
        self.assertEqual(list(ll), ref)
        del ll[len(ll) - 1]
        del ref[len(ref) - 1]
        self.assertEqual(list(ll), ref)
        del ll[(len(ll) - 1) / 2]
        del ref[(len(ref) - 1) / 2]
        self.assertEqual(list(ll), ref)

        def del_item(idx):
            del ll[idx]
        self.assertRaises(IndexError, del_item, len(ll))

        for i in xrange(len(ll)):
            del ll[0]
        self.assertEqual(len(ll), 0)

    def test_list_readonly_attributes(self):
        ll = dllist(range(4))
        self.assertRaises(AttributeError, setattr, ll, 'first', None)
        self.assertRaises(AttributeError, setattr, ll, 'last', None)
        self.assertRaises(AttributeError, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        ll = dllistnode()
        self.assertRaises(AttributeError, setattr, ll, 'prev', None)
        self.assertRaises(AttributeError, setattr, ll, 'next', None)


class testsllist(unittest.TestCase):

    def test_init_empty(self):
        ll = sllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)

    def test_init_with_non_sequence(self):
        self.assertRaises(TypeError, sllist, 1)
        self.assertRaises(TypeError, sllist, 1.5)

    def test_str(self):
        a = sllist([])
        self.assertEqual(str(a), 'sllist()')
        b = sllist([None, 1, 'abc'])
        self.assertEqual(str(b), 'sllist([None, 1, abc])')

    def test_repr(self):
        a = sllist([])
        self.assertEqual(repr(a), 'sllist()')
        b = sllist([None, 1, 'abc'])
        self.assertEqual(repr(b), 'sllist([None, 1, \'abc\'])')

    def test_node_str(self):
        a = sllist([None, None]).first
        self.assertEqual(str(a), 'sllistnode(None)')
        b = sllist([1, None]).first
        self.assertEqual(str(b), 'sllistnode(1)')
        c = sllist(['abc', None]).first
        self.assertEqual(str(c), 'sllistnode(abc)')
        pass

    def test_node_repr(self):
        a = sllist([None]).first
        self.assertEqual(repr(a), '<sllistnode(None)>')
        b = sllist([1, None]).first
        self.assertEqual(repr(b), '<sllistnode(1)>')
        c = sllist(['abc', None]).first
        self.assertEqual(repr(c), '<sllistnode(\'abc\')>')
        pass

    def test_cmp(self):
        a = sllist(xrange(0, 1100))
        b = sllist(xrange(0, 1101))
        c = [xrange(0, 1100)]
        self.assertEqual(cmp(a, a), 0)
        self.assertEqual(cmp(a, b), -1)
        self.assertEqual(cmp(b, a), 1)
        self.assertEqual(cmp(a, c), 1)
        self.assertEqual(cmp(c, a), -1)
        self.assertEqual(cmp([], []), 0)
        self.assertEqual(cmp([], a), -1)
        self.assertEqual(cmp(a, []), 1)

    def test_iter(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        idx = 0
        for val in ll:
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iter_empty(self):
        ll = sllist()
        count = 0
        for val in ll:
            count += 1
        self.assertEqual(count, 0)

    def test_insert_value(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        arg_node = sllistnode(10)
        new_node = ll.insert(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_value_before(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 10, 2, 3])
        arg_node = sllistnode(10)
        new_node = ll.insert(arg_node, ll[2])
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, ll[3])
        self.assertEqual(ll[1].next, new_node)
        self.assertEqual(ll, ref)

    def test_insert_invalid_ref(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.insert, 10, 1)
        self.assertRaises(TypeError, ll.insert, 10, 'abc')
        self.assertRaises(TypeError, ll.insert, 10, [])

    def test_append(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        arg_node = sllistnode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_appendleft(self):
        ll = sllist(xrange(4))
        ref = sllist([10, 0, 1, 2, 3])
        arg_node = sllistnode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, ll[1])
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_appendright(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        arg_node = sllistnode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(ll[-2].next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.pop()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_del(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        del ll[0]
        del ref[0]
        self.assertEqual(list(ll), ref)
        del ll[len(ll) - 1]
        del ref[len(ref) - 1]
        self.assertEqual(list(ll), ref)
        del ll[(len(ll) - 1) / 2]
        del ref[(len(ref) - 1) / 2]
        self.assertEqual(list(ll), ref)

        def del_item(idx):
            del ll[idx]
        self.assertRaises(IndexError, del_item, len(ll))

        for i in xrange(len(ll)):
            del ll[0]
        self.assertEqual(len(ll), 0)

    def test_list_readonly_attributes(self):
        ll = sllist(range(4))
        self.assertRaises(AttributeError, setattr, ll, 'first', None)
        self.assertRaises(AttributeError, setattr, ll, 'last', None)
        self.assertRaises(AttributeError, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        ll = sllistnode()
        self.assertRaises(AttributeError, setattr, ll, 'next', None)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testdllist))
    suite.addTest(unittest.makeSuite(testsllist))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
