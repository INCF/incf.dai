import doctest
doctest.testfile("README.txt", optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
doctest.testfile("docs/UCSD.txt", optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
#doctest.testfile("docs/EMAP.txt", optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
