# BIHAR BATCH 7 CANDIDATE APPROVAL PREVIEW

> **Status**: PROPOSED FOR HUMAN APPROVAL (STRICT READ-ONLY AUDIT MODE)  
> **Current Active Baseline**: 128 destinations across 38/38 Bihar districts (Batch 1–6 Live & Verified)  
> **Projected Active Inventory After Batch 7**: 138 destinations  
> **Statewide District Coverage**: 38/38 districts (100% maintained)  
> **Database Safety**: Zero database mutations, zero schema changes, zero modified existing records.

---

## 1. Executive Summary & Strategic Rationale

Following the successful atomic deployment and verification of Batch 6 (which established the current verified baseline of 128 active places across all 38 districts of Bihar), **Batch 7** executes a targeted strategy focused on **depth in weakly represented districts**, **institutional heritage flagships**, and **thematic experience diversity**.

Rather than concentrating additional destinations in saturated tourism hubs (such as Patna with 18 destinations, Gaya with 12, or Jamui with 11), Batch 7 delivers three transformative strategic breakthroughs:

1. **Empowering Five 1-Place Districts into Multi-Destination Tourism Circuits**:
   - **Siwan** (1 → 2): **Baba Mahendra Nath Temple, Mehdar** (17th-century King of Nepal Shaivite temple on 55-acre Kamaldah Lake, state-sponsored Mehdar Mahotsav)
   - **Arwal** (1 → 2): **Aganoor Mini Hydroelectric Project** (Scenic barrage, mini hydel waterfalls, and canal promenade on the Sone River network)
   - **Samastipur** (1 → 2): **Dr. Rajendra Prasad Central Agricultural University** (India's historic 1905 Imperial Agricultural Research Institute heritage campus, colonial architecture, Curzon grounds, agricultural museum)
   - **Madhepura** (1 → 2): **Baba Vishu Raut Temple, Pachrasi Dham** (300-year-old pastoral folk hero shrine, perpetual milk-offering tradition, state-recognized Rajkiya Mela)
   - **Kishanganj** (1 → 2): **Kanhaiya Ji Mandir, Bandarjhula** (ASI Centrally Protected Monument, 8th–9th century black basalt monolithic Vishnu/Krishna statue and ancient mounds on the Indo-Nepal border)

2. **Deepening Three 2-Place Districts into Tri-Destination Tourism Corridors**:
   - **Begusarai** (2 → 3): **Jaimangla Garh** (Ancient fortified island mound and 9th–10th century Chandi Mangla Devi Shaktipeeth on Kanwar Lake)
   - **Buxar** (2 → 3): **Ramrekha Ghat** (Prime sacred Ganga riverfront, Ramayana Treta Yuga crossing site, ₹13.24 Cr Bihar Tourism development, evening Ganga Aarti)
   - **Saran** (2 → 3): **Gautam Asthan, Revelganj** (Sacred hermitage on the Saryu River, Ramayana Ahilya Uddhar site, Kartik Purnima fair)

3. **Deploying Seniority-Audited P0 Flagship Monuments**:
   - **West Champaran**: **Bhitiharwa Gandhi Ashram** (P0 crown jewel; founded 20 November 1917 by Mahatma Gandhi during Champaran Satyagraha, original Kasturba school hut, preserved bell, Gandhi Smriti museum)
   - **Madhubani**: **Raja Bali Ka Garh** (Centrally Protected Monument of National Importance under ASI since 1938; sprawling 176-acre fortified ancient city with 40-foot brick ramparts)

---

## 2. Batch Composition & Experience Diversity Check

- **Total Proposed Candidates**: Exactly 10 (Quality > Quantity)
- **Districts Represented**: Exactly 10 unique districts (West Champaran, Siwan, Begusarai, Buxar, Arwal, Madhubani, Samastipur, Madhepura, Kishanganj, Saran) — **Zero district repetition**
- **Districts Gaining Second Destination**: 5 districts (Siwan, Arwal, Samastipur, Madhepura, Kishanganj)
- **Districts Gaining Third Destination**: 3 districts (Begusarai, Buxar, Saran)
- **Category Distribution**:
  - `historical`: 5 (*Bhitiharwa Gandhi Ashram*, *Jaimangla Garh*, *Raja Bali Ka Garh*, *Dr. Rajendra Prasad Central Agricultural University*, *Kanhaiya Ji Mandir, Bandarjhula*)
  - `cultural`: 3 (*Ramrekha Ghat*, *Baba Vishu Raut Temple, Pachrasi Dham*, *Gautam Asthan, Revelganj*)
  - `temple`: 1 (*Baba Mahendra Nath Temple, Mehdar*)
  - `tourist_spot`: 1 (*Aganoor Mini Hydroelectric Project*)
- **Category Rule Adherence**: 100% compliant with existing allowed database categories. Zero new enum values introduced.
- **Institutional Evidence Standard**: 100% Grade A (ASI Centrally Protected, Ministry of Culture, Bihar Tourism, District NIC portals, Central University Act).

---

## 3. Candidate Master Table

| Rank | Candidate Name | District | District ID | Category | Latitude | Longitude | Canonical Slug | Nearest Active Place | Haversine (km) | Overlap Classification | Confidence | Priority |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **1** | **Bhitiharwa Gandhi Ashram** | West Champaran | 9 | `historical` | 27.2437 | 84.4838 | `bhitiharwa-gandhi-ashram-west-champaran` | Rampurva Ashokan Pillars (ID 149) | 3.25 | Legitimate separate destination (Freedom struggle vs Mauryan pillar) | **A** | **P0** |
| **2** | **Baba Mahendra Nath Temple, Mehdar** | Siwan | 35 | `temple` | 25.9870 | 84.4380 | `baba-mahendra-nath-temple-mehdar-siwan` | Zeeradei (ID 135) | 33.40 | Clearly separate destination (>33 km; major Shaivite lake shrine) | **A** | **P0** |
| **3** | **Jaimangla Garh** | Begusarai | 15 | `historical` | 25.5921 | 86.1613 | `jaimangla-garh-begusarai` | Kanwar Lake Bird Sanctuary (ID 20) | 6.54 | Genuinely separate destination (Fort mound/temple vs wetland reserve) | **A** | **P1** |
| **4** | **Ramrekha Ghat** | Buxar | 17 | `cultural` | 25.5761 | 83.9711 | `ramrekha-ghat-buxar` | Battle of Buxar Memorial (ID 23) | 1.73 | Legitimate companion destination (Ganga pilgrim ghat vs inland battle park) | **A** | **P0** |
| **5** | **Aganoor Mini Hydroelectric Project** | Arwal | 12 | `tourist_spot` | 25.1328 | 84.5385 | `aganoor-mini-hydroelectric-project-arwal` | Daud Khan Fort (ID 152) / Makhdum Dargah (ID 115) | 17.74 | Clearly separate destination (>17 km; scenic river barrage in south Arwal) | **A** | **P1** |
| **6** | **Raja Bali Ka Garh** | Madhubani | 20 | `historical` | 26.4595 | 86.3230 | `raja-bali-ka-garh-madhubani` | Rajnagar Palace Complex (ID 154) | 18.96 | Clearly separate destination (>18 km; 176-acre ASI national monument) | **A** | **P0** |
| **7** | **Dr. Rajendra Prasad Central Agricultural University** | Samastipur | 30 | `historical` | 25.9860 | 85.6754 | `dr-rajendra-prasad-central-agricultural-university-samastipur` | Sujani Craft Cluster (ID 168) / Vidyapati Dham (ID 131) | 26.71 | Clearly separate destination (>26 km; 1905 imperial colonial campus) | **A** | **P1** |
| **8** | **Baba Vishu Raut Temple, Pachrasi Dham** | Madhepura | 27 | `cultural` | 25.4450 | 87.0250 | `baba-vishu-raut-temple-pachrasi-dham-madhepura` | Vikramshila Gangetic Dolphin (ID 118) / Singheshwar (ID 128) | 17.11 | Clearly separate destination (>17 km; pastoral folklore shrine & state fair) | **A** | **P1** |
| **9** | **Kanhaiya Ji Mandir, Bandarjhula** | Kishanganj | 25 | `historical` | 26.3683 | 87.9636 | `kanhaiya-ji-mandir-bandarjhula-kishanganj` | Kishanganj Tea Gardens (ID 126) | 18.34 | Clearly separate destination (>18 km; ASI protected black basalt statue) | **A** | **P1** |
| **10** | **Gautam Asthan, Revelganj** | Saran | 31 | `cultural` | 25.7812 | 84.6712 | `gautam-asthan-revelganj-saran` | Chirand Archaeological Site (ID 148) | 16.08 | Clearly separate destination (>16 km; Saryu riverfront Ramayana hermitage) | **A** | **P1** |

---

## 4. Comprehensive Destination Dossiers

### Candidate #1: Bhitiharwa Gandhi Ashram
- **District**: West Champaran (District ID: 9)
- **Category**: `historical`
- **Coordinates**: `27.2437, 84.4838`
- **Nearest Active Destination**: Rampurva Ashokan Pillars (ID 149) at **3.25 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Legitimate separate destination (3.25 km SW; national 20th-century freedom struggle heritage vs 3rd-century BC Mauryan epigraphy).
- **Tourism Value & Why It Adds Value**:
  - Founded on 20 November 1917 by Mahatma Gandhi during the historic Champaran Satyagraha, serving as his grassroots operational headquarters and the first basic school in India.
  - Features the preserved mud-walled and thatched hut where Kasturba Gandhi and Bapu resided, the original historic school bell rung by Gandhi, prayer grounds, and an extensive museum exhibiting authentic khadi artifacts, original correspondence, and rare photographs.
  - Anchor of Bihar Tourism's official Gandhian Circuit; elevates West Champaran beyond ancient monuments into the epicenter of modern Indian freedom history.
- **Primary Source**: District Administration West Champaran (NIC Portal) — https://westchamparan.nic.in/tourist-places/
- **Secondary Source**: Bihar Tourism (Department of Tourism, Govt of Bihar) — https://tourism.bihar.gov.in/en/destinations
- **Confidence**: Grade A | **Priority**: P0

---

### Candidate #2: Baba Mahendra Nath Temple, Mehdar
- **District**: Siwan (District ID: 35)
- **Category**: `temple`
- **Coordinates**: `25.9870, 84.4380`
- **Nearest Active Destination**: Zeeradei (Dr. Rajendra Prasad Ancestral House, ID 135) at **33.40 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>33 km southeast of Zeeradei; major rural Shaivite pilgrimage and lake complex).
- **Tourism Value & Why It Adds Value**:
  - Monumental 17th-century Shaivite pilgrimage complex constructed by King Mahendra Bir Bikram Shah of Nepal on the banks of the expansive 55-acre *Kamaldah Sarovar* (Kamaldah Lake), famous for sacred blooming water lilies.
  - Enshrines an ancient self-manifested Swayambhu Shiva Lingam believed to cure ailments; hosts the annual state-sponsored "Mehdar Mahotsav" and massive Sawan/Mahashivratri congregations.
  - Empowers Siwan from a single-destination district into a multi-destination hub, adding a spiritual, aquatic, and architectural anchor 33 km away from Zeeradei.
