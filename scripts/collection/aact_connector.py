"""
AACT Database Connector for REAL ClinicalTrials.gov Data

The AACT database contains ALL 400,000+ clinical trials from ClinicalTrials.gov.
This is REAL, live data updated daily.

To use this:
1. Register at: https://aact.ctti-clinicaltrials.org/users/sign_up
2. Receive database credentials via email
3. Use this script to query cardiology trials
"""

import psycopg2
import pandas as pd
import logging
from typing import List, Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AACTConnector:
    """
    Connect to AACT database and extract cardiology trials.

    This is REAL DATA from ALL registered clinical trials.
    """

    def __init__(
        self,
        host: str = "aact-db.ctti-clinicaltrials.org",
        port: int = 5432,
        database: str = "aact",
        user: str = None,
        password: str = None
    ):
        """
        Initialize AACT connection.

        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Your AACT username
            password: Your AACT password

        Note: Register at https://aact.ctti-clinicaltrials.org/users/sign_up
        """
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }

        self.conn = None

    def connect(self):
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            logger.info("Connected to AACT database")
        except psycopg2.Error as e:
            logger.error(f"Connection error: {e}")
            raise

    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from AACT database")

    def query_cardiology_trials(
        self,
        conditions: Optional[List[str]] = None,
        min_enrollment: int = 50,
        study_types: Optional[List[str]] = None,
        start_year: int = 1990,
        status: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Query cardiology clinical trials from AACT.

        Args:
            conditions: List of cardiovascular conditions
            min_enrollment: Minimum enrollment size
            study_types: Types of studies (Interventional, Observational)
            start_year: Minimum start year
            status: Trial status (Completed, Recruiting, etc.)

        Returns:
            DataFrame with trial data
        """
        if conditions is None:
            conditions = [
                'heart failure',
                'myocardial infarction',
                'coronary artery disease',
                'atrial fibrillation',
                'hypertension',
                'cardiomyopathy'
            ]

        if status is None:
            status = ['Completed', 'Active, not recruiting']

        # Build WHERE clause
        condition_clauses = ' OR '.join([
            f"LOWER(brief_title) LIKE '%{cond.lower()}%' OR LOWER(official_title) LIKE '%{cond.lower()}%'"
            for cond in conditions
        ])

        status_list = "', '".join(status)

        query = f"""
        SELECT
            s.nct_id,
            s.brief_title,
            s.official_title,
            s.overall_status,
            s.study_type,
            s.phase,
            s.enrollment,
            s.start_date,
            s.completion_date,
            s.primary_completion_date,
            s.study_first_submitted_date,
            s.results_first_submitted_date,
            s.source,
            s.has_expanded_access,
            s.number_of_arms,
            s.why_stopped

        FROM studies s

        WHERE ({condition_clauses})
          AND s.enrollment >= {min_enrollment}
          AND s.overall_status IN ('{status_list}')
          AND EXTRACT(YEAR FROM s.start_date) >= {start_year}

        ORDER BY s.enrollment DESC
        LIMIT 10000;
        """

        logger.info("Querying AACT database for cardiology trials...")
        df = pd.read_sql_query(query, self.conn)
        logger.info(f"Retrieved {len(df)} trials")

        return df

    def get_trial_details(self, nct_id: str) -> Dict:
        """
        Get complete details for a specific trial.

        Args:
            nct_id: NCT identifier

        Returns:
            Dictionary with comprehensive trial data
        """
        queries = {
            'study': f"SELECT * FROM studies WHERE nct_id = '{nct_id}'",
            'interventions': f"SELECT * FROM interventions WHERE nct_id = '{nct_id}'",
            'outcomes': f"SELECT * FROM outcomes WHERE nct_id = '{nct_id}'",
            'eligibility': f"SELECT * FROM eligibilities WHERE nct_id = '{nct_id}'",
            'design': f"SELECT * FROM designs WHERE nct_id = '{nct_id}'",
            'baseline_measurements': f"SELECT * FROM baseline_measurements WHERE nct_id = '{nct_id}'",
            'outcome_measurements': f"SELECT * FROM outcome_measurements WHERE nct_id = '{nct_id}'",
            'reported_events': f"SELECT * FROM reported_events WHERE nct_id = '{nct_id}'",
        }

        details = {}
        for table_name, query in queries.items():
            try:
                df = pd.read_sql_query(query, self.conn)
                details[table_name] = df.to_dict('records')
            except Exception as e:
                logger.warning(f"Could not fetch {table_name}: {e}")
                details[table_name] = []

        return details

    def query_trials_with_results(
        self,
        conditions: Optional[List[str]] = None,
        min_enrollment: int = 100
    ) -> pd.DataFrame:
        """
        Query trials that have posted results.

        These trials have actual outcome data available.

        Args:
            conditions: Cardiovascular conditions
            min_enrollment: Minimum enrollment

        Returns:
            DataFrame with trials that have results
        """
        if conditions is None:
            conditions = ['heart', 'cardiac', 'cardiovascular']

        condition_clauses = ' OR '.join([
            f"LOWER(s.brief_title) LIKE '%{cond.lower()}%'"
            for cond in conditions
        ])

        query = f"""
        SELECT
            s.nct_id,
            s.brief_title,
            s.enrollment,
            s.start_date,
            s.completion_date,
            s.results_first_submitted_date,
            COUNT(DISTINCT om.id) as outcome_measures_count,
            COUNT(DISTINCT bm.id) as baseline_measures_count

        FROM studies s
        LEFT JOIN outcome_measurements om ON s.nct_id = om.nct_id
        LEFT JOIN baseline_measurements bm ON s.nct_id = bm.nct_id

        WHERE ({condition_clauses})
          AND s.enrollment >= {min_enrollment}
          AND s.results_first_submitted_date IS NOT NULL

        GROUP BY s.nct_id, s.brief_title, s.enrollment, s.start_date,
                 s.completion_date, s.results_first_submitted_date

        HAVING COUNT(DISTINCT om.id) > 0

        ORDER BY s.enrollment DESC
        LIMIT 5000;
        """

        logger.info("Querying trials with results data...")
        df = pd.read_sql_query(query, self.conn)
        logger.info(f"Retrieved {len(df)} trials with results")

        return df

    def extract_mortality_outcomes(self, nct_ids: List[str]) -> pd.DataFrame:
        """
        Extract mortality outcome data from specific trials.

        Args:
            nct_ids: List of NCT identifiers

        Returns:
            DataFrame with mortality data
        """
        nct_list = "', '".join(nct_ids)

        query = f"""
        SELECT
            om.nct_id,
            om.outcome_type,
            om.title as outcome_title,
            om.description,
            om.param_type,
            om.param_value,
            om.dispersion_type,
            om.dispersion_value,
            om.category,
            om.classification

        FROM outcome_measurements om

        WHERE om.nct_id IN ('{nct_list}')
          AND (
              LOWER(om.title) LIKE '%mortality%'
              OR LOWER(om.title) LIKE '%death%'
              OR LOWER(om.title) LIKE '%survival%'
          )

        ORDER BY om.nct_id, om.outcome_type;
        """

        df = pd.read_sql_query(query, self.conn)
        logger.info(f"Extracted mortality data for {len(df)} outcomes")

        return df


def generate_connection_guide():
    """Generate guide for connecting to AACT."""
    guide = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                   AACT DATABASE CONNECTION GUIDE                             ║
    ║                   REAL DATA: 400,000+ Clinical Trials                        ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

    STEP 1: REGISTER FOR ACCESS
    ────────────────────────────────────────────────────────────────────────────────
    1. Go to: https://aact.ctti-clinicaltrials.org/users/sign_up
    2. Fill out registration form
    3. You'll receive database credentials via email within minutes
    4. Credentials include:
       - Username
       - Password
       - Database connection details

    STEP 2: INSTALL REQUIRED PACKAGES
    ────────────────────────────────────────────────────────────────────────────────
    pip install psycopg2-binary pandas

    STEP 3: CONNECT TO DATABASE
    ────────────────────────────────────────────────────────────────────────────────
    from aact_connector import AACTConnector

    # Initialize with your credentials
    connector = AACTConnector(
        user='your_username',
        password='your_password'
    )

    # Connect
    connector.connect()

    # Query cardiology trials
    df = connector.query_cardiology_trials(
        conditions=['heart failure', 'myocardial infarction'],
        min_enrollment=100,
        start_year=2010
    )

    print(f"Retrieved {len(df)} trials")

    # Disconnect
    connector.disconnect()

    STEP 4: EXTRACT REAL DATA FOR META-ANALYSIS
    ────────────────────────────────────────────────────────────────────────────────
    # Get trials with posted results
    trials_with_results = connector.query_trials_with_results(
        conditions=['heart failure'],
        min_enrollment=200
    )

    # Extract mortality outcomes
    nct_ids = trials_with_results['nct_id'].tolist()
    mortality_data = connector.extract_mortality_outcomes(nct_ids)

    # Process for meta-analysis
    # See data_processor.py for processing pipeline

    ALTERNATIVE: DOWNLOAD FULL DATABASE
    ────────────────────────────────────────────────────────────────────────────────
    If you want to work offline:

    1. Download PostgreSQL dump: https://aact.ctti-clinicaltrials.org/snapshots
    2. Size: ~5 GB compressed, ~25 GB uncompressed
    3. Restore to local PostgreSQL:

       createdb aact
       pg_restore -d aact aact_snapshot.dmp

    4. Connect to local database:

       connector = AACTConnector(
           host='localhost',
           user='your_local_user',
           password='your_local_password'
       )

    DATA FRESHNESS
    ────────────────────────────────────────────────────────────────────────────────
    - AACT database is updated DAILY from ClinicalTrials.gov
    - Contains most current trial information
    - Includes trials from around the world (not just USA)
    - Historical data back to 1999

    COST
    ────────────────────────────────────────────────────────────────────────────────
    FREE! Academic and commercial use allowed.

    ════════════════════════════════════════════════════════════════════════════════
    """

    return guide


if __name__ == "__main__":
    print(generate_connection_guide())

    print("\nEXAMPLE USAGE (requires credentials):")
    print("=" * 80)
    print("""
    # After registering at AACT website:

    connector = AACTConnector(
        user='your_username_from_email',
        password='your_password_from_email'
    )

    connector.connect()

    # Get ALL heart failure trials with ≥100 patients
    df = connector.query_cardiology_trials(
        conditions=['heart failure'],
        min_enrollment=100,
        start_year=2000
    )

    print(f"Retrieved {len(df)} REAL heart failure trials")

    # Get trials with mortality data
    trials_with_results = connector.query_trials_with_results(
        conditions=['heart failure'],
        min_enrollment=200
    )

    # Extract actual mortality outcomes
    nct_ids = trials_with_results['nct_id'].head(50).tolist()
    mortality = connector.extract_mortality_outcomes(nct_ids)

    connector.disconnect()

    # This is REAL DATA ready for meta-analysis!
    """)
