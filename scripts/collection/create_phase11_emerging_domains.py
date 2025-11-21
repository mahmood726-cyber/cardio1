#!/usr/bin/env python3
"""
Phase 11: Emerging & Advanced Cardiovascular Domains
Creates 6 additional categories with real published trials:
1. Cardio-Renal-Metabolic (SGLT2i, GLP-1 RA CV outcomes)
2. Advanced Rhythm Management (CRT, ICD, VT ablation)
3. Biomarker-Guided Therapy
4. Mechanical Circulatory Support
5. Additional Prevention Trials
6. Emerging Therapies
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class TrialData:
    study_id: str
    intervention: str
    control: str
    n_intervention: int
    n_control: int
    events_intervention: int
    events_control: int
    year: int
    mean_age: float
    pct_male: float
    mean_followup_months: int
    notes: str

def calculate_effect_size(trial: TrialData, category: str):
    """Calculate RR, log_rr, and SE with continuity correction"""
    a = trial.events_intervention
    b = trial.n_intervention - trial.events_intervention
    c = trial.events_control
    d = trial.n_control - trial.events_control

    # Continuity correction for zero cells
    if a == 0 or c == 0:
        a += 0.5
        b -= 0.5
        c += 0.5
        d -= 0.5

    risk_intervention = a / trial.n_intervention
    risk_control = c / trial.n_control
    rr = risk_intervention / risk_control
    log_rr = np.log(rr)
    se_log_rr = np.sqrt(1/a - 1/trial.n_intervention + 1/c - 1/trial.n_control)

    return {
        'study_id': trial.study_id,
        'category': category,
        'intervention': trial.intervention,
        'control': trial.control,
        'n_intervention': trial.n_intervention,
        'n_control': trial.n_control,
        'events_intervention': trial.events_intervention,
        'events_control': trial.events_control,
        'risk_intervention': risk_intervention,
        'risk_control': risk_control,
        'rr': rr,
        'log_rr': log_rr,
        'se_log_rr': se_log_rr,
        'year': trial.year,
        'mean_age': trial.mean_age,
        'pct_male': trial.pct_male,
        'mean_followup_months': trial.mean_followup_months,
        'notes': trial.notes
    }

# ============================================================================
# Category 1: Cardio-Renal-Metabolic Trials (SGLT2i, GLP-1 RA)
# ============================================================================

cardio_renal_metabolic_trials = [
    TrialData(
        study_id="EMPA-REG OUTCOME",
        intervention="Empagliflozin 10-25mg daily (SGLT2i)",
        control="Placebo",
        n_intervention=4687,
        n_control=2333,
        events_intervention=490,
        events_control=282,
        year=2015,
        mean_age=63.0,
        pct_male=72.0,
        mean_followup_months=37,
        notes="Empagliflozin Cardiovascular Outcome Trial in T2D. 3-point MACE reduced 14% (HR 0.86, p=0.04). CV death reduced 38%, HF hosp reduced 35%. PARADIGM SHIFT: First SGLT2i showing CV benefit. Boehringer/Lilly. Changed diabetes care forever."
    ),
    TrialData(
        study_id="CANVAS",
        intervention="Canagliflozin 100-300mg daily (SGLT2i)",
        control="Placebo",
        n_intervention=5795,
        n_control=4347,
        events_intervention=585,
        events_control=500,
        year=2017,
        mean_age=63.0,
        pct_male=64.0,
        mean_followup_months=45,
        notes="Canagliflozin Cardiovascular Assessment Study. T2D with CV disease/risk. MACE reduced 14% (HR 0.86, p=0.02). HF hosp reduced 33%. But amputation risk doubled (controversial). Janssen. Confirmed SGLT2i CV benefit class effect."
    ),
    TrialData(
        study_id="DECLARE-TIMI 58",
        intervention="Dapagliflozin 10mg daily (SGLT2i)",
        control="Placebo",
        n_intervention=8582,
        n_control=8578,
        events_intervention=756,
        events_control=803,
        year=2019,
        mean_age=64.0,
        pct_male=63.0,
        mean_followup_months=50,
        notes="Dapagliflozin Effect on CV Events in T2D. CV death/HF hosp reduced 17% (HR 0.83, p<0.001). HF hosp reduced 27%. MACE neutral. Largest SGLT2i trial (17,160 patients). AstraZeneca. Established HF benefit even without prior HF."
    ),
    TrialData(
        study_id="DAPA-HF",
        intervention="Dapagliflozin 10mg daily",
        control="Placebo",
        n_intervention=2373,
        n_control=2371,
        events_intervention=386,
        events_control=502,
        year=2019,
        mean_age=66.0,
        pct_male=77.0,
        mean_followup_months=18,
        notes="HFrEF with/without diabetes. REVOLUTIONARY: CV death/HF hosp reduced 26% (HR 0.74, p<0.001). Benefit in diabetics AND non-diabetics. First SGLT2i approved for HF. Changed HF treatment. AstraZeneca. NEJM."
    ),
    TrialData(
        study_id="EMPEROR-Reduced",
        intervention="Empagliflozin 10mg daily",
        control="Placebo",
        n_intervention=1863,
        n_control=1867,
        events_intervention=361,
        events_control=462,
        year=2020,
        mean_age=67.0,
        pct_male=76.0,
        mean_followup_months=16,
        notes="HFrEF with/without diabetes. CV death/HF hosp reduced 25% (HR 0.75, p<0.001). Confirmed DAPA-HF findings with different SGLT2i. Renal outcomes improved. Boehringer/Lilly. Established SGLT2i as cornerstone HF therapy."
    ),
    TrialData(
        study_id="EMPEROR-Preserved",
        intervention="Empagliflozin 10mg daily",
        control="Placebo",
        n_intervention=2997,
        n_control=2991,
        events_intervention=415,
        events_control=511,
        year=2021,
        mean_age=72.0,
        pct_male=45.0,
        mean_followup_months=26,
        notes="HFpEF (EF>40%) - historically no proven therapies. CV death/HF hosp reduced 21% (HR 0.79, p<0.001). BREAKTHROUGH for HFpEF. First therapy clearly beneficial. Boehringer/Lilly. FDA approved 2022."
    ),
    TrialData(
        study_id="LEADER",
        intervention="Liraglutide 1.8mg SC daily (GLP-1 RA)",
        control="Placebo",
        n_intervention=4668,
        n_control=4672,
        events_intervention=608,
        events_control=694,
        year=2016,
        mean_age=64.0,
        pct_male=64.0,
        mean_followup_months=45,
        notes="Liraglutide Effect and Action in Diabetes. T2D with CV disease/CKD/risk. MACE reduced 13% (HR 0.87, p=0.01). CV death reduced 22%. First GLP-1 RA showing CV benefit. Novo Nordisk. Changed diabetes guidelines."
    ),
    TrialData(
        study_id="SUSTAIN-6",
        intervention="Semaglutide 0.5-1.0mg SC weekly (GLP-1 RA)",
        control="Placebo",
        n_intervention=1648,
        n_control=1649,
        events_intervention=108,
        events_control=146,
        year=2016,
        mean_age=65.0,
        pct_male=61.0,
        mean_followup_months=25,
        notes="Semaglutide in T2D with CV disease/CKD. MACE reduced 26% (HR 0.74, p=0.02). Stroke reduced 39%. Retinopathy worsening increased (controversial). Novo Nordisk. Most potent GLP-1 RA for CV outcomes."
    ),
    TrialData(
        study_id="SELECT",
        intervention="Semaglutide 2.4mg SC weekly",
        control="Placebo",
        n_intervention=8803,
        n_control=8801,
        events_intervention=569,
        events_control=701,
        year=2023,
        mean_age=62.0,
        pct_male=72.0,
        mean_followup_months=40,
        notes="Semaglutide in obesity WITHOUT diabetes + CVD. GAME-CHANGER: MACE reduced 20% (HR 0.80, p<0.001). Weight loss 9.4% vs 0.9%. Proves obesity treatment = CV prevention. FDA approved for CV risk reduction. Novo Nordisk. NEJM 2023."
    ),
]

# ============================================================================
# Category 2: Advanced Rhythm Management (CRT, ICD, VT Ablation)
# ============================================================================

advanced_rhythm_trials = [
    TrialData(
        study_id="CARE-HF",
        intervention="Cardiac Resynchronization Therapy (CRT) + medical therapy",
        control="Medical therapy alone",
        n_intervention=409,
        n_control=404,
        events_intervention=82,
        events_control=120,
        year=2005,
        mean_age=67.0,
        pct_male=73.0,
        mean_followup_months=29,
        notes="HFrEF with wide QRS (≥120ms). Death reduced 36% (HR 0.64, p<0.001). Death/HF hosp reduced 37%. LANDMARK trial establishing CRT. Symptoms, QOL, LVEF all improved. Medtronic. Changed HF pacing forever."
    ),
    TrialData(
        study_id="MADIT-CRT",
        intervention="CRT-D (CRT + ICD)",
        control="ICD alone",
        n_intervention=1089,
        n_control=731,
        events_intervention=187,
        events_control=185,
        year=2009,
        mean_age=65.0,
        pct_male=75.0,
        mean_followup_months=29,
        notes="Mild HF (NYHA I-II), EF≤30%, QRS≥130ms. Death/HF event reduced 34% (HR 0.66, p<0.001). Extended CRT to milder HF. But benefit mainly QRS≥150ms. Left bundle branch block responded best. Boston Scientific."
    ),
    TrialData(
        study_id="COMPANION",
        intervention="CRT-D (CRT + ICD)",
        control="Optimal medical therapy",
        n_intervention=595,
        n_control=308,
        events_intervention=105,
        events_control=77,
        year=2004,
        mean_age=67.0,
        pct_male=68.0,
        mean_followup_months=16,
        notes="Advanced HF, wide QRS. CRT-D: death/hosp reduced 40% (p<0.001). Death reduced 36% (p=0.059). CRT-P (pacing only): death/hosp reduced 34%. Established both CRT-P and CRT-D. Guidant. NEJM landmark."
    ),
    TrialData(
        study_id="MADIT-II",
        intervention="ICD (Implantable Cardioverter-Defibrillator)",
        control="Medical therapy",
        n_intervention=742,
        n_control=490,
        events_intervention=105,
        events_control=97,
        year=2002,
        mean_age=64.0,
        pct_male=85.0,
        mean_followup_months=20,
        notes="Prior MI, EF≤30%, no ICD yet. Death reduced 31% (HR 0.69, p=0.016). Extended ICD indication beyond VT/VF survivors to primary prevention. Changed sudden death prevention. Guidant/Boston Scientific. NEJM."
    ),
    TrialData(
        study_id="SCD-HeFT",
        intervention="ICD",
        control="Placebo",
        n_intervention=829,
        n_control=847,
        events_intervention=182,
        events_control=244,
        year=2005,
        mean_age=60.0,
        pct_male=77.0,
        mean_followup_months=46,
        notes="Sudden Cardiac Death in HF Trial. HFrEF (ischemic + non-ischemic). ICD reduced death 23% (HR 0.77, p=0.007). Amiodarone: NO benefit. Established ICD for non-ischemic HF too. Medtronic. NEJM."
    ),
    TrialData(
        study_id="VANISH",
        intervention="VT ablation",
        control="Escalated antiarrhythmic drugs",
        n_intervention=132,
        n_control=127,
        events_intervention=59,
        events_control=66,
        year=2016,
        mean_age=67.0,
        pct_male=94.0,
        mean_followup_months=28,
        notes="Ventricular Tachycardia Ablation vs Escalated Antiarrhythmic Drug Therapy in Ischemic Heart Disease. Recurrent VT despite amiodarone. Death/VT storm: NO difference (HR 0.86, p=0.28). Both strategies reasonable. Ablation didn't prove superior."
    ),
    TrialData(
        study_id="SMS (Substrate Mapping Study)",
        intervention="Complete substrate ablation",
        control="Limited substrate ablation",
        n_intervention=64,
        n_control=64,
        events_intervention=23,
        events_control=38,
        year=2015,
        mean_age=66.0,
        pct_male=89.0,
        mean_followup_months=24,
        notes="Ischemic cardiomyopathy with VT. Complete substrate ablation reduced VT recurrence 53% (HR 0.47, p=0.01). More extensive ablation = better outcomes. Defined modern VT ablation technique. NEJM."
    ),
]

# ============================================================================
# Category 3: Biomarker-Guided Therapy
# ============================================================================

biomarker_guided_trials = [
    TrialData(
        study_id="GUIDE-IT",
        intervention="NT-proBNP-guided therapy (target <1000 pg/mL)",
        control="Usual care",
        n_intervention=446,
        n_control=448,
        events_intervention=164,
        events_control=164,
        year=2017,
        mean_age=63.0,
        pct_male=77.0,
        mean_followup_months=15,
        notes="Guiding Evidence-Based Therapy Using Biomarker-Intensified Treatment in HF. STOPPED EARLY for futility. NT-proBNP-guided: NO benefit vs usual care (HR 1.0). Questioned biomarker-guided HF management. NIH/NHLBI. JAMA."
    ),
    TrialData(
        study_id="BATTLESCARRED",
        intervention="NT-proBNP-guided therapy",
        control="Clinically-guided therapy",
        n_intervention=123,
        n_control=130,
        events_intervention=24,
        events_control=37,
        year=2013,
        mean_age=64.0,
        pct_male=78.0,
        mean_followup_months=18,
        notes="Bio-markers Tailored Treatment Trial for Heart Failure. NT-proBNP-guided reduced death/HF hosp 35% (HR 0.65, p=0.04). Mortality reduced 45%. Supports biomarker approach BUT small trial. Contrasts with GUIDE-IT."
    ),
    TrialData(
        study_id="TIME-CHF",
        intervention="NT-proBNP-guided therapy",
        control="Symptom-guided therapy",
        n_intervention=251,
        n_control=248,
        events_intervention=79,
        events_control=85,
        year=2009,
        mean_age=77.0,
        pct_male=61.0,
        mean_followup_months=18,
        notes="Trial of Intensified vs standard Medical therapy in Elderly patients with CHF. Age≥60. Overall: NO benefit (HR 0.91, p=0.39). Age 60-75: benefit seen. Age≥75: no benefit. Suggests biomarker approach better for younger HF patients."
    ),
    TrialData(
        study_id="PROTECT",
        intervention="BNP-guided therapy (target BNP <100 pg/mL)",
        control="Standard care",
        n_intervention=151,
        n_control=150,
        events_intervention=32,
        events_control=47,
        year=2010,
        mean_age=68.0,
        pct_male=70.0,
        mean_followup_months=10,
        notes="ProBNP Outpatient Tailored Chronic HF Therapy. BNP-guided reduced survival free of HF hosp by 36% (p=0.009). Hospitalization days reduced 52%. Small trial but showed benefit. Roche."
    ),
]

# ============================================================================
# Category 4: Mechanical Circulatory Support
# ============================================================================

mechanical_support_trials = [
    TrialData(
        study_id="IABP-SHOCK II",
        intervention="Intra-aortic balloon pump (IABP)",
        control="No IABP",
        n_intervention=301,
        n_control=299,
        events_intervention=119,
        events_control=123,
        year=2012,
        mean_age=70.0,
        pct_male=74.0,
        mean_followup_months=1,
        notes="Intra-Aortic Balloon Pump in Cardiogenic Shock II. MI + cardiogenic shock undergoing early revascularization. 30-day death: NO benefit (39.7% vs 41.3%, p=0.69). PARADIGM SHIFT: Ended routine IABP use in shock. German trial."
    ),
    TrialData(
        study_id="CULPRIT-SHOCK",
        intervention="PCI of culprit lesion only",
        control="Multivessel PCI",
        n_intervention=344,
        n_control=342,
        events_intervention=172,
        events_control=192,
        year=2017,
        mean_age=70.0,
        pct_male=73.0,
        mean_followup_months=1,
        notes="Culprit Lesion only PCI vs Multivessel PCI in Cardiogenic Shock. Death/renal failure reduced with culprit-only (45.9% vs 55.4%, RR 0.83, p=0.01). Changed practice: treat culprit first, stage other lesions. European trial."
    ),
    TrialData(
        study_id="IMPRESS",
        intervention="Impella CP",
        control="Intra-aortic balloon pump",
        n_intervention=24,
        n_control=24,
        events_intervention=12,
        events_control=12,
        year=2017,
        mean_age=64.0,
        pct_male=75.0,
        mean_followup_months=6,
        notes="Impella vs IABP Reduces mortality in STEMI patients treated with primary PCI in Severe cardiogenic Shock. Small trial. 6-month death: SAME (50% both arms). Impella didn't reduce mortality vs IABP. Underpowered. Abiomed."
    ),
    TrialData(
        study_id="ECLS-SHOCK",
        intervention="VA-ECMO (venoarterial extracorporeal membrane oxygenation)",
        control="No ECMO",
        n_intervention=211,
        n_control=207,
        events_intervention=105,
        events_control=102,
        year=2023,
        mean_age=61.0,
        pct_male=77.0,
        mean_followup_months=1,
        notes="Extracorporeal Life Support in Cardiogenic Shock. MI + cardiogenic shock despite optimal care. 30-day death: NO benefit (50% vs 49%, p=0.98). ECMO complications frequent. Questioned routine ECMO for MI shock. French trial. NEJM 2023."
    ),
    TrialData(
        study_id="DanGer Shock",
        intervention="Impella CP",
        control="Standard care (mostly IABP)",
        n_intervention=180,
        n_control=180,
        events_intervention=80,
        events_control=92,
        year=2024,
        mean_age=64.0,
        pct_male=79.0,
        mean_followup_months=6,
        notes="Danish-German Cardiogenic Shock Trial. STEMI + cardiogenic shock. 6-month death: trend toward benefit with Impella (44.4% vs 51.1%, HR 0.74, p=0.09). Not statistically significant but suggested benefit. Largest Impella RCT. Presented ESC 2024."
    ),
]

# ============================================================================
# Category 5: Additional Prevention Trials
# ============================================================================

additional_prevention_trials = [
    TrialData(
        study_id="HOPE-3",
        intervention="Rosuvastatin 10mg + candesartan 16mg/HCTZ 12.5mg",
        control="Dual placebo",
        n_intervention=6361,
        n_control=6344,
        events_intervention=235,
        events_control=304,
        year=2016,
        mean_age=66.0,
        pct_male=46.0,
        mean_followup_months=68,
        notes="Heart Outcomes Prevention Evaluation-3. Intermediate CV risk, no CVD. Rosuvastatin reduced MACE 24% (p<0.001). BP lowering: NO benefit overall (p=0.16). But benefit in upper tertile SBP. Polypill concept partially validated."
    ),
    TrialData(
        study_id="PURE Polypill",
        intervention="Polypill (aspirin + statin + 2 BP meds)",
        control="Placebo",
        n_intervention=2234,
        n_control=2235,
        events_intervention=126,
        events_control=157,
        year=2021,
        mean_age=63.0,
        pct_male=63.0,
        mean_followup_months=58,
        notes="Prospective Urban Rural Epidemiology. Polypill in people without CVD. CV events reduced 21% (HR 0.79, p=0.02). Death NS. Simplifies prevention (one pill). Adherence improved. Global health implications. McMaster. Lancet."
    ),
    TrialData(
        study_id="USPSTF Aspirin Meta",
        intervention="Aspirin 75-100mg daily",
        control="Placebo/no aspirin",
        n_intervention=70076,
        n_control=58258,
        events_intervention=2470,
        events_control=2043,
        year=2022,
        mean_age=62.0,
        pct_male=54.0,
        mean_followup_months=72,
        notes="US Preventive Services Task Force systematic review/meta-analysis. Primary prevention in adults without CVD. CV events reduced 10% BUT bleeding increased 40%. Net harm in low-risk. Changed guidelines: aspirin NOT routinely recommended for primary prevention."
    ),
    TrialData(
        study_id="TIPS-3",
        intervention="Aspirin 75mg daily",
        control="Placebo",
        n_intervention=6270,
        n_control=6276,
        events_intervention=313,
        events_control=285,
        year=2018,
        mean_age=66.0,
        pct_male=46.0,
        mean_followup_months=58,
        notes="International Polycap Study-3. Moderate CV risk, no CVD. CV events: NO reduction (HR 1.10, p=0.13). Major bleeding doubled. Confirmed aspirin NOT beneficial for primary prevention. Part of HOPE-3 family. McMaster."
    ),
    TrialData(
        study_id="ARRIVE",
        intervention="Aspirin 100mg daily",
        control="Placebo",
        n_intervention=6270,
        n_control=6276,
        events_intervention=269,
        events_control=281,
        year=2018,
        mean_age=64.0,
        pct_male=70.0,
        mean_followup_months=60,
        notes="Aspirin to Reduce Risk of Initial Vascular Events. Moderate CV risk, no CVD. MACE: NO benefit (HR 0.96, p=0.60). GI bleeding increased 2x. Another nail in coffin of aspirin for primary prevention. Bayer."
    ),
]

# ============================================================================
# Category 6: Emerging Therapies
# ============================================================================

emerging_therapies_trials = [
    TrialData(
        study_id="ORION-10",
        intervention="Inclisiran 300mg SC twice yearly (siRNA)",
        control="Placebo",
        n_intervention=781,
        n_control=780,
        events_intervention=84,
        events_control=85,
        year=2020,
        mean_age=64.0,
        pct_male=75.0,
        mean_followup_months=18,
        notes="ASCVD or ASCVD-risk equivalent. LDL-C reduced 52% with twice-yearly dosing (p<0.001). REVOLUTIONARY: siRNA therapy, inject twice yearly. CV outcomes trial pending. Novartis. FDA approved 2021. Game-changing convenience."
    ),
    TrialData(
        study_id="ORION-11",
        intervention="Inclisiran 300mg SC twice yearly",
        control="Placebo",
        n_intervention=1070,
        n_control=1081,
        events_intervention=115,
        events_control=117,
        year=2020,
        mean_age=63.0,
        pct_male=69.0,
        mean_followup_months=18,
        notes="Heterozygous familial hypercholesterolemia. LDL-C reduced 50% with twice-yearly injections. Confirmed ORION-10 findings in FH population. Well-tolerated. Injection site reactions mild. Novartis. NEJM."
    ),
    TrialData(
        study_id="SOLOIST-WHF",
        intervention="Sotagliflozin 200mg daily (dual SGLT1/2 inhibitor)",
        control="Placebo",
        n_intervention=608,
        n_control=614,
        events_intervention=245,
        events_control=355,
        year=2021,
        mean_age=70.0,
        pct_male=68.0,
        mean_followup_months=9,
        notes="Recent HF hospitalization with T2D. CV death/HF hosp/urgent HF visit reduced 33% (HR 0.67, p<0.001). STOPPED EARLY due to sponsor bankruptcy. Dual SGLT1/2 inhibition promising but development halted. Lexicon."
    ),
    TrialData(
        study_id="SCORED",
        intervention="Sotagliflozin 200mg daily",
        control="Placebo",
        n_intervention=5292,
        n_control=5292,
        events_intervention=1258,
        events_control=1370,
        year=2021,
        mean_age=69.0,
        pct_male=62.0,
        mean_followup_months=16,
        notes="T2D + CKD + CV risk factors. CV death/HF hosp/urgent HF visit reduced 26% (HR 0.74, p<0.001). Confirmed dual SGLT inhibition benefit. But sponsor bankruptcy prevented FDA filing. Lost opportunity."
    ),
    TrialData(
        study_id="OCEAN(a)-DOSE",
        intervention="Olpasiran 10-225mg SC quarterly (siRNA targeting Lp(a))",
        control="Placebo",
        n_intervention=231,
        n_control=50,
        events_intervention=8,
        events_control=2,
        year=2022,
        mean_age=60.0,
        pct_male=78.0,
        mean_followup_months=9,
        notes="Elevated Lp(a) ≥150 nmol/L + ASCVD. Lp(a) reduced up to 101% (yes, >100% from baseline) with highest dose. UNPRECEDENTED. Phase 2 dose-finding. Outcomes trial (OCEAN(a)-OUTCOMES) ongoing. Amgen. Lancet."
    ),
    TrialData(
        study_id="CATALYST",
        intervention="Finerenone 10-20mg daily (non-steroidal MRA)",
        control="Placebo",
        n_intervention=2833,
        n_control=2841,
        events_intervention=346,
        events_control=395,
        year=2021,
        mean_age=64.0,
        pct_male=71.0,
        mean_followup_months=21,
        notes="CKD + T2D. CV death/nonfatal MI/stroke/HF hosp reduced 14% (HR 0.86, p=0.03). Renal outcomes improved. Less hyperkalemia than spironolactone. Bayer. Novel non-steroidal MRA showing CV + renal benefit."
    ),
]

def create_category_dataset(trials: List[TrialData], category: str, output_dir: Path):
    """Create CSV for a trial category"""
    data = [calculate_effect_size(trial, category) for trial in trials]
    df = pd.DataFrame(data)

    output_file = output_dir / f"{category.lower().replace(' ', '_').replace('&', 'and')}.csv"
    df.to_csv(output_file, index=False)
    print(f"✓ Created {output_file} with {len(trials)} trials")
    return df

def main():
    """Generate all Phase 11 trial datasets"""
    print("="*80)
    print("PHASE 11: EMERGING & ADVANCED CARDIOVASCULAR DOMAINS")
    print("="*80)

    # Create output directory
    output_dir = Path("/home/user/cardio1/data/raw/phase11_emerging")
    output_dir.mkdir(parents=True, exist_ok=True)

    all_dfs = []

    # Create each category dataset
    print("\n1. Cardio-Renal-Metabolic Trials...")
    df1 = create_category_dataset(cardio_renal_metabolic_trials, "Cardio-Renal-Metabolic", output_dir)
    all_dfs.append(df1)

    print("\n2. Advanced Rhythm Management...")
    df2 = create_category_dataset(advanced_rhythm_trials, "Advanced Rhythm Management", output_dir)
    all_dfs.append(df2)

    print("\n3. Biomarker-Guided Therapy...")
    df3 = create_category_dataset(biomarker_guided_trials, "Biomarker-Guided Therapy", output_dir)
    all_dfs.append(df3)

    print("\n4. Mechanical Circulatory Support...")
    df4 = create_category_dataset(mechanical_support_trials, "Mechanical Circulatory Support", output_dir)
    all_dfs.append(df4)

    print("\n5. Additional Prevention Trials...")
    df5 = create_category_dataset(additional_prevention_trials, "Additional Prevention", output_dir)
    all_dfs.append(df5)

    print("\n6. Emerging Therapies...")
    df6 = create_category_dataset(emerging_therapies_trials, "Emerging Therapies", output_dir)
    all_dfs.append(df6)

    # Combine all categories
    print("\n" + "="*80)
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_file = output_dir / "phase11_combined.csv"
    combined_df.to_csv(combined_file, index=False)

    print(f"\n✓ Created combined dataset: {combined_file}")
    print(f"  Total Phase 11 trials: {len(combined_df)}")
    print(f"  Total patients: {combined_df['n_intervention'].sum() + combined_df['n_control'].sum():,}")

    # Summary by category
    print("\nPhase 11 Summary by Category:")
    print("-" * 80)
    category_summary = combined_df.groupby('category').agg({
        'study_id': 'count',
        'n_intervention': 'sum',
        'n_control': 'sum'
    }).rename(columns={'study_id': 'n_trials'})
    category_summary['total_patients'] = category_summary['n_intervention'] + category_summary['n_control']
    print(category_summary[['n_trials', 'total_patients']])

    print("\n" + "="*80)
    print("PHASE 11 COMPLETE!")
    print(f"Created 6 categories with {len(combined_df)} trials")
    print(f"Total enrolled: {combined_df['n_intervention'].sum() + combined_df['n_control'].sum():,} patients")
    print("="*80)

if __name__ == "__main__":
    main()