- **Primary Source**: District Administration Siwan (NIC Portal) — https://siwan.nic.in/tourist-place/mahendranath-temple/
- **Secondary Source**: Bihar Tourism (Department of Tourism, Govt of Bihar) — https://tourism.bihar.gov.in/en/destinations
- **Confidence**: Grade A | **Priority**: P0

---

### Candidate #3: Jaimangla Garh
- **District**: Begusarai (District ID: 15)
- **Category**: `historical`
- **Coordinates**: `25.5921, 86.1613`
- **Nearest Active Destination**: Kanwar Lake Bird Sanctuary (ID 20) at **6.54 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Genuinely separate destination (6.54 km SE; fortified archaeological island mound and Shaktipeeth temple vs open-water wetland bird sanctuary).
- **Tourism Value & Why It Adds Value**:
  - Ancient fortified island promontory on the southern shore of Kabartal / Kanwar Lake, excavated by the State Archaeology Directorate and ASI, uncovering pre-medieval Pala brick ramparts, moats, and stone sculptures.
  - Houses the sacred 9th–10th century Chandi Mangla Devi Shaktipeeth temple, where the deity is carved in rare black basalt stone, drawing massive pilgrimages during Navratri.
  - Distinguishes the archaeological and religious island promontory from the open-water Ramsar wetland sanctuary, giving Begusarai a rich heritage dimension.
