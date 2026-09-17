# HiddenYatra — Batch 8 Candidate Research & Approval Preview

## 1. Executive Summary & Verified Baseline

- **Current Active Inventory:** 138 destinations (`deleted_at IS NULL`)
- **Bihar Districts Covered:** 38 / 38 (100% geographic coverage)
- **Current Maximum ID:** 188
- **Latest Live Batch:** Batch 7 (IDs 179–188, fully regression tested)
- **Database Status:** LIVE, verified, strictly READ-ONLY for this research phase.
- **Batch 8 Candidate Target:** Exactly 10 top-tier, non-inserted destinations meeting strict **Grade A** authoritative evidence standards.
- **Verified District IDs:** All 10 district IDs queried directly from the `districts` table (`Bhojpur=16`, `Darbhanga=18`, `Muzaffarpur=7`, `Saharsa=29`, `Purnia=28`, `Buxar=17`, `Nawada=38`, `Saran=31`, `Gopalganj=19`, `Supaul=36`).

---

## 2. Approved Batch 8 Candidate Table

| Rank | Candidate Name | District | Dist ID | Category | Latitude | Longitude | Canonical Slug | Nearest Existing Place | Min Dist (km) | Overlap Class | Tourism Value | Why It Adds New Value | Primary Source | Evidence Conf. | Priority | Risk / Notes |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | Ara House | Bhojpur | 16 | `historical` | 25.5539 | 84.6680 | `ara-house-bhojpur` | Aranya Devi Temple (Bhojpur) | 0.88 | SAME SITE / SEVERE OVERLAP (Special Scrutiny) | Historic 1857 uprising fortification where 68 defenders endured the Siege of Arrah by Babu Veer Kunwar Singh; two-storeyed defensive structure with original embrasures on high plinth. | Adds premier 1857 Indian Mutiny military history to Bhojpur; perfectly complements Veer Kunwar Singh Fort in Jagdishpur and expands central Bihar heritage. | `bihar.gov.in` (Heritage Site: Ara House, Maharaja College) | **HIGH (Grade A)** | **P1** | Located 0.88 km south of Aranya Devi in Maharaja College campus; distinct historical military site vs. religious temple. Approved with Special Scrutiny justification. |
| **2** | Ahilya Sthan, Ahiyari | Darbhanga | 18 | `cultural` | 26.2917 | 85.8015 | `ahilya-sthan-ahiyari-darbhanga` | Darbhanga Raj (Laxmi Vilas Palace) (Darbhanga) | 18.21 | DISTINCT DESTINATION | Ancient Ramayana circuit heritage shrine in Ahiyari village marking the spot of Devi Ahilya’s deliverance by Lord Rama; celebrated venue of massive Ram Navami gatherings. | Brings authentic epic Ramayana circuit heritage to Darbhanga; situated 18.2 km northwest of Darbhanga Raj Palace, providing critical rural tourism spread in Jale block. | `darbhanga.nic.in` (Places of Interest: Ahilya Sthan) | **HIGH (Grade A)** | **P1** | Distinct from Ahirauli in Buxar; this is the primary Darbhanga Ahilya Sthan in Ahiyari village near Kamtaul. Fully verified. |
| **3** | Baba Garibnath Temple | Muzaffarpur | 7 | `temple` | 26.1205 | 85.3912 | `baba-garibnath-temple-muzaffarpur` | Litchi Gardens & Jubba Sahni Park (Muzaffarpur) | 2.65 | NEARBY BUT DISTINCT (Special Scrutiny) | Celebrated as the "Deoghar of North Bihar"; historic 300-year-old Shiva pilgrimage center and primary terminus for millions of Kanwariya pilgrims performing Jalabhishek during Shravan. | Fills a major spiritual pilgrimage void in Muzaffarpur district; actively backed by Bihar State Tourism Development Corporation (BSTDC) corridor redevelopment project. | `tourism.bihar.gov.in` (Baba Garibnath Temple & BSTDC Corridor) | **HIGH (Grade A)** | **P1** | Located 2.65 km from Jubba Sahni Park in urban Muzaffarpur; distinct spiritual temple typology vs municipal park. Approved with Special Scrutiny justification. |
| **4** | Surya Mandir, Kandaha | Saharsa | 29 | `historical` | 25.8820 | 86.4670 | `surya-mandir-kandaha-saharsa` | Shri Ugratara Sthan, Mahishi (Saharsa) | 2.58 | NEARBY BUT DISTINCT (Special Scrutiny) | Rare medieval Sun temple housing an exquisitely carved monolithic granite idol of Lord Surya on a seven-horse chariot, bearing an authentic 14th-century Sanskrit inscription of King Narasimha Deva. | Adds exceptional archaeological and epigraphic depth to Saharsa; recognized by the Archaeological Survey of India (ASI) and featured on the official district portal. | `saharsa.nic.in` (Places of Interest: Surya Mandir, Kandaha) | **HIGH (Grade A)** | **P1** | Located 2.58 km from Ugratara Sthan in distinct Kandaha village/Pastwar panchayat; forms ideal archaeological-spiritual circuit in western Saharsa. Approved with Special Scrutiny. |
| **5** | Mata Puran Devi Temple | Purnia | 28 | `cultural` | 25.7725 | 87.4580 | `mata-puran-devi-temple-purnia` | Kajha Kothi Eco Park (Purnia) | 12.27 | DISTINCT DESTINATION | Ancient titular temple dedicated to Goddess Puran Devi, universally acknowledged as the eponym from which the historic district and city of Purnia derives its name. | Provides essential cultural identity and origin heritage to Purnia district; currently supported by active Bihar Tourism infrastructure redevelopment. | `purnea.nic.in` (Tourist Places: Puran Devi Mandir) | **HIGH (Grade A)** | **P1** | Located 5 km from Purnea city center; 12.27 km from Kajha Kothi. Zero overlap with existing inventory. |
| **6** | Baba Brahmeshwar Nath Temple, Brahmpur | Buxar | 17 | `temple` | 25.5992 | 84.2882 | `baba-brahmeshwar-nath-temple-brahmpur-buxar` | Veer Kunwar Singh Fort, Jagdishpur (Bhojpur) | 19.58 | DISTINCT DESTINATION | Ancient west-facing swayambhu Shiva temple reverently known as "Mini Kashi" of Shahabad; host of the historic annual Brahmpur cattle fair and major Shaivite pilgrimage destination. | Anchors eastern Buxar’s pilgrimage corridor along NH-922 / Bhojpur border; situated 32.5 km east of Buxar town, expanding district coverage beyond the municipal center. | `tourism.bihar.gov.in` (Brahmeshwar Nath Temple, Brahmapur) | **HIGH (Grade A)** | **P1** | High seasonal pilgrim traffic during Mahashivratri and Sawan. Established road connectivity from Ara and Buxar. |
| **7** | Gunawa Ji (Jain Tirth) | Nawada | 38 | `cultural` | 24.8944 | 85.5312 | `gunawa-ji-jain-tirth-nawada` | Ghora Katora Lake Eco-Reserve (Nalanda) | 11.98 | DISTINCT DESTINATION | Picturesque Jain Jal Mandir constructed in the center of an expansive lotus lake; sacred site where Indrabhuti Gautama Swami, chief disciple of Lord Mahavira, attained Kevala Jnana. | Expands Bihar’s renowned Jain pilgrimage circuit into Nawada district; beautifully complements Pawapuri Jal Mandir and Kakolat Waterfall. | `tourism.bihar.gov.in` (Jain Circuit: Gunawa Ji Tirth, Nawada) | **HIGH (Grade A)** | **P1** | Located 3 km from Nawada town on the Patna-Ranchi Highway; peaceful water temple complex with dharmashala facilities. |
| **8** | Ambika Sthan, Aami | Saran | 31 | `cultural` | 25.6881 | 85.0062 | `ambika-sthan-aami-saran` | Maner Sharif (Patna) | 12.94 | DISTINCT DESTINATION | Ancient Shaktipeeth fort-mound temple complex perched on the northern cliff of the Ganga at Dighwara; mythologically linked to Daksha’s Yajna and the sacred clay pindi of Maa Ambika. | Brings sacred riverfront Shaktipeeth heritage to Saran district; situated 34.8 km east of Gautam Asthan and 22 km west of Sonepur, linking the Chhapra-Patna corridor. | `tourism.bihar.gov.in` (Ambika Sthan, Aami, Dighwara) | **HIGH (Grade A)** | **P1** | Historic elevated mound structure overlooking the Ganga floodplain; substantial Navratri congregations. |
| **9** | Lakri Dargah | Gopalganj | 19 | `cultural` | 26.3150 | 84.4720 | `lakri-dargah-gopalganj` | Thawe Mandir (Gopalganj) | 15.92 | DISTINCT DESTINATION | Historic 16th-century Sufi pilgrimage shrine and mausoleum of saint Shah Arzan, richly endowed by Mughal Emperor Aurangzeb; renowned for antique wood craftsmanship and annual Urs. | Enriches Gopalganj’s tourism profile beyond temple sites (Thawe) and prehistoric mounds (Dighwa Dubauli) by adding prominent Sufi architecture and syncretic cultural heritage. | `gopalganj.nic.in` (Places of Interest: Lakri Dargah) | **HIGH (Grade A)** | **P1** | Located in Barharia/Manjha block; 15.92 km from Thawe Mandir. Stable rural road access. |
| **10** | Baba Tileshwar Nath Mandir, Sukhpur | Supaul | 36 | `temple` | 26.0620 | 86.6080 | `baba-tileshwar-nath-mandir-sukhpur-supaul` | Matsyagandha Lake & Raktakali Temple (Saharsa) | 19.98 | DISTINCT DESTINATION | Ancient, venerated Swayambhu Shivalinga temple located in Sukhpur Solhani; celebrated as the primary traditional spiritual pilgrimage center of the lower Kosi basin. | Provides indispensable second destination depth to Supaul district (which currently has only 1 active destination, Kosi Barrage); supported by district administration tourism initiatives. | `supaul.nic.in` (Places of Interest: Tileshwar Mandir) | **HIGH (Grade A)** | **P1** | Located 10 km south of Supaul headquarters; 54 km south of Kosi Barrage (Birpur). Zero collision risk. |

