from hypothesis.strategies import booleans, integers
from hypothesis.strategies import composite, just, lists, one_of

from .utils import to_ascii

@composite
def radix_number_as_str(draw):
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
    return f'{sign}{radix}{r_or_R}{"".join(digits)}'

@composite
def hex_number_as_str(draw):
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
    return f'{sign}0{x_or_X}{"".join(digits)}{end_n}'

@composite
def octal_number_as_str(draw):
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
    return f'{sign}0{"".join(digits)}{m_or_n}'

@composite
def ratio_as_str(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    p = draw(integers(min_value=0))
    q = draw(integers(min_value=1))
    #
    return f'{sign}{p}/{q}'

@composite
def double_as_str(draw):
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
    return f'{sign}{left_of_dot}{dot_part}{exp_part}{end_m}'

@composite
def integer_as_str(draw):
    sign = draw(one_of(just(""), just("+"), just("-")))
    #
    i = draw(integers(min_value=0))
    #
    m_or_n = draw(one_of(just(""), just("M"), just("N")))
    #
    return f'{sign}{i}{m_or_n}'

@composite
def number_as_str(draw):
    number = draw(one_of(radix_number_as_str(),
                         hex_number_as_str(),
                         octal_number_as_str(),
                         ratio_as_str(),
                         double_as_str(),
                         integer_as_str()))
    #
    return number
