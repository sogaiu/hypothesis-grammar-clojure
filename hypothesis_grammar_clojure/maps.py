from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .forms import form_items

from .separators import separator_strings

from custom.label.maps import label
from custom.verify.maps import verify, verify_with_metadata
from custom.parameters import coll_max, metadata_max

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
def bare_map_items(draw,
                   elements=form_items(),
                   separators=separator_strings(),
                   label=label,
                   verify=verify):
    # XXX: what about this /2?
    n = 2 * draw(integers(min_value=0, max_value=coll_max/2))
    #
    items = draw(lists(elements=elements, min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separators,
                          min_size=n, max_size=n))
    if n > 0:
        sep_strs = sep_strs[:-1] + [""]
    #
    return {"inputs": items,
            "label": label,
            "to_str": build_map_str,
            "verify": verify,
            "separators": sep_strs,
            "open": open_delim,
            "close": close_delim}

@composite
def map_with_metadata_items(draw,
                            elements=form_items(),
                            separators=separator_strings(),
                            metadata="metadata",
                            label=label,
                            verify=verify_with_metadata):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    map_item = draw(bare_map_items(elements=elements,
                                   separators=separators,
                                   label=label,
                                   verify=verify))
    #
    str_builder = make_form_with_metadata_str_builder(build_map_str)
    #
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=m, max_size=m))
    #
    map_item.update({"to_str": str_builder,
                     "metadata": md_items})
    #
    return map_item

@composite
def map_items(draw,
              elements=form_items(),
              separators=separator_strings(),
              metadata=False,
              label=label,
              verify=verify):
    if not metadata:
        return draw(bare_map_items(elements=elements,
                                   separators=separators,
                                   label=label,
                                   verify=verify))
    else:
        return draw(map_with_metadata_items(elements=elements,
                                            separators=separators,
                                            metadata=metadata,
                                            label=label,
                                            verify=verify))