- **Primary Source**: District Administration Begusarai (NIC Portal) — https://begusarai.nic.in/tourist-place/jaimangla-garh/
- **Secondary Source**: Bihar Tourism (Department of Tourism, Govt of Bihar) — https://tourism.bihar.gov.in/en/destinations
- **Confidence**: Grade A | **Priority**: P1

---

### Candidate #4: Ramrekha Ghat
- **District**: Buxar (District ID: 17)
- **Category**: `cultural`
- **Coordinates**: `25.5761, 83.9711`
- **Nearest Active Destination**: Battle of Buxar Memorial (ID 23) at **1.73 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Legitimate companion riverfront destination (1.73 km N; sacred ancient Ganga riverfront ghat and ₹13.24 Cr Ganga Aarti pavilion vs inland 1764 colonial battle monument park).
- **Tourism Value & Why It Adds Value**:
  - Prime sacred Ganga riverfront ghat of Buxar where Lord Rama and Lakshmana crossed the Ganges with Sage Vishwamitra after slaying demoness Tadaka in the Treta Yuga.
  - Features an ancient clay-carved Shivling bearing the legendary handprint of Lord Rama, along with sacred foot imprints (Charan Paduka).
  - Site of a comprehensive ₹13.24 Cr Bihar Tourism riverfront development, featuring paved promenades, illuminated pavilions, and nightly evening Maha Aarti ceremonies modeled after Varanasi.
  - Solves Buxar's severe thematic monotony: currently, Buxar has only two destinations and BOTH are military battlefields (*Battle of Buxar Memorial* and *Chausa Battlefield*). Ramrekha Ghat provides essential living riverfront culture.
