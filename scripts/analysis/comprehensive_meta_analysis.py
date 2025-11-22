#!/usr/bin/env python3
"""
Comprehensive Meta-Analysis of 1001 Cardiovascular Trials
==========================================================

This script performs meta-analyses on the complete cardiovascular database:
- Overall meta-analysis across all 1001 trials
- Subgroup analyses by category
- Subgroup analyses by decade
- Heterogeneity assessment (I², tau²)
- Publication bias assessment (funnel plots, Egger's test)
- Forest plots for major categories
- Summary statistics and visualizations

Author: Research Team
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def calculate_pooled_effect(log_rr, se_log_rr, method='random'):
    """
    Calculate pooled effect size using inverse-variance weighting

    Parameters:
    -----------
    log_rr : array-like
        Log risk ratios
    se_log_rr : array-like
        Standard errors of log risk ratios
    method : str
        'fixed' or 'random' effects model

    Returns:
    --------
    dict with pooled estimate, CI, heterogeneity stats
    """
    # Remove invalid values
    valid = ~(np.isnan(log_rr) | np.isnan(se_log_rr) | np.isinf(log_rr) | np.isinf(se_log_rr))
    log_rr = np.array(log_rr)[valid]
    se_log_rr = np.array(se_log_rr)[valid]

    if len(log_rr) < 2:
        return None

    # Calculate weights (inverse variance)
    weights = 1 / (se_log_rr ** 2)

    # Fixed-effect estimate
    pooled_log_rr_fixed = np.sum(weights * log_rr) / np.sum(weights)
    se_pooled_fixed = np.sqrt(1 / np.sum(weights))

    # Calculate Q statistic for heterogeneity
    Q = np.sum(weights * (log_rr - pooled_log_rr_fixed) ** 2)
    df = len(log_rr) - 1
    p_heterogeneity = 1 - stats.chi2.cdf(Q, df)

    # Calculate I² (percentage of variance due to heterogeneity)
    I2 = max(0, 100 * (Q - df) / Q) if Q > 0 else 0

    # Calculate tau² (between-study variance)
    C = np.sum(weights) - np.sum(weights**2) / np.sum(weights)
    tau2 = max(0, (Q - df) / C) if C > 0 else 0

    # Random-effects estimate (DerSimonian-Laird)
    if method == 'random':
        weights_random = 1 / (se_log_rr ** 2 + tau2)
        pooled_log_rr = np.sum(weights_random * log_rr) / np.sum(weights_random)
        se_pooled = np.sqrt(1 / np.sum(weights_random))
    else:
        pooled_log_rr = pooled_log_rr_fixed
        se_pooled = se_pooled_fixed

    # Convert to RR scale
    pooled_rr = np.exp(pooled_log_rr)
    ci_lower = np.exp(pooled_log_rr - 1.96 * se_pooled)
    ci_upper = np.exp(pooled_log_rr + 1.96 * se_pooled)

    # Z-test and p-value
    z = pooled_log_rr / se_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        'n_trials': len(log_rr),
        'pooled_rr': pooled_rr,
        'pooled_log_rr': pooled_log_rr,
        'se_pooled': se_pooled,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'z_score': z,
        'p_value': p_value,
        'Q': Q,
        'df': df,
        'p_heterogeneity': p_heterogeneity,
        'I2': I2,
        'tau2': tau2
    }

def egger_test(log_rr, se_log_rr):
    """
    Egger's test for publication bias
    Tests whether there's a relationship between effect size and precision
    """
    valid = ~(np.isnan(log_rr) | np.isnan(se_log_rr) | np.isinf(log_rr) | np.isinf(se_log_rr))
    log_rr = np.array(log_rr)[valid]
    se_log_rr = np.array(se_log_rr)[valid]

    if len(log_rr) < 3:
        return None

    # Precision (1/SE)
    precision = 1 / se_log_rr

    # Regression: effect size ~ precision
    slope, intercept, r_value, p_value, std_err = stats.linregress(precision, log_rr)

    return {
        'slope': slope,
        'intercept': intercept,
        'p_value': p_value,
        'significant_bias': p_value < 0.05
    }

def create_forest_plot(df, title, filename, top_n=20):
    """Create forest plot for top categories"""

    fig, ax = plt.subplots(figsize=(14, max(8, top_n * 0.4)))

    # Sort by number of trials and take top N
    df_sorted = df.nsmallest(top_n, 'pooled_rr')

    y_pos = np.arange(len(df_sorted))

    # Plot point estimates
    ax.scatter(df_sorted['pooled_rr'], y_pos, s=100, color='darkblue', zorder=3, alpha=0.8)

    # Plot confidence intervals
    for i, row in df_sorted.iterrows():
        ax.plot([row['ci_lower'], row['ci_upper']], [y_pos[df_sorted.index.get_loc(i)], y_pos[df_sorted.index.get_loc(i)]],
                'b-', linewidth=2, alpha=0.6)

    # Add vertical line at RR = 1 (no effect)
    ax.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='No effect (RR=1)')

    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{idx}\n(n={row['n_trials']})" for idx, row in df_sorted.iterrows()], fontsize=9)
    ax.set_xlabel('Risk Ratio (95% CI)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0.5, 1.5)
    ax.grid(axis='x', alpha=0.3)
    ax.legend(fontsize=10)

    # Add I² values as text
    for i, row in df_sorted.iterrows():
        x_pos = row['ci_upper'] + 0.05
        ax.text(x_pos, y_pos[df_sorted.index.get_loc(i)], f"I²={row['I2']:.0f}%",
                fontsize=8, va='center', color='darkgreen')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Saved forest plot: {filename}")

def create_funnel_plot(log_rr, se_log_rr, title, filename):
    """Create funnel plot for publication bias assessment"""

    # Remove invalid values
    valid = ~(np.isnan(log_rr) | np.isnan(se_log_rr) | np.isinf(log_rr) | np.isinf(se_log_rr))
    log_rr_clean = np.array(log_rr)[valid]
    se_log_rr_clean = np.array(se_log_rr)[valid]

    if len(log_rr_clean) < 10:
        return

    fig, ax = plt.subplots(figsize=(10, 8))

    # Scatter plot (inverted y-axis: smaller SE at top)
    ax.scatter(log_rr_clean, se_log_rr_clean, alpha=0.5, s=30, color='steelblue')

    # Add pooled estimate line
    pooled = calculate_pooled_effect(log_rr_clean, se_log_rr_clean, method='random')
    if pooled:
        ax.axvline(x=pooled['pooled_log_rr'], color='red', linestyle='--', linewidth=2, label='Pooled effect')

    # Add pseudo 95% CI lines
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.3, label='No effect')

    # Formatting
    ax.set_xlabel('Log Risk Ratio', fontsize=12, fontweight='bold')
    ax.set_ylabel('Standard Error', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()  # Smaller SE at top
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Saved funnel plot: {filename}")

def main():
    """Main analysis pipeline"""

    print("\n" + "="*80)
    print("COMPREHENSIVE META-ANALYSIS: 1001 CARDIOVASCULAR TRIALS")
    print("="*80 + "\n")

    # Load master dataset
    data_file = Path("data/processed/master_cardiovascular_metaanalysis_1001trials.csv")

    if not data_file.exists():
        print(f"ERROR: Master dataset not found at {data_file}")
        return

    df = pd.read_csv(data_file)

    # Add decade column if not present
    if 'decade' not in df.columns:
        df['decade'] = (df['year'] // 10) * 10

    # Calculate confidence intervals for individual trials if not present
    if 'ci_lower' not in df.columns:
        df['ci_lower'] = np.exp(df['log_rr'] - 1.96 * df['se_log_rr'])
        df['ci_upper'] = np.exp(df['log_rr'] + 1.96 * df['se_log_rr'])

    print(f"✓ Loaded {len(df)} trials from master dataset")
    print(f"✓ Total patients: {df['n_intervention'].sum() + df['n_control'].sum():,}")
    print(f"✓ Date range: {df['year'].min()} - {df['year'].max()}")
    print()

    # Create output directory
    output_dir = Path("data/analysis/meta_analysis_results")
    output_dir.mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # 1. OVERALL META-ANALYSIS
    # ========================================================================
    print("="*80)
    print("1. OVERALL META-ANALYSIS (ALL 1001 TRIALS)")
    print("="*80)

    overall = calculate_pooled_effect(df['log_rr'], df['se_log_rr'], method='random')

    if overall:
        print(f"\nRandom-Effects Model:")
        print(f"  Number of trials: {overall['n_trials']}")
        print(f"  Pooled RR: {overall['pooled_rr']:.3f} (95% CI: {overall['ci_lower']:.3f} - {overall['ci_upper']:.3f})")
        print(f"  Z-score: {overall['z_score']:.3f}")
        print(f"  P-value: {overall['p_value']:.6f}")
        print(f"\nHeterogeneity Statistics:")
        print(f"  Q statistic: {overall['Q']:.2f} (df={overall['df']})")
        print(f"  P-heterogeneity: {overall['p_heterogeneity']:.6f}")
        print(f"  I² (variance due to heterogeneity): {overall['I2']:.1f}%")
        print(f"  τ² (between-study variance): {overall['tau2']:.4f}")

        if overall['I2'] > 75:
            print(f"  → High heterogeneity detected (I² > 75%)")
        elif overall['I2'] > 50:
            print(f"  → Moderate heterogeneity detected (I² > 50%)")
        else:
            print(f"  → Low heterogeneity (I² < 50%)")

    # Publication bias assessment
    print(f"\nPublication Bias Assessment:")
    egger = egger_test(df['log_rr'], df['se_log_rr'])
    if egger:
        print(f"  Egger's test p-value: {egger['p_value']:.4f}")
        if egger['significant_bias']:
            print(f"  → Significant publication bias detected (p < 0.05)")
        else:
            print(f"  → No significant publication bias detected")

    # Create overall funnel plot
    create_funnel_plot(df['log_rr'], df['se_log_rr'],
                      "Funnel Plot: All 1001 Trials",
                      output_dir / "funnel_plot_overall.png")

    # ========================================================================
    # 2. META-ANALYSIS BY CATEGORY
    # ========================================================================
    print("\n" + "="*80)
    print("2. SUBGROUP META-ANALYSIS BY CATEGORY")
    print("="*80 + "\n")

    category_results = []

    for category in df['category'].value_counts().head(30).index:
        df_cat = df[df['category'] == category]
        result = calculate_pooled_effect(df_cat['log_rr'], df_cat['se_log_rr'], method='random')

        if result and result['n_trials'] >= 3:
            result['category'] = category
            category_results.append(result)

            print(f"{category} (n={result['n_trials']} trials):")
            print(f"  Pooled RR: {result['pooled_rr']:.3f} (95% CI: {result['ci_lower']:.3f} - {result['ci_upper']:.3f})")
            print(f"  I²: {result['I2']:.1f}%, τ²: {result['tau2']:.4f}, p={result['p_value']:.4f}")
            print()

    # Convert to DataFrame and save
    df_categories = pd.DataFrame(category_results)
    if len(df_categories) > 0:
        df_categories = df_categories.sort_values('n_trials', ascending=False)
        df_categories.to_csv(output_dir / "meta_analysis_by_category.csv", index=False)
        print(f"✓ Saved category meta-analysis results: {output_dir / 'meta_analysis_by_category.csv'}")

        # Create forest plot for top categories
        create_forest_plot(df_categories.set_index('category'),
                          "Forest Plot: Meta-Analysis by Category (Top 20)",
                          output_dir / "forest_plot_by_category.png",
                          top_n=20)

    # ========================================================================
    # 3. META-ANALYSIS BY DECADE
    # ========================================================================
    print("\n" + "="*80)
    print("3. TEMPORAL TRENDS: META-ANALYSIS BY DECADE")
    print("="*80 + "\n")

    decade_results = []

    for decade in sorted(df['decade'].unique()):
        df_decade = df[df['decade'] == decade]
        result = calculate_pooled_effect(df_decade['log_rr'], df_decade['se_log_rr'], method='random')

        if result:
            result['decade'] = decade
            decade_results.append(result)

            print(f"{decade}s (n={result['n_trials']} trials):")
            print(f"  Pooled RR: {result['pooled_rr']:.3f} (95% CI: {result['ci_lower']:.3f} - {result['ci_upper']:.3f})")
            print(f"  I²: {result['I2']:.1f}%, p={result['p_value']:.4f}")
            print()

    # Convert to DataFrame and save
    df_decades = pd.DataFrame(decade_results)
    if len(df_decades) > 0:
        df_decades = df_decades.sort_values('decade')
        df_decades.to_csv(output_dir / "meta_analysis_by_decade.csv", index=False)
        print(f"✓ Saved decade meta-analysis results: {output_dir / 'meta_analysis_by_decade.csv'}")

        # Create temporal trend plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Plot 1: Pooled RR over time
        ax1.errorbar(df_decades['decade'], df_decades['pooled_rr'],
                    yerr=[df_decades['pooled_rr'] - df_decades['ci_lower'],
                          df_decades['ci_upper'] - df_decades['pooled_rr']],
                    marker='o', markersize=10, linewidth=2, capsize=5, capthick=2,
                    color='darkblue', label='Pooled RR')
        ax1.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='No effect')
        ax1.set_xlabel('Decade', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Pooled Risk Ratio (95% CI)', fontsize=12, fontweight='bold')
        ax1.set_title('Temporal Trends in Treatment Effects', fontsize=14, fontweight='bold')
        ax1.grid(alpha=0.3)
        ax1.legend(fontsize=10)

        # Plot 2: I² heterogeneity over time
        ax2.bar(df_decades['decade'], df_decades['I2'], color='steelblue', alpha=0.7, edgecolor='black')
        ax2.axhline(y=50, color='orange', linestyle='--', linewidth=2, label='Moderate heterogeneity')
        ax2.axhline(y=75, color='red', linestyle='--', linewidth=2, label='High heterogeneity')
        ax2.set_xlabel('Decade', fontsize=12, fontweight='bold')
        ax2.set_ylabel('I² (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Heterogeneity Trends Over Time', fontsize=14, fontweight='bold')
        ax2.grid(alpha=0.3, axis='y')
        ax2.legend(fontsize=10)

        plt.tight_layout()
        plt.savefig(output_dir / "temporal_trends.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved temporal trends plot: {output_dir / 'temporal_trends.png'}")

    # ========================================================================
    # 4. SUMMARY STATISTICS
    # ========================================================================
    print("\n" + "="*80)
    print("4. SUMMARY STATISTICS")
    print("="*80 + "\n")

    summary_stats = {
        'Total Trials': len(df),
        'Total Patients': int(df['n_intervention'].sum() + df['n_control'].sum()),
        'Date Range': f"{df['year'].min()}-{df['year'].max()}",
        'Mean Age': f"{df['mean_age'].mean():.1f} years",
        'Percent Male': f"{df['pct_male'].mean():.1f}%",
        'Mean Follow-up': f"{df['mean_followup_months'].mean():.1f} months",
        'Number of Categories': df['category'].nunique(),
        'Number of Decades': df['decade'].nunique(),
        'Overall Pooled RR': f"{overall['pooled_rr']:.3f} ({overall['ci_lower']:.3f}-{overall['ci_upper']:.3f})" if overall else 'N/A',
        'Overall I²': f"{overall['I2']:.1f}%" if overall else 'N/A',
        'Egger Test P-value': f"{egger['p_value']:.4f}" if egger else 'N/A'
    }

    for key, value in summary_stats.items():
        print(f"  {key}: {value}")

    # Save summary statistics
    pd.Series(summary_stats).to_csv(output_dir / "summary_statistics.csv")
    print(f"\n✓ Saved summary statistics: {output_dir / 'summary_statistics.csv'}")

    # ========================================================================
    # 5. TOP FINDINGS
    # ========================================================================
    print("\n" + "="*80)
    print("5. TOP FINDINGS BY EFFECT SIZE")
    print("="*80 + "\n")

    # Beneficial treatments (RR < 1, significant)
    df_beneficial = df[(df['rr'] < 1) & (df['ci_upper'] < 1)].nsmallest(10, 'rr')[['study_id', 'category', 'rr', 'ci_lower', 'ci_upper', 'notes']]
    print("Top 10 Most Beneficial Interventions (RR < 1, significant):")
    for idx, row in df_beneficial.iterrows():
        print(f"\n  {row['study_id']} - {row['category']}")
        print(f"    RR: {row['rr']:.3f} (95% CI: {row['ci_lower']:.3f}-{row['ci_upper']:.3f})")
        print(f"    {row['notes'][:100]}...")

    # Harmful treatments (RR > 1, significant)
    df_harmful = df[(df['rr'] > 1) & (df['ci_lower'] > 1)].nlargest(10, 'rr')[['study_id', 'category', 'rr', 'ci_lower', 'ci_upper', 'notes']]
    print(f"\n\nTop 10 Harmful/Ineffective Interventions (RR > 1, significant):")
    for idx, row in df_harmful.iterrows():
        print(f"\n  {row['study_id']} - {row['category']}")
        print(f"    RR: {row['rr']:.3f} (95% CI: {row['ci_lower']:.3f}-{row['ci_upper']:.3f})")
        print(f"    {row['notes'][:100]}...")

    print("\n" + "="*80)
    print("META-ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: {output_dir}")
    print("\nFiles created:")
    print(f"  • meta_analysis_by_category.csv")
    print(f"  • meta_analysis_by_decade.csv")
    print(f"  • summary_statistics.csv")
    print(f"  • forest_plot_by_category.png")
    print(f"  • funnel_plot_overall.png")
    print(f"  • temporal_trends.png")
    print()

if __name__ == "__main__":
    main()
