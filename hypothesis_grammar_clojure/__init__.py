"""Hypothesis strategies for Clojure grammars."""

__version__ = '0.0.1'

# grammatical pieces
#
# subatomic (1)
#   + auto_res_marker
#
# atomic (10)
#   + boolean
#   + character
#   + comment
#   + keyword
#   + nil
#   + number
#   + regex
#   + string
#   + symbol
#   + symbolic_value
#
# collection-like (8)
#   + anon_func
#   + list
#   + map
#   + namespaced_map
#   + read_cond
#   + read_cond_splicing
#   + set
#   + vector
#
# adorned form (7)
#   + deref_form
#   + eval_form
#   + quote_form
#   + syntax_quote_form
#   + unquote_form
#   + unquote_splicing_form
#   + var_quote_form
#
# other (2)
#   + discard_expr
#   + tagged_literal
#
# compound but not standalone (2)
#   + metadata
#   + old_metadata

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
