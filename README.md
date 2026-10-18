```
<div align="center">

# 🛡️ AI-CM-DSS
### AI-Enabled Integrated Cybercrime Management & Decision Support System

**For Uttar Pradesh Police**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*An intelligent, AI-powered platform for automated cybercrime complaint handling, investigation support, and bank coordination.*

[Features](#-key-features) • [Architecture](#-system-architecture) • [Installation](#-installation-guide) • [Usage](#-usage-guide) • [Objectives](#-project-objectives) • [Team](#-team)

</div>

---

## 📖 Overview

**AI-CM-DSS** is a comprehensive, AI-powered cybercrime management and decision support system designed specifically for **Uttar Pradesh Police**. The system automates the entire lifecycle of cybercrime complaint handling—from registration and classification to investigation support, transaction blocking, and fund reversal coordination.

The system leverages **Natural Language Processing (NLP)** and **Machine Learning (Logistic Regression)** to automatically classify complaints into five major cybercrime categories, generate category-specific Standard Operating Procedures (SOPs), calculate risk scores, and provide decision support for investigating officers.

---

## 🎯 Project Objectives

| # | Objective | Status |
|---|-----------|--------|
| **1** | **Automated First-Level Cybercrime Categorization** – Automatically classify complaints into 5 crime categories with confidence scores within seconds | ✅ Achieved |
| **2** | **Category-Wise Investigation SOPs** – Generate structured SOPs with legal sections, investigation steps, and required documentation | ✅ Achieved |
| **3** | **AI-Assisted Transaction Blocking** – Identify financial fraud cases eligible for urgent transaction blocking and generate freeze request documents | ✅ Achieved |
| **4** | **Fund Reversal Support** – Provide AI-generated case summaries, transaction timelines, RBI compliance status, and reversal progress tracking | ✅ Achieved |

---

## ✨ Key Features

### 🤖 AI & Machine Learning
- **Auto Classification** – NLP + Logistic Regression classifies complaints into 5 categories
- **Confidence Scores** – Transparent AI predictions with probability percentages
- **Risk Scoring** – Dynamic risk calculation based on amount, severity, and confidence
- **TF-IDF Vectorization** – Advanced text feature extraction

### 📋 Investigation Support
- **Category-wise SOPs** – Step-by-step investigation workflow for each crime type
- **Legal Sections** – Auto-suggested IPC and IT Act sections
- **Documentation Checklist** – Required evidence and documents per category
- **Inter-agency Coordination** – Required authorities and external bodies

### ❄️ Transaction Blocking
- **Freeze Request Generation** – Formal bank coordination documents
- **Priority Scoring** – Automated priority based on amount and risk
- **Request Tracking** – Status monitoring (Pending/Approved/Completed)
- **PDF Export** – Professional freeze request letters

### 🔄 Fund Reversal Support
- **AI Case Summary** – Auto-generated 2-3 line complaint summary
- **Transaction Timeline** – Chronological event tracking
- **RBI Deadline Compliance** – COMPLIANT / URGENT / CRITICAL status
- **Reversal Tracker** – Step-by-step progress monitoring
- **Bank Letter Generator** – Formal reversal coordination letters

### 🔒 Security & Access Control
- **Role-Based Access Control** – 6 hierarchical roles (Admin, SP, CCI, IO, AIO, Viewer)
- **Audit Logging** – Complete trail of all user actions
- **Password Hashing** – Secure credential storage
- **Session Management** – Secure login/logout

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│         HTML • CSS • JavaScript • Jinja2 Templates           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│              Flask Routes • Blueprints • Sessions            │
│    Complaint Routes │ AI Routes │ FIR Routes │ Admin Routes  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       AI LAYER                               │
│    NLP Preprocessing → TF-IDF Vectorization → LR Model      │
│    Classification → Risk Scoring → SOP Generation            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                           │
│                        MongoDB                               │
│   users │ complaints │ predictions │ freeze_requests │ logs  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
cybercrime_project/
│
├── app.py                          # Main Flask application entry point
├── requirements.txt                # Python dependencies
├── config.py                       # Configuration settings
├── .env                            # Environment variables
│
├── models/                         # ML Models
│   ├── lr_model.pkl                # Trained Logistic Regression model
│   └── tfidf_vectorizer.pkl        # TF-IDF vectorizer
│
├── routes/                         # Flask Blueprints
│   ├── auth_routes.py              # Authentication
│   ├── complaint_routes.py         # Complaint management
│   ├── ai_routes.py                # AI classification
│   ├── fir_routes.py               # FIR generation
│   ├── assignment_routes.py        # Case assignment
│   ├── dashboard_routes.py         # Dashboard
│   └── admin_routes.py             # Admin panel
│
├── templates/                      # Jinja2 Templates
│   ├── base.html                   # Base layout
│   ├── auth/                       # Login/register
│   ├── complaints/                 # Complaint views
│   ├── ai/                         # AI results
│   ├── fir/                        # FIR templates
│   └── admin/                      # Admin pages
│
├── static/                         # Static Assets
│   ├── css/
│   │   └── style.css               # Main stylesheet
│   ├── js/
│   │   └── script.js               # JavaScript
│   ├── sops.json                   # Category-wise SOP database
│   └── images/                     # Logo and assets
│
├── utils/                          # Utility Functions
│   ├── ml_utils.py                 # ML helpers
│   ├── pdf_generator.py            # PDF generation
│   ├── risk_calculator.py          # Risk scoring
│   └── validators.py               # Input validation
│
├── uploads/                        # Uploaded evidence files
├── logs/                           # Application logs
└── README.md                       # This file
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface |
| **Template Engine** | Jinja2 | Server-side rendering |
| **Backend** | Python 3.10+, Flask 2.3+ | Web framework |
| **Database** | MongoDB 6.0+ | NoSQL data storage |
| **ML Library** | Scikit-learn | Classification models |
| **NLP** | TF-IDF Vectorizer | Text feature extraction |
| **PDF Generation** | ReportLab | Freeze/Reversal letters |
| **Authentication** | Flask-Login, bcrypt | Secure sessions |

---

## 🚀 Installation Guide

### Prerequisites

Ensure you have the following installed:

- **Python 3.10+** – [Download](https://python.org/downloads/)
- **MongoDB 6.0+** – [Download](https://mongodb.com/try/download/community)
- **Git** – [Download](https://git-scm.com/)
- **Web Browser** – Chrome, Firefox, or Edge

### Step 1: Clone the Repository

```bash
git clone https://github.com/shamyt9/Software-Exhibition-2026---Lakshya-Forum.git
cd Software-Exhibition-2026---Lakshya-Forum
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/cybercrime_dss
DB_NAME=cybercrime_dss
UPLOAD_FOLDER=uploads
```

### Step 5: Start MongoDB

```bash
# Windows (as service)
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
# OR
mongod
```

### Step 6: Train ML Model

```bash
python train_model.py
```

### Step 7: Initialize Database

```bash
python database_setup.py
```

### Step 8: Run the Application

```bash
python app.py
```

### Step 9: Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

### Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **IO** | `io_lucknow` | `io123` |
| **SP** | `sp_lucknow` | `sp123` |
| **CCI** | `cci_lucknow` | `cci123` |
| **AIO** | `aio_lucknow` | `aio123` |

> ⚠️ **Important:** Change all default passwords immediately after first login in production.

---

## 📖 Usage Guide

### For Admin
1. Login with admin credentials
2. Manage users, districts, and system configuration
3. Configure risk weights and SOP templates
4. View audit logs and generate reports

### For AIO (Assistant IO)
1. Login and navigate to "Register Complaint"
2. Enter complainant details and complaint description
3. AI automatically classifies and assesses risk
4. Upload evidence if available

### For CCI (Cyber Cell Incharge)
1. Login and view unassigned cases
2. Assign cases to Investigating Officers
3. Review investigation progress
4. Approve FIR drafts

### For IO (Investigating Officer)
1. Login and view assigned cases
2. Follow category-specific SOP checklist
3. Generate freeze requests for financial frauds
4. Track fund reversal progress
5. File FIR and update case status

### For SP (Superintendent of Police)
1. Login to view district dashboard
2. Monitor high-risk cases
3. Approve high-value freeze requests
4. Review district analytics

---

## 🔬 AI Model Details

### Classification Categories

| Category | Description | Example Keywords |
|----------|-------------|------------------|
| **Financial Fraud** | UPI scams, phishing, credit card fraud | UPI, OTP, bank, transaction |
| **Digital Arrest** | Fake CBI/Police calls | CBI, arrest, warrant, video call |
| **Fake News** | WhatsApp rumors, misinformation | viral, forward, fake, rumor |
| **Darknet** | Illegal marketplace, cryptocurrency | dark web, bitcoin, Tor |
| **Identity Theft** | Aadhaar/PAN misuse, fake profiles | Aadhaar, PAN, fake profile, impersonation |

### Model Performance

| Metric | Value |
|--------|-------|
| **Algorithm** | Logistic Regression |
| **Feature Extraction** | TF-IDF (5000 features) |
| **Training Samples** | 500+ synthetic complaints |
| **Accuracy** | ~90% |
| **Training Time** | < 30 seconds |
| **Prediction Time** | < 1 second |

### Risk Scoring Formula

```
Risk Score = (AI Confidence × 10) + (Amount Band × 2) + Category Severity

