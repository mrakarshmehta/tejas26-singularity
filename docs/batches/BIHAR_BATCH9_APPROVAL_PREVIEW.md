# HiddenYatra — Batch 9 Candidate Research & Approval Preview

## 1. Executive Summary & Verified Baseline

- **Current Active Inventory:** 148 destinations (`deleted_at IS NULL`)
- **Bihar Districts Covered:** 38 / 38 (100% geographic coverage)
- **Current Maximum ID:** 198
- **Latest Live Batch:** Batch 8 (IDs 189–198, fully regression tested)
- **Database Status:** LIVE, verified, strictly READ-ONLY for this research phase.
- **Batch 9 Objective:** Prepare the next highest-quality tourism candidates for Batch 9, adhering strictly to **QUALITY > QUANTITY**.
- **Batch 9 Candidate Target:** Exactly 10 top-tier, non-inserted destinations meeting strict **Grade A** authoritative institutional evidence standards.
- **Verified District IDs:** All 10 district IDs queried directly from the live `districts` table:
  - `Lakhisarai = 26`
  - `Samastipur = 30`
  - `Sitamarhi = 34`
  - `Katihar = 23`
  - `Munger = 6`
  - `Darbhanga = 18`
  - `Siwan = 35`
  - `Saran = 31`
  - `Kaimur = 22`
  - `Patna = 1`

---

## 2. Approved Batch 9 Candidate Table

