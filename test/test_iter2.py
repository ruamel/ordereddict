#@pytest.mark.skipif(sys.version_info[:2] != (2,7),
#                    reason="only in 2.7")
def test_iterkeys(self):
    index = 0
    for y in self.z.iterkeys():
        assert all_lowercase[index] == y
        index += 1
    assert index == 26

@pytest.mark.skipif(sys.version_info[:2] != (2,7),
                    reason="only in 2.7")
def test_iterkeys_rev(self):
    index = 0
    for y in self.z.iterkeys(reverse=True):
        assert all_lowercase[25 - index] == y
        index += 1
    assert index == 26

@pytest.mark.skipif(sys.version_info[:2] != (2,7),
                    reason="only in 2.7")
def test_iterkeys_iterator(self):
    tmp = self.z.iterkeys()
    assert tmp.__length_hint__() == 26

def test_iter(self):
    res = ""
    for y in self.z:
        res += y
    assert all_lowercase == res

@pytest.mark.skipif(sys.version_info[:2] != (2,7),
                    reason="only in 2.7")
def test_itervalues(self):
    index = 0
    for index, y in enumerate(self.z.itervalues()):
        assert index == y

@pytest.mark.skipif(sys.version_info[:2] != (2,7),
                    reason="only in 2.7")
def test_itervalues_rev(self):
    index = 0
    for y in self.z.itervalues(reverse=True):
        assert 25 - index == y
        index += 1
    assert index == 26

@pytest.mark.skipif(sys.version_info[:2] != (2,7),
                    reason="only in 2.7")
def test_iteritems(self):
    index = 0
    for index, y in enumerate(self.z.iteritems()):
        assert all_lowercase[index] == y[0]
        assert index == y[1]

@pytest.mark.skipif(sys.version_info[:2] != (2,7),
                    reason="only in 2.7")
def test_iteritems_rev(self):
    index = 0
    for y in self.z.iteritems(reverse=True):
        assert all_lowercase[25-index] == y[0]
        assert 25 - index == y[1]
        index += 1
    assert index == 26
