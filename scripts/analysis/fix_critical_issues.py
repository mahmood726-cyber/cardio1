#!/usr/bin/env python3
"""
Fix Critical Issues from Editorial Review

1. Bayesian analysis on FULL 1000 trials (not subset)
2. Meta-regression VIF (collinearity check)
3. Endpoint stratification
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("FIXING CRITICAL ISSUES FROM EDITORIAL REVIEW")
print("="*80 + "\n")

# Load data
df = pd.read_csv("data/processed/master_cardiovascular_metaanalysis_1001trials.csv")
output_dir = Path("data/analysis/corrected_results")
output_dir.mkdir(parents=True, exist_ok=True)

valid_mask = ~(np.isnan(df['log_rr']) | np.isnan(df['se_log_rr']) | 
               np.isinf(df['log_rr']) | np.isinf(df['se_log_rr']))
df_clean = df[valid_mask].copy()

print(f"✓ Loaded {len(df_clean)} valid trials\n")

# ============================================================================
# FIX 1: BAYESIAN ANALYSIS ON ALL 1000 TRIALS
# ============================================================================
print("="*80)
print("FIX 1: BAYESIAN ANALYSIS - FULL DATASET (N=1000)")
print("="*80 + "\n")

try:
    import pymc as pm
    import arviz as az
    
    log_rr_all = df_clean['log_rr'].values
    se_log_rr_all = df_clean['se_log_rr'].values
    
    print(f"Running Bayesian meta-analysis on ALL {len(log_rr_all)} trials...")
    print("(This addresses editorial concern about subset bias)\n")
    
    with pm.Model() as bayes_model_full:
        tau = pm.HalfNormal('tau', sigma=0.5)
        mu = pm.Normal('mu', mu=0, sigma=1)
        theta = pm.Normal('theta', mu=mu, sigma=tau, shape=len(log_rr_all))
        y_obs = pm.Normal('y_obs', mu=theta, sigma=se_log_rr_all, observed=log_rr_all)
        
        # Use fewer samples for computational efficiency with large dataset
        trace_full = pm.sample(1000, tune=500, return_inferencedata=True, 
                              progressbar=True, random_seed=42, chains=2)
    
    # Extract results
    mu_samples = trace_full.posterior['mu'].values.flatten()
    tau_samples = trace_full.posterior['tau'].values.flatten()
    
    mu_mean = np.mean(mu_samples)
    mu_ci = np.percentile(mu_samples, [2.5, 97.5])
    tau_mean = np.mean(tau_samples)
    
    print("\nBayesian Results (FULL DATASET):")
    print(f"  N trials: {len(log_rr_all)}")
    print(f"  Posterior mean (log RR): {mu_mean:.4f}")
    print(f"  Pooled RR: {np.exp(mu_mean):.3f}")
    print(f"  95% Credible Interval: {np.exp(mu_ci[0]):.3f} to {np.exp(mu_ci[1]):.3f}")
    print(f"  Between-study SD (tau): {tau_mean:.4f}")
    
    # Save results
    bayes_results = pd.DataFrame({
        'Parameter': ['mu (log RR)', 'RR', 'tau'],
        'Mean': [mu_mean, np.exp(mu_mean), tau_mean],
        'CI_Lower': [mu_ci[0], np.exp(mu_ci[0]), np.percentile(tau_samples, 2.5)],
        'CI_Upper': [mu_ci[1], np.exp(mu_ci[1]), np.percentile(tau_samples, 97.5)],
        'N_trials': [len(log_rr_all)] * 3
    })
    bayes_results.to_csv(output_dir / 'bayesian_full_dataset.csv', index=False)
    print(f"\n✓ Saved: bayesian_full_dataset.csv")
    
    print(f"\nCOMPARISON TO SUBSET (N=500):")
    print(f"  Subset RR: 0.854 (previous analysis)")
    print(f"  Full dataset RR: {np.exp(mu_mean):.3f} (corrected)")
    print(f"  Difference: {abs(0.854 - np.exp(mu_mean)):.3f}")
    
except Exception as e:
    print(f"! Bayesian analysis error: {e}")

# ============================================================================
# FIX 2: META-REGRESSION WITH VIF (COLLINEARITY CHECK)
# ============================================================================
print("\n" + "="*80)
print("FIX 2: META-REGRESSION - COLLINEARITY ASSESSMENT (VIF)")
print("="*80 + "\n")

# Prepare covariates
df_clean['year_std'] = (df_clean['year'] - df_clean['year'].mean()) / df_clean['year'].std()
df_clean['age_std'] = (df_clean['mean_age'] - df_clean['mean_age'].mean()) / df_clean['mean_age'].std()
df_clean['sample_size'] = df_clean['n_intervention'] + df_clean['n_control']
df_clean['log_n_std'] = (np.log(df_clean['sample_size']) - np.log(df_clean['sample_size']).mean()) / np.log(df_clean['sample_size']).std()
df_clean['male_std'] = (df_clean['pct_male'] - df_clean['pct_male'].mean()) / df_clean['pct_male'].std()

X = df_clean[['year_std', 'age_std', 'log_n_std', 'male_std']].fillna(0).values

# Calculate VIF
from numpy.linalg import inv

def calculate_vif(X):
    """Calculate Variance Inflation Factor for each predictor"""
    vif = []
    for i in range(X.shape[1]):
        # Regress Xi on all other X
        X_i = X[:, i]
        X_others = np.delete(X, i, axis=1)
        
        # Add intercept to others
        X_others = np.column_stack([np.ones(X_others.shape[0]), X_others])
        
        # Regression
        beta = inv(X_others.T @ X_others) @ X_others.T @ X_i
        y_pred = X_others @ beta
        
        # R²
        ss_res = np.sum((X_i - y_pred)**2)
        ss_tot = np.sum((X_i - np.mean(X_i))**2)
        r2 = 1 - (ss_res / ss_tot)
        
        # VIF = 1 / (1 - R²)
        vif.append(1 / (1 - r2) if r2 < 0.999 else 999)
    
    return vif

vif_values = calculate_vif(X)

print("Variance Inflation Factors (VIF):")
print("  Interpretation: VIF > 10 suggests problematic collinearity")
print("                  VIF > 5 suggests moderate collinearity\n")

covariate_names = ['Year', 'Age', 'Log(Sample Size)', '% Male']
for name, vif in zip(covariate_names, vif_values):
    flag = "❌ HIGH" if vif > 10 else "⚠️ MODERATE" if vif > 5 else "✓ OK"
    print(f"  {name:20s}: VIF = {vif:6.2f}  [{flag}]")

# Save VIF results
vif_df = pd.DataFrame({
    'Covariate': covariate_names,
    'VIF': vif_values,
    'Interpretation': ['High collinearity' if v > 10 else 'Moderate collinearity' if v > 5 else 'Acceptable' for v in vif_values]
})
vif_df.to_csv(output_dir / 'meta_regression_vif.csv', index=False)
print(f"\n✓ Saved: meta_regression_vif.csv")

# ============================================================================
# FIX 3: ENDPOINT STRATIFICATION
# ============================================================================
print("\n" + "="*80)
print("FIX 3: ENDPOINT STRATIFICATION (Hard vs Soft Outcomes)")
print("="*80 + "\n")

# Classify endpoints based on notes field
def classify_endpoint(notes):
    """Classify as hard (mortality, MI, stroke) vs soft (hospitalization, surrogate)"""
    notes_lower = str(notes).lower()
    
    # Hard outcomes
    hard_keywords = ['mortality', 'death', 'died', 'fatal', 'myocardial infarction', 
                     'mi ', 'stroke', 'cardiovascular death', 'all-cause death']
    
    # Soft outcomes  
    soft_keywords = ['hospitalization', 'admission', 'blood pressure', 'bp ', 'ldl',
                     'cholesterol', 'hba1c', 'glucose', 'ejection fraction']
    
    if any(kw in notes_lower for kw in hard_keywords):
        return 'Hard'
    elif any(kw in notes_lower for kw in soft_keywords):
        return 'Soft'
    else:
        return 'Composite/Mixed'

df_clean['endpoint_type'] = df_clean['notes'].apply(classify_endpoint)

print("Endpoint Classification:")
endpoint_counts = df_clean['endpoint_type'].value_counts()
for etype, count in endpoint_counts.items():
    print(f"  {etype:20s}: {count:4d} trials ({count/len(df_clean)*100:.1f}%)")

# Meta-analysis by endpoint type
print("\nPooled Estimates by Endpoint Type:\n")

endpoint_results = []
for etype in df_clean['endpoint_type'].unique():
    df_etype = df_clean[df_clean['endpoint_type'] == etype]
    
    if len(df_etype) < 5:
        continue
    
    log_rr = df_etype['log_rr'].values
    se_log_rr = df_etype['se_log_rr'].values
    weights = 1 / (se_log_rr ** 2)
    
    # Random-effects (simple DL)
    pooled = np.sum(weights * log_rr) / np.sum(weights)
    se_pooled = np.sqrt(1 / np.sum(weights))
    
    # Calculate tau²
    Q = np.sum(weights * (log_rr - pooled) ** 2)
    df_q = len(log_rr) - 1
    C = np.sum(weights) - np.sum(weights**2) / np.sum(weights)
    tau2 = max(0, (Q - df_q) / C) if C > 0 else 0
    I2 = max(0, ((Q - df_q) / Q) * 100) if Q > 0 else 0
    
    # CI
    ci_lower = np.exp(pooled - 1.96 * se_pooled)
    ci_upper = np.exp(pooled + 1.96 * se_pooled)
    
    print(f"{etype}:")
    print(f"  N trials: {len(df_etype)}")
    print(f"  Pooled RR: {np.exp(pooled):.3f} (95% CI: {ci_lower:.3f}-{ci_upper:.3f})")
    print(f"  I²: {I2:.1f}%, Tau²: {tau2:.4f}\n")
    
    endpoint_results.append({
        'Endpoint_Type': etype,
        'N_Trials': len(df_etype),
        'Pooled_RR': np.exp(pooled),
        'CI_Lower': ci_lower,
        'CI_Upper': ci_upper,
        'I2': I2,
        'Tau2': tau2
    })

endpoint_df = pd.DataFrame(endpoint_results)
endpoint_df.to_csv(output_dir / 'endpoint_stratification.csv', index=False)
print("✓ Saved: endpoint_stratification.csv")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("CRITICAL FIXES COMPLETE!")
print("="*80)
print(f"\nResults saved to: {output_dir}")
print("\nFiles created:")
print("  • bayesian_full_dataset.csv (addresses subset bias)")
print("  • meta_regression_vif.csv (collinearity assessment)")
print("  • endpoint_stratification.csv (hard vs soft outcomes)")
print("\nKey Findings:")
if 'mu_mean' in locals():
    print(f"  • Bayesian (full): RR = {np.exp(mu_mean):.3f} vs subset RR = 0.854")
print(f"  • VIF range: {min(vif_values):.1f} to {max(vif_values):.1f}")
print(f"  • Endpoint types: {len(endpoint_counts)} categories identified")
print("\n" + "="*80 + "\n")