- **Primary Source**: District Administration Buxar (NIC Portal) — https://buxar.nic.in/tourist-place/ramrekha-ghat/
- **Secondary Source**: Bihar Tourism (Department of Tourism, Govt of Bihar) — https://tourism.bihar.gov.in/en/destinations
- **Confidence**: Grade A | **Priority**: P0

---

### Candidate #5: Aganoor Mini Hydroelectric Project
- **District**: Arwal (District ID: 12)
- **Category**: `tourist_spot`
- **Coordinates**: `25.1328, 84.5385`
- **Nearest Active Destination**: Daud Khan Fort (ID 152 in Aurangabad) at **17.74 km**; Makhdum Shah Baba Dargah (ID 115 in Arwal) at **18.37 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>17 km; scenic river barrage, mini hydel station, and canal waterfalls in southern Arwal).
- **Tourism Value & Why It Adds Value**:
  - Scenic river barrage and run-of-the-river mini hydroelectric installation built across the major canal network fed by the Sone River in Kaler block.
  - Creates dynamic cascading canal waterfalls, serene reservoir vistas, tree-lined walking bunds, and popular eco-tourism picnic grounds.
  - Empowers Arwal from a single-destination district (previously only Makhdum Shah Baba Dargah) into a multi-destination district, adding modern eco-engineering leisure.
- **Primary Source**: District Administration Arwal (NIC Portal) — https://arwal.nic.in/tourist-place/aganoor-mini-hydroelectric-project/
- **Secondary Source**: Department of Energy, Government of Bihar / BSEB — https://energy.bihar.gov.in/
- **Confidence**: Grade A | **Priority**: P1

---

### Candidate #6: Raja Bali Ka Garh
- **District**: Madhubani (District ID: 20)
- **Category**: `historical`
- **Coordinates**: `26.4595, 86.3230`
- **Nearest Active Destination**: Rajnagar Palace Complex (ID 154) at **18.96 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>18 km; 176-acre ASI Centrally Protected ancient fortified city of national importance).
- **Tourism Value & Why It Adds Value**:
  - Centrally Protected Monument of National Importance under ASI (declared 1938). Sprawling 176-acre fortified ancient city at Balirajgarh (Babubarhi block) enclosed by massive brick ramparts up to 40 feet high.
  - Systematic excavations by ASI revealed five continuous cultural strata: Northern Black Polished Ware (NBPW), Sunga, Kushan, Gupta, and Pala periods, yielding Sunga terracotta art, silver punch-marked coins, and structural brick fortifications.
  - Identified by historians as an ancient urban capital of the Videha Kingdom / Mithila civilization; introduces an archaeological monument of national significance to Madhubani.
- **Primary Source**: Archaeological Survey of India (ASI Patna Circle) — https://asipatnacircle.gov.in/
- **Secondary Source**: District Administration Madhubani (NIC Portal) — https://madhubani.nic.in/tourist-place/baligarh/
- **Confidence**: Grade A | **Priority**: P0

---

