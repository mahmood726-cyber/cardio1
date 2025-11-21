"""
PubMed Data Collector for Cardiology Meta-Analysis

This module collects cardiology literature from PubMed using the Entrez API.
Implements rate limiting and error handling as per NCBI guidelines.
"""

import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

try:
    from Bio import Entrez
except ImportError:
    print("BioPython not installed. Install with: pip install biopython")
    Entrez = None

import json


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PubMedCollector:
    """
    Collects cardiology research articles from PubMed.

    Attributes:
        email (str): Required by NCBI for API access
        api_key (str): Optional API key for higher rate limits (10 req/s vs 3 req/s)
        rate_limit (float): Time to wait between requests (seconds)
    """

    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        Initialize PubMed collector.

        Args:
            email: Email address (required by NCBI)
            api_key: NCBI API key for increased rate limits
        """
        if Entrez is None:
            raise ImportError("BioPython is required. Install with: pip install biopython")

        self.email = email
        self.api_key = api_key

        # Configure Entrez
        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key
            self.rate_limit = 0.1  # 10 requests per second with API key
        else:
            self.rate_limit = 0.34  # 3 requests per second without API key

        logger.info(f"PubMed collector initialized with email: {email}")

    def search_cardiology(
        self,
        query: Optional[str] = None,
        start_year: int = 1990,
        end_year: Optional[int] = None,
        max_results: int = 10000,
        study_types: Optional[List[str]] = None
    ) -> List[str]:
        """
        Search for cardiology publications.

        Args:
            query: Custom search query (if None, uses default cardiology terms)
            start_year: Starting year for search
            end_year: Ending year (defaults to current year)
            max_results: Maximum number of results to retrieve
            study_types: Filter by study types (e.g., ['Clinical Trial', 'Meta-Analysis'])

        Returns:
            List of PubMed IDs (PMIDs)
        """
        if end_year is None:
            end_year = datetime.now().year

        # Default cardiology search query
        if query is None:
            query = self._build_cardiology_query(study_types)

        # Add date range
        date_query = f"{query} AND {start_year}:{end_year}[pdat]"

        logger.info(f"Searching PubMed with query: {date_query}")
        logger.info(f"Requesting up to {max_results} results")

        try:
            # Search PubMed
            handle = Entrez.esearch(
                db="pubmed",
                term=date_query,
                retmax=max_results,
                sort="relevance",
                usehistory="y"
            )
            time.sleep(self.rate_limit)

            record = Entrez.read(handle)
            handle.close()

            id_list = record["IdList"]
            count = int(record["Count"])

            logger.info(f"Found {count} total results, retrieved {len(id_list)} PMIDs")

            return id_list

        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            raise

    def _build_cardiology_query(self, study_types: Optional[List[str]] = None) -> str:
        """
        Build comprehensive cardiology search query.

        Args:
            study_types: Optional list of study types to include

        Returns:
            Query string
        """
        # Core cardiology terms
        cardiology_terms = [
            "cardiology[MeSH Terms]",
            "heart diseases[MeSH Terms]",
            "cardiovascular diseases[MeSH Terms]",
            "coronary artery disease[MeSH Terms]",
            "heart failure[MeSH Terms]",
            "arrhythmias cardiac[MeSH Terms]",
            "myocardial infarction[MeSH Terms]",
            "hypertension[MeSH Terms]",
            "cardiomyopathies[MeSH Terms]"
        ]

        # Combine with OR
        base_query = "(" + " OR ".join(cardiology_terms) + ")"

        # Add study type filters if specified
        if study_types:
            type_filters = [f"{stype}[Publication Type]" for stype in study_types]
            type_query = "(" + " OR ".join(type_filters) + ")"
            base_query = f"{base_query} AND {type_query}"

        # Add quality filters
        base_query += " AND (English[Language])"
        base_query += " AND (humans[MeSH Terms])"

        return base_query

    def fetch_details(self, pmid_list: List[str], batch_size: int = 200) -> List[Dict]:
        """
        Fetch detailed information for a list of PMIDs.

        Args:
            pmid_list: List of PubMed IDs
            batch_size: Number of records to fetch per request

        Returns:
            List of article dictionaries with detailed information
        """
        articles = []

        # Process in batches
        for i in range(0, len(pmid_list), batch_size):
            batch = pmid_list[i:i+batch_size]
            logger.info(f"Fetching details for PMIDs {i+1}-{min(i+batch_size, len(pmid_list))}")

            try:
                # Fetch article details
                handle = Entrez.efetch(
                    db="pubmed",
                    id=batch,
                    rettype="medline",
                    retmode="xml"
                )
                time.sleep(self.rate_limit)

                records = Entrez.read(handle)
                handle.close()

                # Parse articles
                for record in records['PubmedArticle']:
                    article = self._parse_article(record)
                    articles.append(article)

            except Exception as e:
                logger.error(f"Error fetching batch {i}: {e}")
                continue

        logger.info(f"Successfully fetched {len(articles)} articles")
        return articles

    def _parse_article(self, record: Dict) -> Dict:
        """
        Parse PubMed article record into structured dictionary.

        Args:
            record: Raw PubMed article record

        Returns:
            Structured article dictionary
        """
        try:
            medline = record['MedlineCitation']
            article = medline['Article']

            # Extract basic information
            pmid = str(medline['PMID'])
            title = article.get('ArticleTitle', '')

            # Abstract
            abstract_parts = article.get('Abstract', {}).get('AbstractText', [])
            if isinstance(abstract_parts, list):
                abstract = ' '.join(str(part) for part in abstract_parts)
            else:
                abstract = str(abstract_parts)

            # Authors
            author_list = article.get('AuthorList', [])
            authors = []
            for author in author_list:
                if 'LastName' in author and 'ForeName' in author:
                    authors.append(f"{author['LastName']}, {author['ForeName']}")

            # Journal information
            journal_info = article.get('Journal', {})
            journal = journal_info.get('Title', '')

            pub_date = journal_info.get('JournalIssue', {}).get('PubDate', {})
            year = pub_date.get('Year', '')

            # DOI
            doi = None
            article_ids = record.get('PubmedData', {}).get('ArticleIdList', [])
            for aid in article_ids:
                if aid.attributes.get('IdType') == 'doi':
                    doi = str(aid)
                    break

            # MeSH terms
            mesh_headings = medline.get('MeshHeadingList', [])
            mesh_terms = []
            for heading in mesh_headings:
                descriptor = heading.get('DescriptorName', '')
                if descriptor:
                    mesh_terms.append(str(descriptor))

            # Publication types
            pub_types = []
            pub_type_list = article.get('PublicationTypeList', [])
            for ptype in pub_type_list:
                pub_types.append(str(ptype))

            # Construct article dictionary
            article_dict = {
                'pmid': pmid,
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'publication_year': year,
                'doi': doi,
                'mesh_terms': mesh_terms,
                'publication_types': pub_types,
                'data_source': 'PubMed',
                'extraction_date': datetime.now().isoformat()
            }

            return article_dict

        except Exception as e:
            logger.error(f"Error parsing article: {e}")
            return {}

    def save_to_json(self, articles: List[Dict], output_path: str):
        """
        Save articles to JSON file.

        Args:
            articles: List of article dictionaries
            output_path: Path to output JSON file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(articles)} articles to {output_path}")

    def collect_cardiology_dataset(
        self,
        output_dir: str = "./data/raw/pubmed",
        start_year: int = 1990,
        end_year: Optional[int] = None,
        max_results: int = 10000
    ):
        """
        Full pipeline to collect cardiology dataset from PubMed.

        Args:
            output_dir: Directory to save output files
            start_year: Starting year for search
            end_year: Ending year
            max_results: Maximum number of articles to retrieve
        """
        logger.info("=" * 80)
        logger.info("STARTING PUBMED CARDIOLOGY DATA COLLECTION")
        logger.info("=" * 80)

        # Search for articles
        pmid_list = self.search_cardiology(
            start_year=start_year,
            end_year=end_year,
            max_results=max_results
        )

        if not pmid_list:
            logger.warning("No articles found!")
            return

        # Fetch article details
        articles = self.fetch_details(pmid_list)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_dir}/cardiology_articles_{timestamp}.json"
        self.save_to_json(articles, output_path)

        logger.info("=" * 80)
        logger.info(f"COLLECTION COMPLETE: {len(articles)} articles saved")
        logger.info("=" * 80)


def main():
    """
    Example usage of PubMed collector.
    """
    # Configuration
    EMAIL = "your.email@example.com"  # REPLACE WITH YOUR EMAIL
    API_KEY = None  # Optional: get from https://www.ncbi.nlm.nih.gov/account/

    # Initialize collector
    collector = PubMedCollector(email=EMAIL, api_key=API_KEY)

    # Collect cardiology literature
    # Start with a smaller sample for testing
    collector.collect_cardiology_dataset(
        output_dir="./data/raw/pubmed",
        start_year=2020,
        end_year=2025,
        max_results=1000  # Start small for testing
    )


if __name__ == "__main__":
    main()
