# Po Dead Code Analysis — BlackJack COBOL Estate
**Generated:** 2026-03-09
**Analyst:** Po (COBOL Analysis Agent)
**Source folder:** `blackjack/source/`
**Modules analysed:** 8

---

## Summary

| Category | Count |
|----------|-------|
| Commented-out dead paragraphs | 7 |
| Active but unreachable paragraphs | 2 |
| Declared but unused working-storage variables | 5 |
| Effectively dead active code (no-ops / broken stubs) | 4 |
| Data passed to dead modules (never processed) | 2 |
| **Total dead code items** | **20** |

---

## 1. Commented-Out Dead Paragraphs

These paragraphs exist in source but are commented out and will never execute. They represent features that were disabled or removed — often without explanation of whether they should be re-enabled or permanently deleted.

### 1.1 BJACK-MAIN — `PROC-SP` (Split Hand Entry Point)
**File:** `bjack-main.cob` lines 135–142
**Disabled:** MGR NOTE 09/87 — "NOT ACTIVE"
**What it did:** Entry point for split hand play. Accepted a split bet, dealt to a second hand slot, and routed to `LOOP-A`.
**Status:** Feature was never completed. BJACK-DEAL's corresponding `PROC-DS` was also removed (see 1.2). Re-enabling this without implementing the full split flow would cause a crash.
```cobol
*  PROC-SP -- SPLIT HAND ENTRY POINT. NOT ACTIVE PER MGR NOTE 09/87
*   PROC-SP.
*       MOVE 'Y' TO WS-SP
*       MOVE WS-BET TO WS-BET       ← no-op: assigns field to itself
*       CALL 'BJACK-DEAL' ...
```

---

### 1.2 BJACK-DEAL — `PROC-DS` (Deal to Split Hand)
**File:** `bjack-deal.cob` lines 61–67
**Disabled:** "REMOVED 10/87 SPLIT NOT TESTED"
**What it did:** Dealt a card to a third hand slot (`WS-SS`/`WS-SV`) for split hand play.
**Note:** The comment reads "ACHTUNG: KARTENLOGIK NACH AENDERUNG NICHT GETESTET 08/88" (German: card logic not tested after change). Three different languages appear in comments across this codebase — English, German, French — suggesting multiple development teams or contractors.
```cobol
*  PROC-DS -- DEAL TO SPLIT HAND. REMOVED 10/87 SPLIT NOT TESTED
*   PROC-DS.
*       ADD 1 TO WS-SC
*       MOVE WS-S1(WS-CT1) TO WS-SS(WS-SC)
```

---

### 1.3 BJACK-SCORE — `PROC-CB` (Five-Card Charlie Bonus)
**File:** `bjack-score.cob` lines 81–87
**Disabled:** "NEVADA RULE. DROPPED 06/88"
**What it did:** Awarded double bet payout when player reached 5 cards without busting (Nevada casino bonus rule).
**Impact:** `WS-CB` (Charlie Bonus Flag) was declared in WORKING-STORAGE for this feature and is now permanently orphaned.
```cobol
*  PROC-CB -- FIVE CARD CHARLIE BONUS. NEVADA RULE. DROPPED 06/88
*   PROC-CB.
*       IF WS-PC = 5 AND WS-PT < 22
*           MOVE 'Y' TO WS-STAT
*           COMPUTE WS-BAL = WS-BAL + WS-BET * 2
```

---

### 1.4 BJACK-DEALER — `PROC-INS` (Insurance Offer)
**File:** `bjack-dealer.cob` lines 75–81
**Disabled:** "DISABLED 1988"
**What it did:** Offered the player insurance when the dealer's first card was an Ace.
**Note:** The trigger condition (`WS-DS1(1) = 'A'`) is correct — but the routing after acceptance was never implemented. The `ACCEPT WS-INS` stores the response but there's no follow-up logic.
```cobol
*  PROC-INS -- INSURANCE OFFER WHEN DEALER SHOWS ACE. DISABLED 1988
*   PROC-INS.
*       IF WS-DS1(1) = 'A'
*           DISPLAY '   INSURANCE? Y/N:'
*           ACCEPT WS-INS
*       END-IF
*       GO TO LOOP-A.   ← never handled the Y/N response
```

---

### 1.5 BJACK-DISPL — `CALC-8`, `CALC-8A`, `CALC-8X` (Split Hand Display)
**File:** `bjack-displ.cob` lines 279–291
**Disabled:** Removed alongside split hand feature
**What it did:** Displayed the split hand cards on screen.
**Note:** These three paragraphs were removed together. `CALC-8X` had a `GO TO CALC-3` that would have re-entered the player hand display — likely the intended continuation after rendering the split.
```cobol
*  CALC-8 -- DISPLAY SPLIT HAND. SEE PROC-DS. REMOVED WITH SPLIT.
*   CALC-8.
*       DISPLAY '   SPLIT HAND:'
...
*  CALC-8X.
*       GO TO CALC-3.
```

---

