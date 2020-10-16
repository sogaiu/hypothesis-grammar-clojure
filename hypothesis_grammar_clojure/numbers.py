from hypothesis.strategies import booleans, integers
from hypothesis.strategies import composite, just, lists, one_of

from .util import to_ascii

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_num_str(item):
    return item["inputs"]

@composite
def hex_number_items(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    x_or_X = draw(one_of(just("X"), just("x")))
    # XXX: too many digits is a problem
    n = draw(integers(min_value=1, max_value=20))
    pre_digits = draw(lists(elements=integers(min_value=0,
                                              max_value=15),
                            min_size=n, max_size=n))
    caps = draw(lists(elements=booleans(),
                      min_size=n, max_size=n))
    digits = map(to_ascii, pre_digits, caps)
    #
    end_n = draw(one_of(just(""), just("N")))
    #
    num_str = f'{sign}0{x_or_X}{"".join(digits)}{end_n}'
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def octal_number_items(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    # XXX: too many digits is a problem
    n = draw(integers(min_value=1, max_value=20))
    pre_digits = draw(lists(elements=integers(min_value=0,
                                              max_value=7),
                            min_size=n, max_size=n))
    digits = map(lambda d: chr(d + 48), pre_digits)
    #
    m_or_n = draw(one_of(just(""), just("M"), just("N")))
    #
    num_str = f'{sign}0{"".join(digits)}{m_or_n}'
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def radix_number_items(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    radix = draw(integers(min_value=2, max_value=36))
    #
    r_or_R = draw(one_of(just("R"), just("r")))
    # XXX: too many digits is a problem
    n = draw(integers(min_value=1, max_value=20))
    pre_digits = draw(lists(elements=integers(min_value=0,
                                              max_value=radix - 1),
                            min_size=n, max_size=n))
    caps = draw(lists(elements=booleans(),
                      min_size=n, max_size=n))
    digits = map(to_ascii, pre_digits, caps)
    #
    num_str = f'{sign}{radix}{r_or_R}{"".join(digits)}'
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def ratio_items(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    p = draw(integers(min_value=0))
    q = draw(integers(min_value=1))
    #
    num_str = f'{sign}{p}/{q}'
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def double_items(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    left_of_dot = draw(integers(min_value=0))
    #
    has_dot_part = draw(booleans())
    if has_dot_part:
        dot_part = f'.{draw(integers(min_value=0))}'
    else:
        dot_part = ""
    #
    has_exp_part = draw(booleans())
    if has_exp_part:
        e_or_E = draw(one_of(just("E"), just("e")))
        exp_sign = draw(one_of(just(""), just("+"), just("-")))
        exp_num = draw(integers(min_value=0))
        exp_part = f'{e_or_E}{exp_sign}{exp_num}'
    else:
        exp_part = ""
    #
    end_m = draw(one_of(just(""), just("M")))
    #
    num_str = f'{sign}{left_of_dot}{dot_part}{exp_part}{end_m}'
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def integer_items(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    i = draw(integers(min_value=0))
    #
    m_or_n = draw(one_of(just(""), just("M"), just("N")))
    #
    num_str = f'{sign}{i}{m_or_n}'
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def number_items(draw):
    num_item = draw(one_of(radix_number_items(),
                           hex_number_items(),
                           octal_number_items(),
                           ratio_items(),
                           double_items(),
                           integer_items()))
    return num_item