### Candidate #7: Dr. Rajendra Prasad Central Agricultural University
- **District**: Samastipur (District ID: 30)
- **Category**: `historical`
- **Coordinates**: `25.9860, 85.6754`
- **Nearest Active Destination**: Sujani Embroidery Craft Cluster (ID 168 in Muzaffarpur) at **26.71 km**; Vidyapati Dham (ID 131 in Samastipur) at **40.52 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>26 km; 1905 Imperial colonial architecture campus, Curzon grounds, agricultural museum).
- **Tourism Value & Why It Adds Value**:
  - The historic birthplace of modern agricultural research in India, founded in 1905 by British Viceroy Lord Curzon with a $100,000 philanthropic grant from American philanthropist Henry Phipps as the Imperial Agricultural Research Institute.
  - Sprawling heritage campus showcasing grand Edwardian architecture, the historic Phipps Laboratory ruins, Curzon Ground, botanical gardens, and arboretum.
  - Houses the Central University Museum exhibiting antique agronomic instruments, pre-independence scientific archives, and plant genetics galleries.
  - Empowers Samastipur from a single-destination district (previously only Vidyapati Dham) into a multi-destination district, adding unique scientific and colonial architectural heritage.
- **Primary Source**: District Administration Samastipur (NIC Portal) — https://samastipur.nic.in/tourist-place/dr-rajendra-prasad-central-agricultural-university-pusa/
- **Secondary Source**: Ministry of Agriculture & Farmers Welfare, Government of India — https://www.pusavarsity.org.in/
- **Confidence**: Grade A | **Priority**: P1

---

### Candidate #8: Baba Vishu Raut Temple, Pachrasi Dham
- **District**: Madhepura (District ID: 27)
- **Category**: `cultural`
- **Coordinates**: `25.4450, 87.0250`
- **Nearest Active Destination**: Vikramshila Gangetic Dolphin Sanctuary (ID 118 across river in Bhagalpur) at **17.11 km**; Singheshwar Sthan Temple (ID 128 in Madhepura) at **66.72 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>17 km; 300-year-old pastoral folk deity shrine & Rajkiya Mela in southern Madhepura).
- **Tourism Value & Why It Adds Value**:
  - Revered 300-year-old folk pastoral shrine and samadhi sthal dedicated to Baba Vishu Raut, an 18th-century cowherd hero who sacrificed his life protecting communal cattle herds from wild predators.
  - Features an extraordinary living cultural tradition where tens of thousands of pastoralists and dairy farmers converge to pour thousands of liters of unboiled milk over the sacred memorial in a perpetual milky stream.
  - Hosts an annual official 4-day Rajkiya Mela every April (Chaitra Sankranti) drawing over 500,000 visitors, complete with traditional wrestling bouts (dangal), folk music, and rural craft markets.
  - Gives Madhepura its 2nd active destination, introducing authentic pastoral folklore culture 66 km south of Singheshwar Sthan.
- **Primary Source**: District Administration Madhepura (NIC Portal) — https://madhepura.nic.in/tourist-place/baba-vishu-raut/
- **Secondary Source**: Bihar Tourism (Department of Tourism, Govt of Bihar) — https://tourism.bihar.gov.in/en/destinations
- **Confidence**: Grade A | **Priority**: P1

---

### Candidate #9: Kanhaiya Ji Mandir, Bandarjhula
- **District**: Kishanganj (District ID: 25)
- **Category**: `historical`
- **Coordinates**: `26.3683, 87.9636`
- **Nearest Active Destination**: Kishanganj Tea Gardens (ID 126) at **18.34 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>18 km; ASI Centrally Protected 8th-9th century black basalt Vishnu idol & border archaeological mound).
- **Tourism Value & Why It Adds Value**:
  - Centrally Protected Monument under the Archaeological Survey of India (Patna Circle), representing one of the rare protected sculptural heritage monuments in northeastern Bihar.
  - Preserves an exquisite 8th–9th century monolithic black basalt stone statue of Lord Vishnu/Krishna (locally revered as Kanhaiya Ji) discovered during the excavation of ancient brick mounds near the Indo-Nepal border.
  - Site contains ancient structural brick platforms, carved stone pedestals, and mounds associated with pre-medieval trans-Himalayan trade routes.
  - Empowers Kishanganj from a single-destination district (previously only Kishanganj Tea Gardens) into a multi-destination district, adding an ASI national monument.
- **Primary Source**: Archaeological Survey of India (Centrally Protected Monument List) — https://asi.nic.in/
- **Secondary Source**: District Administration Kishanganj (NIC Portal) — https://kishanganj.nic.in/
- **Confidence**: Grade A | **Priority**: P1

