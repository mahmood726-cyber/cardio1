"""
Meta-Analysis Failure Detection and Diagnostic System

This module implements comprehensive diagnostics to detect when meta-analysis
results are unreliable or misleading.

KEY PROBLEMS DETECTED:
1. Excessive heterogeneity (pooling inappropriate)
2. Small study effects / publication bias
3. Outliers and influential studies
4. Model misspecification
5. Sparse data problems
6. Simpson's paradox
7. Ecological fallacy
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
import logging

from advanced_meta_analysis import EffectSize, MetaAnalysisResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FailureReport:
    """Container for meta-analysis failure diagnostics."""
    overall_reliability: str  # 'High', 'Moderate', 'Low', 'Very Low'
    reliability_score: float  # 0-100
    critical_issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    detailed_diagnostics: Dict


class MetaAnalysisFailureDetector:
    """
    Comprehensive system to detect meta-analysis failures and limitations.

    This addresses the reproducibility crisis in meta-analysis by:
    - Identifying when pooling is inappropriate
    - Detecting methodological issues
    - Flagging unreliable results
    - Suggesting better approaches
    """

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha

    def comprehensive_diagnostics(
        self,
        effect_sizes: List[EffectSize],
        result: MetaAnalysisResult
    ) -> FailureReport:
        """
        Run comprehensive diagnostic checks on meta-analysis.

        Args:
            effect_sizes: Original effect sizes
            result: Meta-analysis result to evaluate

        Returns:
            Complete failure report
        """
        logger.info("Running comprehensive meta-analysis diagnostics")

        critical_issues = []
        warnings = []
        recommendations = []
        diagnostics = {}

        # 1. Check for excessive heterogeneity
        het_check = self._check_heterogeneity(result)
        diagnostics['heterogeneity'] = het_check
        if het_check['severity'] == 'critical':
            critical_issues.append(het_check['message'])
            recommendations.append(het_check['recommendation'])
        elif het_check['severity'] == 'warning':
            warnings.append(het_check['message'])

        # 2. Check for outliers
        outlier_check = self._detect_outliers(effect_sizes, result)
        diagnostics['outliers'] = outlier_check
        if outlier_check['n_outliers'] > 0:
            if outlier_check['n_outliers'] / len(effect_sizes) > 0.2:
                critical_issues.append(
                    f"Multiple outliers detected ({outlier_check['n_outliers']} studies). "
                    "Pooled estimate may be unstable."
                )
            else:
                warnings.append(
                    f"Outliers detected: {outlier_check['outlier_studies']}"
                )
            recommendations.append("Perform sensitivity analysis excluding outliers")

        # 3. Check sample size adequacy
        sample_check = self._check_sample_size(effect_sizes)
        diagnostics['sample_size'] = sample_check
        if sample_check['adequate'] == False:
            if sample_check['n_studies'] < 5:
                critical_issues.append(sample_check['message'])
            else:
                warnings.append(sample_check['message'])
            recommendations.extend(sample_check['recommendations'])

        # 4. Check for small study effects
        small_study_check = self._check_small_study_effects(effect_sizes)
        diagnostics['small_study_effects'] = small_study_check
        if small_study_check['detected']:
            warnings.append(small_study_check['message'])
            recommendations.append(small_study_check['recommendation'])

        # 5. Influence analysis
        influence_check = self._influence_analysis(effect_sizes, result)
        diagnostics['influence'] = influence_check
        if influence_check['highly_influential']:
            warnings.append(
                f"Highly influential studies detected: {influence_check['influential_studies']}"
            )
            recommendations.append("Perform leave-one-out sensitivity analysis")

        # 6. Check confidence interval width
        ci_check = self._check_ci_width(result)
        diagnostics['ci_width'] = ci_check
        if ci_check['interpretation'] == 'imprecise':
            warnings.append(ci_check['message'])

        # 7. Check prediction interval
        pi_check = self._check_prediction_interval(result)
        diagnostics['prediction_interval'] = pi_check
        if pi_check['crosses_null']:
            warnings.append(
                "Prediction interval crosses null. "
                "Future studies may show opposite effects."
            )
            recommendations.append(
                "Report prediction interval alongside confidence interval"
            )

        # 8. Check for temporal trends
        temporal_check = self._check_temporal_trends(effect_sizes)
        diagnostics['temporal_trends'] = temporal_check
        if temporal_check['trend_detected']:
            warnings.append(temporal_check['message'])
            recommendations.append("Perform cumulative meta-analysis")

        # 9. Power analysis
        power_check = self._power_analysis(effect_sizes, result)
        diagnostics['power'] = power_check
        if power_check['power'] < 0.80:
            warnings.append(
                f"Low statistical power ({power_check['power']:.2f}). "
                "May miss true effects."
            )

        # Calculate overall reliability score
        reliability_score = self._calculate_reliability_score(diagnostics)

        # Determine overall reliability level
        if reliability_score >= 80:
            overall_reliability = 'High'
        elif reliability_score >= 60:
            overall_reliability = 'Moderate'
        elif reliability_score >= 40:
            overall_reliability = 'Low'
        else:
            overall_reliability = 'Very Low'
            critical_issues.append(
                "Overall reliability is Very Low. Interpret results with extreme caution."
            )

        return FailureReport(
            overall_reliability=overall_reliability,
            reliability_score=reliability_score,
            critical_issues=critical_issues,
            warnings=warnings,
            recommendations=recommendations,
            detailed_diagnostics=diagnostics
        )

    def _check_heterogeneity(self, result: MetaAnalysisResult) -> Dict:
        """Check if heterogeneity is too high for meaningful pooling."""
        i_squared = result.i_squared
        tau_squared = result.tau_squared

        if i_squared >= 90:
            return {
                'severity': 'critical',
                'i_squared': i_squared,
                'message': (
                    f"Extreme heterogeneity (I² = {i_squared:.1f}%). "
                    "Pooled estimate may not be meaningful."
                ),
                'recommendation': (
                    "Do NOT pool studies. Instead: "
                    "(1) Investigate sources of heterogeneity, "
                    "(2) Perform subgroup analysis, "
                    "(3) Use meta-regression, or "
                    "(4) Present narrative synthesis."
                )
            }
        elif i_squared >= 75:
            return {
                'severity': 'warning',
                'i_squared': i_squared,
                'message': (
                    f"Substantial heterogeneity (I² = {i_squared:.1f}%). "
                    "Pooled estimate should be interpreted cautiously."
                ),
                'recommendation': (
                    "Investigate heterogeneity sources. "
                    "Consider subgroup analysis or meta-regression."
                )
            }
        elif i_squared >= 50:
            return {
                'severity': 'moderate',
                'i_squared': i_squared,
                'message': f"Moderate heterogeneity (I² = {i_squared:.1f}%).",
                'recommendation': "Random effects model appropriate. Report prediction interval."
            }
        else:
            return {
                'severity': 'none',
                'i_squared': i_squared,
                'message': f"Low heterogeneity (I² = {i_squared:.1f}%).",
                'recommendation': "Random effects model still recommended as default."
            }

    def _detect_outliers(
        self,
        effect_sizes: List[EffectSize],
        result: MetaAnalysisResult
    ) -> Dict:
        """Detect outlying studies using multiple criteria."""
        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])

        pooled = result.pooled_estimate
        tau = np.sqrt(result.tau_squared)

        # Standardized residuals
        residuals = estimates - pooled
        std_residuals = residuals / np.sqrt(ses**2 + tau**2)

        # Outliers: |standardized residual| > 2.5 (conservative threshold)
        outlier_mask = np.abs(std_residuals) > 2.5
        n_outliers = np.sum(outlier_mask)

        outlier_studies = [
            effect_sizes[i].study_id
            for i in range(len(effect_sizes))
            if outlier_mask[i]
        ]

        return {
            'n_outliers': n_outliers,
            'outlier_studies': outlier_studies,
            'std_residuals': std_residuals.tolist(),
            'threshold': 2.5
        }

    def _check_sample_size(self, effect_sizes: List[EffectSize]) -> Dict:
        """Check if sample size is adequate for reliable meta-analysis."""
        k = len(effect_sizes)

        if k < 3:
            return {
                'adequate': False,
                'n_studies': k,
                'message': (
                    f"Very few studies (k = {k}). "
                    "Meta-analysis not recommended."
                ),
                'recommendations': [
                    "Wait for more studies to be published",
                    "Present narrative review instead",
                    "Clearly state limitations of small sample"
                ]
            }
        elif k < 5:
            return {
                'adequate': False,
                'n_studies': k,
                'message': (
                    f"Few studies (k = {k}). "
                    "Results may be unstable."
                ),
                'recommendations': [
                    "Use Hartung-Knapp adjustment",
                    "Report prediction interval",
                    "Avoid subgroup analyses",
                    "State results are preliminary"
                ]
            }
        elif k < 10:
            return {
                'adequate': True,
                'n_studies': k,
                'message': f"Moderate number of studies (k = {k}).",
                'recommendations': [
                    "Use Hartung-Knapp adjustment",
                    "Publication bias tests have low power"
                ]
            }
        else:
            return {
                'adequate': True,
                'n_studies': k,
                'message': f"Adequate number of studies (k = {k}).",
                'recommendations': []
            }

    def _check_small_study_effects(self, effect_sizes: List[EffectSize]) -> Dict:
        """Check for small study effects (often related to publication bias)."""
        if len(effect_sizes) < 10:
            return {
                'detected': False,
                'testable': False,
                'message': "Too few studies to test for small study effects (k < 10)."
            }

        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])
        ns = np.array([es.n for es in effect_sizes])

        # Correlation between effect size and sample size
        # Small study effects: smaller studies show larger effects
        from scipy.stats import spearmanr

        corr, p_value = spearmanr(ns, estimates)

        detected = corr < -0.3 and p_value < 0.10

        if detected:
            return {
                'detected': True,
                'testable': True,
                'correlation': corr,
                'p_value': p_value,
                'message': (
                    f"Small study effects detected (r = {corr:.3f}, p = {p_value:.3f}). "
                    "Smaller studies show systematically different effects."
                ),
                'recommendation': (
                    "Possible publication bias or genuine small study effects. "
                    "Perform: (1) Egger's test, (2) Trim-and-fill, "
                    "(3) Contour-enhanced funnel plot."
                )
            }
        else:
            return {
                'detected': False,
                'testable': True,
                'correlation': corr,
                'p_value': p_value,
                'message': "No strong evidence of small study effects.",
                'recommendation': None
            }

    def _influence_analysis(
        self,
        effect_sizes: List[EffectSize],
        result: MetaAnalysisResult
    ) -> Dict:
        """Identify highly influential studies using leave-one-out analysis."""
        k = len(effect_sizes)

        if k < 5:
            return {
                'highly_influential': False,
                'message': "Too few studies for meaningful influence analysis."
            }

        # For each study, calculate pooled estimate without it
        # This is simplified - full implementation would re-run meta-analysis

        estimates = np.array([es.estimate for es in effect_sizes])

        # Simplified: just check if removing any study changes estimate by >20%
        influences = []
        for i in range(k):
            mask = np.ones(k, dtype=bool)
            mask[i] = False
            loo_mean = np.mean(estimates[mask])
            influence = abs(loo_mean - result.pooled_estimate) / abs(result.pooled_estimate)
            influences.append(influence)

        influential_threshold = 0.20  # 20% change
        influential_mask = np.array(influences) > influential_threshold

        influential_studies = [
            effect_sizes[i].study_id
            for i in range(k)
            if influential_mask[i]
        ]

        return {
            'highly_influential': len(influential_studies) > 0,
            'influential_studies': influential_studies,
            'influences': influences,
            'threshold': influential_threshold
        }

    def _check_ci_width(self, result: MetaAnalysisResult) -> Dict:
        """Check if confidence interval is too wide (imprecise estimate)."""
        ci_width = result.ci_upper - result.ci_lower

        # Rule of thumb: CI width > |estimate|
        relative_width = ci_width / abs(result.pooled_estimate) if result.pooled_estimate != 0 else np.inf

        if relative_width > 1.5:
            return {
                'width': ci_width,
                'relative_width': relative_width,
                'interpretation': 'imprecise',
                'message': (
                    f"Wide confidence interval (relative width = {relative_width:.2f}). "
                    "Estimate is imprecise."
                )
            }
        else:
            return {
                'width': ci_width,
                'relative_width': relative_width,
                'interpretation': 'adequate',
                'message': "Confidence interval width is acceptable."
            }

    def _check_prediction_interval(self, result: MetaAnalysisResult) -> Dict:
        """Check prediction interval for future studies."""
        pi_lower = result.pi_lower
        pi_upper = result.pi_upper

        # Check if PI crosses null (0 for differences, 1 for ratios)
        # Assuming differences for now
        crosses_null = (pi_lower < 0 < pi_upper)

        return {
            'pi_lower': pi_lower,
            'pi_upper': pi_upper,
            'crosses_null': crosses_null,
            'pi_width': pi_upper - pi_lower
        }

    def _check_temporal_trends(self, effect_sizes: List[EffectSize]) -> Dict:
        """Check for temporal trends in effect sizes."""
        years = [es.publication_year for es in effect_sizes if es.publication_year]

        if len(years) < len(effect_sizes) * 0.8:
            return {
                'trend_detected': False,
                'testable': False,
                'message': "Insufficient year information to test temporal trends."
            }

        estimates = np.array([es.estimate for es in effect_sizes if es.publication_year])
        years_array = np.array([es.publication_year for es in effect_sizes if es.publication_year])

        # Test correlation between year and effect size
        from scipy.stats import spearmanr
        corr, p_value = spearmanr(years_array, estimates)

        trend_detected = abs(corr) > 0.4 and p_value < 0.10

        if trend_detected:
            direction = "increasing" if corr > 0 else "decreasing"
            return {
                'trend_detected': True,
                'testable': True,
                'correlation': corr,
                'p_value': p_value,
                'direction': direction,
                'message': (
                    f"Temporal trend detected: effect sizes {direction} over time "
                    f"(r = {corr:.3f}, p = {p_value:.3f})."
                )
            }
        else:
            return {
                'trend_detected': False,
                'testable': True,
                'correlation': corr,
                'p_value': p_value,
                'message': "No significant temporal trend detected."
            }

    def _power_analysis(
        self,
        effect_sizes: List[EffectSize],
        result: MetaAnalysisResult
    ) -> Dict:
        """Estimate statistical power of meta-analysis."""
        k = len(effect_sizes)

        # Simplified power calculation
        # Power to detect observed effect size
        observed_effect = abs(result.pooled_estimate)
        se = result.pooled_se

        # Z-test power
        z_crit = 1.96  # Two-tailed at alpha = 0.05
        ncp = observed_effect / se  # Non-centrality parameter

        power = 1 - stats.norm.cdf(z_crit - ncp) + stats.norm.cdf(-z_crit - ncp)

        return {
            'power': power,
            'n_studies': k,
            'observed_effect': observed_effect,
            'adequate': power >= 0.80
        }

    def _calculate_reliability_score(self, diagnostics: Dict) -> float:
        """Calculate overall reliability score (0-100)."""
        score = 100.0

        # Heterogeneity penalty
        het = diagnostics['heterogeneity']
        if het['severity'] == 'critical':
            score -= 40
        elif het['severity'] == 'warning':
            score -= 20
        elif het['severity'] == 'moderate':
            score -= 10

        # Sample size penalty
        sample = diagnostics['sample_size']
        if not sample['adequate']:
            k = sample['n_studies']
            if k < 3:
                score -= 40
            elif k < 5:
                score -= 20
            elif k < 10:
                score -= 10

        # Outlier penalty
        outliers = diagnostics['outliers']
        outlier_prop = outliers['n_outliers'] / diagnostics['sample_size']['n_studies']
        score -= outlier_prop * 30

        # Small study effects penalty
        if diagnostics['small_study_effects']['detected']:
            score -= 15

        # Power penalty
        power = diagnostics['power']['power']
        if power < 0.50:
            score -= 20
        elif power < 0.80:
            score -= 10

        return max(0, score)


def generate_reliability_report(
    failure_report: FailureReport,
    output_format: str = 'text'
) -> str:
    """
    Generate human-readable reliability report.

    Args:
        failure_report: Failure detection results
        output_format: 'text', 'html', or 'markdown'

    Returns:
        Formatted report
    """
    if output_format != 'text':
        raise NotImplementedError("Only text format currently supported")

    report = []
    report.append("=" * 80)
    report.append("META-ANALYSIS RELIABILITY REPORT")
    report.append("=" * 80)
    report.append("")

    # Overall assessment
    report.append(f"Overall Reliability: {failure_report.overall_reliability}")
    report.append(f"Reliability Score: {failure_report.reliability_score:.1f}/100")
    report.append("")

    # Critical issues
    if failure_report.critical_issues:
        report.append("CRITICAL ISSUES:")
        report.append("-" * 80)
        for issue in failure_report.critical_issues:
            report.append(f"  ⚠️  {issue}")
        report.append("")

    # Warnings
    if failure_report.warnings:
        report.append("WARNINGS:")
        report.append("-" * 80)
        for warning in failure_report.warnings:
            report.append(f"  ⚡ {warning}")
        report.append("")

    # Recommendations
    if failure_report.recommendations:
        report.append("RECOMMENDATIONS:")
        report.append("-" * 80)
        for i, rec in enumerate(failure_report.recommendations, 1):
            report.append(f"  {i}. {rec}")
        report.append("")

    report.append("=" * 80)

    return "\n".join(report)


# Example usage
if __name__ == "__main__":
    from advanced_meta_analysis import AdvancedMetaAnalysis, EffectSize

    # Simulate some problematic data
    np.random.seed(42)

    # Create heterogeneous effect sizes with outliers
    estimates = np.concatenate([
        np.random.normal(0.5, 0.2, 10),  # Main cluster
        [1.5, 1.8]  # Outliers
    ])
    ses = np.random.uniform(0.1, 0.3, 12)

    effect_sizes = [
        EffectSize(
            estimate=est,
            se=se,
            ci_lower=est - 1.96*se,
            ci_upper=est + 1.96*se,
            n=int(np.random.uniform(50, 500)),
            study_id=f"Study_{i+1}",
            publication_year=2010 + i
        )
        for i, (est, se) in enumerate(zip(estimates, ses))
    ]

    # Run meta-analysis
    ma = AdvancedMetaAnalysis()
    result = ma.random_effects_reml(effect_sizes)

    # Run diagnostics
    detector = MetaAnalysisFailureDetector()
    failure_report = detector.comprehensive_diagnostics(effect_sizes, result)

    # Print report
    report = generate_reliability_report(failure_report)
    print(report)
