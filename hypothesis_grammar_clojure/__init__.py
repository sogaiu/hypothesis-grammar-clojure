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

from .comments import comment_items
#
from .nils import nil_items
from .booleans import boolean_items
from .characters import character_items
from .keywords import keyword_items
from .numbers import number_items
from .strings import string_items
from .symbols import symbol_items
from .symbolic_values import symbolic_value_items
from .regex import regex_items
#
from .atoms import atom_items
#
from .lists import list_items
from .maps import map_items
from .namespaced_maps import namespaced_map_items
from .sets import set_items
from .vectors import vector_items
#
from .collections import collection_items, recursive_collection_items
#
from .read_conds import read_cond_items
from .read_cond_splicings import read_cond_splicing_items
#
from .anon_funcs import anon_func_items
#
from .deref_forms import deref_form_items
from .var_quote_forms import var_quote_form_items
from .eval_forms import eval_form_items
from .quote_forms import quote_form_items
from .syntax_quote_forms import syntax_quote_form_items
from .unquote_forms import unquote_form_items
from .unquote_splicing_forms import unquote_splicing_form_items
#
from .tagged_literals import tagged_literal_items
#
from .discard_exprs import discard_expr_items
#
from .forms import form_items
#
from .metadata import metadata_items