---

### Candidate #10: Gautam Asthan, Revelganj
- **District**: Saran (District ID: 31)
- **Category**: `cultural`
- **Coordinates**: `25.7812, 84.6712`
- **Nearest Active Destination**: Chirand Archaeological Site (ID 148) at **16.08 km**
- **Collision Check**: Exact Match: NO | Case-Insensitive: NO | Slug Collision: NO | Same-Site: NO
- **Overlap Classification**: Clearly separate destination (>16 km; sacred Ramayana Gautama Maharshi ashram and Ahilya Uddhar ghat on Saryu river).
- **Tourism Value & Why It Adds Value**:
  - Sacred ancient hermitage and pilgrimage site situated on the high bank of the holy Saryu (Ghaghara) River, 8 km west of Chhapra.
  - Revered in Valmiki Ramayana, Puranas, and local tradition as the ashram of Sage Maharshi Gautama and the sacred *Ahilya Uddhar Sthal*, where Goddess Ahilya was redeemed from her stone curse by the touch of Lord Rama's feet.
  - Features the ancient Gautam Rishi Mandir, sacred bathing ghats, parikrama halls, and the vibrant annual Kartik Purnima religious mela attracting pilgrims across Bihar and eastern Uttar Pradesh.
  - Completes Saran's cultural triad: Chirand (Neolithic archaeology), Sonepur (world-famous cattle & cultural fair), and Gautam Asthan (Vedic/Ramayana riverfront hermitage).
- **Primary Source**: District Administration Saran (NIC Portal) — https://saran.nic.in/tourist-place/gautam-asthan/
- **Secondary Source**: Bihar Tourism (Department of Tourism, Govt of Bihar) — https://tourism.bihar.gov.in/en/destinations
- **Confidence**: Grade A | **Priority**: P1

---

## 5. Spatial Discovery Circuit Analysis

Batch 7 significantly enhances five distinct regional tourism discovery circuits across Bihar:

```mermaid
graph TD
  subgraph Circuit 1: Gandhian Satyagraha & Terai Heritage
    A1[Valmiki National Park #17] --> A2[Someshwar Fort #144]
    A2 --> A3[Rampurva Ashokan Pillars #149]
    A3 --> A4["Bhitiharwa Gandhi Ashram (Batch 7)"]
    A4 --> A5[Lauriya Nandangarh #153]
    A5 --> A6[Udaipur Wildlife Sanctuary #162]
  end

  subgraph Circuit 2: Western Ganga & Ramayana Corridor
    B1[Battle of Buxar Memorial #23] --> B2["Ramrekha Ghat (Batch 7)"]
    B2 --> B3[Chausa Battlefield #120]
    B3 --> B4[Zeeradei Siwan #135]
    B4 --> B5["Mehdar Dham Siwan (Batch 7)"]
    B5 --> B6["Gautam Asthan Saran (Batch 7)"]
    B6 --> B7[Chirand Neolithic Site #148]
  end

  subgraph Circuit 3: Central Mithila & Agricultural Science
    C1[Sujani Embroidery Muzaffarpur #168] --> C2["DRPCAU Pusa Heritage (Batch 7)"]
    C2 --> C3[Vidyapati Dham Samastipur #131]
    C3 --> C4[Rajnagar Palace Complex #154]
    C4 --> C5["Raja Bali Ka Garh (Batch 7)"]
    C5 --> C6[Madhubani Art Village #121]
    C6 --> C7["Jaimangla Garh Begusarai (Batch 7)"]
    C7 --> C8[Kanwar Lake #20]
  end

  subgraph Circuit 4: Seemanchal & Kosi Pastoral Corridor
    D1[Kishanganj Tea Gardens #126] --> D2["Bandarjhula Kanhaiya Ji (Batch 7)"]
    D2 --> D3[Kajha Kothi Eco Park Purnia #174]
    D3 --> D4[Singheshwar Sthan Madhepura #128]
    D4 --> D5["Pachrasi Dham Madhepura (Batch 7)"]
  end

  subgraph Circuit 5: Sone River Eco-Engineering & Magadh Corridor
    E1[Makhdum Shah Dargah Arwal #115] --> E2["Aganoor Hydel Project (Batch 7)"]
    E2 --> E3[Daud Khan Fort Aurangabad #152]
    E3 --> E4[Deokund Aurangabad #178]
    E4 --> E5[Umga Sun Temple #159]
  end
```

