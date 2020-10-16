from hypothesis import assume

from hypothesis.strategies import composite, one_of, recursive

from .forms import form_items

from .lists import list_items
from .maps import map_items
from .namespaced_maps import namespaced_map_items
from .sets import set_items
from .vectors import vector_items

# XXX: metadata support?
@composite
def collection_items(draw, elements=form_items()):
    coll_item = draw(one_of(list_items(elements=elements),
                            map_items(elements=elements),
                            namespaced_map_items(elements=elements),
                            vector_items(elements=elements),
                            set_items(elements=elements)))
    return coll_item

# XXX: metadata support?
# XXX: also ends up testing non-collections -- is that a problem?
@composite
def recursive_collection_items(draw, elements=form_items()):
    rec_coll_item = draw(recursive(elements, collection_items))
    # XXX: without this seems to test too many degenerate cases?
    assume(len(rec_coll_item["inputs"]) > 0)
    #
    return rec_coll_item
