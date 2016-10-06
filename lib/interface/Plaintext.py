from lib.interface.Text import Text


class Plaintext(Text):
    input_standard = input
    input_obfuscated = input
    output_standard = print
    console_width = 60