### 1.6 LEGACY-RANDOM-GEN — `PROC-R1` (Linear Congruential Generator)
**File:** `legacy-random-gen.cob` lines 20–24
**Disabled:** "REPLACED WITH FIXED VALUE PER DEFECT 0042"
**What it did:** The actual pseudo-random number generator using the linear congruential method (`WS-X1 * 1103515245 + 12345 mod 65536`).
**Critical impact:** Replacing this with a fixed value of `7` means `BJACK-DECK` always swaps card position 1 with position 7, card 2 with 7, card 3 with 7... etc. The deck is not shuffled. Every game plays the same card order. **This is a casino-critical defect.**
```cobol
*  PROC-R1 -- ORIGINAL LCG. REPLACED WITH FIXED VALUE PER DEFECT 0042
*   PROC-R1.
*       COMPUTE WS-X1 = FUNCTION MOD
*              (WS-X1 * 1103515245 + 12345, 65536)
*       MOVE WS-X1 TO LS-R1
```

---

### 1.7 CASINO-AUDIT-LOG — `PROC-WR` (Audit File Write)
**File:** `casino-audit-log.cob` lines 21–25
**Disabled:** "DISABLED 1989. AUDIT FILE NOT CONFIGURED."
**What it did:** Wrote a formatted audit record to a file for regulatory compliance.
**Critical impact:** Every round of play calls `CASINO-AUDIT-LOG` from `BJACK-MAIN.CALC-2`. The call succeeds and returns normally — but no record is ever written. The audit trail is entirely absent.
```cobol
*  PROC-WR -- FILE WRITE. DISABLED 1989. AUDIT FILE NOT CONFIGURED.
*   PROC-WR.
*       MOVE LS-A1 TO WS-X1
*       MOVE LS-A2 TO LS-A2        ← no-op: assigns to itself
*       WRITE LS-A2
```

---

## 2. Active but Unreachable / Broken Paragraphs

These paragraphs are not commented out — they compile and are present in the running program — but either cannot be reached or do not perform their intended function.

### 2.1 BJACK-DECK — `DEAD-1` (Deck Rebalance Subroutine)
**File:** `bjack-deck.cob` lines 141–145
**Issue:** No paragraph in any module contains a `GO TO DEAD-1` or `CALL` that reaches this paragraph. It is unreachable dead code named `DEAD-1` — the original developer apparently knew.
**What it does:** Resets `WS-CT4` and `WS-CT2` to 0 and goes to `PROC-A`, which would rebuild the deck from scratch. The intent (deck rebalancing) is never triggered.
```cobol
* DEAD-1 -- DECK REBALANCE SUBROUTINE (RESERVED FOR FUTURE USE)
 DEAD-1.
     MOVE 0 TO WS-CT4
     MOVE 0 TO WS-CT2
     GO TO PROC-A.
```

---

### 2.2 BJACK-DEALER — `SOFT-1` (Soft 17 Hit Rule — broken)
**File:** `bjack-dealer.cob` lines 29–35
**Issue:** `SOFT-1` is reachable (called from `PROC-A` when `WS-DT >= 17`) but both branches unconditionally route to `CHECK-X` (stand). The dealer never draws on soft 17.
**Root cause:** The paragraph tests `WS-CT3 > 0` to detect a soft hand (ace counted as 11). `WS-CT3` is correctly accumulated in `CALC-2` — but the logic in `SOFT-1` routes *both* the soft-17 case AND the hard-17 case to `CHECK-X`. The correct target for the soft-17 hit should be `LOOP-A`, not `CHECK-X`.
**Impact:** Dealer always stands on soft 17, violating the Nevada Gaming Commission rule that was supposedly implemented in the 1989 update.
```cobol
* SOFT-1 -- HIT ON SOFT 17 PER NEVADA GAMING COMMISSION RULES
 SOFT-1.
     IF WS-DT = 17
         IF WS-CT3 > 0
             GO TO CHECK-X   ← BUG: should be GO TO LOOP-A
         END-IF
     END-IF
     GO TO CHECK-X.           ← both paths exit — dealer never hits
```

---

## 3. Declared but Unused Working-Storage Variables

These variables are defined in WORKING-STORAGE but are never referenced in the PROCEDURE DIVISION of their module.

| Variable | Module | PIC | Comment in source | Root cause |
|----------|--------|-----|-------------------|------------|
| `WS-X2` | `bjack-deal.cob` | `PIC 9` | "TEMPORARY CARD BUFFER. RESERVED FOR PHASE 2 1987." | Phase 2 never implemented |
| `WS-CB` | `bjack-score.cob` | `PIC 9` | "CHARLIE BONUS FLAG. OBSOLETE AFTER PROC-CB REMOVED." | Left after `PROC-CB` commented out |
| `WS-X1` | `bjack-displ.cob` | `PIC 9` | None | Declared, never referenced in any DISPLAY or COMPUTE |
| `WS-X1` | `legacy-random-gen.cob` | `PIC 9` | None | Only used by `PROC-R1` which is commented out |
| `WS-X1` | `casino-audit-log.cob` | `PIC 9` | None | Only used by `PROC-WR` which is commented out |

