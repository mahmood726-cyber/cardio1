# Complete Guide to Accessing REAL Cardiology Data

This guide explains how to access and download REAL cardiology research data from authoritative sources. All data sources listed here provide actual clinical trial data, patient records, or published research.

## 🔴 LIVE DATABASE ACCESS (Real-Time Data)

### 1. AACT Database - ALL ClinicalTrials.gov Data

**What it is:** Complete database of ALL 400,000+ clinical trials registered worldwide
**Data Type:** REAL clinical trial data, updated DAILY
**Cost:** FREE

**How to Access:**

```bash
# Step 1: Register (takes 2 minutes)
# Go to: https://aact.ctti-clinicaltrials.org/users/sign_up
# You'll receive database credentials via email immediately

# Step 2: Install Python connector
pip install psycopg2-binary pandas

# Step 3: Connect and query
from scripts.collection.aact_connector import AACTConnector

connector = AACTConnector(
    user='your_username_from_email',
    password='your_password_from_email'
)

connector.connect()

# Query cardiology trials
cardio_trials = connector.query_cardiology_trials(
    conditions=['heart failure', 'myocardial infarction'],
    min_enrollment=100,
    start_year=2000
)

print(f"Retrieved {len(cardio_trials)} REAL trials")

# Get trials with actual mortality data
trials_with_results = connector.query_trials_with_results(
    conditions=['heart failure'],
    min_enrollment=200
)

connector.disconnect()
```

**What You Get:**
- 400,000+ real clinical trials
- Trial protocols, interventions, eligibility criteria
- Posted results (when available)
- Baseline characteristics
- Outcome measurements
- Adverse events
- Updated daily from ClinicalTrials.gov

---

### 2. PubMed E-utilities API - ALL Medical Literature

**What it is:** Complete PubMed database (36+ million articles)
**Data Type:** REAL published research, updated DAILY
**Cost:** FREE (register for API key for higher limits)

**How to Access:**

```bash
# Step 1: Get API key (optional but recommended)
# Go to: https://www.ncbi.nlm.nih.gov/account/
# Create account → Settings → API Key Management

# Step 2: Use PubMed collector
from scripts.collection.pubmed_collector import PubMedCollector

collector = PubMedCollector(
    email='your.email@example.com',  # Required
    api_key='your_api_key'            # Optional, increases rate limit
)

# Search for cardiology RCTs
pmids = collector.search_cardiology(
    start_year=2010,
    end_year=2025,
    study_types=['Randomized Controlled Trial', 'Meta-Analysis'],
    max_results=5000
)

# Fetch full article details
articles = collector.fetch_details(pmids)

# Save to file
collector.save_to_json(articles, 'data/raw/pubmed/cardiology_rcts.json')
```

**What You Get:**
- 36+ million biomedical articles
- Abstracts, authors, citations
- MeSH terms, keywords
- Publication types
- DOIs, PMIDs for tracking

---

## 📦 BULK DATA DOWNLOADS (Complete Datasets)

### 3. AACT Monthly Snapshots

**Download Complete Database:**

```bash
# Option A: Via website
# 1. Go to: https://aact.ctti-clinicaltrials.org/snapshots
# 2. Download latest snapshot (~5 GB compressed)
# 3. Extract and restore to local PostgreSQL:

createdb aact
pg_restore -d aact aact_snapshot.dmp

# Option B: Via command line
wget https://aact.ctti-clinicaltrials.org/static/static_db_copies/daily/20251121_clinical_trials.zip
unzip 20251121_clinical_trials.zip
pg_restore -d aact daily_snapshot.dmp
```

---

### 4. PubMed Baseline Files

**Download Complete PubMed:**

```bash
# WARNING: 200+ GB total
# Visit: https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/

# Download all files
wget -r -np -nd ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed*.xml.gz

# OR download specific files
wget ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed25n0001.xml.gz

# Uncompress
gunzip pubmed*.xml.gz

# Parse using BioPython (see pubmed_collector.py)
```

---

### 5. Kaggle Cardiovascular Disease Dataset

**REAL DATA:** 70,000 patient records from medical examinations

```bash
# Method 1: Kaggle API
pip install kaggle

# Get API token from https://www.kaggle.com/account
# Save to ~/.kaggle/kaggle.json

kaggle datasets download -d sulianova/cardiovascular-disease-dataset
unzip cardiovascular-disease-dataset.zip -d data/raw/kaggle/

# Method 2: Manual download
# Go to: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset
# Click "Download" (requires free Kaggle account)
```

**Data Includes:**
- 70,000 patients
- Age, gender, height, weight
- Blood pressure (systolic/diastolic)
- Cholesterol levels
- Glucose levels
- Smoking, alcohol intake
- Physical activity
- CVD presence (outcome)

---

### 6. UCI Heart Disease Dataset

**REAL DATA:** Multi-institutional heart disease data

```bash
# Automated download (included in project)
python scripts/collection/bulk_data_downloader.py

# Manual download
# Cleveland: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data
# Hungary: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.hungarian.data
# Switzerland: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.switzerland.data
# Long Beach VA: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.va.data
```

**Data Includes:**
- 1000+ patients from 4 institutions
- 76 attributes per patient
- Angiographic disease status
- Clinical measurements
- ECG results

---

### 7. MIMIC-III/IV Critical Care Database

**REAL DATA:** 40,000+ ICU patients with comprehensive data

**Access Requirements:**
1. Complete CITI "Data or Specimens Only Research" course
2. Register at PhysioNet: https://mimic.mit.edu/docs/gettingstarted/
3. Sign data use agreement
4. Approval typically takes 24-48 hours

