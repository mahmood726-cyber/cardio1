#!/usr/bin/env python3
"""
Novel Advanced Meta-Analysis Methods
for 1001 Cardiovascular Trials
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("NOVEL ADVANCED META-ANALYSIS METHODS")
print("1001 Cardiovascular Trials")
print("="*80 + "\n")

# Load data
df = pd.read_csv("data/processed/master_cardiovascular_metaanalysis_1001trials.csv")
output_dir = Path("data/analysis/novel_advanced_results")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"✓ Loaded {len(df)} trials\n")

# Clean data once
valid_mask = ~(np.isnan(df['log_rr']) | np.isnan(df['se_log_rr']) | 
               np.isinf(df['log_rr']) | np.isinf(df['se_log_rr']))
df_clean = df[valid_mask].copy()

# ============================================================================
# 1. BAYESIAN HIERARCHICAL META-ANALYSIS
# ============================================================================
print("="*80)
print("1. BAYESIAN HIERARCHICAL META-ANALYSIS")
print("="*80 + "\n")

try:
    import pymc as pm
    import arviz as az
    
    # Use subset for speed
    subset_size = 500
    log_rr_subset = df_clean['log_rr'].values[:subset_size]
    se_log_rr_subset = df_clean['se_log_rr'].values[:subset_size]
    
    print(f"Running Bayesian meta-analysis on {len(log_rr_subset)} trials...")
    print("(Using subset for computational efficiency)\n")
    
    with pm.Model() as bayes_model:
        tau = pm.HalfNormal('tau', sigma=0.5)
        mu = pm.Normal('mu', mu=0, sigma=1)
        theta = pm.Normal('theta', mu=mu, sigma=tau, shape=len(log_rr_subset))
        y_obs = pm.Normal('y_obs', mu=theta, sigma=se_log_rr_subset, observed=log_rr_subset)
        trace = pm.sample(2000, tune=1000, return_inferencedata=True, 
                         progressbar=False, random_seed=42, chains=2)
    
    # Extract results carefully
    mu_samples = trace.posterior['mu'].values.flatten()
    tau_samples = trace.posterior['tau'].values.flatten()
    
    mu_mean = np.mean(mu_samples)
    mu_ci = np.percentile(mu_samples, [2.5, 97.5])
    tau_mean = np.mean(tau_samples)
    
    print("Bayesian Random-Effects Results:")
    print(f"  Posterior mean (log RR): {mu_mean:.4f}")
    print(f"  Pooled RR: {np.exp(mu_mean):.3f}")
    print(f"  95% Credible Interval: {np.exp(mu_ci[0]):.3f} to {np.exp(mu_ci[1]):.3f}")
    print(f"  Between-study SD (tau): {tau_mean:.4f}\n")
    
    # Plot posterior
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(mu_samples, bins=50, alpha=0.7, edgecolor='black')
    axes[0].axvline(mu_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mu_mean:.3f}')
    axes[0].axvline(mu_ci[0], color='blue', linestyle=':', alpha=0.7)
    axes[0].axvline(mu_ci[1], color='blue', linestyle=':', alpha=0.7, label='95% CI')
    axes[0].set_xlabel('Log Risk Ratio (μ)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Posterior Distribution: Pooled Effect', fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    axes[1].hist(tau_samples, bins=50, alpha=0.7, edgecolor='black', color='orange')
    axes[1].axvline(tau_mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {tau_mean:.3f}')
    axes[1].set_xlabel('Between-Study SD (τ)')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Posterior Distribution: Heterogeneity', fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'bayesian_posterior.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Saved: bayesian_posterior.png\n")
    
except Exception as e:
    print(f"! Bayesian analysis error: {e}\n")

# ============================================================================
# 2. REML WITH HARTUNG-KNAPP ADJUSTMENT
# ============================================================================
print("="*80)
print("2. REML WITH HARTUNG-KNAPP ADJUSTMENT")
print("="*80 + "\n")

log_rr_all = df_clean['log_rr'].values
se_log_rr_all = df_clean['se_log_rr'].values
variances = se_log_rr_all ** 2
k = len(log_rr_all)

def reml_objective(tau2):
    weights = 1 / (variances + tau2)
    mu = np.sum(weights * log_rr_all) / np.sum(weights)
    q = np.sum(weights * (log_rr_all - mu) ** 2)
    log_det = np.sum(np.log(variances + tau2))
    log_sum_weights = np.log(np.sum(weights))
    return log_det + log_sum_weights + q

result = minimize(reml_objective, x0=0.01, method='L-BFGS-B', bounds=[(0, None)])
tau2_reml = result.x[0]

weights = 1 / (variances + tau2_reml)
pooled = np.sum(weights * log_rr_all) / np.sum(weights)

# Hartung-Knapp
residuals = log_rr_all - pooled
hk_var = np.sum(weights * residuals ** 2) / ((k - 1) * np.sum(weights))
hk_se = np.sqrt(hk_var)

df_hk = k - 1
t_crit = stats.t.ppf(0.975, df_hk)
ci_lower_hk = pooled - t_crit * hk_se
ci_upper_hk = pooled + t_crit * hk_se

naive_se = np.sqrt(1 / np.sum(weights))
ci_lower_naive = pooled - 1.96 * naive_se
ci_upper_naive = pooled + 1.96 * naive_se

print("REML Estimation:")
print(f"  Tau² (REML): {tau2_reml:.4f}")
print(f"  Pooled RR: {np.exp(pooled):.3f}")
print(f"\nHartung-Knapp Adjustment:")
print(f"  HK Standard Error: {hk_se:.4f}  (vs naive: {naive_se:.4f})")
print(f"  SE inflation: {hk_se/naive_se:.2f}x")
print(f"  95% CI (HK):    {np.exp(ci_lower_hk):.3f} to {np.exp(ci_upper_hk):.3f}")
print(f"  95% CI (naive): {np.exp(ci_lower_naive):.3f} to {np.exp(ci_upper_naive):.3f}")

if hk_se / naive_se > 1.5:
    print(f"\n  ⚠ Substantial SE inflation - large residual heterogeneity")
else:
    print(f"\n  ✓ Moderate adjustment - heterogeneity well-characterized")

# ============================================================================
# 3. META-REGRESSION
# ============================================================================
print("\n" + "="*80)
print("3. META-REGRESSION ANALYSIS")
print("="*80 + "\n")

# Prepare covariates
df_clean['year_std'] = (df_clean['year'] - df_clean['year'].mean()) / df_clean['year'].std()
df_clean['age_std'] = (df_clean['mean_age'] - df_clean['mean_age'].mean()) / df_clean['mean_age'].std()
df_clean['sample_size'] = df_clean['n_intervention'] + df_clean['n_control']
df_clean['log_n_std'] = (np.log(df_clean['sample_size']) - np.log(df_clean['sample_size']).mean()) / np.log(df_clean['sample_size']).std()
df_clean['male_std'] = (df_clean['pct_male'] - df_clean['pct_male'].mean()) / df_clean['pct_male'].std()

X = df_clean[['year_std', 'age_std', 'log_n_std', 'male_std']].fillna(0).values
y = log_rr_all
n, p = X.shape
X = np.column_stack([np.ones(n), X])

# Weighted least squares
W = np.diag(weights)
XtWX = X.T @ W @ X
XtWy = X.T @ W @ y

beta = np.linalg.solve(XtWX, XtWy)
y_pred = X @ beta
residuals_mr = y - y_pred

Q_resid = np.sum(weights * residuals_mr**2)
df_resid = n - p - 1
tau2_resid = max(0, (Q_resid - df_resid) / (np.sum(weights) - np.sum(weights**2) / np.sum(weights)))

var_beta = np.linalg.inv(XtWX) * tau2_resid
se_beta = np.sqrt(np.diag(var_beta))
t_stats = beta / se_beta
p_vals = 2 * (1 - stats.t.cdf(np.abs(t_stats), df_resid))

pooled_null = np.sum(weights * y) / np.sum(weights)
Q_total = np.sum(weights * (y - pooled_null)**2)
R2 = max(0, 1 - Q_resid / Q_total)

print("Meta-Regression Results:")
print(f"  N studies: {n}")
print(f"  Residual tau²: {tau2_resid:.4f}")
print(f"  R² (variance explained): {R2*100:.1f}%\n")
print("  Coefficients:")

coef_names = ['Intercept', 'Year', 'Age', 'Log(Sample Size)', '% Male']
results_list = []
for name, b, se, t, p in zip(coef_names, beta, se_beta, t_stats, p_vals):
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"    {name:20s}: β={b:7.4f}, SE={se:.4f}, t={t:6.2f}, p={p:.4f} {sig}")
    results_list.append({'Covariate': name, 'Beta': b, 'SE': se, 't': t, 'p': p})

pd.DataFrame(results_list).to_csv(output_dir / 'meta_regression.csv', index=False)
print(f"\n✓ Saved: meta_regression.csv")

if R2 > 0.25:
    print(f"\n  ✓ Covariates explain substantial heterogeneity (R² = {R2*100:.1f}%)")
else:
    print(f"\n  ! Limited variance explained (R² = {R2*100:.1f}%)")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("NOVEL ADVANCED METHODS COMPLETE!")
print("="*80)
print(f"\nResults saved to: {output_dir}")
print("\nFiles created:")
print("  • bayesian_posterior.png")
print("  • meta_regression.csv")
print("\nKey Findings:")
print(f"  • Bayesian pooled RR: {np.exp(mu_mean):.3f}" if 'mu_mean' in locals() else "  • Bayesian: Not available")
print(f"  • REML pooled RR: {np.exp(pooled):.3f}")
print(f"  • Meta-regression R²: {R2*100:.1f}%")
print("\n" + "="*80 + "\n")

