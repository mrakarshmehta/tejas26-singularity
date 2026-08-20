# 💎 HiddenYatra — Discover Bihar's Untold Wonders

> **National Hackathon Flagship Submission**  
> *An AI-Powered, Hyper-Local Tourism Platform & Smart Itinerary Engine for Bihar*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/Tests-101%2F101%20Passing-brightgreen?style=for-the-badge)](#testing--verification)

---

## 🌟 Pitch Statement

**HiddenYatra** bridges the digital gap for offbeat tourism in Bihar. While popular destinations like Bodh Gaya and Rajgir draw international visitors, hundreds of ancient ruins, cascading waterfalls, pristine lakes, and sacred temples remain unexplored due to fragmented information.

HiddenYatra is a **production-ready, AI-driven, hyper-local tourism ecosystem** designed to promote sustainable eco-tourism, empower local communities, and provide travelers with personalized, budget-aware multi-day itineraries in seconds.

---

## 🔥 Key Features

### 🤖 1. AI Trip Planner & Smart Itinerary Engine
- **Intelligent Itinerary Generation**: Generates 1, 2, 3, or 5-day itineraries using Haversine geographic distance clustering.
- **Persona-Aware Modes**: Tailored travel flows for **Solo Explorers 👤**, **Couple Getaways 👩‍❤️‍👨**, and **Family Trips 👨‍👩‍👧‍👦**.
- **Dynamic Budget Estimator**: Calculates accurate package cost breakdowns for Transport, Food, Accommodations, and Entry Fees across Budget, Standard, and Luxury tiers.
- **Local Food & Hotel Integration**: Recommends authentic district-specific delicacies (e.g., Litti Chokha, Khaja, Anarsa) and verified stays.
- **PDF Export & Print**: One-click print-optimized PDF generation for offline travel.

### 🔍 2. Natural Language Search & Smart Filtering
- Instant autocomplete with district and category badges (`/api/autocomplete`).
- Intent detection search (`/api/smart-search`) supporting queries like *"waterfalls near Rohtas under ₹2000"*.
- Multi-dimensional filters: Category (Temples, Forts, Waterfalls, Nature, Hidden Gems), Budget Tier, Best Season, and Distance.

### 🗺️ 4. Interactive Map & District Explorer
- Interactive Bihar map with district pins and place clusters (`/explore`).
- District-level landing pages with historical context, famous foods, nearby facilities, and travel guidelines (`/district/<slug>`).

### 🛡️ 5. Enterprise-Grade Admin Control Center (11 Modules)
- **Dashboard Analytics**: Live statistics for total places, pending user submissions, active users, and visitor reviews.
- **Content Management**: Complete CRUD for Places, Districts, Hero Media, Featured Trending Spots, and Nearby Services.
- **Moderation Engine**: Approve/Reject community place submissions (`/admin/submissions`), merge duplicate entries, and audit user-submitted photos (`/admin/user-photos`).
- **Recycle Bin & Audit Logs**: Soft delete protection with restore/permanent delete capabilities and detailed admin action history.

---

## 🏗️ Architecture & Tech Stack

```
HiddenYatra Platform Architecture
 ├── Presentation Layer (Jinja2, Modern Vanilla CSS, Custom Components, PWA)
 ├── Application Layer (Flask 3.0 Blueprint Architecture)
 │    ├── main_bp (Homepage, Search, State, Districts)
 │    ├── places_bp (Place detail, Facilities, Nearby)
 │    ├── itinerary_bp (AI Trip Planner Engine)
 │    ├── api_bp (Autocomplete, Smart Search, Yatra AI Chat)
 │    ├── auth_bp (Login, Signup, OTP Verification, Password Reset)
 │    ├── admin_bp (16 Moderation & Management Views)
 │    ├── reviews_bp (Ratings & Review Moderation)
 │    ├── wishlist_bp (Personal Saved Destinations)
 │    └── community_bp (User Place Submissions & My Contributions)
 └── Data Layer (MySQL 8.0, DBUtils Connection Pool, Thread-Safe Singleton)
```

| Component | Technology |
|:---|:---|
| **Backend Framework** | Flask 3.0+ (Python 3.11+) |
| **Database** | MySQL 8.0 / MariaDB (DBUtils Connection Pooling) |
| **Frontend** | HTML5, Vanilla CSS3 (Design Tokens, Glassmorphism, Responsive CSS Grid), Vanilla JS |
| **Security** | CSRF Protection (`markupsafe`), Password Hashing (`werkzeug`), Magic Byte File Validation, Rate Limiting |
| **Testing** | `unittest` (87 tests), Custom E2E Route Verification (40 checks) |
| **Deployment** | Docker, Gunicorn, Nginx, Render / AWS EC2 Ready |

---

## ⚡ Quick Start & Installation

### Prerequisites
- Python 3.11+
- MySQL 8.0+ or MariaDB
- Git

### 1. Clone & Setup Environment
```bash
git clone https://github.com/user/HiddenYatra.git
cd HiddenYatra

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# On Windows PowerShell:
Copy-Item .env.example .env
# On Command Prompt / Bash:
cp .env.example .env
```
Edit `.env` with your local MySQL credentials:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=hiddenyatra
DB_USER=root
DB_PASSWORD=your_local_mysql_password
```

### 3. Initialize Database & Seed Development Data
Run the automated environment setup script:
```bash
python scripts/setup_dev_environment.py
```
This script automatically:
1. Connects to your local MySQL server.
2. Creates the `hiddenyatra` database if missing.
3. Executes `mysql_schema.sql` to build all 34 tables.
4. Seeds all 38 Bihar districts, sample tourist destinations, homestay listings, and demo user accounts.

### 4. Start Development Server
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🔐 Credentials for Local Development & Testing

| Account Role | Username | Password | Purpose |
|:---|:---|:---|:---|
| **Administrator** | `admin` | `admin123` | Access `/admin/login` & full admin dashboard |
| **Local Host** | `demo_host` | `password123` | Host Homestay & Free Stay management (`/host/dashboard`) |
| **Traveler** | `demo_traveler` | `password123` | Normal traveler account for testing bookings & reviews |

---

## 🧪 Testing & Verification

HiddenYatra includes a complete automated testing suite:

```bash
# 1. Python Syntax & Compilation Check
python -m py_compile app.py models/database.py routes/*.py

# 2. Run All 87 Unit Tests
python -m unittest discover tests

# 3. Run E2E Route Verification Suite (40 Routes)
python e2e_verify.py
```

---

## 📜 License & Acknowledgments

Built with ❤️ for Bihar Tourism & Eco-Exploration.  
Released under the [MIT License](LICENSE).
