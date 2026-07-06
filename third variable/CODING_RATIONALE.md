# Cascade Heatmap — Coding Rationale

**Coding rule:** A cell is marked 1 (filled) only where public reporting confirms
*meaningful operational or data impact to that sector*. Cells stay 0 (empty) where a
sector was theoretically exposed but no realized sector-level cascade was documented.
This conservative rule means the heatmap under-counts rather than over-counts.

**Sectors:** Financial | Healthcare | Telecom | Government | Education | Logistics/Supply Chain | Energy/Utilities | IT/Cloud Services

**AI-era demarcation:** mid-2023 (WormGPT/FraudGPT public availability on criminal forums).
Events dated after this are coded `ai_era`.

---

## PRE-AI ERA

### SolarWinds (Dec 2020) — software supply chain
- Government: ✅ 9 federal agencies incl. Treasury, State, DHS, Energy, Pentagon (White House/NPR/GAO).
- IT/Cloud: ✅ Microsoft, Cisco, Intel, VMware, FireEye, Deloitte compromised.
- Healthcare: ✅ HHS Office for Civil Rights warned the sector; TechTarget HealthTechSecurity reporting.
- Energy/Utilities: ✅ Dept of Energy affected; critical-infrastructure/grid concern flagged (GAO, terrazone).
- Financial: ❌ NY DFS explicitly found financial-services firms were exposed but *not actively exploited* — kept empty per conservative rule (illustrative footnote candidate).

### Microsoft Exchange / ProxyLogon (Mar 2021) — zero-day, on-prem Exchange
- Broadest confirmed sector spread. S-RM: "banks, credit unions, telecommunication providers, public utilities, and police, fire, and rescue units." Plus higher-ed, defense, local government (Wikipedia, CSO, FireEye/Mandiant).
- Financial ✅ (banks, credit unions); Healthcare ✅ (disease researchers, health orgs); Telecom ✅; Government ✅ (local govts, police/fire); Education ✅ (universities); Energy/Utilities ✅ (public utilities); IT/Cloud ✅ (Exchange infrastructure itself).
- Logistics: ❌ no specific documented logistics-sector cascade.

### Kaseya VSA (Jul 2021) — MSP software supply chain (REvil)
- IT/Cloud ✅ (60 MSPs, the core mechanism); Retail→Logistics/Supply Chain ✅ (Coop, 800 stores closed; POS disabled); Education ✅ (11 NZ schools); Government ✅ (a town in Maryland).
- Also Swedish State Railway (transport) — folded into Logistics.
- Financial/Healthcare/Telecom/Energy: ❌ not specifically documented at sector level.
- NOTE: Coop is grocery *retail*. Coded under Logistics/Supply Chain as the nearest column;
  worth flagging to user — a "Retail" column could be added if desired.

### Log4j / Log4Shell (Dec 2021) — ubiquitous library RCE
- Special case: a *vulnerability*, near-universal in Java stacks, not a single cascade.
- IT/Cloud ✅ (AWS, Azure, GCP, VMware, hundreds of millions of devices).
- Government ✅ (Belgian Ministry of Defense confirmed breached via Log4Shell).
- Others: exploited broadly but concrete *sector-level operational cascades* poorly documented →
  kept empty per conservative rule. This is the clearest "under-counted" row; belongs in a footnote.

### LastPass (Aug 2022) — credential/vault theft
- IT/Cloud ✅ (source-code + vault-backup theft; later tied to $150M crypto heist).
- No documented sector-level operational cascade; primarily end-user credential exposure.
- All other sectors ❌. Illustrates credential-cascade potential, not realized multi-sector disruption.

### Okta / Lapsus$ (Oct 2022) — identity provider compromise
- IT/Cloud ✅ (Okta itself; Cloudflare, BeyondTrust targeted).
- HIGH cascade *potential* (identity provider) but LOW *realized* impact: final Okta investigation
  found 366 customers exposed, only 2 tenants actually accessed in the window, no cross-sector
  operational cascade. Kept all non-IT sectors empty. Strong footnote candidate: "potential ≠ realized."

---

## AI ERA (mid-2023 →)

