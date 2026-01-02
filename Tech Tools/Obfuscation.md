## ROT 
So ROT 1 is moving the word 1 char , so the A becomes a B , sooooooooo ROT2 moves 2 and so on. 

## XOR
each word has a byte and the is a key , each word goes against that work byte by byte to then get out a complete diff word , 

Word XOR KEY = NEWWORD <this is reversable if you have the key>


ROT1 - common words look “one letter off”, spaces stay the same. Easy enough to detect.
ROT13 - Look for three-letter words. Common ones like  the become gur. And and becomes naq. spaces stay the same.
Base64 - Long strings containing mostly alphanumeric characters (i.e., A-Z, a-z, 0–9), sometimes with + or /, often ending in = or ==.
XOR - A bit more tricky. Looks like random symbols but stays the same length as the original. If a short secret was reused, you may notice a tiny repeat every few characters.

## Unfamiliar Patterns
Not sure what you’re looking at? It's fine. Even if you don't have an idea of what cipher was used, it is easy enough to keep on trying different operations just to see if the text becomes readable.

CyberChef also includes an operation called Magic that automatically guesses and tries common decoders for you. To use it, just add the Magic operation and look at the results. It will display multiple results and it's up to you to check which one ends up making sense. You can even check "Intensive mode" to make sure it tests more possibilities before giving up.