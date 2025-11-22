#!/usr/bin/env python3
"""
Create Master Combined Dataset from All Phases

This script combines all phase datasets into a single master cardiovascular
meta-analysis database containing 861 trials across 19 phases.

Author: Research Team
Date: November 2025
"""

import pandas as pd
from pathlib import Path


def create_master_dataset():
    """Combine all phase datasets into master database."""

    base_dir = Path(__file__).parent.parent.parent
    data_dir = base_dir / "data" / "raw"
    output_dir = base_dir / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("CREATING MASTER CARDIOVASCULAR META-ANALYSIS DATABASE")
    print("=" * 80)
    print()

    # Define all phase combined files
    phase_files = [
        "phase1_expansion/phase1_combined.csv",
        "phase2_expansion/phase2_all_combined.csv",
        "phase3_expansion/phase3_all_combined.csv",
        "phase4_expansion/phase4_devices_combined.csv",
        "phase4_expansion/phase4_coronary_interventions_combined.csv",
        "phase4_expansion/phase4_antiinflammatory_combined.csv",
        "phase4_expansion/phase4_historical_combined.csv",
        "phase5_expansion/phase5_ckd_combined.csv",
        "phase6_expansion/phase6_arrhythmias_combined.csv",
        "phase7_expansion/phase7_preventive_combined.csv",
        "phase8_expansion/phase8_cardiomyopathies_combined.csv",
        "phase9_expansion/phase9_combined.csv",
        "phase10_expansion/phase10_combined.csv",
        "phase11_emerging/phase11_combined.csv",
        "phase12_specialized/phase12_combined.csv",
        "phase13_imaging/phase13_combined.csv",
        "phase14_rare_conditions/phase14_combined.csv",
        "phase15_quality_systems/phase15_combined.csv",
        "phase16_additional_domains/phase16_combined.csv",
        "phase17_additional_domains2/phase17_combined.csv",
        "phase18_additional_domains3/phase18_combined.csv",
        "phase19_additional_domains4/phase19_combined.csv",
    ]

    # Read and combine all phases
    all_phases = []
    total_trials = 0
    total_patients = 0

    for i, phase_file in enumerate(phase_files, 1):
        file_path = data_dir / phase_file
        if file_path.exists():
            df = pd.read_csv(file_path)
            phase_name = phase_file.split('/')[0].replace('_expansion', '').replace('_', ' ').title()

            trials = len(df)
            patients = df['n_intervention'].sum() + df['n_control'].sum()

            print(f"Phase {i}: {phase_name}")
            print(f"  Trials: {trials:,}")
            print(f"  Patients: {patients:,}")
            print(f"  File: {phase_file}")
            print()

            all_phases.append(df)
            total_trials += trials
            total_patients += patients
        else:
            print(f"WARNING: {file_path} not found")
            print()

    # Combine all phases
    print("=" * 80)
    print("COMBINING ALL PHASES")
    print("=" * 80)
    print()

    master_df = pd.concat(all_phases, ignore_index=True)

    print(f"✓ Total trials: {total_trials:,}")
    print(f"✓ Total patients: {total_patients:,}")
    print(f"✓ Date range: {master_df['year'].min():.0f} - {master_df['year'].max():.0f}")
    print()

    # Save master dataset
    master_file = output_dir / f"master_cardiovascular_metaanalysis_{total_trials}trials.csv"
    master_df.to_csv(master_file, index=False)
    print(f"✓ Saved master dataset: {master_file}")
    print()

    # Create summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()

    print("By Category:")
    print(master_df['category'].value_counts().head(20))
    print()

    print("By Decade:")
    master_df['decade'] = (master_df['year'] // 10) * 10
    print(master_df['decade'].value_counts().sort_index())
    print()

    print("Patient Characteristics:")
    print(f"  Mean age: {master_df['mean_age'].mean():.1f} years")
    print(f"  % Male: {master_df['pct_male'].mean():.1f}%")
    print(f"  Mean follow-up: {master_df['mean_followup_months'].mean():.1f} months")
    print()

    # Save summary
    summary_file = output_dir / "master_dataset_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("MASTER CARDIOVASCULAR META-ANALYSIS DATABASE\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Trials: {total_trials:,}\n")
        f.write(f"Total Patients: {total_patients:,}\n")
        f.write(f"Date Range: {master_df['year'].min():.0f} - {master_df['year'].max():.0f}\n")
        f.write(f"\nCategories: {master_df['category'].nunique()}\n")
        f.write(f"Interventions: {master_df['intervention'].nunique()}\n")
        f.write(f"\nMean Age: {master_df['mean_age'].mean():.1f} years\n")
        f.write(f"% Male: {master_df['pct_male'].mean():.1f}%\n")
        f.write(f"Mean Follow-up: {master_df['mean_followup_months'].mean():.1f} months\n")

    print(f"✓ Saved summary: {summary_file}")
    print()

    print("=" * 80)
    print("MASTER DATABASE CREATION COMPLETE!")
    print("=" * 80)
    print()
    print(f"File: {master_file}")
    print(f"Size: {len(master_df):,} trials")
    print(f"Columns: {', '.join(master_df.columns)}")
    print()

    return master_df


if __name__ == "__main__":
    create_master_dataset()
