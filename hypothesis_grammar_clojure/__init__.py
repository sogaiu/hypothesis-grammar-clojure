"""Hypothesis strategies for Clojure grammars."""

__version__ = '0.0.1'

# grammatical pieces
#
# subatomic (1)
#   auto_resolve_marker
#
# atomic (10)
#   boolean
#   + character
#   comment
#   + keyword
#   nil
#   + number
#   regex
#   + string
#   + symbol
#   symbolic_value
#
# compound (17)
#   discard_expr
#   list
#   map
#   vector
#   set
#   anon_func
#   read_cond
#   read_cond_splicing
#   namespaced_map
#   var_quote_form
#   eval_form
#   tagged_literal
#   syntax_quote_form
#   quote_form
#   unquote_splicing_form
#   unquote_form
#   deref_form
#
# compound but not standalone (2)
#   metadata
#   old_metadata

# potential users
#
# - parcera
# - parinferish
# - rewrite-cljc
# - tree-sitter-clojure
