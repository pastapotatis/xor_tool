"""
Simple XOR obfuscation tool for binary files.
"""

import argparse
import sys
import os
import base64

import pyfiglet
from colorama import Fore, Style

# 1. Read file
def load_file(filename):
    """
    Load a file from disk and return its raw bytes.
    """
    if not os.path.exists(filename):
        print(f"Error, can't find filename: \"{filename}\"")
        sys.exit(1)

    try:
        with open(filename, "rb") as file:
            return file.read()
    except OSError as e:
        print(f"While reading file, error: {e}")
        sys.exit(1)

# 2. XOR Code

def xor_with_key(data, key_str):
    """
    XOR the code with the key string (key_str) of users choosing.
    """
    try:
        key = key_str.encode()  # gör om sträng → bytes
    except UnicodeError as e:
        print(f"While XORing code, error: {e}")
        sys.exit(1)

    key_len = len(key)
    return bytes([data[i] ^ key[i % key_len] for i in range(len(data))])

# 3. Format output
def format_output(data: bytes, fmt: str) -> bytes:
    """
    Format XORed data into one of the supported output formats:

        bn - raw binary
        hx - hexadecimal string
        ca - C array
        bs - Base64
    """
    fmt = fmt.lower()

    # Raw binary, no conversion
    if fmt == "bn":
        return data

    # Hexadecimal
    if fmt == "hx":
        hex_str = data.hex()
        return hex_str.encode()

    # C-array format
    if fmt == "ca":
        hex_values = ", ".join(f"0x{b:02X}" for b in data)
        c_array = f"unsigned char buf[] = { hex_values };"
        return c_array.encode()

    # Base64
    if fmt == "bs":
        return base64.b64encode(data)

    print(
        "Error: Unknown format. Valid formats: "
        "bn (binary), hx (hexadecimal), ca (C-array), bs (base64)"
    )
    sys.exit(1)

# 4. Writing XORed code to file
def save_file(filename, data):
    """
    Writing XORed code to filename.any-extension, with overwrite prompt.
    """
    try:
        if os.path.exists(filename):
            answer = input(f"Warning file {filename} already exists, overwrite? (y/n): ").lower()
            if answer != "y":
                print("Aborting")
                sys.exit(0)
            else:
                # Overwriting existing file
                print(f"Overwriting {filename}")
                with open(filename, "wb") as file:
                    file.write(data)
        else:
            # File does not exist, creating file
            print(f"Creating {filename}")
            with open(filename, "wb") as file:
                file.write(data)

    except OSError as e:
        print(f"While writing file, error: {e}")

# Ascii_art and parsers
def main():
    """Main entry point"""
    ascii_art = pyfiglet.figlet_format("GoldBaer  XOR-tool")
    print(Fore.YELLOW + ascii_art + Style.RESET_ALL)

    parser = argparse.ArgumentParser(
        description=(
            "XOR-tool by Swat. Note: This is not a secure encryption method,"
            "this is only obfuscation!\n"
            "Example: xor_tool.py -i shellcode.raw -o newshellcode.c -e password123 -f ca"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-i", "--input-file",
                        required=True,
                        help="Path to file to XOR")
    parser.add_argument("-o", "--output-file",
                        required=True,
                        help="New XORed filename")
    parser.add_argument("-e", "--encryption-key",
                        required=True,
                        help="Encryption key (any string)")
    parser.add_argument("-f", "--format",
                        required=True,
                        help="Output format, choose between 'bn' binary, 'hx' hexadecimal, "
                        "'ca' C array or 'bs' Base64")

    args = parser.parse_args()


    ## 1. Read file
    data = load_file(args.input_file)

    ## 2. XOR
    cipher = xor_with_key(data, args.encryption_key)

    ## 3. Output format
    formatted = format_output(cipher, args.format)

    ## 4. Write file
    save_file(args.output_file, formatted)

    ## 5. Selfest if encryption == decryption is True
    try:
        decrypted = xor_with_key(cipher, args.encryption_key)
    except UnicodeError as e:
        print(f"While decryption test, error: {e}")


    if decrypted == data:
        print("Encryption successful")
    else:
        print("Encryption/decryption did not match or other error")


if __name__ == "__main__":
    main()
