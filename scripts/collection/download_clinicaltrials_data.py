#!/usr/bin/env python3
"""
Download and process cardiovascular trial data from ClinicalTrials.gov AACT database.

This script downloads the publicly available AACT (Aggregate Analysis of ClinicalTrials.gov)
database and extracts cardiovascular trials to expand our meta-analysis database.

Data source: https://aact.ctti-clinicaltrials.org/
License: Public domain (US government data)

Author: Research Team
Date: November 2025
"""

import requests
import zipfile
import pandas as pd
from pathlib import Path
import io


class ClinicalTrialsDownloader:
    """Download and process cardiovascular trials from ClinicalTrials.gov AACT database."""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.output_dir = self.base_dir / "data" / "external" / "clinicaltrials_gov"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # AACT static database URL (updated daily)
        self.aact_url = "https://aact.ctti-clinicaltrials.org/static/static_db_copies/daily/"

    def download_aact_database(self):
        """
        Download the AACT database static copy.

        The AACT database is ~2GB compressed, contains all ClinicalTrials.gov data.
        We'll download and extract only the tables we need.
        """
        print("=" * 80)
        print("DOWNLOADING CLINICALTRIALS.GOV DATA (AACT DATABASE)")
        print("=" * 80)
        print()
        print("Source: https://aact.ctti-clinicaltrials.org/")
        print("Data: Public domain - US National Library of Medicine")
        print()

        # Note: The full AACT database is large (~2GB). For demonstration,
        # we'll show how to access it. In production, you might want to:
        # 1. Download the full PostgreSQL database OR
        # 2. Use their API OR
        # 3. Query their public PostgreSQL instance directly

        print("OPTION 1: Direct PostgreSQL Query (Recommended)")
        print("-" * 80)
        print("Instead of downloading 2GB, connect directly to AACT database:")
        print()
        print("  Host: aact-db.ctti-clinicaltrials.org")
        print("  Port: 5432")
        print("  Database: aact")
        print("  User: aact")
        print("  Password: aact")
        print()
        print("Python connection example:")
        print("  import psycopg2")
        print("  conn = psycopg2.connect(")
        print("      host='aact-db.ctti-clinicaltrials.org',")
        print("      port=5432,")
        print("      database='aact',")
        print("      user='aact',")
        print("      password='aact'")
        print("  )")
        print()

        print("OPTION 2: Download CSV Pipe Files")
        print("-" * 80)
        print("For offline use, download static copy (large file):")
        print(f"  URL: {self.aact_url}aact_pipe.zip")
        print()

        return True

    def query_cardiovascular_trials_direct(self):
        """
        Query AACT database directly for cardiovascular trials.

        This is the recommended approach - no large downloads needed.
        """
        print("=" * 80)
        print("QUERYING AACT DATABASE FOR CARDIOVASCULAR TRIALS")
        print("=" * 80)
        print()

        try:
            import psycopg2
        except ImportError:
            print("ERROR: psycopg2 not installed.")
            print("Install with: pip install psycopg2-binary")
            print()
            print("Alternative: Use the AACT web interface:")
            print("  https://aact.ctti-clinicaltrials.org/snapshots")
            return None

        try:
            print("Connecting to AACT PostgreSQL database...")
            conn = psycopg2.connect(
                host='aact-db.ctti-clinicaltrials.org',
                port=5432,
                database='aact',
                user='aact',
                password='aact'
            )

            print("✓ Connected successfully!")
            print()
            print("Querying cardiovascular trials...")
            print("  - Phase 3 or Phase 4")
            print("  - Interventional studies")
            print("  - Enrollment ≥ 200 patients")
            print("  - Cardiovascular conditions")
            print()

            # SQL query to extract cardiovascular trials
            query = """
            SELECT DISTINCT
                s.nct_id,
                s.brief_title,
                s.official_title,
                s.overall_status,
                s.phase,
                s.enrollment,
                s.study_type,
                s.start_date,
                s.completion_date,
                s.number_of_arms,
                string_agg(DISTINCT c.name, '; ') as conditions,
                string_agg(DISTINCT i.name, '; ') as interventions,
                string_agg(DISTINCT o.measure, '; ') as outcomes
            FROM studies s
            LEFT JOIN conditions c ON s.nct_id = c.nct_id
            LEFT JOIN interventions i ON s.nct_id = i.nct_id
            LEFT JOIN outcomes o ON s.nct_id = o.nct_id
            WHERE
                s.study_type = 'Interventional'
                AND s.phase IN ('Phase 3', 'Phase 4', 'Phase 2/Phase 3', 'Phase 3/Phase 4')
                AND s.enrollment >= 200
                AND s.overall_status IN ('Completed', 'Active, not recruiting')
                AND (
                    c.name ILIKE '%cardiovascular%' OR
                    c.name ILIKE '%heart failure%' OR
                    c.name ILIKE '%myocardial infarction%' OR
                    c.name ILIKE '%coronary%' OR
                    c.name ILIKE '%atrial fibrillation%' OR
                    c.name ILIKE '%hypertension%' OR
                    c.name ILIKE '%stroke%' OR
                    c.name ILIKE '%cardiac%'
                )
            GROUP BY s.nct_id, s.brief_title, s.official_title, s.overall_status,
                     s.phase, s.enrollment, s.study_type, s.start_date, s.completion_date,
                     s.number_of_arms
            ORDER BY s.enrollment DESC
            LIMIT 1000;
            """

            df = pd.read_sql_query(query, conn)
            conn.close()

            print(f"✓ Query complete! Found {len(df)} cardiovascular trials")
            print()

            # Save to CSV
            output_file = self.output_dir / "clinicaltrials_gov_cardiovascular.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Saved to: {output_file}")
            print()

            # Display summary statistics
            print("=" * 80)
            print("SUMMARY STATISTICS")
            print("=" * 80)
            print(f"Total trials: {len(df)}")
            print(f"Total patients: {df['enrollment'].sum():,}")
            print()
            print("By phase:")
            print(df['phase'].value_counts())
            print()
            print("By status:")
            print(df['overall_status'].value_counts())
            print()

            # Show top 10 largest trials
            print("=" * 80)
            print("TOP 10 LARGEST TRIALS")
            print("=" * 80)
            top_trials = df.nlargest(10, 'enrollment')[
                ['nct_id', 'brief_title', 'enrollment', 'phase']
            ]
            print(top_trials.to_string(index=False))
            print()

            return df

        except Exception as e:
            print(f"ERROR connecting to AACT database: {e}")
            print()
            print("Alternative approaches:")
            print("1. Check your internet connection")
            print("2. Visit AACT website for manual download: https://aact.ctti-clinicaltrials.org/")
            print("3. Use Cochrane or other data sources (see DATA_SOURCES_GUIDE.md)")
            return None

    def integrate_with_existing_database(self, clinicaltrials_df, existing_trials_path=None):
        """
        Integrate ClinicalTrials.gov data with existing trial database.

        Args:
            clinicaltrials_df: DataFrame with ClinicalTrials.gov data
            existing_trials_path: Path to existing trial database (optional)
        """
        if clinicaltrials_df is None or len(clinicaltrials_df) == 0:
            print("No ClinicalTrials.gov data to integrate")
            return

        print("=" * 80)
        print("INTEGRATING WITH EXISTING DATABASE")
        print("=" * 80)
        print()

        # Convert to our standardized format
        print("Converting to standardized format...")
        standardized = pd.DataFrame({
            'study_id': clinicaltrials_df['nct_id'],
            'title': clinicaltrials_df['brief_title'],
            'category': 'ClinicalTrials.gov Import',
            'intervention': clinicaltrials_df['interventions'],
            'control': 'Comparator',  # Would need to parse from interventions
            'n_total': clinicaltrials_df['enrollment'],
            'phase': clinicaltrials_df['phase'],
            'status': clinicaltrials_df['overall_status'],
            'conditions': clinicaltrials_df['conditions'],
            'outcomes': clinicaltrials_df['outcomes'],
            'start_date': clinicaltrials_df['start_date'],
            'completion_date': clinicaltrials_df['completion_date'],
            'source': 'ClinicalTrials.gov AACT Database'
        })

        # Save standardized version
        output_file = self.output_dir / "clinicaltrials_gov_standardized.csv"
        standardized.to_csv(output_file, index=False)
        print(f"✓ Saved standardized format: {output_file}")
        print()

        # Note about further processing needed
        print("NOTE: ClinicalTrials.gov data needs further processing:")
        print("  - Extract specific outcomes and effect sizes")
        print("  - Parse intervention vs control groups")
        print("  - Link to published results (if available)")
        print("  - Calculate standardized effect sizes")
        print()
        print("Many trials in ClinicalTrials.gov don't have posted results.")
        print("Best approach: Use this as a catalog, then extract published data")
        print("from journal articles for trials of interest.")
        print()

        return standardized


