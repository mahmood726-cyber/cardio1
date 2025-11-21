"""
Test Advanced Statistical Methods on Real Cardiology Data

Tests:
1. Meta-Regression on ICD trials (age, LVEF, etiology covariates)
2. Dose-Response Meta-Analysis on statin trials (nonlinear relationships)
3. Network Meta-Analysis on antihypertensive trials (indirect comparisons)

Demonstrates practical application of cutting-edge methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.analysis.advanced_statistical_methods import (
    MetaRegression,
    DoseResponseMetaAnalysis,
    NetworkMetaAnalysis
)


def test_metaregression():
    """Test meta-regression on ICD primary prevention trials."""
    print("\n" + "=" * 80)
    print("META-REGRESSION: ICD Primary Prevention")
    print("=" * 80)

    # Load data
    df = pd.read_csv('data/raw/advanced_datasets/icd_primary_prevention.csv')

    print(f"\nDataset: {len(df)} trials, {df['n_intervention'].sum() + df['n_control'].sum():,} patients")
    print(f"Age range: {df['mean_age'].min():.0f}-{df['mean_age'].max():.0f} years")
    print(f"LVEF range: {df['mean_lvef'].min():.0f}-{df['mean_lvef'].max():.0f}%")
    print(f"Ischemic: {len(df[df['pct_ischemic']>=90])} trials")
    print(f"Nonischemic: {len(df[df['pct_ischemic']<=10])} trials")

    # Prepare data
    effect_sizes = df['log_rr'].values
    variances = df['se_log_rr'].values ** 2

    # Covariates
    covariates = df[['mean_age', 'mean_lvef', 'etiology']].copy()

    # Fit meta-regression
    print("\n\nFitting meta-regression model...")
    mr = MetaRegression()
    result = mr.fit(effect_sizes, variances, covariates)

    print("\n" + "-" * 80)
    print("RESULTS")
    print("-" * 80)

    print(f"\nModel: log(RR) ~ age + LVEF + etiology")
    print(f"\nNumber of studies: {result.n_studies}")
    print(f"Number of covariates: {result.n_covariates}")

    print(f"\nHeterogeneity:")
    print(f"  τ² (without covariates): {result.tau_squared:.4f}")
    print(f"  τ² (residual, with covariates): {result.tau_squared_residual:.4f}")
    print(f"  R² (heterogeneity explained): {result.r_squared:.1%}")

    print(f"\nTest for moderators:")
    print(f"  QM statistic: {result.qm_statistic:.2f}")
    print(f"  P-value: {result.qm_pvalue:.4f}")
    print(f"  {'*** Covariates explain heterogeneity ***' if result.qm_pvalue < 0.05 else '(Not significant)'}")

    print(f"\nCoefficients:")
    for name, coef in result.coefficients.items():
        se = result.se[name]
        pval = result.p_values[name]
        ci_low = result.ci_lower[name]
        ci_high = result.ci_upper[name]

        sig = "***" if pval < 0.001 else ("**" if pval < 0.01 else ("*" if pval < 0.05 else ""))

        if name == 'Intercept':
            print(f"  {name:20s}: {coef:7.3f} (SE: {se:.3f}, p={pval:.3f}) [{ci_low:.3f}, {ci_high:.3f}] {sig}")
        else:
            # Convert to RR scale for interpretation
            rr_per_unit = np.exp(coef)
            print(f"  {name:20s}: {coef:7.3f} (SE: {se:.3f}, p={pval:.3f}) [{ci_low:.3f}, {ci_high:.3f}] {sig}")
            if 'age' in name.lower():
                print(f"                        → RR per 10-year increase: {rr_per_unit**10:.3f}")
            elif 'lvef' in name.lower():
                print(f"                        → RR per 10% increase in LVEF: {rr_per_unit**10:.3f}")

    print("\nInterpretation:")
    if result.r_squared > 0.5:
        print(f"  ✓ Covariates explain {result.r_squared:.0%} of heterogeneity - EXCELLENT")
    elif result.r_squared > 0.25:
        print(f"  ✓ Covariates explain {result.r_squared:.0%} of heterogeneity - GOOD")
    else:
        print(f"  • Covariates explain {result.r_squared:.0%} of heterogeneity - LIMITED")


def test_dose_response():
    """Test dose-response meta-analysis on statin trials."""
    print("\n\n" + "=" * 80)
    print("DOSE-RESPONSE META-ANALYSIS: Statins and LDL Reduction")
    print("=" * 80)

    # Load data
    df = pd.read_csv('data/raw/advanced_datasets/statin_dose_response.csv')

    print(f"\nDataset: {len(df)} trials, {df['n_intervention'].sum() + df['n_control'].sum():,} patients")
    print(f"LDL reduction range: {df['ldl_reduction_mmol'].min():.1f}-{df['ldl_reduction_mmol'].max():.1f} mmol/L")
    print(f"Dose range: {df['dose_mg'].min():.0f}-{df['dose_mg'].max():.0f} mg")

    # Prepare data
    doses = df['ldl_reduction_mmol'].values
    effect_sizes = df['log_rr'].values
    variances = df['se_log_rr'].values ** 2

    # Test all models
    models = ['linear', 'quadratic', 'rcs']

    print("\n" + "-" * 80)
    print("MODEL COMPARISON")
    print("-" * 80)

    results = {}
    for model_name in models:
        print(f"\n{model_name.upper()} MODEL:")

        drma = DoseResponseMetaAnalysis(n_knots=3)
        result = drma.fit(doses, effect_sizes, variances, model=model_name)
        results[model_name] = result

        print(f"  Model type: {result.model_type}")
        print(f"  P for nonlinearity: {result.p_nonlinearity:.4f}")

        if result.p_nonlinearity < 0.05:
            print(f"  *** Significant nonlinearity detected ***")
        else:
            print(f"  (Linear relationship adequate)")

        if result.optimal_dose is not None:
            print(f"  Optimal LDL reduction: {result.optimal_dose:.2f} mmol/L")
            idx = np.argmin(np.abs(result.dose_range - result.optimal_dose))
            optimal_rr = np.exp(result.effect_at_dose[idx])
            print(f"  Effect at optimal dose: RR = {optimal_rr:.3f}")

        # Show effects at specific doses
        print(f"\n  Effects at specific LDL reductions:")
        for target_dose in [0.5, 1.0, 1.5, 2.0]:
            if target_dose >= doses.min() and target_dose <= doses.max():
                idx = np.argmin(np.abs(result.dose_range - target_dose))
                rr = np.exp(result.effect_at_dose[idx])
                ci_low = np.exp(result.ci_lower_at_dose[idx])
                ci_high = np.exp(result.ci_upper_at_dose[idx])
                print(f"    {target_dose:.1f} mmol/L: RR = {rr:.3f} (95% CI: {ci_low:.3f}-{ci_high:.3f})")

    # Compare models
    print("\n" + "-" * 80)
    print("CONCLUSION")
    print("-" * 80)

    if results['rcs'].p_nonlinearity < 0.05:
        print("\n  ✓ NONLINEAR relationship detected")
        print("  → Use restricted cubic spline model")
        print("  → Benefit may plateau or diminish at very high LDL reductions")
    elif results['quadratic'].p_nonlinearity < 0.05:
        print("\n  ✓ QUADRATIC relationship detected")
        print("  → Linear model insufficient")
    else:
        print("\n  ✓ LINEAR relationship adequate")
        print("  → Each 1 mmol/L LDL reduction provides consistent benefit")


def test_network_metaanalysis():
    """Test network meta-analysis on antihypertensive drug classes."""
    print("\n\n" + "=" * 80)
    print("NETWORK META-ANALYSIS: Antihypertensive Drug Classes")
    print("=" * 80)

    # Load data
    df = pd.read_csv('data/raw/advanced_datasets/antihypertensive_network.csv')

    print(f"\nDataset: {len(df)} trials, {df['n_intervention'].sum() + df['n_control'].sum():,} patients")

    # Get unique treatments
    treatments_a = df['treatment_a'].unique()
    treatments_b = df['treatment_b'].unique()
    all_treatments = sorted(list(set(treatments_a) | set(treatments_b)))

    print(f"Treatments: {len(all_treatments)}")
    for trt in all_treatments:
        print(f"  - {trt}")

    print(f"\nDirect comparisons: {len(df)}")
    for _, row in df.iterrows():
        print(f"  - {row['treatment_a']} vs {row['treatment_b']} ({row['study_id']})")

    # Fit network meta-analysis
    print("\n" + "-" * 80)
    print("FITTING NETWORK META-ANALYSIS")
    print("-" * 80)

    nma = NetworkMetaAnalysis()
    result = nma.fit(df, 'treatment_a', 'treatment_b', 'log_rr', 'se_log_rr')

    print("\n✓ Network analysis complete")

    # Show all pairwise comparisons
    print("\n" + "-" * 80)
    print("ALL PAIRWISE COMPARISONS (Log RR)")
    print("-" * 80)

    print("\n" + " " * 20, end="")
    for trt in result.treatments:
        print(f"{trt[:15]:>17s}", end="")
    print()
    print("-" * (20 + 17 * len(result.treatments)))

    for i, trt_a in enumerate(result.treatments):
        print(f"{trt_a:20s}", end="")
        for j, trt_b in enumerate(result.treatments):
            if i == j:
                print(f"{'---':>17s}", end="")
            elif not np.isnan(result.effect_matrix[i, j]):
                effect = result.effect_matrix[i, j]
                print(f"{effect:>17.3f}", end="")
            else:
                print(f"{'NA':>17s}", end="")
        print()

    # Convert to RR and show key comparisons
    print("\n" + "-" * 80)
    print("KEY COMPARISONS (Relative Risk)")
    print("-" * 80)

    for i, trt_a in enumerate(result.treatments):
        for j, trt_b in enumerate(result.treatments):
            if i < j and not np.isnan(result.effect_matrix[i, j]):
                rr = np.exp(result.effect_matrix[i, j])
                se = result.se_matrix[i, j]
                ci_low = np.exp(result.effect_matrix[i, j] - 1.96 * se)
                ci_high = np.exp(result.effect_matrix[i, j] + 1.96 * se)
                p = result.p_matrix[i, j]

                sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else ""))

                print(f"\n{trt_a} vs {trt_b}:")
                print(f"  RR = {rr:.3f} (95% CI: {ci_low:.3f}-{ci_high:.3f}), p={p:.4f} {sig}")

    # SUCRA scores (treatment rankings)
    print("\n" + "-" * 80)
    print("TREATMENT RANKINGS (SUCRA scores)")
    print("-" * 80)
    print("\nSUCRA = Surface Under Cumulative Ranking")
    print("Higher score = more likely to be best treatment")
    print()

    sorted_sucra = sorted(result.sucra_scores.items(), key=lambda x: x[1], reverse=True)
    for rank, (trt, score) in enumerate(sorted_sucra, 1):
        print(f"  {rank}. {trt:25s}: {score:5.1f}/100")

    print("\nInterpretation:")
    best_trt = sorted_sucra[0][0]
    best_score = sorted_sucra[0][1]
    print(f"  ✓ {best_trt} appears most likely to be best treatment (SUCRA = {best_score:.1f})")


def main():
    """Run all tests."""
    print("=" * 80)
    print("TESTING ADVANCED STATISTICAL METHODS ON REAL CARDIOLOGY DATA")
    print("=" * 80)
    print("\nMethods tested:")
    print("  1. Meta-Regression (exploring heterogeneity with covariates)")
    print("  2. Dose-Response Meta-Analysis (nonlinear relationships)")
    print("  3. Network Meta-Analysis (multiple treatment comparisons)")

    try:
        test_metaregression()
    except Exception as e:
        print(f"\nError in meta-regression: {e}")
        import traceback
        traceback.print_exc()

    try:
        test_dose_response()
    except Exception as e:
        print(f"\nError in dose-response: {e}")
        import traceback
        traceback.print_exc()

    try:
        test_network_metaanalysis()
    except Exception as e:
        print(f"\nError in network meta-analysis: {e}")
        import traceback
        traceback.print_exc()

    print("\n\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
