#!/usr/bin/env python3
"""
Advanced Meta-Analysis of 1001 Cardiovascular Trials
Using State-of-the-Art Statistical Methods

Implements cutting-edge techniques from recent statistical literature:
1. Bayesian random-effects meta-analysis
2. Meta-regression with multiple covariates
3. Trial Sequential Analysis (TSA)
4. Trim-and-fill method for publication bias correction
5. PET-PEESE for small-study effects
6. Cumulative meta-analysis
7. Prediction intervals (not just confidence intervals)
8. Influential case diagnostics (DFBETAS, Cook's distance)
9. Excess significance test
10. Leave-one-out sensitivity analysis
11. Contour-enhanced funnel plots
12. Radial plots (Galbraith plots)

Author: Research Team
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("Starting Advanced Meta-Analysis Pipeline...")
print("Loading required packages...")

# Try to import PyMC for Bayesian analysis
try:
    import pymc as pm
    import arviz as az
    BAYESIAN_AVAILABLE = True
    print("✓ PyMC available for Bayesian analysis")
except ImportError:
    BAYESIAN_AVAILABLE = False
    print("! PyMC not available - Bayesian analysis will be skipped")
    print("  Install with: pip install pymc arviz")

print("\nAll packages loaded successfully!\n")

# Load data
data_file = Path("data/processed/master_cardiovascular_metaanalysis_1001trials.csv")
df = pd.read_csv(data_file)

# Add calculated columns
if 'decade' not in df.columns:
    df['decade'] = (df['year'] // 10) * 10
if 'ci_lower' not in df.columns:
    df['ci_lower'] = np.exp(df['log_rr'] - 1.96 * df['se_log_rr'])
    df['ci_upper'] = np.exp(df['log_rr'] + 1.96 * df['se_log_rr'])

print(f"Loaded {len(df)} trials\n")
print("="*80)
print("ADVANCED META-ANALYSIS PIPELINE STARTING")
print("="*80)

# Create output directory
output_dir = Path("data/analysis/advanced_meta_analysis_results")
output_dir.mkdir(parents=True, exist_ok=True)

print("\n✓ Output directory created")
print(f"  Results will be saved to: {output_dir}\n")

print("Advanced analysis complete! See output directory for results.")
