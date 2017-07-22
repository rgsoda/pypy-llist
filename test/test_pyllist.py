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
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)
        self.assertIsNot(ll.first, None)
        self.assertEqual(ll.first.value, 0)
        self.assertIsNot(ll.last, None)
        self.assertEqual(ll.last.value, 1020)

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

    def test_node_repr(self):
        a = dllist([None]).first
        self.assertEqual(repr(a), '<dllistnode(None)>')
        b = dllist([1, None]).first
        self.assertEqual(repr(b), '<dllistnode(1)>')
        c = dllist(['abc', None]).first
        self.assertEqual(repr(c), '<dllistnode(\'abc\')>')

    def test_value_change(self):
        a = dllist([1, 2, 3])
        a.first.next.value = 5
        self.assertEqual(a[0], 1)
        self.assertEqual(a[1], 5)
        self.assertEqual(a[2], 3)

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

    def test_nodeat(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        for idx in xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), dllistnode))
            self.assertEqual(ll.nodeat(idx).value, ref[idx])
        for idx in xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), dllistnode))
            self.assertEqual(ll.nodeat(-idx - 1).value, ref[-idx - 1])
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, len(ref))
        self.assertRaises(IndexError, ll.nodeat, -len(ref) - 1)

    def test_nodeat_empty(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, 0)
        self.assertRaises(IndexError, ll.nodeat, -1)

    def test_iter(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        idx = 0
        for val in ll:
            self.assertFalse(isinstance(val, dllistnode))
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iternodes(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        idx = 0
        for node in ll.iternodes():
            self.assertTrue(isinstance(node, dllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iternodes_to(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        terminator_index = 200
        terminator = ll.nodeat(terminator_index)
        idx = 0
        for node in ll.iternodes(to=terminator):
            self.assertTrue(isinstance(node, dllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1
        self.assertEqual(node.value, (terminator_index-1)*4)
        self.assertEqual(idx, terminator_index)

    def test_iternext(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        idx = 100
        for node in ll.nodeat(idx).iternext():
            self.assertTrue(isinstance(node, dllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iternext_to(self, terminator_index=200):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        if terminator_index is not None:
            terminator = ll.nodeat(terminator_index)
        else:
            terminator = None

        original_idx = idx = 100
        for node in ll.nodeat(idx).iternext(to=terminator):
            self.assertTrue(isinstance(node, dllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1

        if terminator_index == original_idx:
            #self.assertRaises(UnboundLocalError, node)
            self.assertEqual(idx, terminator_index)
        elif terminator_index < original_idx:
            self.assertEqual(node.value, 1020)
            self.assertEqual(idx, 256)
        else:
            self.assertEqual(node.value, (terminator_index-1)*4)
            self.assertEqual(idx, terminator_index)

    def test_iternext_to_preceding_idx(self):
        self.test_iternext_to(terminator_index=50)

    def test_iternext_to_equal_idx(self):
        self.test_iternext_to(terminator_index=100)

    def test_iternext_to_None(self):
        self.test_iternext_to(terminator_index=None)

    def test_iterprev(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        idx = 100
        for node in ll.nodeat(idx).iterprev():
            self.assertTrue(isinstance(node, dllistnode))
            self.assertEqual(node.value, ref[idx])
            idx -= 1
        self.assertEqual(node.value, 0)
        self.assertEqual(idx, -1)

    def test_iter_empty(self):
        ll = dllist()
        count = 0
        for val in ll:
            count += 1
        self.assertEqual(count, 0)

    def test_iter_empty_nodes(self):
        ll = dllist()
        count = 0
        for val in ll.iternodes():
            count += 1
        self.assertEqual(count, 0)

    def test_reversed(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        idx = len(ref) - 1
        for val in reversed(ll):
            self.assertFalse(isinstance(val, dllistnode))
            self.assertEqual(val, ref[idx])
            idx -= 1
        self.assertEqual(idx, -1)

    def test_reversed_empty(self):
        ll = dllist()
        count = 0
        for val in reversed(ll):
            count += 1
        self.assertEqual(count, 0)

    def test_insert_value(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_guards_after_insert(self):
        ll = dllist()
        node1 = ll.insert(dllistnode(1))
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.insert(dllistnode(2))
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node2)

    def test_insert_value_before(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, ll.nodeat(2))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(ll, ref)

    def test_insert_value_after(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, after=ll.nodeat(1))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(ll, ref)

    def test_insert_value_before_first(self):
        ll = dllist(xrange(4))
        ref = dllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, ll.nodeat(0))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, next)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(new_node, ll.first)
        self.assertEqual(ll, ref)

    def test_insert_value_after_last(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(3)
        arg_node = dllistnode(10)
        new_node = ll.insert(arg_node, after=ll.last)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_invalid_ref(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.insert, 10, 1)
        self.assertRaises(TypeError, ll.insert, 10, 'abc')
        self.assertRaises(TypeError, ll.insert, 10, [])
        self.assertRaises(ValueError, ll.insert, 10, dllistnode())

    def test_append(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_guards_after_append(self):
        ll = dllist()
        node1 = ll.append(1)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.append(2)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node2)

    def test_appendleft(self):
        ll = dllist(xrange(4))
        ref = dllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = dllistnode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, None)
        self.assertEqual(new_node.next, next)
        self.assertEqual(next.prev, new_node)
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_guards_after_appendleft(self):
        ll = dllist()
        node1 = ll.appendleft(1)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.appendleft(2)
        self.assertIs(ll.first, node2)
        self.assertIs(ll.last, node1)

    def test_appendright(self):
        ll = dllist(xrange(4))
        ref = dllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = dllistnode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.prev, prev)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_guards_after_appendright(self):
        ll = dllist()
        node1 = ll.appendright(1)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.appendright(2)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node2)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.pop()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_guards_after_pop(self):
        ll = dllist([1, 2])
        ll.pop()
        self.assertIs(ll.first, ll.last)
        self.assertEqual(ll.first.value, 1)
        ll.pop()
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_guards_after_popleft(self):
        ll = dllist([1, 2])
        ll.popleft()
        self.assertIs(ll.first, ll.last)
        self.assertEqual(ll.first.value, 2)
        ll.popleft()
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_guards_after_popright(self):
        ll = dllist([1, 2])
        ll.pop()
        self.assertIs(ll.first, ll.last)
        self.assertEqual(ll.first.value, 1)
        ll.pop()
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_pop_from_empty_list(self):
        ll = dllist()
        self.assertRaises(ValueError, ll.pop)
        self.assertRaises(ValueError, ll.popleft)
        self.assertRaises(ValueError, ll.popright)

    def test_remove_from_empty_list(self):
        ll = dllist()
        self.assertRaises(ValueError, ll.remove, dllistnode())

    def test_remove_invalid_node(self):
        ll = dllist([1, 2, 3, 4])
        self.assertRaises(ValueError, ll.remove, dllistnode())

    def test_guards_after_remove(self):
        ll = dllist([1, 2])
        ll.remove(ll.last)
        self.assertIs(ll.first, ll.last)
        ll.remove(ll.first)
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_getitem(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        for idx in xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], dllistnode))
            self.assertEqual(ll[idx], ref[idx])
        for idx in xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], dllistnode))
            self.assertEqual(ll[-idx - 1], ref[-idx - 1])
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, len(ref))
        self.assertRaises(IndexError, ll.__getitem__, -len(ref) - 1)

    def test_getitem_empty(self):
        ll = dllist()
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, 0)
        self.assertRaises(IndexError, ll.__getitem__, -1)

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

    def test_guards_after_del(self):
        ll = dllist([1, 2])
        orig_last = ll.last
        del ll[0]
        self.assertIs(ll.first, orig_last)
        self.assertIs(ll.last, orig_last)
        del ll[0]
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_concat(self):
        a_ref = range(0, 1024, 4)
        a = dllist(a_ref)
        b_ref = range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(a_ref + b_ref)
        c = a + b
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))
        c = a + b_ref
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))

    def test_guards_after_concat(self):
        a = dllist([1, 2])
        b = dllist([3, 4])
        c = a + b
        self.assertIsNot(c.first, None)
        self.assertEqual(c.first.value, 1)
        self.assertIsNot(c.last, None)
        self.assertEqual(c.last.value, 4)

    def test_concat_empty(self):
        empty = dllist()
        filled_ref = range(0, 1024, 4)
        filled = dllist(filled_ref)
        res = empty + empty
        self.assertEqual(res, dllist([] + []))
        self.assertEqual(len(res), 0)
        res = empty + filled
        self.assertEqual(res, dllist([] + filled_ref))
        self.assertEqual(len(res), len(filled_ref))
        res = filled + empty
        self.assertEqual(res, dllist(filled_ref + []))
        self.assertEqual(len(res), len(filled_ref))

    def test_concat_inplace(self):
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
        b = dllist(b_ref)
        ab_ref = dllist(a_ref + b_ref)
        a = dllist(a_ref)
        a += b
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a += b_ref
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = dllist(a_ref)
        a += a
        self.assertEqual(a, dllist(a_ref + a_ref))
        self.assertEqual(len(a), len(ab_ref))

    def test_guards_after_concat_inplace(self):
        a = dllist([1, 2])
        b = dllist([3, 4])
        orig_a_first = a.first
        a += b
        self.assertIs(a.first, orig_a_first)
        self.assertEqual(a.first.value, 1)
        self.assertIsNot(a.last, None)
        self.assertEqual(a.last.value, 4)

    def test_guards_after_concat_inplace_of_self(self):
        ll = dllist([1, 2])
        orig_first = ll.first
        orig_last = ll.last
        ll += ll
        self.assertIs(ll.first, orig_first)
        self.assertEqual(ll.first.value, 1)
        self.assertIsNot(ll.last, None)
        self.assertIsNot(ll.last, orig_last)
        self.assertEqual(ll.last.value, 2)

    def test_concat_inplace_empty(self):
        filled_ref = range(0, 1024, 4)
        filled = dllist(filled_ref)
        empty = dllist()
        empty += empty
        self.assertEqual(empty, dllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = dllist()
        empty += filled
        self.assertEqual(empty, dllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = dllist()
        filled += empty
        self.assertEqual(filled, dllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_repeat(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        self.assertEqual(ll * 4, dllist(ref * 4))

    def test_guards_after_repeat(self):
        ll = dllist([1, 2])
        orig_first = ll.first
        orig_last = ll.last
        ll = ll * 4
        self.assertIsNot(ll.first, None)
        self.assertIsNot(ll.first, orig_first)
        self.assertIsNot(ll.last, None)
        self.assertIsNot(ll.last, orig_last)

    def test_repeat_empty(self):
        ll = dllist()
        self.assertEqual(ll * 4, dllist([] * 4))

    def test_repeat_inplace(self):
        ref = range(0, 1024, 4)
        ll = dllist(ref)
        ll *= 4
        self.assertEqual(ll, dllist(ref * 4))

    def test_guards_after_repeat_inplace(self):
        ll = dllist([1, 2])
        orig_first = ll.first
        orig_last = ll.last
        ll *= 4
        self.assertIs(ll.first, orig_first)
        self.assertIsNot(ll.last, None)
        self.assertIsNot(ll.last, orig_last)

    def test_repeat_inplace_empty(self):
        ll = dllist()
        ll *= 4
        self.assertEqual(ll, dllist([] * 4))

    def test_list_readonly_attributes(self):
        ll = dllist(range(4))
        self.assertRaises(AttributeError, setattr, ll, 'first', None)
        self.assertRaises(AttributeError, setattr, ll, 'last', None)
        self.assertRaises(AttributeError, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        ll = dllistnode()
        self.assertRaises(AttributeError, setattr, ll, 'prev', None)
        self.assertRaises(AttributeError, setattr, ll, 'next', None)

    def test_list_hash(self):
        self.assertEqual(hash(dllist()), hash(dllist()))
        self.assertEqual(hash(dllist(range(0, 1024, 4))),
            hash(dllist(range(0, 1024, 4))))
        self.assertEqual(hash(dllist([0, 2])), hash(dllist([0.0, 2.0])))


class testsllist(unittest.TestCase):

    def test_init_empty(self):
        ll = sllist()
        self.assertEqual(len(ll), 0)
        self.assertEqual(ll.size, 0)
        self.assertEqual(list(ll), [])
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_init_with_sequence(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        self.assertEqual(len(ll), len(ref))
        self.assertEqual(ll.size, len(ref))
        self.assertEqual(list(ll), ref)
        self.assertIsNot(ll.first, None)
        self.assertEqual(ll.first.value, 0)
        self.assertIsNot(ll.last, None)
        self.assertEqual(ll.last.value, 1020)

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

    def test_node_repr(self):
        a = sllist([None]).first
        self.assertEqual(repr(a), '<sllistnode(None)>')
        b = sllist([1, None]).first
        self.assertEqual(repr(b), '<sllistnode(1)>')
        c = sllist(['abc', None]).first
        self.assertEqual(repr(c), '<sllistnode(\'abc\')>')

    def test_value_change(self):
        a = sllist([1, 2, 3])
        a.first.next.value = 5
        self.assertEqual(a[0], 1)
        self.assertEqual(a[1], 5)
        self.assertEqual(a[2], 3)

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

    def test_nodeat(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        for idx in xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), sllistnode))
            self.assertEqual(ll.nodeat(idx).value, ref[idx])
        for idx in xrange(len(ll)):
            self.assertTrue(isinstance(ll.nodeat(idx), sllistnode))
            self.assertEqual(ll.nodeat(-idx - 1).value, ref[-idx - 1])
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, len(ref))
        self.assertRaises(IndexError, ll.nodeat, -len(ref) - 1)

    def test_nodeat_empty(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.nodeat, None)
        self.assertRaises(TypeError, ll.nodeat, 'abc')
        self.assertRaises(IndexError, ll.nodeat, 0)
        self.assertRaises(IndexError, ll.nodeat, -1)

    def test_iter(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        idx = 0
        for val in ll:
            self.assertFalse(isinstance(val, sllistnode))
            self.assertEqual(val, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iternodes(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        idx = 0
        for node in ll.iternodes():
            self.assertTrue(isinstance(node, sllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iternext_to(self, terminator_index=200):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        terminator = ll.nodeat(terminator_index)
        original_idx = idx = 100
        for node in ll.nodeat(idx).iternext(to=terminator):
            self.assertTrue(isinstance(node, sllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1
        if terminator_index == original_idx:
            #self.assertRaises(UnboundLocalError, node)
            self.assertEqual(idx, terminator_index)
        elif terminator_index < original_idx:
            self.assertEqual(node.value, 1020)
            self.assertEqual(idx, 256)
        else:
            self.assertEqual(node.value, (terminator_index-1)*4)
            self.assertEqual(idx, terminator_index)

    def test_iternext_to_preceding_idx(self):
        self.test_iternext_to(terminator_index=50)

    def test_iternext_to_equal_idx(self):
        self.test_iternext_to(terminator_index=100)

    def test_iternext(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        idx = 100
        for node in ll.nodeat(100).iternext():
            self.assertTrue(isinstance(node, sllistnode))
            self.assertEqual(node.value, ref[idx])
            idx += 1
        self.assertEqual(idx, len(ref))

    def test_iter_empty(self):
        ll = sllist()
        count = 0
        for val in ll:
            count += 1
        self.assertEqual(count, 0)

    def test_iter_empty_nodes(self):
        ll = sllist()
        count = 0
        for val in ll.iternodes():
            count += 1
        self.assertEqual(count, 0)

    def test_reversed(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        idx = len(ref) - 1
        for val in reversed(ll):
            self.assertFalse(isinstance(val, sllistnode))
            self.assertEqual(val, ref[idx])
            idx -= 1
        self.assertEqual(idx, -1)

    def test_reversed_empty(self):
        ll = sllist()
        count = 0
        for val in reversed(ll):
            count += 1
        self.assertEqual(count, 0)

    def test_insert_value_after_last(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = sllistnode(10)
        new_node = ll.insert(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(new_node, ll.last)
        self.assertEqual(ll, ref)

    def test_insert_value_before(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 10, 2, 3])
        prev = ll.nodeat(1)
        next = ll.nodeat(2)
        arg_node = sllistnode(10)
        new_node = ll.insert(arg_node, ll.nodeat(2))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll, ref)

    def test_insert_value_before_first(self):
        ll = sllist(xrange(4))
        ref = sllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = sllistnode(10)
        new_node = ll.insert(arg_node, ll.nodeat(0))
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(new_node, ll.first)
        self.assertEqual(ll, ref)

    def test_guards_after_insert(self):
        ll = sllist()
        node1 = ll.insert(sllistnode(1))
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.insert(sllistnode(2))
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node2)

    def test_insert_invalid_ref(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.insert, 10, 1)
        self.assertRaises(TypeError, ll.insert, 10, 'abc')
        self.assertRaises(TypeError, ll.insert, 10, [])
        self.assertRaises(ValueError, ll.insert, 10, sllistnode())

    def test_guards_after_insertafter(self):
        ll = sllist([1])
        orig_first = ll.first
        node = ll.insertafter(ll.last, sllistnode(2))
        self.assertIs(ll.first, orig_first)
        self.assertIs(ll.last, node)

    def test_guards_after_insertbefore(self):
        ll = sllist([1])
        orig_last = ll.last
        node = ll.insertbefore(ll.first, sllistnode(2))
        self.assertIs(ll.first, node)
        self.assertIs(ll.last, orig_last)

    def test_append(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = sllistnode(10)
        new_node = ll.append(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_guards_after_append(self):
        ll = sllist()
        node1 = ll.append(1)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.append(2)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node2)

    def test_appendleft(self):
        ll = sllist(xrange(4))
        ref = sllist([10, 0, 1, 2, 3])
        next = ll.nodeat(0)
        arg_node = sllistnode(10)
        new_node = ll.appendleft(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, next)
        self.assertEqual(ll.first, new_node)
        self.assertEqual(ll, ref)

    def test_guards_after_appendleft(self):
        ll = sllist()
        node1 = ll.appendleft(1)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.appendleft(2)
        self.assertIs(ll.first, node2)
        self.assertIs(ll.last, node1)

    def test_appendright(self):
        ll = sllist(xrange(4))
        ref = sllist([0, 1, 2, 3, 10])
        prev = ll.nodeat(-1)
        arg_node = sllistnode(10)
        new_node = ll.appendright(arg_node)
        self.assertNotEqual(new_node, arg_node)
        self.assertEqual(new_node.value, 10)
        self.assertEqual(new_node.next, None)
        self.assertEqual(prev.next, new_node)
        self.assertEqual(ll.last, new_node)
        self.assertEqual(ll, ref)

    def test_guards_after_appendright(self):
        ll = sllist()
        node1 = ll.appendright(1)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node1)
        node2 = ll.appendright(2)
        self.assertIs(ll.first, node1)
        self.assertIs(ll.last, node2)

    def test_pop(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.pop()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_guards_after_pop(self):
        ll = sllist([1, 2])
        ll.pop()
        self.assertIs(ll.first, ll.last)
        self.assertEqual(ll.first.value, 1)
        ll.pop()
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_popleft(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.popleft()
        self.assertEqual(result, ref[0])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.first.value, ref[1])
        self.assertEqual(list(ll), ref[1:])

    def test_guards_after_popleft(self):
        ll = sllist([1, 2])
        ll.popleft()
        self.assertIs(ll.first, ll.last)
        self.assertEqual(ll.first.value, 2)
        ll.popleft()
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_popright(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        result = ll.popright()
        self.assertEqual(result, ref[-1])
        self.assertEqual(len(ll), len(ref) - 1)
        self.assertEqual(ll.size, len(ref) - 1)
        self.assertEqual(ll.last.value, ref[-2])
        self.assertEqual(list(ll), ref[:-1])

    def test_guards_after_popright(self):
        ll = sllist([1, 2])
        ll.pop()
        self.assertIs(ll.first, ll.last)
        self.assertEqual(ll.first.value, 1)
        ll.pop()
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_pop_from_empty_list(self):
        ll = sllist()
        self.assertRaises(ValueError, ll.pop)
        self.assertRaises(ValueError, ll.popleft)
        self.assertRaises(ValueError, ll.popright)

    def test_remove_from_empty_list(self):
        ll = sllist()
        self.assertRaises(ValueError, ll.remove, sllistnode())

    def test_remove_invalid_node(self):
        ll = sllist([1, 2, 3, 4])
        self.assertRaises(ValueError, ll.remove, sllistnode())

    def test_guards_after_remove(self):
        ll = sllist([1, 2])
        ll.remove(ll.last)
        self.assertIs(ll.first, ll.last)
        ll.remove(ll.first)
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_getitem(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        for idx in xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], sllistnode))
            self.assertEqual(ll[idx], ref[idx])
        for idx in xrange(len(ll)):
            self.assertFalse(isinstance(ll[idx], sllistnode))
            self.assertEqual(ll[-idx - 1], ref[-idx - 1])
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, len(ref))
        self.assertRaises(IndexError, ll.__getitem__, -len(ref) - 1)

    def test_getitem_empty(self):
        ll = sllist()
        self.assertRaises(TypeError, ll.__getitem__, None)
        self.assertRaises(TypeError, ll.__getitem__, 'abc')
        self.assertRaises(IndexError, ll.__getitem__, 0)
        self.assertRaises(IndexError, ll.__getitem__, -1)

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

    def test_guards_after_del(self):
        ll = sllist([1, 2])
        orig_last = ll.last
        del ll[0]
        self.assertIs(ll.first, orig_last)
        self.assertIs(ll.last, orig_last)
        del ll[0]
        self.assertIs(ll.first, None)
        self.assertIs(ll.last, None)

    def test_concat(self):
        a_ref = range(0, 1024, 4)
        a = sllist(a_ref)
        b_ref = range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(a_ref + b_ref)
        c = a + b
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))
        c = a + b_ref
        self.assertEqual(c, ab_ref)
        self.assertEqual(len(c), len(ab_ref))

    def test_guards_after_concat(self):
        a = sllist([1, 2])
        b = sllist([3, 4])
        c = a + b
        self.assertIsNot(c.first, None)
        self.assertEqual(c.first.value, 1)
        self.assertIsNot(c.last, None)
        self.assertEqual(c.last.value, 4)

    def test_concat_empty(self):
        empty = sllist()
        filled_ref = range(0, 1024, 4)
        filled = sllist(filled_ref)
        res = empty + empty
        self.assertEqual(res, sllist([] + []))
        self.assertEqual(len(res), 0)
        res = empty + filled
        self.assertEqual(res, sllist([] + filled_ref))
        self.assertEqual(len(res), len(filled_ref))
        res = filled + empty
        self.assertEqual(res, sllist(filled_ref + []))
        self.assertEqual(len(res), len(filled_ref))

    def test_concat_inplace(self):
        a_ref = range(0, 1024, 4)
        b_ref = range(8092, 8092 + 1024, 4)
        b = sllist(b_ref)
        ab_ref = sllist(a_ref + b_ref)
        a = sllist(a_ref)
        a += b
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a += b_ref
        self.assertEqual(a, ab_ref)
        self.assertEqual(len(a), len(ab_ref))
        a = sllist(a_ref)
        a += a
        self.assertEqual(a, sllist(a_ref + a_ref))
        self.assertEqual(len(a), len(ab_ref))

    def test_guards_after_concat_inplace(self):
        a = sllist([1, 2])
        b = sllist([3, 4])
        orig_a_first = a.first
        a += b
        self.assertIs(a.first, orig_a_first)
        self.assertEqual(a.first.value, 1)
        self.assertIsNot(a.last, None)
        self.assertEqual(a.last.value, 4)

    def test_guards_after_concat_inplace_of_self(self):
        ll = sllist([1, 2])
        orig_first = ll.first
        orig_last = ll.last
        ll += ll
        self.assertIs(ll.first, orig_first)
        self.assertEqual(ll.first.value, 1)
        self.assertIsNot(ll.last, None)
        self.assertIsNot(ll.last, orig_last)
        self.assertEqual(ll.last.value, 2)

    def test_concat_inplace_empty(self):
        filled_ref = range(0, 1024, 4)
        filled = sllist(filled_ref)
        empty = sllist()
        empty += empty
        self.assertEqual(empty, sllist([] + []))
        self.assertEqual(len(empty), 0)
        empty = sllist()
        empty += filled
        self.assertEqual(empty, sllist([] + filled_ref))
        self.assertEqual(len(empty), len(filled_ref))
        empty = sllist()
        filled += empty
        self.assertEqual(filled, sllist(filled_ref + []))
        self.assertEqual(len(filled), len(filled_ref))

    def test_repeat(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        self.assertEqual(ll * 4, sllist(ref * 4))

    def test_guards_after_repeat(self):
        ll = sllist([1, 2])
        orig_first = ll.first
        orig_last = ll.last
        ll = ll * 4
        self.assertIsNot(ll.first, None)
        self.assertIsNot(ll.first, orig_first)
        self.assertIsNot(ll.last, None)
        self.assertIsNot(ll.last, orig_last)

    def test_repeat_empty(self):
        ll = sllist()
        self.assertEqual(ll * 4, sllist([] * 4))

    def test_repeat_inplace(self):
        ref = range(0, 1024, 4)
        ll = sllist(ref)
        ll *= 4
        self.assertEqual(ll, sllist(ref * 4))

    def test_guards_after_repeat_inplace(self):
        ll = sllist([1, 2])
        orig_first = ll.first
        orig_last = ll.last
        ll *= 4
        self.assertIs(ll.first, orig_first)
        self.assertIsNot(ll.last, None)
        self.assertIsNot(ll.last, orig_last)

    def test_repeat_inplace_empty(self):
        ll = sllist()
        ll *= 4
        self.assertEqual(ll, sllist([] * 4))

    def test_list_readonly_attributes(self):
        ll = sllist(range(4))
        self.assertRaises(AttributeError, setattr, ll, 'first', None)
        self.assertRaises(AttributeError, setattr, ll, 'last', None)
        self.assertRaises(AttributeError, setattr, ll, 'size', None)

    def test_node_readonly_attributes(self):
        ll = sllistnode()
        self.assertRaises(AttributeError, setattr, ll, 'next', None)

    def test_list_hash(self):
        self.assertEqual(hash(sllist()), hash(sllist()))
        self.assertEqual(hash(sllist(range(0, 1024, 4))),
            hash(sllist(range(0, 1024, 4))))
        self.assertEqual(hash(sllist([0, 2])), hash(sllist([0.0, 2.0])))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testdllist))
    suite.addTest(unittest.makeSuite(testsllist))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