---

## 6. Hold, Duplicate, and Rejection Audit Breakdown

### 6.1 Candidates on Strict HOLD

| Candidate Name | District | Category | Nearest Active Place | Distance (km) | Audit Verdict | Detailed Rationale & Risk Assessment |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Buddha Relic Stupa, Vaishali** | Vaishali | `historical` | Vaishali - Birthplace of Democracy (ID 10) | 0.93 | **HOLD** | Excavated mud stupa that yielded the authentic casket containing Buddha's corporeal relics (casket now preserved in Patna Museum). Held strictly due to 0.93 km marker proximity to ID 10; Vaishali already gained 2 places in Batch 5 (*Kolhua Ashokan Pillar* and *Baraila Lake*). |
| **Nagi Dam Bird Sanctuary** | Jamui | `nature` | Nakti Dam Bird Sanctuary (ID 67) | 3.10 | **HOLD** | Notified Wildlife Sanctuary and 2024 Ramsar Wetland site, host of Kalrav Bird Festival. Situated 3.10 km from Nakti Dam Bird Sanctuary. Jamui already possesses 11 active destinations (2nd highest statewide); held to prioritize 1-place and 2-place districts. |
| **Brahmeshwar Nath Temple, Brahmpur** | Buxar | `temple` | Veer Kunwar Singh Fort, Jagdishpur (ID 114) | 19.45 | **HOLD** | Ancient west-facing Shiva temple ('Mini Kashi') and cattle fair venue in eastern Buxar (33 km from Buxar town). Strong candidate; held for Batch 8 to keep Batch 7 strictly at 1 candidate per district. |
| **Kauwadol Hill & Colossal Buddha Statue** | Gaya | `historical` | Barabar Caves (ID 2) | 4.10 | **HOLD** | ASI Centrally Protected Monument featuring an 8-foot seated stone Buddha and rock-cut carvings. Located 4.10 km from Barabar Caves. Gaya already has 12 active destinations; held to maintain geographic balance. |
| **Indrasal Cave, Parvati Hill** | Nawada | `historical` | Ghora Katora Lake (ID 146) | 3.40 | **HOLD** | Ancient cave associated with Sakkapanha Sutta. Held due to scholarly debate and coordinate ambiguity between Giriyak Hill in Nalanda and Parvati Hill in Kashichak Nawada; requires fresh field verification. |
| **Sheohar Raj Palace** | Sheohar | `historical` | Baba Bhuwaneshwar Nath Temple (ID 134) | 4.10 | **HOLD** | Former 19th-century zamindari estate residence. Held due to lack of official government/ASI heritage notification on sheohar.nic.in; currently a private/disputed residential property. |
| **Kosi-Bagmati-Gandak Riverfront** | Khagaria | `nature` | Katyayani Asthan (ID 125) | 10.50 | **HOLD** | Generic river confluence area. Held due to lack of formal municipal tourism infrastructure or official listing on khagaria.nic.in. |
| **Ambika Sthan, Aami** | Saran | `temple` | Maner Sharif (ID 8) / Chirand (ID 148) | 10.50 | **HOLD** | Ancient Shaktipeeth and Yajna Kunda mound on the Ganga in Dighwara. High-value candidate held for Batch 8 since Saran is represented by Gautam Asthan in Batch 7. |
| **Dharahara Narasimha Pillar** | Purnia | `historical` | Raniganj Vriksh Vatika (ID 143) | 20.90 | **HOLD** | Ancient stone pillar and mound associated with Narasimha lore. Purnia gained Kajha Kothi in Batch 6; held for further structural documentation. |
| **Bhaluni Dham** | Bhojpur | `temple` | Daud Khan Fort (ID 152) | 20.60 | **HOLD** | Ancient Parvati temple on Bhojpur/Rohtas border; modest regional tourism footprint; held for Batch 8 consideration. |
| **Chankigarh Fort** | West Champaran | `historical` | Lauriya Nandangarh (ID 153) | 13.58 | **HOLD** | Massive 90-foot ancient brick mound in Narkatiaganj block. West Champaran is represented by Bhitiharwa Ashram in Batch 7; held for Batch 8. |
| **Bettiah Raj Palace Complex** | West Champaran | `historical` | Udaipur Wildlife Sanctuary (ID 162) | 6.36 | **HOLD** | Historic 18th-century palace complex of the Bettiah Raj zamindari estate. Complex legal disputes and ongoing court receiver administration; held pending preservation assessment. |

