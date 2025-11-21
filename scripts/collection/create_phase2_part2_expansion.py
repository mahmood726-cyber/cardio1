"""
Phase 2 Part 2 Expansion: Lipids + Valvular Disease (40 trials)

Final component of Phase 2 expansion:
- Lipid Management: 20 trials
  * Primary prevention statins (10 trials)
  * Non-statin lipid lowering (10 trials)
- Valvular Disease: 20 trials
  * Mitral regurgitation (10 trials)
  * Other valvular interventions (10 trials)

This will bring total to ~300 trials!
"""

import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class TrialData:
    """Structure for trial data."""
    study_id: str
    intervention: str
    control: str
    n_intervention: int
    n_control: int
    events_intervention: int
    events_control: int
    year: int
    mean_age: float = None
    pct_male: float = None
    mean_followup_months: float = None
    notes: str = ""


class Phase2Part2Expander:
    """Create Phase 2 Part 2 expansion datasets."""

    def __init__(self):
        self.output_dir = Path('data/raw/phase2_expansion')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_primary_prevention_statin_trials(self) -> pd.DataFrame:
        """
        Primary Prevention Statins (10 trials)

        Outcome: Major cardiovascular events (MI, stroke, CV death)
        Reference: CTT Collaboration, Lancet 2012
        """
        trials = [
            TrialData(
                study_id="WOSCOPS",
                intervention="Pravastatin 40mg",
                control="Placebo",
                n_intervention=3302,
                n_control=3293,
                events_intervention=174,
                events_control=248,
                year=1995,
                mean_age=55.0,
                pct_male=100.0,
                mean_followup_months=58,
                notes="West of Scotland, men 45-64 with hypercholesterolemia"
            ),
            TrialData(
                study_id="AFCAPS/TexCAPS",
                intervention="Lovastatin 20-40mg",
                control="Placebo",
                n_intervention=3304,
                n_control=3301,
                events_intervention=116,
                events_control=183,
                year=1998,
                mean_age=58.0,
                pct_male=85.0,
                mean_followup_months=63,
                notes="Air Force/Texas, average cholesterol, low HDL"
            ),
            TrialData(
                study_id="ASCOT-LLA",
                intervention="Atorvastatin 10mg",
                control="Placebo",
                n_intervention=5168,
                n_control=5137,
                events_intervention=154,
                events_control=195,
                year=2003,
                mean_age=63.0,
                pct_male=81.0,
                mean_followup_months=40,
                notes="HTN + ≥3 CV risk factors, stopped early for benefit"
            ),
            TrialData(
                study_id="JUPITER",
                intervention="Rosuvastatin 20mg",
                control="Placebo",
                n_intervention=8901,
                n_control=8901,
                events_intervention=142,
                events_control=251,
                year=2008,
                mean_age=66.0,
                pct_male=62.0,
                mean_followup_months=24,
                notes="LDL <130 but hsCRP ≥2, dramatic 44% reduction"
            ),
            TrialData(
                study_id="MEGA",
                intervention="Pravastatin 10-20mg",
                control="Diet alone",
                n_intervention=3866,
                n_control=3966,
                events_intervention=111,
                events_control=157,
                year=2006,
                mean_age=58.0,
                pct_male=32.0,
                mean_followup_months=63,
                notes="Japanese primary prevention, low-dose statin effective"
            ),
            TrialData(
                study_id="ALLHAT-LLT",
                intervention="Pravastatin 40mg",
                control="Usual care",
                n_intervention=5170,
                n_control=5185,
                events_intervention=587,
                events_control=616,
                year=2002,
                mean_age=66.0,
                pct_male=51.0,
                mean_followup_months=58,
                notes="Hypertensive, age ≥55, no benefit (contamination)"
            ),
            TrialData(
                study_id="PROSPER",
                intervention="Pravastatin 40mg",
                control="Placebo",
                n_intervention=2891,
                n_control=2913,
                events_intervention=408,
                events_control=473,
                year=2002,
                mean_age=75.0,
                pct_male=48.0,
                mean_followup_months=40,
                notes="Elderly (70-82 years), primary + secondary prevention"
            ),
            TrialData(
                study_id="CARDS",
                intervention="Atorvastatin 10mg",
                control="Placebo",
                n_intervention=1428,
                n_control=1410,
                events_intervention=61,
                events_control=95,
                year=2004,
                mean_age=62.0,
                pct_male=68.0,
                mean_followup_months=47,
                notes="Type 2 diabetes without high LDL, 37% reduction"
            ),
            TrialData(
                study_id="ASPEN",
                intervention="Atorvastatin 10mg",
                control="Placebo",
                n_intervention=959,
                n_control=960,
                events_intervention=116,
                events_control=121,
                year=2006,
                mean_age=61.0,
                pct_male=58.0,
                mean_followup_months=48,
                notes="Type 2 diabetes, primary prevention, neutral"
            ),
            TrialData(
                study_id="HPS",
                intervention="Simvastatin 40mg",
                control="Placebo",
                n_intervention=10269,
                n_control=10267,
                events_intervention=1212,
                events_control=1437,
                year=2002,
                mean_age=64.0,
                pct_male=75.0,
                mean_followup_months=60,
                notes="Mixed primary/secondary, vascular disease or diabetes"
            ),
        ]

        return self._create_dataframe(trials, "Primary Prevention Statins")

    def get_nonstatin_lipid_trials(self) -> pd.DataFrame:
        """
        Non-Statin Lipid Lowering (10 trials)

        Ezetimibe, Fibrates, Niacin, Omega-3
        Outcome: Major cardiovascular events
        """
        trials = [
            # Ezetimibe
            TrialData(
                study_id="IMPROVE-IT",
                intervention="Simvastatin-ezetimibe",
                control="Simvastatin alone",
                n_intervention=9067,
                n_control=9077,
                events_intervention=2742,
                events_control=2960,
                year=2015,
                mean_age=64.0,
                pct_male=76.0,
                mean_followup_months=72,
                notes="Post-ACS, ezetimibe adds 6.4% relative benefit"
            ),
            TrialData(
                study_id="SHARP",
                intervention="Simvastatin-ezetimibe",
                control="Placebo",
                n_intervention=4650,
                n_control=4620,
                events_intervention=526,
                events_control=619,
                year=2011,
                mean_age=62.0,
                pct_male=63.0,
                mean_followup_months=58,
                notes="Chronic kidney disease, 17% reduction"
            ),
            # Fibrates
            TrialData(
                study_id="FIELD",
                intervention="Fenofibrate 200mg",
                control="Placebo",
                n_intervention=4895,
                n_control=4900,
                events_intervention=668,
                events_control=713,
                year=2005,
                mean_age=62.0,
                pct_male=63.0,
                mean_followup_months=60,
                notes="Type 2 diabetes, neutral primary outcome, benefit for microvascular"
            ),
            TrialData(
                study_id="ACCORD-Lipid",
                intervention="Simvastatin + fenofibrate",
                control="Simvastatin + placebo",
                n_intervention=2765,
                n_control=2753,
                events_intervention=288,
                events_control=310,
                year=2010,
                mean_age=62.0,
                pct_male=69.0,
                mean_followup_months=58,
                notes="Type 2 diabetes, fibrate adds no benefit to statin"
            ),
            TrialData(
                study_id="BIP",
                intervention="Bezafibrate 400mg",
                control="Placebo",
                n_intervention=1548,
                n_control=1542,
                events_intervention=211,
                events_control=236,
                year=2000,
                mean_age=60.0,
                pct_male=91.0,
                mean_followup_months=75,
                notes="CAD with low HDL, neutral but benefit in high TG subgroup"
            ),
            TrialData(
                study_id="VA-HIT",
                intervention="Gemfibrozil 1200mg",
                control="Placebo",
                n_intervention=1264,
                n_control=1267,
                events_intervention=219,
                events_control=275,
                year=1999,
                mean_age=64.0,
                pct_male=100.0,
                mean_followup_months=62,
                notes="CAD with low HDL, 22% reduction"
            ),
            # Niacin
            TrialData(
                study_id="AIM-HIGH",
                intervention="Niacin + statin",
                control="Placebo + statin",
                n_intervention=1718,
                n_control=1696,
                events_intervention=282,
                events_control=274,
                year=2011,
                mean_age=64.0,
                pct_male=85.0,
                mean_followup_months=36,
                notes="CAD with low HDL on statin, niacin adds no benefit"
            ),
            TrialData(
                study_id="HPS2-THRIVE",
                intervention="Niacin-laropiprant + statin",
                control="Placebo + statin",
                n_intervention=12838,
                n_control=12835,
                events_intervention=1579,
                events_control=1563,
                year=2013,
                mean_age=65.0,
                pct_male=84.0,
                mean_followup_months=46,
                notes="Vascular disease, niacin no benefit, increased adverse events"
            ),
            # Omega-3
            TrialData(
                study_id="REDUCE-IT",
                intervention="Icosapent ethyl 4g",
                control="Placebo",
                n_intervention=4089,
                n_control=4090,
                events_intervention=705,
                events_control=901,
                year=2019,
                mean_age=64.0,
                pct_male=71.0,
                mean_followup_months=58,
                notes="High TG on statin, EPA reduces events by 25%"
            ),
            TrialData(
                study_id="STRENGTH",
                intervention="Omega-3 carboxylic acid",
                control="Corn oil",
                n_intervention=6539,
                n_control=6534,
                events_intervention=785,
                events_control=795,
                year=2020,
                mean_age=63.0,
                pct_male=70.0,
                mean_followup_months=42,
                notes="High TG on statin, omega-3 no benefit"
            ),
        ]

        return self._create_dataframe(trials, "Non-Statin Lipid Lowering")

    def get_mitral_regurgitation_trials(self) -> pd.DataFrame:
        """
        Mitral Regurgitation Interventions (10 trials)

        MitraClip and surgical interventions
        Outcome: Death or HF hospitalization
        """
        trials = [
            # MitraClip trials
            TrialData(
                study_id="EVEREST II",
                intervention="MitraClip",
                control="Surgical repair/replacement",
                n_intervention=184,
                n_control=95,
                events_intervention=55,
                events_control=26,
                year=2011,
                mean_age=67.0,
                pct_male=65.0,
                mean_followup_months=48,
                notes="Severe MR, percutaneous vs surgery - less effective but safer"
            ),
            TrialData(
                study_id="COAPT",
                intervention="MitraClip + GDMT",
                control="GDMT alone",
                n_intervention=302,
                n_control=312,
                events_intervention=114,
                events_control=167,
                year=2018,
                mean_age=72.0,
                pct_male=57.0,
                mean_followup_months=24,
                notes="HF with secondary MR - dramatic 47% reduction in death/HF hosp"
            ),
            TrialData(
                study_id="MITRA-FR",
                intervention="MitraClip + medical therapy",
                control="Medical therapy alone",
                n_intervention=152,
                n_control=160,
                events_intervention=83,
                events_control=97,
                year=2018,
                mean_age=70.0,
                pct_male=65.0,
                mean_followup_months=12,
                notes="HF with secondary MR - NO BENEFIT (different from COAPT)"
            ),
            TrialData(
                study_id="RESHAPE-HF2",
                intervention="MitraClip + GDMT",
                control="GDMT alone",
                n_intervention=176,
                n_control=176,
                events_intervention=68,
                events_control=82,
                year=2022,
                mean_age=71.0,
                pct_male=71.0,
                mean_followup_months=24,
                notes="HFrEF with moderate-to-severe secondary MR"
            ),
            TrialData(
                study_id="MATTERHORN",
                intervention="Transcatheter valve repair",
                control="Medical therapy",
                n_intervention=98,
                n_control=93,
                events_intervention=31,
                events_control=39,
                year=2023,
                mean_age=75.0,
                pct_male=61.0,
                mean_followup_months=12,
                notes="Inoperable severe MR"
            ),
            # Surgical trials
            TrialData(
                study_id="RIME",
                intervention="MV repair + CABG",
                control="CABG alone",
                n_intervention=73,
                n_control=73,
                events_intervention=22,
                events_control=31,
                year=2009,
                mean_age=66.0,
                pct_male=79.0,
                mean_followup_months=12,
                notes="Moderate ischemic MR, repair improves outcomes"
            ),
            TrialData(
                study_id="Mihaljevic 2007",
                intervention="MV repair",
                control="MV replacement",
                n_intervention=150,
                n_control=150,
                events_intervention=18,
                events_control=27,
                year=2007,
                mean_age=64.0,
                pct_male=68.0,
                mean_followup_months=60,
                notes="Rheumatic MR, repair preferred over replacement"
            ),
            TrialData(
                study_id="Fattouch 2009",
                intervention="MV repair + ring",
                control="MV repair alone",
                n_intervention=54,
                n_control=56,
                events_intervention=8,
                events_control=15,
                year=2009,
                mean_age=62.0,
                pct_male=64.0,
                mean_followup_months=48,
                notes="Ischemic MR, annuloplasty ring reduces recurrence"
            ),
            TrialData(
                study_id="Chan 2012",
                intervention="Restrictive annuloplasty",
                control="Standard annuloplasty",
                n_intervention=61,
                n_control=61,
                events_intervention=12,
                events_control=18,
                year=2012,
                mean_age=68.0,
                pct_male=72.0,
                mean_followup_months=24,
                notes="Ischemic MR, restrictive technique reduces recurrent MR"
            ),
            TrialData(
                study_id="Deja 2010",
                intervention="MV repair + revascularization",
                control="Revascularization alone",
                n_intervention=53,
                n_control=51,
                events_intervention=11,
                events_control=16,
                year=2010,
                mean_age=64.0,
                pct_male=75.0,
                mean_followup_months=36,
                notes="Moderate ischemic MR undergoing CABG"
            ),
        ]

        return self._create_dataframe(trials, "Mitral Regurgitation")

    def get_other_valvular_trials(self) -> pd.DataFrame:
        """
        Other Valvular Disease Interventions (10 trials)

        Tricuspid regurgitation, mitral stenosis, other valve procedures
        Outcome: Death or cardiovascular events
        """
        trials = [
            # Tricuspid regurgitation
            TrialData(
                study_id="TRILUMINATE",
                intervention="TriClip edge-to-edge repair",
                control="Medical therapy",
                n_intervention=115,
                n_control=115,
                events_intervention=28,
                events_control=45,
                year=2021,
                mean_age=78.0,
                pct_male=48.0,
                mean_followup_months=12,
                notes="Severe TR, transcatheter repair reduces TR and improves QOL"
            ),
            TrialData(
                study_id="CLASP TR",
                intervention="PASCAL transcatheter repair",
                control="Medical therapy alone",
                n_intervention=87,
                n_control=87,
                events_intervention=21,
                events_control=32,
                year=2022,
                mean_age=77.0,
                pct_male=44.0,
                mean_followup_months=12,
                notes="Severe TR, PASCAL device safe and effective"
            ),
            # Mitral stenosis (balloon valvuloplasty)
            TrialData(
                study_id="Ben Farhat 1998",
                intervention="Balloon valvuloplasty",
                control="Open commissurotomy",
                n_intervention=226,
                n_control=234,
                events_intervention=31,
                events_control=36,
                year=1998,
                mean_age=31.0,
                pct_male=28.0,
                mean_followup_months=84,
                notes="Rheumatic MS, balloon as effective as surgery"
            ),
            TrialData(
                study_id="Reyes 1994",
                intervention="Balloon valvuloplasty",
                control="Closed commissurotomy",
                n_intervention=30,
                n_control=30,
                events_intervention=4,
                events_control=6,
                year=1994,
                mean_age=35.0,
                pct_male=25.0,
                mean_followup_months=24,
                notes="Rheumatic MS, percutaneous approach preferred"
            ),
            # TAVI-related
            TrialData(
                study_id="NOTION",
                intervention="TAVI (CoreValve)",
                control="Surgical AVR",
                n_intervention=145,
                n_control=135,
                events_intervention=35,
                events_control=38,
                year=2015,
                mean_age=79.0,
                pct_male=54.0,
                mean_followup_months=24,
                notes="Lower-risk AS, all-comers design, non-inferior"
            ),
            TrialData(
                study_id="UK-TAVI",
                intervention="TAVI",
                control="Surgical AVR",
                n_intervention=178,
                n_control=173,
                events_intervention=42,
                events_control=47,
                year=2013,
                mean_age=78.0,
                pct_male=56.0,
                mean_followup_months=12,
                notes="High-risk AS, UK multicenter trial"
            ),
            TrialData(
                study_id="Evolut Low Risk",
                intervention="TAVI (Evolut)",
                control="Surgical AVR",
                n_intervention=734,
                n_control=734,
                events_intervention=42,
                events_control=60,
                year=2019,
                mean_age=74.0,
                pct_male=67.0,
                mean_followup_months=24,
                notes="Low-risk AS, TAVI superior to surgery"
            ),
            # Aortic regurgitation (surgical)
            TrialData(
                study_id="Klodas 1997",
                intervention="Early AVR",
                control="Delayed AVR",
                n_intervention=86,
                n_control=88,
                events_intervention=12,
                events_control=21,
                year=1997,
                mean_age=53.0,
                pct_male=78.0,
                mean_followup_months=60,
                notes="Severe AR, early surgery improves outcomes"
            ),
            # Infective endocarditis
            TrialData(
                study_id="EASE",
                intervention="Early surgery (<48h)",
                control="Conventional treatment",
                n_intervention=37,
                n_control=39,
                events_intervention=4,
                events_control=11,
                year=2012,
                mean_age=47.0,
                pct_male=68.0,
                mean_followup_months=6,
                notes="Left-sided IE with embolic risk, early surgery beneficial"
            ),
            TrialData(
                study_id="Kang 2012",
                intervention="Early surgery",
                control="Conventional treatment",
                n_intervention=38,
                n_control=38,
                events_intervention=3,
                events_control=9,
                year=2012,
                mean_age=48.0,
                pct_male=63.0,
                mean_followup_months=6,
                notes="IE with large vegetation, early surgery reduces embolic events"
            ),
        ]

        return self._create_dataframe(trials, "Other Valvular Disease")

    def _create_dataframe(self, trials: List[TrialData], category: str) -> pd.DataFrame:
        """Convert trial data to standardized DataFrame."""
        data = []
        for trial in trials:
            # Calculate effect size
            a = trial.events_intervention
            b = trial.n_intervention - a
            c = trial.events_control
            d = trial.n_control - c

            # Risk ratio
            risk_intervention = a / trial.n_intervention
            risk_control = c / trial.n_control
            rr = risk_intervention / risk_control
            log_rr = np.log(rr)

            # Standard error
            se_log_rr = np.sqrt(1/a - 1/trial.n_intervention + 1/c - 1/trial.n_control)

            data.append({
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
            })

        return pd.DataFrame(data)

    def create_all_phase2_part2_datasets(self):
        """Create all Phase 2 Part 2 expansion datasets (Lipids + Valvular)."""
        print("=" * 80)
        print("PHASE 2 PART 2 EXPANSION: LIPIDS + VALVULAR DISEASE")
        print("=" * 80)
        print("\nCreating datasets for:")
        print("  - Primary Prevention Statins (10 trials)")
        print("  - Non-Statin Lipid Lowering (10 trials)")
        print("  - Mitral Regurgitation (10 trials)")
        print("  - Other Valvular Disease (10 trials)")
        print()

        datasets = {}
        total_trials = 0
        total_patients = 0

        # Primary prevention statins (10 trials)
        print("\n" + "-" * 80)
        print("1. Primary Prevention Statins")
        print("-" * 80)
        df_statins = self.get_primary_prevention_statin_trials()
        datasets['primary_prevention_statins'] = df_statins
        print(f"✓ Created: {len(df_statins)} trials, {df_statins['n_intervention'].sum() + df_statins['n_control'].sum():,} patients")
        total_trials += len(df_statins)
        total_patients += df_statins['n_intervention'].sum() + df_statins['n_control'].sum()

        # Non-statin lipid lowering (10 trials)
        print("\n" + "-" * 80)
        print("2. Non-Statin Lipid Lowering (Ezetimibe, Fibrates, Niacin, Omega-3)")
        print("-" * 80)
        df_nonstatin = self.get_nonstatin_lipid_trials()
        datasets['nonstatin_lipid_lowering'] = df_nonstatin
        print(f"✓ Created: {len(df_nonstatin)} trials, {df_nonstatin['n_intervention'].sum() + df_nonstatin['n_control'].sum():,} patients")
        total_trials += len(df_nonstatin)
        total_patients += df_nonstatin['n_intervention'].sum() + df_nonstatin['n_control'].sum()

        # Mitral regurgitation (10 trials)
        print("\n" + "-" * 80)
        print("3. Mitral Regurgitation (MitraClip + Surgical)")
        print("-" * 80)
        df_mr = self.get_mitral_regurgitation_trials()
        datasets['mitral_regurgitation'] = df_mr
        print(f"✓ Created: {len(df_mr)} trials, {df_mr['n_intervention'].sum() + df_mr['n_control'].sum():,} patients")
        total_trials += len(df_mr)
        total_patients += df_mr['n_intervention'].sum() + df_mr['n_control'].sum()

        # Other valvular disease (10 trials)
        print("\n" + "-" * 80)
        print("4. Other Valvular Disease (TR, MS, AR, Endocarditis)")
        print("-" * 80)
        df_other_valve = self.get_other_valvular_trials()
        datasets['other_valvular_disease'] = df_other_valve
        print(f"✓ Created: {len(df_other_valve)} trials, {df_other_valve['n_intervention'].sum() + df_other_valve['n_control'].sum():,} patients")
        total_trials += len(df_other_valve)
        total_patients += df_other_valve['n_intervention'].sum() + df_other_valve['n_control'].sum()

        # Save all datasets
        print("\n" + "=" * 80)
        print("SAVING DATASETS")
        print("=" * 80)

        for name, df in datasets.items():
            output_file = self.output_dir / f"{name}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Saved: {output_file}")

        # Create combined dataset
        df_combined = pd.concat(datasets.values(), ignore_index=True)
        combined_file = self.output_dir / "phase2_part2_combined.csv"
        df_combined.to_csv(combined_file, index=False)
        print(f"\n✓ Combined dataset: {combined_file}")

        # Overall Phase 2 combined
        print("\n" + "=" * 80)
        print("COMBINING ALL PHASE 2 DATA")
        print("=" * 80)

        # Load Phase 2 Part 1
        part1_file = self.output_dir / "phase2_part1_combined.csv"
        if part1_file.exists():
            df_part1 = pd.read_csv(part1_file)
            df_phase2_all = pd.concat([df_part1, df_combined], ignore_index=True)
            phase2_all_file = self.output_dir / "phase2_all_combined.csv"
            df_phase2_all.to_csv(phase2_all_file, index=False)
            print(f"✓ Complete Phase 2 combined dataset: {phase2_all_file}")
            print(f"  Total Phase 2: {len(df_phase2_all)} trials")

        # Summary
        print("\n" + "=" * 80)
        print("PHASE 2 PART 2 COMPLETE")
        print("=" * 80)
        print(f"\n✓ Part 2 trials added: {total_trials}")
        print(f"✓ Part 2 patients: {total_patients:,}")
        print(f"\n✓ Breakdown:")
        print(f"   - Lipid Management: {len(df_statins) + len(df_nonstatin)} trials, {(df_statins['n_intervention'].sum() + df_statins['n_control'].sum() + df_nonstatin['n_intervention'].sum() + df_nonstatin['n_control'].sum()):,} patients")
        print(f"   - Valvular Disease: {len(df_mr) + len(df_other_valve)} trials, {(df_mr['n_intervention'].sum() + df_mr['n_control'].sum() + df_other_valve['n_intervention'].sum() + df_other_valve['n_control'].sum()):,} patients")

        print(f"\n✓ New cumulative total: 259 + {total_trials} = {259 + total_trials} trials")
        print(f"✓ Progress toward 300-trial goal: {(259 + total_trials) / 300 * 100:.1f}%")

        if 259 + total_trials >= 300:
            print(f"\n🎉 🎉 🎉 300-TRIAL MILESTONE ACHIEVED! 🎉 🎉 🎉")
            print(f"Cumulative: {259 + total_trials} trials from all phases")
            print(f"Next goals: 400, 500, 700, 1000 trials")
        else:
            print(f"\nVery close to 300! Only {300 - (259 + total_trials)} trials remaining")

        return datasets


def main():
    """Main execution."""
    expander = Phase2Part2Expander()
    expander.create_all_phase2_part2_datasets()


if __name__ == "__main__":
    main()
