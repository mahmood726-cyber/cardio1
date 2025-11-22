#!/usr/bin/env python3
"""
Generate Supplementary Materials for Paper 3: Evidence Mapping
- Supplementary Figure 1: Evidence map heat map
- Supplementary Figure 2: Temporal trends detailed
- Supplementary Table 1: Complete trial list (1,001 trials)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 9

# Create output directory
output_dir = Path('papers/supplementary/paper3')
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Generating supplementary materials for Paper 3 (Evidence Mapping)...")

# Load master dataset
df = pd.read_csv('data/processed/master_cardiovascular_metaanalysis_1001trials.csv')

# Add decade column if not present
if 'decade' not in df.columns:
    df['decade'] = (df['year'] // 10) * 10

print(f"Total trials in dataset: {len(df)}")

# =============================================================================
# Categorize trials into clinical domains
# =============================================================================

def categorize_intervention(notes, intervention):
    """Categorize trials into clinical domains"""
    text = f"{notes} {intervention}".lower()

    # Define keywords for each domain
    if any(kw in text for kw in ['heart failure', 'hf ', ' hfref', ' hfpef', 'lvef', 'ejection fraction']):
        return 'Heart Failure Pharmacotherapy'
    elif any(kw in text for kw in ['acs', 'stemi', 'nstemi', 'acute coronary', 'myocardial infarction', ' mi ']):
        return 'Acute Coronary Syndromes'
    elif any(kw in text for kw in ['hypertension', 'blood pressure', ' bp ', 'antihypertensive']):
        return 'Hypertension Management'
    elif any(kw in text for kw in ['statin', 'lipid', 'cholesterol', 'ldl', 'pcsk9']):
        return 'Lipid-Lowering Therapies'
    elif any(kw in text for kw in ['atrial fibrillation', 'af ', 'afib', 'rhythm control', 'rate control']):
        return 'Atrial Fibrillation'
    elif any(kw in text for kw in ['stent', 'pci', 'percutaneous', 'angioplasty', 'tavr', 'tavi']):
        return 'Interventional Cardiology'
    elif any(kw in text for kw in ['stroke', 'tia', 'cerebrovascular', 'carotid']):
        return 'Stroke Prevention'
    elif any(kw in text for kw in ['diabetes', 'diabetic', 'glycemic', 'sglt2', 'glp-1']):
        return 'Diabetes & CVD'
    elif any(kw in text for kw in ['icd', 'crt', 'pacemaker', 'defibrillator', 'device']):
        return 'Device Therapy'
    elif any(kw in text for kw in ['primary prevention', 'healthy', 'aspirin prevention', 'statin prevention']):
        return 'Primary Prevention'
    elif any(kw in text for kw in ['anticoagul', 'warfarin', 'dabigatran', 'rivaroxaban', 'apixaban', 'edoxaban', 'noac', 'doac']):
        return 'Anticoagulation'
    elif any(kw in text for kw in ['antiplatelet', 'aspirin', 'clopidogrel', 'prasugrel', 'ticagrelor', 'dapt']):
        return 'Antiplatelet Therapy'
    elif any(kw in text for kw in ['arrhythmia', 'vt ', 'ventricular tach', 'ablation']):
        return 'Arrhythmia Management'
    elif any(kw in text for kw in ['thromboly', 'fibrinoly', 'alteplase', 'tenecteplase']):
        return 'Thrombolysis'
    elif any(kw in text for kw in ['ace inhibitor', 'acei', 'arb ', 'angiotensin']):
        return 'RAAS Inhibition'
    else:
        return 'Other Cardiovascular'

df['domain'] = df.apply(lambda row: categorize_intervention(row['notes'], row['intervention']), axis=1)

# =============================================================================
# SUPPLEMENTARY FIGURE 1: Evidence Map Heat Map
# =============================================================================

# Create evidence matrix: Domains × Decades
evidence_matrix = pd.crosstab(df['domain'], df['decade'], values=df['n_intervention'] + df['n_control'],
                             aggfunc='sum').fillna(0)

# Sort by total patients
domain_totals = evidence_matrix.sum(axis=1).sort_values(ascending=False)
evidence_matrix = evidence_matrix.loc[domain_totals.index]

# Select top 20 domains
evidence_matrix_top = evidence_matrix.head(20)

# Create heat map
fig, ax = plt.subplots(figsize=(14, 10))

# Use log scale for better visualization
evidence_matrix_log = np.log10(evidence_matrix_top + 1)

sns.heatmap(evidence_matrix_log, annot=False, cmap='YlOrRd',
           linewidths=0.5, linecolor='gray', cbar_kws={'label': 'log₁₀(Patients + 1)'},
           ax=ax)

ax.set_xlabel('Decade', fontsize=12, fontweight='bold')
ax.set_ylabel('Clinical Domain', fontsize=12, fontweight='bold')
ax.set_title('Supplementary Figure 1: Evidence Map Heat Map\n' +
            'Distribution of Trial Participants by Clinical Domain and Decade (Top 20 Domains)',
            fontsize=13, fontweight='bold', pad=15)

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / 'SupplementaryFigure1_EvidenceMap_HeatMap.png',
            dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'SupplementaryFigure1_EvidenceMap_HeatMap.pdf',
            bbox_inches='tight')
print("✓ Created Supplementary Figure 1: Evidence map heat map")
plt.close()

# =============================================================================
# SUPPLEMENTARY FIGURE 2: Temporal Trends Detailed
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Panel A: Trials per decade
trials_per_decade = df.groupby('decade').size()
axes[0, 0].bar(trials_per_decade.index, trials_per_decade.values,
              color='#2E86AB', alpha=0.7, edgecolor='black')
axes[0, 0].set_xlabel('Decade', fontweight='bold')
axes[0, 0].set_ylabel('Number of Trials', fontweight='bold')
axes[0, 0].set_title('A. Trials Published by Decade', fontweight='bold', fontsize=11)
axes[0, 0].grid(True, alpha=0.3, axis='y')
for i, (decade, count) in enumerate(trials_per_decade.items()):
    axes[0, 0].text(decade, count + 10, str(count), ha='center', fontweight='bold')

# Panel B: Patients enrolled per decade
patients_per_decade = df.groupby('decade').apply(
    lambda x: (x['n_intervention'] + x['n_control']).sum()
)
axes[0, 1].bar(patients_per_decade.index, patients_per_decade.values / 1000,
              color='#A23B72', alpha=0.7, edgecolor='black')
axes[0, 1].set_xlabel('Decade', fontweight='bold')
axes[0, 1].set_ylabel('Patients Enrolled (thousands)', fontweight='bold')
axes[0, 1].set_title('B. Patients Enrolled by Decade', fontweight='bold', fontsize=11)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Panel C: Average trial size over time
avg_size_per_decade = df.groupby('decade').apply(
    lambda x: (x['n_intervention'] + x['n_control']).mean()
)
axes[1, 0].plot(avg_size_per_decade.index, avg_size_per_decade.values,
               marker='o', linewidth=2, markersize=8, color='#F18F01')
axes[1, 0].set_xlabel('Decade', fontweight='bold')
axes[1, 0].set_ylabel('Average Trial Size (patients)', fontweight='bold')
axes[1, 0].set_title('C. Average Trial Size Over Time', fontweight='bold', fontsize=11)
axes[1, 0].grid(True, alpha=0.3)

# Panel D: Top domains over time
top_domains = df['domain'].value_counts().head(6).index
domain_counts_over_time = pd.DataFrame()
for domain in top_domains:
    domain_counts = df[df['domain'] == domain].groupby('decade').size()
    domain_counts_over_time[domain] = domain_counts

domain_counts_over_time = domain_counts_over_time.fillna(0)
domain_counts_over_time.plot(kind='line', marker='o', ax=axes[1, 1], linewidth=2)
axes[1, 1].set_xlabel('Decade', fontweight='bold')
axes[1, 1].set_ylabel('Number of Trials', fontweight='bold')
axes[1, 1].set_title('D. Top 6 Clinical Domains Over Time', fontweight='bold', fontsize=11)
axes[1, 1].legend(loc='upper left', fontsize=8, frameon=True)
axes[1, 1].grid(True, alpha=0.3)

fig.suptitle('Supplementary Figure 2: Detailed Temporal Trends in Cardiovascular Trials (1970-2024)',
            fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(output_dir / 'SupplementaryFigure2_TemporalTrends.png',
            dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'SupplementaryFigure2_TemporalTrends.pdf',
            bbox_inches='tight')
print("✓ Created Supplementary Figure 2: Temporal trends")
plt.close()

# =============================================================================
# SUPPLEMENTARY TABLE 1: Complete Trial List
# =============================================================================

# Create comprehensive trial list
df_export = df[[
    'study_id', 'year', 'intervention', 'control', 'domain',
    'n_intervention', 'n_control', 'events_intervention', 'events_control',
    'mean_age', 'pct_male', 'mean_followup_months', 'notes'
]].copy()

df_export['total_n'] = df_export['n_intervention'] + df_export['n_control']
df_export = df_export.sort_values(['domain', 'year'])

# Save full table
df_export.to_csv(output_dir / 'SupplementaryTable1_Complete_Trial_List.csv', index=False)
print(f"✓ Created Supplementary Table 1: Complete trial list ({len(df_export)} trials)")

# Create summary statistics table
summary_stats = df.groupby('domain').agg({
    'study_id': 'count',
    'n_intervention': lambda x: (x + df.loc[x.index, 'n_control']).sum(),
    'year': ['min', 'max'],
    'mean_age': 'mean',
    'pct_male': 'mean'
}).round(1)

summary_stats.columns = ['N_Trials', 'Total_Patients', 'Year_First', 'Year_Last',
                        'Mean_Age', 'Pct_Male']
summary_stats = summary_stats.sort_values('N_Trials', ascending=False)
summary_stats.to_csv(output_dir / 'SupplementaryTable1_Summary_by_Domain.csv')
print("✓ Created Supplementary Table 1: Summary by domain")

# =============================================================================
# SUPPLEMENTARY FIGURE 3: Evidence Gap Visualization
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Panel A: Trials by domain (top 15 vs bottom 15)
domain_counts = df['domain'].value_counts()

# Top 15
ax1 = axes[0]
top15 = domain_counts.head(15)
ax1.barh(range(len(top15)), top15.values, color='#2E86AB', alpha=0.7, edgecolor='black')
ax1.set_yticks(range(len(top15)))
ax1.set_yticklabels(top15.index, fontsize=9)
ax1.set_xlabel('Number of Trials', fontweight='bold')
ax1.set_title('A. Well-Studied Domains (Top 15)', fontweight='bold', fontsize=11)
ax1.grid(True, alpha=0.3, axis='x')
ax1.invert_yaxis()

# Add trial counts
for i, (domain, count) in enumerate(top15.items()):
    ax1.text(count + 2, i, str(count), va='center', fontweight='bold')

# Bottom 15 (evidence gaps)
ax2 = axes[1]
bottom15 = domain_counts.tail(15).sort_values()
ax2.barh(range(len(bottom15)), bottom15.values, color='#DC3545', alpha=0.7, edgecolor='black')
ax2.set_yticks(range(len(bottom15)))
ax2.set_yticklabels(bottom15.index, fontsize=9)
ax2.set_xlabel('Number of Trials', fontweight='bold')
ax2.set_title('B. Evidence Gaps (Bottom 15 Domains)', fontweight='bold', fontsize=11)
ax2.grid(True, alpha=0.3, axis='x')
ax2.invert_yaxis()

# Add trial counts
for i, (domain, count) in enumerate(bottom15.items()):
    ax2.text(count + 0.3, i, str(count), va='center', fontweight='bold')

fig.suptitle('Supplementary Figure 3: Evidence Distribution - Concentrations vs Gaps',
            fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'SupplementaryFigure3_EvidenceGaps.png',
            dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'SupplementaryFigure3_EvidenceGaps.pdf',
            bbox_inches='tight')
print("✓ Created Supplementary Figure 3: Evidence gaps")
plt.close()

# =============================================================================
# Create summary statistics file
# =============================================================================

summary_text = f"""
PAPER 3 SUPPLEMENTARY MATERIALS - SUMMARY STATISTICS
{'='*70}