### 6.2 Duplicates & Clustered Subcomponents

| Candidate Name | District | Nearest Active Destination | Distance (km) | Overlap Verdict | Detailed Rationale |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Saptaparni Cave** | Nalanda | Rajgir (Rajagriha) (ID 9) | 1.48 | **DUPLICATE / ALIAS** | Subcomponent of Rajgir hill complex; first Buddhist council cave, already subsumed under active destination ID 9. |
| **Cyclopean Wall of Rajgir** | Nalanda | Rajgir (Rajagriha) (ID 9) | 1.48 | **DUPLICATE / ALIAS** | Ancient 40-km pre-Mauryan cyclopean stone masonry wall surrounding Rajgir; integral perimeter feature of active destination ID 9. |
| **Rajgir Glass Bridge & Nature Safari** | Nalanda | Rajgir (Rajagriha) (ID 9) | 5.58 | **DUPLICATE / ALIAS** | Eco-adventure park and glass skywalk in Jethian valley, 5.58 km from Rajgir; Nalanda already has 5 active destinations. |
| **Papaharini Tank** | Banka | Mandar Hill (ID 21) | 0.42 | **DUPLICATE / ALIAS** | Sacred water tank situated directly at the foothills of Mandar Hill; same-site complex component. |
| **Sujata Stupa & Kuti** | Gaya | Bodh Gaya Archaeological Museum (ID 4) | 1.42 | **DUPLICATE / ALIAS** | Excavated brick stupa across Falgu river, 1.42 km from Bodh Gaya museum / Mahabodhi complex; tightly clustered with existing Gaya inventory. |
| **Ranti Art Village** | Madhubani | Madhubani Art Village (Jitwarpur) (ID 121) | 1.72 | **DUPLICATE / ALIAS** | Mithila painting artisan village 1.72 km from Jitwarpur Art Village; same craft cluster. |
| **Nagarjuni Caves** | Jehanabad | Barabar Caves & Siddheshwar Nath (ID 5) | 1.78 | **DUPLICATE / ALIAS** | Adjacent Maurya-era cave complex 1.78 km from Barabar Caves; part of the canonical Barabar-Nagarjuni archaeological cluster. |

### 6.3 Explicitly Rejected Items

| Candidate Name | District | Category | Rejection Reason |
| :--- | :--- | :--- | :--- |
| **Arwal Bus Stand Commercial Complex** | Arwal | `transit` | Generic transit infrastructure; zero tourism value. |
| **Barauni IOCL Refinery Township** | Begusarai | `industrial` | Active petrochemical industrial complex; restricted entry. |
| **Ara Sadar Hospital** | Bhojpur | `medical` | Municipal healthcare facility; zero tourism value. |
| **Buxar Central Jail** | Buxar | `restricted` | Active correctional security institution; restricted access. |
| **Samastipur Dairy Milk Plant** | Samastipur | `industrial` | Industrial dairy processing facility; commercial property. |
| **Chhapra Main Bazar Cloth Market** | Saran | `commercial` | Local commercial clothing market; generic retail. |
| **Hotel Grand Sheohar** | Sheohar | `commercial` | Commercial hotel lodging; generic business establishment. |
| **Siwan Civil Court Complex** | Siwan | `administrative` | Judicial administrative premises; zero tourism value. |

---

## 7. Database Invariance Verification

A strict automated check of the MySQL database (`hiddenyatra`) confirms:

```sql
SELECT COUNT(*) FROM places WHERE deleted_at IS NULL;
-- Result: 128 (Baseline perfectly preserved)

SELECT MAX(id) FROM places;
-- Result: 178 (Zero new insertions)

SELECT COUNT(DISTINCT district_id) FROM places WHERE deleted_at IS NULL;
-- Result: 38 (38/38 statewide coverage intact)
```

**State**: READ-ONLY. Zero mutations executed.

---

## 8. Summary & Human Approval Protocol

The Batch 7 Candidate Selection Phase is complete. All 10 candidates have been verified against authoritative government, institutional, and archaeological records. Full collision checks have been executed against all 128 active destinations.

**No database writes, insertions, updates, or deletions have been performed.**

BATCH 7 PREVIEW READY — WAITING FOR HUMAN APPROVAL.
