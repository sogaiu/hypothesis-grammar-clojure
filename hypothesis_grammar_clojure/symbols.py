from hypothesis import assume
from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of, sampled_from

import re

from .parameters import metadata_max

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, verify_with_metadata = verify_fns(name)
label = label_for(name)

from .util import make_form_with_metadata_str_builder

def build_sym_str(item):
    return item["inputs"]

@composite
def unqualified_symbol_items(draw):
    sym_str = draw(unqualified_symbol_as_str())
    # XXX: ignoring non-ascii
    ok_in_head = ["*", "+", "!", "-", "_",
                  "?", "<", ">", "=",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z",
                  "/",
                  "."]
    ok_in_body = ["*", "+", "!", "-", "_", "'",
                  "?", "<", ">", "=",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z",
                  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                  ".",
                  ":",
                  "#"]
    #
    n = draw(integers(min_value=0, max_value=19))
    #
    head_char = draw(sampled_from(ok_in_head))
    # slash by itself can be in a symbol, but for unqualified symbols,
    # this is only allowed if the symbol is exactly slash (division)
    if head_char == "/":
        m = 0
    else:
        m = n
    body_chars = \
        draw(lists(elements=sampled_from(ok_in_body),
                   min_size=m, max_size=m))
    sym_body = "".join(body_chars)
    # ensure the colon-releated constraints are enforced
    # XXX: :: is reserved for keywords, but "ending in a colon"
    #      is reserved for future use in clojure...what happens
    #      if that ends up being used?
    assume(not(re.search("::", sym_body)))
    assume(not(re.search(":$", sym_body)))
    # ensure a number hasn't been generated
    # XXX: this is incomplete and quite possibly a fair bit of work to
    #      get right as it may require weeding out all possible number
    #      representations...
    if n > 0:
        if (head_char == "+") or (head_char == "-"):
            assume(not(re.search("^[0-9]$", sym_body[0])))
    #
    sym_str = f'{head_char}{sym_body}'
    #
    return {"inputs": sym_str,
            "label": label,
            "to_str": build_sym_str,
            "verify": verify}

@composite
def qualified_symbol_items(draw):
    # XXX: ignoring on-ascii
    ok_in_head = ["*", "+", "!", "-", "_",
                  "?", "<", ">", "=",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z",
                  "."]
    ok_in_body = ["*", "+", "!", "-", "_", "'",
                  "?", "<", ">", "=",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z",
                  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                  ".",
                  ":",
                  "#"]
    #
    n = draw(integers(min_value=0, max_value=19))
    #
    head_char = draw(sampled_from(ok_in_head))
    body_chars = \
        draw(lists(elements=sampled_from(ok_in_body),
                   min_size=n, max_size=n))
    sym_body = "".join(body_chars)
    # ensure the colon-releated constraints are enforced
    # XXX: :: is reserved for keywords, but "ending in a colon"
    #      is reserved for future use in clojure...what happens
    #      if that ends up being used?
    assume(not(re.search("::", sym_body)))
    assume(not(re.search(":$", sym_body)))
    # ensure a number hasn't been generated
    # XXX: this is incomplete and quite possibly a fair bit of work to
    #      get right as it may require weeding out all possible number
    #      representations...
    if n > 0:
        if (head_char == "+") or (head_char == "-"):
            assume(not(re.search("^[0-9]$", sym_body[0])))
    #
    uq_sym = draw(unqualified_symbol_as_str())
    #
    sym_str = f'{head_char}{sym_body}/{uq_sym}'
    #
    return {"inputs": sym_str,
            "label": label,
            "to_str": build_sym_str,
            "verify": verify}

@composite
def symbol_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    sym_item = draw(one_of(unqualified_symbol_items(),
                           qualified_symbol_items()))
    #
    if not metadata:
        return sym_item
    else:
        # XXX: not sure about this approach
        sym_str = sym_item["to_str"](sym_item)
        #
        str_builder = make_form_with_metadata_str_builder(build_sym_str)
        #
        n = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = \
            draw(lists(elements=metadata_items(flavor=metadata),
                       min_size=n, max_size=n))
        #
        return {"inputs": sym_str,
                "label": label,
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items}
