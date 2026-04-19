import streamlit as st
import pandas as pd
import math
import collections
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EpiLab — Outbreak Lab",
    page_icon="🔍",
    layout="wide",
)

# ── Minimal branding header ───────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1e3a5f 0%,#2563eb 100%);
     padding:18px 28px 14px 28px;border-radius:10px;margin-bottom:20px;">
  <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
    <div>
      <div style="font-size:26px;font-weight:800;color:white;letter-spacing:-0.5px;">
        🔍 EpiLab — Outbreak Lab
      </div>
      <div style="font-size:13px;color:#93c5fd;margin-top:2px;">
        A free preview module from <strong style="color:#bfdbfe;">EpiLab Interactive</strong>
        &nbsp;·&nbsp; Developed by Mary W. Mathis, DrPH
      </div>
    </div>
    <div style="margin-left:auto;">
      <a href="https://mathiscope504.gumroad.com/l/mknsox" target="_blank"
         style="background:#f59e0b;color:#1a1a1a;font-weight:700;font-size:12px;
                padding:8px 16px;border-radius:6px;text-decoration:none;white-space:nowrap;">
        🛒 Get Full EpiLab →
      </a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.title("🔍 Outbreak Lab")
st.markdown("""
You are an Epidemic Intelligence Service (EIS) officer. Three outbreaks have been reported. Work through the clues, make decisions, calculate the numbers, and solve each investigation. Every decision maps to the **10-step outbreak investigation framework**.
""")

import math as _omath

OB1_STEPS = [
    "Step 1 — Verify the diagnosis & establish the outbreak",
    "Step 2 — Construct a case definition",
    "Step 3 — Epidemic curve & descriptive epidemiology",
    "Step 4 — Generate & test hypotheses (attack rates)",
    "Step 5 — Control measures & resolution",
]
OB2_STEPS = [
    "Step 1 — Verify diagnosis & chain of infection",
    "Step 2 — Herd immunity & the math behind the outbreak",
    "Step 3 — Contact tracing & case finding",
    "Step 4 — Control measures",
    "Step 5 — Could this have been prevented?",
]
OB3_STEPS = [
    "Step 1 — Build the case definition & line list",
    "Step 2 — Epidemic curve & incubation period estimation",
    "Step 3 — Food-specific attack rates (calculate)",
    "Step 4 — Environmental investigation",
    "Step 5 — Control, report & prevent recurrence",
]

def next_step_button(current_step, all_steps, idx_key, label="Next Step"):
    """Advance step using a plain (non-widget-bound) index in session state."""
    # Initialize if not set
    if idx_key not in st.session_state:
        st.session_state[idx_key] = 0
    idx = all_steps.index(current_step) if current_step in all_steps else 0
    if idx >= 0 and idx < len(all_steps) - 1:
        next_label = all_steps[idx + 1]
        st.markdown("---")
        col_nb1, col_nb2, col_nb3 = st.columns([3, 2, 3])
        with col_nb2:
            if st.button(f"➡️ {label}", key=f"next_{idx_key}_{idx}", use_container_width=True):
                st.session_state[idx_key] = idx + 1
                st.rerun()
        st.caption(f"Next: **{next_label}**")
    elif idx == len(all_steps) - 1:
        st.markdown("---")
        st.success("🎉 **Scenario complete!** Select a new outbreak above, or jump back to any step to review.")


