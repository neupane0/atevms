# 01 Project Overview & Nepal Constraints

## Mission
Edge-AI Smart Traffic Camera + automated e-Challan platform for Nepal intersections. Goal: field-testable
MVP/PoC for Nepal Police Traffic Directorate, municipalities (Kathmandu/Lalitpur/Biratnagar), DoTM, DoR.
Replaces manual policing with automated, tamper-evident violation detection and digital fines.

## Honest scope statement
A demo-grade MVP is a 30-day goal. A legally defensible, multi-violation, multi-site pilot is ~9-18 months
(see `05_ROADMAP.md`). Never claim "field-tested" or "legally admissible" before shadow-mode pilot results exist.

## Nepal-specific constraints (design for ALL of these)
1. Plates:
   - Legacy zonal Devanagari, e.g. `बा. २ च १२३४`, `को. १ प ५६७८` (painted/embossed, faded, non-standard fonts)
   - Provincial Devanagari, e.g. `प्रदेश ३-०१-०२२ च ५६७८`, `कोशी प्रदेश ०१-००१ प १२३४`
   - Embossed English, e.g. `B AA 1234`
   - Colour indicates category (private/public/government/tourist/diplomatic).
     TODO(verify): confirm the current official colour scheme with DoTM. Earlier notes were inconsistent
     (private listed white/black but a sample payload used RED_WHITE for a motorcycle). Do not hard-code until verified.
2. Traffic: dense two-wheelers weaving between lanes, cars, microbuses, trucks, tempos/e-rickshaws. LEFT-hand traffic.
3. Infrastructure: power instability (LiFePO4/UPS, graceful low-power), poor bandwidth (edge inference only; send
   only JSON + crops + ~5s clip), offline buffering up to 72h on NVMe with store-and-forward sync.
4. Sovereignty/legal: all citizen data, lookups, media on servers physically in Nepal (e.g., GIDC).
   Media hashed (SHA-256) at capture and signed. TODO(verify): legal basis for camera-evidence e-challans
   (Motor Vehicles and Transport Management Act), Privacy Act 2018, Electronic Transactions Act. Needs a Nepali lawyer.

## Stakeholders
Nepal Police Traffic Directorate, DoTM, DoR, municipalities. Officers are the human-in-the-loop for every fine.
