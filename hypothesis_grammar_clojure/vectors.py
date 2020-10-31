from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .forms import form_items

from .separators import separator_strings

from custom.label.vectors import label
from custom.verify.vectors import verify, verify_with_metadata
from custom.parameters import coll_max, metadata_max

from .util import make_form_with_metadata_str_builder

open_delim = "["
close_delim = "]"

# XXX: could also have stuff before and after delimiters
def build_vector_str(vector_item):
    items = vector_item["inputs"]
    seps = vector_item["separators"]
    vector_elts = []
    for i, s in zip(items, seps):
        vector_elts += i["to_str"](i) + s
    return open_delim + "".join(vector_elts) + close_delim

@composite
def bare_vector_items(draw,
                      elements=form_items(),
                      separators=separator_strings()):
    n = draw(integers(min_value=0, max_value=coll_max))
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
            "to_str": build_vector_str,
            "verify": verify,
            "separators": sep_strs,
            "open": open_delim,
            "close": close_delim}

@composite
def vector_with_metadata_items(draw,
                               elements=form_items(),
                               separators=separator_strings(),
                               metadata="metadata"):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    vec_item = draw(bare_vector_items(elements=elements,
                                      separators=separators))
    #
    str_builder = make_form_with_metadata_str_builder(build_vector_str)
    #
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=m, max_size=m))
    #
    vec_item.update({"to_str": str_builder,
                     "verify": verify_with_metadata,
                     "metadata": md_items})
    #
    return vec_item

@composite
def vector_items(draw,
                 elements=form_items(),
                 separators=separator_strings(),
                 metadata=False):
    if not metadata:
        return draw(bare_vector_items(elements=elements,
                                      separators=separators))
    else:
        return draw(vector_with_metadata_items(elements=elements,
                                               separators=separators,
                                               metadata=metadata))