Total Trials: {len(df)}
Total Patients: {(df['n_intervention'] + df['n_control']).sum():,}
Year Range: {df['year'].min()}-{df['year'].max()}

Clinical Domains Identified: {df['domain'].nunique()}

TOP 10 DOMAINS BY TRIAL COUNT:
{domain_counts.head(10).to_string()}

BOTTOM 10 DOMAINS (EVIDENCE GAPS):
{domain_counts.tail(10).to_string()}

TEMPORAL DISTRIBUTION:
{trials_per_decade.to_string()}

AVERAGE TRIAL SIZE BY DECADE:
{avg_size_per_decade.round(0).to_string()}

FILES GENERATED:
- SupplementaryFigure1_EvidenceMap_HeatMap.png/pdf
- SupplementaryFigure2_TemporalTrends.png/pdf
- SupplementaryFigure3_EvidenceGaps.png/pdf
- SupplementaryTable1_Complete_Trial_List.csv
- SupplementaryTable1_Summary_by_Domain.csv

{'='*70}
"""

with open(output_dir / 'SUMMARY_STATISTICS.txt', 'w') as f:
    f.write(summary_text)

print(summary_text)

print(f"\n{'='*70}")
print(f"Paper 3 supplementary materials complete!")
print(f"Output directory: {output_dir}")
print(f"{'='*70}")
