#
# Ported to Python from the C source at
#
#   https://github.com/ariya/FastLZ
#


def decompress(data):
    out = bytes()
    index = 0
    while index < len(data):
        typ = data[index] >> 5
        if typ == 0:
            # Literal
            length = data[index] + 1
            out += data[index+1:length+index+1]
            index += length+1
        elif typ < 7:
            # Short match
            offset = 256 * (data[index] & 0x1f) + data[index+1]
            length = 2 + (data[index] >> 5)
            ref = len(out) - offset - 1
            out += out[ref:ref+length]
            index += 2
        else:
            # Long match
            offset = 256 * (data[index] & 0x1f) + data[index+2]
            length = 9 + data[index+1]
            index += 3
            ref = len(out) - offset - 1
            out += out[ref:ref+length]
    return out
