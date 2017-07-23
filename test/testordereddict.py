# coding: utf-8

from __future__ import print_function

if __name__ != "__main__":
    import py
import string
import os
import sys
import random
if sys.version_info < (3,):
    import cPickle

py3 = sys.version_info >= (3,)

from ruamel.ordereddict import ordereddict, sorteddict

all_lowercase = 'abcdefghijklmnopqrstuvwxyz'
all_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class TestOrderedDict(object):
    def __init__(self, nopytest=False):
        self.nopytest = nopytest

    def setup_method(self, method):
        self.x = ordereddict()
        self.x['a'] = 1
        self.x['b'] = 2
        self.x['c'] = 3
        self.x['d'] = 4
        self.z = ordereddict()
        for index, ch in enumerate(all_lowercase):
            self.z[ch] = index
        self.e = ordereddict()
        self.part = ordereddict((('f', 5),('g', 6),('h', 7),('i', 8), ('j', 9)))
        #self.revpart = ordereddict((('j', 9),('g', 6),('i', 8),('h', 7), ('f', 5)))
        self.upperlower = ordereddict([('A', 1), ('a', 2), ('B', 4), ('b', 4)])

    def test_od_setitems(self):
        r = self.z
        r.setitems([('f', 5),('g', 6),('h', 7),('i', 8), ('j', 9)])
        assert r == self.part

    def test_sd_init_from_seq(self):
        r = sorteddict((('j', 9),('g', 6),('i', 8),('h', 7), ('f', 5)))
        assert r == self.part

    def test_sd_setitems(self):
        r = sorteddict()
        r['b'] = 1
        r['c'] = 2
        r['d'] = 3
        r['f'] = 5
        r['g'] = 6
        r['h'] = 7
        r['i'] = 8
        r['a'] = 0
        r['j'] = 9
        r['l'] = 11
        r['k'] = 10
        r['m'] = 12
        r['n'] = 13
        r['o'] = 14
        r['p'] = 15
        r['q'] = 16
        r['s'] = 18
        r['v'] = 21
        r['w'] = 22
        r['x'] = 23
        r['y'] = 24
        r['z'] = 25
        r['e'] = 4
        r['r'] = 17
        r['t'] = 19
        r['u'] = 20
        assert r == self.z

    def test_sorted_from_ordered(self):
        if py3:
            return
        i = self.z.items(reverse=True)
        random.shuffle(i)
        i = ordereddict(i)
        sd = sorteddict(i)
        assert sd == self.z

    def test_len(self):
        assert len(self.z) == len(all_lowercase)
        assert len(self.e) == 0

    def test_brackets(self):
        assert self.x['b'] == 2

    def test_del(self):
        self.x['1234'] = 1234
        del self.x['1234']
        assert self.x.get('1234') is None

    def test_clear(self):
        x = ordereddict()
        x['a'] = 1
        x['b'] = 2
        x['c'] = 3
        x['d'] = 4
        assert len(x) == 4
        x.clear()
        assert len(x) == 0

    def test_copy(self):
        x = self.x.copy()
        assert len(x) == 4
        assert x['c'] == 3
        x['c'] = 4
        assert self.x['c'] == 3

    def test_sd_copy(self):
        x1 = sorteddict(self.z)
        x = x1.copy()
        assert len(x) == 26
        assert x['c'] == 2
        x['c'] = 4
        assert self.x['c'] == 3
        assert x['c'] == 4

    def test_sd_lower(self):
        if py3:
            return
        r = sorteddict(self.upperlower)
        assert r != self.upperlower
        assert r.index('a') == 2
        rl = sorteddict(self.upperlower, key=string.lower)
        assert rl == self.upperlower

    def test_in(self):
        assert 'c' in self.z

    def test_not_in(self):
        assert 'C' not in self.z

    if not py3:
        def test_has_key(self):
            assert self.z.has_key('z')

    def test_items(self):
        "unlikely to function in a non-ordered dictionary"
        index = 0
        for index, y in enumerate(self.z.items()):
            assert all_lowercase[index] == y[0]
            assert index == y[1]

    def test_items_rev(self):
        if py3:
            return
        for index, y in enumerate(self.z.items(reverse=True)):
            i = 25 - index
            assert all_lowercase[i] == y[0]
            assert i == y[1]

    def test_keys(self):
        "unlikely to function in a non-ordered dictionary"
        index = 0
        for y in self.z.keys():
            assert self.z[y] == index
            index += 1

    def test_keys_rev(self):
        "unlikely to function in a non-ordered dictionary"
        if py3:
            return
        index = 25
        for y in self.z.keys(reverse=True):
            assert all_lowercase[index] == y
            index -= 1


    def test_update(self):
        if py3:
            return
        y = ordereddict()
        y[1] = 'x'
        y['b'] = 'abc'
        y[3] = 'xx'
        y.update(self.x)
        assert len(y) == 6
        assert y.values()[1] == self.x.values()[1]
        assert y.values()[3] == self.x.values()[0]
        assert y.values()[4] == self.x.values()[2]
        assert y.values()[5] == self.x.values()[3]

    def test_sd_fromkeys(self):
        x = sorteddict.fromkeys([1,2,3,4,5,6])
        assert len(x) == 6
        assert x[6] is None
        x = sorteddict.fromkeys((1,2,3,4,5), 'abc')
        assert len(x) == 5
        assert x[5] == 'abc'

    def test_fromkeys(self):
        if py3:
            return
        x = ordereddict.fromkeys([1,2,3,4,5,6])
        assert len(x) == 6
        assert x[6] is None
        x = ordereddict.fromkeys((1,2,3,4,5), 'abc')
        assert len(x) == 5
        assert x[5] == 'abc'
        print(x.keys())
        assert x.keys() == [1,2,3,4,5]

    def test_values(self):
        "unlikely to function in a non-ordered dictionary"
        index = 0
        for y in self.z.values():
            assert y == index
            index += 1

    def test_values_rev(self):
        if py3:
            return
        index = 25
        for y in self.z.values(reverse=True):
            assert y == index
            index -= 1

    def test_get1(self):
        assert self.x.get('b') == 2

    def test_get2(self):
        assert self.x.get('A') is None

    def test_get3(self):
        assert self.x.get('A', 'abc') == 'abc'

    def test_dict3(self):
        assert self.x.get('B', 'hello') == "hello"

    def test_setdefault(self):
        y = self.x.copy()
        res = y.setdefault('c', 42)
        assert res == 3
        assert y['c'] == 3
        res = y.setdefault('ab', 42)
        assert res == 42
        assert y['ab'] == 42

    def test_pop(self):
        y = self.x.copy()
        assert y.pop('b') == 2
        assert y.pop('y', 42) == 42
        assert len(y) == 3
        if not self.nopytest:
            py.test.raises(KeyError, "y.pop('x')")

    def test_popitem(self):
        y = self.x.copy()
        assert y.popitem() == ('d', 4)
        assert y.popitem(1) == ('b', 2)
        assert y.popitem(-2) == ('a', 1)
        if not self.nopytest:
            py.test.raises(KeyError, "y.popitem(1)")


