"""
Download and Integrate Large Cardiovascular Datasets

This script downloads and prepares large cardiovascular datasets for integration:
1. Kaggle Cardiovascular Disease Dataset (70,000 patients)
2. Other open-access cardiovascular datasets
3. Converts patient-level data to summary statistics for meta-analysis

Note: For Kaggle datasets, you'll need to:
1. Install kaggle: pip install kaggle
2. Set up Kaggle API credentials: https://www.kaggle.com/docs/api
3. Place kaggle.json in ~/.kaggle/ directory
"""

import pandas as pd
import numpy as np
from pathlib import Path
import subprocess
import warnings


class LargeDatasetDownloader:
    """Download and process large cardiovascular datasets."""

    def __init__(self):
        self.output_dir = Path('data/raw/large_datasets')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_kaggle_cardiovascular_70k(self):
        """
        Download Kaggle Cardiovascular Disease Dataset (70,000 patients).

        Dataset: sulianova/cardiovascular-disease-dataset
        Features: age, gender, height, weight, ap_hi, ap_lo, cholesterol,
                  gluc, smoke, alco, active, cardio (target)
        """
        print("=" * 80)
        print("DOWNLOADING KAGGLE CARDIOVASCULAR DATASET (70K PATIENTS)")
        print("=" * 80)

        kaggle_dataset = "sulianova/cardiovascular-disease-dataset"
        output_path = self.output_dir / "kaggle_cardio_70k"
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\nDataset: {kaggle_dataset}")
        print(f"Output: {output_path}")

        # Check if kaggle is installed
        try:
            subprocess.run(['kaggle', '--version'], capture_output=True, check=True)
            print("\n✓ Kaggle CLI installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("\n✗ Kaggle CLI not installed")
            print("\nTo install:")
            print("  pip install kaggle")
            print("\nThen set up API credentials:")
            print("  1. Go to https://www.kaggle.com/account")
            print("  2. Click 'Create New API Token'")
            print("  3. Place kaggle.json in ~/.kaggle/")
            print("  4. chmod 600 ~/.kaggle/kaggle.json")
            return None

        # Download dataset
        try:
            print("\nDownloading dataset (this may take a few minutes)...")
            cmd = ['kaggle', 'datasets', 'download', '-d', kaggle_dataset,
                   '-p', str(output_path), '--unzip']
            subprocess.run(cmd, check=True)
            print("✓ Download complete")

            # Find the CSV file
            csv_files = list(output_path.glob('*.csv'))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                print(f"\n✓ Loaded dataset: {len(df):,} records")
                print(f"  Columns: {', '.join(df.columns.tolist())}")
                print(f"  CVD positive: {df['cardio'].sum():,} ({df['cardio'].mean():.1%})")
                print(f"  CVD negative: {(df['cardio']==0).sum():,}")

                return df
            else:
                print("✗ No CSV file found after download")
                return None

        except subprocess.CalledProcessError as e:
            print(f"\n✗ Error downloading: {e}")
            print("\nMake sure you have:")
            print("  1. Kaggle API credentials set up")
            print("  2. Accepted the dataset terms on Kaggle website")
            return None

    def create_summary_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert patient-level data to summary statistics.

        For meta-analysis, we need aggregate statistics by subgroups.
        """
        print("\n" + "=" * 80)
        print("CREATING SUMMARY STATISTICS FOR META-ANALYSIS")
        print("=" * 80)

        # Age groups
        df['age_group'] = pd.cut(df['age'] / 365, bins=[0, 40, 50, 60, 70, 100],
                                  labels=['<40', '40-49', '50-59', '60-69', '70+'])

        # Gender
        df['gender_label'] = df['gender'].map({1: 'Female', 2: 'Male'})

        # BMI
        df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
        df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, 100],
                                      labels=['Underweight', 'Normal', 'Overweight', 'Obese'])

        # Hypertension
        df['hypertension'] = ((df['ap_hi'] >= 140) | (df['ap_lo'] >= 90)).astype(int)

        # Create summary by subgroups
        summaries = []

        for group_var in ['age_group', 'gender_label', 'bmi_category']:
            for group_val in df[group_var].dropna().unique():
                subset = df[df[group_var] == group_val]

                n_total = len(subset)
                n_cvd = subset['cardio'].sum()
                n_no_cvd = n_total - n_cvd

                # Calculate risk ratio vs overall population
                risk_group = n_cvd / n_total
                risk_overall = df['cardio'].mean()
                rr = risk_group / risk_overall if risk_overall > 0 else 1.0

                summaries.append({
                    'subgroup_variable': group_var,
                    'subgroup_value': group_val,
                    'n_total': n_total,
                    'n_cvd': n_cvd,
                    'n_no_cvd': n_no_cvd,
                    'prevalence_cvd': risk_group,
                    'risk_ratio_vs_overall': rr,
                    'log_rr': np.log(rr),
                    'se_log_rr': np.sqrt(1/n_cvd + 1/n_no_cvd - 1/n_total)
                })

        summary_df = pd.DataFrame(summaries)

        # Save summary
        output_file = self.output_dir / "kaggle_cardio_70k_summary.csv"
        summary_df.to_csv(output_file, index=False)

        print(f"\n✓ Summary statistics created")
        print(f"  Subgroups: {len(summary_df)}")
        print(f"  Saved to: {output_file}")

        return summary_df

    def download_and_process_all(self):
        """Download and process all large datasets."""
        print("\n" + "=" * 80)
        print("LARGE CARDIOVASCULAR DATASET DOWNLOADER")
        print("=" * 80)
        print("\nThis script will download and process:")
        print("  1. Kaggle Cardiovascular Dataset (70K patients)")
        print("  2. Convert to meta-analysis summary statistics")
        print()

        # Download Kaggle dataset
        df_kaggle = self.download_kaggle_cardiovascular_70k()

        if df_kaggle is not None:
            # Create summary statistics
            summary_df = self.create_summary_statistics(df_kaggle)

            print("\n" + "=" * 80)
            print("SUMMARY")
            print("=" * 80)
            print(f"\n✓ Downloaded: {len(df_kaggle):,} patient records")
            print(f"✓ Created: {len(summary_df)} subgroup summaries")
            print(f"✓ Data saved to: {self.output_dir}")

            return df_kaggle, summary_df
        else:
            print("\n" + "=" * 80)
            print("DOWNLOAD FAILED")
            print("=" * 80)
            print("\nPlease:")
            print("  1. Install Kaggle CLI: pip install kaggle")
            print("  2. Set up API credentials: https://www.kaggle.com/docs/api")
            print("  3. Run this script again")

            return None, None


def main():
    """Main execution."""
    downloader = LargeDatasetDownloader()
    downloader.download_and_process_all()


if __name__ == "__main__":
    main()
