from hypothesis.strategies import integers, lists
from hypothesis.strategies import composite, sampled_from

from custom.label.whitespace import label
from custom.verify.whitespace import verify

def build_whitespace_str(item):
    return item["inputs"]

@composite
def whitespace_items(draw):
    # see java.lang.Character isWhitespace
    allowed = [",", # clojure treats a comma as whitespace
               # space separators excluding U+00A0, U+2007, U+202F
               " ",
               '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004',
               '\u2005', '\u2006', '\u2008', '\u2009', '\u200A', '\u205F',
               '\u3000',
               # line separator
               '\u2028',
               # paragraph separator
               '\u2029',
               # vertical tabulation
               '\u000B',
               # file separator
               '\u001c',
               # group separator
               '\u001d',
               # record separator
               '\u001e',
               # unit separator
               '\u001f',
               # other things with familiar names
               "\f", "\n", "\r", "\t"]
    #
    n = draw(integers(min_value=1, max_value=19))
    #
    ws_chars = \
        draw(lists(elements=sampled_from(allowed),
                   min_size=n, max_size=n))
    #
    ws_str = "".join(ws_chars)
    #
    return {"inputs": ws_str,
            "label": label,
            "to_str": build_whitespace_str,
            "verify": verify}
