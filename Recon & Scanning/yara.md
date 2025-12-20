## Yara Rules

it's a tool that lets you check for patterns in files  , it's flexible where you can search for bytes , ints , strings

you can use it to identify behaviour and detect it , and you can create your own way of rules that detects what is malicious , but there is already a ton of rules out there from experts that was attacked once , but you can take them and adjust them based on your needs

you can use it post incident analysis
               Threat Hunting -> endpoint checking
               Memory anlysis
               Smart scans -> detection

the rule is built from 

meta data
strings
conditions


## Strings

it's the clues , the text , the bytes that the rule look for  , you can use arguments to search deeper

- nocase <Search using all the cases>
```
$string = "mamamia" nocase <searches for MAMAMIA MaMmia...>
```
- wide ascii <matchs the bytes of the word wide goes for 2 byte , ascii goes for 1 byte checks>
- xor <use it to unconcel anything that uses xor function to hide data>
- base64 <decodes anything that is base64 so in case of using encoding to concel data>
- {HEX VALUES,HEX} <Matches the Hex  value of the bytes>
- regex search <Helps you to detect stings that normal string and hex won't help you in like using the strings that is not written in a straight way>

## Conditions

Using what you want detect and the strings it gets you the string out

1- add the word only
2- two words using operators like and
3- any of them <if any of the strings detected>
4- all of them <stricter need them all to be there>
5- operators <like word x or word y and not word z>

Yara can also check properties , so you can use hash values , file sizes and so on

## practical
```
rule TBFC_Simple_MZ_Detect
{
    meta:
        author = "TBFC SOC L2"
        description = "IcedID Rule"
        date = "2025-10-10"
        confidence = "low"

    strings:
        $mz   = { 4D 5A }                        // "MZ" header (PE file)
        $hex1 = { 48 8B ?? ?? 48 89 }            // malicious binary fragment
        $s1   = "malhare" nocase                 // story / IOC string

    condition:
        all of them and filesize < 10485760     // < 10MB size
}
```
```
yara -r RUle.yar [Location]
icedid_starter  C:\Users\WarevilleElf\AppData\Roaming\TBFC_Presents\malhare_gift_loader.exe
```
We can use the man yara command to find out what flags could be useful in our scenario, and we find the following:
```
-r - Allows YARA to scan directories recursively and follow symlinks
-s - Prints the strings found within files that match the rule
```