###################

    def test_deepcopy(self):
        if sys.version_info < (3,):
            import copy
        else:
            return
            import copy3
        y = self.x.copy()
        z = self.x.copy()
        y['r'] = z
        dc = copy.deepcopy(y)
        assert y['r']['d'] == 4
        y['r']['d'] = 5
        assert y['r']['d'] == 5
        assert dc['r']['d'] == 4


    def test_init1(self):
        y = ordereddict(self.x)
        y['b'] = 42
        assert self.x['b'] == 2
        assert y['c'] == 3
        assert y['b'] == 42

    def test_init2(self):
        a = {'a': 1}
        if not self.nopytest:
            py.test.raises(TypeError, "y = ordereddict(a)")

    def test_init3(self):
        y = ordereddict([('a',1), ('b',2), ('c',3), ('d', 4)])
        assert y == self.x

    def test_compare_wrong_order(self):
        y = ordereddict([('a',1), ('b',2), ('d',4), ('c', 3)])
        assert y != self.x

    def test_compare_wrong_value(self):
        y = ordereddict([('a',1), ('b',2), ('c',4), ('d', 3)])
        assert y != self.x

    def test_compare(self):
        y = ordereddict([('a',1), ('b',2), ('c',3), ('d', 4)])
        assert y == self.x

    def test_index(self):
        assert self.x.index('c') == 2
        if not self.nopytest:
            py.test.raises(ValueError, "self.x.index('1')")


