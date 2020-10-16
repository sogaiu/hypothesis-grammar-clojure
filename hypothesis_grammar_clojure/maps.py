from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max, metadata_max

from .forms import form_items

from .separators import separator_strings

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, verify_with_metadata = verify_fns(name)
label = label_for(name)

from .util import make_form_with_metadata_str_builder

open_delim = "{"
close_delim = "}"

# XXX: could also have stuff before and after delimiters
def build_map_str(map_item):
    items = map_item["inputs"]
    seps = map_item["separators"]
    map_elts = []
    for i, s in zip(items, seps):
        map_elts += i["to_str"](i) + s
    return open_delim + "".join(map_elts) + close_delim

@composite
def map_items(draw, elements=form_items(), metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    # XXX: what about this /2?
    n = 2 * draw(integers(min_value=0, max_value=coll_max/2))
    #
    items = draw(lists(elements=elements, min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    if not metadata:
        return {"inputs": items,
                "label": label,
                "to_str": build_map_str,
                "verify": verify,
                "separators": sep_strs,
                "open": open_delim,
                "close": close_delim}
    else:
        str_builder = make_form_with_metadata_str_builder(build_map_str)
        #
        m = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(flavor=metadata),
                              min_size=m, max_size=m))
        #
        return {"inputs": items,
                "label": label,
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items,
                "separators": sep_strs,
                "open": open_delim,
                "close": close_delim}

