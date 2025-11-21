# Comprehensive Data Sources for Cardiology Meta-Analysis

## 1. PubMed Knowledge Graph (PKG) 2.0

### Overview
- **Size**: 36+ million papers, 1.3 million patents, 480,000 clinical trials
- **Last Updated**: July 2025 (PKG24S4)
- **Format**: SQL and TSV files
- **Coverage**: Entire PubMed + ClinicalTrials.gov

### Access Information
- **Website**: https://pubmedkg.github.io/
- **Download**: Science Data Bank
- **API**: PubMed E-utilities
- **Cost**: Free

### Cardiology Filtering
- MeSH terms: "Cardiology", "Heart Diseases", "Cardiovascular Diseases"
- Keywords: coronary, cardiac, cardiovascular, heart failure, arrhythmia
- Journal filters: Major cardiology journals

### Data Fields
- PMID, Title, Abstract
- Authors, Affiliations
- Publication date, Journal
- MeSH terms, Keywords
- Citations and references
- Clinical trial registry numbers

## 2. ClinicalTrials.gov / AACT Database

### Overview
- **Size**: All registered clinical trials worldwide
- **Updates**: Daily
- **Format**: PostgreSQL relational database
- **Coverage**: 1999 - present

### Access Information
- **Website**: https://clinicaltrials.gov
- **AACT Database**: https://aact.ctti-clinicaltrials.org/
- **API**: https://clinicaltrials.gov/data-api/api
- **Cost**: Free

### Cardiology Filtering
```sql
SELECT * FROM studies
WHERE conditions LIKE '%cardiovascular%'
   OR conditions LIKE '%cardiac%'
   OR conditions LIKE '%heart%';
```

### Key Tables
- `studies` - Basic trial information
- `interventions` - Treatment arms
- `outcomes` - Endpoints measured
- `design_groups` - Study arms
- `result_groups` - Outcome data
- `baseline_measurements` - Patient characteristics
- `outcome_measurements` - Results

### Data Fields
- NCT ID, Trial title
- Phase, Status
- Enrollment
- Interventions
- Primary/secondary outcomes
- Results (if posted)
- Sponsor information

## 3. Cochrane Database of Systematic Reviews (CDSR)

### Overview
- **Size**: 10,000+ systematic reviews (subset cardiology)
- **Updates**: Monthly
- **Format**: Structured reviews + data tables
- **Coverage**: 1990s - present

### Access Information
- **Website**: https://www.cochranelibrary.com
- **Access**: Free in many countries, institutional subscription
- **Format**: PDF, XML
- **Cost**: Free in 100+ countries, subscription elsewhere

### Cardiology-Specific Content
- **Cardiac rehabilitation**: 148+ RCTs, 97,486 participants
- **Heart failure interventions**
- **Coronary revascularization**
- **Hypertension management**
- **Arrhythmia treatments**
- **Preventive cardiology**

### Review Groups
- Cochrane Heart Group
- Cochrane Hypertension Group
- Cochrane Stroke Group (overlaps)

### Data Extraction
- Characteristics of included studies
- Risk of bias assessments
- Extracted outcome data
- Forest plots (digitizable)
- Summary of findings tables

## 4. Duke Clinical Research Institute (DCRI)

### Overview
- **Size**: One of world's largest cardiovascular databanks
- **Coverage**: 1985 - present
- **Format**: Relational database
- **Specialty**: Real-world clinical data

### Key Datasets

#### DukeCath Dataset
- **Period**: 1985-2013
- **Patients**: All cardiac catheterization patients at Duke
- **Variables**: 1000+ clinical variables
- **Procedures**: Diagnostic cath, PCI, FFR

#### Duke Databank for Cardiovascular Disease (DDCD)
- Comprehensive cardiovascular outcomes
- Long-term follow-up data
- Mortality tracking
- Revascularization procedures

### Access Information
- **Website**: https://dcri.org/solutions/analytics-and-data-science/data-sharing/soar-data
- **Access**: Research collaboration, data sharing agreements
- **Cost**: Varies, academic collaborations possible

### Data Fields
- Demographics
- Risk factors
- Comorbidities
- Angiographic data
- Procedure details
- Medications
- Laboratory values
- Long-term outcomes

