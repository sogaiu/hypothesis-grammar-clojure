# Hypothesis Grammar Clojure

Hypothesis strategies / generators for testing Clojure grammars.

## Status

Early stage.

## Usage

Currently, to get an idea of how to use this, please take a look at
[prop-test-ts-clj](https://github.com/sogaiu/prop-test-ts-clj).

The following should give an idea of some of the important points
involved though:

* Install (e.g. clone via git or use pip)
* Create and fill in top-level `custom` directory appropriately (stubs provided)
* Create a Python file that uses the above to test via Hypothesis

The `custom` directory contains `verify`, `label`, and
`parameters.py`.  These are used to express specifics of the target
"grammar" implementation.

The bulk of the work is likely to be in implementing the `verify`
package.  For prop-test-ts-clj, the key pieces are in
[verify.py](https://github.com/sogaiu/prop-test-ts-clj/blob/master/custom/verify/verify.py).
Most of the other files in that package just use bits from
`verify.py`,
e.g. [anon_funcs.py](https://github.com/sogaiu/prop-test-ts-clj/blob/master/custom/verify/anon_funcs.py).

The `label` package is used to specify the names of various
grammatical constructs, e.g. `var_quote_form` for var quote forms in
tree-sitter-clojure.  For prop-test-ts-clj, an example file within
this package is
[var_quote_forms.py](https://github.com/sogaiu/prop-test-ts-clj/blob/master/custom/label/var_quote_forms.py).
(If the target grammar for testing has no such labels, it may be that
using the default stubs could work.)

The `parameters.py` file contains some bits used to tweak defaults for
generators (e.g. maximum number of elements in a collection).

The Python testing file is fairly straight-forward Hypothesis in
action --
[prop-test-ts-clj.py](https://github.com/sogaiu/prop-test-ts-clj/blob/master/prop-test-ts-clj.py).
Roughly, it involves making the generators available, setting up
testing conditions + definitions, and then sequentially invoking each
defined property-based test.

## Users

* [prop-test-ts-clj](https://github.com/sogaiu/prop-test-ts-clj) - property-based testing of [tree-sitter-clojure](https://github.com/sogaiu/tree-sitter-clojure)

## Why Python?

In short:

1) test.check has [the bind problem](https://github.com/clojure/test.check/blob/master/doc/growth-and-shrinking.md#unnecessary-bind) and most if not all of the generators in question would likely be affected
2) Hypothesis provides decent property-based goodness and apparently does not suffer from the aforementioned issue
3) Hypothesis is available in Python
4) It's possible to interface with Clojure (via libpython-clj), Python, and rudimentary JavaScript/TypeScript (via py-mini-racer)

The last point means that it may be possible to apply this to test the
following:

* Calva's lexer (TypeScript/JavaScript)
* parcera (Clojure)
* rewrite-clj* (Clojure)
* tree-sitter-clojure (Python, if using Python bindings)