---

## 3. District Depth & Representation Impact

All 10 proposed candidates provide **depth expansion to underrepresented districts**, with 8 out of 10 candidates elevating districts that currently possess only 1 or 2 destinations:

| District | Actual DB ID | Current Active Places | Post-Batch 8 Projected | Delta | Added Destination | Current Destinations in District |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Supaul** | **36** | 1 | **2** | +1 | Baba Tileshwar Nath Mandir, Sukhpur | Kosi Barrage, Birpur |
| **Bhojpur** | **16** | 2 | **3** | +1 | Ara House | Veer Kunwar Singh Fort, Aranya Devi Temple |
| **Darbhanga** | **18** | 2 | **3** | +1 | Ahilya Sthan, Ahiyari | Darbhanga Raj (Laxmi Vilas Palace), Kusheshwar Asthan |
| **Muzaffarpur** | **7** | 2 | **3** | +1 | Baba Garibnath Temple | Litchi Gardens / Jubba Sahni Park, Sujani Embroidery Cluster |
| **Saharsa** | **29** | 2 | **3** | +1 | Surya Mandir, Kandaha | Shri Ugratara Sthan, Matsyagandha Lake & Raktakali Temple |
| **Purnia** | **28** | 2 | **3** | +1 | Mata Puran Devi Temple | Jalalgarh Fort, Kajha Kothi Eco Park |
| **Nawada** | **38** | 2 | **3** | +1 | Gunawa Ji (Jain Tirth) | Kakolat Waterfall, Sarvodaya Ashram (Shekhodeora) |
| **Gopalganj** | **19** | 2 | **3** | +1 | Lakri Dargah | Thawe Mandir, Dighwa Dubauli Archaeological Mounds |
| **Buxar** | **17** | 3 | **4** | +1 | Baba Brahmeshwar Nath Temple | Battle of Buxar Memorial, Chausa Battlefield, Ramrekha Ghat |
| **Saran** | **31** | 3 | **4** | +1 | Ambika Sthan, Aami | Sonepur Hariharnath Temple, Chirand Site, Gautam Asthan |