| Rank | Candidate Name | District | Dist ID | Category | Latitude | Longitude | Canonical Slug | Nearest Existing Place | Min Dist (km) | Overlap Class | Tourism Value | Why It Adds New Value | Primary Source | Secondary Source | Evidence Conf. | Priority | Risk / Notes |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | Lali Pahadi Archaeological Site | Lakhisarai | 26 | `historical` | 25.1764 | 85.9981 | `lali-pahadi-archaeological-site` | Ashok Dham Temple (Lakhisarai) | 6.35 | DISTINCT DESTINATION | First excavated hilltop Buddhist nunnery ('Shrimaddharma Vihara') in the Gangetic plains, excavated jointly by BHDS & Visva-Bharati; features 27 cells, central shrine, and ancient monk quarters. | Strengthens 2-place Lakhisarai with world-class Buddhist monastic archaeology, complementing Ashok Dham and Shringirishi Dham. | Bihar Heritage Development Society (BHDS) / Dept of Art, Culture & Youth | Lakhisarai District Administration (`lakhisarai.nic.in`) / Visva-Bharati University | **HIGH (Grade A)** | **P0** | Officially excavated and inaugurated by CM Nitish Kumar; hilltop archaeological park located 6.35 km from Ashok Dham Temple. |
| **2** | Khudneshwar Asthan, Morwa | Samastipur | 30 | `cultural` | 25.7610 | 85.6890 | `khudneshwar-asthan-morwa` | Vidyapati Dham (Samastipur) | 18.17 | DISTINCT DESTINATION | Historic 1858 syncretic shrine where a sacred Shivalinga and the mazar of a Muslim woman devotee (Khudni Biwi) share the same inner sanctum, exemplifying communal harmony and Ganga-Jamuni tehzeeb. | Expands 2-place Samastipur with a profound living cultural heritage site demonstrating Bihar's syncretic traditions; complements Vidyapati Dham. | Samastipur District Administration (`samastipur.nic.in`) - Places of Interest | Bihar Tourism (`tourism.bihar.gov.in`) - Cultural & Religious Circuit | **HIGH (Grade A)** | **P0** | Unique Hindu-Muslim shared sanctum sanctorum; attracts large festive crowds during Shivratri and Shravani Mela. 18.17 km from Vidyapati Dham. |
| **3** | Panth Pakar | Sitamarhi | 34 | `cultural` | 26.6370 | 85.4520 | `panth-pakar` | Punaura Dham (Sitamarhi) | 2.73 | NEARBY BUT DISTINCT (Special Scrutiny) | Ancient sprawling sacred Banyan tree (spread across ~1 acre) in Riga block where, according to Ramayana tradition, the bridal palanquin (doli) of Devi Sita and Lord Rama rested on their journey to Ayodhya. | Strengthens 2-place Sitamarhi on the Ramayana Circuit with a unique botanical-sacred living heritage landmark distinct from town temples. | Bihar Tourism (`tourism.bihar.gov.in`) - Ramayana Circuit | Sitamarhi District Administration (`sitamarhi.nic.in`) - Tourism & Heritage | **HIGH (Grade A)** | **P0** | Located 2.73 km from Punaura Dham. Completely independent pilgrimage site (living centuries-old banyan tree vs Janaki temple). Special scrutiny fully documented. |
| **4** | Manihari Ganga Ghat & Maharshi Mehi Ashram | Katihar | 23 | `cultural` | 25.3370 | 87.6250 | `manihari-ganga-ghat-maharshi-mehi-ashram` | Gogabil Lake Bird Sanctuary (Katihar) | 2.67 | NEARBY BUT DISTINCT (Special Scrutiny) | Historic Ganga riverfront and sacred bathing ghat at Manihari, paired with the pioneering spiritual retreat and ashram of Santmat reformer Maharshi Mehi Paramhans. | Strengthens 2-place Katihar with an authentic riverfront pilgrimage and spiritual retreat destination, complementing Gogabil Lake Bird Sanctuary. | Katihar District Administration (`katihar.nic.in`) - Tourism & Places of Interest | Bihar Tourism (`tourism.bihar.gov.in`) / Santmat Spiritual Publications | **HIGH (Grade A)** | **P0** | Located 2.67 km from Gogabil Lake. Completely distinct visitor intent (sacred riverfront/ashram vs oxbow wetland sanctuary). Special scrutiny fully documented. |
| **5** | Rishi Kund | Munger | 6 | `nature` | 25.2630 | 86.5180 | `rishi-kund` | Munger Fort (Munger) | 13.25 | DISTINCT DESTINATION | Natural perennial thermal hot springs set in a scenic forested valley of the Kharagpur Hills, renowned for therapeutic mineral waters and the triennial Malmas Mela. | Enriches Munger's eco-tourism and nature inventory with a legendary natural hot spring resort distinct from Bhimbandh and Munger Fort. | Munger District Administration (`munger.nic.in`) - Places of Interest & Tourism | Bihar State Tourism Development Corporation (BSTDC) / Geological Survey of India | **HIGH (Grade A)** | **P0** | Distinct forested geothermal spring complex situated 12.2 km north of Kharagpur Lake and 13.25 km from Munger Fort. |
| **6** | Chandradhari Museum | Darbhanga | 18 | `cultural` | 26.1550 | 85.8980 | `chandradhari-museum` | Darbhanga Raj (Laxmi Vilas Palace) (Darbhanga) | 0.87 | NEARBY BUT DISTINCT (Special Scrutiny) | Premier public cultural repository of North Bihar established in 1957, housing over 13,000 rare antiquities across 11 thematic galleries including Mithila paintings, ancient terracottas, and Royal Darbhanga relics. | Adds a high-caliber cultural institution and museum to Mithilanchal, creating a balanced urban heritage circuit alongside Laxmi Vilas Palace and Shyama Mai Temple. | Directorate of Museums, Department of Art, Culture & Youth, Govt of Bihar (`museums.bihar.gov.in`) | Darbhanga District Administration (`darbhanga.nic.in`) - Tourism & Culture | **HIGH (Grade A)** | **P0** | Located 0.87 km from Laxmi Vilas Palace on the bank of Mansarovar Lake. Independent institutional museum destination. Special scrutiny fully documented. |
| **7** | Sohagara Dham | Siwan | 35 | `temple` | 26.0820 | 84.0850 | `sohagara-dham` | Zeeradei (Dr. Rajendra Prasad House) (Siwan) | 23.53 | DISTINCT DESTINATION | Ancient Swayambhu Baba Hansnath Mandir situated on the Jharahi river at the Bihar-UP border, housing an enormous subterranean black-stone Shivalinga with deep historical reverence. | Expands 2-place Siwan with an iconic regional pilgrimage landmark that attracts hundreds of thousands of pilgrims during Maha Shivratri and Shravani Mela. | Siwan District Administration (`siwan.nic.in`) - Tourism & Places of Interest | Bihar Tourism (`tourism.bihar.gov.in`) - Spiritual Circuit | **HIGH (Grade A)** | **P0** | Border pilgrimage landmark situated 23.53 km from Zeeradei and 26.4 km from Baba Mahendra Nath Temple; serves as major cross-state cultural bridge. |
| **8** | Manjhi Fort Ruins & Ancient Mound | Saran | 31 | `historical` | 25.8230 | 84.5820 | `manjhi-fort-ruins-ancient-mound` | Gautam Asthan, Revelganj (Saran) | 10.07 | DISTINCT DESTINATION | Centrally Protected Monument under Archaeological Survey of India (ASI Patna Circle); massive ancient riverfront citadel mound and ramparts overlooking the Ghaghra (Saryu) and Ganga confluence. | Adds genuine ASI-protected archaeological depth to Saran, representing Chero dynasty fortification and NBPW-to-medieval continuous occupation. | Archaeological Survey of India (ASI Patna Circle) - Centrally Protected Monuments | Saran District Administration (`saran.nic.in`) - History & Monuments | **HIGH (Grade A)** | **P0** | ASI Centrally Protected site situated 10.07 km upstream from Revelganj / Gautam Asthan. |
| **9** | Tomb of Bakhtiyar Khan, Chainpur | Kaimur | 22 | `historical` | 25.0430 | 83.5180 | `tomb-of-bakhtiyar-khan-chainpur` | Karkatgarh Waterfall & Eco Park (Kaimur) | 4.28 | NEARBY BUT DISTINCT (Special Scrutiny) | State Protected Monument representing monumental 16th-century Suri-Afghan funerary architecture; majestic octagonal sandstone mausoleum on a high raised plinth with battlemented enclosures. | Adds exquisite medieval Afghan architecture to Kaimur, diversifying its portfolio beyond waterfalls and ancient temples. | Directorate of Archaeology, Dept of Art, Culture & Youth, Govt of Bihar - State Protected Monuments | Kaimur District Administration (`kaimur.nic.in`) - Tourism & Monuments | **HIGH (Grade A)** | **P0** | Located 4.28 km from Karkatgarh Waterfall in Chainpur town. Completely distinct heritage destination (16th-century Afghan mausoleum vs natural waterfall/eco-park). Special scrutiny fully documented. |
| **10** | Khuda Bakhsh Oriental Public Library | Patna | 1 | `cultural` | 25.6185 | 85.1630 | `khuda-bakhsh-oriental-public-library` | Takht Sri Patna Sahib (Patna) | 1.35 | NEARBY BUT DISTINCT (Special Scrutiny) | Institution of National Importance (Act of Parliament, 1969) housing over 21,000 priceless Arabic, Persian, and Urdu manuscripts, including the unique illustrated Tarikh-e-Khandan-e-Timuriya and Padshahnama. | Introduces intellectual and bibliographic heritage of global stature, offering cultural travellers an unparalleled encounter with Mughal imperial history and arts. | Ministry of Culture, Government of India / Khuda Bakhsh Oriental Public Library Act (No. 43 of 1969) | Patna District Administration (`patna.nic.in`) - Tourism & Heritage / Bihar Tourism | **HIGH (Grade A)** | **P0** | Located 1.35 km from Takht Sri Patna Sahib on Ashok Rajpath. Autonomous statutory national institution with independent visitor profile. Special scrutiny fully documented. |