---

## 4. Effectively Dead Active Code

These are lines that execute but produce no meaningful effect.

### 4.1 BJACK-MAIN — No-op stability computation
**File:** `bjack-main.cob` line 31
**Code:** `COMPUTE WS-X1 = WS-X1 + 0`
**Comment:** "STABILITY FIX -- PREVENT OVERFLOW ON RE-ENTRY 1988"
**Assessment:** Adding 0 to a variable does nothing. `WS-X1` (PIC 9) has a range of 0–9 and there is no path in `INIT-1` where overflow could occur. This is a cargo-cult fix — someone thought it was preventing a problem but it has no effect.

---

### 4.2 CASINO-AUDIT-LOG — Entire module is a stub
**File:** `casino-audit-log.cob`
**Code:** `PROC-A. GOBACK.`
**Assessment:** The module accepts two parameters (`LS-A1`, `LS-A2`) and immediately returns without reading or using them. The module executes every round (called from `BJACK-MAIN.CALC-2`) and consumes a CALL overhead for zero effect.

---

### 4.3 LEGACY-RANDOM-GEN — Fixed return value masquerading as random
**File:** `legacy-random-gen.cob`
**Code:** `MOVE 7 TO LS-R1` followed by `GOBACK`
**Assessment:** Called in a loop from `BJACK-DECK.LOOP-B` 52 times to shuffle the deck. Always returns 7. The shuffle loop swaps every card with position 7, resulting in a deterministic, non-random deck order on every game.

---

### 4.4 CASINO-AUDIT-LOG — Self-assignment in commented-out code
**File:** `casino-audit-log.cob` line 23 (within `PROC-WR`)
**Code:** `MOVE LS-A2 TO LS-A2`
**Assessment:** Even if `PROC-WR` were re-enabled, this line assigns a field to itself — a no-op. The audit record passed in would not be modified. This suggests `PROC-WR` was never fully implemented before it was disabled.

---

## 5. Data Passed to Dead Modules (Never Processed)

### 5.1 BJACK-MAIN → CASINO-AUDIT-LOG: `WS-FLG-A` and `WS-AM`
**File:** `bjack-main.cob` line 122
**Code:** `CALL 'CASINO-AUDIT-LOG' USING BY REFERENCE WS-FLG-A WS-AM`
- `WS-FLG-A` — player action flag (H/S/D)
- `WS-AM` — 50-character audit message field
Both are passed on every completed round. `CASINO-AUDIT-LOG` ignores both and returns immediately.

### 5.2 BJACK-DECK → LEGACY-RANDOM-GEN: `WS-X2` (receives fixed 7 always)
**File:** `bjack-deck.cob` line 126
**Code:** `CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2`
`WS-X2` is passed as the output variable for the random index. It receives `7` on every call. The caller uses `WS-X2` as the swap target position in the shuffle, meaning position 7 is the only ever-swapped target.

---

## 6. Feature Removal Timeline

Reconstructed from comments across all modules:

| Year | Feature Removed | Modules Affected |
|------|----------------|-----------------|
| 1983 | LCG randomiser replaced with fixed value (Defect 0042) | `legacy-random-gen.cob` |
| 1987 | Split hand feature disabled (MGR NOTE) | `bjack-main.cob`, `bjack-deal.cob` |
| 1988 | Insurance offer disabled | `bjack-dealer.cob` |
| 1988 | Five-card Charlie bonus dropped (Nevada rule) | `bjack-score.cob` |
| 1989 | Audit file write disabled (file not configured) | `casino-audit-log.cob` |
| 1989 | Soft-17 rule update attempted but broken | `bjack-dealer.cob` |
| ~1987 | Split hand display removed | `bjack-displ.cob` |

> **Note on comment languages:** Inline comments appear in English, German ("ACHTUNG", "HINWEIS", "PRUEFPROTOKOLL"), and French ("AJUSTEMENT", "AFFICHAGE ECRAN", "CORRECTION"). This suggests multiple development teams or offshore contractors worked on this codebase across its lifetime. No single team appears to have had full visibility of all modules.

---

## 7. Recommended Actions

| Priority | Action | Modules |
|----------|--------|---------|
| 🔴 Immediate | Investigate and resolve Defect 0042 — restore or replace the shuffle | `legacy-random-gen.cob` |
| 🔴 Immediate | Configure and re-enable audit file write — regulatory exposure | `casino-audit-log.cob` |
| 🟠 High | Fix `SOFT-1` — change `GO TO CHECK-X` to `GO TO LOOP-A` for soft-17 hit | `bjack-dealer.cob` |
| 🟡 Medium | Remove all commented-out dead paragraphs (7 items) — reduces confusion during migration | All modules |
| 🟡 Medium | Remove orphaned working-storage variables (5 items) | Multiple |
| 🟢 Low | Remove `DEAD-1` paragraph from BJACK-DECK | `bjack-deck.cob` |
| 🟢 Low | Remove stability no-op `COMPUTE WS-X1 = WS-X1 + 0` | `bjack-main.cob` |
