import sys
import fastlz
import struct

#
# Partially decode and decompress chunks for an LG inverter and battery
#

# Sample chunks
TLS_CHUNKS = [
    b'&\x0f\x0blg-uploader\x00\x00\x00\x00\x02\x00\x00\x03?\x00\x00\x02\x0c\x1d{"type":"powerReport","err_cod@\x18\x01OK \x0f\x0emsg":{"deviceID /\x0475072 \x19\x08timestamp \x13\x0b202605212050 \x1a\x1cregs":[[46006,"27888"],[45221 \x0f\xc0\x0b\x050,"364\xa0\r\x0419,"0\xa0\x0b\x004 %\xe0\x00\x0b %\x0111\xa0\x18\x003\xe0\x02$\x006\xe0\x02$\x006\xe0\x03$\x005\xc0$\x02500@c\x0110`K \r\x000 &\xe0\x00\x0b\x002\xe0\x01\x0b\x0124\xe0\x02\x0b\x005\xe0\x01\x0b\x000\xc0\x17\x0449963\xa0\x17@\x0b\xe0\x02\x17\x0157\xe0\x01\x17\x009\xe0\x03\x0b\x008\xe0\x02\x17\xe0\x01\x91\x0121 G!\x11\x000a\x11@\x0f 3\x031410a\x15\x035015!1\xe0\x00\xb1\x001@]\x0193@\xfd@* Fa\t \x18\x006 &\x02225\x80\x19\x0116 D\x0122\xc0BA\r\xa0\xe6\x002@\xc2\xa03!\x9d\xe0\x02\x17 ?\x0149@>!\xa5\x001\xe0\x00\xab\x006!\xc9\xa0$@\x0b\xc1# \x0b\x007\xe0\x00\xf3 \x0b\xc0H\x034007 /\x02247`I < \r`z!%\x004 U\x81\xdd"\x07!y`\xc6@\x0b!\xb8\x005`\xab@\x0c!\x0e\x800 $ n\x80\x93A\xab\xe0\x00c!>\xe0\x00{ \x0b \x17`\xd0 0@{\xc0<\x007!\x02\xc0\x0b\x005@#\x0134![\x0172\xc0\xe3AI\xc0\x1f\x006 \x1f\x037372!\x83\x0b],"oldErrorC"\xf7"\xb7\x03{"pc \x06 ,#\x0e\x00m\xc0\t\x0ebattery":"0"}}}',
]

def main():
    for tls_chunk in TLS_CHUNKS:
        # The structure of the chunks is:
        # b'&' (type of chunk?)
        # b'\x0f' (length of subchunk)
            # b'\x0b' (length of string)
                # 'lg-uploader' (string data)
            # b'\x00\x00\x00'  (rest of subchunk)
        # b'\x00\x02' (big-endian counter, incremented every chunk)
        # b'\x00\x00\x03?' (big-endian compressed length)
        # b'\x00\x00\x02\x0c' (big-endian uncompressed length)
        # FastLZ compressed JSON follows... \x1d{"type" <...>
        # Sometimes there's more stuff after the JSON chunk.

        # Proof of concept:
        counter, uncompressed_length, compressed_length = struct.unpack('>HII',tls_chunk[17:27])

        d = fastlz.decompress(tls_chunk[27:])
        print("counter={},compressed_length={}, uncompressed_length={}".format(
            counter, compressed_length, uncompressed_length))

        print(d)

if __name__ == "__main__":
    main()