###################

    def test_dict4(self):
        self.walk('b', 2)

    def test_dict5(self):
        if not self.nopytest:
            py.test.raises(KeyError, "self.walk('ba', 999)")

    def walk(self, key, val):
        for y in self.x:
            if y == key:
                assert self.x[y] == val
                break
        else:
            raise KeyError

    def test_walk_ordereddict(self):
        index = 0
        for y in self.z:
            assert self.z[y] == index
            index += 1

    if not py3:
        def test_iterkeys(self):
            index = 0
            for y in self.z.iterkeys():
                assert all_lowercase[index] == y
                index += 1
            assert index == 26

        def test_iterkeys_rev(self):
            index = 0
            for y in self.z.iterkeys(reverse=True):
                assert all_lowercase[25 - index] == y
                index += 1
            assert index == 26

        def test_iterkeys_iterator(self):
            tmp = self.z.iterkeys()
            assert tmp.__length_hint__() == 26

        def test_iter(self):
            res = ""
            for y in self.z:
                res += y
            assert all_lowercase == res

        def test_itervalues(self):
            index = 0
            for index, y in enumerate(self.z.itervalues()):
                assert index == y

        def test_itervalues_rev(self):
            index = 0
            for y in self.z.itervalues(reverse=True):
                assert 25 - index == y
                index += 1
            assert index == 26

        def test_iteritems(self):
            index = 0
            for index, y in enumerate(self.z.iteritems()):
                assert all_lowercase[index] == y[0]
                assert index == y[1]

        def test_iteritems_rev(self):
            index = 0
            for y in self.z.iteritems(reverse=True):
                assert all_lowercase[25-index] == y[0]
                assert 25 - index == y[1]
                index += 1
            assert index == 26


    def test_repr(self):
        d = ordereddict()
        assert repr(d) == 'ordereddict([])'
        d['a'] = 1
        assert repr(d) == "ordereddict([('a', 1)])"
        d[2] = 'b'
        assert repr(d) == "ordereddict([('a', 1), (2, 'b')])"


    def test_insert_newitem(self):
        if py3:
            return
        r = self.x.copy()
        r.insert(3, 'ca', 8)
        assert r.index('ca') == 3
        assert r.get('ca') == 8
        assert len(r) == 5

    def test_insert_existing_key_sameplace(self):
        if py3:
            return
        r = self.z
        pos = r.index('k')
        r.insert(pos, 'k', 42)
        assert r.index('k') == pos
        assert r.get('k') == 42
        assert len(r) == len(all_lowercase)

    def test_reverse(self):
        if py3:
            return
        r = self.z
        r.reverse()
        res = []
        for index, ch in enumerate(all_lowercase):
            assert r[ch] == index
            res.insert(0, ch)
        assert res == r.keys()

    def test_consequitive_slice(self):
        r = self.z
        assert r[5:10] == self.part
        assert r[-2:] == ordereddict([('y', 24),('z', 25)])
        assert r[-4:-2] == ordereddict([('w', 22),('x', 23)])
        assert r[:] == self.z

    def test_slice(self):
        r = self.z
        rp = self.part.copy()
        rp.reverse()
        assert r[9:4:-1] == rp
        assert r[5:25:5] == ordereddict([('f', 5), ('k', 10), ('p', 15), ('u', 20)])

    def test_del_consequitive_slice(self):
        r = self.z
        del r[3:24]
        assert r == ordereddict([('a', 0), ('b', 1), ('c', 2), ('y', 24), ('z', 25)])

    def test_del_non_consequitive_slice(self):
        r = self.z
        del r[4:24:2]
        t = ordereddict()
        for index, ch in enumerate(all_lowercase):
            if ch not in 'abcdfhjlnprtvxyz':
                continue
            t[ch] = index
        #print r
        #print t
        assert r == t

    def test_sd_slice(self):
        r = sorteddict(self.z)
        #print r
        y = r[3:6]
        #print y
        assert y['d'] == 3
        assert y['e'] == 4
        assert y['f'] == 5

    def test_sd_del_consequitive_slice(self):
        r = sorteddict(self.z)
        if not self.nopytest:
            py.test.raises(TypeError, "del r[3:24]")

    def test_sd_del_non_consequitive_slice(self):
        r = sorteddict(self.z)
        if not self.nopytest:
            py.test.raises(TypeError, "del r[4:24:2]")

    def test_del_rev_non_consequitive_slice(self):
        r = self.z
        del r[22:3:-2]
        t = ordereddict()
        for index, ch in enumerate(all_lowercase):
            if ch not in 'abcdfhjlnprtvxyz':
                continue
            t[ch] = index
        #print r
        #print t
        assert r == t

    def test_ass_consequitive_slice_wrong_size(self):
        r = self.z
        if not self.nopytest:
            py.test.raises(ValueError, "r[10:15] = ordereddict([(1, 0), (2, 1), (3, 2),])")

    def test_ass_consequitive_slice_wrong_type(self):
        r = self.z
        if not self.nopytest:
            py.test.raises(TypeError, "r[10:15] = dict([(1, 0), (2, 1), (3, 2),  (4, 24), (5, 25)])")

    if sys.version_info < (3,):
        def test_ass_consequitive_slice(self):
            r = self.z
            r[10:15] = ordereddict([(1, 0), (2, 1), (3, 2), (4, 24), (5, 25)])
            assert r[9:16] == ordereddict([('j', 9), (1, 0), (2, 1), (3, 2),
                                           (4, 24), (5, 25), ('p', 15)])

        def test_sd_ass_consequitive_slice(self):
            r = sorteddict(self.z)
            if not self.nopytest:
                py.test.raises(TypeError,
                "r[10:15] = ordereddict([(1, 0), (2, 1), (3, 2), (4, 24), (5, 25)])")


        def test_ass_non_consequitive_slice_wrong_size(self):
            r = self.z
            if not self.nopytest:
                py.test.raises(ValueError, "r[10:20:2] = ordereddict([(1, 0), (2, 1), (3, 2),])")

        def test_ass_non_consequitive_slice_wrong_type(self):
            r = self.z
            if not self.nopytest:
                py.test.raises(TypeError, "r[10:20:2] = dict([(1, 0), (2, 1), (3, 2),  (4, 24), (5, 25)])")

        def test_ass_non_consequitive_slice(self):
            r = self.z
            r[10:15:2] = ordereddict([(1, 0), (2, 1), (3, 2),])
            #print r[9:16]
            #print ordereddict([('j', 9), (1, 0), ('l', 11), (2, 1),
            #                               ('n', 13), (3, 2), ('p', 15)])
            assert r[9:16] == ordereddict([('j', 9), (1, 0), ('l', 11), (2, 1),
                                           ('n', 13), (3, 2), ('p', 15)])

        def test_sd_ass_non_consequitive_slice(self):
            r = sorteddict(self.z)
            if not self.nopytest:
                py.test.raises(TypeError, "r[10:15:2] = ordereddict([(1, 0), (2, 1), (3, 2),])")

        def test_ass_reverse_non_consequitive_slice(self):
            r = self.z
            r[14:9:-2] = ordereddict([(3, 2), (2, 1), (1, 0),])
            assert len(r) == 26
            #print r[9:16]
            #print ordereddict([('j', 9), (1, 0), ('l', 11), (2, 1),
            #                               ('n', 13), (3, 2), ('p', 15)])
            assert r[9:16] == ordereddict([('j', 9), (1, 0), ('l', 11), (2, 1),
                                           ('n', 13), (3, 2), ('p', 15)])


    def test_rename(self):
        if py3:
            return
        self.x.rename('c', 'caaa')
        assert self.x == ordereddict([('a',1), ('b',2), ('caaa',3), ('d', 4)])

    def test_sd_rename(self):
        x = sorteddict(self.x)
        if not self.nopytest:
            py.test.raises(TypeError, "x.rename('c', 'caaa')")


    def test_setvalues(self):
        r1 = self.z[:5]
        r2 = self.z[:5]
        for k in r1:
            r1[k] = r1[k] + 100
        r2.setvalues([100, 101, 102, 103, 104])
        assert r1 == r2
        if not self.nopytest:
            py.test.raises(ValueError, "r2.setvalues([100, 101, 102, 103])")
            py.test.raises(ValueError, "r2.setvalues([100, 101, 102, 103, 104, 105])")
        # we don't know length upfront
        r2.setvalues((x for x in [100, 101, 102, 103, 104]))
        if not self.nopytest:
            py.test.raises(ValueError, "r2.setvalues((x for x in [100, 101, 102, 103]))")
            py.test.raises(ValueError, "r2.setvalues((x for x in [100, 101, 102, 103, 104, 105]))")

    def test_setkeys(self):
        self.x[42] = 'abc'
        r1 = self.x.copy()
        r2 = ordereddict([('d', 4), ('c', 3), ('a', 1), (42, 'abc'), ('b', 2),])
        r1.setkeys(('d', 'c', 'a', 42, 'b',))
        assert r1 == r2
        if not self.nopytest:
            py.test.raises(KeyError, "r1.setkeys(('d', 'e', 'a', 42, 'b',))")
            py.test.raises(KeyError, "r1.setkeys(('d', 42, 'a', 42, 'b',))")
            py.test.raises(ValueError, "r1.setkeys(('d', 'c', 'a', 42, 'b', 'a',))")
            py.test.raises(ValueError, "r1.setkeys(('g', 'c', 'a', 42,))")

    def test_sd_setkeys(self):
        x = sorteddict.fromkeys((1,2,3,4,5), 'abc')
        if not self.nopytest:
            py.test.raises(TypeError, "x.setkeys((5, 3, 1, 2, 4,))")

    def test_setitems(self):
        r = self.z
        r.setitems([('f', 5),('g', 6),('h', 7),('i', 8), ('j', 9)])
        assert r == self.part

    def test_insert_existing_key_before(self):
        if py3:
            return
        r = self.z
        pos = r.index('k')
        r.insert(pos-3, 'k', 42)
        assert r.index('k') == pos - 3
        assert r.get('k') == 42
        assert len(r) == len(all_lowercase)

    def test_insert_existing_key_after(self):
        if py3:
            return
        r = self.z
        pos = r.index('k')
        r.insert(pos+3, 'k', 42)
        assert r.index('k') == pos + 3
        assert r.get('k') == 42
        assert len(r) == len(all_lowercase)

    def test_insert_existing_non_last_key_beyond(self):
        if py3:
            return
        r = self.z
        pos = r.index('y')
        pos += 1
        r.insert(pos, 'y', 42)
        assert r.index('y') == pos
        assert r.get('y') == 42
        assert len(r) == len(all_lowercase)

    def test_insert_existing_last_key_at_end(self):
        if py3:
            return
        r = self.z
        pos = r.index('z')
        r.insert(pos, 'z', 42)
        assert r.index('z') == pos
        assert r.get('z') == 42
        assert len(r) == len(all_lowercase)

    def test_insert_existing_last_key_beyond_end(self):
        if py3:
            return
        r = self.z
        pos = r.index('z')
        r.insert(pos + 1, 'z', 42)
        assert r.index('z') == pos
        assert r.get('z') == 42
        assert len(r) == len(all_lowercase)

    def test_insert_range(self):
        if py3:
            return
        r = ordereddict()
        r['c'] = 3
        r.insert(0, 'b', 2)
        r.insert(-10, 'a', 1)
        r.insert(3, 'd', 4)
        r.insert(10, 'e', 5)
        self.x['e'] = 5
        assert r == self.x

    def test_pickle(self):
        if py3:
            return
        fname = 'tmpdata.pkl'
        r = self.z.copy()
        r[(1,2)] = self.x
        fp = open(fname, 'wb')
        cPickle.dump(r, fp)
        fp.close()
        s = cPickle.load(open(fname, 'rb'))
        assert s == r
        os.remove(fname)

    def test_pickle_kvio(self):
        if py3:
            return
        fname = 'tmpdata.pkl'
        r = ordereddict(self.z, kvio=True)
        fp = open(fname, 'wb')
        cPickle.dump(r, fp)
        fp.close()
        s = cPickle.load(open(fname, 'rb'))
        assert s == r
        r['k'] = 42
        s['k'] = 42
        assert s == r
        os.remove(fname)


    def test_sd_pickle(self):
        if py3:
            return
        fname = 'tmpdata.pkl'
        r = sorteddict(self.z)
        fp = open(fname, 'wb')
        cPickle.dump(r, fp)
        fp.close()
        s = cPickle.load(open(fname, 'rb'))
        assert s == r
        s['k'] = 10
        assert s == self.z
        os.remove(fname)


    def test_kvio1(self):
        r = ordereddict(kvio=True)
        r.update(self.x)
        r['b']=42
        assert r == ordereddict([('a', 1), ('c', 3), ('d', 4), ('b', 42)])

    def test_kvio2(self):
        r = ordereddict(kvio=True)
        r.update(self.x)
        r['b']=2
        assert r != self.x
        r.update([('c', 3), ('d', 4)])
        assert r == self.x

    def test_kvio_copy(self):
        r = ordereddict(kvio=True)
        r.update(self.x)
        r['b']=2
        r1 = r.copy()
        assert r1 != self.x
        r1.update([('c', 3), ('d', 4)])
        assert r1 == self.x

    def test_relax(self):
        if py3:
            return
        nd = dict(z=1,y=2,w=3,v=4,x=5)
        if not self.nopytest:
            py.test.raises(TypeError, "r = ordereddict(nd)")
        r = ordereddict(nd, relax=True)
        assert nd.keys() == r.keys()
        assert nd.values() == r.values()

    def test_relax_class(self):
        if py3:
            return
        class relaxed_ordereddict(ordereddict):
            def __init__(self, *args, **kw):
                kw['relax'] = True
                ordereddict.__init__(self, *args, **kw)

        nd = dict(z=1,y=2,w=3,v=4,x=5)
        r = relaxed_ordereddict(nd)
        assert nd.keys() == r.keys()
        assert nd.values() == r.values()


    def test_relax_update(self):
        d = ordereddict()
        nd = dict(z=1,y=2,w=3,v=4,x=5)
        if not self.nopytest:
            py.test.raises(TypeError, "d.update(nd)")
        d.update(nd, relax=True)
        assert len(d) == 5

    def _test_order(self):
        nd = dict(z=1,y=2,w=3,v=4,x=5)
        r = ordereddict(nd, key=True)
        assert nd.keys() == r.keys()
        assert nd.values() == r.values()

    def test_subclass_sorted(self): # found thanks to Sam Pointon
        if py3:
            return

        class SD(sorteddict):
            pass
        s = SD({0: 'foo', 2: 'bar'})
        s[1] = 'abc'
        #print s.items()
        assert s.items() == [(0, 'foo'), (1, 'abc'), (2, 'bar')]

    def test_subclass_sorted_repr(self): # found thanks to Sam Pointon
        if py3:
            return
        class SD(sorteddict):
            pass
        s = SD({0: 'foo', 2: 'bar'})
        x = repr(s)
        assert x == "sorteddict([(0, 'foo'), (2, 'bar')])"

    def test_deepcopy2(self): # found thanks to Alexandre Andrade
        if sys.version_info < (3,):
            import copy
        else:
            return
            import copy3
        import gc
        d = ordereddict([(1, 2)])
        gc.collect()
        none_refcount = sys.getrefcount(None)
        for i in xrange(10):
            copy.deepcopy(d)
            gc.collect()
        assert none_refcount == sys.getrefcount(None)

    # this failed
    def test_multiple_inserts_then_deletes(self):
        if py3:
            return
        d = ordereddict()

        for i in range(1,6):
            d.insert(i-1, i, 'a')

        for i in range(1,6):
            del d[i]

        d.insert(0, 0, 'will this crash?')
        #print d.items()

    # this failed
    def test_repeated_add_delete(self):
        d = ordereddict()
        for el in range(0,9):
            d[el]=el
            del d[el]


#############################

    def _test_alloc_many(self):
        res = []
        times = 1000
        while times > 0:
            times -= 1
            td = ordereddict()
            count = 100000
            while count > 0:
                td['ab%08d' % count] = dict(abcdef = '%09d' % (count))
                count -= 1
            count = 100000
            while count > 0:
                del td['ab%08d' % count]
                count -= 1
            res.append(td)

# if py.test is not being used
def main():
    verbose = False
    total = 0
    failed = 0
    for func in (f for f in sorted(dir(TestOrderedDict)) if f.startswith('test_')):
        total += 1
        x = TestOrderedDict(True)
        x.setup_method(True)
        print('\r--> %50s ' % (func), end='')
        sys.stdout.flush()
        try:
            getattr(x, func)()
        except KeyError:
            if not verbose: print('\r--> %50s ' % (func),)
            failed += 1
            print('Failed')
        else:
            if verbose:
                print('Ok')
            else:
                print('\r                                                              \r', end='')
                sys.stdout.flush()
    print("Total %d, Failed %d" % (total, failed))

if __name__ == "__main__":
    main()
