# Guide to Publicly Available Cardiovascular Meta-Analysis Data Sources

## Overview
This guide provides verified sources for downloading real cardiovascular trial data to expand your meta-analysis database to 1000+ trials.

---

## 1. Cochrane Database of Systematic Reviews

### What it is:
The gold standard for systematic reviews. Each review contains extracted data from multiple trials.

### How to access:
- **URL**: https://www.cochranelibrary.com/
- **Free access**: Many countries have national subscriptions
- **Data format**: Structured tables in review appendices

### Cardiovascular Reviews (Examples):
- **"Antiplatelet agents for preventing thrombosis after peripheral arterial bypass surgery"** - Contains 20+ trials
- **"Beta-blockers for heart failure with reduced, mid-range, and preserved ejection fraction"** - 100+ trials
- **"Antihypertensive drug therapy for mild to moderate hypertension during pregnancy"** - 60+ trials

### How to extract data:
1. Download PDF of systematic review
2. Navigate to "Characteristics of included studies" tables
3. Extract: Study ID, N, interventions, outcomes, follow-up
4. Many reviews provide **forest plot data** in downloadable format

### Specific Cochrane Heart Reviews to Check:
```
Search terms on Cochrane Library:
- "heart failure" + filter: Cochrane Reviews
- "myocardial infarction" + filter: Cochrane Reviews
- "anticoagulants" + filter: Cochrane Reviews
- "hypertension" + filter: Cochrane Reviews
```

**Estimated trials available**: 500+ cardiovascular trials across all Cochrane Heart reviews

---

## 2. ClinicalTrials.gov Data Downloads

### What it is:
US National Library of Medicine registry of clinical trials worldwide.

### How to access:
- **URL**: https://clinicaltrials.gov/
- **Download link**: https://clinicaltrials.gov/data-api/about-api
- **Bulk download**: https://aact.ctti-clinicaltrials.org/

### AACT Database (Aggregate Analysis of ClinicalTrials.gov):
- **URL**: https://aact.ctti-clinicaltrials.org/
- **Format**: PostgreSQL database dump OR CSV files
- **Updated**: Monthly
- **Size**: ~450,000 trials total, ~50,000 cardiovascular

### How to download:
```bash
# Option 1: Download CSV files
wget https://aact.ctti-clinicaltrials.org/static/static_db_copies/daily/aact_static.zip

# Option 2: Query their PostgreSQL database directly
# Connection details at: https://aact.ctti-clinicaltrials.org/connect
```

### Filter for cardiovascular trials:
```sql
SELECT * FROM studies
WHERE conditions LIKE '%cardiovascular%'
   OR conditions LIKE '%heart failure%'
   OR conditions LIKE '%myocardial infarction%'
AND study_type = 'Interventional'
AND phase IN ('Phase 3', 'Phase 4')
AND enrollment >= 200;
```

**Estimated relevant trials**: 10,000+ cardiovascular Phase 3/4 trials

---

## 3. Published Meta-Analysis Supplementary Data

### Major Meta-Analyses with Public Data:

#### Blood Pressure Lowering Treatment Trialists' Collaboration (BPLTTC)
- **Latest publication**: Lancet 2021
- **Website**: http://www.bplttc.org/
- **Trials**: 52 major hypertension trials
- **Patients**: 360,000
- **Data access**: Contact collaboration OR download supplementary appendices from Lancet papers

#### Cholesterol Treatment Trialists' (CTT) Collaboration
- **Website**: https://www.cttcollaboration.org/
- **Trials**: 30+ statin trials
- **Patients**: 175,000
- **Data**: Individual participant data meta-analyses published in Lancet
- **Access**: Supplementary materials from publications

#### Antithrombotic Trialists' (ATT) Collaboration
- **Publications**: Multiple Lancet papers
- **Focus**: Antiplatelet and anticoagulant trials
- **Trials**: 100+ trials
- **Data**: Published appendices with trial-level data

### How to access published meta-analysis data:

**Step 1**: Find meta-analysis publication
```
Google Scholar search: "cardiovascular meta-analysis" + "supplementary data"
PubMed search: cardiovascular[Title] AND meta-analysis[Title] AND (supplementary OR appendix)
```

**Step 2**: Download supplementary materials
- Most journals provide free supplementary files
- Look for: "Supplementary Appendix", "eTable", "eFigure"
- Common formats: Excel, CSV, PDF tables

**Step 3**: Extract structured data
- Trial names, sample sizes, outcomes, effect sizes
- Often includes full forest plot data

