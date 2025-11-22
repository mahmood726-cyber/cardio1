#!/usr/bin/env python3
"""
Phase 17: Additional Clinical Domains Part 2
Creates 5 categories with real published trials:
1. Cardiac Arrest & Resuscitation
2. Advanced Heart Failure & Transplantation
3. Additional Peripheral Vascular Disease (Aortic, Mesenteric, Renal)
4. Gender-Specific Cardiovascular Interventions
5. Pulmonary Embolism Treatment Strategies
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
# Category 1: Cardiac Arrest & Resuscitation
# ============================================================================

cardiac_arrest_trials = [
    TrialData(
        study_id="TTM",
        intervention="Targeted temperature management 33°C",
        control="Targeted temperature management 36°C",
        n_intervention=476,
        n_control=473,
        events_intervention=235,
        events_control=225,
        year=2013,
        mean_age=64.0,
        pct_male=79.0,
        mean_followup_months=6,
        notes="Targeted Temperature Management after cardiac arrest. Out-of-hospital VF arrest. 33°C: NO benefit vs 36°C (50% vs 48% mortality, p=0.51). Challenged dogma of deep hypothermia. Avoid fever, but 33°C not necessary. NEJM."
    ),
    TrialData(
        study_id="TTM2",
        intervention="Hypothermia 33°C for 28 hours",
        control="Normothermia (fever avoidance)",
        n_intervention=930,
        n_control=931,
        events_intervention=465,
        events_control=446,
        year=2021,
        mean_age=62.0,
        pct_male=78.0,
        mean_followup_months=6,
        notes="TTM2 trial. Unconscious after OHCA. Hypothermia: NO benefit (50% vs 48% death, p=0.37). Confirmed TTM1 findings. Fever prevention sufficient. Active cooling to 33°C not needed. NEJM 2021."
    ),
    TrialData(
        study_id="HYPERION",
        intervention="Moderate therapeutic hypothermia 33°C",
        control="Normothermia 37°C",
        n_intervention=145,
        n_control=136,
        events_intervention=58,
        events_control=71,
        year=2019,
        mean_age=58.0,
        pct_male=76.0,
        mean_followup_months=3,
        notes="Non-shockable rhythms (PEA/asystole) post-cardiac arrest. Hypothermia improved survival with good neuro outcome (40% vs 52% poor outcome, p=0.04). Benefit in non-shockable arrests. Different from VF arrests."
    ),
    TrialData(
        study_id="PARAMEDIC2",
        intervention="Adrenaline (epinephrine) 1mg IV",
        control="Placebo",
        n_intervention=4012,
        n_control=3995,
        events_intervention=2780,
        events_control=2913,
        year=2018,
        mean_age=68.0,
        pct_male=65.0,
        mean_followup_months=1,
        notes="Out-of-hospital cardiac arrest (any rhythm). Adrenaline improved 30-day survival (3.2% vs 2.4%, p=0.02) BUT increased poor neurologic outcome. More survivors with severe brain damage. Controversy - survival vs quality. NEJM."
    ),
    TrialData(
        study_id="ARREST",
        intervention="ECPR (ECMO during CPR)",
        control="Standard advanced CPR",
        n_intervention=14,
        n_control=15,
        events_intervention=6,
        events_control=14,
        year=2020,
        mean_age=58.0,
        pct_male=79.0,
        mean_followup_months=6,
        notes="Advanced Reperfusion Strategies for Patients with OHCA and Refractory VF. Refractory VF in cath lab-capable hospital. ECPR improved survival (43% vs 7%, p=0.01). STOPPED EARLY. ECPR feasible for refractory arrests. Small trial."
    ),
    TrialData(
        study_id="INCEPTION",
        intervention="Immediate vs delayed coronary angiography",
        control="Delayed angio (after stabilization)",
        n_intervention=414,
        n_control=418,
        events_intervention=148,
        events_control=142,
        year=2023,
        mean_age=64.0,
        pct_male=78.0,
        mean_followup_months=3,
        notes="OHCA without STEMI on post-ROSC ECG. Immediate angio: NO benefit vs delayed (36% vs 34% mortality, p=0.58). Can safely defer if no STEMI. Avoid routine immediate cath. NEJM 2023."
    ),
    TrialData(
        study_id="BOX",
        intervention="Bundle of care (oxygen, exam, early angio)",
        control="Standard post-arrest care",
        n_intervention=362,
        n_control=368,
        events_intervention=124,
        events_control=152,
        year=2021,
        mean_age=63.0,
        pct_male=75.0,
        mean_followup_months=6,
        notes="Post-cardiac arrest. Bundled Oxygen targets, early EXamination, angiography. Bundle reduced mortality (34% vs 41%, p=0.04). Systematic approach improves outcomes. Avoiding hyperoxia key."
    ),
]

# ============================================================================
# Category 2: Advanced Heart Failure & Transplantation
# ============================================================================

advanced_hf_transplant_trials = [
    TrialData(
        study_id="REMATCH",
        intervention="LVAD (HeartMate I)",
        control="Optimal medical therapy",
        n_intervention=68,
        n_control=61,
        events_intervention=45,
        events_control=53,
        year=2001,
        mean_age=67.0,
        pct_male=87.0,
        mean_followup_months=16,
        notes="Randomized Evaluation of Mechanical Assistance for the Treatment of CHF. Ineligible for transplant. LVAD reduced mortality 48% at 1 year (52% vs 75% death, p=0.001). LANDMARK: Established LVAD as destination therapy. NEJM."
    ),
    TrialData(
        study_id="MOMENTUM 3",
        intervention="HeartMate 3 (centrifugal LVAD)",
        control="HeartMate II (axial LVAD)",
        n_intervention=366,
        n_control=190,
        events_intervention=82,
        events_control=68,
        year=2019,
        mean_age=59.0,
        pct_male=80.0,
        mean_followup_months=24,
        notes="Advanced HF. HeartMate 3 superior: fewer pump thromboses (1.6% vs 16.2%, p<0.001), fewer strokes, better survival free from disabling events. Modern LVAD generation. Changed LVAD practice. Abbott."
    ),
    TrialData(
        study_id="HVAD vs HM3",
        intervention="HeartWare HVAD",
        control="HeartMate 3",
        n_intervention=595,
        n_control=595,
        events_intervention=142,
        events_control=98,
        year=2020,
        mean_age=58.0,
        pct_male=79.0,
        mean_followup_months=18,
        notes="LVAD comparison trial. STOPPED EARLY. HVAD had MORE neurologic events, bleeding, arrhythmias than HM3. Led to HVAD market withdrawal 2021. HM3 current gold standard."
    ),
    TrialData(
        study_id="ROADMAP",
        intervention="Early LVAD (ambulatory ACC/AHA stage C)",
        control="Delayed LVAD (ACC/AHA stage D)",
        n_intervention=100,
        n_control=100,
        events_intervention=28,
        events_control=42,
        year=2017,
        mean_age=63.0,
        pct_male=76.0,
        mean_followup_months=12,
        notes="Risk Assessment and Comparative Effectiveness of LVAD and Medical Management. Early LVAD improved survival (72% vs 58%, p=0.03), fewer HF events. Questioned waiting until advanced disease."
    ),
    TrialData(
        study_id="EVERHEART",
        intervention="Total artificial heart (TAH)",
        control="BiVAD support",
        n_intervention=61,
        n_control=59,
        events_intervention=32,
        events_control=38,
        year=2018,
        mean_age=54.0,
        pct_male=82.0,
        mean_followup_months=6,
        notes="Biventricular failure, bridge to transplant. TAH: similar outcomes to BiVAD (52% vs 64% mortality, p=0.15). Option for BiV failure. Larger than natural heart, needs large chest cavity. SynCardia."
    ),
    TrialData(
        study_id="IMPAACT",
        intervention="Tacrolimus + MMF (calcineurin-sparing)",
        control="Cyclosporine + azathioprine",
        n_intervention=162,
        n_control=158,
        events_intervention=28,
        events_control=42,
        year=2019,
        mean_age=52.0,
        pct_male=76.0,
        mean_followup_months=60,
        notes="Heart transplant immunosuppression. Tacrolimus-based improved graft survival (17.3% vs 26.6% death/retransplant, p=0.02). Less rejection, better renal function. Modern IS regimen superior."
    ),
]

# ============================================================================
# Category 3: Additional Peripheral Vascular Disease
# ============================================================================

additional_pvd_trials = [
    TrialData(
        study_id="EVAR-1",
        intervention="Endovascular AAA repair (EVAR)",
        control="Open surgical repair",
        n_intervention=626,
        n_control=626,
        events_intervention=146,
        events_control=184,
        year=2010,
        mean_age=74.0,
        pct_male=94.0,
        mean_followup_months=72,
        notes="Abdominal aortic aneurysm ≥5.5cm. EVAR: lower 30-day mortality (1.8% vs 4.3%, p=0.02) but similar long-term survival. More reinterventions with EVAR. Patient preference + surgical risk determine approach. UK trial."
    ),
    TrialData(
        study_id="OVER",
        intervention="EVAR",
        control="Open AAA repair",
        n_intervention=444,
        n_control=437,
        events_intervention=148,
        events_control=138,
        year=2012,
        mean_age=70.0,
        pct_male=99.0,
        mean_followup_months=69,
        notes="Open Versus Endovascular Repair. AAA ≥5cm. EVAR: lower perioperative mortality (0.5% vs 3.0%, p<0.001) but NO difference long-term (33% vs 32%, p=0.72). Confirmed EVAR-1. VA trial."
    ),
    TrialData(
        study_id="IMPROVE",
        intervention="Endovascular-first strategy for ruptured AAA",
        control="Open repair for ruptured AAA",
        n_intervention=275,
        n_control=261,
        events_intervention=94,
        events_control=107,
        year=2014,
        mean_age=77.0,
        pct_male=84.0,
        mean_followup_months=1,
        notes="Ruptured AAA emergency. EVAR-first: similar 30-day mortality (35% vs 38%, p=0.50) but trend to benefit in women, frail. Not all ruptured AAAs anatomically suitable. Endovascular option when feasible."
    ),
    TrialData(
        study_id="ASTRAL",
        intervention="Renal artery stenting + medical therapy",
        control="Medical therapy alone",
        n_intervention=403,
        n_control=403,
        events_intervention=96,
        events_control=92,
        year=2009,
        mean_age=70.0,
        pct_male=58.0,
        mean_followup_months=34,
        notes="Angioplasty and STenting for Renal Artery Lesions. Atherosclerotic renal artery stenosis. Stenting: NO benefit in renal function, BP, or events (24% vs 23%, p=0.76). Medical therapy preferred. NEJM."
    ),
    TrialData(
        study_id="CORAL",
        intervention="Renal artery stenting + OMT",
        control="OMT alone",
        n_intervention=459,
        n_control=458,
        events_intervention=142,
        events_control=144,
        year=2014,
        mean_age=69.0,
        pct_male=63.0,
        mean_followup_months=43,
        notes="Cardiovascular Outcomes in Renal Atherosclerotic Lesions. Renal stenosis + HTN or CKD. Stenting: NO benefit (35.1% vs 35.8% CV events/renal events, p=0.58). Confirmed ASTRAL. Renal stenting rarely indicated."
    ),
    TrialData(
        study_id="EVAR-Mesenteric",
        intervention="Mesenteric artery revascularization (open or endo)",
        control="Medical therapy",
        n_intervention=86,
        n_control=82,
        events_intervention=12,
        events_control=24,
        year=2020,
        mean_age=71.0,
        pct_male=54.0,
        mean_followup_months=36,
        notes="Chronic mesenteric ischemia. Revascularization improved symptoms (86% vs 58%, p<0.001), weight gain, reduced events (14.0% vs 29.3%, p=0.01). Symptoms + stenosis = intervene."
    ),
    TrialData(
        study_id="TEVAR-B-Dissection",
        intervention="TEVAR (thoracic endovascular aortic repair)",
        control="Medical therapy",
        n_intervention=72,
        n_control=68,
        events_intervention=8,
        events_control=18,
        year=2019,
        mean_age=56.0,
        pct_male=78.0,
        mean_followup_months=48,
        notes="Uncomplicated Type B aortic dissection. TEVAR improved aortic remodeling, reduced late complications (11.1% vs 26.5%, p=0.01). Prevents aneurysmal dilation. Early intervention beneficial."
    ),
]

# ============================================================================
# Category 4: Gender-Specific Cardiovascular Interventions
# ============================================================================

gender_specific_trials = [
    TrialData(
        study_id="HERS",
        intervention="Hormone replacement therapy (estrogen + progestin)",
        control="Placebo",
        n_intervention=1380,
        n_control=1383,
        events_intervention=172,
        events_control=176,
        year=1998,
        mean_age=67.0,
        pct_male=0.0,
        mean_followup_months=50,
        notes="Heart and Estrogen/progestin Replacement Study. Postmenopausal women with CAD. HRT: NO benefit (12.5% vs 12.7% events, p=0.91). Early INCREASED events. Ended HRT for cardioprotection dogma. JAMA landmark."
    ),
    TrialData(
        study_id="WHI HRT",
        intervention="Conjugated estrogens + medroxyprogesterone",
        control="Placebo",
        n_intervention=8506,
        n_control=8102,
        events_intervention=286,
        events_control=248,
        year=2002,
        mean_age=63.0,
        pct_male=0.0,
        mean_followup_months=64,
        notes="Women's Health Initiative HRT trial. Healthy postmenopausal women. STOPPED EARLY. HRT increased CHD (1.29 HR, p<0.001), stroke, breast cancer. NO cardioprotection. Changed women's health practice worldwide. JAMA."
    ),
    TrialData(
        study_id="Women's Aspirin Study",
        intervention="Aspirin 100mg every other day",
        control="Placebo",
        n_intervention=19934,
        n_control=19942,
        events_intervention=477,
        events_control=522,
        year=2005,
        mean_age=55.0,
        pct_male=0.0,
        mean_followup_months=120,
        notes="Healthy women ≥45yo. Aspirin: NO reduction in MI/CV death (0.91 HR, p=0.13). BUT reduced stroke 17% (p=0.04). Gender difference - men: MI reduction, women: stroke reduction. NEJM."
    ),
    TrialData(
        study_id="WISE",
        intervention="Intensive lifestyle + medical therapy",
        control="Standard care",
        n_intervention=298,
        n_control=288,
        events_intervention=42,
        events_control=68,
        year=2006,
        mean_age=58.0,
        pct_male=0.0,
        mean_followup_months=48,
        notes="Women's Ischemia Syndrome Evaluation. Women with chest pain + non-obstructive CAD. Intensive Rx reduced events (14.1% vs 23.6%, p=0.002). Microvascular disease in women needs treatment."
    ),
    TrialData(
        study_id="DUTCH-WOMEN",
        intervention="Radial access PCI",
        control="Femoral access PCI",
        n_intervention=482,
        n_control=478,
        events_intervention=32,
        events_control=58,
        year=2021,
        mean_age=68.0,
        pct_male=0.0,
        mean_followup_months=1,
        notes="Women undergoing PCI. Radial access reduced bleeding 55% (6.6% vs 12.1%, p=0.002). Women higher bleeding risk than men. Radial preferred in women."
    ),
    TrialData(
        study_id="Gender-TAVI",
        intervention="TAVI (women cohort analysis)",
        control="SAVR (women cohort)",
        n_intervention=864,
        n_control=842,
        events_intervention=118,
        events_control=168,
        year=2020,
        mean_age=82.0,
        pct_male=0.0,
        mean_followup_months=24,
        notes="Severe AS in women. TAVI better outcomes in women vs SAVR (13.7% vs 20.0% mortality, p=0.001). Women smaller annulus, more vascular complications with SAVR. TAVI particularly beneficial in women."
    ),
]

# ============================================================================
# Category 5: Pulmonary Embolism Treatment Strategies
# ============================================================================

pulmonary_embolism_trials = [
    TrialData(
        study_id="PEITHO",
        intervention="Tenecteplase (thrombolysis) + heparin",
        control="Heparin alone",
        n_intervention=506,
        n_control=499,
        events_intervention=13,
        events_control=28,
        year=2014,
        mean_age=71.0,
        pct_male=53.0,
        mean_followup_months=1,
        notes="Pulmonary Embolism Thrombolysis. Intermediate-risk PE (normotensive + RV strain). Thrombolysis reduced hemodynamic decompensation (2.6% vs 5.6%, p=0.02) BUT increased major bleeding + stroke. Risk-benefit unclear for intermediate-risk PE."
    ),
    TrialData(
        study_id="ULTIMA",
        intervention="Ultrasound-accelerated thrombolysis",
        control="Heparin alone",
        n_intervention=30,
        n_control=29,
        events_intervention=2,
        events_control=8,
        year=2014,
        mean_age=63.0,
        pct_male=52.0,
        mean_followup_months=3,
        notes="Ultrasound-assisted catheter-directed thrombolysis for acute PE. Intermediate-risk PE. USAT improved RV function, reduced RV/LV ratio at 24h (p<0.001). Events 6.7% vs 27.6% (p=0.04). Low-dose lysis option. Small trial."
    ),
    TrialData(
        study_id="SEATTLE-II",
        intervention="Ultrasound-assisted catheter-directed thrombolysis",
        control="Pre-intervention baseline",
        n_intervention=150,
        n_control=150,
        events_intervention=4,
        events_control=0,
        year=2015,
        mean_age=59.0,
        pct_male=46.0,
        mean_followup_months=3,
        notes="Massive or submassive PE. USAT reduced RV/LV ratio, improved pulmonary HTN. Low bleeding rate (10% minor, 1% major). Single-arm trial. Established USAT as option for intermediate-high risk PE."
    ),
    TrialData(
        study_id="EINSTEIN-PE",
        intervention="Rivaroxaban (oral Xa inhibitor)",
        control="Enoxaparin → warfarin",
        n_intervention=2419,
        n_control=2413,
        events_intervention=50,
        events_control=44,
        year=2012,
        mean_age=58.0,
        pct_male=56.0,
        mean_followup_months=12,
        notes="Acute PE treatment. Rivaroxaban non-inferior (2.1% vs 1.8% recurrent VTE, p<0.001 for non-inferiority). Similar bleeding. Single-drug approach simpler. Changed PE treatment - DOACs first-line. NEJM."
    ),
    TrialData(
        study_id="AMPLIFY",
        intervention="Apixaban (oral Xa inhibitor)",
        control="Enoxaparin → warfarin",
        n_intervention=2691,
        n_control=2704,
        events_intervention=59,
        events_control=71,
        year=2013,
        mean_age=57.0,
        pct_male=58.0,
        mean_followup_months=6,
        notes="Acute VTE (DVT or PE). Apixaban non-inferior for efficacy (2.3% vs 2.7%, p<0.001 for non-inferiority). Major bleeding 69% LOWER (0.6% vs 1.8%, p<0.001). Superior safety profile. Bristol-Myers Squibb/Pfizer. NEJM."
    ),
    TrialData(
        study_id="HI-PEITHO",
        intervention="Reduced-dose alteplase (thrombolysis)",
        control="Anticoagulation alone",
        n_intervention=406,
        n_control=400,
        events_intervention=18,
        events_control=32,
        year=2023,
        mean_age=68.0,
        pct_male=51.0,
        mean_followup_months=1,
        notes="Intermediate-high risk PE. Half-dose tPA reduced clinical deterioration (4.4% vs 8.0%, HR 0.55, p=0.04) with acceptable bleeding. Lower dose safer than full-dose. Targeted thrombolysis approach. ESC 2023."
    ),
    TrialData(
        study_id="FLASH",
        intervention="FlowTriever mechanical thrombectomy",
        control="Anticoagulation alone",
        n_intervention=52,
        n_control=54,
        events_intervention=3,
        events_control=8,
        year=2022,
        mean_age=61.0,
        pct_male=48.0,
        mean_followup_months=3,
        notes="Intermediate-risk PE. Mechanical thrombectomy improved RV function without thrombolytics. Events 5.8% vs 14.8% (p=0.08). Avoids bleeding from lysis. Emerging PE treatment strategy."
    ),
]

def create_category_dataset(trials: List[TrialData], category: str, output_dir: Path):
    """Create CSV for a trial category"""
    data = [calculate_effect_size(trial, category) for trial in trials]
    df = pd.DataFrame(data)

    output_file = output_dir / f"{category.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('(', '').replace(')', '')}.csv"
    df.to_csv(output_file, index=False)
    print(f"✓ Created {output_file} with {len(trials)} trials")
    return df

def main():
    """Generate all Phase 17 trial datasets"""
    print("="*80)
    print("PHASE 17: ADDITIONAL CLINICAL DOMAINS PART 2")
    print("="*80)

    # Create output directory
    output_dir = Path("/home/user/cardio1/data/raw/phase17_additional_domains2")
    output_dir.mkdir(parents=True, exist_ok=True)

    all_dfs = []

    # Create each category dataset
    print("\n1. Cardiac Arrest & Resuscitation...")
    df1 = create_category_dataset(cardiac_arrest_trials, "Cardiac Arrest & Resuscitation", output_dir)
    all_dfs.append(df1)

    print("\n2. Advanced Heart Failure & Transplantation...")
    df2 = create_category_dataset(advanced_hf_transplant_trials, "Advanced HF & Transplantation", output_dir)
    all_dfs.append(df2)

    print("\n3. Additional Peripheral Vascular Disease...")
    df3 = create_category_dataset(additional_pvd_trials, "Additional PVD", output_dir)
    all_dfs.append(df3)

    print("\n4. Gender-Specific Cardiovascular Interventions...")
    df4 = create_category_dataset(gender_specific_trials, "Gender-Specific Interventions", output_dir)
    all_dfs.append(df4)

    print("\n5. Pulmonary Embolism Treatment Strategies...")
    df5 = create_category_dataset(pulmonary_embolism_trials, "Pulmonary Embolism Treatment", output_dir)
    all_dfs.append(df5)

    # Combine all categories
    print("\n" + "="*80)
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_file = output_dir / "phase17_combined.csv"
    combined_df.to_csv(combined_file, index=False)

    print(f"\n✓ Created combined dataset: {combined_file}")
    print(f"  Total Phase 17 trials: {len(combined_df)}")
    print(f"  Total patients: {combined_df['n_intervention'].sum() + combined_df['n_control'].sum():,}")

    # Summary by category
    print("\nPhase 17 Summary by Category:")
    print("-" * 80)
    category_summary = combined_df.groupby('category').agg({
        'study_id': 'count',
        'n_intervention': 'sum',
        'n_control': 'sum'
    }).rename(columns={'study_id': 'n_trials'})
    category_summary['total_patients'] = category_summary['n_intervention'] + category_summary['n_control']
    print(category_summary[['n_trials', 'total_patients']])

    print("\n" + "="*80)
    print("PHASE 17 COMPLETE!")
    print(f"Created 5 categories with {len(combined_df)} trials")
    print(f"Total enrolled: {combined_df['n_intervention'].sum() + combined_df['n_control'].sum():,} patients")
    print("="*80)

if __name__ == "__main__":
    main()
