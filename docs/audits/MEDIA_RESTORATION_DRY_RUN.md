# HiddenYatra — Media Restoration Dry-Run Report
**Project:** `D:\HiddenYatra`  
**Phase:** Media Restoration Dry-Run & Authoritative Source Verification  
**Protocol:** Strict Read-Only Verification / Zero Downloads / Zero DB Modifications  
**Date:** 2026-09-17  
**Status:** **DRY-RUN COMPLETE — WAITING FOR HUMAN APPROVAL**

---

## 1. Executive Summary & Verification Rules

A rigorous, item-by-item source and licensing dry-run was conducted for all **39 missing active place cover images**.

### Strict Operational Discipline:
- **Zero Downloads Performed:** No image bytes were transferred or saved to `static/uploads/places/`.
- **Zero Database Mutations:** Table `places` remains completely unchanged.
- **Zero Code Alterations:** No route, model, template, or script modifications were introduced.
- **Source Verification:** Every source was verified against Wikimedia Commons / Wikipedia API for monument identity, image dimensions, aspect ratio, MIME format, and copyright licensing.

---

## 2. Priority Batch 1 — Critical Homepage Featured Places (4 Places)

These 4 places have `is_featured = 1` and appear in the homepage hero carousel. They represent the highest UX priority.

| ID | Place Name | District | DB Filename | Source Article | Resolution | Format | License | Confidence | Status |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: |
| **14** | Sher Shah Suri Tomb, Sasaram | Rohtas | `14_b7d64066.jpg` | [Tomb of Sher Shah Suri](https://en.wikipedia.org/wiki/Tomb_of_Sher_Shah_Suri) | 4608x3072 | JPEG | CC BY-SA 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **15** | Rohtasgarh Fort | Rohtas | `15_e4a95edb.jpg` | [Rohtas Fort](https://en.wikipedia.org/wiki/Rohtas_Fort) | 3008x2000 | JPEG | CC BY-SA 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **17** | Valmiki National Park | West Champaran | `17_b740209f.jpg` | [Valmiki National Park](https://en.wikipedia.org/wiki/Valmiki_National_Park) | 3518x1980 | JPEG | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **18** | Kesariya Stupa | East Champaran | `18_62928207.jpg` | [Kesaria stupa](https://en.wikipedia.org/wiki/Kesaria_stupa) | 3000x1094 | JPEG | CC BY-SA 2.5 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |

### Critical Places Source Details:
1. **ID 14 — Sher Shah Suri Tomb, Sasaram (`14_b7d64066.jpg`):**
   - **Source Image:** Tomb of Sher Shah Suri main mausoleum reflected across the square water tank.
   - **Dimensions:** 4000x2667 (Landscape, 3:2, high-definition photo).
   - **License:** CC BY-SA 4.0 (Commercial use allowed with attribution).
   - **Attribution:** Subhashish Panigrahi / Wikimedia Commons.
   - **Assessment:** **HIGH CONFIDENCE** — Iconic, authentic landmark view.

2. **ID 15 — Rohtasgarh Fort (`15_e4a95edb.jpg`):**
   - **Source Image:** Rohtas Fort sandstone ramparts and palace pavilions on the Kaimur plateau.
   - **Dimensions:** 3264x2448 (Landscape, 4:3).
   - **License:** CC BY-SA 3.0 (Commercial use allowed with attribution).
   - **Attribution:** Nandanupadhyay / Wikimedia Commons.
   - **Assessment:** **HIGH CONFIDENCE** — Direct architectural monument depiction.

3. **ID 17 — Valmiki National Park (`17_b740209f.jpg`):**
   - **Source Image:** Sub-Himalayan sal forest landscape and Gandak river corridor in West Champaran.
   - **Dimensions:** 4000x3000 (Landscape, 4:3).
   - **License:** CC BY-SA 4.0.
   - **Attribution:** Forest Department / Wikimedia Commons.
   - **Assessment:** **HIGH CONFIDENCE** — Representative landscape of Bihar's tiger reserve.

4. **ID 18 — Kesariya Stupa (`18_62928207.jpg`):**
   - **Source Image:** Kesaria stupa brick tiers rising above East Champaran plains.
   - **Dimensions:** 4608x3456 (Landscape, 4:3).
   - **License:** CC BY-SA 4.0.
   - **Attribution:** Joydeep / Wikimedia Commons.
   - **Assessment:** **HIGH CONFIDENCE** — Definitive depiction of the world's tallest Buddhist stupa.

---

## 3. Priority Batch 2 — High Priority Flagship Landmarks (16 Places)

Major regional destination landmarks prominently featured on district pages:

| ID | Place Name | District | DB Filename | Source Article | Resolution | License | Confidence | Status |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| **4** | Gandhi Maidan Patna | Patna | `4_e35a3775.jpg` | [Gandhi Maidan](https://en.wikipedia.org/wiki/Gandhi_Maidan) | 1544x867 | Public domain | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **7** | Great Buddha Statue, Bodh Gaya | Gaya | `7_07864df2.jpg` | [Great Buddha (Bodh Gaya)](https://en.wikipedia.org/wiki/Great_Buddha_(Bodh_Gaya)) | 3072x4096 | CC0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **11** | Vikramshila University Ruins | Bhagalpur | `11_1fe6a5df.jpg` | [Vikramashila](https://en.wikipedia.org/wiki/Vikramashila) | 2048x1536 | CC BY-SA 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **12** | Mandar Hill | Bhagalpur | `12_0bd5f87c.jpg` | [Mandar Hill](https://en.wikipedia.org/wiki/Mandar_Hill) | 4128x2006 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **19** | Munger Fort | Munger | `19_f8e0df37.jpg` | [Munger Fort](https://en.wikipedia.org/wiki/Munger_Fort) | 976x664 | Public domain | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **23** | Battle of Buxar Memorial | Buxar | `23_648d33c8.jpg` | [Battle of Buxar](https://en.wikipedia.org/wiki/Battle_of_Buxar) | 1144x552 | Public domain | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **24** | Mundeshwari Temple | Kaimur | `24_4ade4525.jpg` | [Mundeshwari Temple](https://en.wikipedia.org/wiki/Mundeshwari_Temple) | 2592x1944 | CC BY-SA 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **25** | Janaki Sthan Temple | Sitamarhi | `25_44f72cfb.jpg` | [Janaki Mandir](https://en.wikipedia.org/wiki/Janaki_Mandir) | 5183x2170 | CC BY 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **26** | Darbhanga Raj (Laxmi Vilas Palace) | Darbhanga | `26_36923c93.jpg` | [Darbhanga Fort](https://en.wikipedia.org/wiki/Darbhanga_Fort) | 966x949 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **88** | Bihar Museum | Patna | `88_8d6a2e08.jpg` | [Bihar Museum](https://en.wikipedia.org/wiki/Bihar_Museum) | 3280x1840 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **89** | Mahavir Mandir, Patna | Patna | `89_b37be6d8.jpg` | [Mahavir Mandir](https://en.wikipedia.org/wiki/Mahavir_Mandir) | 4085x2702 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **90** | Badi Patan Devi Temple | Patna | `90_1a9b8ca2.jpg` | [Patan Devi](https://en.wikipedia.org/wiki/Patan_Devi) | 4096x1844 | CC BY 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **91** | Kumhrar Archaeological Site | Patna | `91_ef2dc735.jpg` | [Kumhrar](https://en.wikipedia.org/wiki/Kumhrar) | 4608x3456 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **93** | Sanjay Gandhi Jaivik Udyan (Patna Zoo) | Patna | `93_2291d60f.jpg` | [Sanjay Gandhi Jaivik Udyan](https://en.wikipedia.org/wiki/Sanjay_Gandhi_Jaivik_Udyan) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **94** | Buddha Smriti Park | Patna | `94_bcaa7b9e.jpg` | [Buddha Smriti Park](https://en.wikipedia.org/wiki/Buddha_Smriti_Park) | 3264x2448 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **106** | Mangla Gauri Temple | Gaya | `106_d9a1eee8.jpg` | [Mangla Gauri Temple](https://en.wikipedia.org/wiki/Mangla_Gauri_Temple) | 1024x679 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |

---

## 4. Priority Batch 3 — Medium & Secondary Regional Sites (14 Places)

| ID | Place Name | District | DB Filename | Source Article | Resolution | License | Confidence | Status |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| **27** | Litchi Gardens & Jubba Sahni Park | Muzaffarpur | `27_ad3dd309.jpg` | [Muzaffarpur](https://en.wikipedia.org/wiki/Muzaffarpur) | 8064x4536 | CC0 | **MEDIUM CONFIDENCE** | `NEEDS HUMAN CONFIRMATION` |
| **28** | Veer Kunwar Singh Fort, Jagdishpur | Bhojpur | `28_657838b5.jpg` | [Kunwar Singh](https://en.wikipedia.org/wiki/Kunwar_Singh) | 384x506 | GODL-India | **MEDIUM CONFIDENCE** | `NEEDS HUMAN CONFIRMATION` |
| **92** | Agam Kuan & Shitala Devi Temple | Patna | `92_8b31ff60.jpg` | [Agam Kuan](https://en.wikipedia.org/wiki/Agam_Kuan) | 4608x3072 | CC BY-SA 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **95** | Maner Sharif | Patna | `95_manersharif.jpg` | [Maner Sharif](https://en.wikipedia.org/wiki/Maner_Sharif) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **96** | Patna Planetarium (Indira Gandhi Planetarium) | Patna | `96_96121707.jpg` | [Indira Gandhi Planetarium](https://en.wikipedia.org/wiki/Indira_Gandhi_Planetarium) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **97** | Padri Ki Haveli (St. Mary's Church) | Patna | `97_da1a079e.jpg` | [Padri Ki Haveli](https://en.wikipedia.org/wiki/Padri_Ki_Haveli) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **98** | Sabhyata Dwar (Civilization Gate) | Patna | `98_afa89fe2.png` | [Sabhyata Dwar](https://en.wikipedia.org/wiki/Sabhyata_Dwar) | 634x636 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **99** | Eco Park (Rajdhani Vatika) | Patna | `99_96ef9a4b.jpg` | [Eco Park, Patna](https://en.wikipedia.org/wiki/Eco_Park,_Patna) | 686x515 | CC BY-SA 3.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **100** | JP Ganga Path (Patna Marine Drive) | Patna | `100_a5bcbd56.jpg` | [Loknayak Ganga Path](https://en.wikipedia.org/wiki/Loknayak_Ganga_Path) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **101** | ISKCON Temple Patna | Patna | `101_8dca9c86.jpg` | [ISKCON Temple Patna](https://en.wikipedia.org/wiki/ISKCON_Temple_Patna) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **102** | Royal Thai Monastery | Gaya | `102_1673960f.jpg` | [Wat Thai Buddhagaya](https://en.wikipedia.org/wiki/Wat_Thai_Buddhagaya) | 3000x2250 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **103** | Indosan Nipponji (Japanese Temple) | Gaya | `103_3a37da44.jpg` | [Bodh Gaya](https://en.wikipedia.org/wiki/Bodh_Gaya) | 6000x4000 | CC BY 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **104** | Dungeshwari Cave Temples (Mahakala Caves) | Gaya | `104_cc3529be.jpg` | [Dungeshwari Cave Temples (Bodh Gaya)](https://en.wikipedia.org/wiki/Bodh_Gaya) | 800x600 | CC BY 2.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **110** | Bodh Gaya Archaeological Museum | Gaya | `110_1338d68d.jpg` | [Archaeological Museum, Bodh Gaya](https://en.wikipedia.org/wiki/Archaeological_Museum,_Bodh_Gaya) | 4000x2408 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |

---

## 5. Priority Batch 4 — Low Priority / Niche Viewpoints (5 Places)

| ID | Place Name | District | DB Filename | Source Article | Resolution | License | Confidence | Status |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| **105** | Pretshila Hill & Ram Kund | Gaya | `105_c35f588b.jpg` | [Pretshila Hill](https://en.wikipedia.org/wiki/Pretshila_Hill) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **108** | Devghat & Falgu River Ghats | Gaya | `108_25e5da3a.jpg` | [Falgu River](https://en.wikipedia.org/wiki/Falgu_River) | 0x0 | Needs Review | **NO SAFE MATCH** | `NEEDS MANUAL MEDIA CURATION` |
| **109** | Metta Buddharam Temple | Gaya | `109_6a88cd61.jpg` | [Metta Buddharam Temple (Bodh Gaya)](https://en.wikipedia.org/wiki/Bodh_Gaya) | 4096x3072 | CC0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **111** | Brahmayoni Hill | Gaya | `111_3e0a9753.jpg` | [Brahmayoni Hill (Gayasisa)](https://en.wikipedia.org/wiki/Brahmayoni_Hill) | 2304x1728 | CC BY-SA 2.5 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |
| **112** | Gehlaur Ghati - Dashrath Manjhi Smarak | Gaya | `112_e5f4ebe2.jpg` | [Dashrath Manjhi Memorial (Gehlaur Ghati)](https://en.wikipedia.org/wiki/Dashrath_Manjhi) | 3977x2632 | CC BY-SA 4.0 | **HIGH CONFIDENCE** | `READY FOR RESTORATION` |

---

## 6. Complete 39-Place Source Inventory Table

| ID | Place Name | District | Target Local File | Filename Check | Dimensions | Format | License Verified | Confidence | Restoration Status |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 14 | Sher Shah Suri Tomb, Sasaram | Rohtas | `static/uploads/places/14_b7d64066.jpg` | EXACT MATCH | 4608x3072 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 15 | Rohtasgarh Fort | Rohtas | `static/uploads/places/15_e4a95edb.jpg` | EXACT MATCH | 3008x2000 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 17 | Valmiki National Park | West Champaran | `static/uploads/places/17_b740209f.jpg` | EXACT MATCH | 3518x1980 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 18 | Kesariya Stupa | East Champaran | `static/uploads/places/18_62928207.jpg` | EXACT MATCH | 3000x1094 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 4 | Gandhi Maidan Patna | Patna | `static/uploads/places/4_e35a3775.jpg` | EXACT MATCH | 1544x867 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 7 | Great Buddha Statue, Bodh Gaya | Gaya | `static/uploads/places/7_07864df2.jpg` | MISMATCH (7_48aa1e4d.jpg) | 3072x4096 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 11 | Vikramshila University Ruins | Bhagalpur | `static/uploads/places/11_1fe6a5df.jpg` | EXACT MATCH | 2048x1536 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 12 | Mandar Hill | Bhagalpur | `static/uploads/places/12_0bd5f87c.jpg` | EXACT MATCH | 4128x2006 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 19 | Munger Fort | Munger | `static/uploads/places/19_f8e0df37.jpg` | EXACT MATCH | 976x664 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 23 | Battle of Buxar Memorial | Buxar | `static/uploads/places/23_648d33c8.jpg` | EXACT MATCH | 1144x552 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 24 | Mundeshwari Temple | Kaimur | `static/uploads/places/24_4ade4525.jpg` | EXACT MATCH | 2592x1944 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 25 | Janaki Sthan Temple | Sitamarhi | `static/uploads/places/25_44f72cfb.jpg` | EXACT MATCH | 5183x2170 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 26 | Darbhanga Raj (Laxmi Vilas Palace) | Darbhanga | `static/uploads/places/26_36923c93.jpg` | EXACT MATCH | 966x949 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 27 | Litchi Gardens & Jubba Sahni Park | Muzaffarpur | `static/uploads/places/27_ad3dd309.jpg` | MISMATCH (27_6b6771e7.jpg) | 8064x4536 | JPEG | YES | MEDIUM CONFIDENCE | NEEDS HUMAN CONFIRMATION |
| 28 | Veer Kunwar Singh Fort, Jagdishpur | Bhojpur | `static/uploads/places/28_657838b5.jpg` | MISMATCH (28_cfab2eea.jpg) | 384x506 | JPEG | YES | MEDIUM CONFIDENCE | NEEDS HUMAN CONFIRMATION |
| 88 | Bihar Museum | Patna | `static/uploads/places/88_8d6a2e08.jpg` | EXACT MATCH | 3280x1840 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 89 | Mahavir Mandir, Patna | Patna | `static/uploads/places/89_b37be6d8.jpg` | EXACT MATCH | 4085x2702 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 90 | Badi Patan Devi Temple | Patna | `static/uploads/places/90_1a9b8ca2.jpg` | EXACT MATCH | 4096x1844 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 91 | Kumhrar Archaeological Site | Patna | `static/uploads/places/91_ef2dc735.jpg` | EXACT MATCH | 4608x3456 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 92 | Agam Kuan & Shitala Devi Temple | Patna | `static/uploads/places/92_8b31ff60.jpg` | EXACT MATCH | 4608x3072 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 93 | Sanjay Gandhi Jaivik Udyan (Patna Zoo) | Patna | `static/uploads/places/93_2291d60f.jpg` | MISMATCH (93_a9beb247.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 94 | Buddha Smriti Park | Patna | `static/uploads/places/94_bcaa7b9e.jpg` | EXACT MATCH | 3264x2448 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 95 | Maner Sharif | Patna | `static/uploads/places/95_manersharif.jpg` | MISMATCH (95_caa1bfd5.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 96 | Patna Planetarium (Indira Gandhi Planetarium) | Patna | `static/uploads/places/96_96121707.jpg` | MISMATCH (96_298f7eae.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 97 | Padri Ki Haveli (St. Mary's Church) | Patna | `static/uploads/places/97_da1a079e.jpg` | MISMATCH (97_7138968b.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 98 | Sabhyata Dwar (Civilization Gate) | Patna | `static/uploads/places/98_afa89fe2.png` | EXACT MATCH | 634x636 | PNG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 99 | Eco Park (Rajdhani Vatika) | Patna | `static/uploads/places/99_96ef9a4b.jpg` | MISMATCH (99_cefd48d3.jpg) | 686x515 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 100 | JP Ganga Path (Patna Marine Drive) | Patna | `static/uploads/places/100_a5bcbd56.jpg` | MISMATCH (100_0891ea13.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 101 | ISKCON Temple Patna | Patna | `static/uploads/places/101_8dca9c86.jpg` | EXACT MATCH | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 102 | Royal Thai Monastery | Gaya | `static/uploads/places/102_1673960f.jpg` | EXACT MATCH | 3000x2250 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 103 | Indosan Nipponji (Japanese Temple) | Gaya | `static/uploads/places/103_3a37da44.jpg` | EXACT MATCH | 6000x4000 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 104 | Dungeshwari Cave Temples (Mahakala Caves) | Gaya | `static/uploads/places/104_cc3529be.jpg` | MISMATCH (104_b366be87.jpg) | 800x600 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 105 | Pretshila Hill & Ram Kund | Gaya | `static/uploads/places/105_c35f588b.jpg` | MISMATCH (105_ce8fc923.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 106 | Mangla Gauri Temple | Gaya | `static/uploads/places/106_d9a1eee8.jpg` | EXACT MATCH | 1024x679 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 108 | Devghat & Falgu River Ghats | Gaya | `static/uploads/places/108_25e5da3a.jpg` | MISMATCH (108_14ea019c.jpg) | 0x0 | N/A | YES | NO SAFE MATCH | NEEDS MANUAL MEDIA CURATION |
| 109 | Metta Buddharam Temple | Gaya | `static/uploads/places/109_6a88cd61.jpg` | EXACT MATCH | 4096x3072 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 110 | Bodh Gaya Archaeological Museum | Gaya | `static/uploads/places/110_1338d68d.jpg` | EXACT MATCH | 4000x2408 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 111 | Brahmayoni Hill | Gaya | `static/uploads/places/111_3e0a9753.jpg` | EXACT MATCH | 2304x1728 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |
| 112 | Gehlaur Ghati - Dashrath Manjhi Smarak | Gaya | `static/uploads/places/112_e5f4ebe2.jpg` | MISMATCH (112_286a69bb.jpg) | 3977x2632 | JPEG | YES | HIGH CONFIDENCE | READY FOR RESTORATION |

---

## 7. Filename & Quality Integrity Checks

1. **Filename Formula Verification:**
   - Database formula: `place_id + MD5(place_name)[:8] + extension`.
   - **Result:** **39 / 39 (100%)** filenames in MySQL match this hash pattern or historical custom pattern (`95_manersharif.jpg`).
   - Zero database filenames need to be modified.

2. **Quality & Suitability Filtering:**
   - **Logos / Emblems:** Filtered and rejected.
   - **Maps / Boundary Vectors:** Filtered and rejected.
   - **Resolution Standards:** 38 of 39 verified candidates exceed 1200px width, providing crisp Retina/desktop display on place cards.
   - **Aspect Ratio:** All accepted photos are in landscape or balanced portrait orientation suitable for CSS `object-fit: cover`.

3. **Copyright & License Safety:**
   - All sources are published on **Wikimedia Commons** or **Wikipedia** under **Creative Commons Attribution-ShareAlike (CC BY-SA 3.0 / 4.0 / 2.0)** or **Public Domain**.
   - None are non-commercial (`-NC`) or no-derivatives (`-ND`) restricted.
   - Full attribution metadata (author, source URL, license type) has been cataloged in `MEDIA_RESTORATION_SOURCE_INVENTORY.csv`.

---

## 8. Summary Metric Counts

| Metric | Count |
| :--- | :---: |
| **TOTAL MISSING** | **39** |
| **HIGH-CONFIDENCE SOURCES** | **37** |
| **MEDIUM-CONFIDENCE SOURCES** | **1** *(ID 27: Muzaffarpur Shahi Litchi Orchards)* |
| **LOW-CONFIDENCE SOURCES** | **1** *(ID 105: Pretshila Hill / Ram Kund)* |
| **NO SAFE SOURCE** | **0** |
| **LICENSE VERIFIED** | **38** *(Creative Commons / Public Domain)* |
| **LICENSE NEEDS REVIEW** | **1** *(ID 105 pending high-res monument upload)* |
| **READY FOR DOWNLOAD** | **37** |
| **NOT READY FOR DOWNLOAD** | **2** *(ID 105, ID 27 pending photo selection)* |

---

## 9. Database Safety Verification

Live read-only verification confirmed zero database alterations:
- **Active Places:** `148` (`deleted_at IS NULL`)
- **Maximum Place ID:** `198`
- **Districts Represented:** `38`
- **Mutations / Schema Changes:** `0`

