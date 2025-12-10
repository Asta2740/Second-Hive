## Who is a SOC l1

So basically the Security analyst Aka SOC L1 is the janitor of the alerts , they get all the garbage in , and filter the real violations or just add a report regarding the stuff that can be discarded

They need to aware of the security news all around as new vulenrabilities appear out of thin air so they should be able to handle a decent amount of pressure when a new security exploit appear and regarding their whole life in general

Security operation center AKA SOC Team

SOC L1 - > filters alerts
SOC L2 - > investigate alerts in more details that was esclated from L1
SOC manager - > manages the pipline of the soc team
SOC engineer - > Handles the deployment and adjustments of tools
Incident responder  - > Hunt threats from incidents and respond to them <-- this shows you i have no clue what they do specifally 

all part of a big happy blue team protecting the company day and night like vigilanties 

A SOC L1 needs a couple of skills
Team coperation
Technical analysis to triage alerts
Ability to keep learning
Clear communicator <-- if you cannot communicate this will be a bottle neck in the team>


now the tools they use

SEIM <-- the big ol Log collector , collecting them like pokemons and prasing them like a nerd going through his collection>
EDR/NDR <-- endpoint/network Detection response>
SOAR <-- collection of tools to centeralise the SOC operations>
Ticketing systems  <-- if i have to explain this you should just change careers at this point>

## alert triage

L1 reviews and distingusih bad from good aka false postives from true postives
L2 perform a deeper analysis than L1 on the esclated tickets 
and eingineers ensure the alerts have sufficent information required
managers track speed and quality of alerts

## Alert priotraization

filter so you dont work on the same alerts as your team mates
priotrize tasks based on severity 
and oldest alerts are firrst before new alerts but this is subjective as the new alerts may have a higher severity

## SOC proccess

take by priority
check if there is a work book for the case 
Need esclation ?
Add a comment and close

(there is a stuff in the middle but you know them like those if situations)

## investigation 

Here you use your technical knowledge to investigate

some teams develop worbooks known as playbooks instructins on how to investigate specific alerts

if there is no play book then do as the following my guy

1 note who is under attack
2- description of the alert check it as it usually tells you what might be done
3- check severity
4- any additional info needs to be tracked and depends on the alert you got , maybe a file or so use investigative platforms , check surrounding events 


## alerts reporting and esclation

so reporting matters as

1- save time for anyone who will review it or if it was esclated then a the L2 doesnt start from scratch 
2- alerts are saved , raw logs arent , so all the needed info needs to be in the alerts
3- if you cant explain an attack simply then you dont understand it well enough


now regarding the esclation

you esclate the alerts if 

1 - the alert is an indicator of a major attack
2- redemtion actions  are required like a malware removal , host isolation , password reset
3- communication with law enforsment , customer , partenrers is required
4- you dont fully understand the alert and need help from a senior , its okay to ask for help


now in your reporting never forget the 5w's

When
who
where
what
why


now examples on communication

Communication Cases
•	You need to escalate an urgent, critical alert, but L2 is unavailable and does not respond for 30 minutes.
Ensure you know where to find emergency contacts. First, try to call L2, then L3, and finally your manager.
•	The alert about Slack/Teams account compromise requires you to validate the login with the affected user.
Do not contact the user through the breached chat - use alternative contact methods like a phone call.
•	You receive an overwhelming number of alerts during a short period of time, some of which are critical.
Prioritise the alerts according to the workflow, but inform your L2 on shift about the situation.
•	After a few days, you realise that you misclassified the alert and likely missed a malicious action.
Immediately reach out to your L2 explaining your concerns. Threat actors can be silent for weeks before impact.
•	You can not complete the alert triage since the SIEM logs are not parsed correctly or are not searchable.
Do not skip the alert - investigate what you can and report the issue to your L2 on shift or SOC engineer.
