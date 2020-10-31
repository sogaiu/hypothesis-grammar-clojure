from hypothesis import assume
from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, sampled_from

from .symbols import symbol_items

from .forms import form_items

from .separators import separator_strings

from custom.label.tagged_literals import label
from custom.verify.tagged_literals import verify, verify_with_metadata
from custom.parameters import metadata_max

from .util import make_form_with_metadata_str_builder

marker = '#'

# XXX: could also have stuff before and after delimiters
def build_tagged_literal_str(tagged_literal_item):
    form_item = tagged_literal_item["inputs"]
    form_str = form_item["to_str"](form_item)
    #
    seps = tagged_literal_item["separators"]
    #
    tag_item = tagged_literal_item["tag"]
    tag_str = tag_item["to_str"](tag_item)
    #
    # XXX: consider again later
    #return marker + seps[0] + tag_str + seps[1] + form_str
    return marker + tag_str + " " + form_str

@composite
def tag_items(draw):
    # XXX: symbol with metadata should be possible too...
    #      may need to go over other parts of code to find
    #      similar cases
    tag_item = draw(symbol_items())
    #
    # "# followed immediately by a symbol starting with an alphabetic
    #  character indicates that that symbol is a tag"
    #
    # via: https://github.com/edn-format/edn#tagged-elements
    #
    tag_head = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z",
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z"]
    tag_head_str = draw(sampled_from(tag_head))
    #
    tag_item["inputs"] = tag_head_str + tag_item["inputs"]
    #
    return tag_item

@composite
def bare_tagged_literal_items(draw,
                              separators=separator_strings()):
    form_item = draw(form_items())
    #
    tag_item = draw(tag_items())
    #
    sep_strs = draw(lists(elements=separators,
                          min_size=2, max_size=2))
    return {"inputs": form_item,
            "label": label,
            "to_str": build_tagged_literal_str,
            "verify": verify,
            "tag": tag_item,
            "separators": sep_strs,
            "marker": marker}

@composite
def tagged_literal_with_metadata_items(draw,
                                       separators=separator_strings(),
                                       metadata="metadata"):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_flavor
    #
    check_metadata_flavor(metadata)
    #
    tl_item = draw(bare_tagged_literal_items(separators=separators))
    #
    str_builder = \
        make_form_with_metadata_str_builder(build_tagged_literal_str)
    #
    n = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(flavor=metadata),
                          min_size=n, max_size=n))
    #
    tl_item.update({"to_str": str_builder,
                    "verify": verify_with_metadata,
                    "metadata": md_items})
    #
    return tl_item

@composite
def tagged_literal_items(draw,
                         separators=separator_strings(),
                         metadata=False):
    if not metadata:
        return draw(bare_tagged_literal_items(separators=separators))
    else:
        return \
            draw(tagged_literal_with_metadata_items(separators=separators,
                                                    metadata=metadata))