---

## 4. Category Diversity Analysis

The Batch 8 candidate roster deliberately avoids generic repetition by curating diverse heritage domains:

| Category | Batch 8 Count | Percentage | Candidates |
| :--- | :---: | :---: | :--- |
| **cultural** | 5 | 50.0% | Ahilya Sthan (Epic Ramayana Circuit), Mata Puran Devi (Titular city heritage), Gunawa Ji (Jain Jal Mandir on lake), Ambika Sthan (Ancient river-cliff Shaktipeeth), Lakri Dargah (Mughal-era Sufi shrine) |
| **temple** | 3 | 30.0% | Baba Garibnath (Deoghar of North Bihar), Baba Brahmeshwar Nath (Mini Kashi & Cattle Fair), Baba Tileshwar Nath (Swayambhu Kosi Shivalinga) |
| **historical** | 2 | 20.0% | Ara House (1857 Mutiny fortress siege site), Surya Mandir Kandaha (ASI recognized 14th-century Oinwar inscribed temple) |
| **Total** | **10** | **100.0%** | **Balanced across 10 separate districts** |

---

## 5. Special Scrutiny: Candidates Under 5 km

In strict compliance with the Special Scrutiny directive, three candidates situated within 5 km of existing markers were rigorously audited:

### 1. Ara House (Bhojpur) — 0.88 km from Aranya Devi Temple (ID 119)
- **Is it the same attraction?** **No.** Aranya Devi is an ancient religious shrine dedicated to the presiding goddess of the forest/town situated in the old market near the Gangi river. Ara House is a secular 19th-century British-engineered military fortress building located inside the Maharaja College campus south of Ramna Maidan.
- **Is it an attached monument?** **No.** They sit on completely separate municipal parcels with distinct addresses, separated by the main town thoroughfare, urban market streets, and distinct administrative bodies.
- **Legitimacy as a standalone destination:** Ara House is an internationally celebrated landmark of the 1857 Indian Uprising (site of the historic 8-day Siege of Arrah by Babu Veer Kunwar Singh), featured independently on `bihar.gov.in` under State Heritage Monuments. It offers a totally distinct educational/historical military visitor experience compared to the ancient temple.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION** (Completely distinct identity, category, and parcel).

