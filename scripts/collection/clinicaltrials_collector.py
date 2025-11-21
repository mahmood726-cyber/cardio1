"""
ClinicalTrials.gov Data Collector for Cardiology Meta-Analysis

This module collects cardiology clinical trials from ClinicalTrials.gov API v2.
Comprehensive data extraction for cardiovascular interventions and outcomes.
"""

import requests
import logging
import time
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClinicalTrialsCollector:
    """
    Collects clinical trial data from ClinicalTrials.gov API.

    API Documentation: https://clinicaltrials.gov/data-api/api
    """

    def __init__(self, api_url: str = "https://clinicaltrials.gov/api/v2"):
        """
        Initialize ClinicalTrials.gov collector.

        Args:
            api_url: Base URL for ClinicalTrials.gov API
        """
        self.api_url = api_url
        self.rate_limit = 0.5  # Conservative rate limit (2 requests/second)
        logger.info("ClinicalTrials.gov collector initialized")

    def search_cardiology_trials(
        self,
        conditions: Optional[List[str]] = None,
        min_enrollment: int = 50,
        max_results: int = 1000,
        start_date: Optional[str] = None,
        completion_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for cardiology clinical trials.

        Args:
            conditions: List of cardiovascular conditions to search
            min_enrollment: Minimum enrollment size
            max_results: Maximum number of results
            start_date: Minimum start date (YYYY-MM-DD)
            completion_date: Maximum completion date (YYYY-MM-DD)

        Returns:
            List of trial summaries
        """
        if conditions is None:
            conditions = self._default_cardiology_conditions()

        logger.info(f"Searching for cardiology trials with conditions: {conditions}")

        all_trials = []

        # Search for each condition
        for condition in conditions:
            logger.info(f"Searching for condition: {condition}")

            try:
                trials = self._search_by_condition(
                    condition=condition,
                    min_enrollment=min_enrollment,
                    max_results=max_results,
                    start_date=start_date,
                    completion_date=completion_date
                )

                all_trials.extend(trials)
                logger.info(f"Found {len(trials)} trials for {condition}")

                time.sleep(self.rate_limit)

            except Exception as e:
                logger.error(f"Error searching for {condition}: {e}")
                continue

        # Remove duplicates based on NCT ID
        unique_trials = {trial['nct_id']: trial for trial in all_trials}
        unique_trials_list = list(unique_trials.values())

        logger.info(f"Total unique trials found: {len(unique_trials_list)}")

        return unique_trials_list

    def _default_cardiology_conditions(self) -> List[str]:
        """
        Default list of cardiovascular conditions to search.

        Returns:
            List of condition terms
        """
        return [
            "Coronary Artery Disease",
            "Myocardial Infarction",
            "Heart Failure",
            "Atrial Fibrillation",
            "Hypertension",
            "Cardiomyopathy",
            "Valvular Heart Disease",
            "Arrhythmia",
            "Angina",
            "Acute Coronary Syndrome",
            "Ventricular Tachycardia",
            "Cardiac Arrest",
            "Aortic Stenosis",
            "Mitral Regurgitation",
            "Pulmonary Hypertension"
        ]

    def _search_by_condition(
        self,
        condition: str,
        min_enrollment: int,
        max_results: int,
        start_date: Optional[str] = None,
        completion_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for trials by specific condition.

        Args:
            condition: Medical condition
            min_enrollment: Minimum enrollment
            max_results: Maximum results
            start_date: Minimum start date
            completion_date: Maximum completion date

        Returns:
            List of trial dictionaries
        """
        # Build query parameters
        params = {
            "query.cond": condition,
            "filter.overallStatus": ["COMPLETED", "ACTIVE_NOT_RECRUITING", "RECRUITING"],
            "pageSize": min(max_results, 1000),  # API limit
            "format": "json"
        }

        # Add optional filters
        if start_date:
            params["filter.advanced"] = f"AREA[StartDate]RANGE[{start_date},MAX]"

        endpoint = f"{self.api_url}/studies"

        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            studies = data.get("studies", [])

            # Extract basic information
            trials = []
            for study in studies:
                protocol = study.get("protocolSection", {})
                trial_info = self._extract_trial_summary(protocol)

                # Filter by minimum enrollment
                if trial_info.get("enrollment", 0) >= min_enrollment:
                    trials.append(trial_info)

            return trials

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error searching for {condition}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error processing results for {condition}: {e}")
            return []

    def _extract_trial_summary(self, protocol: Dict) -> Dict:
        """
        Extract summary information from trial protocol.

        Args:
            protocol: Protocol section of trial data

        Returns:
            Trial summary dictionary
        """
        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        arms = protocol.get("armsInterventionsModule", {})
        outcomes = protocol.get("outcomesModule", {})
        eligibility = protocol.get("eligibilityModule", {})

        trial = {
            # Identification
            "nct_id": identification.get("nctId", ""),
            "title": identification.get("briefTitle", ""),
            "official_title": identification.get("officialTitle", ""),
            "acronym": identification.get("acronym", ""),

            # Status
            "overall_status": status.get("overallStatus", ""),
            "start_date": status.get("startDateStruct", {}).get("date", ""),
            "completion_date": status.get("completionDateStruct", {}).get("date", ""),
            "enrollment": status.get("enrollmentInfo", {}).get("count", 0),

            # Design
            "study_type": design.get("studyType", ""),
            "phases": design.get("phases", []),
            "allocation": design.get("designInfo", {}).get("allocation", ""),
            "intervention_model": design.get("designInfo", {}).get("interventionModel", ""),
            "primary_purpose": design.get("designInfo", {}).get("primaryPurpose", ""),
            "masking": design.get("designInfo", {}).get("maskingInfo", {}).get("masking", ""),

            # Interventions
            "interventions": self._extract_interventions(arms.get("interventions", [])),
            "arms": [arm.get("label", "") for arm in arms.get("armGroups", [])],

            # Outcomes
            "primary_outcomes": self._extract_outcomes(outcomes.get("primaryOutcomes", [])),
            "secondary_outcomes": self._extract_outcomes(outcomes.get("secondaryOutcomes", [])),

            # Eligibility
            "min_age": eligibility.get("minimumAge", ""),
            "max_age": eligibility.get("maximumAge", ""),
            "sex": eligibility.get("sex", ""),
            "criteria": eligibility.get("eligibilityCriteria", ""),

            # Metadata
            "data_source": "ClinicalTrials.gov",
            "extraction_date": datetime.now().isoformat()
        }

        return trial

    def _extract_interventions(self, interventions: List[Dict]) -> List[Dict]:
        """
        Extract intervention details.

        Args:
            interventions: List of intervention dictionaries

        Returns:
            Processed intervention list
        """
        processed = []
        for intervention in interventions:
            processed.append({
                "type": intervention.get("type", ""),
                "name": intervention.get("name", ""),
                "description": intervention.get("description", ""),
                "other_names": intervention.get("otherNames", [])
            })
        return processed

    def _extract_outcomes(self, outcomes: List[Dict]) -> List[Dict]:
        """
        Extract outcome measures.

        Args:
            outcomes: List of outcome dictionaries

        Returns:
            Processed outcome list
        """
        processed = []
        for outcome in outcomes:
            processed.append({
                "measure": outcome.get("measure", ""),
                "description": outcome.get("description", ""),
                "time_frame": outcome.get("timeFrame", "")
            })
        return processed

    def fetch_detailed_trial(self, nct_id: str) -> Optional[Dict]:
        """
        Fetch detailed information for a specific trial.

        Args:
            nct_id: NCT identifier

        Returns:
            Detailed trial dictionary or None if error
        """
        logger.info(f"Fetching detailed data for {nct_id}")

        endpoint = f"{self.api_url}/studies/{nct_id}"

        try:
            response = requests.get(endpoint, timeout=30)
            response.raise_for_status()

            data = response.json()
            protocol = data.get("protocolSection", {})
            results = data.get("resultsSection", {})

            # Extract comprehensive information
            detailed_trial = self._extract_trial_summary(protocol)

            # Add results if available
            if results:
                detailed_trial["has_results"] = True
                detailed_trial["results"] = self._extract_results(results)
            else:
                detailed_trial["has_results"] = False

            time.sleep(self.rate_limit)

            return detailed_trial

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error fetching {nct_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing {nct_id}: {e}")
            return None

    def _extract_results(self, results: Dict) -> Dict:
        """
        Extract results section data.

        Args:
            results: Results section dictionary

        Returns:
            Processed results dictionary
        """
        participant_flow = results.get("participantFlowModule", {})
        baseline = results.get("baselineCharacteristicsModule", {})
        outcome_measures = results.get("outcomeMeasuresModule", {})

        return {
            "participant_flow": participant_flow,
            "baseline_measures": baseline.get("measures", []),
            "outcome_measures": outcome_measures.get("outcomeMeasures", [])
        }

    def save_to_json(self, trials: List[Dict], output_path: str):
        """
        Save trials to JSON file.

        Args:
            trials: List of trial dictionaries
            output_path: Path to output JSON file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(trials, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(trials)} trials to {output_path}")

    def collect_cardiology_trials(
        self,
        output_dir: str = "./data/raw/clinicaltrials",
        min_enrollment: int = 50,
        max_results: int = 1000,
        fetch_detailed: bool = False
    ):
        """
        Full pipeline to collect cardiology trials.

        Args:
            output_dir: Directory to save output files
            min_enrollment: Minimum enrollment size
            max_results: Maximum results per condition
            fetch_detailed: Whether to fetch detailed data for each trial
        """
        logger.info("=" * 80)
        logger.info("STARTING CLINICALTRIALS.GOV CARDIOLOGY DATA COLLECTION")
        logger.info("=" * 80)

        # Search for trials
        trials = self.search_cardiology_trials(
            min_enrollment=min_enrollment,
            max_results=max_results
        )

        if not trials:
            logger.warning("No trials found!")
            return

        # Optionally fetch detailed information
        if fetch_detailed:
            logger.info("Fetching detailed information for each trial...")
            detailed_trials = []

            for trial in trials:
                nct_id = trial.get("nct_id")
                if nct_id:
                    detailed = self.fetch_detailed_trial(nct_id)
                    if detailed:
                        detailed_trials.append(detailed)

            trials = detailed_trials

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_dir}/cardiology_trials_{timestamp}.json"
        self.save_to_json(trials, output_path)

        logger.info("=" * 80)
        logger.info(f"COLLECTION COMPLETE: {len(trials)} trials saved")
        logger.info("=" * 80)


def main():
    """
    Example usage of ClinicalTrials.gov collector.
    """
    # Initialize collector
    collector = ClinicalTrialsCollector()

    # Collect cardiology trials
    collector.collect_cardiology_trials(
        output_dir="./data/raw/clinicaltrials",
        min_enrollment=100,
        max_results=500,  # Per condition
        fetch_detailed=False  # Set to True for complete data (slower)
    )


if __name__ == "__main__":
    main()
