# 05 Roadmap (estimates, not promises)
Full build: 9-12 months with a small team, 12-18 solo. Critical path = data, hardware, government approvals.

| Phase | When | Goal | Exit criteria |
|---|---|---|---|
| 0 Demo MVP | Days 1-30 | Red-light only, 1 intersection, recorded video, full review-to-e-Challan flow | Live e2e demo + metrics report |
| 1 Data + ANPR v1 | Months 2-3 | 5k-10k labeled plates (Devanagari+English, day/night/dirty); fine-tuned detector + OCR | >=90% plate-level accuracy on held-out set |
| 2 Hardware prototype | Months 3-4 | Jetson, global-shutter cam, IR, signal interface, UPS, enclosure | 72h offline buffer + power-cut recovery pass |
| 3 Shadow pilot | Months 4-6 | 1 real intersection, 4-8 weeks, NO fines issued | Precision >=95% red-light; FP log reviewed with police |
| 4 Expand + compliance | Months 6-9 | Speed (radar+homography), helmet, wrong-way; real DoTM; GIDC; pen test; legal basis | Per-violation accuracy reports; signed approvals |
| 5 Multi-site | Months 9-12 | 5-10 intersections, OTA, fleet monitoring, training | 30 days stable at uptime target |

## Parallel tracks (start day 1)
Data (never stop collecting) | Approvals (MoU for shadow pilot by month 3) | Hardware (off-the-shelf Jetson + IP cam) | Software.

## Phase 0 week plan
- Week 1: repo, CI + security scanners, threat model, JSON contract, server skeleton, mock DoTM, sample video + start plate collection.
- Week 2: detection + tracking, stop-line + signal logic, evidence packaging/hash/sign.
- Week 3: plate detector + OCR (English then Devanagari), dashboard, e-Challan PDF + QR.
- Week 4: mTLS sync + offline outbox, Jetson optimization (if hardware), demo script, metrics report (precision/recall).

## Speed-ups
One violation type first; shadow mode; ready-made radar/cameras; pretrained models then fine-tune; active-learning loop
(officer OCR corrections become training data); mock what is not yet available; defer helmet/speed.

## Top risks
Government approval delays (+3-6 months), Devanagari data shortage, signal-controller access, night/rain performance,
legal uncertainty on automated fines.
