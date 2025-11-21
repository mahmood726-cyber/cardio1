"""
Data Processing and ETL Pipeline for Real Cardiology Data

Processes raw data from multiple sources into standardized format for meta-analysis.
Handles:
- PubMed XML/JSON
- ClinicalTrials.gov data
- CSV/Excel files
- Database exports
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, asdict
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class StandardizedStudy:
    """Standardized study format for meta-analysis."""
    # Identifiers
    study_id: str
    pmid: Optional[str] = None
    nct_id: Optional[str] = None
    doi: Optional[str] = None

    # Study info
    title: str = ""
    authors: List[str] = None
    journal: str = ""
    year: int = None

    # Design
    study_type: str = ""  # RCT, Observational, etc.
    intervention: str = ""
    control: str = ""

    # Sample
    n_intervention: int = None
    n_control: int = None

    # Outcomes
    events_intervention: int = None
    events_control: int = None
    outcome_measure: str = ""

    # Effect estimates
    effect_measure: str = ""  # RR, OR, HR, MD, SMD
    estimate: float = None
    se: float = None
    ci_lower: float = None
    ci_upper: float = None
    p_value: float = None

    # Quality
    risk_of_bias: str = ""

    # Source
    data_source: str = ""
    extraction_date: str = ""

    def __post_init__(self):
        if self.authors is None:
            self.authors = []


class DataProcessor:
    """Processes raw cardiology data into standardized format."""

    def __init__(self, output_dir: str = "./data/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_clinical_trials(
        self,
        input_file: str,
        outcome_of_interest: str = "mortality"
    ) -> pd.DataFrame:
        """
        Process ClinicalTrials.gov JSON data.

        Args:
            input_file: Path to JSON file
            outcome_of_interest: Primary outcome to extract

        Returns:
            DataFrame of standardized studies
        """
        logger.info(f"Processing ClinicalTrials.gov data: {input_file}")

        with open(input_file, 'r') as f:
            trials = json.load(f)

        studies = []
        for trial in trials:
            # Extract relevant fields
            study = StandardizedStudy(
                study_id=trial.get('nct_id', ''),
                nct_id=trial.get('nct_id'),
                title=trial.get('title', ''),
                year=self._extract_year(trial.get('start_date', '')),
                study_type=trial.get('study_type', ''),
                intervention=self._extract_intervention_name(trial.get('interventions', [])),
                n_intervention=trial.get('enrollment', 0) // 2,  # Approximate
                n_control=trial.get('enrollment', 0) // 2,
                outcome_measure=outcome_of_interest,
                data_source='ClinicalTrials.gov'
            )

            studies.append(asdict(study))

        df = pd.DataFrame(studies)
        logger.info(f"Processed {len(df)} trials")

        return df

    def process_pubmed_data(
        self,
        input_file: str
    ) -> pd.DataFrame:
        """
        Process PubMed JSON data.

        Args:
            input_file: Path to JSON file

        Returns:
            DataFrame of standardized studies
        """
        logger.info(f"Processing PubMed data: {input_file}")

        with open(input_file, 'r') as f:
            articles = json.load(f)

        studies = []
        for article in articles:
            # Check if it's a clinical trial
            pub_types = article.get('publication_types', [])
            is_trial = any('trial' in pt.lower() for pt in pub_types)

            if not is_trial:
                continue

            study = StandardizedStudy(
                study_id=article.get('pmid', ''),
                pmid=article.get('pmid'),
                doi=article.get('doi'),
                title=article.get('title', ''),
                authors=article.get('authors', []),
                journal=article.get('journal', ''),
                year=int(article.get('publication_year', 0)) if article.get('publication_year') else None,
                study_type='RCT' if is_trial else 'Unknown',
                data_source='PubMed'
            )

            studies.append(asdict(study))

        df = pd.DataFrame(studies)
        logger.info(f"Processed {len(df)} articles")

        return df

    def process_csv_meta_analysis(
        self,
        input_file: str,
        effect_type: str = "log_rr"
    ) -> pd.DataFrame:
        """
        Process CSV file with meta-analysis data.

        Expected columns:
        - study_id: Study identifier
        - year: Publication year
        - n_intervention: Sample size intervention
        - n_control: Sample size control
        - events_intervention: Events in intervention
        - events_control: Events in control
        - OR columns with effect estimates: estimate, se, ci_lower, ci_upper

        Args:
            input_file: Path to CSV file
            effect_type: Type of effect measure

        Returns:
            DataFrame of standardized studies
        """
        logger.info(f"Processing CSV meta-analysis data: {input_file}")

        df = pd.read_csv(input_file)

        # Check required columns
        required = ['study_id']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Standardize
        studies = []
        for _, row in df.iterrows():
            study = StandardizedStudy(
                study_id=row.get('study_id', ''),
                study_name=row.get('study_name', ''),
                nct_id=row.get('nct_id'),
                title=row.get('title', row.get('study_name', '')),
                year=int(row['year']) if 'year' in row and pd.notna(row['year']) else None,
                intervention=row.get('intervention', ''),
                control=row.get('control', ''),
                n_intervention=int(row['n_intervention']) if 'n_intervention' in row and pd.notna(row['n_intervention']) else None,
                n_control=int(row['n_control']) if 'n_control' in row and pd.notna(row['n_control']) else None,
                events_intervention=int(row['events_intervention']) if 'events_intervention' in row and pd.notna(row['events_intervention']) else None,
                events_control=int(row['events_control']) if 'events_control' in row and pd.notna(row['events_control']) else None,
                outcome_measure=row.get('outcome', ''),
                effect_measure=effect_type,
                estimate=float(row[effect_type]) if effect_type in row and pd.notna(row[effect_type]) else None,
                se=float(row[f'se_{effect_type}']) if f'se_{effect_type}' in row and pd.notna(row[f'se_{effect_type}']) else None,
                ci_lower=float(row['ci_lower']) if 'ci_lower' in row and pd.notna(row['ci_lower']) else None,
                ci_upper=float(row['ci_upper']) if 'ci_upper' in row and pd.notna(row['ci_upper']) else None,
                p_value=float(row['p_value']) if 'p_value' in row and pd.notna(row['p_value']) else None,
                risk_of_bias=row.get('quality_score', ''),
                data_source=row.get('data_source', 'CSV')
            )

            studies.append(asdict(study))

        df_standardized = pd.DataFrame(studies)
        logger.info(f"Standardized {len(df_standardized)} studies")

        return df_standardized

    def calculate_effect_sizes(
        self,
        df: pd.DataFrame,
        effect_type: str = "log_rr"
    ) -> pd.DataFrame:
        """
        Calculate effect sizes from raw count data.

        Args:
            df: DataFrame with count data
            effect_type: Type of effect to calculate (log_rr, log_or, log_hr, md, smd)

        Returns:
            DataFrame with calculated effect sizes
        """
        logger.info(f"Calculating {effect_type} from raw data")

        df = df.copy()

        if effect_type == "log_rr":
            # Log risk ratio
            df['estimate'] = self._calculate_log_rr(df)
            df['se'] = self._calculate_se_log_rr(df)
        elif effect_type == "log_or":
            # Log odds ratio
            df['estimate'] = self._calculate_log_or(df)
            df['se'] = self._calculate_se_log_or(df)
        else:
            raise ValueError(f"Unsupported effect type: {effect_type}")

        # Calculate CI
        df['ci_lower'] = df['estimate'] - 1.96 * df['se']
        df['ci_upper'] = df['estimate'] + 1.96 * df['se']

        # Calculate p-value
        df['p_value'] = 2 * (1 - stats.norm.cdf(np.abs(df['estimate'] / df['se'])))

        return df

    def _calculate_log_rr(self, df: pd.DataFrame) -> pd.Series:
        """Calculate log risk ratio."""
        events_i = df['events_intervention']
        n_i = df['n_intervention']
        events_c = df['events_control']
        n_c = df['n_control']

        # Add continuity correction for zero cells
        events_i_adj = events_i + 0.5 * (events_i == 0)
        events_c_adj = events_c + 0.5 * (events_c == 0)

        risk_i = events_i_adj / n_i
        risk_c = events_c_adj / n_c

        return np.log(risk_i / risk_c)

    def _calculate_se_log_rr(self, df: pd.DataFrame) -> pd.Series:
        """Calculate standard error of log risk ratio."""
        events_i = df['events_intervention']
        n_i = df['n_intervention']
        events_c = df['events_control']
        n_c = df['n_control']

        # Add continuity correction
        events_i_adj = events_i + 0.5 * (events_i == 0)
        events_c_adj = events_c + 0.5 * (events_c == 0)

        se = np.sqrt(
            (1 / events_i_adj) - (1 / n_i) +
            (1 / events_c_adj) - (1 / n_c)
        )

        return se

    def _calculate_log_or(self, df: pd.DataFrame) -> pd.Series:
        """Calculate log odds ratio."""
        events_i = df['events_intervention']
        n_i = df['n_intervention']
        events_c = df['events_control']
        n_c = df['n_control']

        # Add continuity correction
        a = events_i + 0.5
        b = n_i - events_i + 0.5
        c = events_c + 0.5
        d = n_c - events_c + 0.5

        return np.log((a * d) / (b * c))

    def _calculate_se_log_or(self, df: pd.DataFrame) -> pd.Series:
        """Calculate standard error of log odds ratio."""
        events_i = df['events_intervention']
        n_i = df['n_intervention']
        events_c = df['events_control']
        n_c = df['n_control']

        # Add continuity correction
        a = events_i + 0.5
        b = n_i - events_i + 0.5
        c = events_c + 0.5
        d = n_c - events_c + 0.5

        se = np.sqrt(
            (1 / a) + (1 / b) + (1 / c) + (1 / d)
        )

        return se

    def _extract_year(self, date_str: str) -> Optional[int]:
        """Extract year from date string."""
        if not date_str:
            return None

        # Try to find 4-digit year
        match = re.search(r'(\d{4})', date_str)
        if match:
            return int(match.group(1))

        return None

    def _extract_intervention_name(self, interventions: List[Dict]) -> str:
        """Extract primary intervention name."""
        if not interventions:
            return ""

        # Get first drug or device intervention
        for interv in interventions:
            if interv.get('type') in ['Drug', 'Device', 'Biological']:
                return interv.get('name', '')

        # Fallback to first intervention
        return interventions[0].get('name', '')

    def merge_duplicate_studies(
        self,
        df: pd.DataFrame,
        match_fields: List[str] = ['pmid', 'nct_id', 'doi']
    ) -> pd.DataFrame:
        """
        Merge duplicate studies from different sources.

        Args:
            df: DataFrame with studies
            match_fields: Fields to match on

        Returns:
            Deduplicated DataFrame
        """
        logger.info("Detecting and merging duplicate studies")

        initial_count = len(df)

        # For each match field, find duplicates
        for field in match_fields:
            if field not in df.columns:
                continue

            # Group by field
            grouped = df.groupby(field)

            # For groups with multiple entries, keep most complete
            for name, group in grouped:
                if len(group) > 1 and pd.notna(name) and name != '':
                    # Count non-null values per row
                    completeness = group.notna().sum(axis=1)
                    best_idx = completeness.idxmax()

                    # Drop other rows
                    drop_indices = group.index[group.index != best_idx]
                    df = df.drop(drop_indices)

        final_count = len(df)
        duplicates_removed = initial_count - final_count

        logger.info(f"Removed {duplicates_removed} duplicate studies")
        logger.info(f"Final count: {final_count} studies")

        return df.reset_index(drop=True)

    def save_processed_data(
        self,
        df: pd.DataFrame,
        filename: str,
        format: str = 'csv'
    ):
        """Save processed data."""
        output_path = self.output_dir / filename

        if format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'parquet':
            df.to_parquet(output_path, index=False)
        elif format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Saved processed data to: {output_path}")


# Example usage
if __name__ == "__main__":
    from scipy import stats

    processor = DataProcessor()

    # Process beta-blocker meta-analysis
    logger.info("Processing beta-blocker trial data...")

    df = processor.process_csv_meta_analysis(
        'data/raw/sample_metaanalysis/beta_blockers_hf_mortality.csv',
        effect_type='log_rr'
    )

    print("\nProcessed Data Summary:")
    print(f"Number of studies: {len(df)}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    print(f"Studies with effect estimates: {df['estimate'].notna().sum()}")

    # Save
    processor.save_processed_data(df, 'beta_blockers_processed.csv')

    logger.info("Processing complete!")