def main():
    """Main execution."""
    downloader = ClinicalTrialsDownloader()

    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║  CLINICALTRIALS.GOV CARDIOVASCULAR DATA DOWNLOADER                       ║
    ║  Data Source: AACT Database (Aggregate Analysis of ClinicalTrials.gov)  ║
    ║  License: Public Domain (US Government Data)                             ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)

    # Show download options
    downloader.download_aact_database()

    # Attempt direct database query
    print("ATTEMPTING DIRECT DATABASE QUERY...")
    print()
    df = downloader.query_cardiovascular_trials_direct()

    if df is not None:
        # Integrate with existing database
        downloader.integrate_with_existing_database(df)

        print("=" * 80)
        print("SUCCESS!")
        print("=" * 80)
        print(f"Downloaded {len(df)} cardiovascular trials from ClinicalTrials.gov")
        print()
        print("Next steps:")
        print("1. Review: data/external/clinicaltrials_gov/clinicaltrials_gov_cardiovascular.csv")
        print("2. Select trials of interest")
        print("3. Extract published results from journal articles")
        print("4. Integrate with existing 625-trial database")
        print()
    else:
        print("=" * 80)
        print("ALTERNATIVE APPROACH")
        print("=" * 80)
        print("If direct database query failed, please:")
        print()
        print("1. Visit: https://aact.ctti-clinicaltrials.org/snapshots")
        print("2. Download monthly snapshot (CSV format)")
        print("3. Extract 'studies.txt', 'conditions.txt', 'interventions.txt'")
        print("4. Re-run this script with local files")
        print()
        print("OR use other data sources (see DATA_SOURCES_GUIDE.md):")
        print("  - Cochrane systematic reviews (easiest)")
        print("  - Published meta-analysis supplementary data")
        print("  - WHO ICTRP database")
        print()


if __name__ == "__main__":
    main()
