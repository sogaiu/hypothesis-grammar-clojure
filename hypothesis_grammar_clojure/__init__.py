"""Hypothesis strategies for Clojure grammars."""

__version__ = '0.0.1'

# potential users
#
# - calva (see src/cursor-doc)
#     https://github.com/BetterThanTomorrow/calva
#     https://www.npmjs.com/package/calva-clojure-cursor-doc
# - parcera
#     https://github.com/carocad/parcera
# - parinferish
#     https://github.com/oakes/parinferish
# - rewrite-cljc
#     https://github.com/lread/rewrite-cljc-playground
# - tree-sitter-clojure
#     https://github.com/sogaiu/tree-sitter-clojure

# XXX: there might be some things missing from below

from hypothesis_grammar_clojure.comments import comment_items
#
from hypothesis_grammar_clojure.nils import nil_items
from hypothesis_grammar_clojure.booleans import boolean_items
from hypothesis_grammar_clojure.characters import character_items
from hypothesis_grammar_clojure.keywords import keyword_items
from hypothesis_grammar_clojure.numbers import number_items
from hypothesis_grammar_clojure.strings import string_items
from hypothesis_grammar_clojure.symbols import symbol_items
from hypothesis_grammar_clojure.symbolic_values import symbolic_value_items
from hypothesis_grammar_clojure.regex import regex_items
#
from hypothesis_grammar_clojure.atoms import atom_items
#
from hypothesis_grammar_clojure.lists import list_items
from hypothesis_grammar_clojure.maps import map_items
from hypothesis_grammar_clojure.namespaced_maps import namespaced_map_items
from hypothesis_grammar_clojure.sets import set_items
from hypothesis_grammar_clojure.vectors import vector_items
#
from hypothesis_grammar_clojure.collections import collection_items, \
    recursive_collection_items
#
from hypothesis_grammar_clojure.read_conds import read_cond_items
from hypothesis_grammar_clojure.read_cond_splicings import \
    read_cond_splicing_items
#
from hypothesis_grammar_clojure.anon_funcs import anon_func_items
#
from hypothesis_grammar_clojure.deref_forms import deref_form_items
from hypothesis_grammar_clojure.var_quote_forms import var_quote_form_items
from hypothesis_grammar_clojure.eval_forms import eval_form_items
from hypothesis_grammar_clojure.quote_forms import quote_form_items
from hypothesis_grammar_clojure.syntax_quote_forms import \
    syntax_quote_form_items
from hypothesis_grammar_clojure.unquote_forms import unquote_form_items
from hypothesis_grammar_clojure.unquote_splicing_forms import \
    unquote_splicing_form_items
#
from hypothesis_grammar_clojure.tagged_literals import tagged_literal_items
#
from hypothesis_grammar_clojure.discard_exprs import discard_expr_items
#
from hypothesis_grammar_clojure.forms import form_items
#
from hypothesis_grammar_clojure.metadata import metadata_items