### 2. Baba Garibnath Temple (Muzaffarpur) — 2.65 km from Litchi Gardens & Jubba Sahni Park (ID 27)
- **Is it the same attraction?** **No.** Jubba Sahni Park is an eco-park and municipal recreational garden on Club Road/Mithanpura. Baba Garibnath is a 300-year-old major Hindu pilgrimage temple located in the heart of old Muzaffarpur.
- **Is it an attached monument?** **No.** Located 2.65 km apart in completely separate sectors of Muzaffarpur city.
- **Legitimacy as a standalone destination:** Celebrated as the "Deoghar of North Bihar", it is the premier Shaivite pilgrimage destination of Tirhut division drawing millions of Kanwariyas during Shravani Mela. It has an active multi-crore state corridor redevelopment project by BSTDC.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION** (Complementary urban pairing, distinct category and visitor profile).

### 3. Surya Mandir, Kandaha (Saharsa) — 2.58 km from Shri Ugratara Sthan, Mahishi (ID 130)
- **Is it the same attraction?** **No.** Ugratara Sthan is an active Tantric Shaktipeeth temple in Mahishi bazaar. Kandaha Sun Temple is a distinct archaeological site in Pastwar Panchayat (Kandaha village), featuring a 14th-century Oinwar dynasty inscription of King Narasimha Deva and black granite Surya idol on a seven-horse chariot.
- **Is it an attached monument?** **No.** Located 2.58 km apart across separate revenue villages and panchayats.
- **Legitimacy as a standalone destination:** Recognized by the Archaeological Survey of India (ASI) and featured separately on `saharsa.nic.in`. Forms an ideal day-tour circuit with Mahishi without spatial or thematic confusion.
- **Recommendation:** **APPROVED WITH SPECIAL SCRUTINY JUSTIFICATION** (Distinct village, distinct deity, ASI-documented archaeological and epigraphical value).

---

## 6. Candidate Queues Reconciliation & Summary of Non-Selected Candidates

### Summary of Evaluated Candidates
- **Total Candidates Evaluated:** 44
- **Approval-Ready:** 10
- **Hold (Plausible / Low Priority / Proximity):** 15
- **Rejected (Commercial / Infrastructure / No Tourism Value):** 10
- **Duplicate / Alias / Subcomponent:** 9

