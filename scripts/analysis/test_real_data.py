"""
Test Advanced Meta-Analysis Methods on REAL Cardiology Data

This script demonstrates the advanced methods on actual clinical trials:
- 10 beta-blocker trials in heart failure
- Real patient data, real outcomes
- Published in major journals (NEJM, Lancet, etc.)

PURPOSE: Show WHY traditional meta-analysis fails and how to improve it.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from advanced_meta_analysis import (
    AdvancedMetaAnalysis,
    EffectSize,
    PublicationBiasDetection
)
from failure_detection import (
    MetaAnalysisFailureDetector,
    generate_reliability_report
)


def load_beta_blocker_data() -> list:
    """Load real beta-blocker trial data."""
    df = pd.read_csv('data/raw/sample_metaanalysis/beta_blockers_hf_mortality.csv')

    print("=" * 80)
    print("LOADING REAL CLINICAL TRIALS DATA")
    print("=" * 80)
    print(f"\nDataset: Beta-blockers for Heart Failure Mortality")
    print(f"Number of trials: {len(df)}")
    print(f"Time span: {df['year'].min()} - {df['year'].max()}")
    print(f"Total patients: {(df['n_intervention'] + df['n_control']).sum():,}")
    print("\nIncluded Trials:")
    for _, row in df.iterrows():
        print(f"  - {row['study_id']} ({row['year']}): {row['intervention']}")
    print()

    # Convert to EffectSize objects
    effect_sizes = []
    for _, row in df.iterrows():
        effect_sizes.append(EffectSize(
            estimate=row['log_rr'],
            se=row['se_log_rr'],
            ci_lower=np.log(row['ci_lower']),
            ci_upper=np.log(row['ci_upper']),
            n=int(row['n_intervention'] + row['n_control']),
            study_id=row['study_id'],
            study_quality=row['quality_score'],
            publication_year=int(row['year'])
        ))

    return effect_sizes


def demonstrate_method_comparison(effect_sizes: list):
    """Compare different meta-analysis methods."""
    print("=" * 80)
    print("COMPARING META-ANALYSIS METHODS ON REAL DATA")
    print("=" * 80)
    print("\nQUESTION: Do beta-blockers reduce mortality in heart failure?")
    print()

    ma = AdvancedMetaAnalysis()

    # Compare all methods
    comparison = ma.compare_methods(effect_sizes)

    print(comparison.to_string(index=False))
    print()

    # Interpretation
    print("INTERPRETATION:")
    print("-" * 80)

    # Check consistency across methods
    estimates = comparison['Estimate'].values
    ci_widths = comparison['CI_Width'].values

    mean_estimate = np.mean(estimates)
    std_estimate = np.std(estimates)

    print(f"Mean estimate across methods: {mean_estimate:.3f} (log RR)")
    print(f"RR = {np.exp(mean_estimate):.3f}")
    print(f"Std deviation: {std_estimate:.3f}")

    if std_estimate < 0.05:
        print("\n✓ Estimates are CONSISTENT across methods")
        print("  → Results are robust to method choice")
    else:
        print("\n⚠ Estimates vary SUBSTANTIALLY across methods")
        print("  → Results are sensitive to method choice")
        print("  → Report all methods or use recommended (Hartung-Knapp)")

    # Check significance consistency
    sig_count = comparison['Significant_5pct'].sum()
    if sig_count == len(comparison):
        print(f"\n✓ ALL methods show statistically significant benefit")
        print("  → Strong evidence for effect")
    elif sig_count == 0:
        print(f"\n✗ NO methods show statistically significant benefit")
        print("  → Insufficient evidence")
    else:
        print(f"\n⚠ {sig_count}/{len(comparison)} methods show significance")
        print("  → Borderline result, interpret cautiously")

    # Hartung-Knapp vs DL comparison
    hk_row = comparison[comparison['Method'] == 'Hartung-Knapp'].iloc[0]
    dl_row = comparison[comparison['Method'] == 'DerSimonian-Laird'].iloc[0]

    print(f"\nHartung-Knapp vs DerSimonian-Laird:")
    print(f"  CI Width (HK): {hk_row['CI_Width']:.3f}")
    print(f"  CI Width (DL): {dl_row['CI_Width']:.3f}")
    print(f"  Inflation factor: {hk_row['CI_Width'] / dl_row['CI_Width']:.2f}x")

    if hk_row['CI_Width'] / dl_row['CI_Width'] > 1.2:
        print("  → HK provides more conservative estimates")
        print("  → Standard random effects may be too optimistic")

    return comparison


def demonstrate_publication_bias(effect_sizes: list):
    """Test for publication bias."""
    print("\n" + "=" * 80)
    print("PUBLICATION BIAS ASSESSMENT")
    print("=" * 80)

    pb = PublicationBiasDetection()

    # Egger's test
    print("\n1. Egger's Regression Test for Funnel Plot Asymmetry")
    print("-" * 80)
    egger = pb.egger_test(effect_sizes)

    print(f"Intercept: {egger['intercept']:.4f} (SE = {egger['intercept_se']:.4f})")
    print(f"P-value: {egger['p_value']:.4f}")
    print(f"Interpretation: {egger['interpretation']}")

    if egger['p_value'] < 0.10:
        print("\n⚠ Possible publication bias detected!")
        print("  → Smaller studies may show systematically different effects")
        print("  → Could also be due to heterogeneity or chance")
        print("\nRECOMMENDATIONS:")
        print("  1. Inspect funnel plot visually")
        print("  2. Perform trim-and-fill analysis")
        print("  3. Compare with registered trials database")
        print("  4. Use contour-enhanced funnel plot")
    else:
        print("\n✓ No strong evidence of publication bias")
        print("  → Funnel plot appears symmetric")
        print("\nCAVEAT:")
        print("  - Egger's test has low power with few studies")
        print("  - Absence of evidence ≠ evidence of absence")

    if egger['limitation']:
        print(f"\nLIMITATION: {egger['limitation']}")

    # Sample size vs effect size correlation
    print("\n2. Small Study Effects")
    print("-" * 80)

    sample_sizes = np.array([es.n for es in effect_sizes])
    estimates = np.array([es.estimate for es in effect_sizes])

    from scipy.stats import spearmanr
    corr, p_val = spearmanr(sample_sizes, estimates)

    print(f"Correlation (sample size vs effect size): {corr:.3f}")
    print(f"P-value: {p_val:.4f}")

    if corr > 0.3:
        print("\n✓ Larger trials show LARGER effects")
        print("  → Unusual pattern, investigate causes")
    elif corr < -0.3:
        print("\n⚠ Smaller trials show LARGER effects")
        print("  → Classic pattern of publication bias or small study effects")
    else:
        print("\n✓ No systematic relationship between sample size and effect")


def demonstrate_failure_detection(effect_sizes: list, result):
    """Run comprehensive failure diagnostics."""
    print("\n" + "=" * 80)
    print("META-ANALYSIS RELIABILITY DIAGNOSTICS")
    print("=" * 80)

    detector = MetaAnalysisFailureDetector()
    failure_report = detector.comprehensive_diagnostics(effect_sizes, result)

    # Generate and print report
    report = generate_reliability_report(failure_report)
    print(report)

    # Additional insights
    print("\nDETAILED DIAGNOSTICS:")
    print("-" * 80)

    # Heterogeneity
    het = failure_report.detailed_diagnostics['heterogeneity']
    print(f"\n1. Heterogeneity: I² = {het['i_squared']:.1f}%")
    if het['i_squared'] < 25:
        print("   → Low heterogeneity: Studies are similar")
    elif het['i_squared'] < 50:
        print("   → Moderate heterogeneity: Some variability")
    elif het['i_squared'] < 75:
        print("   → Substantial heterogeneity: Important differences")
    else:
        print("   → Extreme heterogeneity: Pooling questionable")

    # Outliers
    outliers = failure_report.detailed_diagnostics['outliers']
    if outliers['n_outliers'] > 0:
        print(f"\n2. Outliers: {outliers['n_outliers']} detected")
        print(f"   Studies: {', '.join(outliers['outlier_studies'])}")
        print("   → Perform sensitivity analysis excluding these")
    else:
        print(f"\n2. Outliers: None detected")

    # Prediction interval
    pi = failure_report.detailed_diagnostics['prediction_interval']
    print(f"\n3. Prediction Interval: [{np.exp(pi['pi_lower']):.2f}, {np.exp(pi['pi_upper']):.2f}]")
    if pi['crosses_null']:
        print("   ⚠ Crosses null (RR = 1.0)")
        print("   → Future trials might show opposite results")
        print("   → Considerable uncertainty remains")
    else:
        print("   ✓ Does not cross null")
        print("   → Direction of effect is clear")

    # Statistical power
    power = failure_report.detailed_diagnostics['power']
    print(f"\n4. Statistical Power: {power['power']:.1%}")
    if power['power'] < 0.80:
        print("   ⚠ Underpowered - may miss true effects")
    else:
        print("   ✓ Adequate power to detect effects")

    return failure_report


def clinical_bottom_line(comparison, failure_report):
    """Provide clinical interpretation."""
    print("\n" + "=" * 80)
    print("CLINICAL BOTTOM LINE")
    print("=" * 80)

    # Get REML result (recommended method)
    reml_row = comparison[comparison['Method'] == 'REML'].iloc[0]
    rr = np.exp(reml_row['Estimate'])
    ci_lower = np.exp(reml_row['CI_Lower'])
    ci_upper = np.exp(reml_row['CI_Upper'])

    print(f"\nPooled Relative Risk: {rr:.2f} (95% CI: {ci_lower:.2f} to {ci_upper:.2f})")
    print(f"P-value: {reml_row['P_value']:.4f}")

    # Interpret effect size
    rrr = (1 - rr) * 100  # Relative risk reduction
    print(f"\nEffect Size:")
    print(f"  Relative Risk Reduction: {rrr:.1f}%")

    if rrr > 30:
        print("  → LARGE clinical benefit")
    elif rrr > 15:
        print("  → MODERATE clinical benefit")
    elif rrr > 5:
        print("  → SMALL clinical benefit")
    else:
        print("  → MINIMAL clinical benefit")

    # Number needed to treat (approximate)
    # Assuming baseline risk of ~15% mortality per year
    baseline_risk = 0.15
    arr = baseline_risk * (1 - rr)  # Absolute risk reduction
    nnt = 1 / arr if arr > 0 else np.inf

    print(f"\nAssuming baseline mortality risk of {baseline_risk*100:.0f}%:")
    print(f"  Absolute Risk Reduction: {arr*100:.1f}%")
    print(f"  Number Needed to Treat: {nnt:.0f} patients")
    print(f"  → Treat {nnt:.0f} patients to prevent 1 death")

    # Quality of evidence
    print(f"\nQuality of Evidence:")
    print(f"  Reliability Score: {failure_report.reliability_score:.1f}/100")
    print(f"  Overall Rating: {failure_report.overall_reliability}")

    if failure_report.overall_reliability in ['High', 'Moderate']:
        print("  ✓ Can inform clinical practice")
    else:
        print("  ⚠ Interpret with caution")

    # Recommendations
    print(f"\nClinical Recommendations:")
    if reml_row['Significant_5pct'] and failure_report.overall_reliability in ['High', 'Moderate']:
        print("  ✓ Beta-blockers REDUCE mortality in heart failure")
        print("  ✓ Strong recommendation for clinical use")
        print("  ✓ Consistent with current guidelines")
    else:
        print("  → Evidence is insufficient or unreliable")
        print("  → More research needed")

    # Caveats
    print(f"\nImportant Caveats:")
    if comparison['I²'].iloc[0] > 50:
        print("  • Substantial heterogeneity - not all patients benefit equally")
        print("  • Consider patient characteristics when prescribing")
    print("  • Results apply to patients similar to trial populations")
    print("  • Efficacy in trials may differ from real-world effectiveness")


def main():
    """Run complete demonstration on real data."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  ADVANCED META-ANALYSIS: REAL-WORLD DEMONSTRATION".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Beta-Blockers for Heart Failure Mortality".center(78) + "║")
    print("║" + "  10 Major Randomized Controlled Trials".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # Load data
    effect_sizes = load_beta_blocker_data()

    # Method comparison
    comparison = demonstrate_method_comparison(effect_sizes)

    # Get REML result for diagnostics
    ma = AdvancedMetaAnalysis()
    reml_result = ma.random_effects_reml(effect_sizes)

    # Publication bias
    demonstrate_publication_bias(effect_sizes)

    # Failure detection
    failure_report = demonstrate_failure_detection(effect_sizes, reml_result)

    # Clinical interpretation
    clinical_bottom_line(comparison, failure_report)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nThis demonstration shows:")
    print("  1. Different methods can give different results")
    print("  2. Standard methods (DL) may be too optimistic")
    print("  3. Comprehensive diagnostics reveal hidden issues")
    print("  4. Clinical interpretation requires careful consideration")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
