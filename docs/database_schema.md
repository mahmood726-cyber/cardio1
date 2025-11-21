# Database Schema for Cardiology Meta-Analysis Dataset

## Overview
This document describes the comprehensive database schema for storing and managing the world's largest cardiology meta-analysis dataset. The schema follows PRISMA guidelines and supports systematic review and meta-analysis workflows.

## Schema Design Principles

1. **Normalization**: Minimize redundancy while maintaining query performance
2. **Flexibility**: Support various study types (RCT, observational, systematic reviews)
3. **Traceability**: Full provenance tracking for data quality
4. **Extensibility**: Easy to add new fields and data sources
5. **Standards Compliance**: Align with PRISMA, GRADE, Cochrane standards

## Core Tables

### 1. studies
Primary table containing study-level metadata.

```sql
CREATE TABLE studies (
    -- Primary Key
    study_id SERIAL PRIMARY KEY,

    -- Identifiers
    pmid VARCHAR(20),                    -- PubMed ID
    doi VARCHAR(255),                    -- Digital Object Identifier
    nct_id VARCHAR(20),                  -- ClinicalTrials.gov ID
    cochrane_id VARCHAR(50),             -- Cochrane review ID
    other_ids JSONB,                     -- Other registry IDs

    -- Basic Information
    title TEXT NOT NULL,
    authors TEXT[],                      -- Array of author names
    corresponding_author VARCHAR(500),
    publication_year INTEGER,
    publication_date DATE,

    -- Publication Details
    journal VARCHAR(500),
    journal_impact_factor DECIMAL(5,3),
    volume VARCHAR(50),
    issue VARCHAR(50),
    pages VARCHAR(50),

    -- Study Type
    study_type VARCHAR(100),             -- RCT, Observational, Systematic Review, etc.
    study_design VARCHAR(100),           -- Parallel, Crossover, Cohort, Case-control

    -- Study Characteristics
    total_enrollment INTEGER,
    number_of_sites INTEGER,
    countries TEXT[],
    study_duration_months INTEGER,
    followup_duration_months INTEGER,

    -- Funding and Conflicts
    funding_source VARCHAR(500),
    funding_type VARCHAR(100),           -- Industry, Government, Non-profit, None
    conflicts_of_interest TEXT,

    -- Abstract and Keywords
    abstract TEXT,
    keywords TEXT[],
    mesh_terms TEXT[],

    -- Cardiology Domain
    cardiology_domain VARCHAR(100),      -- CAD, HF, Arrhythmia, etc.
    cardiology_subdomain VARCHAR(100),

    -- Data Source
    data_source VARCHAR(100),            -- PubMed, Cochrane, ClinicalTrials.gov
    data_source_url TEXT,

    -- Quality Indicators
    peer_reviewed BOOLEAN,
    retracted BOOLEAN DEFAULT FALSE,
    retraction_reason TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    extracted_by VARCHAR(100),
    extraction_date DATE,

    -- Full Text
    full_text_available BOOLEAN,
    full_text_url TEXT,

    CONSTRAINT unique_pmid UNIQUE (pmid),
    CONSTRAINT unique_doi UNIQUE (doi),
    CONSTRAINT unique_nct_id UNIQUE (nct_id)
);

CREATE INDEX idx_studies_pmid ON studies(pmid);
CREATE INDEX idx_studies_doi ON studies(doi);
CREATE INDEX idx_studies_year ON studies(publication_year);
CREATE INDEX idx_studies_domain ON studies(cardiology_domain);
CREATE INDEX idx_studies_type ON studies(study_type);
```

### 2. populations
Patient population characteristics for each study.

```sql
CREATE TABLE populations (
    population_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,

    -- Sample Size
    sample_size INTEGER NOT NULL,
    arm_name VARCHAR(255),               -- For multi-arm studies

    -- Demographics
    mean_age DECIMAL(5,2),
    age_range_min INTEGER,
    age_range_max INTEGER,
    age_sd DECIMAL(5,2),

    -- Sex Distribution
    percent_male DECIMAL(5,2),
    percent_female DECIMAL(5,2),

    -- Race/Ethnicity
    percent_white DECIMAL(5,2),
    percent_black DECIMAL(5,2),
    percent_asian DECIMAL(5,2),
    percent_hispanic DECIMAL(5,2),
    percent_other DECIMAL(5,2),

    -- Geographic
    country_distribution JSONB,

    -- Clinical Characteristics
    mean_bmi DECIMAL(5,2),
    bmi_sd DECIMAL(5,2),

    -- Cardiovascular Specific
    mean_lvef DECIMAL(5,2),              -- Left ventricular ejection fraction
    lvef_sd DECIMAL(5,2),
    mean_nyha_class DECIMAL(3,2),

    -- Comorbidities (Percentages)
    percent_diabetes DECIMAL(5,2),
    percent_hypertension DECIMAL(5,2),
    percent_hyperlipidemia DECIMAL(5,2),
    percent_smoking DECIMAL(5,2),
    percent_prior_mi DECIMAL(5,2),
    percent_prior_pci DECIMAL(5,2),
    percent_prior_cabg DECIMAL(5,2),
    percent_ckd DECIMAL(5,2),
    percent_copd DECIMAL(5,2),
    percent_stroke DECIMAL(5,2),

    -- Additional Comorbidities
    comorbidities JSONB,                 -- Flexible for additional conditions

    -- Inclusion/Exclusion Criteria
    inclusion_criteria TEXT[],
    exclusion_criteria TEXT[],

    -- Baseline Medications
    baseline_medications JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_populations_study ON populations(study_id);
```