### Held Candidates (15)
1. **Chandradhari Museum, Darbhanga:** Premier 11-gallery Mithila antiquities museum. Located 0.87 km from Darbhanga Raj Palace. Held for future batch to prioritize rural Ramayana Circuit anchor Ahilya Sthan (Ahiyari) for Darbhanga in Batch 8.
2. **Khudneshwar Asthan, Samastipur:** Historic 1858 Hindu-Muslim syncretic shrine in Morwa where a Shivalinga and mazar of Khudni Biwi share the sanctum. Held for Batch 9 to preserve strict 1-candidate-per-district balance.
3. **Lali Pahadi Archaeological Site, Lakhisarai:** Excavated hilltop Buddhist nunnery ("Shrimaddharma Vihara") with 27 cells. Lakhisarai recently gained Shringirishi Dham in Batch 6; held for Batch 9 to prioritize underrepresented districts.
4. **Manihari Ganga Ghat, Katihar:** Sacred Ganga ghat and Maharshi Mehi Ashram; held for Batch 9 as Katihar recently gained Lakshmipur Gurdwara in Batch 6.
5. **Sun Temple, Tarari, Bhojpur:** Medieval Sun temple in Dev village; held in favor of 1857 flagship fortress Ara House for Bhojpur.
6. **Buddha Relic Stupa, Vaishali:** Excavated mud stupa of the Lichchhavis; held due to 0.14 km marker proximity to ID 10; Vaishali already has 3 places.
7. **Nagi Dam Bird Sanctuary, Jamui:** Notified Wildlife Sanctuary and Ramsar site; located 3.10 km from Nakti Dam; Jamui already has 11 active places.
8. **Kauwadol Hill & Colossal Buddha Statue, Gaya:** ASI protected monument with 8-foot seated Buddha; located 4.10 km from Barabar; Gaya already has 12 active places.
9. **Dharahara Village, Supaul:** Renowned tree-planting social tradition; held as community socio-cultural practice without formal tourism infrastructure.
10. **Chankigarh Fort, West Champaran:** Massive 90-foot ancient brick mound; held to avoid Champaran saturation (already 6 active places).
11. **Bettiah Raj Palace Complex, West Champaran:** Historic 18th-century zamindari palace; ongoing court receiver administration and property disputes.
12. **Tomb of Bakhtiyar Khan, Kaimur:** State Protected medieval mausoleum in Chainpur; Kaimur already has 4 active places; held for geographic balance.
13. **Amjhar Sharif, Aurangabad:** Sufi shrine on official Bihar Tourism circuit; Aurangabad already has 4 active places; held for geographic balance.
14. **Sheohar Raj Palace, Sheohar:** Former 19th-century estate residence; disputed private property without official tourism department notification.
15. **Indrasal Cave, Parvati Hill, Nawada:** Scholarly debate and coordinate divergence between Giriyak Hill and Parvati Hill; held pending field verification.

### Rejected Candidates (10)
1. **Arwal Bus Stand Commercial Complex:** Generic transit retail infrastructure; zero tourism value.
2. **Barauni IOCL Refinery Township:** Active petrochemical industrial complex; restricted entry, no public tourism access.
3. **Ara Sadar Hospital:** Municipal healthcare facility; zero tourism value.
4. **Buxar Central Jail:** Active correctional security institution; restricted access.
5. **Samastipur Dairy Milk Plant:** Industrial milk processing plant; commercial industrial property.
6. **Chhapra Main Bazar Cloth Market:** Local commercial clothing market; generic retail.
7. **Hotel Grand Sheohar:** Commercial lodging business; generic private enterprise.
8. **Siwan Civil Court Complex:** Judicial administrative premises; zero tourism value.
9. **Katihar Railway Junction Yard:** Active railway operational infrastructure; restricted entry.
10. **Purnea College Academic Campus:** Active educational institution; not a standalone tourism destination.

### Duplicate / Alias / Subcomponent Candidates (9)
1. **Saptaparni Cave:** Subcomponent of Rajgir hill complex (ID 9, 1.48 km); first Buddhist council cave, already subsumed under Rajgir destination.
2. **Cyclopean Wall of Rajgir:** Pre-Mauryan 40-km cyclopean perimeter wall surrounding Rajgir; integral perimeter feature of active destination ID 9.
3. **Rajgir Glass Bridge & Nature Safari:** Eco-adventure park in Jethian valley, 5.58 km from Rajgir (ID 9); Nalanda already has 5 active destinations.
4. **Papaharini Tank:** Sacred water tank situated directly at the foothills of Mandar Hill (ID 12, 0.42 km); same-site complex component.
5. **Sujata Stupa & Kuti:** Excavated brick stupa across Falgu river, 1.42 km from Bodh Gaya / Mahabodhi complex; tightly clustered with existing Gaya inventory.
6. **Ranti Art Village:** Mithila painting artisan village 1.72 km from Jitwarpur Art Village (ID 13); same artisan cluster.
7. **Nagarjuni Caves:** Adjacent Maurya-era cave complex 1.78 km from Barabar Caves (ID 5); part of the canonical Barabar-Nagarjuni archaeological cluster.
8. **Balirajgarh:** Alternate local name / official archaeological name for Raja Bali Ka Garh (ID 184).
9. **Ahirauli Ahilya Sthan:** Buxar rural shrine 4.12 km from Battle of Buxar Memorial; distinct from Ahilya Sthan, Ahiyari (Darbhanga).

---

## 7. Database Invariance Audit

Verification executed against active MySQL database:
```sql
SELECT COUNT(*) FROM places WHERE deleted_at IS NULL;       -- Result: 138 (Verified)
SELECT MAX(id) FROM places;                                  -- Result: 188 (Verified)
SELECT COUNT(DISTINCT district_id) FROM places WHERE deleted_at IS NULL; -- Result: 38 (Verified)
```
- Active inventory has remained **100% read-only and invariant** throughout this phase.
- Zero INSERT, UPDATE, DELETE, or schema alterations were performed.