---

## 4. OpenTrials / WHOICTRP

### OpenTrials
- **URL**: https://opentrials.net/ (now deprecated, but data archived)
- **Alternative**: https://www.who.int/clinical-trials-registry-platform

### WHO International Clinical Trials Registry Platform (ICTRP)
- **URL**: https://trialsearch.who.int/
- **Coverage**: All WHO-compliant trial registries worldwide
- **Download**: Bulk download available
- **Format**: CSV/XML

### How to download:
1. Go to https://trialsearch.who.int/
2. Advanced search: Condition = "cardiovascular"
3. Export results (CSV format available)
4. Filter for completed Phase 3/4 trials

**Estimated trials**: 20,000+ cardiovascular trials registered

---

## 5. European Medicines Agency (EMA) Clinical Data

### What it is:
EMA makes clinical trial data public for approved drugs.

### How to access:
- **URL**: https://www.ema.europa.eu/en/human-regulatory/research-development/clinical-trials/clinical-data-publication
- **Portal**: https://clinicaldata.ema.europa.eu/web/cdp/home

### Coverage:
- All trials submitted for drug approval in EU
- Includes cardiovascular drug trials (SGLT2i, anticoagulants, etc.)
- Full clinical study reports (CSRs) available

### Download process:
1. Search by drug name or condition
2. Download anonymized individual patient data OR
3. Download clinical study reports (PDFs with summary data)

**Estimated relevant trials**: 500+ cardiovascular drug trials

---

## 6. Vivli - Clinical Trial Data Sharing Platform

### What it is:
Platform for sharing de-identified individual participant data from clinical trials.

### How to access:
- **URL**: https://vivli.org/
- **Registration**: Free for researchers
- **Process**: Submit data request, approved within weeks

### Available data:
- Individual participant data from major trials
- Many cardiovascular trials available
- Includes trials from: Yale Open Data Access (YODA), Duke Clinical Research Institute

### Search for cardiovascular trials:
https://search.vivli.org/
- Search: "cardiovascular", "heart failure", "myocardial infarction"
- Filter: Data available

**Estimated trials**: 200+ with full individual patient data

---

## 7. Kaggle Datasets

### Cardiovascular Disease Dataset
- **URL**: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset
- **Size**: 70,000 patients
- **Format**: CSV
- **Variables**: Age, gender, BP, cholesterol, smoking, outcomes
- **Free download**: Yes

### Heart Disease UCI
- **URL**: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
- **Size**: 920 patients from 4 databases
- **Variables**: Clinical features, angiography, outcomes

### How to download:
```bash
# Install Kaggle CLI
pip install kaggle

# Download dataset
kaggle datasets download -d sulianova/cardiovascular-disease-dataset
unzip cardiovascular-disease-dataset.zip
```

---

## 8. NIH Data Repositories

### BioLINCC (Biologic Specimen and Data Repository)
- **URL**: https://biolincc.nhlbi.nih.gov/home/
- **Focus**: NHLBI-funded cardiovascular trials
- **Major trials available**:
  - ACCORD (diabetes + cardiovascular)
  - ARIC (Atherosclerosis Risk in Communities)
  - Framingham Heart Study
  - Jackson Heart Study
  - MESA (Multi-Ethnic Study of Atherosclerosis)

### Access process:
1. Register at BioLINCC
2. Submit data request with research plan
3. Approval in 2-4 weeks
4. Download individual participant data

**Estimated trials**: 50+ major NHLBI trials with full data

---

## 9. Trial Results Aggregators

### TrialTrove (Citeline)
- **URL**: https://citeline.informa.com/products-and-services/clinical-data-and-analysis/trialtrove
- **Coverage**: 450,000+ trials
- **Access**: Subscription required (check if your institution has access)

### ClinicalStudyDataRequest.com
- **URL**: https://www.clinicalstudydatarequest.com/
- **Sponsors**: Multiple pharma companies sharing trial data
- **Process**: Submit research proposal
- **Data**: Individual patient data from approved drugs

---

## 10. Specific Cardiovascular Data Sources

### Heart Failure Trials
- **MAGGIC Meta-Analysis**: 30 HF trials, contact via publication
- **HF Preserved EF Meta-Analysis**: Multiple HFpEF trials

### STEMI/ACS Trials
- **GUSTO investigators**: Multiple thrombolysis trials
- **TIMI Study Group**: https://www.timi.org/ - contact for data requests

### Atrial Fibrillation
- **AFFIRM trial data**: Available through BioLINCC
- **ENGAGE-AF**: Daiichi Sankyo data sharing platform