**Download:**

```bash
# After approval, download via PhysioNet
wget -r -N -c -np --user YOUR_USERNAME --ask-password \
    https://physionet.org/files/mimiciii/1.4/
```

**Data Includes:**
- Demographics
- Vital signs (high resolution)
- Laboratory tests
- Medications
- Procedures
- ICD codes
- ECG waveforms
- Mortality outcomes

**Cardiovascular Subset:**
- Cardiac ICU admissions
- Post-cardiac surgery
- Acute MI
- Heart failure exacerbations
- Arrhythmias

---

### 8. Cochrane Database of Systematic Reviews

**REAL DATA:** High-quality systematic reviews with extracted data

**Access:**

```bash
# Method 1: National provision (FREE in many countries)
# Check if your country has free access: https://www.cochranelibrary.com/

# Method 2: Institutional subscription
# Check if your institution subscribes

# Method 3: Individual review purchase
# Pay-per-view for specific reviews
```

**Cardiac-Specific Reviews:**
- Cardiac rehabilitation (148+ RCTs)
- Heart failure interventions
- Coronary revascularization
- Hypertension management
- Arrhythmia treatments

**Data Available:**
- Characteristics of studies tables
- Risk of bias assessments
- Extracted outcome data
- Forest plots
- Summary of findings tables

---

## 🏥 REAL-WORLD CLINICAL DATA

### 9. UK Biobank (Research Access)

**REAL DATA:** 500,000+ participants with genetic, imaging, and health data

**Access:** https://www.ukbiobank.ac.uk/enable-your-research/apply-for-access

**Requirements:**
- Research proposal
- Ethics approval
- Institution affiliation
- ~£6,000 GBP application fee

---

### 10. All of Us Research Program (USA)

**REAL DATA:** 1+ million US participants

**Access:** https://www.researchallofus.org/

**Requirements:**
- Register as researcher
- Complete training
- Data use agreement

---

## 📊 USING REAL DATA IN THIS PROJECT

Once you have downloaded real data, process it using our pipelines:

### Step 1: Download Data

```bash
# Example: AACT database
python scripts/collection/aact_connector.py

# Or: PubMed data
python scripts/collection/pubmed_collector.py \
    --email your@email.com \
    --api-key YOUR_KEY

# Or: Kaggle data
kaggle datasets download -d sulianova/cardiovascular-disease-dataset
```

### Step 2: Process Data

```bash
# Standardize format
python scripts/processing/data_processor.py \
    --input data/raw/clinicaltrials/trials.json \
    --output data/processed/standardized_trials.csv
```

### Step 3: Run Advanced Meta-Analysis

```bash
# Run analysis with failure detection
python scripts/analysis/test_real_data.py
```

### Step 4: Generate Reports

```bash
# Create comprehensive report
python scripts/analysis/generate_report.py \
    --data data/processed/standardized_trials.csv \
    --output reports/meta_analysis_report.html
```

---

## 📈 DATA COMPLETENESS COMPARISON

| Data Source | Size | Completeness | Update Frequency | Cost |
|-------------|------|--------------|------------------|------|
| AACT | 400K+ trials | High | Daily | FREE |
| PubMed | 36M+ articles | Medium | Daily | FREE |
| Kaggle CVD | 70K patients | High | Static | FREE |
| MIMIC | 40K+ ICU patients | Very High | Annual | FREE* |
| UK Biobank | 500K+ participants | Very High | Ongoing | $$$ |
| Cochrane | 10K+ reviews | High | Monthly | FREE** |

\* Free after approval
** Free in many countries

---

## 🔐 IMPORTANT: DATA ETHICS

When using REAL patient data:

1. **Privacy:** All patient data must be de-identified
2. **Ethics:** Follow IRB guidelines
3. **Data Use Agreements:** Respect terms of use
4. **Attribution:** Cite data sources properly
5. **Transparency:** Report data sources in publications

---

## 🚀 QUICK START FOR REAL DATA COLLECTION

**Easiest Path (No Registration):**

```bash
# 1. Download Kaggle dataset (70K patients)
kaggle datasets download -d sulianova/cardiovascular-disease-dataset

# 2. Run meta-analysis on included real trials
python scripts/analysis/test_real_data.py
```

**Best Path (Maximum Real Data):**

```bash
# 1. Register for AACT (2 minutes)
# Visit: https://aact.ctti-clinicaltrials.org/users/sign_up

# 2. Get NCBI API key (2 minutes)
# Visit: https://www.ncbi.nlm.nih.gov/account/

# 3. Collect data
python scripts/main_pipeline.py \
    --email your@email.com \
    --api-key YOUR_NCBI_KEY

# 4. Connect to AACT
python scripts/collection/aact_connector.py

# 5. Run advanced meta-analysis
python scripts/analysis/test_real_data.py
```

---

## 📞 SUPPORT

- **AACT Support:** aact@duke.edu
- **PubMed Support:** https://support.nlm.nih.gov/
- **MIMIC Support:** https://mimic.mit.edu/about/contact/
- **This Project:** Open an issue on GitHub

---

## 📝 SUMMARY

**You now have access to:**
- 400,000+ clinical trials (AACT)
- 36M+ research articles (PubMed)
- 70,000+ patient records (Kaggle)
- 40,000+ ICU patients (MIMIC)
- 500,000+ UK participants (UK Biobank)
- Systematic reviews (Cochrane)

**All REAL data. No simulations. Ready for rigorous meta-analysis.**

Last updated: 2025-11-21
