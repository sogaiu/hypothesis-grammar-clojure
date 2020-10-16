from hypothesis.strategies import composite, one_of

# XXX: support metadata?
@composite
def form_items(draw):
    # avoiding circular dependencies
    from .nils import nil_items
    from .booleans import boolean_items
    from .characters import character_items
    from .keywords import keyword_items
    from .numbers import number_items
    from .strings import string_items
    from .symbols import symbol_items
    from .symbolic_values import symbolic_value_items
    from .regex import regex_items
    #
    from .lists import list_items
    from .maps import map_items
    from .namespaced_maps import namespaced_map_items
    from .sets import set_items
    from .vectors import vector_items
    #
    from .read_conds import read_cond_items
    from .read_cond_splicings import read_cond_splicing_items
    from .anon_funcs import anon_func_items
    #
    from .deref_forms import deref_form_items
    from .var_quote_forms import var_quote_form_items
    from .eval_forms import eval_form_items
    from .quote_forms import quote_form_items
    from .syntax_quote_forms import syntax_quote_form_items
    from .unquote_forms import unquote_form_items
    from .unquote_splicing_forms import unquote_splicing_form_items
    #
    from .tagged_literals import tagged_literal_items
    #
    form_item = draw(one_of(nil_items(),
                            boolean_items(),
                            character_items(),
                            keyword_items(),
                            number_items(),
                            string_items(),
                            symbol_items(),
                            symbolic_value_items(),
                            regex_items(),
                            #
                            list_items(form_items()),
                            map_items(form_items()),
                            namespaced_map_items(form_items()),
                            set_items(form_items()),
                            vector_items(form_items()),
                            #
                            read_cond_items(),
                            read_cond_splicing_items(),
                            anon_func_items(),
                            #
                            deref_form_items(),
                            var_quote_form_items(),
                            eval_form_items(),
                            quote_form_items(),
                            syntax_quote_form_items(),
                            unquote_form_items(),
                            unquote_splicing_form_items(),
                            #
                            tagged_literal_items()))
    #
    return form_item