### 3. interventions
Details of interventions/exposures studied.

```sql
CREATE TABLE interventions (
    intervention_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,

    -- Intervention Identification
    arm_name VARCHAR(255),
    intervention_type VARCHAR(100),      -- Drug, Device, Procedure, Lifestyle

    -- Drug Interventions
    drug_name VARCHAR(255),
    drug_class VARCHAR(255),
    dose VARCHAR(255),
    frequency VARCHAR(100),
    duration_weeks INTEGER,
    route VARCHAR(100),                  -- Oral, IV, SC, etc.

    -- Device Interventions
    device_name VARCHAR(255),
    device_type VARCHAR(100),            -- ICD, CRT, Pacemaker, Stent, etc.
    device_manufacturer VARCHAR(255),

    -- Procedure Interventions
    procedure_name VARCHAR(255),
    procedure_type VARCHAR(100),         -- PCI, CABG, TAVR, etc.

    -- Lifestyle/Non-pharmacological
    lifestyle_intervention TEXT,

    -- Detailed Description
    intervention_description TEXT,

    -- Control/Comparator
    is_control BOOLEAN DEFAULT FALSE,
    control_type VARCHAR(100),           -- Placebo, Standard care, Active comparator

    -- Sample Size in Arm
    n_randomized INTEGER,
    n_analyzed INTEGER,

    -- Adherence
    adherence_rate DECIMAL(5,2),
    dropout_rate DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_interventions_study ON interventions(study_id);
CREATE INDEX idx_interventions_type ON interventions(intervention_type);
CREATE INDEX idx_interventions_drug ON interventions(drug_name);
```

### 4. outcomes
Primary and secondary outcomes measured.

```sql
CREATE TABLE outcomes (
    outcome_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,

    -- Outcome Classification
    outcome_type VARCHAR(50),            -- Primary, Secondary, Exploratory
    outcome_category VARCHAR(100),       -- Efficacy, Safety, Quality of Life

    -- Outcome Definition
    outcome_name VARCHAR(500) NOT NULL,
    outcome_description TEXT,
    outcome_measure VARCHAR(255),        -- Mortality, MACE, Hospitalization, etc.

    -- Timing
    assessment_timepoint VARCHAR(100),
    followup_months INTEGER,

    -- Outcome Specifics
    outcome_domain VARCHAR(100),         -- Clinical, Surrogate, Patient-reported

    -- Composite Outcomes
    is_composite BOOLEAN DEFAULT FALSE,
    composite_components TEXT[],

    -- Measurement Details
    measurement_tool VARCHAR(255),       -- e.g., SF-36, KCCQ, etc. for QoL
    measurement_unit VARCHAR(100),

    -- Clinical Significance
    minimal_clinically_important_difference DECIMAL(10,4),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_outcomes_study ON outcomes(study_id);
CREATE INDEX idx_outcomes_type ON outcomes(outcome_type);
CREATE INDEX idx_outcomes_measure ON outcomes(outcome_measure);
```

### 5. results
Statistical results for outcomes.

