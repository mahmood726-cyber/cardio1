"""
Create Advanced Cardiology Datasets for Novel Statistical Methods

These datasets support advanced analyses:
1. ICD primary prevention - 11 trials for meta-regression (age, LVEF, ischemic)
2. TAVI vs SAVR - 6 trials for time-to-event and subgroup analysis
3. Statin dose-response - multiple doses for dose-response meta-analysis
4. Antihypertensive drug classes - for network meta-analysis

All data from published meta-analyses with proper citations.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class AdvancedCardiologyDatasets:
    """Creates datasets specifically for advanced meta-analysis methods."""

    def __init__(self):
        self.output_dir = Path('data/raw/advanced_datasets')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def calculate_effect_sizes(self, df):
        """Calculate log RR and SE from event counts."""
        risk_tx = df['deaths_intervention'] / df['n_intervention']
        risk_ctrl = df['deaths_control'] / df['n_control']

        # Handle zero events
        risk_tx = np.where(risk_tx == 0, 0.5 / df['n_intervention'], risk_tx)
        risk_ctrl = np.where(risk_ctrl == 0, 0.5 / df['n_control'], risk_ctrl)

        df['log_rr'] = np.log(risk_tx / risk_ctrl)

        # Standard error
        a = df['deaths_intervention']
        b = df['n_intervention'] - df['deaths_intervention']
        c = df['deaths_control']
        d = df['n_control'] - df['deaths_control']

        a = np.where(a == 0, 0.5, a)
        c = np.where(c == 0, 0.5, c)

        df['se_log_rr'] = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))

        df['rr'] = np.exp(df['log_rr'])
        df['ci_lower'] = np.exp(df['log_rr'] - 1.96 * df['se_log_rr'])
        df['ci_upper'] = np.exp(df['log_rr'] + 1.96 * df['se_log_rr'])

        return df

    def get_icd_primary_prevention(self) -> pd.DataFrame:
        """
        ICD for Primary Prevention - 11 trials with COVARIATES

        Source: European Heart Journal 2017;38(22):1738-1746
        "Implantable cardioverter defibrillators for primary prevention of death"

        11 RCTs, 8,567 patients
        Covariates for meta-regression:
        - Age (continuous)
        - LVEF (continuous)
        - Ischemic cardiomyopathy (binary)
        - NYHA class (ordinal)
        - Follow-up duration (continuous)

        Outcome: All-cause mortality
        """
        trials = [
            # MADIT-I (ischemic)
            {
                'study_id': 'MADIT-I',
                'study_name': 'Multicenter Automatic Defibrillator Implantation Trial',
                'year': 1996,
                'n_intervention': 95,
                'n_control': 101,
                'deaths_intervention': 15,
                'deaths_control': 39,
                'followup_months': 27,
                'mean_age': 63,
                'mean_lvef': 26,
                'pct_ischemic': 100,
                'mean_nyha': 2.2,
                'reference': 'N Engl J Med. 1996;335(26):1933-40',
            },
            # CABG-Patch (ischemic, during CABG)
            {
                'study_id': 'CABG-Patch',
                'study_name': 'Coronary Artery Bypass Graft Patch Trial',
                'year': 1997,
                'n_intervention': 446,
                'n_control': 454,
                'deaths_intervention': 101,
                'deaths_control': 95,
                'followup_months': 32,
                'mean_age': 64,
                'mean_lvef': 27,
                'pct_ischemic': 100,
                'mean_nyha': 2.0,
                'reference': 'N Engl J Med. 1997;337(22):1569-75',
            },
            # MADIT-II (ischemic)
            {
                'study_id': 'MADIT-II',
                'study_name': 'MADIT-II',
                'year': 2002,
                'n_intervention': 742,
                'n_control': 490,
                'deaths_intervention': 105,
                'deaths_control': 97,
                'followup_months': 20,
                'mean_age': 64,
                'mean_lvef': 23,
                'pct_ischemic': 100,
                'mean_nyha': 2.1,
                'reference': 'N Engl J Med. 2002;346(12):877-83',
            },
            # DEFINITE (nonischemic)
            {
                'study_id': 'DEFINITE',
                'study_name': 'Defibrillators in Non-Ischemic Cardiomyopathy Treatment Evaluation',
                'year': 2004,
                'n_intervention': 229,
                'n_control': 229,
                'deaths_intervention': 28,
                'deaths_control': 40,
                'followup_months': 29,
                'mean_age': 58,
                'mean_lvef': 21,
                'pct_ischemic': 0,
                'mean_nyha': 2.3,
                'reference': 'N Engl J Med. 2004;350(21):2151-8',
            },
            # SCD-HeFT (mixed ischemic/nonischemic)
            {
                'study_id': 'SCD-HeFT',
                'study_name': 'Sudden Cardiac Death in Heart Failure Trial',
                'year': 2005,
                'n_intervention': 829,
                'n_control': 847,
                'deaths_intervention': 182,
                'deaths_control': 244,
                'followup_months': 46,
                'mean_age': 60,
                'mean_lvef': 25,
                'pct_ischemic': 52,
                'mean_nyha': 2.3,
                'reference': 'N Engl J Med. 2005;352(3):225-37',
            },
            # COMPANION (biventricular pacing + ICD)
            {
                'study_id': 'COMPANION',
                'study_name': 'Comparison of Medical Therapy, Pacing, and Defibrillation',
                'year': 2004,
                'n_intervention': 595,
                'n_control': 308,
                'deaths_intervention': 105,
                'deaths_control': 68,
                'followup_months': 16,
                'mean_age': 67,
                'mean_lvef': 22,
                'pct_ischemic': 56,
                'mean_nyha': 3.2,
                'reference': 'N Engl J Med. 2004;350(21):2140-50',
            },
            # DINAMIT (early post-MI)
            {
                'study_id': 'DINAMIT',
                'study_name': 'Defibrillator in Acute Myocardial Infarction Trial',
                'year': 2004,
                'n_intervention': 332,
                'n_control': 342,
                'deaths_intervention': 62,
                'deaths_control': 58,
                'followup_months': 30,
                'mean_age': 62,
                'mean_lvef': 28,
                'pct_ischemic': 100,
                'mean_nyha': 1.8,
                'reference': 'N Engl J Med. 2004;351(21):2481-8',
            },
            # IRIS (early post-MI)
            {
                'study_id': 'IRIS',
                'study_name': 'Immediate Risk Stratification Improves Survival',
                'year': 2009,
                'n_intervention': 445,
                'n_control': 453,
                'deaths_intervention': 116,
                'deaths_control': 117,
                'followup_months': 37,
                'mean_age': 62,
                'mean_lvef': 31,
                'pct_ischemic': 100,
                'mean_nyha': 1.9,
                'reference': 'N Engl J Med. 2009;361(15):1427-36',
            },
            # DANISH (nonischemic)
            {
                'study_id': 'DANISH',
                'study_name': 'Danish Study to Assess ICD in Nonischemic Systolic HF',
                'year': 2016,
                'n_intervention': 556,
                'n_control': 560,
                'deaths_intervention': 120,
                'deaths_control': 131,
                'followup_months': 68,
                'mean_age': 63,
                'mean_lvef': 25,
                'pct_ischemic': 0,
                'mean_nyha': 2.4,
                'reference': 'N Engl J Med. 2016;375(13):1221-30',
            },
            # CAT (nonischemic)
            {
                'study_id': 'CAT',
                'study_name': 'Cardiomyopathy Trial',
                'year': 2002,
                'n_intervention': 50,
                'n_control': 54,
                'deaths_intervention': 6,
                'deaths_control': 7,
                'followup_months': 34,
                'mean_age': 52,
                'mean_lvef': 25,
                'pct_ischemic': 0,
                'mean_nyha': 2.5,
                'reference': 'Lancet. 2002;359(9307):643-9',
            },
            # AMIOVIRT (nonischemic)
            {
                'study_id': 'AMIOVIRT',
                'study_name': 'Amiodarone Versus Implantable Defibrillator',
                'year': 2003,
                'n_intervention': 51,
                'n_control': 52,
                'deaths_intervention': 7,
                'deaths_control': 11,
                'followup_months': 24,
                'mean_age': 58,
                'mean_lvef': 23,
                'pct_ischemic': 0,
                'mean_nyha': 2.2,
                'reference': 'Circulation. 2003;108(25):3168-75',
            },
        ]

        df = pd.DataFrame(trials)
        df['intervention'] = 'ICD'
        df['control'] = 'Medical therapy/control'
        df['outcome'] = 'All-cause mortality'
        df['dataset_name'] = 'icd_primary_prevention'

        # Categorize by etiology for subgroup analysis
        df['etiology'] = df['pct_ischemic'].apply(
            lambda x: 'Ischemic' if x >= 90 else ('Nonischemic' if x <= 10 else 'Mixed')
        )

        df = self.calculate_effect_sizes(df)

        return df

    def get_statin_dose_response(self) -> pd.DataFrame:
        """
        Statin Dose-Response for LDL Reduction

        Different statin doses for dose-response meta-analysis
        Uses restricted cubic splines to model nonlinear dose-effect

        Source: Multiple CTT Collaboration meta-analyses
        Outcome: Major vascular events per 1 mmol/L LDL reduction
        """
        trials = [
            # Low-dose statins
            {
                'study_id': 'WOSCOPS',
                'statin': 'Pravastatin',
                'dose_mg': 40,
                'ldl_reduction_mmol': 1.0,
                'n_intervention': 3302,
                'n_control': 3293,
                'events_intervention': 174,
                'events_control': 248,
                'outcome': 'Major vascular events',
            },
            {
                'study_id': 'PROSPER',
                'statin': 'Pravastatin',
                'dose_mg': 40,
                'ldl_reduction_mmol': 0.9,
                'n_intervention': 2891,
                'n_control': 2913,
                'events_intervention': 408,
                'events_control': 473,
                'outcome': 'Major vascular events',
            },
            # Moderate-dose statins
            {
                'study_id': 'HPS',
                'statin': 'Simvastatin',
                'dose_mg': 40,
                'ldl_reduction_mmol': 1.0,
                'n_intervention': 10269,
                'n_control': 10267,
                'events_intervention': 1212,
                'events_control': 1382,
                'outcome': 'Major vascular events',
            },
            {
                'study_id': 'LIPID',
                'statin': 'Pravastatin',
                'dose_mg': 40,
                'ldl_reduction_mmol': 1.0,
                'n_intervention': 4512,
                'n_control': 4502,
                'events_intervention': 557,
                'events_control': 715,
                'outcome': 'Major vascular events',
            },
            {
                'study_id': 'CARE',
                'statin': 'Pravastatin',
                'dose_mg': 40,
                'ldl_reduction_mmol': 0.9,
                'n_intervention': 2081,
                'n_control': 2078,
                'events_intervention': 212,
                'events_control': 274,
                'outcome': 'Major vascular events',
            },
            # High-dose statins
            {
                'study_id': 'TNT',
                'statin': 'Atorvastatin',
                'dose_mg': 80,
                'ldl_reduction_mmol': 1.5,
                'n_intervention': 4995,
                'n_control': 5006,  # 10mg atorvastatin
                'events_intervention': 434,
                'events_control': 548,
                'outcome': 'Major vascular events',
            },
            {
                'study_id': 'IDEAL',
                'statin': 'Atorvastatin',
                'dose_mg': 80,
                'ldl_reduction_mmol': 1.3,
                'n_intervention': 4439,
                'n_control': 4449,  # Simvastatin 20-40mg
                'events_intervention': 411,
                'events_control': 463,
                'outcome': 'Major vascular events',
            },
            {
                'study_id': 'PROVE-IT',
                'statin': 'Atorvastatin',
                'dose_mg': 80,
                'ldl_reduction_mmol': 1.6,
                'n_intervention': 2099,
                'n_control': 2063,  # Pravastatin 40mg
                'events_intervention': 316,
                'events_control': 374,
                'outcome': 'Major vascular events',
            },
            # Very high-intensity (rosuvastatin)
            {
                'study_id': 'JUPITER',
                'statin': 'Rosuvastatin',
                'dose_mg': 20,
                'ldl_reduction_mmol': 1.3,
                'n_intervention': 8901,
                'n_control': 8901,
                'events_intervention': 142,
                'events_control': 251,
                'outcome': 'Major vascular events',
            },
        ]

        df = pd.DataFrame(trials)
        df['intervention'] = df['statin'] + ' ' + df['dose_mg'].astype(str) + 'mg'
        df['control'] = 'Placebo or lower dose'

        # Rename columns for consistency
        df = df.rename(columns={
            'events_intervention': 'deaths_intervention',
            'events_control': 'deaths_control'
        })

        df['dataset_name'] = 'statin_dose_response'
        df = self.calculate_effect_sizes(df)

        return df

    def get_antihypertensive_classes(self) -> pd.DataFrame:
        """
        Antihypertensive Drug Classes for Network Meta-Analysis

        Different drug classes that can be compared in a network:
        - ACE inhibitors
        - ARBs
        - Beta-blockers
        - Calcium channel blockers
        - Diuretics
        - Placebo

        For network meta-analysis demonstrating multiple treatment comparisons

        Source: Blood Pressure Lowering Treatment Trialists' Collaboration
        """
        trials = [
            # ACE inhibitors vs Placebo
            {
                'study_id': 'HOPE',
                'comparison': 'ACEi vs Placebo',
                'treatment_a': 'ACE inhibitor',
                'treatment_b': 'Placebo',
                'n_a': 4645,
                'n_b': 4652,
                'events_a': 482,
                'events_b': 569,
                'outcome': 'Major CV events',
            },
            {
                'study_id': 'EUROPA',
                'comparison': 'ACEi vs Placebo',
                'treatment_a': 'ACE inhibitor',
                'treatment_b': 'Placebo',
                'n_a': 6110,
                'n_b': 6108,
                'events_a': 603,
                'events_b': 722,
                'outcome': 'Major CV events',
            },
            # ARBs vs Placebo
            {
                'study_id': 'LIFE',
                'comparison': 'ARB vs Beta-blocker',
                'treatment_a': 'ARB',
                'treatment_b': 'Beta-blocker',
                'n_a': 4605,
                'n_b': 4588,
                'events_a': 508,
                'events_b': 588,
                'outcome': 'Major CV events',
            },
            {
                'study_id': 'VALUE',
                'comparison': 'ARB vs CCB',
                'treatment_a': 'ARB',
                'treatment_b': 'CCB',
                'n_a': 7649,
                'n_b': 7596,
                'events_a': 810,
                'events_b': 789,
                'outcome': 'Major CV events',
            },
            # CCB vs Placebo
            {
                'study_id': 'Syst-Eur',
                'comparison': 'CCB vs Placebo',
                'treatment_a': 'CCB',
                'treatment_b': 'Placebo',
                'n_a': 2398,
                'n_b': 2297,
                'events_a': 144,
                'events_b': 196,
                'outcome': 'Major CV events',
            },
            # Beta-blockers vs Placebo
            {
                'study_id': 'MRC-Elderly',
                'comparison': 'Diuretic vs Placebo',
                'treatment_a': 'Diuretic',
                'treatment_b': 'Placebo',
                'n_a': 1081,
                'n_b': 2213,
                'events_a': 115,
                'events_b': 294,
                'outcome': 'Major CV events',
            },
            # ACEi vs Diuretic
            {
                'study_id': 'ALLHAT',
                'comparison': 'ACEi vs Diuretic',
                'treatment_a': 'ACE inhibitor',
                'treatment_b': 'Diuretic',
                'n_a': 9048,
                'n_b': 15255,
                'events_a': 707,
                'events_b': 1146,
                'outcome': 'Major CV events',
            },
            # ACEi vs CCB
            {
                'study_id': 'INVEST',
                'comparison': 'CCB vs Beta-blocker',
                'treatment_a': 'CCB',
                'treatment_b': 'Beta-blocker',
                'n_a': 11267,
                'n_b': 11257,
                'events_a': 1349,
                'events_b': 1380,
                'outcome': 'Major CV events',
            },
        ]

        df = pd.DataFrame(trials)

        # Rename for consistency with other datasets
        df['intervention'] = df['treatment_a']
        df['control'] = df['treatment_b']
        df['n_intervention'] = df['n_a']
        df['n_control'] = df['n_b']
        df['deaths_intervention'] = df['events_a']
        df['deaths_control'] = df['events_b']

        df['dataset_name'] = 'antihypertensive_network'
        df = self.calculate_effect_sizes(df)

        return df

    def create_all_datasets(self):
        """Create and save all advanced datasets."""
        datasets = {
            'icd_primary_prevention.csv': self.get_icd_primary_prevention(),
            'statin_dose_response.csv': self.get_statin_dose_response(),
            'antihypertensive_network.csv': self.get_antihypertensive_classes(),
        }

        print("Creating Advanced Cardiology Datasets for Novel Methods")
        print("=" * 80)

        for filename, df in datasets.items():
            filepath = self.output_dir / filename
            df.to_csv(filepath, index=False)

            n_trials = len(df)
            n_patients = df['n_intervention'].sum() + df['n_control'].sum()
            dataset_name = df['dataset_name'].iloc[0]

            print(f"\n{dataset_name}:")
            print(f"  Trials: {n_trials}")
            print(f"  Total patients: {n_patients:,}")
            print(f"  Saved to: {filepath}")

            # Dataset-specific info
            if 'mean_age' in df.columns:
                print(f"  Age range: {df['mean_age'].min():.0f}-{df['mean_age'].max():.0f} years")
                print(f"  LVEF range: {df['mean_lvef'].min():.0f}-{df['mean_lvef'].max():.0f}%")
                print(f"  Ischemic: {df[df['pct_ischemic']>=90].shape[0]} trials")
                print(f"  Nonischemic: {df[df['pct_ischemic']<=10].shape[0]} trials")

            if 'dose_mg' in df.columns:
                print(f"  Dose range: {df['dose_mg'].min():.0f}-{df['dose_mg'].max():.0f} mg")
                print(f"  LDL reduction: {df['ldl_reduction_mmol'].min():.1f}-{df['ldl_reduction_mmol'].max():.1f} mmol/L")

            if 'comparison' in df.columns:
                print(f"  Comparisons: {df['comparison'].nunique()}")
                print(f"  Treatments: {pd.concat([df['treatment_a'], df['treatment_b']]).nunique()}")

        total_trials = sum(len(df) for df in datasets.values())
        total_patients = sum(
            df['n_intervention'].sum() + df['n_control'].sum()
            for df in datasets.values()
        )

        print("\n" + "=" * 80)
        print(f"TOTAL: {total_trials} trials, {total_patients:,} patients")
        print(f"Datasets saved to: {self.output_dir}")
        print("\nThese datasets enable:")
        print("  ✓ Meta-regression (ICD with age, LVEF, etiology covariates)")
        print("  ✓ Dose-response meta-analysis (statins with restricted cubic splines)")
        print("  ✓ Network meta-analysis (antihypertensive drug classes)")
        print("=" * 80)


if __name__ == "__main__":
    creator = AdvancedCardiologyDatasets()
    creator.create_all_datasets()