## 5. CardioDataSets Package

### Overview
- **Type**: R/Python package with curated datasets
- **Updates**: Regular (CRAN)
- **Format**: Data frames, tibbles
- **Focus**: Research-ready datasets

### Access Information
- **R Package**: `install.packages("CardioDataSets")`
- **GitHub**: https://github.com/lightbluetitan/cardiodatasets
- **Documentation**: https://lightbluetitan.github.io/cardiodatasets/
- **Cost**: Free, open source

### Included Datasets
1. `heartdisease_tbl_df` - Heart disease patients clinical data
2. `cardioRiskFactors_df` - Cardiovascular risk factors
3. `emotion_heartrate_df` - Emotion and heart rate study
4. Additional datasets (use `view_datasets_CardioDataSets()`)

### Topics Covered
- Heart disease
- Myocardial infarction
- Heart failure
- Aortic dissection
- Cardiovascular risk factors
- Clinical outcomes
- Drug effects
- Mortality trends

## 6. UCI Heart Disease Dataset

### Overview
- **Size**: 1000+ patients
- **Institutions**: 4 international centers
- **Format**: CSV, ARFF
- **Status**: Classic benchmark dataset

### Contributing Centers
1. **Cleveland Clinic Foundation** (303 patients)
2. **Hungarian Institute of Cardiology, Budapest**
3. **V.A. Medical Center, Long Beach, CA**
4. **University Hospital, Zurich, Switzerland**

### Access Information
- **Website**: https://archive.ics.uci.edu/ml/datasets/Heart+Disease
- **GitHub**: Multiple repositories
- **Cost**: Free

### Data Fields (76 attributes)
- Age, Sex
- Chest pain type (4 values)
- Resting blood pressure
- Serum cholesterol
- Fasting blood sugar
- Resting ECG results
- Maximum heart rate
- Exercise-induced angina
- ST depression
- Slope of peak exercise ST segment
- Number of major vessels (0-3)
- Thalassemia
- Diagnosis (angiographic disease status)

### Common Use
- Machine learning benchmarks
- Diagnostic prediction models
- Feature importance studies

## 7. Kaggle Cardiovascular Datasets

### Key Datasets

#### Cardiovascular Disease Dataset
- **Size**: 70,000 patient records
- **Source**: Medical examination data
- **Format**: CSV
- **URL**: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset

**Features**:
- Age, gender, height, weight
- Systolic and diastolic blood pressure
- Cholesterol levels
- Glucose levels
- Smoking, alcohol intake
- Physical activity
- Cardiovascular disease presence

#### Heart Disease Dataset (Multiple)
- Various collections from different sources
- UCI dataset variants
- Framingham Heart Study derived data

### Access Information
- **Platform**: Kaggle.com
- **Account**: Free Kaggle account required
- **Download**: Direct CSV download
- **Cost**: Free

## 8. MIMIC-III / MIMIC-IV

### Overview
- **Size**: 40,000+ ICU patients (MIMIC-III)
- **Institution**: MIT Lab for Computational Physiology
- **Format**: PostgreSQL database
- **Coverage**: Critical care data

### Access Information
- **Website**: https://mimic.mit.edu
- **Access**: Free after completing training
- **Requirements**: CITI training certification
- **Cost**: Free

### Cardiovascular Subset
- Cardiac ICU admissions
- Post-cardiac surgery patients
- Acute MI
- Heart failure exacerbations
- Cardiogenic shock
- Arrhythmias

### Data Types
- Demographics
- Vital signs (high resolution)
- Laboratory tests
- Medications
- Procedures
- ICD diagnosis codes
- Mortality outcomes
- ECG waveforms

## 9. American Heart Association (AHA) Repositories

### Approved Repositories
- Dataverse
- Dryad
- figshare
- Mendeley Data
- Open Science Framework (OSF)
- Synapse
- Zenodo

### AHA Journal Datasets
- Circulation
- JAHA (Journal of AHA)
- Circulation Research
- Hypertension
- Stroke

### Access Information
- **Website**: https://professional.heart.org/en/research-programs/awardee-resources/aha-approved-data-repositories
- **Policy**: Increasing data sharing requirements
- **Access**: Varies by dataset

## 10. Cardiac Atlas Project (CAP)