```sql
CREATE TABLE results (
    result_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,
    outcome_id INTEGER REFERENCES outcomes(outcome_id) ON DELETE CASCADE,
    intervention_id INTEGER REFERENCES interventions(intervention_id),

    -- Group Identification
    group_name VARCHAR(255),
    comparison_group VARCHAR(255),

    -- Sample Sizes
    n_analyzed INTEGER,
    n_events INTEGER,                    -- For dichotomous outcomes

    -- Dichotomous Outcomes
    events_intervention INTEGER,
    total_intervention INTEGER,
    events_control INTEGER,
    total_control INTEGER,

    -- Continuous Outcomes
    mean_intervention DECIMAL(10,4),
    sd_intervention DECIMAL(10,4),
    mean_control DECIMAL(10,4),
    sd_control DECIMAL(10,4),

    -- Effect Estimates
    effect_measure_type VARCHAR(50),     -- RR, OR, HR, MD, SMD
    effect_estimate DECIMAL(10,4),
    effect_estimate_lower_ci DECIMAL(10,4),
    effect_estimate_upper_ci DECIMAL(10,4),
    confidence_level INTEGER DEFAULT 95,

    -- Statistical Significance
    p_value DECIMAL(10,8),
    statistical_significance BOOLEAN,

    -- Additional Statistics
    hazard_ratio DECIMAL(10,4),
    hr_lower_ci DECIMAL(10,4),
    hr_upper_ci DECIMAL(10,4),

    odds_ratio DECIMAL(10,4),
    or_lower_ci DECIMAL(10,4),
    or_upper_ci DECIMAL(10,4),

    relative_risk DECIMAL(10,4),
    rr_lower_ci DECIMAL(10,4),
    rr_upper_ci DECIMAL(10,4),

    mean_difference DECIMAL(10,4),
    md_lower_ci DECIMAL(10,4),
    md_upper_ci DECIMAL(10,4),

    standardized_mean_difference DECIMAL(10,4),
    smd_lower_ci DECIMAL(10,4),
    smd_upper_ci DECIMAL(10,4),

    -- Heterogeneity (for meta-analyses)
    i_squared DECIMAL(5,2),
    tau_squared DECIMAL(10,4),
    cochran_q DECIMAL(10,4),

    -- Subgroup Information
    subgroup VARCHAR(255),
    subgroup_category VARCHAR(255),

    -- Time-to-Event
    median_survival_days INTEGER,

    -- Raw Data for Meta-Analysis
    raw_data JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_results_study ON results(study_id);
CREATE INDEX idx_results_outcome ON results(outcome_id);
CREATE INDEX idx_results_intervention ON results(intervention_id);
```

### 6. quality_assessment
Risk of bias and quality ratings.

```sql
CREATE TABLE quality_assessment (
    assessment_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,

    -- Assessment Tool
    assessment_tool VARCHAR(100),        -- Cochrane RoB 2, Newcastle-Ottawa, ROBINS-I
    assessment_version VARCHAR(50),
    assessor VARCHAR(255),
    assessment_date DATE,

    -- Cochrane Risk of Bias 2.0 Domains
    random_sequence_generation VARCHAR(50),     -- Low, High, Unclear
    allocation_concealment VARCHAR(50),
    blinding_participants VARCHAR(50),
    blinding_outcome_assessment VARCHAR(50),
    incomplete_outcome_data VARCHAR(50),
    selective_reporting VARCHAR(50),
    other_bias VARCHAR(50),
    overall_risk_of_bias VARCHAR(50),

    -- ROBINS-I (for observational studies)
    bias_due_to_confounding VARCHAR(50),
    bias_in_selection VARCHAR(50),
    bias_in_classification VARCHAR(50),
    bias_due_to_deviations VARCHAR(50),
    bias_due_to_missing_data VARCHAR(50),
    bias_in_measurement VARCHAR(50),
    bias_in_selection_of_reported VARCHAR(50),

    -- Newcastle-Ottawa Scale (for observational)
    selection_score INTEGER,
    comparability_score INTEGER,
    outcome_score INTEGER,
    total_nos_score INTEGER,

    -- GRADE Assessment
    grade_quality VARCHAR(50),           -- High, Moderate, Low, Very Low
    grade_imprecision VARCHAR(50),
    grade_inconsistency VARCHAR(50),
    grade_indirectness VARCHAR(50),
    grade_publication_bias VARCHAR(50),

    -- Overall Quality Score
    quality_score INTEGER,
    quality_category VARCHAR(50),        -- Excellent, Good, Fair, Poor

    -- Comments
    risk_of_bias_notes TEXT,
    limitations TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quality_study ON quality_assessment(study_id);
CREATE INDEX idx_quality_overall ON quality_assessment(overall_risk_of_bias);
```

### 7. citations
Citation tracking and references.

```sql
CREATE TABLE citations (
    citation_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,

    -- Citation Counts
    times_cited INTEGER DEFAULT 0,
    citation_source VARCHAR(100),        -- Web of Science, Scopus, Google Scholar

    -- References
    references_to JSONB,                 -- Array of PMIDs this study cites
    cited_by JSONB,                      -- Array of PMIDs citing this study

    -- Impact Metrics
    altmetric_score DECIMAL(10,2),
    relative_citation_ratio DECIMAL(10,4),

    -- Update Tracking
    last_updated DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_citations_study ON citations(study_id);
```

