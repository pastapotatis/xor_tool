
Egna Noteringar:
Rent format på XOR skall vara utan backslash \ det är C som gör strängar med \, gör du det med C så avslutas koden med en 0a - kan bli lite konstigt så kör därför utan.

kompilera med gcc (finns ej i windows)
```
gcc filnamn.c -o kompileratfilnamn.exe
```

Visual studio community edition har en inbyggd kompilator.
cl loader


**Ladda ned GCC till VS**
Tryck på CTRL+Shift+X och ladda ned C++ extension pack
gå till :
https://code.visualstudio.com/docs/cpp/config-mingw


* basic felhantering skall finnas med i projektet


**Olika Errors:**
* FileNotFoundError

* PermissionError # Rättighetsfel ff.a linux ex. om sudo behövs. Får man ett PermissionError så tänk till vad scriptet vill göra

* TimeoutError

* KeyboardInterrupt # när man trycker ctrl+c

* raise TimeoutError -> Python skriver ut ett felmeddelande (traceback) om du inte fångar det.
	*  Du kan själv bestämma vad användaren ska se med try/except. ex. except TimeoutError: print("Det tog för lång tid!")


**Starta malwareVM**
Använd filen från Björn från github.
Klistra in XORen i shellcoden där det står att man ska kopiera in XOR-shellcoden, kompilera
```
gcc attack.c -o attack.exe
```
och kör filen i windows malware (säkerhetskopiera windows först).
.\attack.exe
hello from shellcode skall poppa upp.

Strängar i C skapar en slutsträng "\0" som kommer att bli XORad och då fungerar inte programmet.

Björns kod:
/* Byte key: */
0x41 kommer att ge samma resultat som:
/* String key: */
"google";
Endast två olika sätt för samma sak. Kommentera ut stringen om du kör hextal. Kommentera ut 0x41 om du kör kod som nyckel (sträng).

för att kompilera kan man köra strängen som finns i loader.c (som vi tankar ned)
kopiera kommandot:
"cl loader.c /Fe:loader.exe...."
kör i korrekt katalog så kompileras filen.
Kräver: Developer command prompt for VS 2022 eller Visual studio community installerat. 




Ta bort cachen om man råkat ladda upp .env på github
Föreläsning 2026-01-09 Tid: 2:03:00







----------------
# Shellcode XOR Encryptor i Python

## Projektöversikt

I detta slutprojekt ska du skapa ett verktyg som XOR-krypterar shellcode i Python.  
Målet är att bygga ett praktiskt, realistiskt säkerhetsverktyg som används som del i en payload-kedja, där:

- **Python-verktyget obfuskerar shellcoden**
- **ett separat loader-program (ofta byggt i C) avkrypterar och kör den**

Detta motsvarar hur riktiga red-teamers, malwareutvecklare och säkerhetsforskare arbetar.

---

# Mål med projektet

Du ska skapa ett CLI-verktyg som:

1. läser rå shellcode från en fil (binärt eller textformat)
2. XOR-krypterar shellcoden med en nyckel (1 byte eller flera)
3. producerar krypterad shellcode i olika output-format:
   - rå bytes
   - python-array
   - C-array (vanligast i malware/loader-kod)
4. använder argparse för att hantera argument
5. har dokumentation och exempel

Verktyget behöver **inte** kunna dekryptera shellcode.  
Dekryptering sker i *target loadern*, inte här.

---

# Varför används XOR-kryptering på shellcode?

XOR används för:

- att kringgå signaturbaserade antivirus
- att undvika byte-sekvenser som EDR letar efter
- att obfuska payload inför transport eller lagring
- att minimera möjligheten att verktyg som strings, YARA och binwalk upptäcker shellcode

**Detta är inte säker kryptering — det är obfuskering.**  
Men det fungerar effektivt mot enklare detektioner.

---

# Projektkrav

## Funktionalitet

Programmet ska kunna:

- läsa en fil med shellcode (t.ex. `raw.bin`)
- använda en XOR-nyckel (1 byte eller fler)
- generera krypterad shellcode
- spara den till fil samt kunna skriva ut i olika format:

Exempel:

```
python xorcrypt.py --in raw.bin --out encrypted.bin --key 0x42 --format c
```

Output som C-array:

```
unsigned char buf[] = { 0x12, 0xA1, 0x4F };
```

## CLI-argument (argparse)

Exempel på argument:

| Flagga     | Beskrivning                       |
| ---------- | --------------------------------- |
| `--in`     | Inputfil med raw shellcode        |
| `--out`    | Outputfil med krypterad shellcode |
| `--key`    | XOR-nyckel (hex eller string)     |
| `--format` | output-format: raw, python, c     |

**Inga subkommandon behövs.**

---

# Kodstruktur

- `main()` för argparse
- docstrings  
- informativa kommentarer  


---

# README-krav

Din README ska innehålla:

- kort beskrivning av verktyget
- hur man kör det
- exempelkommandon
- exempel på output-format ("ha inte med en hel array med källkod, räcker med en liten bit och snippa bort det sista")

---

# Inlämning

Lägg upp koden och readme på ditt github konto och lämna in länken