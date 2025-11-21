# Getting Started with the Cardiology Meta-Analysis Dataset Project

Welcome to the world's most comprehensive cardiology meta-analysis dataset project! This guide will help you set up the environment and start collecting data.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Data Collection](#data-collection)
5. [Data Structure](#data-structure)
6. [Next Steps](#next-steps)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- Internet connection for API access
- (Optional) NCBI API key for faster PubMed access
- (Optional) PostgreSQL for database storage

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd cardio1

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create necessary directories
mkdir -p data/{raw,processed,curated,metadata} logs

# 5. Check collection status
python scripts/main_pipeline.py --status
```

## Installation

### Step 1: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 2: Install Additional Tools (Optional)

#### For R-based datasets (CardioDataSets):
```bash
# Install R (if not already installed)
# Then install the package in R:
install.packages("CardioDataSets")
```

#### For database storage:
```bash
# Install PostgreSQL
# On Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# On Mac (with Homebrew):
brew install postgresql
```

### Step 3: API Access Setup

#### PubMed/NCBI

1. **Email (Required)**: NCBI requires an email for API access
2. **API Key (Optional but recommended)**:
   - Go to: https://www.ncbi.nlm.nih.gov/account/
   - Create an account or sign in
   - Go to Settings → API Key Management
   - Create a new API key
   - Copy the key for later use

#### ClinicalTrials.gov

- No authentication required!
- API v2 is publicly accessible
- Rate limit: ~2 requests per second

#### AACT Database (Optional)

1. Register at: https://aact.ctti-clinicaltrials.org/users/sign_up
2. You'll receive database credentials
3. Update `config/database.yaml` with credentials

#### Kaggle (Optional)

1. Create Kaggle account: https://www.kaggle.com
2. Go to Account → API → Create New API Token
3. Save `kaggle.json` to `~/.kaggle/` directory

#### MIMIC (Optional)

1. Complete CITI training: https://mimic.mit.edu/docs/gettingstarted/
2. Request access through PhysioNet
3. Approval can take several days

## Configuration

### Edit Configuration File

Open `config/sources.yaml` and update:

```yaml
data_sources:
  pubmed:
    enabled: true  # Enable/disable source
    # ... other settings

  clinicaltrials:
    enabled: true

  # Enable other sources as needed
```

### Set Search Parameters

Modify search parameters in `config/sources.yaml`:

```yaml
search_parameters:
  date_range:
    start_year: 2000  # Adjust as needed
    end_year: 2025

  quality_filters:
    minimum_enrollment: 50  # Minimum sample size
    require_peer_review: true
```

### Environment Variables (Optional)

Create a `.env` file for sensitive information:

```bash
# .env file
NCBI_EMAIL=your.email@example.com
NCBI_API_KEY=your_api_key_here

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cardio_meta
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
```

## Data Collection

### Collect from Single Source

#### PubMed Only

```bash
python scripts/main_pipeline.py \
    --source pubmed \
    --email your.email@example.com \
    --api-key YOUR_API_KEY
```

#### ClinicalTrials.gov Only

```bash
python scripts/main_pipeline.py \
    --source clinicaltrials
```

### Collect from All Sources

```bash
python scripts/main_pipeline.py \
    --email your.email@example.com \
    --api-key YOUR_API_KEY
```

### Check Collection Status

```bash
python scripts/main_pipeline.py --status
```

Output example:
```
================================================================================
DATA COLLECTION STATUS
================================================================================

PUBMED:
  Files collected: 5
  Last collection: 2025-11-21 14:30:00

CLINICALTRIALS:
  Files collected: 3
  Last collection: 2025-11-21 15:45:00
================================================================================
```

### Using Individual Collectors

You can also use collectors directly:

```python
# In Python or Jupyter notebook
from scripts.collection.pubmed_collector import PubMedCollector

# Initialize
collector = PubMedCollector(
    email="your.email@example.com",
    api_key="your_api_key"
)

# Collect data
collector.collect_cardiology_dataset(
    output_dir="./data/raw/pubmed",
    start_year=2020,
    end_year=2025,
    max_results=1000
)
```

## Data Structure

After collection, your data directory will look like:

```
data/
├── raw/                          # Raw data from sources
│   ├── pubmed/
│   │   └── cardiology_articles_20251121_143000.json
│   ├── clinicaltrials/
│   │   └── cardiology_trials_20251121_154500.json
│   ├── cochrane/
│   └── kaggle/
├── processed/                    # Cleaned and standardized
│   ├── studies_processed.parquet
│   └── metadata.json
├── curated/                      # Quality-controlled datasets
│   ├── rct_dataset.csv
│   ├── observational_dataset.csv
│   └── meta_analysis_ready.parquet
└── metadata/                     # Data dictionaries and schemas
    ├── variables.json
    └── quality_reports.html
```

## Data Format

### Raw JSON Structure (PubMed)

```json
{
  "pmid": "12345678",
  "title": "Effect of Beta-Blockers in Heart Failure...",
  "abstract": "Background: ...",
  "authors": ["Smith J", "Doe A"],
  "journal": "Journal of the American College of Cardiology",
  "publication_year": "2023",
  "doi": "10.1016/j.jacc.2023.01.001",
  "mesh_terms": ["Heart Failure", "Adrenergic beta-Antagonists"],
  "publication_types": ["Randomized Controlled Trial"]
}
```

### Raw JSON Structure (ClinicalTrials.gov)

```json
{
  "nct_id": "NCT01234567",
  "title": "Beta-Blockers in Heart Failure Study",
  "overall_status": "COMPLETED",
  "enrollment": 500,
  "study_type": "Interventional",
  "phases": ["Phase 3"],
  "interventions": [
    {
      "type": "Drug",
      "name": "Carvedilol",
      "description": "..."
    }
  ],
  "primary_outcomes": [
    {
      "measure": "All-cause mortality",
      "time_frame": "12 months"
    }
  ]
}
```

## Next Steps

### 1. Explore Collected Data

```python
import pandas as pd
import json

# Load collected data
with open('data/raw/pubmed/cardiology_articles_*.json', 'r') as f:
    articles = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(articles)

# Basic exploration
print(f"Total articles: {len(df)}")
print(f"Year range: {df['publication_year'].min()} - {df['publication_year'].max()}")
print(f"\nTop journals:")
print(df['journal'].value_counts().head(10))
```

### 2. Data Processing Pipeline

Next steps in development:

1. **Data Cleaning**: Remove duplicates, handle missing data
2. **Standardization**: Uniform formats across sources
3. **Quality Assessment**: Risk of bias, GRADE scores
4. **Database Loading**: Import into PostgreSQL
5. **Meta-Analysis**: Statistical pooling of results

### 3. Run Quality Control

```bash
# Future: Quality control script
python scripts/validation/quality_control.py \
    --input data/raw/ \
    --output data/processed/
```

### 4. Database Setup

```bash
# Future: Database initialization
python scripts/setup_database.py \
    --schema docs/database_schema.md
```

### 5. Analysis

```bash
# Future: Meta-analysis script
python scripts/analysis/meta_analysis.py \
    --domain "Heart Failure" \
    --intervention "Beta-blockers" \
    --outcome "Mortality"
```

## Troubleshooting

### Common Issues

#### Rate Limit Errors

**Problem**: Too many requests to API

**Solution**:
- Get an NCBI API key for higher limits
- Reduce batch sizes in config
- Add longer delays between requests

#### Missing Dependencies

**Problem**: `ModuleNotFoundError: No module named 'Bio'`

**Solution**:
```bash
pip install biopython
```

#### Permission Errors

**Problem**: Cannot write to data directory

**Solution**:
```bash
# Ensure directories exist
mkdir -p data/{raw,processed,curated,metadata} logs

# Check permissions
chmod 755 data/ logs/
```

#### API Authentication Errors

**Problem**: NCBI rejects email/API key

**Solution**:
- Verify email is valid
- Check API key is correctly copied
- Ensure no extra spaces in credentials

### Getting Help

- Check the [documentation](docs/)
- Review [data sources](DATA_SOURCES.md)
- Check [database schema](docs/database_schema.md)
- Open an issue on GitHub

## Best Practices

### 1. Start Small

Don't try to collect everything at once:

```bash
# Start with recent years only
python scripts/main_pipeline.py \
    --email your@email.com \
    --source pubmed

# Modify config to:
# start_year: 2020
# max_results: 1000
```

### 2. Incremental Collection

Collect data in phases:
- Phase 1: Recent RCTs (2020-2025)
- Phase 2: Historical RCTs (2010-2019)
- Phase 3: Observational studies
- Phase 4: Systematic reviews

### 3. Regular Backups

```bash
# Backup collected data
tar -czf backup_$(date +%Y%m%d).tar.gz data/raw/
```

### 4. Version Control

Commit configuration changes:
```bash
git add config/sources.yaml
git commit -m "Update search parameters for heart failure subset"
```

### 5. Documentation

Document your collection runs:
```bash
# Keep a log
echo "$(date): Collected 5000 PubMed articles" >> COLLECTION_LOG.md
```

## Resource Estimates

### Time Estimates

- **PubMed** (10,000 articles): 1-2 hours
- **ClinicalTrials.gov** (5,000 trials): 30-45 minutes
- **Full collection** (100,000+ records): 6-12 hours

### Storage Estimates

- Raw JSON: ~100-500 MB per 10,000 records
- Processed data: ~50-200 MB per 10,000 records
- Full database: 50-100 GB (for 100,000+ studies)

### API Limits

- **PubMed** (with key): 10 req/sec = 36,000 req/hour
- **PubMed** (no key): 3 req/sec = 10,800 req/hour
- **ClinicalTrials.gov**: ~2 req/sec = 7,200 req/hour

## Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under CC BY 4.0.

## Acknowledgments

- NCBI/PubMed for literature access
- ClinicalTrials.gov for trial data
- Cochrane Collaboration for systematic reviews
- All data providers and the cardiology research community

---

**Ready to build the world's largest cardiology meta-analysis dataset!**

For questions or issues, please open an issue on GitHub.

Last updated: 2025-11-21
