"""
Simple XOR de-obfuscation tool. Reverses xor_tool.py.
"""

import argparse
import sys
import os
import re
import base64

import pyfiglet
from colorama import Fore, Style


# 1. Read file
def load_file(filename, fmt):
    """
    Load a file from disk. Binary format is read as bytes,
    text-based formats (hx, ca, bs) are read as text.
    """
    try:
        if fmt == "bn":
            with open(filename, "rb") as file:
                return file.read()
        else:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()
    except OSError as e:
        print(f"While reading file, error: {e}")
        sys.exit(1)


# 2. Parse input format back to raw bytes
def parse_input(data, fmt: str) -> bytes:
    """
    Reverse format_output() from xor_tool.py. Convert the formatted
    input back into the raw XORed bytes so we can XOR it again.

        bn - raw binary (already bytes, no conversion)
        hx - hexadecimal string
        ca - C array
        bs - Base64
    """
    fmt = fmt.lower()

    # Raw binary, no conversion needed
    if fmt == "bn":
        return data

    # Hexadecimal: strip whitespace, then decode
    if fmt == "hx":
        try:
            cleaned = "".join(data.split())
            return bytes.fromhex(cleaned)
        except ValueError as e:
            print(f"While parsing hex, error: {e}")
            sys.exit(1)

    # C-array: extract all 0xNN values with regex, then convert
    if fmt == "ca":
        try:
            hex_values = re.findall(r"0x([0-9A-Fa-f]{1,2})", data)
            if not hex_values:
                print("Error: No hex values found in C-array input")
                sys.exit(1)
            return bytes(int(h, 16) for h in hex_values)
        except ValueError as e:
            print(f"While parsing C-array, error: {e}")
            sys.exit(1)

    # Base64
    if fmt == "bs":
        try:
            return base64.b64decode(data)
        except (ValueError, base64.binascii.Error) as e:
            print(f"While parsing base64, error: {e}")
            sys.exit(1)

    print(
        "Error: Unknown format. Valid formats: "
        "bn (binary), hx (hexadecimal), ca (C-array), bs (base64)"
    )
    sys.exit(1)


# 3. XOR (same as encoder - XOR is symmetric)
def xor_with_key(data, key_str):
    """
    XOR the data with the key string. Same operation as encoding -
    XOR is its own inverse when the same key is used.
    """
    try:
        key = key_str.encode()
    except UnicodeError as e:
        print(f"While XORing data, error: {e}")
        sys.exit(1)

    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])


# 4. Writing decoded data to file
def save_file(filename, data):
    """
    Write decoded bytes to file, with overwrite prompt.
    """
    try:
        if os.path.exists(filename):
            answer = input(f"Warning file {filename} already exists, overwrite? (y/n): ").lower()
            if answer != "y":
                print("Aborting")
                sys.exit(0)
            else:
                print(f"Overwriting {filename}")
                with open(filename, "wb") as file:
                    file.write(data)
        else:
            print(f"Creating {filename}")
            with open(filename, "wb") as file:
                file.write(data)

    except OSError as e:
        print(f"While writing file, error: {e}")


# Ascii_art and parsers
def main():
    """Main entry point"""
    ascii_art = pyfiglet.figlet_format("GoldBaer  XOR-decode")
    print(Fore.CYAN + ascii_art + Style.RESET_ALL)

    parser = argparse.ArgumentParser(
        description=(
            "XOR-decoder by Swat. Reverses xor_tool.py.\n"
            "Example: xor_decode.py -i newshellcode.c -o shellcode.raw -e password123 -f ca"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-i", "--input-file",
                        required=True,
                        help="Path to XORed file to decode")
    parser.add_argument("-o", "--output-file",
                        required=True,
                        help="Filename for decoded output")
    parser.add_argument("-e", "--encryption-key",
                        required=True,
                        help="Encryption key used during XOR (same as encoding)")
    parser.add_argument("-f", "--format",
                        required=True,
                        help="Input format, choose between 'bn' binary, 'hx' hexadecimal, "
                        "'ca' C array or 'bs' Base64")

    args = parser.parse_args()

    ## 1. Read file
    data = load_file(args.input_file, args.format)

    ## 2. Parse format back to raw XORed bytes
    cipher = parse_input(data, args.format)

    ## 3. XOR with same key to decode
    plaintext = xor_with_key(cipher, args.encryption_key)

    ## 4. Write file
    save_file(args.output_file, plaintext)

    print("Decoding complete")


if __name__ == "__main__":
    main()
