
if __name__ != "__main__":
    import py
import string

from ordereddict import ordereddict

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
        for index, ch in enumerate(string.lowercase):
            self.z[ch] = index
        self.e = ordereddict()    

    def test_len(self):
        assert len(self.z) == len(string.lowercase)
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
        
    def test_in(self):
        assert 'c' in self.z
        
    def test_not_in(self):
        assert 'C' not in self.z
        
    def test_has_key(self):
        assert self.z.has_key('z')
        
    def test_items(self):
        "unlikely to function in a non-ordered dictionary"
        index = 0
        for index, y in enumerate(self.z.items()):
            assert string.lowercase[index] == y[0]
            assert index == y[1]

    def test_keys(self):
        "unlikely to function in a non-ordered dictionary"
        index = 0
        for y in self.z.keys():
            assert self.z[y] == index
            index += 1

    def test_update(self):
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

    def test_fromkeys(self):
        x = ordereddict.fromkeys([1,2,3,4,5,6])
        assert len(x) == 6
        assert x[6] is None
        x = ordereddict.fromkeys((1,2,3,4,5), 'abc')
        assert len(x) == 5
        assert x[5] == 'abc'
        assert x.keys() == [1,2,3,4,5]

    def test_values(self):
        "unlikely to function in a non-ordered dictionary"
        index = 0
        for y in self.z.values():
            assert y == index
            index += 1

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
        import copy
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

    def test_iterkeys(self):
        index = 0
        for index, y in enumerate(self.z.iterkeys()):
            assert string.lowercase[index] == y

    def test_iterkeys_iterator(self):
        tmp = self.z.iterkeys()
        assert tmp.__length_hint__() == 26

    def test_iter(self):
        res = ""
        for y in self.z:
            res += y
        assert string.lowercase == res

    def test_itervalues(self):
        index = 0
        for index, y in enumerate(self.z.itervalues()):
            assert index == y
            
    def test_iteritems(self):
        index = 0
        for index, y in enumerate(self.z.iteritems()):
            assert string.lowercase[index] == y[0]
            assert index == y[1]

    def test_repr(self):
        d = ordereddict()
        assert repr(d) == 'ordereddict([])'
        d['a'] = 1
        assert repr(d) == "ordereddict([('a', 1)])"
        d[2] = 'b'
        assert repr(d) == "ordereddict([('a', 1), (2, 'b')])"

        
    def test_insert_newitem(self):
        r = self.x.copy()
        r.insert(3, 'ca', 8)
        assert r.index('ca') == 3
        assert r.get('ca') == 8
        assert len(r) == 5

    def test_insert_existing_key_sameplace(self):
        r = self.z.copy()
        pos = r.index('k')
        r.insert(pos, 'k', 42)
        assert r.index('k') == pos
        assert r.get('k') == 42
        assert len(r) == len(string.lowercase)

    def test_insert_existing_key_before(self):
        r = self.z.copy()
        pos = r.index('k')
        r.insert(pos-3, 'k', 42)
        assert r.index('k') == pos - 3
        assert r.get('k') == 42
        assert len(r) == len(string.lowercase)

    def test_insert_existing_key_after(self):
        r = self.z.copy()
        pos = r.index('k')
        r.insert(pos+3, 'k', 42)
        assert r.index('k') == pos + 3
        assert r.get('k') == 42
        assert len(r) == len(string.lowercase)


    def test_insert_range(self):
        r = self.x.copy()
        if not self.nopytest:
            py.test.raises(IndexError, "r.insert(10, 'ca', 9)")
            py.test.raises(IndexError, "r.insert(-8, 'ca', 9)")
            # border case, should we allow insert at len + 1?
            py.test.raises(IndexError, "r.insert(5, 'ca', 9)")
        
        
    def test_reverse(self):
        r = self.z.copy()
        r.reverse()
        res = []
        for index, ch in enumerate(string.lowercase):
            assert r[ch] == index
            res.insert(0, ch)
        assert res == r.keys()

# if py.test is not being used
def main():
    for func in (f for f in sorted(dir(TestOrderedDict)) if f.startswith('test_')):
        x = TestOrderedDict(True)
        x.setup_method(True)
        print '--> %30s' % (func),
        try:
            getattr(x, func)()
        except KeyError:
            print 'Failed'
        else:
            print 'Ok'

if __name__ == "__main__":
    main()

