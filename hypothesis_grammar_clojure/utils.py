def to_ascii(n, cap):
    if n <= 9:
        return chr(n + 48)
    else:
        if cap:
            offset = 55
        else:
            offset = 87
        return chr(n + offset)
