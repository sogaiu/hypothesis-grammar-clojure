from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, lists, one_of

from .parameters import coll_max, metadata_max

from .auto_res_markers import auto_res_marker_items
from .forms import form_items
from .keywords import keyword_items

from .separators import separator_strings

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, verify_with_metadata = verify_fns(name)
label = label_for(name)

from .util import make_form_with_metadata_str_builder

marker = "#"
open_delim = "{"
close_delim = "}"

# XXX: could also have stuff before and after delimiters
def build_namespaced_map_str(namespaced_map_item):
    items = namespaced_map_item["inputs"]
    seps = namespaced_map_item["separators"]
    ns_map_elts = []
    for i, s in zip(items, seps):
        ns_map_elts += i["to_str"](i) + s
    #
    prefix = namespaced_map_item["prefix"]
    prefix_str = prefix["to_str"](prefix)
    #
    return marker + prefix_str + \
        open_delim + "".join(ns_map_elts) + close_delim

@composite
def prefix_items(draw):
    prefix_item = draw(one_of(auto_res_marker_items(),
                              keyword_items()))
    return prefix_item

@composite
def namespaced_map_items(draw, elements=form_items(), metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    # XXX: what about this /2?
    n = 2 * draw(integers(min_value=0, max_value=coll_max/2))
    #
    items = draw(lists(elements=elements, min_size=n, max_size=n))
    #
    prefix_item = draw(prefix_items())
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    if not metadata:
        return {"inputs": items,
                "label": label,
                "to_str": build_namespaced_map_str,
                "verify": verify,
                "prefix": prefix_item,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_namespaced_map_str)
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
                "prefix": prefix_item,
                "metadata": md_items,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
