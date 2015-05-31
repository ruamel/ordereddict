# coding: utf-8

# requires:
# pip install ruamel.ordereddict sortedcontainers

import timeit
import sys
import os
import string

import ruamel.ordereddict
import sortedcontainers

LOOP = 1000
MINOF = 10
cls2time = "TimeAll"

this_module = sys.modules[__name__]
mod_name = os.path.splitext(__file__)[0]

ToDo = """
- mark methods to skip for dict using a decorator (isntead of nodict in name)
"""

class TimeAll(object):
    def __init__(self, typ):
        self.typ = typ

    def time000_empty(self):
        """base reference for overhead of doing nothing"""
        pass

    def time001_create_empty(self):
        """just create an instance"""
        x = self.typ()

    def time001_create_five_entry(self):
        """create an instance with five entries"""
        x = self.typ()
        x['a'] = 1
        x['b'] = 2
        x['c'] = 3
        x['d'] = 4
        x['e'] = 5

    def time002_create_26_entry(self):
        """the whole alphabet as entries"""
        x = self.typ()
        for index, ch in enumerate(string.lowercase):
            x[ch] = index
        assert len(x) == 26
        return x

    def time003_create_676_entry(self):
        """create entries aa: 0, ab: 1 ... zz: 675"""
        x = self.typ()
        index = 0
        for ch1 in string.lowercase:
            for ch2 in string.lowercase:
                x[ch1 + ch2] = index
                index += 1
        assert len(x) == 676
        return x

    def time003_create_676_entry_reversed(self):
        """create entries aa: 675, ab: 674 ... zz: 0"""
        x = self.typ()
        index = 0
        for ch1 in reversed(string.lowercase):
            for ch2 in reversed(string.lowercase):
                x[ch1 + ch2] = index
                index += 1
        assert len(x) == 676
        return x

    def time004_create_17576_entry(self):
        # 17576 items 'aaa' ... 'zzz'
        x = self.typ()
        index = 0
        for ch1 in string.lowercase:
            for ch2 in string.lowercase:
                for ch3 in string.lowercase:
                    x[ch1 + ch2 + ch3] = index
                    index += 1
        assert len(x) == 17576
        return x

    def time010_get_keys_from_26_entry(self):
        """return keys as list / SortedSet"""
        x = self.time002_create_26_entry()
        y = x.keys()

    def time020_pop_5_items_26_entry(self):
        """pop 5 items by key and check value and resulting length"""
        x = self.time002_create_26_entry()
        assert x.pop('f') == 5
        assert x.pop('k') == 10
        assert x.pop('p') == 15
        assert x.pop('u') == 20
        assert x.pop('z') == 25
        assert len(x) == 21

    def time021_pop_26_items_676_entry(self):
        """pop 26 items by key and check value and resulting length"""
        x = self.time003_create_676_entry()
        for k in x.keys():
            if k[1] == 'q':
                i = x.pop(k)
                assert (i % 26) == 16
        assert len(x) == 650

    def time030nodict_popitem_first_26_entry(self):
        """pop first item from 26 entry instance"""
        x = self.time002_create_26_entry()
        if self.typ is sortedcontainers.SortedDict:
            i = x.popitem(last=False)
        else:
            i = x.popitem(0)
        assert len(x) == 25

    def time031_popitem_last_26_entry(self):
        """pop last item from 26 entry instance"""
        x = self.time002_create_26_entry()
        x.popitem()
        assert len(x) == 25

    def time032nodict_popitem_first_676_entry(self):
        """pop first item from 676 entry instance"""
        x = self.time003_create_676_entry()
        if self.typ is sortedcontainers.SortedDict:
            i = x.popitem(last=False)
        else:
            i = x.popitem(0)
        assert len(x) == 675

    def time033_popitem_last_676_entry(self):
        """pop last item from 676 entry instance"""
        x = self.time003_create_676_entry()
        x.popitem()
        assert len(x) == 675

    def time032nodict_popitem_100_676_entry(self):
        """pop item with index 100 from 676 entry instance"""
        x = self.time003_create_676_entry_reversed()
        if self.typ is sortedcontainers.SortedDict:
            k = x.iloc[100]
            i = (k, x[k])
            del x.iloc[100]
        else:
            i = x.popitem(100)
        assert i[0] == 'dw'
        assert i[1] == 575  # reverse order of second char
        assert len(x) == 675

    def time040nodict_walk_26_iteritems(self):
        x = self.time002_create_26_entry()
        index = 0
        for y in x.iteritems():
            assert y[0] == string.lowercase[index]
            assert y[1] == index
            index += 1

    def time041nodict_walk_676_iteritems(self):
        x = self.time003_create_676_entry()
        index = 0
        for y in x.iteritems():
            assert y[1] == index
            index += 1


header = '--------------------------------- dict  sorteddict  SortedDict'

def do_time():
    results = ruamel.ordereddict.ordereddict()
    print sys.argv
    if len(sys.argv) > 1:
        todo = sys.argv[1:]
    else:
        todo = sorted([x for x in dir(getattr(this_module, cls2time))
                       if x.startswith('time')])
    print header
    for funname in todo:
        fun = "%-30s" % (funname.split('_', 1)[1],)
        results[fun] = []
        print fun,
        for testdict in (
            "dict",
            "ruamel.ordereddict.sorteddict",
            "sortedcontainers.SortedDict"
            ):
            if testdict != "ruamel.ordereddict.sorteddict" and \
               "sorteddict" in funname:
                res = None
                print '--------',
            elif testdict == "dict" and "nodict" in funname:
                # filter out some that would fail, because of lacking
                # functionality
                res = None
                print '--------',
            else:
                t = timeit.Timer(
                    "%s.%s(%s).%s()" % (mod_name, cls2time, testdict, funname),
                    "import %s, ruamel.ordereddict, sortedcontainers" % mod_name)
                res = min(t.repeat(MINOF, LOOP))
                print '%8.3f' % (res,),
                sys.stdout.flush()
            results[fun].append(res)
        print
    print '\nnormalized to sorteddict'
    print header
    for f, (x, y, z) in results.iteritems():
        print f,
        if x is None:
            print '--------',
        else:
            print '%8.3f' % (x / y),
        print '   1.000',
        if z is None:
            print '--------'
        else:
            print '%8.3f' % (z / y)


if __name__ == "__main__":
    # ta = getattr(this_module, cls2time)(sortedcontainers.SortedDict)
    # ta.time031nodict_popitem_100_676_entry()
    print 'loop:', LOOP, 'minof', MINOF
    do_time()