Where:
- Amount Band: 0 (< ₹10k), 1 (₹10k-50k), 2 (₹50k-1L), 3 (> ₹1L)
- Category Severity: Fake News (1) → Darknet (5)

Risk Levels:
- HIGH: Score ≥ 80
- MEDIUM: Score 50-79
- LOW: Score < 50
```

---

## 🧪 Testing

### Test Case 1: Financial Fraud
```
Input: "Mere SBI account se 1,45,000 rupees gayab ho gaye. 
OTP share karne ke baad fraud hua. Transaction ID: SBITXN20260516784523"

Expected: Cyber Financial Fraud | Risk: HIGH | Freeze request eligible
```

### Test Case 2: Digital Arrest
```
Input: "CBI officer ne call kiya, digital arrest warrant dikhaya, 
3 lakh maange. Video call pe police station background tha."

Expected: Digital Arrest Scam | Risk: HIGH | Legal: 66D IT Act, 384 IPC
```

### Test Case 3: Fake News
```
Input: "WhatsApp par message viral hai ki kal se petrol 200 rupees hoga. 
PIB fact check mein fake nikla. 100+ groups mein share ho chuka hai."

Expected: Fake News | Risk: MEDIUM | Legal: 505 IPC, 66A IT Act
```

---

## 🔒 Security Features

- ✅ **Role-Based Access Control (RBAC)** – 6 hierarchical roles
- ✅ **Password Hashing** – bcrypt with salt
- ✅ **Session Management** – Secure cookie-based sessions
- ✅ **Audit Logging** – All user actions logged with IP and timestamp
- ✅ **Input Validation** – SQL injection and XSS protection
- ✅ **CSRF Protection** – Form tokens
- ✅ **District-level Access** – IOs only see their district cases
- ✅ **Emergency Access** – Admin override with audit trail

---

## 📊 Database Collections

| Collection | Purpose |
|-----------|---------|
| `users` | All user accounts with roles |
| `complaints` | Cybercrime complaint records |
| `predictions` | AI classification results |
| `freeze_requests` | Transaction freeze requests |
| `fir_records` | FIR documents |
| `audit_logs` | Complete audit trail |
| `districts` | District master data |
| `sops` | Category-wise SOP templates |

---

## 🎯 Scope & Scalability

### Current Scope
- **Pilot deployment** for Uttar Pradesh Police
- Covers **5 major cybercrime categories**
- Focuses on **financial fraud investigation**

### Future Scope
- 🚀 **Multi-state deployment** – Configurable for any Indian state
- 🌐 **Multilingual support** – Hindi, Hinglish, regional languages
- 🤖 **Advanced AI** – BERT/Transformer models for better accuracy
- 📱 **Mobile application** – Citizen complaint filing app
- 🔗 **Bank API integration** – Live transaction blocking
- 📞 **WhatsApp bot** – Easy complaint registration
- 🎙️ **Voice-based complaints** – For rural users


---



---

<div align="center">

### ⭐ If you find this project useful, please give it a star!

**Made with ❤️ for a Safer Digital India**

</div>
```

---
