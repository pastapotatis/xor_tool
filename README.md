# Shellcode XOR Encryptor (Python)

Ett CLI‑verktyg skrivet i Python som läser rå shellcode från en fil, XOR‑krypterar den med en valfri nyckel och genererar output i flera format. Verktyget används som del i en payload‑kedja där en separat loader (ofta i C) avkrypterar och kör den.

Detta projekt är skapat i utbildningssyfte för att demonstrera obfuskeringstekniker som används inom säkerhetsforskning och red‑teaming.

---

## ✨ Funktioner

- Läser rå shellcode från fil (.bin eller textformat)
- XOR‑krypterar med valfri nyckel (1 byte eller fler)
- Exporterar i flera format:
  - Rå bytes → sparas som .bin
  - Python‑array
  - C‑array
- CLI‑gränssnitt via argparse
- Grundläggande felhantering
- Tydlig och ren output för användning i loaders

---

## 🔒 Varför XOR‑kryptering?

XOR används inte som säker kryptering, utan som obfuskering.  
Det hjälper till att:

- undvika byte‑sekvenser som EDR letar efter
- kringgå enklare signaturbaserad detektion
- göra shellcode svårare att identifiera i transit
- minska träffar i verktyg som strings, YARA och binwalk

---

## 📦 Installation

Kräver Python 3.8+.






XOR Tool - by GoldBaer

A lightweight command‑line utility for XOR‑encoding and decoding binary data.
This tool is intended for obfuscation, not cryptographic security. It is useful for transforming shellcode, payloads, or any raw byte sequence into different output formats.

The tool supports the following output formats:

    bn – raw binary
    hx – hexadecimal string
    ca – C‑array
    bs – Base64


    Features

    XOR any file with a user‑defined key

    Multiple output formats

    Automatic overwrite protection

    Self‑test to verify if encryption is successful

    Clean and simple CLI interface


Usage

Basic syntax:
```python xor_tool.py -i <input-file> -o <output-file> -e <key> -f <format>
```

Arguments
Flag	Long Option	      Description
-i	  --input-file	    Path to the file you want to XOR
-o	  --output-file	    Output filename
-e	  --encryption-key	XOR key (any string)
-f	  --format	        Output format: bn, hx, ca, bs


Examples
XOR to raw binary with flag
```
python xor_tool.py -i payload.bin -o encoded.bin -e secret123 -f bn
```

With long option
```
python xor_tool.py --input-file shellcode.raw --output-file shellcode.c --encryption-key secret123 --format ca
```

Output Format Example C array
unsigned char buf[] = {
    0x8F, 0x9F, 0x07, 0x73, 0x12, 0x6F, 0x01, ...
};


Verification

After writing the output file, the tool performs a self‑test by XOR‑decoding the data again and checking if it matches the original input:

"Encryption successful"

If data does not match:
"Encryption/decryption did not match or other error"




Disclaimer

This tool is not intended for secure encryption.
XOR with a repeating key is trivial to reverse and should only be used for obfuscation or educational purposes.