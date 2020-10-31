from hypothesis.strategies import characters, integers
from hypothesis.strategies import composite, lists

from custom.label.strings import label
from custom.verify.strings import verify

def build_string_str(item):
    return item["inputs"]

@composite
def string_items(draw,
                 label=label,
                 verify=verify):
    #
    n = draw(integers(min_value=0, max_value=100))
    #
    not_tween_delims = ['"', '\\']
    #
    chars = \
        draw(lists(elements=characters(blacklist_characters=not_tween_delims,
                                       min_codepoint=32, max_codepoint=127),
                   min_size=n, max_size=n))
    #
    # XXX: what about escape sequences? e.g. \", \\, etc.
    str_str = f'"{"".join(chars)}"'
    #
    return {"inputs": str_str,
            "label": label,
            "to_str": build_string_str,
            "verify": verify}
