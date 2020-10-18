from hypothesis import assume
from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of, sampled_from

import re

from custom.label.keywords import label
from custom.verify.keywords import verify

def build_kwd_str(item):
    return item["inputs"]

@composite
def unqualified_keyword_no_sigil_as_str(draw):
    # XXX: ignoring non-ascii
    ok_in_head = ["*", "+", "!", "-", "_",
                  "?", "<", ">", "=",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z",
                  # https://clojure.atlassian.net/browse/TCHECK-155
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
    # XXX: :/ is recognized as a keyword via clojure's repl, however:
    #      https://clojure.atlassian.net/browse/TCHECK-155
    if head_char == "/":
        m = 0
    else:
        m = n
    body_chars = \
        draw(lists(elements=sampled_from(ok_in_body),
                   min_size=m, max_size=m))
    kwd_body = "".join(body_chars)
    # ensure the colon-releated constraints are enforced
    # XXX: :: is not allowed in the body, and "ending in a colon"
    #      is reserved for future use in clojure...what happens
    #      if that ends up being used?
    assume(not(re.search("::", kwd_body)))
    assume(not(re.search(":$", kwd_body)))
    #
    return f'{head_char}{kwd_body}'

@composite
def unqualified_auto_resolved_keyword_items(draw):
    uq_kwd_no_sig = draw(unqualified_keyword_no_sigil_as_str())
    # clojure repl rejects ::/
    assume(uq_kwd_no_sig != "/")
    #
    kwd_str = f'::{uq_kwd_no_sig}'
    #
    return {"inputs": kwd_str,
            "label": label,
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def unqualified_keyword_items(draw):
    uq_kwd_no_sig = draw(unqualified_keyword_no_sigil_as_str())
    #
    kwd_str = f':{uq_kwd_no_sig}'
    #
    return {"inputs": kwd_str,
            "label": label,
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def keyword_ns_as_str(draw):
    # XXX: ignoring non-ascii
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
    kwd_body = "".join(body_chars)
    # ensure the colon-releated constraints are enforced
    # XXX: :: is not allowed in the body, and "ending in a colon"
    #      is reserved for future use in clojure...what happens
    #      if that ends up being used?
    assume(not(re.search("::", kwd_body)))
    assume(not(re.search(":$", kwd_body)))
    #
    return f'{head_char}{kwd_body}'

@composite
def qualified_auto_resolved_keyword_items(draw):
    kwd_ns = draw(keyword_ns_as_str())
    uq_kwd_no_sig = draw(unqualified_keyword_no_sigil_as_str())
    #
    kwd_str =  f'::{kwd_ns}/{uq_kwd_no_sig}'
    #
    return {"inputs": kwd_str,
            "label": label,
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def qualified_keyword_items(draw):
    kwd_ns = draw(keyword_ns_as_str())
    uq_kwd_no_sig = draw(unqualified_keyword_no_sigil_as_str())
    #
    kwd_str = f':{kwd_ns}/{uq_kwd_no_sig}'
    #
    return {"inputs": kwd_str,
            "label": label,
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def keyword_items(draw):
    kwd_item = draw(one_of(unqualified_auto_resolved_keyword_items(),
                           unqualified_keyword_items(),
                           qualified_auto_resolved_keyword_items(),
                           qualified_keyword_items()))
    return kwd_item
