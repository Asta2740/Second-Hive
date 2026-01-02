1) HOST: http://10.81.155.178/ – PORT 80
Discovered Endpoints
Path	Status	Notes
/cgi-bin/	301 → redirect	Likely outdated CGI scripts → exploit potential
/index.html	200	Size: 19522 bytes (served twice; duplicate scan result)
/success.html	200	Size: 179 bytes
Observed Output

Username clue: Hopkins

Old password: Pizza1234$

Successful access → THM{ACCESS_PLACEHOLDER_FLAG}

2) HOST: http://10.81.155.178/ — PORT 8000

Framework identified: Django

Endpoints
Endpoint	Status	Size	Notes
/admin	200	1910	Django admin panel
/chat	200	6263	Likely user posts
/posts	200	6265	Blog-like content
/profiles	200	6271	User profiles
Account Created

Username: Test

Password: !Test123

3) CHARACTERS / NPC DATA (Narrative Clues)

Guard Hopkins

King Malhare

SirCarrotbane

Sir BreachBlocker III

Likely puzzle or enumeration hints for later challenges.

4) PERSONAL FACTS ABOUT HOPKINS

Should be treated as password reset / social engineering intelligence.

Born 1982 → age ≈ 43

Loves pizza

Has a dog named Johnnyboy

Says he has “more” friends — brag

Email: guard.hopkins@hopsecasylum.com

Password patterns may include:
Pizza1982!, Johnnyboy82, Hopkins1982$, etc.
Password Johnnyboy1982!

5) TOOLING HINT PROVIDED

/opt/hashcat-utils/src/combinator.bin
→ Combine wordlists (likely pizza + year + names)

6) CLIENT-SIDE VULNERABILITY
main.js
localStorage.setItem('hopsec_role', 'admin')


→ Client-side trust = broken security model

Setting this allows admin view access.

HTML BYPASS

The login was entirely cosmetic:

document.getElementById("loginWindow").style.display = "none";
document.getElementById("mapScreen").style.display = "block";


Just hide login & show the protected div → instant access.

7) FLAGS IDENTIFIED SO FAR
Flag	Location
THM{h0pp1ing_m4d}	From client-side bypass
THM{ACCESS_PLACEHOLDER_FLAG}	From initial login
