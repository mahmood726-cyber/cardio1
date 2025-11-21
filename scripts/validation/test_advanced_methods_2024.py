"""
Test Advanced Meta-Analysis Methods (2024-2025) on All Datasets

Tests cutting-edge methods from recent literature:
1. Robust outlier methods (Noma et al. 2024)
2. Selection models for publication bias (Bartoš et al. 2024)

Compares standard vs advanced methods across 12 cardiology datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.analysis.advanced_methods_2024 import (
    RobustOutlierMetaAnalysis,
    PublicationBiasSelectionModel,
    compare_methods_on_dataset
)


def load_all_datasets():
    """Load all validation datasets."""
    data_dir = Path('data/raw/validation_datasets')
    sample_dir = Path('data/raw/sample_metaanalysis')

    datasets = {}

    # Validation datasets
    for csv_file in data_dir.glob('*.csv'):
        name = csv_file.stem
        df = pd.read_csv(csv_file)
        datasets[name] = df

    # Sample beta-blocker dataset
    bb_file = sample_dir / 'beta_blockers_hf_mortality.csv'
    if bb_file.exists():
        datasets['beta_blockers_hf'] = pd.read_csv(bb_file)

    return datasets


def test_robust_methods_on_dataset(df, dataset_name):
    """Test robust outlier methods on a dataset."""
    print(f"\n{'='*80}")
    print(f"DATASET: {dataset_name}")
    print(f"{'='*80}")

    effect_sizes = df['log_rr'].values
    se = df['se_log_rr'].values
    variances = se ** 2

    n_studies = len(df)
    total_patients = df['n_intervention'].sum() + df['n_control'].sum()

    print(f"Studies: {n_studies}")
    print(f"Total patients: {total_patients:,}")
    print()

    # Standard meta-analysis
    weights = 1 / variances
    w_sum = np.sum(weights)
    standard_rr = np.exp(np.sum(weights * effect_sizes) / w_sum)

    print(f"Standard RR: {standard_rr:.3f}")

    # Robust meta-analysis
    robust_ma = RobustOutlierMetaAnalysis()
    robust_result = robust_ma.robust_meta_analysis(effect_sizes, variances)

    robust_rr = np.exp(robust_result.effect_size)
    print(f"Robust RR: {robust_rr:.3f}")
    print(f"Difference: {abs(robust_rr - standard_rr):.3f} ({abs(robust_rr - standard_rr) / standard_rr * 100:.1f}%)")

    # Outlier detection
    if robust_result.outliers_detected:
        print(f"\nOUTLIERS DETECTED: {len(robust_result.outliers_detected)}")
        for idx in robust_result.outliers_detected:
            study_id = df.iloc[idx]['study_id'] if 'study_id' in df.columns else f"Study {idx}"
            weight = robust_result.outlier_weights[idx]
            print(f"  - {study_id}: weight = {weight:.2f}")
    else:
        print("\nNo outliers detected")

    # Publication bias
    if n_studies >= 5:  # Need minimum studies for selection model
        selection_ma = PublicationBiasSelectionModel()
        selection_result = selection_ma.simple_selection_model(effect_sizes, variances)

        print(f"\nPUBLICATION BIAS ASSESSMENT:")
        print(f"  Unadjusted RR: {np.exp(selection_result.unadjusted_effect):.3f}")
        print(f"  Adjusted RR: {np.exp(selection_result.adjusted_effect):.3f}")
        print(f"  Selection probability (ρ): {selection_result.selection_probability:.2f}")
        print(f"  Bias severity: {selection_result.bias_severity}")
        print(f"  Egger's test p-value: {selection_result.egger_p:.3f}")

    # Heterogeneity
    print(f"\nHETEROGENEITY:")
    print(f"  τ²: {robust_result.tau_squared:.3f}")
    print(f"  I²: {robust_result.i_squared:.1f}%")
    print(f"  Q: {robust_result.q_statistic:.2f} (p={robust_result.p_value:.3f})")

    return {
        'dataset': dataset_name,
        'n_studies': n_studies,
        'n_patients': total_patients,
        'standard_rr': standard_rr,
        'robust_rr': robust_rr,
        'diff_pct': abs(robust_rr - standard_rr) / standard_rr * 100,
        'n_outliers': len(robust_result.outliers_detected),
        'i_squared': robust_result.i_squared,
        'tau_squared': robust_result.tau_squared,
    }


def main():
    """Run comprehensive testing of advanced methods."""
    print("=" * 80)
    print("TESTING ADVANCED META-ANALYSIS METHODS (2024-2025)")
    print("=" * 80)
    print("\nMethods tested:")
    print("1. Robust outlier detection (Noma et al., Statistics in Medicine 2024)")
    print("2. Selection models for publication bias (Bartoš et al., RSM 2024)")
    print()

    # Load datasets
    datasets = load_all_datasets()

    print(f"Loaded {len(datasets)} datasets")
    print()

    # Test each dataset
    results = []
    for name, df in sorted(datasets.items()):
        try:
            result = test_robust_methods_on_dataset(df, name)
            results.append(result)
        except Exception as e:
            print(f"Error processing {name}: {e}")

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY OF RESULTS")
    print("=" * 80)

    results_df = pd.DataFrame(results)

    print("\nMethod Comparison Across All Datasets:")
    print(results_df[['dataset', 'n_studies', 'standard_rr', 'robust_rr', 'diff_pct', 'n_outliers']].to_string(index=False))

    print(f"\n\nOverall Statistics:")
    print(f"  Total datasets: {len(results_df)}")
    print(f"  Total studies: {results_df['n_studies'].sum()}")
    print(f"  Total patients: {results_df['n_patients'].sum():,}")
    print(f"  Datasets with outliers: {(results_df['n_outliers'] > 0).sum()}")
    print(f"  Mean |difference| in RR: {results_df['diff_pct'].mean():.2f}%")
    print(f"  Max |difference| in RR: {results_df['diff_pct'].max():.2f}%")

    # Identify datasets where methods disagree substantially
    print(f"\n\nDatasets with Substantial Method Disagreement (>5% difference):")
    substantial_diff = results_df[results_df['diff_pct'] > 5.0]
    if len(substantial_diff) > 0:
        for _, row in substantial_diff.iterrows():
            print(f"  - {row['dataset']}: {row['diff_pct']:.1f}% difference")
    else:
        print("  None (excellent agreement)")

    # Save results
    output_file = Path('data/processed/validation_results/advanced_methods_comparison.csv')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_file, index=False)
    print(f"\n\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