### 8. data_extraction_log
Provenance and audit trail.

```sql
CREATE TABLE data_extraction_log (
    log_id SERIAL PRIMARY KEY,
    study_id INTEGER REFERENCES studies(study_id) ON DELETE CASCADE,

    -- Extraction Details
    extractor VARCHAR(255),
    extraction_date DATE,
    extraction_method VARCHAR(100),      -- Manual, Automated, Semi-automated

    -- Data Source
    original_source VARCHAR(255),
    source_url TEXT,

    -- Quality Control
    reviewed_by VARCHAR(255),
    review_date DATE,
    discrepancies TEXT,
    resolution TEXT,

    -- Version Control
    version INTEGER DEFAULT 1,
    changes_made TEXT,

    -- Flags
    needs_review BOOLEAN DEFAULT FALSE,
    review_priority VARCHAR(50),         -- High, Medium, Low

    -- Notes
    extraction_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_log_study ON data_extraction_log(study_id);
CREATE INDEX idx_log_needs_review ON data_extraction_log(needs_review);
```

## Supporting Tables

### 9. mesh_terms
Standardized medical terminology.

```sql
CREATE TABLE mesh_terms (
    mesh_id SERIAL PRIMARY KEY,
    mesh_code VARCHAR(50) UNIQUE,
    mesh_term VARCHAR(255) NOT NULL,
    mesh_tree_number VARCHAR(100),
    mesh_description TEXT,
    cardiology_relevant BOOLEAN DEFAULT FALSE
);
```

### 10. icd_codes
International Classification of Diseases codes.

```sql
CREATE TABLE icd_codes (
    icd_id SERIAL PRIMARY KEY,
    icd_version VARCHAR(20),             -- ICD-9, ICD-10, ICD-11
    icd_code VARCHAR(20),
    icd_description TEXT,
    cardiology_category VARCHAR(100)
);
```

### 11. drugs_registry
Standardized drug information.

```sql
CREATE TABLE drugs_registry (
    drug_id SERIAL PRIMARY KEY,
    generic_name VARCHAR(255),
    brand_names TEXT[],
    drug_class VARCHAR(255),
    mechanism_of_action TEXT,
    cardiology_indication TEXT[],
    atc_code VARCHAR(20)                 -- Anatomical Therapeutic Chemical code
);
```

### 12. meta_analyses
Aggregate meta-analysis results.

```sql
CREATE TABLE meta_analyses (
    meta_analysis_id SERIAL PRIMARY KEY,

    -- Meta-Analysis Identification
    title VARCHAR(500),
    analyst VARCHAR(255),
    analysis_date DATE,

    -- Scope
    research_question TEXT,
    cardiology_domain VARCHAR(100),
    intervention_category VARCHAR(100),
    outcome_category VARCHAR(100),

    -- Inclusion Criteria
    study_selection_criteria TEXT,
    included_study_ids INTEGER[],
    number_of_studies INTEGER,
    total_participants INTEGER,

    -- Pooled Results
    pooled_effect_measure VARCHAR(50),
    pooled_effect_estimate DECIMAL(10,4),
    pooled_ci_lower DECIMAL(10,4),
    pooled_ci_upper DECIMAL(10,4),
    pooled_p_value DECIMAL(10,8),

    -- Heterogeneity
    i_squared DECIMAL(5,2),
    tau_squared DECIMAL(10,4),
    cochran_q DECIMAL(10,4),
    heterogeneity_p_value DECIMAL(10,8),

    -- Model Used
    meta_analysis_model VARCHAR(50),     -- Fixed-effect, Random-effects

    -- Publication Bias
    egger_test_p_value DECIMAL(10,8),
    funnel_plot_asymmetry BOOLEAN,

    -- Subgroup Analyses
    subgroup_analyses JSONB,

    -- Sensitivity Analyses
    sensitivity_analyses JSONB,

    -- Quality of Evidence
    grade_assessment VARCHAR(50),
    certainty_of_evidence VARCHAR(50),

    -- Conclusions
    summary TEXT,
    clinical_implications TEXT,

    -- Visualizations
    forest_plot_url TEXT,
    funnel_plot_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationships and Constraints

### Entity Relationship Diagram

```
studies (1) --- (*) populations
studies (1) --- (*) interventions
studies (1) --- (*) outcomes
studies (1) --- (*) quality_assessment
studies (1) --- (1) citations
studies (1) --- (*) data_extraction_log

