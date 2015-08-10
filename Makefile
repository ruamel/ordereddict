
UTILNAME:=ordereddict
PKGNAME:=ruamel.$(UTILNAME)
VERSION:=$$(python setup.py --version)
REGEN:=/usr/local/bin/ruamel_util_new util --published OrderedDict --skip-util --skip-hg

include ~/.config/ruamel_util_new/Makefile.inc

#clean:
#	rm -rf build .tox $(PKGNAME).egg-info/ README.pdf __pycache__
#	find . -name "*.pyc" -exec rm {} +

clean:
	rm -rf build *.egg-info/ .tox MANIFEST
	@find . -name "*.pyc" -print0  | xargs --no-run-if-empty -0 rm
	@find . -name "*~" -print0  | xargs --no-run-if-empty -0 rm
	find . -name "__pycache__" -print0  | xargs --no-run-if-empty -0 rm -rf

#BB:=ssh://hg@bitbucket.org/ruamel/ordereddict
#
#bitbucket:
#	ssh ruamel@localhost "cd $$PWD; hg push $(BB)"


pull_bb:
	ssh ruamel@localhost "cd $$PWD; hg clone $(BB) ."

rmbookmarks:
	rm  -rf .hg/git* .hg/bookmarks*

github:
	hg push git+ssh://git@github.com:ruamel/ordereddict.git 