# ── Compendium reference ──────────────────────────────────────────────────
with st.expander("📋 Field Reference — Compendium of Acute Foodborne GI Diseases (keep open while investigating)"):
    st.markdown("Use this table to match incubation period, symptoms, and food vehicle to the most likely agent.")
    st.divider()

    st.markdown("#### Group I — Short incubation, vomiting predominant, little or no fever")
    group1 = [
        ["Bacillus cereus (emetic)", "0.5–6 hours", "Nausea, vomiting, cramps; diarrhea occasionally", "Boiled or fried rice"],
        ["Staphylococcus aureus", "2–4 h (range 0.5–8 h)", "Nausea, cramps, vomiting, diarrhea; fever may be present", "Ham, beef, poultry; cream-filled pastries; custard; high-protein leftovers"],
        ["Heavy metals (arsenic, cadmium, copper, mercury, lead, zinc)", "<1–6 hours", "Nausea, vomiting, cramps, diarrhea", "High-acid food/beverages stored in coated or metal-contaminated containers"],
    ]
    import pandas as pd
    g1_df = pd.DataFrame(group1, columns=["Agent", "Incubation", "Symptoms", "Characteristic foods"])
    st.dataframe(g1_df, use_container_width=True, hide_index=True)

    st.markdown("#### Group II — Moderate to long incubation, diarrhea predominant, often with fever")
    group2 = [
        ["Bacillus cereus (diarrheal)", "6–24 hours", "Abdominal cramps, watery diarrhea; vomiting occasionally", "Custards, cereal products, meat loaf, sauces, refried beans, dried potatoes"],
        ["Campylobacter jejuni", "2–5 days (1–10 d)", "Diarrhea (often bloody), cramps, fever, nausea, vomiting", "Raw milk, poultry, water, raw clams, beef liver"],
        ["Clostridium perfringens", "8–12 h (6–24 h)", "Abdominal cramps, watery diarrhea; vomiting and fever rare", "Inadequately heated/reheated meats, stews, gravy, refried beans"],
        ["ETEC (Enterotoxigenic E. coli)", "10–72 hours", "Abdominal cramps, watery diarrhea", "Uncooked vegetables, salads, water"],
        ["STEC / E. coli O157:H7", "3–4 days (2–10 d)", "Bloody diarrhea, cramps; fever infrequent; HUS risk", "Undercooked ground beef, raw milk, produce, soft cheese, water"],
        ["Norovirus", "24–48 h (10–50 h)", "Nausea, vomiting, cramps, watery diarrhea, low fever", "Fecally contaminated ready-to-eat foods, frostings, clams, oysters, water"],
        ["Salmonella spp. (non-typhoidal)", "12–72 h (6 h–7 d)", "Diarrhea, cramps, fever, headache; vomiting occasionally", "Poultry, eggs, meat, raw milk, produce"],
        ["Shigella spp.", "1–3 days (1–7 d)", "Cramps, fever, diarrhea (often bloody), watery diarrhea, nausea", "Fecally contaminated foods, salads, cut fruit, water"],
        ["Vibrio cholerae", "24–72 h (hours–5 d)", "Profuse watery diarrhea (rice-water stools)", "Raw fish/shellfish, crustacean, fecally contaminated water/foods"],
        ["Vibrio parahaemolyticus", "12–24 h (4–96 h)", "Cramps, watery diarrhea, nausea, vomiting, fever; bloody diarrhea occasionally", "Marine fish, shellfish, crustacean (raw or undercooked)"],
        ["Yersinia enterocolitica", "4–6 days (1–14 d)", "Fever, diarrhea, cramps, vomiting; may mimic appendicitis", "Raw milk, tofu, water, undercooked pork"],
    ]
    g2_df = pd.DataFrame(group2, columns=["Agent", "Incubation", "Symptoms", "Characteristic foods"])
    st.dataframe(g2_df, use_container_width=True, hide_index=True)

    st.markdown("#### Group III — Special presentations")
    group3 = [
        ["Clostridium botulinum", "12–48 h (6 h–8 d)", "Nausea, vomiting, diarrhea; blurred vision; descending paralysis", "Canned low-acid foods, smoked fish, cooked potatoes, marine mammals"],
        ["Cryptosporidium spp.", "7 days (2–14 d)", "Watery diarrhea, cramps, nausea, vomiting, fever", "Water, fecally contaminated foods"],
        ["Giardia intestinalis", "7–10 days (3–25 d)", "Cramps, diarrhea, watery diarrhea, fatty stools, bloating", "Water, fecally contaminated foods"],
        ["Hepatitis A virus", "28–30 days (15–50 d)", "Fever, nausea, diarrhea, anorexia, jaundice", "Raw shellfish, cold fecally contaminated foods, water"],
        ["Scombroid fish poisoning", "Minutes–1 hour", "Headache, nausea, vomiting, flushing, dizziness, burning mouth/throat", "Temperature-abused fish (tuna, mahi mahi, bluefish, mackerel, marlin, bonito)"],
    ]
    g3_df = pd.DataFrame(group3, columns=["Agent", "Incubation", "Symptoms", "Characteristic foods"])
    st.dataframe(g3_df, use_container_width=True, hide_index=True)

    st.markdown("""
<div style="font-size:11px;color:#6b7280;margin-top:8px;line-height:1.6;">
<b>Symptom key:</b> AC = cramps; D = diarrhea; BD = bloody diarrhea; WD = watery diarrhea; F = fever; H = headache; N = nausea; V = vomiting<br>
<b>Sources:</b> Heymann DL. <i>Control of Communicable Diseases Manual</i> (19th ed.), APHA 2008; CDC; Wisconsin Division of Public Health P-01257 (4/2016).<br>
<b>How to use:</b> (1) Note incubation period from exposure to symptom onset. (2) Identify predominant symptom pattern. (3) Match to characteristic food vehicle. These three together narrow the differential significantly before lab results return.
</div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🔍 Quick differential by incubation period")
    diff_col1, diff_col2, diff_col3 = st.columns(3)
    with diff_col1:
        st.markdown("""
**< 6 hours**
- Staph aureus toxin
- B. cereus (emetic)
- Heavy metals
- Scombroid (minutes)

*Vomiting dominant; preformed toxin — no replication needed*
        """)
    with diff_col2:
        st.markdown("""
**6–72 hours**
- Clostridium perfringens
- B. cereus (diarrheal)
- Norovirus
- Salmonella
- ETEC

*Mixed picture; diarrhea often prominent*
        """)
    with diff_col3:
        st.markdown("""
**> 3 days**
- Campylobacter (2–5 d)
- STEC/O157 (3–4 d)
- Yersinia (4–6 d)
- Giardia (7–10 d)
- Hepatitis A (28–30 d)

*Longer incubation; fever common; HUS/complications possible*
        """)

# Track scenario to reset step indices when scenario changes
if "ob_prev_scenario" not in st.session_state:
    st.session_state["ob_prev_scenario"] = ""

ob_scenario = st.selectbox("Select an outbreak to investigate:", [
    "— Choose an outbreak —",
    "🍽️ Scenario 1: Norovirus at a University Dining Hall",
    "📚 Scenario 2: Measles in an Under-Vaccinated Elementary School",
    "🥘 Scenario 3: Salmonellosis at a Community Church Potluck",
], key="ob_scenario_select")

# Reset step index when scenario changes
if ob_scenario != st.session_state["ob_prev_scenario"]:
    st.session_state["ob1_idx"] = 0
    st.session_state["ob2_idx"] = 0
    st.session_state["ob3_idx"] = 0
    st.session_state["ob_prev_scenario"] = ob_scenario

st.divider()

# ════════════════════════════════════════════════════════════════
# SCENARIO 1: NOROVIRUS
# ════════════════════════════════════════════════════════════════
if ob_scenario == "🍽️ Scenario 1: Norovirus at a University Dining Hall":

    col_brief, col_stats = st.columns([2,1])
    with col_brief:
        st.markdown("""
### 🎯 Your Mission
A university student health center has reported an unusual cluster of gastrointestinal illness among students who ate in the main dining hall last Tuesday evening. Students report vomiting, diarrhea, and nausea starting 18–36 hours after the meal. Your job: identify the vehicle, control the outbreak, and prevent further spread.
        """)
    with col_stats:
        st.markdown("""
<div style="background:#fef2f2;border-radius:8px;padding:14px;font-size:13px;">
<b>📋 Outbreak Brief</b><br><br>
🤒 <b>Cases reported:</b> 47<br>
🏥 <b>Hospitalizations:</b> 3<br>
💀 <b>Deaths:</b> 0<br>
📍 <b>Location:</b> University campus<br>
⏱️ <b>Exposure date:</b> Tuesday dinner<br>
🦠 <b>Suspected agent:</b> Unknown
</div>
        """, unsafe_allow_html=True)

    ob1_step = st.radio("Jump to step:", [
        "Step 1 — Verify the diagnosis & establish the outbreak",
        "Step 2 — Construct a case definition",
        "Step 3 — Epidemic curve & descriptive epidemiology",
        "Step 4 — Generate & test hypotheses (attack rates)",
        "Step 5 — Control measures & resolution",
    ], index=st.session_state.get("ob1_idx", 0), horizontal=False)
    st.divider()

    # ── STEP 1 ──
    if ob1_step == "Step 1 — Verify the diagnosis & establish the outbreak":
        st.subheader("Step 1 — Does an outbreak actually exist?")
        st.markdown("""
The student health center has seen 47 students with vomiting and diarrhea in 48 hours. The usual Tuesday volume is 2–3 GI cases per week.

**Lab results so far:** 6 stool samples submitted. Results pending. Students report symptoms began 18–36 hours after Tuesday dinner.

**Clinical picture:** Sudden onset nausea, vomiting (projectile in some), watery diarrhea (non-bloody), low-grade fever, muscle aches. Symptoms resolving in 24–48 hours.
        """)
        st.info("💡 **Step 1 of 10:** Prepare for field work + Establish the outbreak exists")

        q1 = st.radio("**Decision 1A:** Based on the information above, does an outbreak exist?", [
            "— Select —",
            "Yes — 47 cases vs. expected 2–3/week clearly exceeds baseline",
            "No — wait for lab results before declaring an outbreak",
            "Maybe — need to interview students first",
        ], key="ob1_q1")

        if q1 == "Yes — 47 cases vs. expected 2–3/week clearly exceeds baseline":
            st.success("""
✅ **Correct.** An outbreak exists when case counts significantly exceed the expected baseline. 47 cases in 48 hours vs. 2–3/week = approximately 16× the baseline rate. You don't need lab confirmation to establish that an outbreak is occurring — epidemiologic evidence is sufficient to begin the investigation.
            """)
            st.markdown("**10-step connection:** Step 2 — *Establish the existence of an outbreak*")

        elif q1 == "No — wait for lab results before declaring an outbreak":
            st.error("""
❌ **Incorrect.** Waiting for lab results before acting is a common error that allows outbreaks to grow. Epidemiologic criteria (cases exceeding expected baseline by time, place, and person) are sufficient to declare and investigate an outbreak. Lab confirmation identifies the agent — it doesn't define whether an outbreak is occurring.
            """)

        elif q1 == "Maybe — need to interview students first":
            st.warning("""
⚠️ **Partially correct.** Interviewing is essential, but you have enough information right now to establish that case counts exceed the baseline. You can declare an outbreak AND begin interviews simultaneously — these are not sequential steps.
            """)

        if q1 != "— Select —":
            st.divider()
            q1b = st.radio("**Decision 1B:** What agent does the clinical picture most suggest?", [
                "— Select —",
                "Staphylococcus aureus toxin (onset 2–6 hours)",
                "Norovirus (onset 12–48 hours, rapid spread, projectile vomiting)",
                "Salmonella (onset 6–72 hours, bloody diarrhea common)",
                "E. coli O157 (onset 1–10 days, bloody diarrhea, HUS risk)",
            ], key="ob1_q1b")

            if q1b == "Norovirus (onset 12–48 hours, rapid spread, projectile vomiting)":
                st.success("""
✅ **Correct.** The 18–36 hour incubation, projectile vomiting, brief duration (24–48h), and high attack rate in a congregate setting are the classic norovirus signature. Staph toxin would present in 2–6 hours. Salmonella typically produces more diarrhea than vomiting. E. coli O157 rarely causes projectile vomiting and has a longer incubation.
                """)
            elif q1b != "— Select —":
                st.error("""
❌ **Incorrect.** Review the incubation periods: Staph toxin = 2–6h (preformed toxin). Norovirus = 12–48h. Salmonella = 6–72h (longer, more diarrhea-predominant). E. coli O157 = 1–10 days (bloody diarrhea, HUS risk). The 18–36h onset + projectile vomiting + brief illness duration = norovirus pattern.
                """)

    # ── STEP 2 ──

        next_step_button(ob1_step, OB1_STEPS, "ob1_idx")

    elif ob1_step == "Step 2 — Construct a case definition":
        st.subheader("Step 2 — Who counts as a case?")
        st.markdown("""
You need a **case definition** before you can count cases, calculate attack rates, or analyze the data. A case definition has four components: **person, place, time, and clinical criteria**.

You currently have:
- Person: Students (and potentially staff) at the university
- Place: Main dining hall, Tuesday dinner service
- Time: Symptoms began between Tuesday evening and Thursday morning
- Clinical: Vomiting and/or diarrhea (3+ loose stools/24h) after eating at the dining hall
        """)
        st.info("💡 **Step 4 of 10:** Construct a working case definition")

        q2a = st.radio("**Decision 2A:** How sensitive should your initial case definition be?", [
            "— Select —",
            "Narrow (confirmed lab-positive only) — precise but will miss most cases",
            "Broad (any GI symptoms after Tuesday dinner) — sensitive, captures more cases early",
            "Moderate (vomiting OR ≥3 loose stools within 72h of Tuesday dinner) — balances sensitivity and specificity",
        ], key="ob1_q2a")

        if q2a == "Moderate (vomiting OR ≥3 loose stools within 72h of Tuesday dinner) — balances sensitivity and specificity":
            st.success("""
✅ **Correct.** Early in an investigation, case definitions should be broad enough to capture cases without being so loose they include unrelated illness. Starting with a moderate definition — vomiting OR ≥3 loose stools within the plausible incubation window — is standard practice. You refine it as more information emerges.
            """)
        elif q2a == "Broad (any GI symptoms after Tuesday dinner) — sensitive, captures more cases early":
            st.warning("""
⚠️ **Acceptable but not ideal.** Being broadly sensitive early is reasonable, but "any GI symptoms" risks including students with pre-existing conditions, mild unrelated illness, or anxiety responses. A minimum symptom threshold (vomiting OR ≥3 loose stools) improves specificity without losing too many true cases.
            """)
        elif q2a == "Narrow (confirmed lab-positive only) — precise but will miss most cases":
            st.error("""
❌ **Incorrect.** Lab-confirmed cases only would capture maybe 5–10% of the true outbreak. Most norovirus cases are never lab-confirmed. Requiring confirmation before counting cases would make your attack rates meaningless and delay control measures by days to weeks.
            """)

        if q2a != "— Select —":
            st.divider()
            st.markdown("#### ✏️ Build Your Case Definition")
            st.markdown("Using the components below, construct the full working case definition:")

            cc_who = st.selectbox("Person:", ["Any person", "Student or staff member", "Student only"], key="ob1_cc1")
            cc_where = st.selectbox("Place:", ["Anywhere on campus", "Who ate in the main dining hall", "Who ate any campus meal"], key="ob1_cc2")
            cc_when = st.selectbox("Time:", ["At any point this semester", "On Tuesday evening (Nov 5)", "Between Nov 4–7"], key="ob1_cc3")
            cc_clinical = st.selectbox("Clinical:", [
                "With any GI complaint",
                "With vomiting OR ≥3 loose stools within 72 hours of the meal",
                "With lab-confirmed norovirus",
            ], key="ob1_cc4")

            if cc_who and cc_where and cc_when and cc_clinical:
                st.info(f"""
**Your case definition:**
"{cc_who} {cc_where} {cc_when} with {cc_clinical.lower().replace('with ', '')}."
                """)
                if "Student or staff" in cc_who and "main dining hall" in cc_where and "Tuesday" in cc_when and "72 hours" in cc_clinical:
                    st.success("✅ This is a strong working case definition — specific enough to be meaningful, sensitive enough to capture cases, time-bounded to the exposure window.")
                elif "lab-confirmed" in cc_clinical:
                    st.error("❌ Lab confirmation requirement will miss most cases and delay your investigation.")
                else:
                    st.info("This definition will work for now. Note your choices — they affect who gets counted as a case.")

    # ── STEP 3 ──

        next_step_button(ob1_step, OB1_STEPS, "ob1_idx")

    elif ob1_step == "Step 3 — Epidemic curve & descriptive epidemiology":
        st.subheader("Step 3 — Describe the outbreak: Person, Place, Time")
        st.markdown("""
You have now interviewed 89 students who ate Tuesday dinner. 47 meet your case definition. Below is what you know about the distribution of cases.
        """)
        st.info("💡 **Step 6 of 10:** Describe the outbreak in terms of person, place, and time")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Cases by time of symptom onset")
            # Time-ordered data: Tuesday dinner 5-8pm, norovirus incubation 18-36h
            # Onset runs Wed 6am through Thu 6am — clean unimodal bell
            onset_labels_ordered = [
                "Wed\n6am", "Wed\n9am", "Wed\n12pm", "Wed\n3pm",
                "Wed\n6pm", "Wed\n9pm", "Thu\n12am", "Thu\n3am", "Thu\n6am"
            ]
            onset_counts_ordered = [1, 4, 9, 13, 11, 6, 2, 1, 0]
            # Render as SVG via components so order is guaranteed
            import streamlit.components.v1 as _ob1_comp
            n_bars = len(onset_labels_ordered)
            max_c = max(onset_counts_ordered)
            cw, ch = 420, 180
            pad_l, pad_b, pad_t, pad_r = 36, 48, 20, 10
            pw = cw - pad_l - pad_r
            ph = ch - pad_b - pad_t
            bw = pw / n_bars - 2
            import math as _m

            # Nice y ticks
            tick_int = 5
            y_max_tick = tick_int * (_m.ceil(max_c / tick_int) + 1)

            bars_svg = ""
            for i, (lbl, cnt) in enumerate(zip(onset_labels_ordered, onset_counts_ordered)):
                bh = (cnt / y_max_tick) * ph if y_max_tick > 0 else 0
                bx = pad_l + i * (pw / n_bars) + 1
                by = pad_t + ph - bh
                bars_svg += f'<rect x="{round(bx,1)}" y="{round(by,1)}" width="{round(bw,1)}" height="{round(bh,1)}" fill="#3b82f6" rx="2"/>'
                # x label (split on \n)
                parts = lbl.split("\n")
                lx = round(bx + bw/2, 1)
                bars_svg += f'<text x="{lx}" y="{ch-28}" font-size="8" fill="#6b7280" text-anchor="middle">{parts[0]}</text>'
                bars_svg += f'<text x="{lx}" y="{ch-18}" font-size="8" fill="#6b7280" text-anchor="middle">{parts[1]}</text>'

            # Y ticks
            yticks_svg = ""
            for v in range(0, y_max_tick + 1, tick_int):
                ty = round(pad_t + ph - (v / y_max_tick) * ph, 1)
                yticks_svg += f'<line x1="{pad_l}" y1="{ty}" x2="{pad_l+pw}" y2="{ty}" stroke="#e5e7eb" stroke-width="1"/>'
                yticks_svg += f'<text x="{pad_l-4}" y="{ty+3}" font-size="8" fill="#9ca3af" text-anchor="end">{v}</text>'

            axes_svg = (
                f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+ph}" stroke="#d1d5db" stroke-width="1.5"/>'
                f'<line x1="{pad_l}" y1="{pad_t+ph}" x2="{pad_l+pw}" y2="{pad_t+ph}" stroke="#d1d5db" stroke-width="1.5"/>'
                f'<text x="14" y="{pad_t+ph//2}" font-size="9" fill="#6b7280" text-anchor="middle" transform="rotate(-90,14,{pad_t+ph//2})">Cases</text>'
            )
            title_svg = f'<text x="{pad_l + pw//2}" y="13" font-size="10" font-weight="bold" fill="#374151" text-anchor="middle">Symptom Onset — Norovirus Outbreak</text>'

            svg_html = f"""<!DOCTYPE html><html><body style="margin:0;padding:0;">
<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" style="font-family:sans-serif;background:#fafafa;border-radius:6px;display:block;">
  {title_svg}{yticks_svg}{bars_svg}{axes_svg}
</svg></body></html>"""
            _ob1_comp.html(svg_html, height=ch + 10, scrolling=False)
            st.caption("Tuesday dinner served 5:00–8:00 PM. X-axis shows time of symptom onset (Wednesday–Thursday).")

        with col2:
            st.markdown("#### 👥 Person characteristics")
            st.markdown("""
| Characteristic | Cases (n=47) | Non-cases (n=42) |
|---|---|---|
| Mean age | 19.8 years | 20.1 years |
| Female | 55% | 52% |
| Freshman | 62% | 58% |
| Ate salad bar | 87% | 41% |
| Ate hot entrée | 71% | 68% |
| Ate dessert bar | 44% | 42% |
| Sat in east section | 61% | 18% |
            """)

        st.divider()
        q3a = st.radio("**Decision 3A:** Based on the epidemic curve, what transmission pattern does this represent?", [
            "— Select —",
            "Propagated (person-to-person) — multiple waves",
            "Point source — single peak, all cases within one incubation period range",
            "Endemic — stable background rate",
            "Mixed — initial point source with secondary spread",
        ], key="ob1_q3a")

        if q3a == "Point source — single peak, all cases within one incubation period range":
            st.success("""
✅ **Correct.** The curve shows a single unimodal peak — cases rise from Wednesday morning, peak Wednesday afternoon, and decline through Thursday. All cases fall within an ~30-hour window (6am Wed to 6am Thu), consistent with a single common exposure at Tuesday dinner 18–36 hours earlier. This is a classic point-source epidemic curve. No secondary wave has appeared yet, suggesting person-to-person spread has not started.
            """)

        elif q3a == "Propagated (person-to-person) — multiple waves":
            st.error("❌ A propagated curve would show multiple waves separated by one incubation period. This curve has one peak — consistent with a single common exposure.")
        elif q3a != "— Select —":
            st.error("❌ The single sharp peak rising and falling within 24 hours, with all cases tracing to a single meal, is a classic point-source pattern.")

        if q3a != "— Select —":
            st.divider()
            st.markdown("""
> **Note before you answer:** Look carefully at both the gaps *and* the type of variable. The east seating section gap (61% vs. 18%) is actually larger than the salad bar gap (87% vs. 41%). Think about *why* one makes more epidemiologic sense as a vehicle than the other.
            """)
            q3b = st.radio("**Decision 3B:** What does the descriptive data suggest as the most likely vehicle?", [
                "— Select —",
                "Hot entrée — 71% of cases ate it",
                "Salad bar — 87% of cases ate it vs. only 41% of non-cases",
                "Dessert bar — similar rates in cases and non-cases",
                "East seating section — cases concentrated there (61% vs. 18%)",
            ], key="ob1_q3b")
            if q3b == "Salad bar — 87% of cases ate it vs. only 41% of non-cases":
                st.success("""
✅ **Correct.** The salad bar is the right hypothesis — and it's worth understanding *why*, because the east section gap is actually larger (43 points vs. 46 points for the salad bar).

**The critical distinction is biological plausibility and causal logic:**
- **Salad bar** is a *food vehicle* — it can be directly contaminated and ingested. This is a biologically plausible route of transmission for norovirus. The difference in exposure rates between cases and non-cases is large and epidemiologically meaningful.
- **East seating section** is a *place*, not a vehicle. Eating in the east section doesn't cause illness — it's almost certainly a confounder or proxy. The most likely explanation: the salad bar was located near or in the east section, so students who sat there were also more likely to eat from it. The seating section correlates with the exposure but is not the cause.

**The lesson:** When both a food item and a place show large gaps, ask whether the place association is explained by differential access to the food. Always prefer the biologically plausible vehicle over a geographical correlate. You'll confirm this with attack rate calculations in Step 4.
                """)
            elif q3b == "East seating section — cases concentrated there (61% vs. 18%)":
                st.warning("""
⚠️ **Good observation, but not the vehicle.** You correctly noticed that the east section gap (61% vs. 18%) is the largest in the table — that's careful reading. But a seating section is a *place*, not a food vehicle. Place cannot directly transmit norovirus.

**The better interpretation:** The east section concentration is almost certainly a proxy for salad bar exposure — the salad bar was likely positioned near or in the east section, so students who sat there disproportionately ate from it. In epi terms, seating section is a *confounder* or *surrogate marker* of the actual exposure (salad bar), not the cause.

**The rule:** When you see a strong association with a place, ask whether the place correlates with a food exposure. Always prioritize the biologically plausible food vehicle over a geographical correlate. The attack rate analysis in Step 4 will test the food hypothesis directly.
                """)
            elif q3b == "Hot entrée — 71% of cases ate it":
                st.error("❌ 71% of cases AND 68% of non-cases ate the hot entrée — almost identical rates, meaning no meaningful difference in exposure. When cases and non-cases ate something at nearly the same rate, that item is unlikely to be the vehicle.")
            elif q3b == "Dessert bar — similar rates in cases and non-cases":
                st.error("❌ The dessert bar shows 44% vs. 42% — nearly identical rates. No association with illness. The vehicle will show a large gap between cases and non-cases.")


    # ── STEP 4 ──

        next_step_button(ob1_step, OB1_STEPS, "ob1_idx")

    elif ob1_step == "Step 4 — Generate & test hypotheses (attack rates)":
        st.subheader("Step 4 — Calculate attack rates and test your hypothesis")
        st.markdown("""
You have completed interviews with all 89 students who ate Tuesday dinner. Now you'll calculate food-specific attack rates and risk ratios to identify the vehicle.
        """)
        st.info("💡 **Steps 7–8 of 10:** Develop hypotheses → Test hypotheses analytically")

        st.markdown("#### 🧮 Interactive Attack Rate Calculator")
        st.markdown("""
For each food item, calculate:
- **Attack rate (exposed)** = sick among those who ate ÷ total who ate × 100
- **Attack rate (unexposed)** = sick among those who didn't eat ÷ total who didn't eat × 100
- **Risk Ratio (RR)** = AR exposed ÷ AR unexposed
        """)

        food_data = {
            "Salad bar (mixed greens)": {"ate_sick": 41, "ate_well": 6, "notate_sick": 6, "notate_well": 36},
            "Caesar salad dressing": {"ate_sick": 38, "ate_well": 5, "notate_sick": 9, "notate_well": 37},
            "Hot entrée (pasta)": {"ate_sick": 33, "ate_well": 30, "notate_sick": 14, "notate_well": 12},
            "Rolls/bread": {"ate_sick": 28, "ate_well": 25, "notate_sick": 19, "notate_well": 17},
            "Soft-serve ice cream": {"ate_sick": 20, "ate_well": 19, "notate_sick": 27, "notate_well": 23},
        }

        results = []
        for food, d in food_data.items():
            ate_total = d["ate_sick"] + d["ate_well"]
            notate_total = d["notate_sick"] + d["notate_well"]
            ar_exp = round(d["ate_sick"] / ate_total * 100, 1) if ate_total > 0 else 0
            ar_unexp = round(d["notate_sick"] / notate_total * 100, 1) if notate_total > 0 else 0
            rr = round(ar_exp / ar_unexp, 2) if ar_unexp > 0 else float("inf")
            results.append({
                "Food item": food,
                "Ate (sick/total)": f"{d['ate_sick']}/{ate_total}",
                "AR exposed (%)": ar_exp,
                "Did not eat (sick/total)": f"{d['notate_sick']}/{notate_total}",
                "AR unexposed (%)": ar_unexp,
                "RR": rr
            })

        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### 🔍 Analyze the table — work through these before drawing conclusions")
        st.markdown("*Answer each question in order. Each one builds on the last.*")

        # ── ANALYSIS Q1: Null RR ──
        aq1 = st.radio(
            "**Analysis 1:** What RR value would indicate that a food item has NO association with illness?",
            ["— Select —", "RR = 0", "RR = 1.0", "RR = 0.5", "RR > 2"],
            key="ob1_aq1"
        )
        if aq1 == "RR = 1.0":
            st.success("✅ Correct. RR = 1.0 means the attack rate is identical in those who ate vs. those who didn't — eating that food conveys no additional risk. Look at rolls/bread (RR = 1.0) and soft-serve ice cream (RR = 0.95) — near-null RRs, no association.")
        elif aq1 != "— Select —":
            st.error("❌ RR = 1.0 is the null value — it means the attack rate in exposed equals the attack rate in unexposed. RR > 1 means increased risk; RR < 1 means decreased risk; RR = 1 means no difference.")

        if aq1 == "RR = 1.0":
            st.divider()
            # ── ANALYSIS Q2: Why AR unexposed matters ──
            aq2 = st.radio(
                "**Analysis 2:** Hot entrée (pasta) has AR exposed = 52.4% — that seems high. Why is it NOT a strong vehicle candidate?",
                ["— Select —",
                 "Because only 63 students ate it",
                 "Because AR unexposed is 53.8% — nearly identical — so eating it made no difference",
                 "Because pasta can't carry norovirus",
                 "Because the RR should be calculated differently for hot foods"],
                key="ob1_aq2"
            )
            if aq2 == "Because AR unexposed is 53.8% — nearly identical — so eating it made no difference":
                st.success("""
✅ Exactly right. This is the single most important concept in foodborne outbreak analysis: **a high AR exposed means nothing without a low AR unexposed.**

Hot entrée: 52.4% of those who ate it got sick. But 53.8% of those who *didn't* eat it also got sick. RR = 0.97 — essentially 1. Whether you ate the pasta or not made no difference to your risk.

This happens when a food is just popular — many people eat it, so many sick people ate it, but many well people did too. Absolute counts mislead; the ratio is what matters.
                """)
            elif aq2 != "— Select —":
                st.error("❌ The issue is the AR unexposed — what happened to people who DIDN'T eat it. If the unexposed get sick at the same rate as the exposed, eating it made no difference.")

            if aq2 == "Because AR unexposed is 53.8% — nearly identical — so eating it made no difference":
                st.divider()
                # ── ANALYSIS Q3: Rank the two candidates ──
                aq3 = st.radio(
                    "**Analysis 3:** Two items show a large gap between AR exposed and AR unexposed: salad bar (mixed greens) and Caesar dressing. Which has the stronger signal and why?",
                    ["— Select —",
                     "Salad bar — more people ate it (47 vs. 43), so the sample is larger",
                     "Caesar dressing — AR exposed 88.4% vs. AR unexposed 19.6%, RR 4.51 vs. salad bar RR 6.1. Wait — salad bar has the higher RR",
                     "Caesar dressing — slightly lower AR exposed but far lower AR unexposed than salad bar (19.6% vs. 14.3%), giving RR 4.51 vs. 6.1. Salad bar actually has the higher RR",
                     "They are identical — both are strong candidates and you cannot distinguish them"],
                    key="ob1_aq3"
                )
                if aq3 == "Caesar dressing — slightly lower AR exposed but far lower AR unexposed than salad bar (19.6% vs. 14.3%), giving RR 4.51 vs. 6.1. Salad bar actually has the higher RR":
                    st.success("""
✅ Sharp reading — the salad bar actually has the higher RR (6.1 vs. 4.51). Both are strong signals. So why do investigators ultimately point to the dressing rather than the greens?

This is where **biological plausibility and ingredient overlap** enter the analysis: nearly every student who took mixed greens also added Caesar dressing, but some students took dressing alone (on other items or as a dip). The dressing is the more *specific* item — it narrows the hypothesis. Caesar dressing made with raw egg is a well-established norovirus vehicle when handled by an ill food worker.

**The method:** Use RR to identify candidates, then use ingredient overlap and biological plausibility to narrow to the specific vehicle. You'll confirm in Step 5 when the environmental swabs come back.
                    """)
                elif aq3 == "Caesar dressing — AR exposed 88.4% vs. AR unexposed 19.6%, RR 4.51 vs. salad bar RR 6.1. Wait — salad bar has the higher RR":
                    st.success("""
✅ You caught the correction mid-answer — that's exactly right. Salad bar RR = 6.1, Caesar dressing RR = 4.51. The greens have the stronger statistical signal.

The reason investigators focus on the dressing anyway comes down to ingredient specificity and biological plausibility — Caesar dressing made with raw egg, handled by an ill worker, is the more actionable specific vehicle. Greens and dressing were nearly always consumed together, making statistical separation difficult.

This illustrates an important limitation of attack rate analysis: when two items are almost always eaten together, it can be hard to separate their individual contributions statistically.
                    """)
                elif aq3 != "— Select —":
                    st.error("❌ Look carefully at both RRs in the table. Compare salad bar greens (RR = 6.1) vs. Caesar dressing (RR = 4.51). Which is numerically higher? Then think about why investigators might still focus on the dressing despite that.")

                if aq3 != "— Select —" and aq3 != "— Select —":
                    st.divider()
                    # ── ANALYSIS Q4: What makes a strong vehicle overall ──
                    aq4 = st.radio(
                        "**Analysis 4:** Using the table, which of the following best describes the pattern of a STRONG vehicle vs. a NON-vehicle?",
                        ["— Select —",
                         "Strong vehicle: high AR exposed AND high AR unexposed / Non-vehicle: low AR in both",
                         "Strong vehicle: high AR exposed AND low AR unexposed (RR >> 1) / Non-vehicle: similar AR in both groups (RR ≈ 1)",
                         "Strong vehicle: high absolute case count / Non-vehicle: low absolute case count",
                         "Strong vehicle: item eaten by more than 50% of attendees / Non-vehicle: eaten by fewer"],
                        key="ob1_aq4"
                    )
                    if aq4 == "Strong vehicle: high AR exposed AND low AR unexposed (RR >> 1) / Non-vehicle: similar AR in both groups (RR ≈ 1)":
                        st.success("""
✅ This is the core rule of foodborne outbreak analysis — and now you can see it clearly in the table:

| Item | AR exposed | AR unexposed | RR | Verdict |
|---|---|---|---|---|
| Salad bar | 87.2% | 14.3% | **6.1** | ✅ Strong vehicle |
| Caesar dressing | 88.4% | 19.6% | **4.51** | ✅ Strong vehicle |
| Hot entrée | 52.4% | 53.8% | **0.97** | ❌ Not a vehicle |
| Rolls/bread | 52.8% | 52.8% | **1.0** | ❌ Not a vehicle |
| Soft-serve | 51.3% | 54.0% | **0.95** | ❌ Not a vehicle |

The vehicles are not the most *popular* foods — they're the foods where eating them made a *difference*. Now identify the most likely specific vehicle below.
                        """)
                    elif aq4 != "— Select —":
                        st.error("❌ Absolute counts and overall popularity are misleading. The defining pattern of a vehicle: people who ate it got sick at a much higher rate than people who didn't eat it. High AR exposed + low AR unexposed = high RR = strong vehicle signal.")

        st.divider()
        q4a = st.radio("**Decision 4A:** Based on your analysis, which food item is the most likely specific vehicle?", [
            "— Select —",
            "Hot entrée (pasta) — most students ate it",
            "Caesar salad dressing — strong RR, biologically plausible, more specific than greens",
            "Salad bar (mixed greens) — highest RR in the table",
            "Soft-serve ice cream — high absolute case count",
        ], key="ob1_q4a")

        if q4a == "Caesar salad dressing — strong RR, biologically plausible, more specific than greens":
            st.success("""
✅ **Correct.** Caesar dressing is the most actionable specific vehicle. Both dressing and greens show strong signals — but the dressing is the more specific item (raw egg, handled by an ill food worker) and is the more testable hypothesis for environmental sampling and food handler investigation. Investigators narrow from a food category (salad bar) to the specific contaminated item (dressing) — this is how outbreak reports cite vehicles.
            """)
        elif q4a == "Salad bar (mixed greens) — highest RR in the table":
            st.warning("""
⚠️ **Statistically defensible, but not the most specific answer.** The salad bar greens do have the highest RR (6.1). However, greens and Caesar dressing were consumed together by nearly everyone who visited the salad bar. The dressing is the more specific vehicle — it narrows the hypothesis to a single contaminated item that has a clear biological mechanism (raw egg + ill food handler). In practice, investigators report the most specific vehicle they can identify.
            """)
        elif q4a != "— Select —":
            st.error("""
❌ Work through the analysis questions above if you haven't already. The key: identify items with high AR exposed AND low AR unexposed (high RR). High absolute case counts or overall popularity are not the right criteria.
            """)

        if q4a != "— Select —":
            st.divider()
            st.markdown("#### 🧮 Calculate the overall attack rate for this outbreak")
            st.markdown("The outbreak brief told you: **47 cases** among **89 students** who ate Tuesday dinner.")
            col_ar1, col_ar2 = st.columns(2)
            with col_ar1:
                total_sick_input = st.number_input("Total sick (cases):", min_value=0, max_value=200, value=0, key="ob1_ar1")
            with col_ar2:
                total_exposed_input = st.number_input("Total who ate Tuesday dinner:", min_value=0, max_value=500, value=0, key="ob1_ar2")

            if total_exposed_input > 0 and total_sick_input > 0:
                overall_ar = round(total_sick_input / total_exposed_input * 100, 1)
                st.metric("Overall attack rate", f"{overall_ar}%")

                correct_sick, correct_total = 47, 89
                correct_ar = round(correct_sick / correct_total * 100, 1)

                if total_sick_input == correct_sick and total_exposed_input == correct_total:
                    st.success(f"✅ **Correct — {total_sick_input}/{total_exposed_input} = {overall_ar}%.** Just over half of all diners became ill. An attack rate above 50% is unusually high for a foodborne outbreak and is consistent with a widely consumed contaminated item (like a salad bar item served to most attendees).")
                elif total_sick_input != correct_sick and total_exposed_input == correct_total:
                    st.error(f"❌ The denominator (89 diners) is correct, but check the numerator. The case count from the outbreak brief is {correct_sick}, not {total_sick_input}. AR = {correct_sick}/{correct_total} = {correct_ar}%.")
                elif total_sick_input == correct_sick and total_exposed_input != correct_total:
                    st.error(f"❌ The case count ({correct_sick}) is correct, but check the denominator. The attack rate uses all people who were exposed to the meal — all {correct_total} students who ate Tuesday dinner, not just those who got sick. AR = {correct_sick}/{correct_total} = {correct_ar}%.")
                elif total_exposed_input < total_sick_input:
                    st.error("❌ The denominator (total exposed) cannot be smaller than the numerator (total sick). The denominator is everyone who ate the meal — sick AND well.")
                else:
                    st.warning(f"⚠️ Not quite. From the scenario: {correct_sick} cases among {correct_total} students who ate Tuesday dinner. AR = {correct_sick}/{correct_total} = **{correct_ar}%**. Check which numbers you used.")
            elif total_sick_input > 0 or total_exposed_input > 0:
                st.info("Enter both values to calculate the attack rate.")


    # ── STEP 5 ──

        next_step_button(ob1_step, OB1_STEPS, "ob1_idx")

    elif ob1_step == "Step 5 — Control measures & resolution":
        st.subheader("Step 5 — Implement control measures")
        st.info("💡 **Steps 9–10 of 10:** Implement control measures → Communicate findings")

        st.markdown("""
**Lab results are in:** Norovirus GII.4 detected in 5 of 6 stool samples. Environmental swabs positive on the salad bar sneeze guard and Caesar dressing pump handle.

**Food handler interview reveals:** One dining hall employee worked a full shift Tuesday despite vomiting that morning. This employee prepared and handled the Caesar dressing.

**Current situation:** 47 cases, 3 hospitalizations (rehydration only, all recovered). No deaths. Two new cases reported Thursday from students who did not eat Tuesday but had contact with ill roommates.
        """)

        q5a = st.radio("**Decision 5A:** The two new Thursday cases (contact with ill roommates) indicate what?", [
            "— Select —",
            "The outbreak is over — these are unrelated",
            "Person-to-person transmission has begun — secondary spread",
            "The Caesar dressing is still being served — still point-source exposure",
        ], key="ob1_q5a")

        if q5a == "Person-to-person transmission has begun — secondary spread":
            st.success("""
✅ **Correct.** Norovirus is highly contagious person-to-person (fecal-oral, vomit aerosol). These two cases represent a secondary wave beginning. The outbreak has shifted from pure point-source to mixed. Control measures must now address both the food source and person-to-person transmission.
            """)
        elif q5a != "— Select —":
            st.error("❌ Two cases in direct contact with ill students, without dining hall exposure, indicates person-to-person transmission has begun. This is a critical inflection point requiring expanded control measures.")

        if q5a != "— Select —":
            st.divider()
            st.markdown("#### Select ALL appropriate control measures (check all that apply):")
            cm1 = st.checkbox("Remove Caesar dressing from service immediately", key="ob1_cm1")
            cm2 = st.checkbox("Close the entire university", key="ob1_cm2")
            cm3 = st.checkbox("Exclude ill food handlers from work until 48h symptom-free", key="ob1_cm3")
            cm4 = st.checkbox("Reinforce hand hygiene among all dining staff", key="ob1_cm4")
            cm5 = st.checkbox("Issue guidance to ill students on isolation and hygiene", key="ob1_cm5")
            cm6 = st.checkbox("Enhance cleaning and disinfection of dining surfaces", key="ob1_cm6")
            cm7 = st.checkbox("Test all food items in the dining hall", key="ob1_cm7")

            if st.button("Submit control measures", key="ob1_cm_submit"):
                score = sum([cm1, cm3, cm4, cm5, cm6])
                if cm2:
                    st.error("❌ Closing the university is not proportionate and would not be recommended at this case count. Targeted interventions are appropriate.")
                if not cm1:
                    st.error("❌ Removing the identified vehicle (Caesar dressing) is the single most important immediate step.")
                if score >= 4 and cm1 and not cm2:
                    st.success(f"""
✅ **Well done.** You selected {score+1}/5 appropriate measures. The key actions are: (1) remove the vehicle, (2) exclude ill food handlers, (3) reinforce hand hygiene, (4) isolate ill students and advise hygiene, (5) enhance disinfection. Testing all food items is low-yield at this stage — focus resources on the identified vehicle and secondary spread.
                    """)
                elif cm1:
                    st.info(f"You selected {score+1} measures. Consider also: {'excluding ill food handlers, ' if not cm3 else ''}{'reinforcing hand hygiene, ' if not cm4 else ''}{'guidance to ill students, ' if not cm5 else ''}{'enhanced disinfection' if not cm6 else ''}")

        st.divider()
        with st.expander("📋 Resolution & What You Applied"):
            st.markdown("""
**Outcome:** The Caesar dressing was prepared using raw shell eggs contaminated with norovirus from the ill food handler. 47 primary cases. 8 secondary cases in the following 4 days. All recovered. No deaths.

**The 10 steps you applied:**
| Step | What you did |
|---|---|
| 1. Prepare | Reviewed clinical picture, incubation period, agent characteristics |
| 2. Establish outbreak | Compared 47 cases to baseline of 2–3/week → clear excess |
| 3. Verify diagnosis | Clinical criteria consistent with norovirus; lab confirmation |
| 4. Case definition | Person (student/staff) + place (dining hall) + time (72h of Tuesday dinner) + clinical (vomiting or ≥3 stools) |
| 5. Case finding | Interviewed all 89 Tuesday diners |
| 6. Descriptive epi | Epidemic curve (point source), person characteristics, place (salad bar cluster) |
| 7. Hypothesis | Caesar dressing as vehicle based on differential exposure rates |
| 8. Test hypothesis | Attack rates and RR confirmed Caesar dressing (RR > 5) |
| 9. Control | Removed vehicle, excluded ill worker, hygiene reinforcement, isolation guidance |
| 10. Communicate | Report to student health, dining services, and state health department |
            """)

            with st.expander("🦠 What is norovirus?"):
                st.markdown("""
**Norovirus** is the leading cause of foodborne illness in the United States, responsible for approximately 19–21 million illnesses annually. Key features:
- **Transmission:** Fecal-oral (food, water, contaminated surfaces), person-to-person, vomit aerosol
- **Incubation:** 12–48 hours (typically 24–36h)
- **Symptoms:** Projectile vomiting, watery non-bloody diarrhea, nausea, low-grade fever, myalgias
- **Duration:** 1–3 days (self-limited)
- **Infectious dose:** Extremely low — as few as 18 viral particles can cause infection
- **Environmental stability:** Survives on surfaces for days; resistant to many standard disinfectants (requires bleach-based products)
- **High-risk settings:** Cruise ships, nursing homes, hospitals, schools, catered events
- **Key control:** Exclude ill food handlers for 48h after symptom resolution; hand hygiene (soap and water — alcohol gel less effective); bleach disinfection of surfaces
                """)


        next_step_button(ob1_step, OB1_STEPS, "ob1_idx")

# ════════════════════════════════════════════════════════════════
# SCENARIO 2: MEASLES
# ════════════════════════════════════════════════════════════════
elif ob_scenario == "📚 Scenario 2: Measles in an Under-Vaccinated Elementary School":

    col_brief, col_stats = st.columns([2,1])
    with col_brief:
        st.markdown("""
### 🎯 Your Mission
A parent calls the county health department: their 7-year-old is home from school with a rash and high fever. The child returned from an international trip 12 days ago. Over the next 3 days, 6 more children at the same school report similar symptoms. The school has a 72% MMR vaccination rate. Your job: confirm the diagnosis, stop transmission, and determine whether the outbreak could have been prevented.
        """)
    with col_stats:
        st.markdown("""
<div style="background:#fef3c7;border-radius:8px;padding:14px;font-size:13px;">
<b>📋 Outbreak Brief</b><br><br>
🤒 <b>Cases reported:</b> 7 (growing)<br>
🏥 <b>Hospitalizations:</b> 1<br>
💀 <b>Deaths:</b> 0<br>
📍 <b>Location:</b> Elementary school<br>
🧒 <b>Population:</b> 450 students<br>
💉 <b>MMR coverage:</b> 72%
</div>
        """, unsafe_allow_html=True)

    ob2_step = st.radio("Jump to step:", [
        "Step 1 — Verify diagnosis & chain of infection",
        "Step 2 — Herd immunity & the math behind the outbreak",
        "Step 3 — Contact tracing & case finding",
        "Step 4 — Control measures",
        "Step 5 — Could this have been prevented?",
    ], index=st.session_state.get("ob2_idx", 0), horizontal=False)
    st.divider()

    if ob2_step == "Step 1 — Verify diagnosis & chain of infection":
        st.subheader("Step 1 — Confirm measles and trace the chain")
        st.markdown("""
**Index case (Patient Zero):** 7-year-old, unvaccinated, returned from international travel 12 days ago. Presents with: 3-day prodrome of high fever (104°F), cough, coryza (runny nose), conjunctivitis. Then: classic maculopapular rash starting at hairline, spreading downward. Koplik spots (white spots on buccal mucosa) noted by clinician.

**Lab:** IgM measles antibody positive (state lab). PCR confirmatory test sent to CDC.

**Exposure timeline:** Returned from trip → attended school for 3 days before rash appeared (highly infectious during prodrome).
        """)

        q1 = st.radio("**Decision 1A:** How long was the index case potentially infectious at school before diagnosis?", [
            "— Select —",
            "0 days — measles is only infectious after rash appears",
            "3 days — infectious during the prodrome (4 days before to 4 days after rash onset)",
            "Only on the day of rash — maximum infectiousness",
            "10 days — for the full incubation period",
        ], key="ob2_q1a")

        if q1 == "3 days — infectious during the prodrome (4 days before to 4 days after rash onset)":
            st.success("""
✅ **Correct.** Measles is infectious from 4 days before to 4 days after rash onset — the prodrome period when the child appears to have "just a cold" is the most dangerous period for transmission. The index case attended school for 3 days during this window, potentially exposing every susceptible student they encountered.

This is why outbreak control is so difficult: by the time measles is diagnosed (rash + Koplik spots), the infectious period is already partially over and secondary cases are incubating.
            """)
        elif q1 != "— Select —":
            st.error("❌ Measles is infectious from 4 days BEFORE rash onset through 4 days AFTER — the prodrome cough/fever/runny nose phase is peak infectiousness. Waiting for the rash to diagnose means exposure has already occurred.")

        if q1 != "— Select —":
            st.divider()
            st.markdown("""
**Chain of infection — measles:**
| Link | Details |
|---|---|
| **Agent** | Measles virus (Paramyxovirus, RNA) |
| **Reservoir** | Humans only (no animal reservoir) |
| **Portal of exit** | Respiratory tract (cough, sneeze) |
| **Transmission** | Airborne — virus survives in air for up to 2 hours after infectious person leaves the room |
| **Portal of entry** | Respiratory tract |
| **Susceptible host** | Unvaccinated or immunocompromised |
            """)
            st.warning("""
⚠️ **Airborne transmission critical point:** Measles is one of the most contagious pathogens known. Unlike respiratory droplets that fall within 1 meter, measles virus remains suspended in the air for up to 2 hours. A susceptible person entering the same room AFTER the index case has left can still be infected. This makes standard droplet precautions insufficient.
            """)


        next_step_button(ob2_step, OB2_STEPS, "ob2_idx")

    elif ob2_step == "Step 2 — Herd immunity & the math behind the outbreak":
        st.subheader("Step 2 — Why did this outbreak happen? The herd immunity calculation")

        st.markdown("""
The school has 72% MMR vaccination rate. Let's calculate whether this is enough to prevent an outbreak using the herd immunity threshold.
        """)

        st.markdown("#### 🧮 Calculate the herd immunity threshold")
        r0_measles = st.slider("R₀ for measles in this school setting:", 10, 18, 15, key="ob2_r0")
        hit = round((1 - 1/r0_measles) * 100, 1)
        current_immunity = 72
        effective_r = round(r0_measles * (1 - current_immunity/100), 2)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Herd Immunity Threshold", f"{hit}%")
        with col2:
            st.metric("Current MMR coverage", "72%", delta=f"{round(72-hit,1)}% below threshold")
        with col3:
            st.metric("Effective R (Rₑ)", effective_r, delta="epidemic growing" if effective_r > 1 else "epidemic declining")

        if effective_r > 1:
            st.error(f"""
**Why the outbreak is happening:** With R₀ = {r0_measles} and only 72% immune, Rₑ = {effective_r}. Each case is generating {effective_r} new cases on average. The school is {round(hit-72,1)} percentage points below the herd immunity threshold — a significant immunity gap that allows the virus to spread efficiently.
            """)

        st.divider()
        q2a = st.radio("**Decision 2A:** The school has 450 students. How many susceptible students are there?", [
            "— Select —",
            "28 students (only those with documented vaccine exemptions)",
            f"126 students (28% of 450 = those not vaccinated)",
            "72 students (the number not vaccinated this year)",
            "It depends on prior infection history — vaccine records alone are insufficient",
        ], key="ob2_q2a")

        if q2a == "It depends on prior infection history — vaccine records alone are insufficient":
            st.success("""
✅ **Correct — and the most sophisticated answer.** Susceptibility = unvaccinated + vaccine failures (2–5% of vaccinated) + immunocompromised vaccinated individuals + those with unknown status. 28% unvaccinated = at minimum 126 susceptibles, but true susceptibility is higher when you account for primary vaccine failure (~2–5% of MMR recipients). This is why the effective R can remain >1 even with seemingly high coverage.
            """)
        elif q2a == "126 students (28% of 450 = those not vaccinated)":
            st.warning("""
⚠️ **Partially correct.** 28% × 450 = 126 unvaccinated students is the minimum count of susceptibles. But some vaccinated students have primary vaccine failure (2–5%), so the true susceptible pool is larger. Additionally, students with unknown or undocumented status add uncertainty.
            """)
        elif q2a != "— Select —":
            st.error("❌ Susceptibility is not simply the number who didn't get vaccinated this year. It includes those with no prior vaccination, vaccine failures, undocumented status, and immunocompromised individuals regardless of vaccination.")

        if q2a != "— Select —":
            st.divider()
            st.markdown("#### 📈 Epidemic curve projection")
            st.markdown(f"""
With Rₑ = **{effective_r}**, project the wave pattern:
- **Generation 1** (index case): 1 case
- **Generation 2** (~10 days later): ~{round(effective_r)} cases
- **Generation 3** (~20 days later): ~{round(effective_r**2)} cases
- **Generation 4** (~30 days later): ~{round(effective_r**3)} cases

This exponential growth pattern continues until susceptibles are exhausted or vaccination coverage increases above the HIT of {hit}%.
            """)


        next_step_button(ob2_step, OB2_STEPS, "ob2_idx")

    elif ob2_step == "Step 3 — Contact tracing & case finding":
        st.subheader("Step 3 — Who was exposed? Contact tracing at scale")
        st.markdown("""
You now have 7 confirmed cases. The index case attended school for 3 days during the infectious period. Your team needs to identify all contacts and determine their immune status.
        """)
        st.info("💡 **Step 5 of 10:** Find cases systematically — active case finding")

        st.markdown("""
**Exposure settings to investigate:**
1. **Classrooms** — same class as index case (25 students + teacher)
2. **School bus** — 42 students rode the same bus
3. **Cafeteria** — shared lunch period with ~180 students
4. **Gymnasium** — PE class (30 students) in a poorly ventilated space
5. **Hallways and common areas** — indirect exposure, hard to quantify
        """)

        q3a = st.radio("**Decision 3A:** For each exposure setting, should you classify contacts as high, medium, or low risk?", [
            "— Select —",
            "All contacts are equal — anyone in the school is at equal risk",
            "Duration and proximity determine risk — classroom and gym (prolonged, enclosed) = highest",
            "Only direct face-to-face contact counts — hallway contacts are not at risk",
        ], key="ob2_q3a")

        if q3a == "Duration and proximity determine risk — classroom and gym (prolonged, enclosed) = highest":
            st.success("""
✅ **Correct.** For airborne transmission, risk is proportional to duration of exposure and ventilation quality. Prolonged shared air space (classroom, gym) = highest risk. Cafeteria (shorter exposure, more people, better ventilation) = moderate. Hallways (brief exposure) = lower risk, but not zero since measles can survive 2 hours in air.
            """)
        elif q3a != "— Select —":
            st.error("❌ For airborne pathogens, exposure duration and ventilation are critical determinants of risk. Not all contacts are equal.")

        if q3a != "— Select —":
            st.divider()
            st.markdown("#### 📋 Contact tracing matrix")
            contact_data = pd.DataFrame({
                "Setting": ["Same classroom", "School bus", "Cafeteria (same period)", "Gymnasium (PE)", "General school"],
                "Contacts identified": [25, 42, 180, 30, 173],
                "Vaccination status known": [24, 38, 120, 28, 90],
                "Confirmed vaccinated": [19, 30, 89, 22, 62],
                "Unvaccinated/unknown": [6, 12, 91, 8, 111],
            })
            st.dataframe(contact_data, use_container_width=True, hide_index=True)

            total_unvax = int(contact_data["Unvaccinated/unknown"].sum())
            total_contacts = int(contact_data["Contacts identified"].sum())
            st.metric("Total contacts identified", total_contacts)
            st.metric("Unvaccinated or unknown status", total_unvax,
                      delta="require post-exposure vaccination or exclusion")

            q3b = st.radio("**Decision 3B:** What should happen to unvaccinated contacts?", [
                "— Select —",
                "Nothing unless they develop symptoms",
                "Exclude from school for 21 days OR vaccinate within 72h of exposure",
                "Require quarantine at home until PCR tested",
                "Vaccinate everyone regardless of prior status",
            ], key="ob2_q3b")

            if q3b == "Exclude from school for 21 days OR vaccinate within 72h of exposure":
                st.success("""
✅ **Correct.** This is the standard public health response for unvaccinated measles contacts. MMR given within 72 hours of exposure can prevent or attenuate illness. If vaccination is refused or >72 hours have passed, exclusion from school for 21 days (one incubation period) prevents further exposure. This is a legally authorized public health measure.
                """)
            elif q3b != "— Select —":
                st.error("❌ 'Wait and see' allows further transmission during the incubation period. Exclusion or post-exposure vaccination is the appropriate public health intervention.")


        next_step_button(ob2_step, OB2_STEPS, "ob2_idx")

    elif ob2_step == "Step 4 — Control measures":
        st.subheader("Step 4 — Emergency vaccination and outbreak control")

        st.markdown("""
**Current status:** 12 confirmed cases (Day 10 of outbreak). The outbreak is in its second generation. 3 hospitalizations (pneumonia complication in one immunocompromised child). 228 unvaccinated or unknown-status contacts identified.

**Available interventions:**
1. Emergency vaccination clinic at school (MMR)
2. School closure (partial or full)
3. Exclusion of unvaccinated students
4. Enhanced surveillance for new cases
5. Healthcare provider alert (notify ER, clinics to report suspect cases)
        """)

        st.markdown("#### 🧮 Calculate vaccination coverage needed")
        current_cov = st.slider("Current school MMR coverage:", 60, 95, 72, key="ob2_vax_slider")
        r0_val = 15
        hit_val = round((1 - 1/r0_val) * 100, 1)
        gap = round(hit_val - current_cov, 1)
        students_needed = round((gap/100) * 450)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("HIT for measles (R₀=15)", f"{hit_val}%")
            st.metric("Current coverage", f"{current_cov}%")
        with col2:
            st.metric("Coverage gap", f"{gap}%", delta=f"Need {students_needed} more students vaccinated")
            reff = round(r0_val * (1 - current_cov/100), 2)
            st.metric("Current Rₑ", reff, delta="outbreak growing" if reff > 1 else "outbreak slowing")

        if current_cov >= hit_val:
            st.success(f"✅ At {current_cov}% coverage, Rₑ = {reff} < 1. Herd immunity achieved — outbreak will decline.")
        else:
            st.warning(f"⚠️ At {current_cov}% coverage, Rₑ = {reff} > 1. Outbreak will continue to grow until coverage reaches {hit_val}%.")

        st.divider()
        q4a = st.radio("**Decision 4A:** Should the school be closed?", [
            "— Select —",
            "Yes, immediately close for 2 weeks",
            "No — targeted exclusion of unvaccinated students is more proportionate and maintains education",
            "Only close if cases exceed 25",
        ], key="ob2_q4a")

        if q4a == "No — targeted exclusion of unvaccinated students is more proportionate and maintains education":
            st.success("""
✅ **Correct.** Excluding only unvaccinated students (who are at risk and can transmit) allows vaccinated students to continue education without interruption. Full school closure is a higher-level intervention reserved for when targeted exclusion fails or when a large proportion of students are susceptible. Proportionality is a core principle of public health intervention.
            """)
        elif q4a == "Yes, immediately close for 2 weeks":
            st.warning("""
⚠️ **Premature.** School closure is a high-impact intervention that disrupts education for vaccinated students who are not at risk. Start with targeted exclusion of unvaccinated contacts. Full closure may become necessary if the outbreak grows and targeted exclusion proves insufficient.
            """)
        elif q4a != "— Select —":
            st.error("❌ Waiting for a specific case count threshold before acting allows exponential growth to occur. Act early with targeted measures.")


        next_step_button(ob2_step, OB2_STEPS, "ob2_idx")

    elif ob2_step == "Step 5 — Could this have been prevented?":
        st.subheader("Step 5 — Prevention and policy implications")
        st.markdown("""
The outbreak is now controlled after an emergency vaccination clinic raised coverage to 95%. Final case count: 23 cases, 4 hospitalizations, 0 deaths. 228 unvaccinated students excluded for varying periods.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Final outbreak summary")
            st.markdown("""
- **Total cases:** 23
- **Hospitalizations:** 4 (pneumonia x2, encephalitis x1, otitis media x1)
- **Deaths:** 0
- **School days missed by unvaccinated students:** 2,850 total (228 students × avg 12.5 days)
- **Cost of emergency response:** Estimated $280,000 (staff, vaccines, investigation)
            """)
        with col2:
            st.markdown("#### What would have prevented this")
            st.markdown("""
- **Vaccination coverage at 93%+:** Would have kept Rₑ < 1; one infectious case would not have sparked an outbreak
- **School vaccination requirement enforcement:** 28% unvaccinated is far above the level compatible with herd immunity
- **Pre-travel health consultation:** Index family could have been counseled on measles risk in destination country
- **Clinician recognition:** Earlier diagnosis (Koplik spots, prodrome) would have shortened exposure window
            """)

        st.divider()
        q5a = st.radio("**Decision 5A:** What policy change would most prevent future outbreaks?", [
            "— Select —",
            "Require vaccination of all staff but allow student exemptions to continue",
            "Enforce existing vaccination requirements and restrict non-medical exemptions",
            "Provide education campaigns — choice is sufficient",
            "Conduct annual screenings but take no policy action",
        ], key="ob2_q5a")

        if q5a == "Enforce existing vaccination requirements and restrict non-medical exemptions":
            st.success("""
✅ **Correct.** Mathematical modeling and real-world data both show that states with easier non-medical (philosophical/religious) exemptions have higher rates of vaccine-preventable disease outbreaks. Enforcement of existing requirements and restriction of non-medical exemptions is the most evidence-based policy intervention to maintain herd immunity.
            """)
        elif q5a != "— Select —":
            st.error("❌ Voluntary measures have consistently proven insufficient to maintain measles herd immunity (93%+). Policy enforcement is the most effective tool.")

        with st.expander("🦠 What is measles?"):
            st.markdown("""
**Measles** is one of the most contagious pathogens ever described. Key features:
- **R₀:** 12–18 in unvaccinated populations (one of the highest known)
- **Herd immunity threshold:** ~93–95%
- **Transmission:** Airborne — survives in air for up to 2 hours after patient leaves
- **Incubation:** 8–12 days to symptom onset; 14–18 days to rash
- **Infectious period:** 4 days before to 4 days after rash onset
- **Prodrome:** Fever, cough, coryza, conjunctivitis (the "3 Cs") — Koplik spots pathognomonic
- **Complications:** Pneumonia (leading cause of measles death), encephalitis, SSPE (rare, fatal, years later)
- **Vaccine:** MMR — 97% effective after 2 doses
- **Elimination:** United States achieved measles elimination in 2000; maintained with high vaccination coverage
- **Re-emergence:** Outbreaks occur in clusters of unvaccinated individuals; imported cases seed outbreaks in communities below HIT
            """)


        next_step_button(ob2_step, OB2_STEPS, "ob2_idx")

# ════════════════════════════════════════════════════════════════
# SCENARIO 3: SALMONELLA
# ════════════════════════════════════════════════════════════════
elif ob_scenario == "🥘 Scenario 3: Salmonellosis at a Community Church Potluck":

    col_brief, col_stats = st.columns([2,1])
    with col_brief:
        st.markdown("""
### 🎯 Your Mission
It's Sunday evening. The county health department receives 4 calls from individuals reporting severe diarrhea, fever, and abdominal cramps after attending a church potluck dinner earlier that day. By Monday morning, 23 people have called with similar symptoms. All attended the same event. The pastor reports approximately 120 people were present. Your job: identify the vehicle, establish the case definition, calculate attack rates, and implement control.
        """)
    with col_stats:
        st.markdown("""
<div style="background:#f0fdf4;border-radius:8px;padding:14px;font-size:13px;">
<b>📋 Outbreak Brief</b><br><br>
🤒 <b>Cases reported:</b> 23 (and growing)<br>
🏥 <b>Hospitalizations:</b> 2<br>
💀 <b>Deaths:</b> 0<br>
📍 <b>Location:</b> Community church<br>
👥 <b>Event attendees:</b> ~120<br>
🕐 <b>Meal time:</b> Sunday 12:30 PM
</div>
        """, unsafe_allow_html=True)

    ob3_step = st.radio("Jump to step:", [
        "Step 1 — Build the case definition & line list",
        "Step 2 — Epidemic curve & incubation period estimation",
        "Step 3 — Food-specific attack rates (calculate)",
        "Step 4 — Environmental investigation",
        "Step 5 — Control, report & prevent recurrence",
    ], index=st.session_state.get("ob3_idx", 0), horizontal=False)
    st.divider()

    if ob3_step == "Step 1 — Build the case definition & line list":
        st.subheader("Step 1 — Case definition and line list construction")
        st.markdown("""
You need to systematically characterize who is sick before you can analyze the data. The **line list** is the epidemiologist's most important tool — one row per case, one column per variable.
        """)
        st.info("💡 **Step 4 of 10:** Construct a working case definition")

        st.markdown("#### ✏️ Interactive case definition builder")
        col1, col2 = st.columns(2)
        with col1:
            cd_person = st.selectbox("Person:", [
                "Any person in the county",
                "Any person who attended the First Baptist Church potluck",
                "Any church member",
            ], key="ob3_cd_person")
            cd_time = st.selectbox("Time:", [
                "Any time in November",
                "Symptom onset between Sunday noon and Tuesday midnight",
                "Only Sunday attendees who got sick same day",
            ], key="ob3_cd_time")
        with col2:
            cd_clinical = st.selectbox("Clinical criteria:", [
                "Any GI symptom",
                "Diarrhea (≥3 loose stools/24h) AND/OR fever (≥38°C) within 72h of meal",
                "Lab-confirmed Salmonella only",
            ], key="ob3_cd_clinical")
            cd_lab = st.selectbox("Lab classification:", [
                "Confirmed (Salmonella isolated from stool)",
                "Probable (clinical criteria met, no lab)",
                "Use both confirmed AND probable",
            ], key="ob3_cd_lab")

        if cd_person and cd_time and cd_clinical and cd_lab:
            case_def = f"{cd_person}, with {cd_clinical.lower()}, {cd_time.lower()}"
            st.info(f"**Your case definition:** {case_def}")

            if "potluck" in cd_person and "72h" in cd_clinical and "Tuesday" in cd_time:
                st.success("✅ Strong case definition — anchored to the exposure event, time-limited, uses appropriate clinical threshold.")
            elif "lab-confirmed" in cd_clinical:
                st.error("❌ Lab-only case definitions miss the majority of cases and delay investigation. Use clinical criteria with lab as confirmation.")

        st.divider()
        st.markdown("#### 📋 Sample line list (first 10 cases)")
        line_list = pd.DataFrame({
            "Case #": range(1, 11),
            "Age": [34, 67, 8, 45, 52, 23, 71, 39, 14, 58],
            "Sex": ["F","M","M","F","F","M","F","M","F","M"],
            "Onset time": ["Sun 8pm","Sun 6pm","Sun 9pm","Mon 2am","Mon 1am","Sun 7pm","Mon 4am","Sun 11pm","Mon 3am","Mon 6am"],
            "Diarrhea": ["✅","✅","✅","✅","✅","✅","✅","✅","✅","✅"],
            "Fever": ["✅","✅","❌","✅","✅","❌","✅","✅","❌","✅"],
            "Vomiting": ["✅","❌","✅","❌","✅","✅","❌","✅","✅","❌"],
            "Chicken salad": ["✅","✅","❌","✅","✅","✅","✅","✅","❌","✅"],
            "Deviled eggs": ["✅","✅","✅","✅","❌","✅","✅","❌","✅","✅"],
            "Potato salad": ["✅","❌","✅","✅","✅","❌","✅","✅","✅","✅"],
        })
        st.dataframe(line_list, use_container_width=True, hide_index=True)

        q1a = st.radio("**Decision 1A:** What does the line list immediately suggest about the most likely vehicle?", [
            "— Select —",
            "Potato salad — appears frequently",
            "Chicken salad or deviled eggs — egg/poultry = Salmonella, and most cases ate one or both",
            "Vomiting pattern suggests norovirus, not Salmonella",
            "Cannot tell from this limited data",
        ], key="ob3_q1a")

        if q1a == "Chicken salad or deviled eggs — egg/poultry = Salmonella, and most cases ate one or both":
            st.success("""
✅ **Correct.** Salmonella is most commonly associated with poultry, eggs, and egg-containing dishes (chicken salad, deviled eggs, mayonnaise-based salads). The line list shows most cases ate chicken salad and/or deviled eggs. This generates the primary hypothesis to test with attack rates. Note also that fever + diarrhea (non-bloody at this stage) is consistent with non-typhoidal Salmonella.
            """)
        elif q1a != "— Select —":
            st.error("❌ Biological plausibility matters: Salmonella's primary vehicles are poultry, eggs, and egg-containing dishes. The line list shows these items prominently in cases.")


        next_step_button(ob3_step, OB3_STEPS, "ob3_idx")

    elif ob3_step == "Step 2 — Epidemic curve & incubation period estimation":
        st.subheader("Step 2 — Epidemic curve and incubation period")
        st.markdown("The meal was served at **12:30 PM Sunday**. Below are the onset times for all 23 confirmed cases.")
        st.info("💡 **Step 6 of 10:** Describe in terms of time — epidemic curve")

        onset_hours = [6, 7, 8, 8, 9, 9, 10, 10, 11, 12, 12, 13, 13, 14, 15, 16, 17, 18, 20, 22, 25, 28, 30]
        onset_labels = [f"+{h}h" for h in onset_hours]

        import collections
        onset_counts = collections.Counter(onset_hours)
        curve_df = pd.DataFrame([{"Hours after meal": h, "Cases": onset_counts.get(h, 0)} for h in range(0, 32)])
        curve_df = curve_df[curve_df["Cases"] > 0]
        st.bar_chart(curve_df.set_index("Hours after meal"))
        st.caption("X-axis: hours after meal (12:30 PM Sunday). Each bar = cases with that onset hour.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
**Summary statistics:**
- First case: +6 hours after meal
- Last case: +30 hours after meal
- **Peak:** +10–14 hours
- **Median incubation:** ~12 hours
- **Range:** 6–30 hours
            """)
        with col2:
            st.markdown("""
**Salmonella incubation reference:**
- Typical: 6–72 hours
- Most common: 12–36 hours
- Median: ~18 hours
- Range varies by inoculum dose
            """)

        q2a = st.radio("**Decision 2A:** What does this epidemic curve confirm?", [
            "— Select —",
            "Propagated outbreak — cases still occurring 30 hours later indicates person-to-person spread",
            "Point-source outbreak — all cases within one incubation period of a single exposure",
            "Endemic pattern — stable ongoing transmission",
            "Mixed — early point source followed by secondary cases",
        ], key="ob3_q2a")

        if q2a == "Point-source outbreak — all cases within one incubation period of a single exposure":
            st.success("""
✅ **Correct.** All 23 cases occurred within 6–30 hours of a single exposure event (the potluck meal). The shape — single peak, rapid rise and fall — is a classic point-source curve. The "tail" of cases at +25–30 hours represents natural variation in incubation time, not a new wave.

The incubation range (6–30h) is consistent with Salmonella, narrowing the list of potential agents before lab confirmation.
            """)
        elif q2a != "— Select —":
            st.error("❌ All cases cluster within 30 hours of a single meal — this is a point-source pattern. For secondary spread (propagated), you would expect a gap of approximately one incubation period before a new wave appears.")

        if q2a != "— Select —":
            st.divider()
            st.markdown("#### 🧮 Use the curve to estimate the exposure time")
            st.markdown("""
**Forensic timing:** The median incubation for Salmonella is ~12–18 hours. Working backward from the peak onset (10–14 hours post-meal), the median case had an incubation of ~12 hours.

If you didn't know when the meal occurred, you could estimate it: find the median onset time, subtract the expected median incubation period for the suspected agent.

**Median onset:** approximately +12 hours after 12:30 PM = ~12:30 AM Monday
**Subtract median incubation (12h):** ~12:30 PM Sunday → consistent with the known meal time ✅

This technique is used in investigations where the exposure time is unknown.
            """)


        next_step_button(ob3_step, OB3_STEPS, "ob3_idx")

    elif ob3_step == "Step 3 — Food-specific attack rates (calculate)":
        st.subheader("Step 3 — Calculate food-specific attack rates")
        st.markdown("""
You have completed telephone interviews with 98 of the 120 attendees (82% response rate). 23 meet the case definition.

For each food item, the table below shows how many attendees ate it, and of those, how many became sick.
        """)
        st.info("💡 **Steps 7–8 of 10:** Develop hypotheses → Test hypotheses analytically")

        food_items_3 = {
            "Chicken salad": (18, 4, 5, 71),
            "Deviled eggs": (17, 5, 6, 70),
            "Potato salad (mayo-based)": (15, 15, 8, 60),
            "Green bean casserole": (8, 52, 15, 23),
            "Macaroni and cheese": (6, 54, 17, 21),
            "Lemonade": (12, 48, 11, 27),
            "Chocolate cake": (10, 50, 13, 25),
        }

        st.markdown("#### 🧮 Complete the table — calculate AR and RR for each food item")
        st.markdown("*AR = (Sick among those who ate) ÷ (Total who ate) × 100. RR = AR exposed ÷ AR unexposed.*")

        results3 = []
        for food, (ate_sick, ate_well, notate_sick, notate_well) in food_items_3.items():
            ate_total = ate_sick + ate_well
            notate_total = notate_sick + notate_well
            ar_exp = round(ate_sick / ate_total * 100, 1)
            ar_unexp = round(notate_sick / notate_total * 100, 1)
            rr = round(ar_exp / ar_unexp, 2) if ar_unexp > 0 else float("inf")
            results3.append({
                "Food": food,
                "Ate: sick/total": f"{ate_sick}/{ate_total}",
                "AR exposed %": ar_exp,
                "Didn't eat: sick/total": f"{notate_sick}/{notate_total}",
                "AR unexposed %": ar_unexp,
                "RR": rr
            })

        results3_df = pd.DataFrame(results3)
        st.dataframe(results3_df, use_container_width=True, hide_index=True)

        q3a = st.radio("**Decision 3A:** Which food item is the most likely vehicle?", [
            "— Select —",
            "Potato salad — high number ate it",
            "Chicken salad — highest RR with very low attack rate in unexposed",
            "Deviled eggs — high RR, egg-Salmonella association",
            "Both chicken salad AND deviled eggs — same cook, cross-contamination likely",
        ], key="ob3_q3a")

        if q3a == "Both chicken salad AND deviled eggs — same cook, cross-contamination likely":
            st.success("""
✅ **Correct — excellent epidemiologic reasoning.** Both chicken salad and deviled eggs show high RR and very low AR unexposed. In real investigations, when two items both show strong associations, look for a common source: the same cook, the same contaminated ingredient (raw chicken), the same utensils, or the same refrigerator. Here, the church member who brought both dishes used the same cutting board for raw chicken and egg preparation — a classic cross-contamination scenario.
            """)
        elif q3a == "Chicken salad — highest RR with very low attack rate in unexposed":
            st.warning("""
⚠️ **Partially correct.** Chicken salad does have the highest RR. But when two items show similar strong signals (chicken salad AND deviled eggs), consider a common source — same cook, same ingredient, cross-contamination. The best answer acknowledges both.
            """)
        elif q3a != "— Select —":
            st.error("❌ Focus on the items with the highest RR AND the lowest AR unexposed. Potato salad actually has similar attack rates in those who ate vs. didn't eat (suggesting no association with illness).")

        if q3a != "— Select —":
            st.divider()
            st.markdown("#### 🧮 Practice: Calculate the RR for chicken salad manually")
            st.markdown("Ate chicken salad: 18 sick, 4 well. Did not eat: 5 sick, 71 well.")

            ar_exp_input = st.number_input("AR exposed (ate chicken salad) %:", 0.0, 100.0, 0.0, 0.1, key="ob3_ar_exp")
            ar_unexp_input = st.number_input("AR unexposed (did not eat) %:", 0.0, 100.0, 0.0, 0.1, key="ob3_ar_unexp")
            rr_input = st.number_input("RR:", 0.0, 50.0, 0.0, 0.01, key="ob3_rr")

            if st.button("Check calculation", key="ob3_check_rr"):
                correct_ar_exp = round(18/22*100, 1)
                correct_ar_unexp = round(5/76*100, 1)
                correct_rr = round(correct_ar_exp/correct_ar_unexp, 2)
                st.markdown(f"""
**Correct values:**
- AR exposed = 18/22 = **{correct_ar_exp}%**
- AR unexposed = 5/76 = **{correct_ar_unexp}%**
- RR = {correct_ar_exp}/{correct_ar_unexp} = **{correct_rr}**

An RR of {correct_rr} means students who ate the chicken salad were {correct_rr}× more likely to become ill than those who did not. This is strong evidence for chicken salad as a vehicle.
                """)
                if abs(ar_exp_input - correct_ar_exp) < 1 and abs(rr_input - correct_rr) < 0.2:
                    st.success("✅ Your calculation is correct!")
                else:
                    st.info("Check your arithmetic — divide sick ÷ total (not sick + well) to get the attack rate.")


        next_step_button(ob3_step, OB3_STEPS, "ob3_idx")

    elif ob3_step == "Step 4 — Environmental investigation":
        st.subheader("Step 4 — Environmental investigation and source tracing")
        st.markdown("""
The analytic study has identified chicken salad and deviled eggs as vehicles. Both were prepared by the same congregation member (Mrs. Johnson). Now you need to trace the contamination to its source.
        """)
        st.info("💡 **Step 8 continued:** Environmental sampling + source tracing")

        st.markdown("""
**Environmental investigation findings:**
- Mrs. Johnson prepared both dishes Saturday evening at home
- She purchased whole chickens from a local grocery store Saturday morning
- She used a wooden cutting board that had been used for raw chicken
- The same cutting board was used to chop celery and onions for the chicken salad
- Deviled eggs were prepared in the same kitchen, same surfaces
- Dishes were refrigerated Saturday night, transported to church in a cooler Sunday
- Temperature at time of service: chicken salad = 58°F (should be ≤41°F)
- Mrs. Johnson reports no illness herself

**Samples collected:**
- Leftover chicken salad: submitted to state lab
- Mrs. Johnson's cutting board: swab submitted
- Remaining whole chicken from grocery store (same purchase): submitted
- Stool samples from 8 cases
        """)

        q4a = st.radio("**Decision 4A:** The chicken salad temperature was 58°F at service. Why does this matter?", [
            "— Select —",
            "It doesn't matter — Salmonella only comes from contaminated animals, not temperature",
            "Temperatures between 41°F and 135°F allow Salmonella to multiply rapidly — the 'danger zone'",
            "58°F is only slightly above the 55°F threshold — minimal risk",
            "Temperature only matters for viruses, not bacteria",
        ], key="ob3_q4a")

        if q4a == "Temperatures between 41°F and 135°F allow Salmonella to multiply rapidly — the 'danger zone'":
            st.success("""
✅ **Correct.** The USDA "temperature danger zone" for bacterial growth is 41°F–135°F (5°C–57°C). At 58°F, Salmonella can double every 20–30 minutes. Even a small initial contamination can reach an infectious dose (10³–10⁶ organisms) within hours at this temperature. The combination of contamination (cross-contamination from raw chicken) AND temperature abuse (inadequate refrigeration/transport) created ideal conditions for a large outbreak.
            """)
        elif q4a != "— Select —":
            st.error("❌ Temperature is critical for bacterial foodborne illness. Unlike viruses (which don't replicate in food), bacteria like Salmonella multiply exponentially at temperatures between 41°F and 135°F.")

        if q4a != "— Select —":
            st.divider()
            q4b = st.radio("**Decision 4B:** Lab results show Salmonella Enteritidis in the leftover chicken salad and cutting board. The grocery store chicken is also positive. What do you do?", [
                "— Select —",
                "Issue press release blaming Mrs. Johnson",
                "Contact the state health department and FDA/USDA to investigate the grocery store chicken supplier",
                "Close the church for 2 weeks",
                "No further action — the event is over",
            ], key="ob3_q4b")

            if q4b == "Contact the state health department and FDA/USDA to investigate the grocery store chicken supplier":
                st.success("""
✅ **Correct.** When a contaminated commercial food product is implicated, investigation extends up the supply chain. This outbreak may be one of many — PulseNet (CDC's molecular surveillance network) may identify the same Salmonella strain in cases from other states linked to the same supplier. A voluntary recall or regulatory action may be needed to prevent further illness nationally.

This is how local foodborne investigations become national — the church potluck is the sentinel event that alerts the system to a broader contamination.
                """)
            elif q4b != "— Select —":
                st.error("❌ When a commercially distributed product is the source, the investigation extends beyond the local outbreak. Other communities may be at risk from the same supplier.")


        next_step_button(ob3_step, OB3_STEPS, "ob3_idx")

    elif ob3_step == "Step 5 — Control, report & prevent recurrence":
        st.subheader("Step 5 — Control, reporting, and prevention")
        st.info("💡 **Steps 9–10 of 10:** Implement control measures → Communicate findings")

        st.markdown("""
**Final outbreak profile:**
- 23 cases, 2 hospitalizations, 0 deaths
- Salmonella Enteritidis serotype confirmed in 7/8 stool samples
- Same strain found in chicken salad and cutting board
- PulseNet match: identical molecular fingerprint to 12 cases in 2 other counties from same grocery chain
- Grocery chain initiated voluntary recall of whole chickens from that distributor

**Lessons applied:**
        """)

        lessons = {
            "Cross-contamination prevention": "Use separate cutting boards for raw meat and ready-to-eat foods",
            "Temperature control": "Keep cold foods at ≤41°F during preparation, storage, and transport",
            "Potluck food safety": "Bring hot foods hot (≥135°F) and cold foods cold (≤41°F)",
            "Hand hygiene": "Wash hands thoroughly after handling raw poultry",
            "Food handler illness": "Exclude food handlers who are ill (though Mrs. Johnson was not ill herself)",
            "Supply chain surveillance": "PulseNet enables local outbreaks to trigger national investigations",
        }

        for lesson, detail in lessons.items():
            with st.expander(f"✅ {lesson}"):
                st.markdown(detail)

        st.divider()
        st.markdown("#### 📝 Write your outbreak report")
        st.markdown("A complete outbreak investigation report includes:")

        report_sections = [
            ("Background", "When and where the outbreak was identified; who was affected"),
            ("Methods", "Case definition used; how cases were found; how data were collected"),
            ("Results", "Epidemic curve; case count; attack rates; most likely vehicle"),
            ("Conclusions", "Probable source; contributing factors; mechanism of contamination"),
            ("Recommendations", "Immediate control measures; long-term prevention"),
        ]

        for section, description in report_sections:
            st.markdown(f"**{section}:** {description}")

        with st.expander("🦠 What is Salmonella?"):
            st.markdown("""
**Salmonella** is a gram-negative bacteria and one of the most common causes of foodborne illness worldwide.

- **Species:** Salmonella enterica (>2,500 serotypes); most common in US = S. Typhimurium and S. Enteritidis
- **Sources:** Poultry, eggs, beef, pork, reptiles, contaminated produce
- **Transmission:** Fecal-oral; ingestion of contaminated food or water; contact with infected animals
- **Incubation:** 6–72 hours (typically 12–36h)
- **Symptoms:** Diarrhea (may be bloody), fever, abdominal cramps, vomiting
- **Duration:** 4–7 days (self-limited in healthy adults)
- **At-risk populations:** Infants, elderly, immunocompromised — may develop bacteremia, meningitis
- **Infectious dose:** As low as 10³ organisms (lower in high-fat vehicles like chocolate, peanut butter)
- **Treatment:** Usually supportive; antibiotics for severe cases or bacteremia (resistance emerging)
- **Prevention:** Cook poultry to 165°F; avoid cross-contamination; refrigerate properly; hand hygiene
- **Surveillance:** Nationally notifiable; PulseNet provides molecular fingerprinting for outbreak detection
            """)


        next_step_button(ob3_step, OB3_STEPS, "ob3_idx")

elif ob_scenario == "— Choose an outbreak —":
    st.info("Select a scenario above to begin your investigation.")
    st.markdown("""
#### 🎯 What you'll practice in Outbreak Lab
Each scenario walks you through a real-style outbreak investigation, applying the **10-step framework** with:
- **Decision points** — choose the right investigative action and get immediate feedback
- **Interactive calculations** — calculate attack rates, RR, and herd immunity thresholds yourself
- **Epidemic curves** — read and interpret real outbreak patterns
- **Case definitions** — build your own and understand the tradeoffs
- **Control measures** — choose and justify interventions

**The three scenarios cover:**
| Scenario | Agent | Key skills |
|---|---|---|
| 🍽️ University Dining Hall | Norovirus | Attack rates, vehicle identification, secondary spread |
| 📚 Elementary School | Measles | Herd immunity math, contact tracing, vaccination policy |
| 🥘 Church Potluck | Salmonella | Case definition, incubation estimation, supply chain tracing |
    """)


# ==================================================


# ── Bottom CTA ────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="background:#f0f9ff;border:1px solid #bfdbfe;border-radius:10px;
     padding:20px 24px;margin-top:24px;">
  <div style="font-size:16px;font-weight:700;color:#1e3a5f;margin-bottom:8px;">
    📚 This is a free preview of EpiLab Interactive
  </div>
  <div style="font-size:13px;color:#374151;line-height:1.7;margin-bottom:14px;">
    The full app includes <strong>4 complete modules</strong> covering study design, disease
    frequency, measures of association, and 35+ practice scenarios — plus these three outbreak
    investigations and four instructor manuals aligned to CEPH competencies.
  </div>
  <a href="https://mathiscope504.gumroad.com/l/mknsox" target="_blank"
     style="background:#2563eb;color:white;font-weight:700;font-size:13px;
            padding:10px 20px;border-radius:6px;text-decoration:none;display:inline-block;">
    Learn More →
  </a>
  &nbsp;&nbsp;
</div>
""", unsafe_allow_html=True)