---

## 3. District Depth & Representation Impact

Batch 9 strategically strengthens **underrepresented districts**, with 5 out of 10 candidates elevating districts that currently possess only 2 destinations, and 2 candidates elevating 3-place districts:

| District | Actual DB ID | Current Active Places | Post-Batch 9 Projected | Delta | Added Destination | Current Destinations in District |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Lakhisarai** | **26** | 2 | **3** | +1 | Lali Pahadi Archaeological Site | Ashok Dham Temple, Shringirishi Dham |
| **Samastipur** | **30** | 2 | **3** | +1 | Khudneshwar Asthan, Morwa | Vidyapati Dham, Dr. Rajendra Prasad Central Agricultural University |
| **Sitamarhi** | **34** | 2 | **3** | +1 | Panth Pakar | Janaki Sthan Temple, Punaura Dham |
| **Katihar** | **23** | 2 | **3** | +1 | Manihari Ganga Ghat & Maharshi Mehi Ashram | Gogabil Lake Bird Sanctuary, Guru Tegh Bahadur Historic Gurdwara |
| **Siwan** | **35** | 2 | **3** | +1 | Sohagara Dham | Zeeradei (Dr. Rajendra Prasad House), Baba Mahendra Nath Temple |
| **Munger** | **6** | 3 | **4** | +1 | Rishi Kund | Munger Fort, Bhimbandh Hot Springs, Kharagpur Lake |
| **Darbhanga** | **18** | 3 | **4** | +1 | Chandradhari Museum | Darbhanga Raj (Laxmi Vilas Palace), Kusheshwar Asthan, Ahilya Sthan |
| **Saran** | **31** | 4 | **5** | +1 | Manjhi Fort Ruins & Ancient Mound | Sonepur Hariharnath Temple, Chirand Site, Gautam Asthan, Ambika Sthan |
| **Kaimur** | **22** | 4 | **5** | +1 | Tomb of Bakhtiyar Khan, Chainpur | Mundeshwari Temple, Karkatgarh Waterfall, Telhar Kund, Kaimur Wildlife Sanctuary |
| **Patna** | **1** | 18 | **19** | +1 | Khuda Bakhsh Oriental Public Library | Golghar, Patna Sahib, Patna Museum, Bihar Museum, Kumhrar, etc. |

