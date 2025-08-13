# _WARD — Live-state behavioural forensics & acquisition for Android
<img width="1366" height="768" alt="Artboard 1" src="https://github.com/user-attachments/assets/aeefb8f2-57de-402c-9216-41a94f6f26d2" />


**THIS TOOL IS IN BETA - PLEASE NOTE THAT FUNCTIONALITY AND HEURISTICS MAY HAVE ERRORS**

**WARD** is a modular, open-source, decentralised, distributed, offline, and privacy-respecting tool for **behavioral mobile forensics and acquisition** using Android ADB–accessible data. It's developed by [BARGHEST](https://barghest.asia), a non-profit organization aiming to support the democratization of threat intelligence in the majority world. 

It grabs and analyses a wide range of live-state system artifacts — crash logs, process and thread listings, diagnostic outputs, Wi-Fi manager logs, installed apps — to **preserve forensic evidence** and surface patterns that might indicate spyware or other unwanted activity.  

Instead of relying on vendor telemetry, malware signatures, or preloaded IOCs, WARD uses **heuristics** to spot anomalies like:
- abnormal wakelock usage
- unexplained battery drain
- location misuse
- persistent background processes
- memory crashes

This lets civil society, journalists, and investigators run **self-service device triage** — making spyware identification more readily available to the many.

---

## Two ways to use WARD

### 1. Self-service “kiosk” triage
WARD directly supports activists, journalists, and human rights defenders who think something’s up with their phone. Our simple, GUI-driven workflow walks you through a safe acquisition — no CLI, no rooting, no specialist training.  

It captures live-state and artifact data, then flags suspicious patterns as if a triage analyst has had a quick look at your device.

It will provide you an overal risk matrix, and guide you to look for certain things on your phone that might be suspicious.  Instead of relying on a “hunch” or waiting for help, you can immediately get a **forensic snapshot** that you can act on yourself or pass to a trusted analyst.

We encourage all users, where if in doubt, to reach out to an expert. You can also use the escalate function to escalate an issue to our team. Note that we are not a helpline or threat lab, but we can assist where our capacity allows.

*This tool is completely offline, we do not collect any data or telemetry, all of your data is retained on your computer alone and thus should be properly and securely handled by you. Note that since we rely purely on Android Debug data, *WARD does not aquire any PII (unless there's a PII leak by an app developer that enters your logs)**

---

### 2. Remote forensic acquisition for helplines & expert teams
For helplines, incident responders, and threat labs.  

We are heavily inspired by the successful work of [AndroidQF](https://github.com/botherder/androidqf) — but aiming to go further — WARD lets you avoid walking non-technical users through complex CLI tools. Our experience of having to remote share/call with victims is a high-friction situation that needs a solution. In addition, we aim to make sense of the complex data patterns within the forensics aquision, so that it can be distributed and understood by a wide range of analysts at all technical levels. 
When a at-risk HRD runs WARD, and it will:
- grab a full bugreport + key volatile data
- wrap it in a tamper-evident case archive
- make it easy to securely hand over offline
- generate a risk assessment JSON, that can be reviewed quickly by an analyst to get a low-down of the device.

This speeds up case intake, preserves volatile detail, and keeps data integrity intact.

---

## Why decentralised, distributed, offline matters
In much of the majority world, internet is slow, censored, risky, or unreliable — which in our experience, is not a safe bet during an active incident.  
Centralised forensic models are fragile and leave people behind.

WARD’s offline-first design means:
- **Wider reach** – anyone with a laptop + USB cable can investigate their own phone.
- **Local control** – evidence stays with the user until they choose to share it.
- **Resilience** – works in low-connectivity or high-threat situations.
- **Easy to distribute** – can be shared as a self-contained package via USB, SD card, or local network.

---

## The expert argument  
Some say putting forensic tools in non-technical hands is risky: evidence could be mishandled, results misread, assumptions mishandled.  
We, Barghest, challenge this for three reasons:

### 1. The cost of delay > the cost of empowerment
- Spyware cases move fast — volatile evidence disappears quickly.
- Waiting days or weeks for a helpline response or trained analyst can mean losing the only proof.
- Too often we rely on people coming in with a “feeling” something’s wrong with their device. i.e, weird restarts or crashes.
- Capturing a structured snapshot **in the moment** can be the difference between a confirmed case and a mystery.

### 2. Built for safety, not blind trust
- WARD isn’t a raw shell — it’s a guided workflow with guardrails.
- Everything is automated to reduce mistakes: data is hashed, timestamped, stored in a tamper-evident archive.
- Results are **signals**, not verdicts. We make it clear: no detection is 100% until a qualified analyst confirms it.

### 3. Decentralisation is the only way to scale
- There are more potential victims than forensic experts.
- Centralised, expert-only models simply can’t reach everyone in time.
- Distributing capability outward multiplies reach without multiplying risk.

---

**The alternative to empowering local actors is leaving them defenceless until outside help arrives — often too late, or never.**  

We believe that decentralised forensic tools like WARD aren’t here to replace experts — they extend their reach.

# GUIDE AND SETUP
<img width="1366" height="768" alt="guideandsetup" src="https://github.com/user-attachments/assets/de787667-e3cb-47e2-83d4-e431db8a7edf" />

