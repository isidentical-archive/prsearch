# PRSearch
```
 $ python prsearch.py Lib/test/test_unparse.py
Matching: Lib/test/test_unparse.py
URL: https://github.com/python/cpython/pull/17797
==============================
Matching: Lib/test/test_unparse.py
URL: https://github.com/python/cpython/pull/17892
==============================
Matching: Lib/test/test_unparse.py
URL: https://github.com/python/cpython/pull/18768
==============================
```
## Creating / Updating the data
```
$ python prsearch.py --repo python/cpython --fresh --token [REDACTED USER ACCESS TOKEN] Lib/ast.py
Crawling the 1th page.
Crawling the 2th page.
Crawling the 3th page.
Crawling the 4th page.
Crawling the 5th page.
Crawling the 6th page.
Crawling the 7th page.
Crawling the 8th page.
Crawling the 9th page.
Crawling the 10th page.
Crawling the 11th page.
Crawling the 12th page.
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/5798
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/9605
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/12382
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/17662
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/17797
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/17892
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/18558
==============================
Matching: Lib/ast.py
URL: https://github.com/python/cpython/pull/18768
==============================
```

