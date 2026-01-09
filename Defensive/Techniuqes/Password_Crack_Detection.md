## Detection of Indicators and Telemetry

Process creation: Password cracking has a small set of well-known binaries and command patterns that we can look out for. A mix of process events, file activity, GPU signals, and network touches tied to tooling and wordlists. Our goal is to make the activity obvious without drowning in noise.

    Binaries and aliases: john, hashcat, fcrackzip, pdfcrack, zip2john, pdf2john.pl, 7z, qpdf, unzip, 7za, perl invoking pdf2john.pl.
    Command‑line traits: --wordlist, -w, --rules, --mask, -a 3, -m in Hashcat, references to rockyou.txt, SecLists, zip2john, pdf2john.
    Potfiles and state: ~/.john/john.pot, .hashcat/hashcat.potfile, john.rec.

SOC setting with analysts performing monitoring and investigation of various alerts. It's worth noting that on Windows systems, Sysmon Event ID 1 captures process creation with full command line properties, while on Linux, auditd, execve, or EDR sensors capture binaries and arguments.

### GPU and Resource Artefacts

GPU cracking is loud. Sudden high utilisation on hosts can be picked up and would need to be investigated.

    nvidia-smi shows long‑running processes named hashcat or john.
    High, steady GPU utilisation and power draw while the fan curve spikes.
    Libraries loaded: nvcuda.dll, OpenCL.dll, libcuda.so, amdocl64.dll.

### Network Hints, Light but Useful

Offline cracking does not need the network once wordlists are present. Yet most operators fetch lists and tools first.

    Downloads of large text files named rockyou.txt, or Git clones of popular wordlist repos.
    Package installs, for example apt install john hashcat, detected by EDR package telemetry.
    Tool updates and driver fetches for GPU runtimes.

## Unusual File Reads

Repeated reads of files such as wordlists or encrypted files would need analysis.

## Detections

Below are some examples of detection rules and hunting queries we can put to use across various environments.

## Sysmon:
```
(ProcessName="C:\Program Files\john\john.exe" OR
 ProcessName="C:\Tools\hashcat\hashcat.exe" OR
 CommandLine="*pdf2john.pl*" OR
 CommandLine="*zip2john*")
```
## Linux audit rules, temporary for an investigation:
```
auditctl -w /usr/share/wordlists/rockyou.txt -p r -k wordlists_read
auditctl -a always,exit -F arch=b64 -S execve -F exe=/usr/bin/john -k crack_exec
auditctl -a always,exit -F arch=b64 -S execve -F exe=/usr/bin/hashcat -k crack_exec

```
## Sigma style rule, Windows process create for cracking tools:
```
title: Password Cracking Tools Execution
id: 9f2f4d3e-4c16-4b0a-bb3a-7b1c6c001234
status: experimental
logsource:
  product: windows
  category: process_creation
detection:
  selection_name:
    Image|endswith:
      - '\john.exe'
      - '\hashcat.exe'
      - '\fcrackzip.exe'
      - '\pdfcrack.exe'
      - '\7z.exe'
      - '\qpdf.exe'
  selection_cmd:
    CommandLine|contains:
      - '--wordlist'
      - 'rockyou.txt'
      - 'zip2john'
      - 'pdf2john'
      - '--mask'
      - ' -a 3'
  condition: selection_name or selection_cmd
level: medium
```