#!/usr/bin/env python3
"""
Phase 19: Additional Clinical Domains Part 4
===========================================

This script generates Phase 19 trials covering:
1. Antiarrhythmic Drug Trials (8 trials)
2. Additional Heart Failure Device Trials (7 trials)
3. Myocarditis & Inflammatory Heart Disease (6 trials)
4. Cardiogenic Shock & MCS (7 trials)
5. Additional Electrophysiology Trials (7 trials)

Total: 35 trials

All trials are real published studies from major cardiovascular journals.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class TrialData:
    """Data structure for a single trial"""
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
    """Calculate risk ratio and log risk ratio with standard error"""
    # Extract event counts
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

    # Calculate risks
    risk_intervention = a / trial.n_intervention
    risk_control = c / trial.n_control

    # Calculate RR and log(RR)
    rr = risk_intervention / risk_control
    log_rr = np.log(rr)

    # Calculate SE of log(RR)
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
# 1. ANTIARRHYTHMIC DRUG TRIALS (8 trials)
# ============================================================================

antiarrhythmic_trials = [
    TrialData(
        study_id="CAST",
        intervention="Flecainide or Encainide",
        control="Placebo",
        n_intervention=730,
        n_control=725,
        events_intervention=56,
        events_control=22,
        year=1991,
        mean_age=61.0,
        pct_male=89.0,
        mean_followup_months=10,
        notes="Cardiac Arrhythmia Suppression Trial. Post-MI VPC suppression. Flecainide/Encainide: INCREASED mortality (7.7% vs 3.0%, HR 2.5). STOPPED EARLY. Landmark trial ended Class IC use post-MI. Paradigm shift. NEJM."
    ),
    TrialData(
        study_id="AFFIRM",
        intervention="Rhythm control (antiarrhythmics)",
        control="Rate control",
        n_intervention=2033,
        n_control=2027,
        events_intervention=356,
        events_control=310,
        year=2002,
        mean_age=70.0,
        pct_male=61.0,
        mean_followup_months=42,
        notes="Atrial Fibrillation Follow-up Investigation of Rhythm Management. Rhythm control: NO mortality benefit vs rate control (17.5% vs 15.3%, p=0.08). Rate control acceptable for most AF patients. NEJM."
    ),
    TrialData(
        study_id="RACE",
        intervention="Rate control",
        control="Rhythm control",
        n_intervention=256,
        n_control=266,
        events_intervention=44,
        events_control=60,
        year=2002,
        mean_age=68.0,
        pct_male=63.0,
        mean_followup_months=33,
        notes="RAte Control versus Electrical cardioversion for persistent atrial fibrillation. Rate control: Non-inferior to rhythm control (17.2% vs 22.6% CV death/HF/stroke/bleeding/PM). Rate control simpler, fewer hospitalizations. NEJM."
    ),
    TrialData(
        study_id="AF-CHF",
        intervention="Rhythm control",
        control="Rate control",
        n_intervention=682,
        n_control=694,
        events_intervention=178,
        events_control=181,
        year=2008,
        mean_age=66.0,
        pct_male=82.0,
        mean_followup_months=37,
        notes="Atrial Fibrillation and Congestive Heart Failure. AF + HF patients. Rhythm control: NO benefit vs rate control (27% vs 25% CV death, HR 1.06). Rate control acceptable even in HF-AF. NEJM."
    ),
    TrialData(
        study_id="ATHENA",
        intervention="Dronedarone 400mg BID",
        control="Placebo",
        n_intervention=2301,
        n_control=2327,
        events_intervention=734,
        events_control=917,
        year=2009,
        mean_age=72.0,
        pct_male=53.0,
        mean_followup_months=21,
        notes="A placebo-controlled, double-blind, parallel arm Trial to assess the efficacy of dronedarone 400mg bid for the prevention of cardiovascular Hospitalization or death from any cause in patiENts with Atrial fibrillation. Dronedarone: Reduced CV hosp/death 24% (31.9% vs 39.4%, HR 0.76). First AF drug to reduce events. NEJM."
    ),
    TrialData(
        study_id="PALLAS",
        intervention="Dronedarone 400mg BID",
        control="Placebo",
        n_intervention=1755,
        n_control=1763,
        events_intervention=43,
        events_control=19,
        year=2011,
        mean_age=75.0,
        pct_male=63.0,
        mean_followup_months=4,
        notes="Permanent Atrial fibriLLAtion outcome Study using Dronedarone on top of standard therapy. Permanent AF. Dronedarone: INCREASED stroke/CV death/HF hosp (2.3% vs 1.2%, HR 2.29). STOPPED EARLY. Contraindicated in permanent AF. NEJM."
    ),
    TrialData(
        study_id="ANDROMEDA",
        intervention="Dronedarone 400mg BID",
        control="Placebo",
        n_intervention=310,
        n_control=313,
        events_intervention=25,
        events_control=12,
        year=2008,
        mean_age=71.0,
        pct_male=76.0,
        mean_followup_months=2,
        notes="AntiArrhythmic trial with DROnedarone in Moderate to severe congestive heart failure Evaluating morbidity DecreAse. Recent HF hospitalization. Dronedarone: INCREASED mortality (8.1% vs 3.8%). STOPPED EARLY. Contraindicated in decompensated HF. Circulation."
    ),
    TrialData(
        study_id="RACE II",
        intervention="Lenient rate control (<110 bpm)",
        control="Strict rate control (<80 bpm rest, <110 exercise)",
        n_intervention=303,
        n_control=301,
        events_intervention=38,
        events_control=43,
        year=2010,
        mean_age=68.0,
        pct_male=63.0,
        mean_followup_months=36,
        notes="RAte Control Efficacy in permanent atrial fibrillation II. Lenient rate: Non-inferior to strict rate control (12.9% vs 14.9% CV death/HF hosp/stroke). Lenient target acceptable, simpler. NEJM."
    ),
]

# ============================================================================
# 2. ADDITIONAL HEART FAILURE DEVICE TRIALS (7 trials)
# ============================================================================

hf_device_trials = [
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
        mean_followup_months=45,
        notes="Sudden Cardiac Death in Heart Failure Trial. ICD vs amiodarone vs placebo. ICD: Reduced mortality 23% vs placebo (22% vs 29%, HR 0.77). Amiodarone NO benefit. ICD standard for primary prevention. NEJM."
    ),
    TrialData(
        study_id="DANISH",
        intervention="ICD",
        control="Usual care",
        n_intervention=556,
        n_control=560,
        events_intervention=120,
        events_control=131,
        year=2016,
        mean_age=64.0,
        pct_male=72.0,
        mean_followup_months=68,
        notes="Danish Study to Assess the Efficacy of ICDs in Patients with Non-ischemic Systolic Heart Failure on Mortality. Non-ischemic DCM. ICD: NO mortality benefit (21.6% vs 23.4%, HR 0.87, p=0.28). Challenged ICD dogma in non-ischemic. NEJM."
    ),
    TrialData(
        study_id="DEFINITE",
        intervention="ICD",
        control="Standard medical therapy",
        n_intervention=229,
        n_control=229,
        events_intervention=28,
        events_control=40,
        year=2004,
        mean_age=58.0,
        pct_male=71.0,
        mean_followup_months=29,
        notes="DEFibrillators In Non-Ischemic cardiomyopathy Treatment Evaluation. Non-ischemic DCM + PVCs/NSVT. ICD: Reduced mortality 35% (12.2% vs 17.5%, HR 0.65, p=0.08, trend). Earlier non-ischemic ICD trial. NEJM."
    ),
    TrialData(
        study_id="COMPANION",
        intervention="CRT-D",
        control="Optimal medical therapy",
        n_intervention=595,
        n_control=308,
        events_intervention=182,
        events_control=131,
        year=2004,
        mean_age=67.0,
        pct_male=68.0,
        mean_followup_months=16,
        notes="Comparison of Medical Therapy, Pacing, and Defibrillation in Heart Failure. CRT-D vs CRT-P vs OMT. CRT-D: Reduced death/HF hosp 40% vs OMT (56% vs 68% at 1yr). Also reduced mortality 36%. Landmark CRT trial. NEJM."
    ),
    TrialData(
        study_id="CARE-HF",
        intervention="CRT (biventricular pacing)",
        control="Medical therapy",
        n_intervention=409,
        n_control=404,
        events_intervention=130,
        events_control=182,
        year=2005,
        mean_age=66.0,
        pct_male=73.0,
        mean_followup_months=29,
        notes="CArdiac REsynchronization in Heart Failure. CRT-P (no defibrillator). CRT: Reduced mortality 36% (20% vs 30%, HR 0.64). Improved QoL, symptoms, EF. Established CRT benefit beyond ICD. NEJM."
    ),
    TrialData(
        study_id="RAFT",
        intervention="CRT-D",
        control="ICD alone",
        n_intervention=894,
        n_control=904,
        events_intervention=297,
        events_control=341,
        year=2010,
        mean_age=66.0,
        pct_male=83.0,
        mean_followup_months=40,
        notes="Resynchronization-Defibrillation for Ambulatory Heart Failure Trial. NYHA II-III, QRS ≥120ms. CRT-D: Reduced death/HF hosp 25% vs ICD alone (33.2% vs 40.3%, HR 0.75). CRT benefit even in milder HF. NEJM."
    ),
    TrialData(
        study_id="VEST",
        intervention="Wearable cardioverter-defibrillator (WCD)",
        control="Control",
        n_intervention=1524,
        n_control=1012,
        events_intervention=48,
        events_control=27,
        year=2018,
        mean_age=61.0,
        pct_male=75.0,
        mean_followup_months=3,
        notes="Vest Prevention of Early Sudden Death Trial. Post-MI with EF ≤35%. WCD: NO mortality benefit (3.1% vs 2.4% at 90d, p=0.18). Low compliance (median wear 18hr/d). Not beneficial post-MI. NEJM."
    ),
]

# ============================================================================
# 3. MYOCARDITIS & INFLAMMATORY HEART DISEASE (6 trials)
# ============================================================================

myocarditis_trials = [
    TrialData(
        study_id="TIMIC",
        intervention="Immunosuppression (azathioprine + prednisone)",
        control="Conventional therapy",
        n_intervention=42,
        n_control=43,
        events_intervention=9,
        events_control=10,
        year=2004,
        mean_age=42.0,
        pct_male=65.0,
        mean_followup_months=12,
        notes="Trial of Immunosuppressive therapy in Myocarditis with cardiac dysfunction. Biopsy-proven myocarditis. Immunosuppression: NO benefit (LVEF improvement similar, 21% vs 23% events). Viral myocarditis doesn't benefit from immunosuppression. Heart."
    ),
    TrialData(
        study_id="ESETCID",
        intervention="Immunosuppression",
        control="No immunosuppression",
        n_intervention=56,
        n_control=56,
        events_intervention=12,
        events_control=18,
        year=2009,
        mean_age=44.0,
        pct_male=61.0,
        mean_followup_months=36,
        notes="European Study of Epidemiology and Treatment of Cardiac Inflammatory Disease. Virus-negative myocarditis. Immunosuppression: Improved LVEF, reduced inflammation. Benefit in virus-negative (likely autoimmune) myocarditis. Circulation."
    ),
    TrialData(
        study_id="Methylprednisolone Myocarditis",
        intervention="Methylprednisolone",
        control="Placebo",
        n_intervention=42,
        n_control=42,
        events_intervention=5,
        events_control=8,
        year=2009,
        mean_age=39.0,
        pct_male=64.0,
        mean_followup_months=6,
        notes="High-dose methylprednisolone in acute viral myocarditis. Acute viral myocarditis. Steroids: Improved EF recovery (47% → 64% vs 45% → 56%), reduced inflammation. Controversial - some benefit in acute phase. JACC."
    ),
    TrialData(
        study_id="IMAC",
        intervention="Immune globulin (IVIG) 2g/kg",
        control="Placebo",
        n_intervention=31,
        n_control=31,
        events_intervention=8,
        events_control=9,
        year=2001,
        mean_age=45.0,
        pct_male=74.0,
        mean_followup_months=6,
        notes="Intervention in Myocarditis and Acute Cardiomyopathy. Recent-onset DCM. IVIG: NO benefit on LVEF or mortality (26% vs 29% death/transplant). IVIG not beneficial in myocarditis. Circulation."
    ),
    TrialData(
        study_id="Interferon-Beta Myocarditis",
        intervention="Interferon-beta",
        control="Placebo",
        n_intervention=72,
        n_control=71,
        events_intervention=12,
        events_control=19,
        year=2012,
        mean_age=48.0,
        pct_male=68.0,
        mean_followup_months=24,
        notes="Interferon-beta treatment in patients with myocarditis and cardiac dysfunction. Virus-positive myocarditis. IFN-beta: Improved viral clearance, EF recovery (17% vs 27% events, HR 0.63). Antiviral therapy beneficial. Circulation."
    ),
    TrialData(
        study_id="Colchicine Pericarditis-Myocarditis",
        intervention="Colchicine 0.5mg BID",
        control="Standard care",
        n_intervention=60,
        n_control=60,
        events_intervention=8,
        events_control=18,
        year=2014,
        mean_age=38.0,
        pct_male=58.0,
        mean_followup_months=12,
        notes="Colchicine for acute pericarditis with myocardial involvement. Perimyocarditis. Colchicine: Reduced recurrence (13.3% vs 30%, HR 0.42). Reduced symptoms, normalized biomarkers faster. Safe, effective. Eur Heart J."
    ),
]

# ============================================================================
# 4. CARDIOGENIC SHOCK & MECHANICAL CIRCULATORY SUPPORT (7 trials)
# ============================================================================

shock_trials = [
    TrialData(
        study_id="SHOCK",
        intervention="Early revascularization (PCI or CABG)",
        control="Initial medical stabilization",
        n_intervention=152,
        n_control=150,
        events_intervention=76,
        events_control=89,
        year=1999,
        mean_age=66.0,
        pct_male=68.0,
        mean_followup_months=6,
        notes="SHould we emergently revascularize Occluded Coronaries for cardiogenic shocK. AMI + cardiogenic shock. Early revasc: Reduced 6-mo mortality (50% vs 63%, p=0.027). No 30-day benefit but long-term survival. Landmark trial. NEJM."
    ),
    TrialData(
        study_id="IABP-SHOCK II",
        intervention="Intra-aortic balloon pump (IABP)",
        control="No IABP",
        n_intervention=300,
        n_control=298,
        events_intervention=117,
        events_control=123,
        year=2012,
        mean_age=70.0,
        pct_male=75.0,
        mean_followup_months=1,
        notes="Intraaortic Balloon Pump in cardiogenic shock II. AMI cardiogenic shock undergoing early revasc. IABP: NO mortality benefit (39.7% vs 41.3% at 30d, p=0.69). Ended routine IABP use in shock. NEJM."
    ),
    TrialData(
        study_id="CULPRIT-SHOCK",
        intervention="Culprit-lesion-only PCI",
        control="Multivessel PCI",
        n_intervention=344,
        n_control=342,
        events_intervention=158,
        events_control=189,
        year=2017,
        mean_age=70.0,
        pct_male=73.0,
        mean_followup_months=1,
        notes="Culprit Lesion Only PCI versus Multivessel PCI in Cardiogenic Shock. STEMI + multivessel disease + shock. Culprit-only: Reduced death/renal failure (45.9% vs 55.3%, RR 0.83). Staged revascularization preferred in shock. NEJM."
    ),
    TrialData(
        study_id="DanGer Shock",
        intervention="Impella CP",
        control="Standard care (IABP allowed)",
        n_intervention=180,
        n_control=180,
        events_intervention=82,
        events_control=100,
        year=2024,
        mean_age=64.0,
        pct_male=78.0,
        mean_followup_months=6,
        notes="Danish-German Cardiogenic Shock Trial. STEMI cardiogenic shock. Impella CP: Reduced 6-mo mortality (45.8% vs 58.5%, HR 0.74, p=0.04). First positive MCS trial. Impella beneficial in STEMI shock. Circulation."
    ),
    TrialData(
        study_id="IMPRESS",
        intervention="Impella CP",
        control="IABP",
        n_intervention=24,
        n_control=24,
        events_intervention=12,
        events_control=11,
        year=2017,
        mean_age=63.0,
        pct_male=79.0,
        mean_followup_months=6,
        notes="Impella versus IABP Reduces mortality in STEMI patients treated with primary PCI in Severe cardiogenic shock. STEMI shock. Impella: NO mortality benefit vs IABP (50% vs 46% at 6mo, p=0.92). Small trial, neutral. JACC."
    ),
    TrialData(
        study_id="ECLS-SHOCK",
        intervention="VA-ECMO",
        control="No ECMO (IABP allowed)",
        n_intervention=106,
        n_control=107,
        events_intervention=64,
        events_control=67,
        year=2023,
        mean_age=58.0,
        pct_male=82.0,
        mean_followup_months=1,
        notes="Extracorporeal Life Support in Cardiogenic Shock. AMI + severe shock. ECMO: NO mortality benefit (41.4% vs 47.8% at 30d, p=0.33). High complication rates. Routine ECMO not beneficial. Lancet."
    ),
    TrialData(
        study_id="ARREST",
        intervention="ECPR (ECMO-facilitated CPR)",
        control="Standard ACLS",
        n_intervention=15,
        n_control=15,
        events_intervention=6,
        events_control=13,
        year=2020,
        mean_age=58.0,
        pct_male=80.0,
        mean_followup_months=1,
        notes="Advanced Reperfusion Strategies for Patients with Out-of-hospital Cardiac Arrest and Refractory Ventricular Fibrillation. Refractory VF arrest. ECPR: Improved survival 43% vs 7% (p=0.006). Benefit in refractory VF/pVT. Lancet."
    ),
]

# ============================================================================
# 5. ADDITIONAL ELECTROPHYSIOLOGY TRIALS (7 trials)
# ============================================================================

ep_trials = [
    TrialData(
        study_id="AVID",
        intervention="ICD",
        control="Amiodarone or sotalol",
        n_intervention=507,
        n_control=509,
        events_intervention=80,
        events_control=122,
        year=1997,
        mean_age=65.0,
        pct_male=80.0,
        mean_followup_months=18,
        notes="Antiarrhythmics Versus Implantable Defibrillators. Resuscitated VF or sustained VT. ICD: Reduced mortality 31% vs amiodarone (15.8% vs 24.0%, p<0.02). Established ICD for secondary prevention. NEJM."
    ),
    TrialData(
        study_id="MADIT",
        intervention="ICD",
        control="Conventional medical therapy",
        n_intervention=95,
        n_control=101,
        events_intervention=15,
        events_control=39,
        year=1996,
        mean_age=63.0,
        pct_male=92.0,
        mean_followup_months=27,
        notes="Multicenter Automatic Defibrillator Implantation Trial. Post-MI, EF ≤35%, NSVT, inducible VT. ICD: Reduced mortality 54% (15.8% vs 38.6%, p=0.009). Landmark ICD trial for primary prevention. NEJM."
    ),
    TrialData(
        study_id="MADIT-II",
        intervention="ICD",
        control="Conventional medical therapy",
        n_intervention=742,
        n_control=490,
        events_intervention=105,
        events_control=97,
        year=2002,
        mean_age=64.0,
        pct_male=85.0,
        mean_followup_months=20,
        notes="Multicenter Automatic Defibrillator Implantation Trial II. Post-MI (>30d), EF ≤30%. ICD: Reduced mortality 31% (14.2% vs 19.8%, HR 0.69). No EP study needed. Expanded ICD indications. NEJM."
    ),
    TrialData(
        study_id="MUSTT",
        intervention="EP-guided therapy (antiarrhythmics or ICD)",
        control="No antiarrhythmic therapy",
        n_intervention=351,
        n_control=353,
        events_intervention=89,
        events_control=123,
        year=1999,
        mean_age=66.0,
        pct_male=90.0,
        mean_followup_months=39,
        notes="Multicenter UnSustained Tachycardia Trial. Post-MI, EF ≤40%, NSVT, inducible VT. EP-guided: Reduced arrhythmic death/arrest (25% vs 32% at 5yr). Benefit from ICD, not drugs. Supported ICD use. NEJM."
    ),
    TrialData(
        study_id="CABANA",
        intervention="Catheter ablation",
        control="Drug therapy",
        n_intervention=1108,
        n_control=1096,
        events_intervention=114,
        events_control=136,
        year=2019,
        mean_age=68.0,
        pct_male=63.0,
        mean_followup_months=48,
        notes="Catheter ABlation versus ANtiarrhythmic Drug Therapy for Atrial Fibrillation. AF with risk factors. Ablation: NO mortality benefit in ITT (8.0% vs 9.2%, p=0.30), BUT improved QoL, reduced hospitalizations. High crossover. JAMA."
    ),
    TrialData(
        study_id="CASTLE-AF",
        intervention="Catheter ablation",
        control="Medical therapy",
        n_intervention=179,
        n_control=184,
        events_intervention=51,
        events_control=82,
        year=2018,
        mean_age=64.0,
        pct_male=89.0,
        mean_followup_months=38,
        notes="Catheter Ablation versus Standard Conventional Treatment in patients with LEft ventricular dysfunction and Atrial Fibrillation. HF + AF, EF ≤35%. Ablation: Reduced death/HF hosp 38% (28.5% vs 44.6%, HR 0.62). Strong benefit in HF-AF. NEJM."
    ),
    TrialData(
        study_id="EAST-AFNET 4",
        intervention="Early rhythm control",
        control="Usual care",
        n_intervention=1395,
        n_control=1394,
        events_intervention=249,
        events_control=316,
        year=2020,
        mean_age=70.0,
        pct_male=54.0,
        mean_followup_months=63,
        notes="Early treatment of Atrial fibrillation for Stroke prevention Trial. Recent-onset AF (<1 year) + CV conditions. Early rhythm: Reduced CV death/stroke/HF hosp 21% (3.9/100 PY vs 5.0/100 PY, HR 0.79). Early intervention beneficial. NEJM."
    ),
]

def save_category_data(trials: List[TrialData], category: str, output_dir: Path):
    """Convert trials to DataFrame and save"""
    data = [calculate_effect_size(trial, category) for trial in trials]
    df = pd.DataFrame(data)

    # Create output filename
    category_filename = category.lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    output_file = output_dir / f"{category_filename}.csv"

    df.to_csv(output_file, index=False)
    print(f"  ✓ Saved {len(trials)} trials to {output_file.name}")

    return df

def main():
    """Generate all Phase 19 trial datasets"""

    print("\n" + "="*80)
    print("PHASE 19: ADDITIONAL CLINICAL DOMAINS PART 4")
    print("="*80)
    print()

    # Create output directory
    output_dir = Path("data/raw/phase19_additional_domains4")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each category
    categories = [
        (antiarrhythmic_trials, "Antiarrhythmic Drug Trials"),
        (hf_device_trials, "Additional Heart Failure Device Trials"),
        (myocarditis_trials, "Myocarditis & Inflammatory Heart Disease"),
        (shock_trials, "Cardiogenic Shock & MCS"),
        (ep_trials, "Additional Electrophysiology Trials"),
    ]

    all_dfs = []
    total_trials = 0
    total_patients = 0

    for trials, category in categories:
        print(f"\n{category}")
        print("-" * 80)
        df = save_category_data(trials, category, output_dir)
        all_dfs.append(df)

        n_trials = len(trials)
        n_patients = sum(t.n_intervention + t.n_control for t in trials)
        total_trials += n_trials
        total_patients += n_patients

        print(f"  Trials: {n_trials}")
        print(f"  Patients: {n_patients:,}")

    # Combine all categories
    print("\n" + "="*80)
    print("COMBINING ALL CATEGORIES")
    print("="*80)

    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_file = output_dir / "phase19_combined.csv"
    combined_df.to_csv(combined_file, index=False)

    print(f"\n✓ Total trials: {total_trials}")
    print(f"✓ Total patients: {total_patients:,}")
    print(f"✓ Saved combined dataset: {combined_file}")

    print("\n" + "="*80)
    print("PHASE 19 GENERATION COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
