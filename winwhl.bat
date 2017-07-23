REM this doesn't work, need to start the 64/32environment, then execute the first 2 and 
REM the appropriate other commands
r:
cd r:\ordereddict
c:\python\2.7\python.exe setup.py bdist_wheel
c:\python\2.6\python.exe setup.py bdist_wheel
c:\python\2.7-32\python.exe setup.py bdist_wheel
c:\python\2.6-32\python.exe setup.py bdist_wheel