---

## 4. Category Diversity Analysis

Batch 9 aggressively combats temple repetition and brings rich, authentic, and diverse experiential domains to HiddenYatra:

| Category | Batch 9 Count | Percentage | Candidates |
| :--- | :---: | :---: | :--- |
| **cultural** | 5 | 50.0% | Khudneshwar Asthan (Syncretic Hindu-Muslim shrine), Panth Pakar (Sacred living banyan tree), Manihari Ganga Ghat (Sacred riverfront & Santmat retreat), Chandradhari Museum (11-gallery antiquities museum), Khuda Bakhsh Library (National manuscript treasure) |
| **historical** | 3 | 30.0% | Lali Pahadi (Excavated Buddhist nunnery), Manjhi Fort Ruins (ASI centrally protected citadel), Tomb of Bakhtiyar Khan (Monumental 16th-century Afghan mausoleum) |
| **nature** | 1 | 10.0% | Rishi Kund (Perennial thermal hot springs & forested valley) |
| **temple** | 1 | 10.0% | Sohagara Dham (Ancient Swayambhu Baba Hansnath Mandir) |
| **Total** | **10** | **100.0%** | **Balanced across 10 distinct districts** |

> [!NOTE]
> Temples constitute only **10%** (1 out of 10) of Batch 9, directly answering the user mandate to avoid temple saturation and prioritize multidimensional cultural and historical tourism assets.

---

## 5. Special Scrutiny: Candidates Under 5 km

In strict compliance with Step 7 of the user prompt, five candidates situated within 5 km of an existing active destination were subjected to rigorous independent scrutiny:

### 1. Panth Pakar (Sitamarhi) — 2.73 km from Punaura Dham (ID 161)
- **Is it the same attraction?** **No.** Punaura Dham is a structured marble temple complex and sacred reservoir marking the birth spot of Sita. Panth Pakar is a colossal, ancient sacred banyan tree spread over nearly an acre in rural Riga block.
- **Is it an attached monument?** **No.** They sit in completely separate revenue villages separated by 2.73 km of rural countryside and road infrastructure.
- **Independent visitor intent:** Punaura Dham attracts temple pilgrims seeking formal puja and darshan. Panth Pakar attracts cultural and epic travellers following the physical Ramayana procession route to experience the living botanical tree where the bridal palanquin (doli) rested.
- **Separate representation justification:** Officially recognized by the Ministry of Tourism and Bihar Tourism as an independent designated milestone on the Ramayana Circuit. Merging them would erase this living botanical landmark.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION**.

### 2. Manihari Ganga Ghat & Maharshi Mehi Ashram (Katihar) — 2.67 km from Gogabil Lake Bird Sanctuary (ID 124)
- **Is it the same attraction?** **No.** Gogabil Lake is a quiet oxbow wetland ecosystem and Community Reserve dedicated to resident and migratory waterbirds. Manihari Ganga Ghat is an active holy riverfront on the main stream of the Ganga, paired with the spiritual headquarters of the Santmat movement.
- **Is it an attached monument?** **No.** Separated by 2.67 km; managed under completely different authorities (Bihar Forest Dept / local community vs Ganga river ghat & Santmat spiritual trust).
- **Independent visitor intent:** Gogabil is visited for eco-tourism, avifaunal photography, and wetland biodiversity. Manihari Ghat is visited for sacred Ganga snan (holy bath), sunset river panoramas, and silent meditation at the ashram.
- **Separate representation justification:** Divergent visitor typologies (nature/wetland vs spiritual riverfront/ashram).
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION**.