### Overview
- **Type**: Cardiac imaging database
- **Focus**: Structural and functional heart data
- **Format**: Image data + derived measurements
- **Coverage**: Normal and pathological hearts

### Access Information
- **Website**: https://www.cardiacatlas.org/
- **Access**: Registration required
- **Cost**: Free for academic use

### Data Types
- MRI imaging
- CT imaging
- Echocardiography
- 3D cardiac models
- Derived measurements (volumes, ejection fraction)
- Motion analysis

## 11. European Heart Journal / ESC Databases

### European Society of Cardiology (ESC) Registries
- EuroHeart survey
- ESC Heart Failure Registry
- ESC Atrial Fibrillation Registry
- EORP (EURObservational Research Programme)

### Access Information
- **Website**: https://www.escardio.org
- **Access**: Research collaboration, data requests
- **Cost**: Varies

## 12. National Registries

### United States
- **NCDR** (National Cardiovascular Data Registry)
  - CathPCI Registry
  - ICD Registry
  - LAAO Registry
  - ACTION Registry (ACS)

### United Kingdom
- **NICOR** (National Institute for Cardiovascular Outcomes Research)
  - Myocardial Ischaemia National Audit Project (MINAP)
  - National Heart Failure Audit
  - National Cardiac Arrest Audit

### Access
- Typically requires collaboration with registry holders
- Aggregate data sometimes publicly available

## 13. WHO Global Health Observatory

### Overview
- **Scope**: Global cardiovascular disease statistics
- **Format**: CSV, Excel, API
- **Coverage**: Country-level data

### Access Information
- **Website**: https://www.who.int/data/gho
- **Cost**: Free
- **API**: Available

### Cardiovascular Indicators
- CVD mortality rates
- Risk factor prevalence
- Healthcare access
- Disease burden (DALYs)

## 14. Framingham Heart Study

### Overview
- **Started**: 1948
- **Generations**: Original, Offspring, Third Generation, Omni cohorts
- **Focus**: CVD risk factors and outcomes

### Access Information
- **Website**: https://www.framinghamheartstudy.org
- **dbGaP**: Database of Genotypes and Phenotypes
- **Access**: Research proposal required
- **Cost**: Free for approved researchers

### Key Contributions
- Risk score development
- Longitudinal cardiovascular data
- Multi-generational follow-up

## Data Integration Strategy

### Priority Tiers

**Tier 1 (Immediate Access)**
- PubMed Knowledge Graph
- ClinicalTrials.gov AACT
- Kaggle public datasets
- UCI Heart Disease
- CardioDataSets package

**Tier 2 (Registration Required)**
- MIMIC-III/IV
- Cardiac Atlas Project
- Cochrane reviews
- WHO data

**Tier 3 (Collaboration/Agreement)**
- Duke DCRI databases
- National registries (NCDR, NICOR)
- ESC registries
- Framingham Heart Study

### Estimated Total Coverage

**Studies**: 100,000+ clinical trials and observational studies
**Patients**: 50+ million patient records (aggregate)
**Publications**: 500,000+ cardiology papers
**Time Span**: 1948 - 2025 (77 years)
**Geographic Coverage**: Global (100+ countries)

## Quality Metrics by Source

| Source | Quality Rating | Data Completeness | Update Frequency |
|--------|----------------|-------------------|------------------|
| PubMed KG | ⭐⭐⭐⭐⭐ | 95%+ | Daily |
| ClinicalTrials.gov | ⭐⭐⭐⭐⭐ | 80-90% | Daily |
| Cochrane | ⭐⭐⭐⭐⭐ | 95%+ | Monthly |
| Duke DCRI | ⭐⭐⭐⭐⭐ | 90%+ | Continuous |
| MIMIC | ⭐⭐⭐⭐⭐ | 85%+ | Annual |
| Kaggle | ⭐⭐⭐ | 60-80% | Variable |
| UCI | ⭐⭐⭐⭐ | 75% | Static |

## Next Steps

1. **API Integration**: Develop connectors for each data source
2. **Schema Mapping**: Create unified data model
3. **ETL Pipelines**: Automate data collection and processing
4. **Quality Control**: Implement validation rules
5. **Documentation**: Maintain detailed provenance records
