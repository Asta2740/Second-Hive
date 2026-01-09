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
![Process](<../Supporting Pictures/SOC Process.png>)

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




## WorkBooks and Lookups

# LookUps

- Identity Inventory
    catalogue of user accounts , service acconts and their privilege and role in the system and what can they access to get a context of the accounts you see in the alerts
- Sources
    AD
    HR
    SSO
    Custom solution like csv , excel sheets

- Asset inventory
    The info regarding the computing resources of the company , the workstations , cloud services , vendor services
- Sources
    AD
    SIEM
    Mobile device managment services
    Custom solutio like excel sheets

- Network Diagram
    A network diagram with the company infrastrucutre , to give the bigger picutre on the organization network , what services , ports , subnets and so on , instead of looking at an excel sheet trying to figure out what goes where


# Workbooks

they're like the processes of the company what  is done and when 
it's a structured document that defines the steps required to investigate and remediate specific threats efficiently and consistently

![SOC Workbook](<../Supporting Pictures/SOC Workbook.png>)


# Metrics and objectives

Alert count     Overall tickets
FP Rate         Level of false positives and noise
Alert Esclation         Level of Experince of the Soc L1 team
Threat Detection rate       Probablity of soc team to detect and intrusion


AC   needs to be at 5 - 30 per day per analyst
FP rate  Should not exceed 80%
Esclation rate , ideal below 50% best below 20%
threat detection needs to be at 100%


You have 
SLA to stay within 
the MTTD , MTTA , MTTR

# improvments for metrics

Issue	
Recommendations

False Positive Rate over 80%

	Your team receives too much noise in the alerts. Try to:
1. Exclude trusted activities like system updates from your EDR or SIEM detection rules
2. Consider automating alert triage for most common alerts using SOAR or custom scripts


Mean Time to Detect over 30 min

	Your team detects a threat with a high delay. Try to:
1. Contact SOC engineers to make the detection rules run faster or with a higher rate
2. Check if SIEM logs are collected in real-time, without a 10-minute delay


Mean Time to Acknowledge over 30 min

	L1 analysts start alert triage with a high delay. Try to:
1. Ensure the analysts are notified in real-time when a new alert appears
2. Try to evenly distribute alerts in the queue between the analysts on shift


Mean Time to Respond over 4 hours

	SOC team can't stop the breach in time. Try to:
1. As L1, make everything possible to quickly escalate the threats to L2
2. Ensure your team has documented what to do during different attack scenarios


## Phishing simulator

Overall analysis

Powered by AI
Your reports provide a good level of detail, but there are areas for improvement in clarity and completeness. While you have covered the 'Who' and 'What' aspects well, the 'When' is consistently mentioned but could be more effectively integrated into the narrative. The 'Where' is somewhat addressed through IP addresses and email domains, but it could be clearer how these locations relate to the incidents. Additionally, the 'Why' behind the escalation decisions could be more explicitly connected to the potential impact or risk level. Enhancing these areas will improve the overall comprehensiveness and clarity of your reports.