### 3CX (Mar 2023) — double software supply chain
- IT/Cloud ✅ (comms software, the mechanism); Telecom ✅ (VoIP/phone-system software).
- Financial ✅ (downstream payload specifically hit cryptocurrency firms); Government ✅ (defense-sector targeting per MITRE; NHS among customer base).
- NOTE: initial trojan spread to many verticals, but the *second-stage cascade payload* only
  landed on crypto + defense targets. Coded narrowly to realized cascade, not the broad install base.

### MOVEit Transfer (Jun 2023) — managed file transfer zero-day (Cl0p)
- Broadest AI-era spread. 2,700+ orgs. Emsisoft sector breakdown: education 39%, health 20%, finance/professional 13%.
- Financial ✅; Healthcare ✅; Telecom ✅ (Ofcom, ComReg); Government ✅ (DoE, state DMVs, TfL); Education ✅ (Johns Hopkins, Univ System of Georgia); Logistics ✅ (British Airways, Aer Lingus, TfL); Energy/Utilities ✅ (Shell, US DoE); IT/Cloud ✅ (the MFT platform itself).
- Effectively all-sector — consistent with a "hydra-headed" file-transfer breach.

### Change Healthcare (Feb 2024) — ransomware on claims clearinghouse
- Healthcare ✅ (largest US healthcare breach; ~190M people; 94% of hospitals reported financial impact).
- Financial ✅ (claims/payment processing halted; $6.3B claims value drop in 3 weeks; provider cash-flow collapse — this is a financial cascade via healthcare payments).
- IT/Cloud ✅ (Change is the centralized platform).
- Retail-pharmacy: 90%+ of 70,000 pharmacies forced to manual workarounds — pharmacy dispensing.
  Coded under Healthcare (closest); a Retail column would also capture this.
- Others ❌.

### CrowdStrike (Jul 2024) — faulty security update
- Widest cross-sector cascade in the set. Financial ✅ (banks worldwide, $1.15B); Healthcare ✅ ($1.94B, hardest hit); Telecom ✅ (telecom providers' IT ops, though networks stayed up); Government ✅ (public safety/911, federal agencies); Logistics ✅ (aviation — 16,896 flights cancelled — plus shipping); Energy/Utilities ✅ (gas stations, utilities per Wikipedia/case studies); IT/Cloud ✅ (the mechanism).
- Education: ❌ not prominently documented as a distinctly affected sector → kept empty (conservative).

### Blue Yonder (Nov 2024) — ransomware on SCM platform
- Logistics/Supply Chain ✅ (core: warehouse mgmt, Morrisons, Sainsbury's, P&G TMS, BIC shipping).
- Retail ✅ (Starbucks scheduling/payroll; grocery shelves) — coded under Logistics as nearest; Retail column would fit better.
- IT/Cloud ✅ (the SaaS platform).
- Others ❌. Notably contained to supply-chain/retail despite large client roster.

### Canvas/Instructure (May 2026) — ransomware on LMS (ShinyHunters)
- Education ✅ (8,809 institutions; 41% of NA higher-ed; finals-week outage; K-12 + universities).
- Government ✅ (US Dept of Education / Federal Student Aid coordinating; FERPA review) — coded 1 as the regulatory/government layer was directly engaged; borderline, could be argued as education-only.
- IT/Cloud ✅ (the platform).
- Others ❌. Single-sector-dominant but massive within it. Most recent AI-era anchor.

---

## Known coding tensions (surface these to the user)
1. **No Retail column.** Coop (Kaseya), Starbucks/grocers (Blue Yonder), pharmacies (Change Healthcare)
   are retail-adjacent and currently absorbed into Logistics or Healthcare. Adding a Retail column
   would make several rows more accurate. Flagged for user decision.
2. **Log4j & Okta are "potential >> realized" rows.** Coded conservatively; both deserve a narrative
   footnote so the heatmap's sparse rows aren't misread as "low severity."
3. **Government cell on Canvas** is the single most debatable fill (regulatory engagement vs. direct
   operational hit). Easy to toggle off if the user prefers strict operational-impact coding.