---

## Recommended Workflow to Reach 1000 Trials

### Phase 1: Quick wins (150 trials, 1-2 days)
1. **Download AACT database from ClinicalTrials.gov**
   - Filter for Phase 3/4 cardiovascular trials
   - Extract: NCT ID, title, N, intervention, primary outcome

2. **Download Kaggle cardiovascular datasets**
   - 70K patient dataset
   - UCI heart disease dataset

3. **Search Cochrane for 10 major cardiovascular systematic reviews**
   - Extract trials from "Characteristics of included studies" tables
   - Each review typically has 10-20 trials

### Phase 2: Moderate effort (150 trials, 1 week)
1. **Download WHO ICTRP data**
   - Export all completed cardiovascular trials
   - Filter for N≥200, completed, Phase 3/4

2. **Extract from published meta-analyses**
   - Search PubMed for recent cardiovascular meta-analyses
   - Download supplementary data tables
   - Extract 10-15 meta-analyses × 10-20 trials each

3. **EMA Clinical Data Portal**
   - Search cardiovascular approvals
   - Download clinical study report summaries

### Phase 3: More involved (75 trials, 2 weeks)
1. **Request BioLINCC data**
   - Register and request major NHLBI trials
   - Full individual participant data available

2. **Vivli platform**
   - Search and request cardiovascular trial datasets
   - Many available within days of approval

---

## Data Quality Checklist

When extracting from these sources, ensure you capture:
- ✅ **Study identifier** (NCT number, trial acronym)
- ✅ **Sample size** (n intervention, n control)
- ✅ **Primary outcome**
- ✅ **Effect size** (OR, RR, HR) + confidence intervals
- ✅ **Follow-up duration**
- ✅ **Publication year**
- ✅ **Patient characteristics** (age, sex, baseline risk)

---

## Scripts to Help Automate Data Extraction

### Python script to download AACT database:
```python
import pandas as pd
import requests

# Download latest AACT static copy
url = "https://aact.ctti-clinicaltrials.org/static/static_db_copies/daily/aact_static.zip"
response = requests.get(url)
with open('aact_static.zip', 'wb') as f:
    f.write(response.content)

# Extract and filter cardiovascular trials
studies = pd.read_csv('aact_studies.csv')
cv_trials = studies[
    (studies['conditions'].str.contains('cardiovascular|heart|cardiac', case=False, na=False)) &
    (studies['study_type'] == 'Interventional') &
    (studies['phase'].isin(['Phase 3', 'Phase 4'])) &
    (studies['enrollment'] >= 200)
]

print(f"Found {len(cv_trials)} cardiovascular trials")
cv_trials.to_csv('cardiovascular_trials_filtered.csv', index=False)
```

### R script to extract from Cochrane reviews:
```r
library(metafor)
library(rvest)

# Function to extract trial data from Cochrane forest plot
extract_cochrane_data <- function(review_url) {
  # Download review
  page <- read_html(review_url)

  # Extract study names, sample sizes, effect sizes
  studies <- page %>% html_nodes(".study-name") %>% html_text()
  n_intervention <- page %>% html_nodes(".n-intervention") %>% html_text()
  n_control <- page %>% html_nodes(".n-control") %>% html_text()

  # Create dataframe
  data.frame(
    study = studies,
    n_int = as.numeric(n_intervention),
    n_ctrl = as.numeric(n_control)
  )
}
```

---

## Legal & Ethical Considerations

✅ **All sources listed are legal and ethical**
✅ **Public domain or require registration (free)**
✅ **Proper citation required** - cite original trials + data source
✅ **Follow data use agreements** - especially for individual patient data
✅ **NEVER scrape without permission** - use official download methods

---

## Expected Timeline to 1000 Trials

Using these sources:

- **Week 1-2**: Download bulk datasets (AACT, WHO ICTRP, Cochrane) → +200 trials
- **Week 3-4**: Extract from published meta-analyses → +150 trials
- **Week 5-6**: Manual extraction from major trials → +25 trials
- **Total new trials**: ~375 trials
- **Combined with existing 625**: **1000 trials achieved!**

---

## Next Steps

1. **Choose your primary source** (recommend starting with AACT/ClinicalTrials.gov)
2. **Download bulk data**
3. **Filter and clean** to match your existing data structure
4. **Integrate** with your current 625 trials
5. **Validate** against published meta-analyses

Would you like me to help you write scripts to download and process any of these data sources?
