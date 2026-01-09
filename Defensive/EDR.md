# EDR

## what's an EDR

End-point detection and response

they protect the devices by detecting malware signatures , and anaomly behaviour and respond to it

## Features

### Visabilty

so this is what makes the EDR systems so special it collects dara from devices like the processes , registry modification and so much more and present them in a strucutred tree format wa in sequance that the analyst can view them easily and this also help in threat hunting

### Detection

It uses signature detection and behaviour anlysis and detection , where any deviation from the baseline will result in triggering and alerting , it maps out the detection with MITR techniques and tactics

### Response

An EDR enables the SOC analyst to take acton on the infected hosts , either by terminating , isolating or Remote access , all from the EDR Console



## EDR Vs AV

So Both provides security for the endpoint but the edr is more advances as it has more visability and behavioural detection  if for example an AV missed a virus due to obfusication as it checked i against the signature database and it came clean , the behaviour detection in the EDR won't

## how do EDR Works


AGENTS installed on the devices Collects Telemtry it can also detect and anlyise behaviour , it sends this data to the console , where it is shown on the dashboard for the analysis to use to make decisions


## Detection

Based on the telemetry received from the endpoints, some advanced detection techniques are applied to this data. Some of these techniques include:

1- Behavioral Detection
```
Instead of just matching the signatures with known threats, it observes the complete behavior of a file. Advanced threats craft their malware to look clean and use legitimate processes to carry out their attack. EDR catches this behavior.
Example: A process winword.exe spawning PowerShell.exe will be flagged by the EDR due to the behavior. A Word document spawning a PowerShell is an unusual parent-child relationship.
```
2- Anomaly Detection
```
With time, EDR understands the baseline behavior of the endpoints. Any activity that deviates from this behavior will be flagged. During any malicious activity, the endpoint's behavior deviates from normal. EDR picks it up. Sometimes, this can generate false positives as well. However, with the full context it gives, the analyst can identify its legitimacy.
Example: On one of the endpoints, a process modifies an auto-start registry key, which is not a common behavior on the endpoint.
```
3- IOC matching
```
EDRs have some strong threat intelligence field integrations. Except for zero-day attacks, most of the attacks have indicators published in the threat intelligence feeds. EDR flags any activity that matches any known IOC.  Example: A user downloads a file that drops an executable. The executable is often used in a specific attack. The hash of this executable will get matched with the threat intelligence feed and instantly flagged by the EDR.
```
4- MITRE ATT&CK Mapping
```
Any activity flagged by the EDR is not only marked as malicious or suspicious but also mapped with the MITRE Tactic and Technique (attack stage) that the particular activity was on. This proves to be very helpful for the analysts.
Example: If the EDR flags the creation of a scheduled task for any reason, it will likely map this activity to the following:
Tactic: Persistence
Technique: Scheduled Task/Job
```
5-Machine Learning Algorithms
```
Advanced threat actors try to evade defenses as much as possible, and their activities may sometimes bypass advanced detection techniques. Modern EDRs have machine learning models trained by a large dataset of normal and malicious behaviors. This can detect complex patterns of an attack.
Example: Attacks in which the individual actions are not inherently malicious, but the ML algorithm identifies the whole chain of activities as malicious. Fileless attacks and multi-staged intrusions are often detected through this.
```
## Response

The next step after any detection is the response. EDR offers both automated and manual responses. You can make policies to block known malicious behaviors automatically. However, manual response gives you a wide range of response capabilities. Let's discuss some of them.

1- Isolate Host
```
During any malicious activity on an endpoint, you can isolate that endpoint from the network through EDR. This is a very effective function for containing malicious activity. Most attacks start from a single endpoint and move laterally to other endpoints to compromise the whole network. Isolating the infected endpoint on time can stop this from happening.
```
2- Terminate Process
```
Not every malicious activity requires host isolation. Some hosts run the core business operations, and isolating them can cause more loss than the malicious activity. In such cases, terminating a process is enough to neutralize the malicious activity. The analysts get this option in the EDR. They can terminate any process at any time. This action should be taken consciously since terminating a legitimate process can disrupt the endpoint.
```
3- Quarantine
```
If a malicious file comes into the endpoint, it can be quarantined. Quarantine ensures that the file is moved to an isolated location where it can not be executed. The analysts can then review the file to restore or permanently remove it. 
```
4- Remote Access
```
Analysts can also remotely access the shell of any endpoint. This is often done when the EDR's built-in response is not enough to take action on a specific activity. Through remote access, analysts can gain deeper visibility into the system or take custom actions within the endpoints. The analysts can also run scripts or collect their desired data from the host through remote access.
Below is an example of CrowdStrike Falcon EDR's RTR (Real Time Response) console, which allows analysts to remotely access the shell of any endpoint and run commands and scripts.
CrowdStrike Falcon EDR's RTR (Real Time Response) console.
```
5- Artefacts Collection
```
Sometimes, the analysts may need to extract some data from the endpoints for detailed forensic investigation or reporting for legal actions. Analysts can extract important artefacts from the endpoints without physically accessing the device. The most commonly extracted artefacts include:
Memory Dump
Event Logs
Specific Folder Contents
Registry Hives
``` 