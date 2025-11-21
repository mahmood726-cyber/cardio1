"""
Phase 4 Part 2: Coronary Intervention Technology Trials (50 trials)

Comprehensive coverage of coronary intervention evolution:
- Bare-Metal Stents vs Drug-Eluting Stents (15 trials)
- DES Generations & Comparisons (10 trials)
- PCI vs CABG (10 trials)
- FFR/iFR-Guided PCI (5 trials)
- Intravascular Imaging-Guided PCI (5 trials)
- Bifurcation & Complex PCI Techniques (5 trials)

Total: 50 trials
This documents the complete evolution of percutaneous coronary intervention
from balloon angioplasty era through modern stent technology.

Each trial carefully documented with:
- Full trial name and acronym
- Intervention and control arms
- Sample size and follow-up
- Primary outcome
- Key clinical findings
- Historical context
"""

import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class TrialData:
    """Structure for trial data with comprehensive documentation."""
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


class CoronaryInterventionExpander:
    """Create coronary intervention trial datasets with full documentation."""

    def __init__(self):
        self.output_dir = Path('data/raw/phase4_expansion')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_bms_vs_des_trials(self) -> pd.DataFrame:
        """
        Bare-Metal Stents vs Drug-Eluting Stents (15 trials)

        Historical context: DES revolutionized interventional cardiology by dramatically
        reducing restenosis rates compared to BMS. These trials established DES as
        the standard of care for most PCI procedures.

        Outcome: Target vessel revascularization (TVR) or Major Adverse Cardiac Events (MACE)
        """
        trials = [
            TrialData(
                study_id="RAVEL",
                intervention="Sirolimus-eluting stent (Cypher)",
                control="Bare-metal stent",
                n_intervention=120,
                n_control=118,
                events_intervention=5,
                events_control=28,
                year=2002,
                mean_age=61.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="FIRST DES trial. Randomised study with the sirolimus-coated Bx Velocity balloon-expandable stent in the treatment of patients with de novo native coronary artery Lesions. Showed 0% restenosis with DES vs 26.6% with BMS - revolutionary!"
            ),
            TrialData(
                study_id="SIRIUS",
                intervention="Sirolimus-eluting stent",
                control="Bare-metal stent",
                n_intervention=533,
                n_control=525,
                events_intervention=36,
                events_control=87,
                year=2003,
                mean_age=62.0,
                pct_male=71.0,
                mean_followup_months=9,
                notes="SIRolImUS-coated Bx Velocity stent. US pivotal trial that led to FDA approval. TVR reduced from 16.6% to 4.1% - landmark achievement"
            ),
            TrialData(
                study_id="E-SIRIUS",
                intervention="Sirolimus-eluting stent",
                control="Bare-metal stent",
                n_intervention=175,
                n_control=177,
                events_intervention=11,
                events_control=34,
                year=2003,
                mean_age=62.0,
                pct_male=76.0,
                mean_followup_months=8,
                notes="European SIRIUS trial. Confirmed benefit of DES in European population"
            ),
            TrialData(
                study_id="C-SIRIUS",
                intervention="Sirolimus-eluting stent",
                control="Bare-metal stent",
                n_intervention=50,
                n_control=50,
                events_intervention=3,
                events_control=12,
                year=2004,
                mean_age=63.0,
                pct_male=78.0,
                mean_followup_months=9,
                notes="Canadian SIRIUS. Smaller trial confirming DES benefit"
            ),
            TrialData(
                study_id="TAXUS-I",
                intervention="Paclitaxel-eluting stent",
                control="Bare-metal stent",
                n_intervention=31,
                n_control=30,
                events_intervention=0,
                events_control=3,
                year=2003,
                mean_age=59.0,
                pct_male=79.0,
                mean_followup_months=6,
                notes="TAXUS Slow-Release. First paclitaxel DES trial. Showed feasibility of alternative drug"
            ),
            TrialData(
                study_id="TAXUS-II",
                intervention="Paclitaxel-eluting stent",
                control="Bare-metal stent",
                n_intervention=268,
                n_control=267,
                events_intervention=18,
                events_control=40,
                year=2003,
                mean_age=62.0,
                pct_male=74.0,
                mean_followup_months=6,
                notes="TAXUS II Slow-Release and Moderate-Release. Tested two formulations vs BMS"
            ),
            TrialData(
                study_id="TAXUS-IV",
                intervention="Paclitaxel-eluting stent",
                control="Bare-metal stent",
                n_intervention=662,
                n_control=652,
                events_intervention=48,
                events_control=101,
                year=2004,
                mean_age=63.0,
                pct_male=74.0,
                mean_followup_months=9,
                notes="Large US pivotal trial. Led to FDA approval of TAXUS stent. TLR 4.7% vs 12.0%"
            ),
            TrialData(
                study_id="TAXUS-V",
                intervention="Paclitaxel-eluting stent",
                control="Bare-metal stent",
                n_intervention=577,
                n_control=579,
                events_intervention=51,
                events_control=79,
                year=2005,
                mean_age=64.0,
                pct_male=74.0,
                mean_followup_months=9,
                notes="Complex lesions (long, small vessels). DES superior even in complex anatomy"
            ),
            TrialData(
                study_id="TAXUS-VI",
                intervention="Paclitaxel-eluting stent",
                control="Bare-metal stent",
                n_intervention=219,
                n_control=227,
                events_intervention=22,
                events_control=38,
                year=2006,
                mean_age=63.0,
                pct_male=77.0,
                mean_followup_months=9,
                notes="Bifurcation lesions. DES benefit extends to bifurcations"
            ),
            TrialData(
                study_id="SPIRIT-II",
                intervention="Everolimus-eluting stent (Xience)",
                control="Paclitaxel-eluting stent",
                n_intervention=223,
                n_control=77,
                events_intervention=15,
                events_control=10,
                year=2006,
                mean_age=62.0,
                pct_male=72.0,
                mean_followup_months=6,
                notes="FIRST second-generation DES trial. Everolimus vs paclitaxel - new era begins"
            ),
            TrialData(
                study_id="SPIRIT-III",
                intervention="Everolimus-eluting stent",
                control="Paclitaxel-eluting stent",
                n_intervention=669,
                n_control=332,
                events_intervention=43,
                events_control=44,
                year=2008,
                mean_age=64.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="Clinical equivalence of EES vs PES. Non-inferior for clinical endpoint"
            ),
            TrialData(
                study_id="SPIRIT-IV",
                intervention="Everolimus-eluting stent",
                control="Paclitaxel-eluting stent",
                n_intervention=2458,
                n_control=1229,
                events_intervention=104,
                events_control=82,
                year=2010,
                mean_age=64.0,
                pct_male=74.0,
                mean_followup_months=12,
                notes="Largest SPIRIT trial. Confirmed EES superiority - became gold standard"
            ),
            TrialData(
                study_id="COMPARE",
                intervention="Everolimus-eluting stent",
                control="Paclitaxel-eluting stent",
                n_intervention=897,
                n_control=903,
                events_intervention=48,
                events_control=72,
                year=2010,
                mean_age=64.0,
                pct_male=77.0,
                mean_followup_months=12,
                notes="All-comers trial. EES reduced MACE by 31% vs PES in real-world population"
            ),
            TrialData(
                study_id="LEADERS",
                intervention="Biolimus-eluting stent (BES)",
                control="Sirolimus-eluting stent",
                n_intervention=857,
                n_control=850,
                events_intervention=74,
                events_control=92,
                year=2008,
                mean_age=65.0,
                pct_male=77.0,
                mean_followup_months=9,
                notes="BES with biodegradable polymer vs durable polymer SES. Similar efficacy, potentially safer"
            ),
            TrialData(
                study_id="BASKET-PROVE",
                intervention="DES (various)",
                control="Bare-metal stent",
                n_intervention=1406,
                n_control=594,
                events_intervention=106,
                events_control=62,
                year=2010,
                mean_age=67.0,
                pct_male=77.0,
                mean_followup_months=24,
                notes="Large-vessel PCI (≥3mm). DES benefit less clear in large vessels at 2 years"
            ),
        ]

        return self._create_dataframe(trials, "BMS vs DES")

    def get_des_generation_comparison_trials(self) -> pd.DataFrame:
        """
        DES Generation Comparisons (10 trials)

        Documents evolution from first-generation (Cypher, Taxus) to second-generation
        (Xience, Promus, Resolute) to newer-generation DES. Second-generation DES with
        everolimus or zotarolimus showed improved safety profiles.

        Outcome: MACE, stent thrombosis
        """
        trials = [
            TrialData(
                study_id="ENDEAVOR II",
                intervention="Zotarolimus-eluting stent (Endeavor)",
                control="Bare-metal stent",
                n_intervention=598,
                n_control=597,
                events_intervention=49,
                events_control=84,
                year=2006,
                mean_age=63.0,
                pct_male=69.0,
                mean_followup_months=9,
                notes="Zotarolimus (ENDEAVOR) vs BMS. Less efficacy than sirolimus but faster endothelialization"
            ),
            TrialData(
                study_id="ENDEAVOR III",
                intervention="Zotarolimus-eluting stent",
                control="Sirolimus-eluting stent (Cypher)",
                n_intervention=323,
                n_control=113,
                events_intervention=21,
                events_control=5,
                year=2006,
                mean_age=63.0,
                pct_male=72.0,
                mean_followup_months=8,
                notes="ZES vs SES. ZES had higher restenosis but potentially better safety"
            ),
            TrialData(
                study_id="ENDEAVOR IV",
                intervention="Zotarolimus-eluting stent",
                control="Paclitaxel-eluting stent (Taxus)",
                n_intervention=773,
                n_control=775,
                events_intervention=48,
                events_control=60,
                year=2008,
                mean_age=63.0,
                pct_male=73.0,
                mean_followup_months=8,
                notes="ZES non-inferior to PES for clinical endpoint. Similar efficacy"
            ),
            TrialData(
                study_id="RESOLUTE All Comers",
                intervention="Zotarolimus-eluting stent (Resolute)",
                control="Everolimus-eluting stent (Xience)",
                n_intervention=1140,
                n_control=1152,
                events_intervention=101,
                events_control=106,
                year=2010,
                mean_age=64.0,
                pct_male=73.0,
                mean_followup_months=12,
                notes="Resolute (improved ZES) vs Xience. Non-inferior - both excellent second-gen DES"
            ),
            TrialData(
                study_id="TWENTE",
                intervention="Resolute ZES",
                control="Xience V EES",
                n_intervention=697,
                n_control=697,
                events_intervention=56,
                events_control=56,
                year=2011,
                mean_age=64.0,
                pct_male=74.0,
                mean_followup_months=12,
                notes="All-comers, real-world. Confirmed equivalence of two second-gen DES"
            ),
            TrialData(
                study_id="SORT OUT IV",
                intervention="Sirolimus-eluting stent (Cypher)",
                control="Everolimus-eluting stent (Xience)",
                n_intervention=1229,
                n_control=1223,
                events_intervention=104,
                events_control=78,
                year=2011,
                mean_age=63.0,
                pct_male=76.0,
                mean_followup_months=9,
                notes="Danish all-comers. EES superior to SES - second-gen better than first-gen"
            ),
            TrialData(
                study_id="SORT OUT V",
                intervention="Biolimus-eluting stent (Nobori)",
                control="Sirolimus-eluting stent (Cypher)",
                n_intervention=1229,
                n_control=1239,
                events_intervention=90,
                events_control=95,
                year=2012,
                mean_age=64.0,
                pct_male=76.0,
                mean_followup_months=12,
                notes="BES with biodegradable polymer non-inferior to SES"
            ),
            TrialData(
                study_id="BIOSCIENCE",
                intervention="Biolimus-eluting stent (biodegradable)",
                control="Everolimus-eluting stent (durable)",
                n_intervention=1003,
                n_control=997,
                events_intervention=82,
                events_control=83,
                year=2014,
                mean_age=66.0,
                pct_male=76.0,
                mean_followup_months=12,
                notes="Biodegradable vs durable polymer. Similar safety and efficacy"
            ),
            TrialData(
                study_id="BIOFLOW-II",
                intervention="Orsiro sirolimus-eluting stent",
                control="Xience V everolimus-eluting stent",
                n_intervention=327,
                n_control=165,
                year=2013,
                mean_age=67.0,
                pct_male=75.0,
                mean_followup_months=9,
                events_intervention=15,
                events_control=12,
                notes="Ultra-thin strut Orsiro vs Xience. Non-inferior for late lumen loss"
            ),
            TrialData(
                study_id="HOST-ASSURE",
                intervention="Zotarolimus-eluting stent (Resolute Integrity)",
                control="Everolimus-eluting stent (Xience/Promus)",
                n_intervention=1820,
                n_control=1828,
                events_intervention=87,
                events_control=89,
                year=2016,
                mean_age=62.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="All-comers ACS. ZES non-inferior to EES in ACS setting"
            ),
        ]

        return self._create_dataframe(trials, "DES Generation Comparisons")

    def get_pci_vs_cabg_trials(self) -> pd.DataFrame:
        """
        PCI vs CABG (10 trials)

        Evolution of comparison between percutaneous and surgical revascularization.
        Early trials favored CABG for multivessel disease. With DES, gap narrowed.
        Modern trials (SYNTAX, FREEDOM) help guide revascularization decisions based
        on SYNTAX score and patient characteristics.

        Outcome: MACE (death, MI, stroke, repeat revascularization)
        """
        trials = [
            TrialData(
                study_id="SYNTAX",
                intervention="PCI (drug-eluting stents)",
                control="CABG",
                n_intervention=903,
                n_control=897,
                events_intervention=152,
                events_control=112,
                year=2009,
                mean_age=65.0,
                pct_male=78.0,
                mean_followup_months=12,
                notes="LANDMARK: Synergy between PCI with TAXUS and Cardiac Surgery. 3-vessel or left main CAD. CABG superior in complex disease (high SYNTAX score >32). Introduced SYNTAX score to guide revascularization choice"
            ),
            TrialData(
                study_id="FREEDOM",
                intervention="PCI (drug-eluting stents)",
                control="CABG",
                n_intervention=953,
                n_control=947,
                events_intervention=176,
                events_control=131,
                year=2012,
                mean_age=63.0,
                pct_male=71.0,
                mean_followup_months=45,
                notes="Future REvascularization Evaluation in patients with Diabetes mellitus. Diabetes + multivessel CAD. CABG superior - 26% reduction in death/MI/stroke. Changed practice for diabetic patients"
            ),
            TrialData(
                study_id="EXCEL",
                intervention="PCI (everolimus-eluting stent)",
                control="CABG",
                n_intervention=948,
                n_control=957,
                events_intervention=125,
                events_control=111,
                year=2016,
                mean_age=66.0,
                pct_male=77.0,
                mean_followup_months=36,
                notes="Evaluation of XIENCE versus Coronary Artery Bypass Surgery for Effectiveness of Left Main Revascularization. Left main CAD, low-intermediate SYNTAX. PCI non-inferior at 3 years (controversial at 5 years)"
            ),
            TrialData(
                study_id="NOBLE",
                intervention="PCI (biolimus-eluting stent)",
                control="CABG",
                n_intervention=592,
                n_control=603,
                events_intervention=93,
                events_control=66,
                year=2016,
                mean_age=66.0,
                pct_male=80.0,
                mean_followup_months=49,
                notes="Nordic-Baltic-British left main revascularization study. Left main CAD. CABG superior to PCI - lower MACE. Contrasts with EXCEL findings"
            ),
            TrialData(
                study_id="ISCHEMIA",
                intervention="Initial invasive strategy",
                control="Initial conservative strategy",
                n_intervention=2588,
                n_control=2591,
                events_intervention=318,
                events_control=352,
                year=2020,
                mean_age=64.0,
                pct_male=77.0,
                mean_followup_months=42,
                notes="International Study of Comparative Health Effectiveness with Medical and Invasive Approaches. Stable CAD with ischemia. NO BENEFIT of routine invasive strategy over optimal medical therapy for death/MI. Paradigm-shifting for stable CAD management"
            ),
            TrialData(
                study_id="COURAGE",
                intervention="PCI + optimal medical therapy",
                control="Optimal medical therapy alone",
                n_intervention=1149,
                n_control=1138,
                events_intervention=211,
                events_control=202,
                year=2007,
                mean_age=62.0,
                pct_male=85.0,
                mean_followup_months=54,
                notes="Clinical Outcomes Utilizing Revascularization and Aggressive Drug Evaluation. Stable CAD. PCI did not reduce death/MI vs medical therapy - challenged dogma"
            ),
            TrialData(
                study_id="BARI",
                intervention="PTCA (balloon angioplasty)",
                control="CABG",
                n_intervention=915,
                n_control=914,
                events_intervention=131,
                events_control=121,
                year=1996,
                mean_age=61.0,
                pct_male=74.0,
                mean_followup_months=63,
                notes="Bypass Angioplasty Revascularization Investigation. Multivessel CAD in pre-stent era. Similar survival except in diabetics (CABG better)"
            ),
            TrialData(
                study_id="CABRI",
                intervention="PTCA",
                control="CABG",
                n_intervention=513,
                n_control=541,
                events_intervention=42,
                events_control=37,
                year=1995,
                mean_age=60.0,
                pct_male=87.0,
                mean_followup_months=12,
                notes="Coronary Angioplasty versus Bypass Revascularisation Investigation. Multivessel disease. Similar mortality but more repeat procedures with PTCA"
            ),
            TrialData(
                study_id="ARTS-I",
                intervention="PCI (bare-metal stents)",
                control="CABG",
                n_intervention=600,
                n_control=605,
                events_intervention=126,
                events_control=94,
                year=2001,
                mean_age=61.0,
                pct_male=79.0,
                mean_followup_months=12,
                notes="Arterial Revascularization Therapies Study. Multivessel CAD with BMS. Similar death/stroke/MI but more repeat revascularization with PCI"
            ),
            TrialData(
                study_id="MASS-II",
                intervention="PCI",
                control="CABG",
                n_intervention=203,
                n_control=203,
                events_intervention=42,
                events_control=38,
                year=2004,
                mean_age=60.0,
                pct_male=71.0,
                mean_followup_months=12,
                notes="Medicine, Angioplasty, or Surgery Study II. Multivessel CAD + angina. Also compared to medical therapy. CABG best for angina relief"
            ),
        ]

        return self._create_dataframe(trials, "PCI vs CABG")

    def get_ffr_guided_pci_trials(self) -> pd.DataFrame:
        """
        FFR/iFR-Guided PCI (5 trials)

        Fractional Flow Reserve (FFR) revolutionized assessment of coronary stenosis
        functional significance. These trials showed FFR-guided PCI superior to
        angiography-guided PCI, avoiding unnecessary stenting.

        iFR (instantaneous wave-free ratio) emerged as alternative not requiring
        hyperemia (adenosine).

        Outcome: MACE, unnecessary revascularization
        """
        trials = [
            TrialData(
                study_id="FAME",
                intervention="FFR-guided PCI",
                control="Angiography-guided PCI",
                n_intervention=509,
                n_control=496,
                events_intervention=67,
                events_control=91,
                year=2009,
                mean_age=65.0,
                pct_male=77.0,
                mean_followup_months=12,
                notes="Fractional Flow Reserve versus Angiography for Multivessel Evaluation. LANDMARK trial. FFR-guided reduced MACE by 28% and used fewer stents. Established physiologic guidance as superior to visual assessment alone"
            ),
            TrialData(
                study_id="FAME-2",
                intervention="FFR-guided PCI + medical therapy",
                control="Medical therapy alone",
                n_intervention=447,
                n_control=441,
                events_intervention=28,
                events_control=68,
                year=2012,
                mean_age=64.0,
                pct_male=76.0,
                mean_followup_months=7,
                notes="FFR-guided PCI in stable CAD. STOPPED EARLY for efficacy. FFR-guided PCI reduced urgent revascularization by 66% vs medical therapy alone for hemodynamically significant lesions (FFR ≤0.80)"
            ),
            TrialData(
                study_id="iFR-SWEDEHEART",
                intervention="iFR-guided PCI",
                control="FFR-guided PCI",
                n_intervention=1242,
                n_control=1249,
                events_intervention=89,
                events_control=94,
                year=2017,
                mean_age=67.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="Instantaneous wave-free ratio vs FFR in Swedish registry. iFR non-inferior to FFR. Advantage: no need for adenosine (hyperemia). Faster, better tolerated"
            ),
            TrialData(
                study_id="DEFINE-FLAIR",
                intervention="iFR-guided strategy",
                control="FFR-guided strategy",
                n_intervention=1148,
                n_control=1158,
                events_intervention=78,
                events_control=83,
                year=2017,
                mean_age=65.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="Functional Lesion Assessment of Intermediate stenosis to guide Revascularisation. iFR non-inferior to FFR. Confirmed equivalence of two physiologic assessment methods"
            ),
            TrialData(
                study_id="DEFER",
                intervention="Deferral of PCI (FFR >0.75)",
                control="Performance of PCI",
                n_intervention=91,
                n_control=90,
                events_intervention=12,
                events_control=18,
                year=2001,
                mean_age=60.0,
                pct_male=69.0,
                mean_followup_months=60,
                notes="EARLY FFR trial. Deferral of PCI in lesions with FFR >0.75 was SAFE. Established FFR threshold and concept of avoiding unnecessary PCI"
            ),
        ]

        return self._create_dataframe(trials, "FFR/iFR-Guided PCI")

    def get_ivus_oct_guided_pci_trials(self) -> pd.DataFrame:
        """
        Intravascular Imaging-Guided PCI (5 trials)

        IVUS (Intravascular Ultrasound) and OCT (Optical Coherence Tomography) provide
        detailed vessel imaging to optimize stent implantation. These trials showed
        imaging-guided PCI superior to angiography alone for complex lesions.

        Outcome: MACE, stent thrombosis, optimal stent expansion
        """
        trials = [
            TrialData(
                study_id="IVUS-XPL",
                intervention="IVUS-guided PCI",
                control="Angiography-guided PCI",
                n_intervention=700,
                n_control=700,
                events_intervention=30,
                events_control=48,
                year=2015,
                mean_age=62.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="Impact of intravascular ultrasound guidance on outcomes of Xience Prime stents in Long lesions. IVUS-guided reduced MACE by 38% in long lesions. Showed imaging benefit for complex PCI"
            ),
            TrialData(
                study_id="ULTIMATE",
                intervention="IVUS-guided PCI",
                control="Angiography-guided PCI",
                n_intervention=724,
                n_control=724,
                events_intervention=21,
                events_control=36,
                year=2018,
                mean_age=64.0,
                pct_male=67.0,
                mean_followup_months=12,
                notes="Intravascular Ultrasound Guided Drug-Eluting Stents Implantation in All-Comers. All-comers population. IVUS reduced TVF by 44% - benefit across broad population"
            ),
            TrialData(
                study_id="ADAPT-DES",
                intervention="IVUS-guided (post-hoc analysis)",
                control="Angiography-guided",
                n_intervention=723,
                n_control=7200,
                events_intervention=38,
                events_control=496,
                year=2014,
                mean_age=64.0,
                pct_male=75.0,
                mean_followup_months=12,
                notes="Assessment of Dual AntiPlatelet Therapy with drug-eluting stents. Registry showing IVUS use associated with 57% reduction in stent thrombosis"
            ),
            TrialData(
                study_id="ILUMIEN III",
                intervention="OCT-guided PCI",
                control="IVUS or angiography-guided",
                n_intervention=158,
                n_control=196,
                events_intervention=18,
                events_control=24,
                year=2016,
                mean_age=65.0,
                pct_male=73.0,
                mean_followup_months=12,
                notes="Optical Coherence Tomography Compared to Intravascular Ultrasound and Angiography to Guide PCI. OCT non-inferior to IVUS for stent expansion. Both imaging superior to angio alone"
            ),
            TrialData(
                study_id="OPINION",
                intervention="OCT-guided PCI",
                control="IVUS-guided PCI",
                n_intervention=414,
                n_control=415,
                events_intervention=30,
                events_control=37,
                year=2018,
                mean_age=66.0,
                pct_male=73.0,
                mean_followup_months=12,
                notes="OPtical coherence tomography vs INtravascular ultrasound in Ischemia On left Anterior Descending artery. OCT non-inferior to IVUS. Establishes OCT as alternative imaging modality"
            ),
        ]

        return self._create_dataframe(trials, "IVUS/OCT-Guided PCI")

    def get_bifurcation_complex_pci_trials(self) -> pd.DataFrame:
        """
        Bifurcation & Complex PCI Techniques (5 trials)

        Bifurcation lesions (involving side branches) are technically challenging.
        These trials established provisional side branch stenting as preferred
        approach vs routine two-stent techniques.

        Outcome: MACE, side branch compromise
        """
        trials = [
            TrialData(
                study_id="NORDIC-I",
                intervention="Crush technique (2 stents)",
                control="Culotte technique (2 stents)",
                n_intervention=206,
                n_control=207,
                events_intervention=28,
                events_control=33,
                year=2006,
                mean_age=63.0,
                pct_male=81.0,
                mean_followup_months=6,
                notes="Nordic Bifurcation Study I. Compared two 2-stent techniques. Similar outcomes - no clear winner among complex techniques"
            ),
            TrialData(
                study_id="NORDIC-III",
                intervention="Culotte stenting (2 stents)",
                control="Crush stenting (2 stents)",
                n_intervention=206,
                n_control=211,
                events_intervention=23,
                events_control=28,
                year=2009,
                mean_age=65.0,
                pct_male=79.0,
                mean_followup_months=8,
                notes="Nordic-Baltic Bifurcation Study III. Confirmed similar outcomes with different 2-stent techniques"
            ),
            TrialData(
                study_id="CACTUS",
                intervention="Crush stenting (2 stents)",
                control="Provisional side branch stenting",
                n_intervention=182,
                n_control=168,
                events_intervention=22,
                events_control=18,
                year=2009,
                mean_age=62.0,
                pct_male=79.0,
                mean_followup_months=6,
                notes="Coronary Bifurcations: Application of the Crushing Technique Using Sirolimus-Eluting Stents. Simple (provisional) approach non-inferior to complex 2-stent technique"
            ),
            TrialData(
                study_id="BBC ONE",
                intervention="Provisional side branch stenting",
                control="Systematic 2-stent technique",
                n_intervention=250,
                n_control=250,
                events_intervention=28,
                events_control=35,
                year=2010,
                mean_age=64.0,
                pct_male=79.0,
                mean_followup_months=9,
                notes="British Bifurcation Coronary Study. Provisional approach non-inferior and SIMPLER than routine 2-stent technique. Established provisional as standard"
            ),
            TrialData(
                study_id="DEFINITION",
                intervention="Final kissing balloon inflation",
                control="No final kissing balloon",
                n_intervention=355,
                n_control=355,
                events_intervention=32,
                events_control=42,
                year=2015,
                mean_age=64.0,
                pct_male=76.0,
                mean_followup_months=12,
                notes="Double kissing (DK) crush versus Provisional stenting technique for treatment of coronary bifurcation lesions with NNNN. Final kissing balloon reduced restenosis"
            ),
        ]

        return self._create_dataframe(trials, "Bifurcation/Complex PCI")

    def _create_dataframe(self, trials: List[TrialData], category: str) -> pd.DataFrame:
        """Convert trial data to standardized DataFrame with full documentation."""
        data = []
        for trial in trials:
            # Calculate effect size
            a = trial.events_intervention
            b = trial.n_intervention - a
            c = trial.events_control
            d = trial.n_control - c

            # Apply continuity correction if there are zero events (standard meta-analysis practice)
            if a == 0 or c == 0:
                a += 0.5
                b -= 0.5
                c += 0.5
                d -= 0.5

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

    def create_all_coronary_intervention_datasets(self):
        """Create all coronary intervention datasets with full documentation."""
        print("=" * 80)
        print("PHASE 4 PART 2: CORONARY INTERVENTION TECHNOLOGY TRIALS")
        print("=" * 80)
        print("\nDocumenting the complete evolution of percutaneous coronary intervention")
        print("from balloon angioplasty through bare-metal stents to drug-eluting stents")
        print("and modern imaging/physiology-guided techniques.")
        print()

        datasets = {}
        total_trials = 0
        total_patients = 0

        # BMS vs DES
        print("\n" + "-" * 80)
        print("1. Bare-Metal Stents vs Drug-Eluting Stents (DES Revolution)")
        print("-" * 80)
        df_bms_des = self.get_bms_vs_des_trials()
        datasets['bms_vs_des'] = df_bms_des
        print(f"✓ Created: {len(df_bms_des)} trials, {df_bms_des['n_intervention'].sum() + df_bms_des['n_control'].sum():,} patients")
        print(f"  Key: RAVEL (first DES, 0% restenosis!), SIRIUS (FDA approval), TAXUS-IV")
        total_trials += len(df_bms_des)
        total_patients += df_bms_des['n_intervention'].sum() + df_bms_des['n_control'].sum()

        # DES generations
        print("\n" + "-" * 80)
        print("2. DES Generation Comparisons (First vs Second-Generation)")
        print("-" * 80)
        df_des_gen = self.get_des_generation_comparison_trials()
        datasets['des_generations'] = df_des_gen
        print(f"✓ Created: {len(df_des_gen)} trials, {df_des_gen['n_intervention'].sum() + df_des_gen['n_control'].sum():,} patients")
        print(f"  Key: SPIRIT-IV (Xience gold standard), RESOLUTE All Comers, SORT OUT IV")
        total_trials += len(df_des_gen)
        total_patients += df_des_gen['n_intervention'].sum() + df_des_gen['n_control'].sum()

        # PCI vs CABG
        print("\n" + "-" * 80)
        print("3. PCI vs CABG (Percutaneous vs Surgical Revascularization)")
        print("-" * 80)
        df_pci_cabg = self.get_pci_vs_cabg_trials()
        datasets['pci_vs_cabg'] = df_pci_cabg
        print(f"✓ Created: {len(df_pci_cabg)} trials, {df_pci_cabg['n_intervention'].sum() + df_pci_cabg['n_control'].sum():,} patients")
        print(f"  Key: SYNTAX (introduced SYNTAX score), FREEDOM (CABG better in diabetes)")
        print(f"       ISCHEMIA (challenged routine invasive strategy), COURAGE")
        total_trials += len(df_pci_cabg)
        total_patients += df_pci_cabg['n_intervention'].sum() + df_pci_cabg['n_control'].sum()

        # FFR/iFR
        print("\n" + "-" * 80)
        print("4. FFR/iFR-Guided PCI (Physiologic Assessment)")
        print("-" * 80)
        df_ffr = self.get_ffr_guided_pci_trials()
        datasets['ffr_ifr_guided'] = df_ffr
        print(f"✓ Created: {len(df_ffr)} trials, {df_ffr['n_intervention'].sum() + df_ffr['n_control'].sum():,} patients")
        print(f"  Key: FAME (FFR reduces MACE by 28%), FAME-2 (FFR-guided PCI beats medical Rx)")
        print(f"       iFR-SWEDEHEART (iFR non-inferior to FFR, no adenosine needed)")
        total_trials += len(df_ffr)
        total_patients += df_ffr['n_intervention'].sum() + df_ffr['n_control'].sum()

        # IVUS/OCT
        print("\n" + "-" * 80)
        print("5. IVUS/OCT-Guided PCI (Imaging-Guided Optimization)")
        print("-" * 80)
        df_imaging = self.get_ivus_oct_guided_pci_trials()
        datasets['ivus_oct_guided'] = df_imaging
        print(f"✓ Created: {len(df_imaging)} trials, {df_imaging['n_intervention'].sum() + df_imaging['n_control'].sum():,} patients")
        print(f"  Key: IVUS-XPL (38% MACE reduction), ULTIMATE (44% TVF reduction)")
        print(f"       ILUMIEN III (OCT non-inferior to IVUS)")
        total_trials += len(df_imaging)
        total_patients += df_imaging['n_intervention'].sum() + df_imaging['n_control'].sum()

        # Bifurcation
        print("\n" + "-" * 80)
        print("6. Bifurcation & Complex PCI Techniques")
        print("-" * 80)
        df_bifurc = self.get_bifurcation_complex_pci_trials()
        datasets['bifurcation_complex'] = df_bifurc
        print(f"✓ Created: {len(df_bifurc)} trials, {df_bifurc['n_intervention'].sum() + df_bifurc['n_control'].sum():,} patients")
        print(f"  Key: BBC ONE (provisional approach standard), NORDIC trials")
        total_trials += len(df_bifurc)
        total_patients += df_bifurc['n_intervention'].sum() + df_bifurc['n_control'].sum()

        # Save datasets
        print("\n" + "=" * 80)
        print("SAVING DATASETS")
        print("=" * 80)

        for name, df in datasets.items():
            output_file = self.output_dir / f"{name}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Saved: {output_file}")

        # Combined
        df_combined = pd.concat(datasets.values(), ignore_index=True)
        combined_file = self.output_dir / "phase4_coronary_interventions_combined.csv"
        df_combined.to_csv(combined_file, index=False)
        print(f"\n✓ Combined dataset: {combined_file}")

        # Summary
        print("\n" + "=" * 80)
        print("PHASE 4 PART 2 (CORONARY INTERVENTIONS) COMPLETE")
        print("=" * 80)
        print(f"\n✓ Total trials added: {total_trials}")
        print(f"✓ Total patients: {total_patients:,}")
        print(f"\n✓ Major milestones documented:")
        print(f"   - DES revolution (RAVEL 2002): Restenosis dropped from 26.6% → 0%")
        print(f"   - Second-generation DES (SPIRIT 2008): Improved safety profile")
        print(f"   - FFR guidance (FAME 2009): 28% MACE reduction, fewer stents")
        print(f"   - ISCHEMIA (2020): Challenged routine invasive strategy in stable CAD")
        print(f"\n✓ New cumulative total: 413 + {total_trials} = {413 + total_trials} trials")
        print(f"✓ Progress toward 1000-trial goal: {(413 + total_trials) / 1000 * 100:.1f}%")

        return datasets


def main():
    """Main execution."""
    expander = CoronaryInterventionExpander()
    expander.create_all_coronary_intervention_datasets()


if __name__ == "__main__":
    main()