outcomes (*) --- (*) results --- (*) interventions

meta_analyses (*) --- (*) studies
```

## Views for Common Queries

### View: Study Summary

```sql
CREATE VIEW study_summary AS
SELECT
    s.study_id,
    s.title,
    s.authors,
    s.publication_year,
    s.journal,
    s.study_type,
    s.cardiology_domain,
    s.total_enrollment,
    q.overall_risk_of_bias,
    q.grade_quality,
    c.times_cited
FROM studies s
LEFT JOIN quality_assessment q ON s.study_id = q.study_id
LEFT JOIN citations c ON s.study_id = c.study_id;
```

### View: RCT Results Summary

```sql
CREATE VIEW rct_results_summary AS
SELECT
    s.study_id,
    s.title,
    s.publication_year,
    i.drug_name,
    o.outcome_measure,
    r.effect_measure_type,
    r.effect_estimate,
    r.effect_estimate_lower_ci,
    r.effect_estimate_upper_ci,
    r.p_value,
    q.overall_risk_of_bias
FROM studies s
JOIN interventions i ON s.study_id = i.study_id
JOIN outcomes o ON s.study_id = o.study_id
JOIN results r ON s.study_id = r.study_id AND o.outcome_id = r.outcome_id
LEFT JOIN quality_assessment q ON s.study_id = q.study_id
WHERE s.study_type = 'RCT';
```

## Data Dictionary

### Variable Naming Conventions
- Use lowercase with underscores
- Be descriptive but concise
- Follow domain standards (e.g., CDISC for clinical trials)

### Controlled Vocabularies

#### Study Types
- RCT (Randomized Controlled Trial)
- Observational_Cohort
- Observational_Case_Control
- Observational_Cross_Sectional
- Systematic_Review
- Meta_Analysis
- Registry
- Case_Series

#### Cardiology Domains
- Coronary_Artery_Disease
- Heart_Failure
- Arrhythmias
- Valvular_Disease
- Hypertension
- Cardiomyopathy
- Congenital_Heart_Disease
- Preventive_Cardiology
- Peripheral_Vascular_Disease

#### Outcome Measures
- All_Cause_Mortality
- Cardiovascular_Mortality
- MACE (Major Adverse Cardiovascular Events)
- MI (Myocardial Infarction)
- Stroke
- Hospitalization
- Revascularization
- Quality_of_Life
- Functional_Capacity

## Performance Optimization

### Indexing Strategy
- Primary keys on all tables
- Foreign keys indexed
- Frequently queried fields indexed
- Composite indexes for common joins

### Partitioning
```sql
-- Partition studies by publication year
CREATE TABLE studies_partitioned (
    LIKE studies INCLUDING ALL
) PARTITION BY RANGE (publication_year);

CREATE TABLE studies_2020_2025 PARTITION OF studies_partitioned
    FOR VALUES FROM (2020) TO (2026);
```

### Materialized Views
```sql
-- Cache expensive aggregations
CREATE MATERIALIZED VIEW studies_by_domain AS
SELECT
    cardiology_domain,
    COUNT(*) as study_count,
    AVG(total_enrollment) as avg_enrollment
FROM studies
GROUP BY cardiology_domain;

-- Refresh periodically
REFRESH MATERIALIZED VIEW studies_by_domain;
```

## Data Validation Rules

### Constraints
1. Enrollment numbers must be positive
2. Dates must be logical (publication_date <= current_date)
3. Percentages must be 0-100
4. Effect estimates with CI bounds
5. P-values between 0 and 1

### Triggers
```sql
-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables
CREATE TRIGGER update_studies_updated_at
    BEFORE UPDATE ON studies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

## Backup and Versioning

### Backup Strategy
- Daily automated backups
- Version snapshots before major updates
- Point-in-time recovery enabled

### Data Versioning
Track schema changes and data updates with version numbers.

## API Access Layer

### REST API Endpoints (Future)
- GET /api/v1/studies
- GET /api/v1/studies/{study_id}
- GET /api/v1/meta-analyses
- POST /api/v1/query (complex queries)

## Summary Statistics

### Expected Database Size
- **Studies**: 100,000+ records
- **Populations**: 200,000+ records
- **Interventions**: 300,000+ records
- **Outcomes**: 500,000+ records
- **Results**: 1,000,000+ records
- **Total Database Size**: ~50-100 GB

### Query Performance Targets
- Simple queries: <100ms
- Complex joins: <1s
- Meta-analysis aggregations: <5s

---

**Document Version**: 1.0
**Last Updated**: 2025-11-21
**Maintained By**: Cardiology Meta-Analysis Team
