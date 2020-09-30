from hypothesis.strategies import integers, lists
from hypothesis.strategies import composite, sampled_from

@composite
def whitespace_as_str(draw):
    allowed = ["\f", "\n", "\r", "\t", ",", " "]
    #
    n = draw(integers(min_value=1, max_value=19))
    #
    ws_chars = \
        draw(lists(elements=sampled_from(allowed),
                   min_size=n, max_size=n))
    #
    return "".join(ws_chars)
