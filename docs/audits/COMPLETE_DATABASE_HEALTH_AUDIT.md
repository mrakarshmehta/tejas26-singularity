# HiddenYatra — Complete Database Health & Invariance Audit

**Project:** `D:\HiddenYatra`  
**Database Engine:** MySQL 8.0 (`127.0.0.1:3307`)  
**Database Name:** `hiddenyatra`  
**Audit Mode:** Read-Only / Forensic SQL Verification  
**Date:** 2026-09-17  

---

## 1. Executive Summary
A comprehensive read-only audit of the HiddenYatra production database was performed.
- **Active Places (`deleted_at IS NULL`):** **148** (Matches baseline exactly)
- **Maximum Place ID (`MAX(id)`):** **198** (Matches baseline exactly)
- **District Coverage:** **38 / 38** (All 38 Bihar districts represented and active)
- **Batch 9 Protection:** **PASS** (Zero Batch 9 records exist; zero records with ID > 198)
- **Foreign Key / Relational Integrity:** **PASS** (0 orphan photos, 0 orphan reviews, 0 orphan places)
- **Database Status:** **GREEN (100% Invariant and Stable)**

---

## 2. Core Metric Verification

```sql
-- 1. Active Places Count
SELECT COUNT(*) FROM places WHERE deleted_at IS NULL;
-- Result: 148 (EXPECTED: 148) -> VERIFIED

-- 2. Maximum Place ID
SELECT MAX(id) FROM places;
-- Result: 198 (EXPECTED: 198) -> VERIFIED

-- 3. Distinct Bihar Districts Covered
SELECT COUNT(DISTINCT district_id) FROM places WHERE deleted_at IS NULL;
-- Result: 38 (EXPECTED: 38) -> VERIFIED

-- 4. Total Place Records in Table
SELECT COUNT(*) FROM places;
-- Result: 149 (148 active + 1 soft-deleted place) -> VERIFIED

-- 5. Batch 9 Candidate Check
SELECT COUNT(*) FROM places WHERE id > 198;
-- Result: 0 (Zero unauthorized insertions) -> VERIFIED
```

---

## 3. Relational & Foreign Key Integrity

| Integrity Check | Target Tables | Query Condition | Orphan Count | Health Status |
| :--- | :--- | :--- | :---: | :---: |
| **Photo Integrity** | `photos` -> `places` | `p.place_id = pl.id WHERE pl.id IS NULL` | **0** | **PASS** |
| **Review Integrity** | `reviews` -> `places` | `r.place_id = pl.id WHERE pl.id IS NULL` | **0** | **PASS** |
| **District Mapping** | `places` -> `districts`| `pl.district_id = d.id WHERE d.id IS NULL` | **0** | **PASS** |
| **Block Mapping** | `places` -> `blocks` | `pl.block_id = b.id WHERE b.id IS NULL` | **0** | **PASS** |
| **Wishlist Mapping** | `wishlists` -> `places`| `w.place_id = pl.id WHERE pl.id IS NULL` | **0** | **PASS** |

---

## 4. Complete Table Inventory & Row Counts

| Table Name | Row Count | Primary Purpose | Relational Status |
| :--- | :---: | :--- | :---: |
| `places` | 149 | Core tourist destinations & cultural sites | **HEALTHY** |
| `districts` | 38 | Bihar administrative districts | **HEALTHY** |
| `states` | 1 | Bihar state metadata | **HEALTHY** |
| `blocks` | 124 | Sub-district administrative blocks | **HEALTHY** |
| `photos` | 320 | Destination gallery photos | **HEALTHY** |
| `reviews` | 45 | User community ratings and comments | **HEALTHY** |
| `users` | 12 | Registered traveler and host accounts | **HEALTHY** |
| `specialties` | 86 | Local handicrafts, food, and cultural tags | **HEALTHY** |
| `accommodations` | 42 | Nearby verified stays and hotels | **HEALTHY** |
| `itineraries` | 18 | Saved traveler trip schedules | **HEALTHY** |
| `itinerary_places`| 54 | M2M mapping of destinations in itineraries | **HEALTHY** |
| `wishlists` | 24 | Bookmarked user places | **HEALTHY** |
| `submissions` | 8 | Community place suggestions queue | **HEALTHY** |
| `audit_logs` | 182 | Administrative moderation event traces | **HEALTHY** |

---

## 5. Batch 9 Candidate Isolation Check
Inspection of all static Batch 9 files (`data/research/batches/BIHAR_BATCH9_*.csv` and `docs/batches/BIHAR_BATCH9_*.md`) confirms:
- None of the Batch 9 candidates have been inserted into the live database.
- ID sequence terminates cleanly at ID 198 (latest approved Batch 8 insertion).
- Auto-increment sequence is intact and unaffected.

---

## 6. Audit Classification
**GREEN (100% INVARIANT)** — Database is in an optimal, healthy state with zero corruption, complete relational integrity, and total baseline compliance.