### 3. Chandradhari Museum (Darbhanga) — 0.87 km from Darbhanga Raj (Laxmi Vilas Palace) (ID 26)
- **Is it the same attraction?** **No.** Darbhanga Raj (Laxmi Vilas Palace) is an imposing royal palace building (now housing Kameshwar Singh Sanskrit University). Chandradhari Museum is an independent public state museum established in 1957 on the eastern bank of Mansarovar Lake.
- **Is it an attached monument?** **No.** Located on independent municipal parcels across the lake precinct, operated by the Directorate of Museums, Government of Bihar.
- **Independent visitor intent:** Tourists visit the palace for its Indo-Saracenic royal architecture and campus grounds. Tourists visit the museum specifically to view 11 curated galleries of Mithila folk paintings, ancient Mauryan and Pala terracottas, medieval coins, ivory carvings, and royal antiquities.
- **Separate representation justification:** It is the premier public cultural museum of North Bihar, essential to the urban cultural circuit of Darbhanga.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION**.

### 4. Tomb of Bakhtiyar Khan, Chainpur (Kaimur) — 4.28 km from Karkatgarh Waterfall & Eco Park (ID 122)
- **Is it the same attraction?** **No.** Karkatgarh is a natural waterfall and eco-park with crocodile conservation on the Karamnasa River canyon. The Tomb of Bakhtiyar Khan is a 16th-century octagonal Afghan sandstone mausoleum inside a fortified enclosure in Chainpur town.
- **Is it an attached monument?** **No.** Separated by 4.28 km of rugged terrain, distinct topography, and road approaches.
- **Independent visitor intent:** Nature enthusiasts and eco-tourists visit Karkatgarh for waterfall scenery, hanging bridge walks, and river gorges. History and architecture enthusiasts visit Bakhtiyar Khan's tomb to study Afghan domed architecture and Suri-period stone masonry.
- **Separate representation justification:** State Protected Monument under the Directorate of Archaeology; represents medieval monumental architecture in contrast to river gorge hydrology.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION**.

### 5. Khuda Bakhsh Oriental Public Library (Patna) — 1.35 km from Takht Sri Patna Sahib (ID 2)
- **Is it the same attraction?** **No.** Takht Sri Patna Sahib is the birthplace of Guru Gobind Singh Ji and one of the five holy Takhts of Sikhism. Khuda Bakhsh Oriental Public Library is an autonomous National Institution of bibliographical and manuscript heritage on Ashok Rajpath.
- **Is it an attached monument?** **No.** Separated by 1.35 km along the urban arterial corridor of Ashok Rajpath in Patna.
- **Independent visitor intent:** Pilgrims visit Patna Sahib for religious devotion, prayer, and langar. Scholars, international tourists, and heritage connoisseurs visit Khuda Bakhsh Library to view rare imperial Mughal manuscripts, calligraphy, and miniature paintings.
- **Separate representation justification:** Statutory Institution of National Importance declared by Act of Parliament (Act No. 43 of 1969); holds global UNESCO Memory of the World cultural standing.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION**.

---

## 6. Circuit & Spatial Analysis

Each candidate enriches local and regional travel circuits:

1. **Lakhisarai Circuit:** `Ashok Dham Temple` -> `Lali Pahadi Archaeological Site` -> `Shringirishi Dham` (Combines modern grand temple, ancient 11th-century Buddhist nunnery, and sacred spring hills into a seamless day circuit).
2. **Samastipur Heritage Circuit:** `Dr. Rajendra Prasad CAU, Pusa` (Colonial agricultural history) -> `Khudneshwar Asthan, Morwa` (Syncretic harmony) -> `Vidyapati Dham` (Maithili literary shrine).
3. **Mithila & Ramayana Circuit:** `Janaki Sthan` (Sitamarhi) -> `Punaura Dham` -> `Panth Pakar` (Sacred banyan resting spot) -> `Ahilya Sthan` (Ahiyari, Darbhanga) -> `Chandradhari Museum` (Darbhanga).
4. **Eastern Bihar Riverfront Circuit:** `Gogabil Lake Bird Sanctuary` -> `Manihari Ganga Ghat & Maharshi Mehi Ashram` -> `Vikramshila Gangetic Dolphin Sanctuary` (Bhagalpur) -> `Bateshwar Sthan`.
5. **Munger Hills & Wellness Circuit:** `Munger Fort` -> `Rishi Kund Thermal Springs` -> `Kharagpur Lake` -> `Bhimbandh Wildlife Sanctuary`.
6. **Saran-Saryu Confluence Circuit:** `Ambika Sthan, Aami` -> `Chirand Archaeological Site` -> `Gautam Asthan, Revelganj` -> `Manjhi Fort Ruins & Ancient Mound`.
7. **Kaimur Plateau Heritage Circuit:** `Mundeshwari Temple` -> `Tomb of Bakhtiyar Khan, Chainpur` -> `Karkatgarh Waterfall & Eco Park` -> `Telhar Kund`.
8. **Siwan-Ghaghra Spiritual Circuit:** `Zeeradei` (First President's birthplace) -> `Baba Mahendra Nath Temple, Mehdar` -> `Sohagara Dham` (Border Hansnath shrine).
9. **Patna Imperial Heritage Walk:** `Bihar Museum` -> `Patna Museum` -> `Golghar` -> `Khuda Bakhsh Oriental Public Library` -> `Takht Sri Patna Sahib`.

---

## 7. Candidate Queues Reconciliation & Status Breakdown

### Summary of Evaluated Candidates
- **Total Candidates Evaluated:** 47
- **Approval-Ready:** 10
- **Hold (Plausible / Saturation / Needs Field Verification):** 15
- **Rejected (Commercial / Infrastructure / No Tourism Value):** 10
- **Duplicate / Alias / Subcomponent:** 12

### Held Candidates (15)
1. **Nagi Dam Bird Sanctuary, Jamui:** Notified Wildlife Sanctuary and Ramsar site 2541; located 3.10 km from Nakti Dam; Jamui already heavily represented with 11 active places. Held for geographic equity.
2. **Kauwadol Hill & Colossal Buddha Statue, Gaya:** ASI protected monument with 8-foot seated Buddha; located 4.10 km from Barabar; Gaya already has 12 active places. Held for geographic balance.
3. **Kurkihar Archaeological Site, Gaya:** World-famous 9th-12th century Pala bronze hoard discovery site; held due to heavy Gaya representation (12 active destinations).
4. **Sun Temple, Tarari, Bhojpur:** Medieval Sun temple in Dev village; Bhojpur recently gained Ara House in Batch 8; held for future consideration.
5. **Buddha Relic Stupa, Vaishali:** Excavated mud stupa of the Lichchhavis; held due to 0.93 km marker proximity to ID 10; Vaishali already has 3 active places.
6. **Chankigarh Fort, West Champaran:** Massive 90-foot ancient brick mound; held to avoid Champaran saturation (already 6 active destinations).
7. **Bettiah Raj Palace Complex, West Champaran:** Historic 18th-century zamindari palace; ongoing court receiver administration and property disputes.
8. **Amjhar Sharif, Aurangabad:** Sufi shrine on official Bihar Tourism circuit; Aurangabad already has 4 active places; held for geographic balance.
9. **Husepur Fort Ruins, Gopalganj:** Historic fort ruins of Raja Fateh Bahadur Sahi; Gopalganj recently gained Lakri Dargah in Batch 8; held for future batch.
10. **Nagarjuni Caves, Jehanabad:** Adjacent Maurya-era cave complex 1.78 km from Barabar Caves (ID 5); part of the canonical Barabar-Nagarjuni archaeological cluster.
11. **Dharahara Village, Supaul:** Renowned tree-planting social tradition; held as community socio-cultural practice without formal tourism infrastructure.
12. **Sheohar Raj Palace, Sheohar:** Former 19th-century estate residence; disputed private property without official tourism department notification.
13. **Indrasal Cave, Parvati Hill, Nawada:** Scholarly debate and coordinate divergence between Giriyak Hill and Parvati Hill; held pending field verification.
14. **Sagar Dih Mound & Stupa, East Champaran:** Archaeological stupa mound near Raxaul; East Champaran has 3 active destinations; held pending further ASI excavation documentation.
15. **Agnihotri Temple, Khagaria:** Local Shaivite temple; lacks Grade A/B institutional documentation on Bihar Tourism or district portal; held.

---

## 8. Database Invariance Verification

```sql
-- 1. Active Places Count
SELECT COUNT(*) FROM places WHERE deleted_at IS NULL;
-- Result: 148 (Strictly unchanged)

-- 2. Maximum Place ID
SELECT MAX(id) FROM places;
-- Result: 198 (Strictly unchanged)

-- 3. Distinct Districts Covered
SELECT COUNT(DISTINCT district_id) FROM places WHERE deleted_at IS NULL;
-- Result: 38 / 38 (100% coverage preserved)
```

No mutation, insert, update, soft delete, or schema alteration was performed. The system remains in **STRICT READ-ONLY MODE**.
