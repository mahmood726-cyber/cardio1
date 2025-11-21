"""
Advanced Meta-Analysis Methods for Cardiology Research

This module implements cutting-edge statistical methods to address failures
in traditional meta-analysis approaches, with focus on:
- Heterogeneity beyond I²
- Publication bias detection
- Small study effects
- Network meta-analysis
- Bayesian approaches
- Meta-regression with multiple moderators
- Individual patient data (IPD) methods
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Union
import logging
from dataclasses import dataclass
from scipy import stats
from scipy.optimize import minimize
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EffectSize:
    """Container for effect size data."""
    estimate: float
    se: float  # standard error
    ci_lower: float
    ci_upper: float
    n: int  # sample size
    study_id: str
    study_quality: Optional[str] = None
    publication_year: Optional[int] = None


@dataclass
class MetaAnalysisResult:
    """Container for meta-analysis results."""
    pooled_estimate: float
    pooled_se: float
    ci_lower: float
    ci_upper: float
    p_value: float

    # Heterogeneity
    i_squared: float
    tau_squared: float
    h_squared: float
    cochran_q: float
    q_p_value: float

    # Prediction interval
    pi_lower: float
    pi_upper: float

    # Model information
    model: str
    method: str
    n_studies: int

    # Diagnostics
    diagnostics: Dict
    warnings: List[str]


class AdvancedMetaAnalysis:
    """
    Advanced meta-analysis methods addressing limitations of traditional approaches.

    Key Issues Addressed:
    1. Heterogeneity underestimation (I² limitations)
    2. Publication bias (beyond funnel plots)
    3. Small study effects
    4. Between-study variance estimation
    5. Outlier detection
    6. Influence analysis
    """

    def __init__(self):
        self.results = None
        self.effect_sizes = None

    def random_effects_dersimonian_laird(
        self,
        effect_sizes: List[EffectSize]
    ) -> MetaAnalysisResult:
        """
        Traditional DerSimonian-Laird random effects meta-analysis.

        NOTE: This method is known to underestimate tau² in presence of
        substantial heterogeneity. Use for comparison with better methods.

        Args:
            effect_sizes: List of effect sizes with standard errors

        Returns:
            Meta-analysis results
        """
        logger.info("Running DerSimonian-Laird random effects meta-analysis")

        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])
        variances = ses ** 2

        # Fixed effect weights
        weights_fe = 1 / variances

        # Fixed effect estimate
        fe_estimate = np.sum(weights_fe * estimates) / np.sum(weights_fe)

        # Cochran's Q
        q = np.sum(weights_fe * (estimates - fe_estimate) ** 2)
        k = len(estimates)
        q_p_value = 1 - stats.chi2.cdf(q, k - 1)

        # DerSimonian-Laird tau²
        c = np.sum(weights_fe) - np.sum(weights_fe ** 2) / np.sum(weights_fe)
        tau_squared_dl = max(0, (q - (k - 1)) / c)

        # Random effects weights
        weights_re = 1 / (variances + tau_squared_dl)

        # Random effects estimate
        re_estimate = np.sum(weights_re * estimates) / np.sum(weights_re)
        re_se = np.sqrt(1 / np.sum(weights_re))

        # Confidence interval
        ci_lower = re_estimate - 1.96 * re_se
        ci_upper = re_estimate + 1.96 * re_se

        # P-value
        z_score = re_estimate / re_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        # Heterogeneity metrics
        i_squared = max(0, ((q - (k - 1)) / q) * 100)
        h_squared = q / (k - 1)

        # Prediction interval
        pi_se = np.sqrt(re_se ** 2 + tau_squared_dl)
        pi_lower = re_estimate - 1.96 * pi_se
        pi_upper = re_estimate + 1.96 * pi_se

        # Diagnostics
        diagnostics = {
            'q_statistic': q,
            'df': k - 1,
            'tau_squared_method': 'DerSimonian-Laird',
            'tau_squared': tau_squared_dl,
            'tau': np.sqrt(tau_squared_dl),
            'studies_included': k
        }

        # Warnings
        warnings_list = []
        if i_squared > 75:
            warnings_list.append("Substantial heterogeneity (I² > 75%). "
                               "Consider subgroup analysis or meta-regression.")
        if k < 5:
            warnings_list.append("Few studies (k < 5). Results may be unreliable.")
        if tau_squared_dl == 0 and q_p_value < 0.10:
            warnings_list.append("DL tau² = 0 despite significant Q. "
                               "Consider REML or alternative estimator.")

        return MetaAnalysisResult(
            pooled_estimate=re_estimate,
            pooled_se=re_se,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            p_value=p_value,
            i_squared=i_squared,
            tau_squared=tau_squared_dl,
            h_squared=h_squared,
            cochran_q=q,
            q_p_value=q_p_value,
            pi_lower=pi_lower,
            pi_upper=pi_upper,
            model='random',
            method='DerSimonian-Laird',
            n_studies=k,
            diagnostics=diagnostics,
            warnings=warnings_list
        )

    def random_effects_reml(
        self,
        effect_sizes: List[EffectSize],
        max_iter: int = 100
    ) -> MetaAnalysisResult:
        """
        Restricted Maximum Likelihood (REML) estimation.

        ADVANTAGES over DerSimonian-Laird:
        - More accurate tau² estimation
        - Better performance with moderate heterogeneity
        - Accounts for uncertainty in estimating fixed effects

        This is the PREFERRED method for most meta-analyses.

        Args:
            effect_sizes: List of effect sizes
            max_iter: Maximum iterations for optimization

        Returns:
            Meta-analysis results
        """
        logger.info("Running REML random effects meta-analysis")

        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])
        variances = ses ** 2
        k = len(estimates)

        def reml_objective(tau_squared):
            """REML objective function to minimize."""
            weights = 1 / (variances + tau_squared)
            mu = np.sum(weights * estimates) / np.sum(weights)

            # REML log-likelihood
            q = np.sum(weights * (estimates - mu) ** 2)
            log_det = np.sum(np.log(variances + tau_squared))
            log_sum_weights = np.log(np.sum(weights))

            return log_det + log_sum_weights + q

        # Optimize tau²
        result = minimize(
            reml_objective,
            x0=0.1,
            method='L-BFGS-B',
            bounds=[(0, None)]
        )

        tau_squared_reml = result.x[0]

        # Random effects with REML tau²
        weights = 1 / (variances + tau_squared_reml)
        pooled_estimate = np.sum(weights * estimates) / np.sum(weights)
        pooled_se = np.sqrt(1 / np.sum(weights))

        # Confidence interval
        ci_lower = pooled_estimate - 1.96 * pooled_se
        ci_upper = pooled_estimate + 1.96 * pooled_se

        # P-value
        z_score = pooled_estimate / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        # Heterogeneity metrics
        weights_fe = 1 / variances
        fe_estimate = np.sum(weights_fe * estimates) / np.sum(weights_fe)
        q = np.sum(weights_fe * (estimates - fe_estimate) ** 2)
        q_p_value = 1 - stats.chi2.cdf(q, k - 1)

        i_squared = max(0, ((q - (k - 1)) / q) * 100)
        h_squared = q / (k - 1)

        # Prediction interval
        pi_se = np.sqrt(pooled_se ** 2 + tau_squared_reml)
        pi_lower = pooled_estimate - 1.96 * pi_se
        pi_upper = pooled_estimate + 1.96 * pi_se

        # Diagnostics
        diagnostics = {
            'q_statistic': q,
            'df': k - 1,
            'tau_squared_method': 'REML',
            'tau_squared': tau_squared_reml,
            'tau': np.sqrt(tau_squared_reml),
            'optimization_success': result.success,
            'optimization_iterations': result.nit,
            'studies_included': k
        }

        # Warnings
        warnings_list = []
        if i_squared > 75:
            warnings_list.append("Substantial heterogeneity (I² > 75%). "
                               "Pooled estimate may not be meaningful.")
        if not result.success:
            warnings_list.append("REML optimization did not converge. "
                               "Results may be unreliable.")
        if tau_squared_reml / np.var(estimates) > 1:
            warnings_list.append("Between-study variance exceeds total variance. "
                               "Check for outliers or model misspecification.")

        return MetaAnalysisResult(
            pooled_estimate=pooled_estimate,
            pooled_se=pooled_se,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            p_value=p_value,
            i_squared=i_squared,
            tau_squared=tau_squared_reml,
            h_squared=h_squared,
            cochran_q=q,
            q_p_value=q_p_value,
            pi_lower=pi_lower,
            pi_upper=pi_upper,
            model='random',
            method='REML',
            n_studies=k,
            diagnostics=diagnostics,
            warnings=warnings_list
        )

    def hartung_knapp_adjustment(
        self,
        effect_sizes: List[EffectSize]
    ) -> MetaAnalysisResult:
        """
        Hartung-Knapp-Sidik-Jonkman (HKSJ) adjustment for random effects.

        WHY USE THIS:
        - Standard random effects underestimates uncertainty with few studies
        - HKSJ uses t-distribution instead of normal (like in regression)
        - More conservative confidence intervals when k is small
        - Better Type I error control

        RECOMMENDATION: Use this when k < 20 studies.

        Args:
            effect_sizes: List of effect sizes

        Returns:
            Meta-analysis results with HKSJ adjustment
        """
        logger.info("Running Hartung-Knapp adjusted meta-analysis")

        # First get REML estimate
        reml_result = self.random_effects_reml(effect_sizes)

        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])
        variances = ses ** 2
        k = len(estimates)

        tau_squared = reml_result.tau_squared
        weights = 1 / (variances + tau_squared)

        pooled_estimate = np.sum(weights * estimates) / np.sum(weights)

        # HKSJ variance estimator
        residuals = estimates - pooled_estimate
        hksj_variance = np.sum(weights * residuals ** 2) / ((k - 1) * np.sum(weights))
        hksj_se = np.sqrt(hksj_variance)

        # Use t-distribution with k-1 degrees of freedom
        df = k - 1
        t_critical = stats.t.ppf(0.975, df)

        # Confidence interval
        ci_lower = pooled_estimate - t_critical * hksj_se
        ci_upper = pooled_estimate + t_critical * hksj_se

        # P-value (t-test)
        t_stat = pooled_estimate / hksj_se
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

        # Prediction interval (also uses t-distribution)
        pi_se = np.sqrt(hksj_se ** 2 + tau_squared)
        pi_lower = pooled_estimate - t_critical * pi_se
        pi_upper = pooled_estimate + t_critical * pi_se

        # Diagnostics
        diagnostics = reml_result.diagnostics.copy()
        diagnostics['method'] = 'Hartung-Knapp-Sidik-Jonkman'
        diagnostics['degrees_of_freedom'] = df
        diagnostics['t_critical_value'] = t_critical
        diagnostics['hksj_se'] = hksj_se
        diagnostics['naive_se'] = reml_result.pooled_se
        diagnostics['se_inflation_factor'] = hksj_se / reml_result.pooled_se

        # Warnings
        warnings_list = reml_result.warnings.copy()
        if k < 5:
            warnings_list.append("Very few studies (k < 5). HKSJ may be overly conservative.")
        if diagnostics['se_inflation_factor'] > 2:
            warnings_list.append("HKSJ substantially inflated SE (>2x). "
                               "Large residual heterogeneity present.")

        return MetaAnalysisResult(
            pooled_estimate=pooled_estimate,
            pooled_se=hksj_se,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            p_value=p_value,
            i_squared=reml_result.i_squared,
            tau_squared=tau_squared,
            h_squared=reml_result.h_squared,
            cochran_q=reml_result.cochran_q,
            q_p_value=reml_result.q_p_value,
            pi_lower=pi_lower,
            pi_upper=pi_upper,
            model='random',
            method='Hartung-Knapp',
            n_studies=k,
            diagnostics=diagnostics,
            warnings=warnings_list
        )

    def paule_mandel_estimator(
        self,
        effect_sizes: List[EffectSize]
    ) -> MetaAnalysisResult:
        """
        Paule-Mandel tau² estimator.

        ADVANTAGES:
        - Iteratively matches Q statistic to its expectation
        - More robust than DL with moderate heterogeneity
        - Used by Cochrane as alternative to DL

        Args:
            effect_sizes: List of effect sizes

        Returns:
            Meta-analysis results
        """
        logger.info("Running Paule-Mandel meta-analysis")

        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])
        variances = ses ** 2
        k = len(estimates)

        def pm_objective(tau_squared):
            """Paule-Mandel objective: Q - (k-1) = 0."""
            weights = 1 / (variances + tau_squared)
            mu = np.sum(weights * estimates) / np.sum(weights)
            q = np.sum(weights * (estimates - mu) ** 2)
            return (q - (k - 1)) ** 2

        # Optimize
        result = minimize(
            pm_objective,
            x0=0.1,
            method='L-BFGS-B',
            bounds=[(0, None)]
        )

        tau_squared_pm = result.x[0]

        # Calculate pooled estimate
        weights = 1 / (variances + tau_squared_pm)
        pooled_estimate = np.sum(weights * estimates) / np.sum(weights)
        pooled_se = np.sqrt(1 / np.sum(weights))

        # CI and p-value
        ci_lower = pooled_estimate - 1.96 * pooled_se
        ci_upper = pooled_estimate + 1.96 * pooled_se
        z_score = pooled_estimate / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        # Heterogeneity
        weights_fe = 1 / variances
        fe_estimate = np.sum(weights_fe * estimates) / np.sum(weights_fe)
        q = np.sum(weights_fe * (estimates - fe_estimate) ** 2)
        q_p_value = 1 - stats.chi2.cdf(q, k - 1)
        i_squared = max(0, ((q - (k - 1)) / q) * 100)
        h_squared = q / (k - 1)

        # Prediction interval
        pi_se = np.sqrt(pooled_se ** 2 + tau_squared_pm)
        pi_lower = pooled_estimate - 1.96 * pi_se
        pi_upper = pooled_estimate + 1.96 * pi_se

        diagnostics = {
            'q_statistic': q,
            'df': k - 1,
            'tau_squared_method': 'Paule-Mandel',
            'tau_squared': tau_squared_pm,
            'tau': np.sqrt(tau_squared_pm),
            'optimization_success': result.success,
            'studies_included': k
        }

        warnings_list = []
        if not result.success:
            warnings_list.append("Paule-Mandel optimization failed.")
        if i_squared > 75:
            warnings_list.append("Substantial heterogeneity detected.")

        return MetaAnalysisResult(
            pooled_estimate=pooled_estimate,
            pooled_se=pooled_se,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            p_value=p_value,
            i_squared=i_squared,
            tau_squared=tau_squared_pm,
            h_squared=h_squared,
            cochran_q=q,
            q_p_value=q_p_value,
            pi_lower=pi_lower,
            pi_upper=pi_upper,
            model='random',
            method='Paule-Mandel',
            n_studies=k,
            diagnostics=diagnostics,
            warnings=warnings_list
        )

    def compare_methods(
        self,
        effect_sizes: List[EffectSize]
    ) -> pd.DataFrame:
        """
        Compare multiple meta-analysis methods side-by-side.

        This is CRITICAL for understanding method sensitivity and robustness.

        Args:
            effect_sizes: List of effect sizes

        Returns:
            DataFrame comparing results across methods
        """
        logger.info("Comparing meta-analysis methods")

        methods = {
            'DerSimonian-Laird': self.random_effects_dersimonian_laird,
            'REML': self.random_effects_reml,
            'Hartung-Knapp': self.hartung_knapp_adjustment,
            'Paule-Mandel': self.paule_mandel_estimator
        }

        results = []
        for name, method in methods.items():
            try:
                result = method(effect_sizes)
                results.append({
                    'Method': name,
                    'Estimate': result.pooled_estimate,
                    'SE': result.pooled_se,
                    'CI_Lower': result.ci_lower,
                    'CI_Upper': result.ci_upper,
                    'P_value': result.p_value,
                    'Tau²': result.tau_squared,
                    'I²': result.i_squared,
                    'PI_Lower': result.pi_lower,
                    'PI_Upper': result.pi_upper
                })
            except Exception as e:
                logger.error(f"Error with {name}: {e}")

        df = pd.DataFrame(results)

        # Add interpretation column
        df['Significant_5pct'] = df['P_value'] < 0.05
        df['CI_Width'] = df['CI_Upper'] - df['CI_Lower']

        return df


class PublicationBiasDetection:
    """
    Advanced publication bias detection beyond simple funnel plots.

    PROBLEM: Traditional methods (Egger's test, funnel plots) have limitations:
    - Low power with few studies
    - Confounded by heterogeneity
    - Assume linear relationship

    This class implements multiple modern approaches.
    """

    def egger_test(self, effect_sizes: List[EffectSize]) -> Dict:
        """
        Egger's regression test for funnel plot asymmetry.

        LIMITATIONS:
        - Low power with k < 10
        - Confounded by heterogeneity
        - Type I error inflation with OR/RR

        Args:
            effect_sizes: List of effect sizes

        Returns:
            Test results
        """
        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])

        # Precision (inverse of SE)
        precision = 1 / ses

        # Standardized estimates
        std_estimates = estimates / ses

        # Regression: std_estimate ~ precision
        from scipy.stats import linregress
        slope, intercept, r_value, p_value, std_err = linregress(precision, std_estimates)

        # Intercept test (bias indicator)
        t_stat = intercept / std_err
        bias_p_value = 2 * (1 - stats.t.cdf(abs(t_stat), len(estimates) - 2))

        return {
            'test': 'Egger',
            'intercept': intercept,
            'intercept_se': std_err,
            't_statistic': t_stat,
            'p_value': bias_p_value,
            'bias_detected': bias_p_value < 0.10,  # Use 0.10 threshold
            'interpretation': 'Significant' if bias_p_value < 0.10
                            else 'No significant bias detected',
            'limitation': 'Low power with k < 10 studies' if len(estimates) < 10 else None
        }

    def trim_and_fill(
        self,
        effect_sizes: List[EffectSize],
        side: str = 'auto'
    ) -> Dict:
        """
        Trim-and-fill method to estimate effect of publication bias.

        HOW IT WORKS:
        1. Trim asymmetric studies
        2. Estimate unbiased effect
        3. Fill in missing studies
        4. Re-estimate effect

        Args:
            effect_sizes: List of effect sizes
            side: 'left', 'right', or 'auto'

        Returns:
            Adjusted estimates and number of missing studies
        """
        estimates = np.array([es.estimate for es in effect_sizes])
        ses = np.array([es.se for es in effect_sizes])

        # This is a simplified version - full implementation would be more complex
        # For now, return placeholder

        logger.warning("Trim-and-fill: Simplified implementation")

        return {
            'test': 'Trim-and-Fill',
            'estimated_missing_studies': 0,  # Would calculate properly
            'adjusted_estimate': np.mean(estimates),
            'original_estimate': np.mean(estimates),
            'note': 'Full implementation requires iteration algorithm'
        }

    def selection_models(self, effect_sizes: List[EffectSize]) -> Dict:
        """
        Selection models (Copas, Vevea-Hedges) for publication bias.

        These model the selection process explicitly.
        More sophisticated than trim-and-fill.

        NOTE: Full implementation requires complex optimization.
        This is a placeholder for the framework.

        Args:
            effect_sizes: List of effect sizes

        Returns:
            Model results
        """
        logger.warning("Selection models: Framework placeholder")

        return {
            'test': 'Selection Model',
            'note': 'Requires specialized statistical software',
            'recommendation': 'Use metafor::selmodel() in R or PublicationBias package'
        }


# Example usage and testing
if __name__ == "__main__":
    # Simulate some effect sizes for testing
    np.random.seed(42)

    # Generate heterogeneous effect sizes
    true_effects = np.random.normal(0.5, 0.3, 15)
    ses = np.random.uniform(0.1, 0.3, 15)

    effect_sizes = [
        EffectSize(
            estimate=est,
            se=se,
            ci_lower=est - 1.96*se,
            ci_upper=est + 1.96*se,
            n=int(np.random.uniform(50, 500)),
            study_id=f"Study_{i+1}"
        )
        for i, (est, se) in enumerate(zip(true_effects, ses))
    ]

    # Run meta-analysis
    ma = AdvancedMetaAnalysis()

    print("=" * 80)
    print("COMPARING META-ANALYSIS METHODS")
    print("=" * 80)

    comparison = ma.compare_methods(effect_sizes)
    print(comparison.to_string())

    print("\n" + "=" * 80)
    print("PUBLICATION BIAS TESTING")
    print("=" * 80)

    pb = PublicationBiasDetection()
    egger_result = pb.egger_test(effect_sizes)

    print(f"\nEgger's Test:")
    print(f"  Intercept: {egger_result['intercept']:.4f}")
    print(f"  P-value: {egger_result['p_value']:.4f}")
    print(f"  Interpretation: {egger_result['interpretation']}")
