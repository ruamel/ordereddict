
from distutils.core import setup, Extension

module1 = Extension('ordereddict',
                    sources = ['ordereddict.c'],
                   )

setup (name = 'ordereddict',
       version = '0.2a',
       description = 'a version of dict that keeps keys in insertion order',
       author = 'Anthon van der Neut',
       author_email = 'anthon@mnt.org',
       url = 'http://www.xs4all.nl/~anthon/ordereddict',
       long_description = """
A derivation of the pyton dictobject.c module that implements 
Key Insertion Order (KIO). By that I mean that the insertion order of 
new keys is being tracked, updating values of existing keys does not
change the order.

The basic C structure is exented with a pointer to a list of item pointers.
When a *new* key is added, this list is extended with a pointer to the item.
The implementation compacts the list of pointers on every deletion (unless
the last added key is removed, such as in popitem()). That 
involves a memmove of all the pointers behind the pointer to the item in 
question.

The .keys, .values, .items, .iterkeys, itervalues, iteritems, __iter__
return things in the order of insertion.

.popitem takes an optional argument (defaulting to -1), which is the
order of the item.

the representation of the ordereddict is the same with Larosa/Foord: 
"ordereddict([(key1, val1), (key2, val2)])"

Extra functions implemented:
.index(key) returns the position of key in the ordereddict:
    for k1 in d.keys():
        d.popitem(d.index(k1))[0] == k1 
.reverse() reverses the ordering of keys
    r = d.copy()
    r.reverse()
    keys = r.keys()
    for index, k in enumerate(reverse(d.keys())):
        assert keys[index] == k
    

Extra functions considered:
- creation option for ordereddict so it will be keeping KVIO
   (Key Value Insertion Order). That means that an update of a value of an 
   existing key moves the key to the end of the list.
   You would have to delete an item first in the current implementation.
- supporting slices 
- applying a sort function on keys
- keeping the keys in a particular order 
 
""",
       ext_modules = [module1],
      )


