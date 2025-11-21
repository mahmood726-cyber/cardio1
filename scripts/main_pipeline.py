"""
Main Data Collection Pipeline for Cardiology Meta-Analysis

Orchestrates data collection from multiple sources and manages the entire ETL process.
"""

import logging
import argparse
import yaml
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from collection.pubmed_collector import PubMedCollector
from collection.clinicaltrials_collector import ClinicalTrialsCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CardiologyDataPipeline:
    """
    Main pipeline for collecting and processing cardiology meta-analysis data.
    """

    def __init__(self, config_path: str = "config/sources.yaml"):
        """
        Initialize pipeline with configuration.

        Args:
            config_path: Path to configuration YAML file
        """
        self.config = self._load_config(config_path)
        logger.info("Pipeline initialized")

    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration: {e}")
            raise

    def collect_pubmed_data(self, email: str, api_key: str = None):
        """
        Collect data from PubMed.

        Args:
            email: Email address for NCBI
            api_key: Optional API key for higher rate limits
        """
        logger.info("=" * 80)
        logger.info("COLLECTING PUBMED DATA")
        logger.info("=" * 80)

        if not self.config['data_sources']['pubmed']['enabled']:
            logger.warning("PubMed collection is disabled in config")
            return

        # Get search parameters
        search_params = self.config['search_parameters']
        quality_filters = self.config['quality_filters']

        # Initialize collector
        collector = PubMedCollector(email=email, api_key=api_key)

        # Collect data
        output_dir = f"{self.config['output']['raw_data_dir']}/pubmed"
        collector.collect_cardiology_dataset(
            output_dir=output_dir,
            start_year=search_params['date_range']['start_year'],
            end_year=search_params['date_range']['end_year'],
            max_results=10000  # Adjust based on needs
        )

        logger.info("PubMed data collection complete")

    def collect_clinicaltrials_data(self):
        """
        Collect data from ClinicalTrials.gov.
        """
        logger.info("=" * 80)
        logger.info("COLLECTING CLINICALTRIALS.GOV DATA")
        logger.info("=" * 80)

        if not self.config['data_sources']['clinicaltrials']['enabled']:
            logger.warning("ClinicalTrials.gov collection is disabled in config")
            return

        # Get search parameters
        quality_filters = self.config['quality_filters']

        # Initialize collector
        collector = ClinicalTrialsCollector()

        # Collect data
        output_dir = f"{self.config['output']['raw_data_dir']}/clinicaltrials"
        collector.collect_cardiology_trials(
            output_dir=output_dir,
            min_enrollment=quality_filters['minimum_enrollment'],
            max_results=1000,
            fetch_detailed=False
        )

        logger.info("ClinicalTrials.gov data collection complete")

    def run_full_pipeline(self, email: str = None, api_key: str = None):
        """
        Run the complete data collection pipeline.

        Args:
            email: Email for PubMed (required if collecting PubMed data)
            api_key: API key for PubMed (optional)
        """
        logger.info("=" * 100)
        logger.info("STARTING FULL CARDIOLOGY META-ANALYSIS DATA COLLECTION PIPELINE")
        logger.info("=" * 100)

        start_time = datetime.now()

        # Create necessary directories
        self._create_directories()

        # Collect from each enabled source
        enabled_sources = [
            name for name, config in self.config['data_sources'].items()
            if config.get('enabled', False)
        ]

        logger.info(f"Enabled data sources: {', '.join(enabled_sources)}")

        # PubMed
        if 'pubmed' in enabled_sources:
            if not email:
                logger.warning("Email required for PubMed - skipping")
            else:
                try:
                    self.collect_pubmed_data(email=email, api_key=api_key)
                except Exception as e:
                    logger.error(f"Error collecting PubMed data: {e}")

        # ClinicalTrials.gov
        if 'clinicaltrials' in enabled_sources:
            try:
                self.collect_clinicaltrials_data()
            except Exception as e:
                logger.error(f"Error collecting ClinicalTrials.gov data: {e}")

        # Future: Add other data sources
        # - Cochrane
        # - AACT
        # - Kaggle datasets
        # - etc.

        end_time = datetime.now()
        duration = end_time - start_time

        logger.info("=" * 100)
        logger.info(f"PIPELINE COMPLETE - Duration: {duration}")
        logger.info("=" * 100)

    def _create_directories(self):
        """
        Create necessary directory structure.
        """
        directories = [
            self.config['output']['raw_data_dir'],
            self.config['output']['processed_data_dir'],
            self.config['output']['curated_data_dir'],
            self.config['output']['metadata_dir'],
            "logs"
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

        logger.info("Directory structure created")

    def get_collection_status(self):
        """
        Get status of data collection from all sources.

        Returns:
            Dictionary with collection statistics
        """
        status = {}

        raw_data_dir = Path(self.config['output']['raw_data_dir'])

        for source_name in self.config['data_sources'].keys():
            source_dir = raw_data_dir / source_name

            if source_dir.exists():
                files = list(source_dir.glob('*.json'))
                status[source_name] = {
                    'files': len(files),
                    'last_collection': max(
                        [f.stat().st_mtime for f in files]
                    ) if files else None
                }
            else:
                status[source_name] = {
                    'files': 0,
                    'last_collection': None
                }

        return status


def main():
    """
    Command-line interface for the pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Cardiology Meta-Analysis Data Collection Pipeline"
    )

    parser.add_argument(
        '--config',
        default='config/sources.yaml',
        help='Path to configuration file'
    )

    parser.add_argument(
        '--email',
        help='Email address for PubMed API (required for PubMed collection)'
    )

    parser.add_argument(
        '--api-key',
        help='NCBI API key for PubMed (optional, increases rate limit)'
    )

    parser.add_argument(
        '--source',
        choices=['all', 'pubmed', 'clinicaltrials'],
        default='all',
        help='Which data source to collect from'
    )

    parser.add_argument(
        '--status',
        action='store_true',
        help='Show collection status and exit'
    )

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = CardiologyDataPipeline(config_path=args.config)

    # Show status if requested
    if args.status:
        status = pipeline.get_collection_status()
        print("\n" + "=" * 80)
        print("DATA COLLECTION STATUS")
        print("=" * 80)
        for source, info in status.items():
            print(f"\n{source.upper()}:")
            print(f"  Files collected: {info['files']}")
            if info['last_collection']:
                last_date = datetime.fromtimestamp(info['last_collection'])
                print(f"  Last collection: {last_date}")
            else:
                print(f"  Last collection: Never")
        print("\n" + "=" * 80)
        return

    # Run collection
    if args.source == 'all':
        pipeline.run_full_pipeline(email=args.email, api_key=args.api_key)
    elif args.source == 'pubmed':
        if not args.email:
            logger.error("Email required for PubMed collection")
            sys.exit(1)
        pipeline.collect_pubmed_data(email=args.email, api_key=args.api_key)
    elif args.source == 'clinicaltrials':
        pipeline.collect_clinicaltrials_data()


if __name__ == "__main__":
    main()
