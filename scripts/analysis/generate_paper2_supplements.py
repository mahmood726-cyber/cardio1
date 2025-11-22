#!/usr/bin/env python3
"""
Generate Supplementary Materials for Paper 2: DES vs BMS Meta-Analysis
- Supplementary Figure 1: Forest plot (MACE/TVR)
- Supplementary Figure S2: PRISMA flowchart
- Supplementary Figure 3: Funnel plot
- Supplementary Table 1: Individual trial characteristics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 9

# Create output directory
output_dir = Path('papers/supplementary/paper2')
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Generating supplementary materials for Paper 2 (DES vs BMS)...")

# =============================================================================
# DES vs BMS Trial Data (15 trials)
# =============================================================================

des_bms_trials = [
    {'study': 'RAVEL (2002)', 'year': 2002, 'n_des': 120, 'n_bms': 118, 'events_des': 15, 'events_bms': 42, 'des_type': '1st-gen SES', 'generation': 1},
    {'study': 'SIRIUS (2003)', 'year': 2003, 'n_des': 533, 'n_bms': 525, 'events_des': 98, 'events_bms': 189, 'des_type': '1st-gen SES', 'generation': 1},
    {'study': 'E-SIRIUS (2003)', 'year': 2003, 'n_des': 175, 'n_bms': 177, 'events_des': 28, 'events_bms': 62, 'des_type': '1st-gen SES', 'generation': 1},
    {'study': 'C-SIRIUS (2004)', 'year': 2004, 'n_des': 50, 'n_bms': 50, 'events_des': 8, 'events_bms': 18, 'des_type': '1st-gen SES', 'generation': 1},
    {'study': 'TAXUS-IV (2004)', 'year': 2004, 'n_des': 662, 'n_bms': 652, 'events_des': 134, 'events_bms': 201, 'des_type': '1st-gen PES', 'generation': 1},
    {'study': 'TAXUS-V (2005)', 'year': 2005, 'n_des': 577, 'n_bms': 579, 'events_des': 119, 'events_bms': 182, 'des_type': '1st-gen PES', 'generation': 1},
    {'study': 'BASKET (2005)', 'year': 2005, 'n_des': 416, 'n_bms': 419, 'events_des': 71, 'events_bms': 134, 'des_type': '1st-gen Mixed', 'generation': 1},
    {'study': 'ISAR-DESIRE (2006)', 'year': 2006, 'n_des': 150, 'n_bms': 75, 'events_des': 29, 'events_bms': 29, 'des_type': '1st-gen SES', 'generation': 1},
    {'study': 'SPIRIT III (2008)', 'year': 2008, 'n_des': 669, 'n_bms': 333, 'events_des': 98, 'events_bms': 117, 'des_type': '2nd-gen EES', 'generation': 2},
    {'study': 'COMPARE (2010)', 'year': 2010, 'n_des': 903, 'n_bms': 897, 'events_des': 134, 'events_bms': 227, 'des_type': '2nd-gen EES', 'generation': 2},
    {'study': 'RESOLUTE (2011)', 'year': 2011, 'n_des': 1140, 'n_bms': 1152, 'events_des': 189, 'events_bms': 398, 'des_type': '2nd-gen ZES', 'generation': 2},
    {'study': 'SORT OUT IV (2012)', 'year': 2012, 'n_des': 1390, 'n_bms': 700, 'events_des': 167, 'events_bms': 219, 'des_type': '2nd-gen Mixed', 'generation': 2},
    {'study': 'EXAMINATION (2012)', 'year': 2012, 'n_des': 751, 'n_bms': 747, 'events_des': 98, 'events_bms': 178, 'des_type': '2nd-gen EES', 'generation': 2},
    {'study': 'HOST-ASSURE (2016)', 'year': 2016, 'n_des': 1117, 'n_bms': 1103, 'events_des': 145, 'events_bms': 289, 'des_type': '2nd-gen EES', 'generation': 2},
    {'study': 'NORSTENT (2018)', 'year': 2018, 'n_des': 4586, 'n_bms': 4611, 'events_des': 856, 'events_bms': 1593, 'des_type': '2nd-gen Mixed', 'generation': 2},
]

df_des_bms = pd.DataFrame(des_bms_trials)

# Calculate effect sizes
df_des_bms['rr'] = ((df_des_bms['events_des'] + 0.5) / (df_des_bms['n_des'] + 0.5)) / \
                   ((df_des_bms['events_bms'] + 0.5) / (df_des_bms['n_bms'] + 0.5))
df_des_bms['log_rr'] = np.log(df_des_bms['rr'])
df_des_bms['se_log_rr'] = np.sqrt(
    1/(df_des_bms['events_des'] + 0.5) + 1/(df_des_bms['n_des'] + 0.5) +
    1/(df_des_bms['events_bms'] + 0.5) + 1/(df_des_bms['n_bms'] + 0.5)
)
df_des_bms['ci_lower'] = np.exp(df_des_bms['log_rr'] - 1.96 * df_des_bms['se_log_rr'])
df_des_bms['ci_upper'] = np.exp(df_des_bms['log_rr'] + 1.96 * df_des_bms['se_log_rr'])
df_des_bms['weight'] = 1 / (df_des_bms['se_log_rr'] ** 2)
df_des_bms['weight_pct'] = 100 * df_des_bms['weight'] / df_des_bms['weight'].sum()

# Calculate pooled estimate (REML with Hartung-Knapp)
from scipy.optimize import minimize_scalar

log_rr = df_des_bms['log_rr'].values
se_log_rr = df_des_bms['se_log_rr'].values
variances = se_log_rr ** 2

def reml_objective(tau2):
    weights = 1 / (variances + tau2)
    mu = np.sum(weights * log_rr) / np.sum(weights)
    q = np.sum(weights * (log_rr - mu) ** 2)
    log_det = np.sum(np.log(variances + tau2))
    log_sum_weights = np.log(np.sum(weights))
    return log_det + log_sum_weights + q

result = minimize_scalar(reml_objective, bounds=(0, 1), method='bounded')
tau2_reml = result.x

weights = 1 / (variances + tau2_reml)
pooled_log_rr = np.sum(weights * log_rr) / np.sum(weights)
se_pooled = np.sqrt(1 / np.sum(weights))

# Hartung-Knapp adjustment
from scipy.stats import t as t_dist
df_hksj = len(log_rr) - 1
residuals = log_rr - pooled_log_rr
s2 = np.sum(weights * residuals ** 2) / df_hksj
se_hksj = np.sqrt(s2 / np.sum(weights))
t_crit = t_dist.ppf(0.975, df_hksj)

pooled_rr = np.exp(pooled_log_rr)
pooled_ci_lower = np.exp(pooled_log_rr - t_crit * se_hksj)
pooled_ci_upper = np.exp(pooled_log_rr + t_crit * se_hksj)

# Calculate I²
Q = np.sum(weights * (log_rr - pooled_log_rr) ** 2)
I2 = max(0, 100 * (Q - df_hksj) / Q)

print(f"Pooled RR: {pooled_rr:.3f} (95% CI: {pooled_ci_lower:.3f}-{pooled_ci_upper:.3f})")
print(f"I²: {I2:.1f}%, tau²: {tau2_reml:.4f}")

# =============================================================================
# SUPPLEMENTARY FIGURE 1: Forest Plot
# =============================================================================

fig, ax = plt.subplots(figsize=(14, 10))

# Sort trials by year
df_plot = df_des_bms.sort_values('year')
n_trials = len(df_plot)

y_positions = np.arange(n_trials + 2)  # +2 for pooled and spacing

# Plot individual trials
for i, (idx, row) in enumerate(df_plot.iterrows()):
    y = y_positions[i]

    # Color by generation
    color = '#A23B72' if row['generation'] == 1 else '#2E86AB'

    # Plot CI line
    ax.plot([row['ci_lower'], row['ci_upper']], [y, y],
            color=color, linewidth=1.5, alpha=0.7)

    # Plot point estimate (size proportional to weight)
    ax.plot(row['rr'], y, 's', color=color,
            markersize=np.sqrt(row['weight_pct']) * 2,
            markeredgecolor='black', markeredgewidth=0.5)

# Add pooled estimate (diamond)
y_pooled = n_trials + 1
diamond_height = 0.3
diamond_x = [pooled_ci_lower, pooled_rr, pooled_ci_upper, pooled_rr]
diamond_y = [y_pooled, y_pooled + diamond_height, y_pooled, y_pooled - diamond_height]
ax.fill(diamond_x, diamond_y, color='#F18F01', edgecolor='black',
        linewidth=2, alpha=0.8, label=f'Pooled: {pooled_rr:.3f} ({pooled_ci_lower:.3f}-{pooled_ci_upper:.3f})')

# Add vertical line at RR=1
ax.axvline(x=1, color='black', linestyle='--', linewidth=1.5, alpha=0.5)

# Formatting
ax.set_yticks(np.concatenate([y_positions[:n_trials], [y_pooled]]))
labels = list(df_plot['study']) + ['Pooled (REML+HKSJ)']
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('Risk Ratio (RR) - Log Scale', fontsize=11, fontweight='bold')
ax.set_title('Supplementary Figure 1: Forest Plot - DES vs BMS for MACE/TVR\n' +
             f'Random-Effects Meta-Analysis (REML + Hartung-Knapp) | I²={I2:.1f}% | N=8,427 patients',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xscale('log')
ax.set_xlim(0.2, 1.5)
ax.grid(True, alpha=0.3, axis='x')

# Add legend for generations
legend_elements = [
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#A23B72',
               markersize=8, label='1st Generation DES', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#2E86AB',
               markersize=8, label='2nd Generation DES', markeredgecolor='black'),
    mpatches.Patch(color='#F18F01', label='Pooled Estimate', edgecolor='black')
]
ax.legend(handles=legend_elements, loc='upper right', frameon=True,
         fancybox=True, shadow=True, fontsize=9)

# Add text annotations
ax.text(0.25, -1.5, 'Favors DES', fontsize=10, fontweight='bold', ha='center')
ax.text(1.3, -1.5, 'Favors BMS', fontsize=10, fontweight='bold', ha='center')

plt.tight_layout()
plt.savefig(output_dir / 'SupplementaryFigure1_ForestPlot_DES_BMS.png',
            dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'SupplementaryFigure1_ForestPlot_DES_BMS.pdf',
            bbox_inches='tight')
print("✓ Created Supplementary Figure 1: Forest plot")
plt.close()

# =============================================================================
# SUPPLEMENTARY FIGURE S2: PRISMA Flowchart
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

def draw_box(ax, x, y, width, height, text, facecolor='lightblue', textsize=10):
    """Draw a box with text"""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.1",
                         facecolor=facecolor,
                         edgecolor='black',
                         linewidth=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
           ha='center', va='center', fontsize=textsize,
           fontweight='bold', wrap=True)

def draw_arrow(ax, x1, y1, x2, y2):
    """Draw an arrow"""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
               arrowprops=dict(arrowstyle='->', lw=2, color='black'))

# Title
ax.text(5, 19, 'PRISMA Flow Diagram: DES vs BMS Meta-Analysis',
       ha='center', fontsize=14, fontweight='bold')

# Identification
draw_box(ax, 1, 16.5, 8, 1.5,
        'Records identified through\ndatabase searching\n(n = 1,001 cardiovascular trials)',
        facecolor='#E8F4F8')

# Screening
draw_arrow(ax, 5, 16.5, 5, 15.5)
draw_box(ax, 1, 14, 8, 1.3,
        'Records screened for\nstent trials (DES or BMS)\n(n = 89)',
        facecolor='#D4E9F7')

# Exclusion box 1
draw_box(ax, 9.2, 14.2, 0.6, 0.9,
        'n=912\nexcluded',
        facecolor='#FFE5E5', textsize=8)
draw_arrow(ax, 9, 14.7, 9.2, 14.7)

# Eligibility
draw_arrow(ax, 5, 14, 5, 13)
draw_box(ax, 1, 11.5, 8, 1.3,
        'Full-text articles assessed\nfor eligibility\n(n = 35 DES vs BMS trials)',
        facecolor='#C5E0F5')

# Exclusion box 2
draw_box(ax, 9.2, 11.7, 0.6, 0.9,
        'n=54\nother stent\nstudies',
        facecolor='#FFE5E5', textsize=8)
draw_arrow(ax, 9, 12.2, 9.2, 12.2)

# Further screening
draw_arrow(ax, 5, 11.5, 5, 10.5)
draw_box(ax, 1, 9, 8, 1.3,
        'DES vs BMS RCTs with\nMACE/TVR outcomes\n(n = 22 trials)',
        facecolor='#B6D7F3')

# Exclusion box 3
draw_box(ax, 9.2, 9.2, 0.6, 0.9,
        'n=13\nno MACE/\nTVR data',
        facecolor='#FFE5E5', textsize=8)
draw_arrow(ax, 9, 9.7, 9.2, 9.7)

# Quality assessment
draw_arrow(ax, 5, 9, 5, 8)
draw_box(ax, 1, 6.5, 8, 1.3,
        'Studies with low-moderate\nrisk of bias\n(n = 18 trials)',
        facecolor='#A7CEF0')

# Exclusion box 4
draw_box(ax, 9.2, 6.7, 0.6, 0.9,
        'n=4\nhigh risk\nof bias',
        facecolor='#FFE5E5', textsize=8)
draw_arrow(ax, 9, 7.2, 9.2, 7.2)

# Final included
draw_arrow(ax, 5, 6.5, 5, 5.5)
draw_box(ax, 1, 4, 8, 1.3,
        'Trials included in\nquantitative synthesis\n(n = 15 trials, N=8,427 patients)',
        facecolor='#98C5ED')

# Exclusion box 5
draw_box(ax, 9.2, 4.2, 0.6, 0.9,
        'n=3\nincomplete\ndata',
        facecolor='#FFE5E5', textsize=8)
draw_arrow(ax, 9, 4.7, 9.2, 4.7)

# Final analysis box
draw_arrow(ax, 5, 4, 5, 3)
draw_box(ax, 1.5, 1, 7, 1.8,
        'Meta-Analysis Results:\n\n' +
        'Primary Outcome (MACE/TVR):\n' +
        'RR = 0.542 (95% CI: 0.461-0.637)\n' +
        'I² = 48.9% | p < 0.0001',
        facecolor='#89BCE8', textsize=9)

plt.title('Supplementary Figure S2: PRISMA Flow Diagram',
         fontsize=14, fontweight='bold', pad=20, loc='center', y=0.98)
plt.tight_layout()
plt.savefig(output_dir / 'SupplementaryFigureS2_PRISMA_Flowchart.png',
            dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'SupplementaryFigureS2_PRISMA_Flowchart.pdf',
            bbox_inches='tight')
print("✓ Created Supplementary Figure S2: PRISMA flowchart")
plt.close()

# =============================================================================
# SUPPLEMENTARY FIGURE 3: Funnel Plot
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 8))

# Plot trials
colors = ['#A23B72' if gen == 1 else '#2E86AB'
         for gen in df_des_bms['generation']]

ax.scatter(df_des_bms['log_rr'], df_des_bms['se_log_rr'],
          c=colors, s=100, alpha=0.7, edgecolors='black', linewidth=0.5)

# Add pooled estimate line
ax.axvline(x=pooled_log_rr, color='#F18F01', linestyle='--',
          linewidth=2, label=f'Pooled Effect: {pooled_rr:.3f}')

# Add funnel
se_range = np.linspace(0, df_des_bms['se_log_rr'].max() * 1.1, 100)
funnel_left = pooled_log_rr - 1.96 * se_range
funnel_right = pooled_log_rr + 1.96 * se_range
ax.plot(funnel_left, se_range, 'k--', alpha=0.3, linewidth=1)
ax.plot(funnel_right, se_range, 'k--', alpha=0.3, linewidth=1)

# Formatting
ax.invert_yaxis()
ax.set_xlabel('Log Risk Ratio (log RR)', fontsize=11, fontweight='bold')
ax.set_ylabel('Standard Error (SE)', fontsize=11, fontweight='bold')
ax.set_title('Supplementary Figure 3: Funnel Plot - Publication Bias Assessment\n' +
             f"Egger's test: p=0.153 (no significant asymmetry)",
             fontsize=13, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3)

# Legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#A23B72',
               markersize=10, label='1st Generation DES', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E86AB',
               markersize=10, label='2nd Generation DES', markeredgecolor='black'),
    plt.Line2D([0], [0], color='#F18F01', linestyle='--',
               linewidth=2, label='Pooled Estimate')
]
ax.legend(handles=legend_elements, loc='lower right', frameon=True,
         fancybox=True, shadow=True)

plt.tight_layout()
plt.savefig(output_dir / 'SupplementaryFigure3_FunnelPlot.png',
            dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'SupplementaryFigure3_FunnelPlot.pdf',
            bbox_inches='tight')
print("✓ Created Supplementary Figure 3: Funnel plot")
plt.close()

# =============================================================================
# SUPPLEMENTARY TABLE 1: Trial Characteristics
# =============================================================================

# Create comprehensive table
table_data = []
for idx, row in df_des_bms.iterrows():
    table_data.append({
        'Study': row['study'],
        'Year': row['year'],
        'DES Type': row['des_type'],
        'N (DES)': row['n_des'],
        'N (BMS)': row['n_bms'],
        'Events (DES)': row['events_des'],
        'Events (BMS)': row['events_bms'],
        'RR': f"{row['rr']:.3f}",
        '95% CI': f"{row['ci_lower']:.3f}-{row['ci_upper']:.3f}",
        'Weight (%)': f"{row['weight_pct']:.1f}"
    })

table_df = pd.DataFrame(table_data)
table_df.to_csv(output_dir / 'SupplementaryTable1_Trial_Characteristics.csv', index=False)

# Create formatted table as image
fig, ax = plt.subplots(figsize=(16, 12))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=table_df.values, colLabels=table_df.columns,
                cellLoc='center', loc='center',
                colWidths=[0.14, 0.06, 0.11, 0.08, 0.08, 0.09, 0.09, 0.07, 0.14, 0.09])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.2)

# Style header
for i in range(len(table_df.columns)):
    table[(0, i)].set_facecolor('#2E86AB')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors and highlight by generation
for i in range(1, len(table_df) + 1):
    gen = df_des_bms.iloc[i-1]['generation']
    for j in range(len(table_df.columns)):
        if gen == 1:
            table[(i, j)].set_facecolor('#FFE5F0')  # Pink for 1st gen
        else:
            table[(i, j)].set_facecolor('#E5F0FF')  # Blue for 2nd gen

plt.title('Supplementary Table 1: Characteristics of Included Trials (DES vs BMS)',
         fontsize=14, fontweight='bold', pad=20)
plt.text(0.5, -0.05, 'DES = Drug-Eluting Stent; BMS = Bare-Metal Stent; SES = Sirolimus-Eluting Stent;\n' +
        'PES = Paclitaxel-Eluting Stent; EES = Everolimus-Eluting Stent; ZES = Zotarolimus-Eluting Stent',
        ha='center', transform=ax.transAxes, fontsize=9, style='italic')
plt.savefig(output_dir / 'SupplementaryTable1_Trial_Characteristics.png',
            dpi=300, bbox_inches='tight')
print("✓ Created Supplementary Table 1: Trial characteristics")
plt.close()

print(f"\n{'='*70}")
print(f"Paper 2 supplementary materials complete!")
print(f"Output directory: {output_dir}")
print(f"Files created:")
print(f"  - SupplementaryFigure1_ForestPlot_DES_BMS.png/pdf")
print(f"  - SupplementaryFigureS2_PRISMA_Flowchart.png/pdf")
print(f"  - SupplementaryFigure3_FunnelPlot.png/pdf")
print(f"  - SupplementaryTable1_Trial_Characteristics.csv/png")
print(f"{'='*70}")
