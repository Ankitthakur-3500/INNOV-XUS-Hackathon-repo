"""
PharmaLink AI — Smart Drug Redistribution Platform
Chandigarh Tri-City Edition (Chandigarh · Mohali · Panchkula)
Run with: streamlit run pharmalink_dashboard.py
Dependencies: pip install streamlit plotly pandas numpy
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random, time

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Medi Flow AI — Chandigarh",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root {
    --blue:#0A3D62; --blue2:#1565C0; --teal:#00838F; --teal2:#4DB6AC;
    --red:#C62828;  --orange:#E65100; --green:#2E7D32; --amber:#F57F17;
    --bg:#F0F4F8;   --card:#FFFFFF;   --border:#DDE5EF;
    --txt:#0D1B2A;  --muted:#546E7A;
}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background:var(--bg)!important;color:var(--txt);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#062a47 0%,#0A3D62 55%,#083351 100%)!important;}
[data-testid="stSidebar"] *{color:#CFD8DC!important;}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label{
    background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
    border-radius:10px;padding:10px 14px;margin-bottom:6px;
    transition:all .2s;font-size:.88rem;font-weight:500;color:#B0BEC5!important;}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover{
    background:rgba(0,131,143,.3);border-color:#4DB6AC;color:#fff!important;}
.page-header{background:linear-gradient(120deg,#0A3D62 0%,#1565C0 55%,#00838F 100%);
    border-radius:16px;padding:26px 32px;margin-bottom:24px;
    display:flex;align-items:center;justify-content:space-between;
    box-shadow:0 6px 24px rgba(10,61,98,.2);}
.page-header h1{color:#fff;font-size:1.6rem;font-weight:700;margin:0;}
.page-header p{color:rgba(255,255,255,.72);font-size:.85rem;margin:4px 0 0;}
.live-badge{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);
    border-radius:20px;padding:6px 16px;color:#fff;font-size:.76rem;font-weight:600;
    display:flex;align-items:center;gap:7px;}
.live-dot{width:8px;height:8px;background:#4CAF50;border-radius:50%;display:inline-block;animation:blink 1.4s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
[data-testid="metric-container"]{background:var(--card);border:1px solid var(--border);
    border-radius:14px;padding:18px 20px;box-shadow:0 2px 10px rgba(10,61,98,.07);
    position:relative;overflow:hidden;}
[data-testid="metric-container"]::before{content:'';position:absolute;top:0;left:0;
    width:4px;height:100%;background:linear-gradient(180deg,#1565C0,#00838F);border-radius:4px 0 0 4px;}
[data-testid="stMetricLabel"]{font-size:.74rem!important;font-weight:600!important;
    letter-spacing:.05em!important;text-transform:uppercase!important;color:var(--muted)!important;}
[data-testid="stMetricValue"]{font-size:1.9rem!important;font-weight:700!important;color:var(--blue)!important;}
[data-testid="stMetricDelta"]{font-size:.78rem!important;}
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;
    padding:18px 20px;box-shadow:0 2px 10px rgba(10,61,98,.06);margin-bottom:16px;}
.card-title{font-size:.86rem;font-weight:700;color:var(--blue);margin-bottom:10px;}
.alert-red{background:#FFEBEE;border-left:4px solid #C62828;border-radius:10px;padding:11px 15px;margin-bottom:8px;font-size:.83rem;}
.alert-amber{background:#FFF8E1;border-left:4px solid #F57F17;border-radius:10px;padding:11px 15px;margin-bottom:8px;font-size:.83rem;}
.alert-blue{background:#E3F2FD;border-left:4px solid #1565C0;border-radius:10px;padding:11px 15px;margin-bottom:8px;font-size:.83rem;}
.alert-green{background:#E8F5E9;border-left:4px solid #2E7D32;border-radius:10px;padding:11px 15px;margin-bottom:8px;font-size:.83rem;}
.tx-card{border:1px solid var(--border);border-radius:10px;padding:9px 12px;margin-bottom:6px;
    background:#fff;font-size:.79rem;line-height:1.5;}
.explain{font-size:.78rem;color:var(--muted);background:#F8FBFF;border-radius:8px;
    padding:7px 12px;margin-top:4px;margin-bottom:12px;border:1px solid #E8EEF6;}
.brand{text-align:center;padding:22px 0 26px;border-bottom:1px solid rgba(255,255,255,.1);margin-bottom:18px;}
.brand .icon{font-size:2.1rem;}
.brand .name{font-size:1.1rem;font-weight:700;color:#fff!important;margin-top:4px;}
.brand .sub{font-size:.68rem;color:#78909C!important;text-transform:uppercase;letter-spacing:.07em;}
[data-testid="stDataFrame"]{border-radius:10px;overflow:hidden;}
[data-testid="stFileUploaderDropzone"]{border:2px dashed var(--teal)!important;
    border-radius:12px!important;background:rgba(0,131,143,.04)!important;}
hr{border:none;border-top:1px solid var(--border);margin:16px 0;}

/* City zone badge */
.zone-badge{display:inline-block;padding:3px 10px;border-radius:20px;
    font-size:.72rem;font-weight:600;margin-right:4px;}
.zone-chd{background:#E3F2FD;color:#0A3D62;}
.zone-mohali{background:#E8F5E9;color:#1B5E20;}
.zone-pkula{background:#FFF8E1;color:#E65100;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# CHANDIGARH TRI-CITY SYNTHETIC DATA
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(42); random.seed(42)

    # ── 10 real hospitals in Chandigarh / Mohali / Panchkula with precise coords ──
    hospitals = pd.DataFrame({
        "name": [
            "PGIMER Chandigarh",
            "Government Medical College & Hospital (GMCH-32)",
            "Government Multi-Specialty Hospital (GMSH-16)",
            "Sector 22 Civil Hospital",
            "Fortis Hospital Mohali",
            "Max Super Speciality Hospital Mohali",
            "Civil Hospital Mohali (Phase 6)",
            "Alchemist Hospital Panchkula",
            "Civil Hospital Panchkula (Sector 6)",
            "Ivy Hospital Sector 71 Mohali",
        ],
        "short": [
            "PGIMER",
            "GMCH-32",
            "GMSH-16",
            "Civil Sec-22",
            "Fortis Mohali",
            "Max Mohali",
            "Civil Mohali",
            "Alchemist Pkula",
            "Civil Pkula",
            "Ivy Mohali",
        ],
        "city": [
            "Chandigarh","Chandigarh","Chandigarh","Chandigarh",
            "Mohali","Mohali","Mohali",
            "Panchkula","Panchkula","Mohali",
        ],
        "zone": [
            "Chandigarh","Chandigarh","Chandigarh","Chandigarh",
            "Mohali","Mohali","Mohali",
            "Panchkula","Panchkula","Mohali",
        ],
        # Precise lat/lon for each hospital
        "lat": [
            30.7650,   # PGIMER
            30.7228,   # GMCH-32
            30.7445,   # GMSH-16
            30.7380,   # Civil Sec-22
            30.7046,   # Fortis Mohali
            30.6960,   # Max Mohali
            30.6880,   # Civil Mohali Phase 6
            30.6970,   # Alchemist Panchkula
            30.6910,   # Civil Panchkula Sec-6
            30.6750,   # Ivy Mohali Sec-71
        ],
        "lon": [
            76.7793,   # PGIMER
            76.7869,   # GMCH-32
            76.7980,   # GMSH-16
            76.7700,   # Civil Sec-22
            76.7175,   # Fortis Mohali
            76.6980,   # Max Mohali
            76.7120,   # Civil Mohali
            76.8580,   # Alchemist Panchkula
            76.8490,   # Civil Panchkula
            76.6930,   # Ivy Mohali
        ],
        "stock_pct":    [72, 45, 88, 33, 91, 22, 61, 54, 78, 40],
        "expiring_30d": [120, 340, 80, 510, 60, 720, 150, 280, 95, 430],
        "status": [
            "Stable","Warning","Stable","Critical",
            "Stable","Critical","Stable",
            "Warning","Stable","Warning",
        ],
        "beds": [2000, 500, 300, 120, 250, 300, 80, 150, 100, 200],
        "type": [
            "Government","Government","Government","Government",
            "Private","Private","Government",
            "Private","Government","Private",
        ],
    })

    medicines = [
        "Amoxicillin 500mg","Metformin 850mg","Atorvastatin 40mg",
        "Paracetamol 650mg","Insulin Glargine","Ceftriaxone 1g",
        "Oseltamivir 75mg","Hydroxychloroquine 200mg","Folic Acid 5mg","Aspirin 75mg",
    ]

    # Transfers only between local hospitals
    transfers = []
    for i in range(18):
        oi = random.randint(0, 9)
        di = random.randint(0, 9)
        while di == oi:
            di = random.randint(0, 9)
        transfers.append({
            "ID":        f"TRF-{2024000+i}",
            "From":      hospitals.iloc[oi]["short"],
            "To":        hospitals.iloc[di]["short"],
            "From Zone": hospitals.iloc[oi]["zone"],
            "To Zone":   hospitals.iloc[di]["zone"],
            "Medicine":  random.choice(medicines),
            "Units":     random.randint(200, 5000),
            "ETA (hrs)": random.randint(1, 6),   # local = short ETA
            "Status":    random.choice(["✅ Delivered","🚛 In-Transit","📦 Dispatched","⚠️ Delayed"]),
            "Priority":  random.choice(["🔴 HIGH","🟡 MED","🔵 LOW"]),
            "_fi": oi, "_ti": di,
        })
    transfers_df = pd.DataFrame(transfers)

    days      = pd.date_range(end=datetime.today(), periods=60)
    pred_days = pd.date_range(start=datetime.today(), periods=31)
    ts_data, pr_data = {}, {}
    for med in medicines[:5]:
        start = random.randint(7000, 12000)
        hist  = np.clip(start + np.cumsum(np.random.normal(-75, 28, 60)), 500, 15000).astype(int)
        fcast = np.clip(hist[-1] + np.cumsum(np.random.normal(-105, 22, 31)), 0, hist[-1]).astype(int)
        ts_data[med] = hist
        pr_data[med] = fcast
    ts_df = pd.DataFrame(ts_data, index=days)
    pr_df = pd.DataFrame(pr_data, index=pred_days)

    categories = ["Antibiotics","Analgesics","Antidiabetics","Cardiac","Vaccines","Oncology"]
    inv_cat = pd.DataFrame({
        "Category": categories,
        "In Stock":  [45200, 38700, 29400, 51000, 12300, 8900],
        "Expiring":  [2100, 1800, 3400, 900, 4200, 350],
        "Critical":  [False, False, True, False, True, False],
    })

    return hospitals, transfers_df, ts_df, pr_df, inv_cat

hospitals, transfers_df, ts_df, pr_df, inv_cat = generate_data()

# Map centre & zoom for Chandigarh tri-city
MAP_CENTER = dict(lat=30.725, lon=76.770)
MAP_ZOOM   = 11.2

# Shared Plotly defaults
PL = dict(
    font=dict(family="Inter", size=12, color="#0D1B2A"),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=8, t=36, b=8),
    xaxis=dict(gridcolor="#EEF2F7", linecolor="#DDE5EF", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#EEF2F7", linecolor="#DDE5EF", tickfont=dict(size=11)),
)

# Zone colours
ZONE_CLR = {"Chandigarh": "#1565C0", "Mohali": "#2E7D32", "Panchkula": "#E65100"}

# ──────────────────────────────────────────────────────────────────────────────
# MAP BUILDER HELPER
# Draws hospital nodes + transfer arcs — reused by both Command Center & Redist.
# ──────────────────────────────────────────────────────────────────────────────
def build_city_map(height=420, show_arcs=True, arc_pairs=None, status_colors=None):
    """
    Returns a Plotly figure of the Chandigarh tri-city hospital network.
    arc_pairs  : list of (from_idx, to_idx) tuples for arc drawing
    status_colors : dict {status_str: hex_color} for arc colouring (redistribution mode)
    """
    fig = go.Figure()

    # ── Zone boundary circles (visual context) ──
    zone_centres = {
        "Chandigarh": (30.7450, 76.7800, "#1565C0"),
        "Mohali":     (30.6950, 76.7150, "#2E7D32"),
        "Panchkula":  (30.6940, 76.8530, "#E65100"),
    }
    for zone, (zlat, zlon, zclr) in zone_centres.items():
        fig.add_trace(go.Scattermapbox(
            lat=[zlat], lon=[zlon],
            mode="markers+text",
            marker=dict(size=52, color=zclr, opacity=0.07),
            text=[zone],
            textposition="top center",
            textfont=dict(size=11, color=zclr),
            hoverinfo="skip",
            showlegend=False,
        ))

    # ── Transfer arcs ──
    if show_arcs:
        if arc_pairs and status_colors:
            # Redistribution mode: colour each arc by transfer status
            for _, row in transfers_df.iterrows():
                oi, di = int(row["_fi"]), int(row["_ti"])
                h1, h2 = hospitals.iloc[oi], hospitals.iloc[di]
                clr = status_colors.get(row.Status, "#90A4AE")
                wid = 3 if "Delayed" in row.Status else 1.8
                mid_lat = (h1.lat + h2.lat) / 2 + 0.008  # small arc lift for local scale
                mid_lon = (h1.lon + h2.lon) / 2
                fig.add_trace(go.Scattermapbox(
                    lat=[h1.lat, mid_lat, h2.lat],
                    lon=[h1.lon, mid_lon, h2.lon],
                    mode="lines",
                    line=dict(width=wid, color=clr),
                    hoverinfo="skip", showlegend=False,
                ))
        else:
            # Command Center mode: teal arcs for sample transfers
            default_pairs = [(0,3),(3,4),(1,5),(2,7),(4,8),(6,0),(5,2),(7,9)]
            for (i, j) in default_pairs:
                h1, h2 = hospitals.iloc[i], hospitals.iloc[j]
                mid_lat = (h1.lat + h2.lat) / 2 + 0.006
                mid_lon = (h1.lon + h2.lon) / 2
                fig.add_trace(go.Scattermapbox(
                    lat=[h1.lat, mid_lat, h2.lat],
                    lon=[h1.lon, mid_lon, h2.lon],
                    mode="lines",
                    line=dict(width=2, color="rgba(0,131,143,0.55)"),
                    hoverinfo="skip", showlegend=False,
                ))

    # ── Hospital nodes grouped by status ──
    status_node_clr = {"Stable": "#1565C0", "Warning": "#F57F17", "Critical": "#C62828"}
    for status, grp in hospitals.groupby("status"):
        fig.add_trace(go.Scattermapbox(
            lat=grp.lat, lon=grp.lon,
            mode="markers+text",
            marker=dict(
                size=grp.stock_pct / 5 + 14,
                color=status_node_clr[status],
                opacity=0.90,
            ),
            text=grp.short,
            textposition="top right",
            textfont=dict(size=9.5, color="#0A3D62"),
            customdata=grp[["name","city","zone","stock_pct","expiring_30d","status","type","beds"]].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "📍 %{customdata[1]} &nbsp;·&nbsp; Zone: %{customdata[2]}<br>"
                "🏥 Type: %{customdata[6]} &nbsp;·&nbsp; Beds: %{customdata[7]}<br>"
                "💊 Stock left: <b>%{customdata[3]}%</b><br>"
                "⚠️ Expiring soon: %{customdata[4]} units<br>"
                "Health: <b>%{customdata[5]}</b><extra></extra>"
            ),
            name=f"{status} stock",
        ))

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=MAP_CENTER,
            zoom=MAP_ZOOM,
        ),
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h", x=0, y=1.03,
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#DDE5EF", borderwidth=1,
            font=dict(size=11),
        ),
    )
    return fig

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="icon">💊</div>
        <div class="name">Medi Flow AI</div>
        <div class="sub">Chandigarh Tri-City Network</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Go to", [
        "🛰️  Command Center",
        "📈  Shortage Predictor",
        "🚚  Redistribution Hub",
        "📦  Inventory Check-in",
    ], label_visibility="collapsed")

    st.markdown("---")
    # Zone legend
    st.markdown("""
    <div style="font-size:.76rem;margin-bottom:12px">
        <div style="color:#90A4AE;font-weight:600;letter-spacing:.06em;
                    text-transform:uppercase;margin-bottom:6px">Coverage Zones</div>
        <span class="zone-badge zone-chd">● Chandigarh</span><br><br>
        <span class="zone-badge zone-mohali">● Mohali</span><br><br>
        <span class="zone-badge zone-pkula">● Panchkula</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:.79rem;line-height:2.2">
        🟢 &nbsp;<b style="color:#CFD8DC">AI Engine</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#4CAF50">Online</span><br>
        🟢 &nbsp;<b style="color:#CFD8DC">Data Feed</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#4CAF50">Active</span><br>
        🟡 &nbsp;<b style="color:#CFD8DC">OCR Module</b>&nbsp;&nbsp;<span style="color:#FFC107">Standby</span><br>
        🔵 &nbsp;<b style="color:#CFD8DC">Last Sync</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#90CAF9">3 min ago</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:.7rem;color:#546E7A;text-align:center;line-height:1.9">
        Ministry of Health &amp; Family Welfare<br>
        Punjab / Chandigarh Region &nbsp;·&nbsp;<span style="color:#4DB6AC">v2.4.1</span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COMMAND CENTER
# ══════════════════════════════════════════════════════════════════════════════
if "Command" in page:
    now = datetime.now().strftime("%d %b %Y  •  %H:%M")
    st.markdown(f"""
    <div class="page-header">
        <div>
            <h1>🛰️ Chandigarh Command Center</h1>
            <p>Live overview — 10 hospitals across Chandigarh · Mohali · Panchkula — {now}</p>
        </div>
        <div class="live-badge"><span class="live-dot"></span> LIVE</div>
    </div>""", unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("🏥 Hospitals Tracked",   "10",       "Tri-city network")
    k2.metric("💊 Total Stock (Units)", "2,85,500", "Across all 10 sites")
    k3.metric("⚠️ Expiring in 30 Days", "13,680",   "+8% vs last month", delta_color="inverse")
    k4.metric("🚚 Active Transfers",    "18",       "+5 today")
    k5.metric("🔴 Critical Sites",      "2",        "GMCH-32 & Max Mohali", delta_color="inverse")

    st.markdown('<p class="explain">💡 <b>Green arrow</b> = improving. <b>Red arrow</b> = getting worse. Numbers refresh every few minutes.</p>', unsafe_allow_html=True)
    st.markdown("")

    # ── City zone summary strip ───────────────────────────────────────────────
    z1, z2, z3 = st.columns(3)
    with z1:
        st.markdown("""
        <div class="card" style="border-top:4px solid #1565C0;padding:14px 18px">
            <div style="font-size:.8rem;font-weight:700;color:#1565C0;margin-bottom:8px">🏙️ Chandigarh (4 Hospitals)</div>
            <div style="font-size:.82rem;color:#37474F;line-height:1.9">
                PGIMER &nbsp;·&nbsp; GMCH-32 &nbsp;·&nbsp; GMSH-16 &nbsp;·&nbsp; Civil Sec-22<br>
                <span style="color:#C62828;font-weight:600">⚠ 1 Critical</span> &nbsp;·&nbsp;
                <span style="color:#F57F17;font-weight:600">1 Warning</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with z2:
        st.markdown("""
        <div class="card" style="border-top:4px solid #2E7D32;padding:14px 18px">
            <div style="font-size:.8rem;font-weight:700;color:#2E7D32;margin-bottom:8px">🌿 Mohali (4 Hospitals)</div>
            <div style="font-size:.82rem;color:#37474F;line-height:1.9">
                Fortis &nbsp;·&nbsp; Max &nbsp;·&nbsp; Civil Mohali &nbsp;·&nbsp; Ivy Sec-71<br>
                <span style="color:#C62828;font-weight:600">⚠ 1 Critical</span> &nbsp;·&nbsp;
                <span style="color:#F57F17;font-weight:600">1 Warning</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with z3:
        st.markdown("""
        <div class="card" style="border-top:4px solid #E65100;padding:14px 18px">
            <div style="font-size:.8rem;font-weight:700;color:#E65100;margin-bottom:8px">🏔️ Panchkula (2 Hospitals)</div>
            <div style="font-size:.82rem;color:#37474F;line-height:1.9">
                Alchemist &nbsp;·&nbsp; Civil Panchkula Sec-6<br>
                <span style="color:#2E7D32;font-weight:600">✅ Both Stable / Warning</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # ── Map + Alerts ──────────────────────────────────────────────────────────
    col_map, col_alerts = st.columns([2, 1], gap="medium")

    with col_map:
        st.markdown('<div class="card-title">🗺️ Tri-City Hospital Network — Chandigarh · Mohali · Panchkula</div>', unsafe_allow_html=True)
        st.markdown("""
        <p class="explain">
            🔵 Blue dot = healthy stock &nbsp;|&nbsp; 🟠 Orange = running low &nbsp;|&nbsp;
            🔴 Red = critical shortage &nbsp;|&nbsp; Bigger dot = more stock<br>
            Teal curved lines = active drug transfers between hospitals right now.
            Hover any dot for full hospital details.
        </p>""", unsafe_allow_html=True)

        st.plotly_chart(build_city_map(height=420), use_container_width=True)

    with col_alerts:
        st.markdown('<div class="card-title">🚨 Alerts That Need Attention Right Now</div>', unsafe_allow_html=True)
        for lvl, title, msg in [
            ("red",   "🔴 URGENT — Civil Sec-22 (CHD)",    "Only 33% stock left. Insulin Glargine nearly out. Needs transfer from PGIMER today."),
            ("red",   "🔴 URGENT — Max Mohali",             "Stock at 22%. 720 units expiring in 18 days. Redistribute to Civil Mohali."),
            ("amber", "🟡 WARNING — GMCH-32 (CHD)",         "45% stock. 340 units expiring this month. Schedule redistribution."),
            ("amber", "🟡 WARNING — Alchemist Panchkula",   "54% stock. Ceftriaxone supply lower than safe level."),
            ("amber", "🟡 WARNING — Ivy Mohali Sec-71",     "40% stock. Amoxicillin running low. Watch closely."),
            ("blue",  "🔵 INFO — Fortis Mohali",            "Routine delivery done. 1,200 units Paracetamol received. Now at 91%."),
            ("blue",  "🔵 AI Alert",                        "Oseltamivir shortage predicted at 3 hospitals within 12 days."),
        ]:
            cls = {"red":"alert-red","amber":"alert-amber","blue":"alert-blue"}[lvl]
            st.markdown(f'<div class="{cls}"><b>{title}</b><br><span style="color:#455A64">{msg}</span></div>',
                        unsafe_allow_html=True)

    st.markdown("---")

    # ── Stock category bar + Transfers table ─────────────────────────────────
    col_bar, col_tbl = st.columns([1, 1], gap="medium")

    with col_bar:
        st.markdown('<div class="card-title">📊 Total Stock by Drug Type (All 10 Hospitals Combined)</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">Bar length = total units stored. Orange overlay = expiring soon. <b style="color:#C62828">Red bar</b> = critical — act now.</p>', unsafe_allow_html=True)
        bar_colors = ["#C62828" if c else "#1565C0" for c in inv_cat.Critical]
        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(x=inv_cat.Category, y=inv_cat["In Stock"],
            marker_color=bar_colors, name="Total in stock",
            text=[f"{v:,}" for v in inv_cat["In Stock"]], textposition="outside", textfont=dict(size=10),
            hovertemplate="<b>%{x}</b><br>In Stock: %{y:,} units<extra></extra>"))
        fig_cat.add_trace(go.Bar(x=inv_cat.Category, y=inv_cat["Expiring"],
            marker_color="#FF9800", opacity=.8, name="Expiring in 30 days",
            hovertemplate="<b>%{x}</b><br>Expiring: %{y:,} units<extra></extra>"))
        fig_cat.update_layout(**PL, barmode="overlay", height=280,
            yaxis_title="Number of Units", legend=dict(orientation="h", y=-0.3, font=dict(size=11)))
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_tbl:
        st.markdown('<div class="card-title">🚚 Latest Transfers — Moving Between Tri-City Hospitals</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">Each row = one drug shipment. Shows which hospital sent it, who receives it, and current status.</p>', unsafe_allow_html=True)
        show_df = transfers_df[["From","To","Medicine","Units","Status"]].head(6).copy()
        st.dataframe(show_df, use_container_width=True, hide_index=True, height=258)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SHORTAGE PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif "Shortage" in page:
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>📈 AI Shortage Predictor</h1>
            <p>AI studies past usage patterns and forecasts when medicines will run out — so we act before it's too late.</p>
        </div>
        <div class="live-badge">🤖 Model Accuracy: 94.7%</div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        sel_meds = st.multiselect("Pick medicines to view:",
            options=list(ts_df.columns), default=list(ts_df.columns[:3]))
    with c2:
        threshold = st.slider("Danger level (units)", 500, 6000, 2500, 250,
                              help="Below this = hospital is in trouble")
    with c3:
        show_hist = st.toggle("Show past 60 days?", value=True)

    if not sel_meds:
        st.warning("Please pick at least one medicine above.")
        st.stop()

    st.markdown(f"""
    <p class="explain">
        📖 <b>How to read this chart:</b>
        <b>Solid lines</b> = actual stock over the last 60 days.
        <b>Dashed lines</b> = AI prediction for the next 30 days.
        The <b style="color:#C62828">red shaded area</b> = danger zone (below {threshold:,} units).
        If a dashed line dips into the red zone, that medicine needs action <i>now</i>.
    </p>""", unsafe_allow_html=True)

    COLORS = ["#1565C0","#00838F","#E65100","#6A1B9A","#2E7D32"]
    fig_p = go.Figure()
    fig_p.add_hrect(y0=0, y1=threshold, fillcolor="rgba(198,40,40,.08)", line_width=0,
        annotation_text="⛔ DANGER ZONE — Act immediately if a line enters here",
        annotation_position="top left",
        annotation_font=dict(color="#C62828", size=11))
    fig_p.add_hline(y=threshold, line_dash="dot", line_color="#C62828", line_width=1.8,
        annotation_text=f"Danger level = {threshold:,} units",
        annotation_font_color="#C62828", annotation_font_size=11)

    for i, med in enumerate(sel_meds):
        c = COLORS[i % len(COLORS)]
        if show_hist:
            fig_p.add_trace(go.Scatter(x=ts_df.index, y=ts_df[med], mode="lines",
                line=dict(color=c, width=2), name=f"{med}  (actual)", legendgroup=med,
                hovertemplate="%{x|%d %b}<br>Actual stock: <b>%{y:,} units</b><extra></extra>"))
        fig_p.add_trace(go.Scatter(x=pr_df.index, y=pr_df[med], mode="lines",
            line=dict(color=c, width=2.5, dash="dash"),
            fill="tozeroy" if pr_df[med].min() < threshold else None,
            fillcolor="rgba(198,40,40,.07)",
            name=f"{med}  (AI forecast)", legendgroup=med,
            hovertemplate="%{x|%d %b}<br>AI forecast: <b>%{y:,} units</b><extra></extra>"))

    fig_p.add_vline(x=datetime.today().timestamp()*1000,
        line_dash="solid", line_color="#607D8B", line_width=1.2,
        annotation_text="Today ▶", annotation_font_color="#607D8B")
    fig_p.update_layout(**PL, height=400,
        title=dict(text="Stock Level Over Time  —  Dashed = AI Prediction", font=dict(size=13, color="#0A3D62")),
        xaxis_title="Date", yaxis_title="Units in storage", hovermode="x unified",
        legend=dict(orientation="h", y=-0.28, font=dict(size=11)))
    st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("---")
    col_r, col_h = st.columns([1, 1], gap="medium")

    with col_r:
        st.markdown('<div class="card-title">🎯 Which Medicines Are Most At Risk of Running Out?</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain"><b style="color:#C62828">Red</b> = act now &nbsp;|&nbsp; <b style="color:#F57F17">Orange</b> = watch closely &nbsp;|&nbsp; <b style="color:#2E7D32">Green</b> = safe for now.</p>', unsafe_allow_html=True)
        risk_rows = []
        for med in ts_df.columns:
            days_left = next((i for i, v in enumerate(pr_df[med]) if v < threshold), 30)
            score = max(0, 100 - int(days_left / 30 * 100))
            risk_rows.append({"Medicine": med, "Days until danger": days_left, "Risk Score": score})
        risk_df = pd.DataFrame(risk_rows).sort_values("Risk Score", ascending=False)
        fig_r = px.bar(risk_df, x="Risk Score", y="Medicine", orientation="h",
            color="Risk Score", color_continuous_scale=["#2E7D32","#F57F17","#C62828"],
            range_color=[0,100], text=risk_df["Risk Score"].astype(str)+"%",
            custom_data=["Days until danger"])
        fig_r.update_traces(textposition="outside",
            hovertemplate="<b>%{y}</b><br>Risk: %{x}%<br>Days until danger: %{customdata[0]}<extra></extra>")
        fig_r.update_layout(**PL, height=300, coloraxis_showscale=False,
            xaxis_title="Risk Score (0 = safe, 100 = critical)", xaxis_range=[0,115])
        st.plotly_chart(fig_r, use_container_width=True)

    with col_h:
        st.markdown('<div class="card-title">🏥 Hospital Stock Health — Tri-City View</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">Stock % = how full the medicine store is. Below 40% = critical. Sorted worst to best.</p>', unsafe_allow_html=True)
        hv = hospitals[["short","zone","stock_pct","expiring_30d","status"]].copy()
        hv.columns = ["Hospital","Zone","Stock Left %","Expiring (30d)","Health"]
        hv = hv.sort_values("Stock Left %")
        def _hl(val):
            if val == "Critical": return "background:#FFEBEE;color:#C62828;font-weight:600"
            if val == "Warning":  return "background:#FFF8E1;color:#E65100;font-weight:600"
            return "background:#E8F5E9;color:#2E7D32;font-weight:600"
        st.dataframe(hv.style.applymap(_hl, subset=["Health"])
            .background_gradient(subset=["Stock Left %"], cmap="RdYlGn", vmin=0, vmax=100),
            use_container_width=True, hide_index=True, height=280)

    st.markdown("---")
    st.markdown('<div class="card-title">✅ AI Recommended Actions (Next 72 Hours)</div>', unsafe_allow_html=True)
    st.markdown('<p class="explain">Based on the forecasts above, here is exactly what the AI recommends doing:</p>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    for i, (lvl, urg, title, desc) in enumerate([
        ("red",   "🔴 Do Today",   "Insulin Glargine → Civil Sec-22",     "Send 1,500 units from PGIMER. Stock hits zero in 4 days. Distance: ~3 km."),
        ("red",   "🔴 Do Today",   "Amoxicillin → Civil Mohali",          "Redistribute 720 expiring units from Max Mohali. 8 km drive, same-day possible."),
        ("red",   "🔴 Do Today",   "Civil Sec-22 — All medicines",        "Overall stock critically low. Activate emergency restock from GMSH-16."),
        ("amber", "🟡 This Week",  "Ceftriaxone → Alchemist Panchkula",   "Stock predicted to cross danger level in 12 days. Schedule transfer from PGIMER."),
        ("amber", "🟡 This Week",  "Amoxicillin — Ivy Mohali + GMCH-32",  "Usage rising. Raise joint purchase order by 20% for Mohali zone."),
        ("blue",  "🔵 Monitor",    "Metformin 850mg — All sites",         "Stable but trending up in usage. Review in 2 weeks."),
    ]):
        cls = {"red":"alert-red","amber":"alert-amber","blue":"alert-blue"}[lvl]
        col = a1 if i % 2 == 0 else a2
        with col:
            st.markdown(f'<div class="{cls}"><b>{urg}</b> · {title}<br>'
                        f'<span style="color:#455A64;font-size:.81rem">{desc}</span></div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REDISTRIBUTION HUB
# ══════════════════════════════════════════════════════════════════════════════
elif "Redistribution" in page:
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>🚚 Redistribution Hub</h1>
            <p>Track every drug shipment moving between Chandigarh · Mohali · Panchkula hospitals right now.</p>
        </div>
        <div class="live-badge"><span class="live-dot"></span> 18 Active Routes</div>
    </div>""", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🚛 Moving Now",    "9",  "in transit")
    k2.metric("✅ Arrived Today", "6",  "delivered")
    k3.metric("📦 Dispatched",   "2",  "leaving now")
    k4.metric("⚠️ Delayed",       "1",  "needs action", delta_color="inverse")
    st.markdown("")

    col_map2, col_feed = st.columns([1, 1], gap="medium")

    with col_map2:
        st.markdown('<div class="card-title">🗺️ Live Transfer Routes — Tri-City Map</div>', unsafe_allow_html=True)
        st.markdown("""
        <p class="explain">
            Each coloured line = one active transfer route.<br>
            🟢 Green = delivered &nbsp;|&nbsp; 🟡 Yellow = in transit &nbsp;|&nbsp;
            🔵 Blue = dispatched &nbsp;|&nbsp; 🔴 Red = delayed<br>
            Hover hospital dots for stock details.
        </p>""", unsafe_allow_html=True)

        s_clr = {
            "✅ Delivered": "#4CAF50",
            "🚛 In-Transit": "#FFC107",
            "📦 Dispatched": "#2196F3",
            "⚠️ Delayed":    "#F44336",
        }
        fig_rt = build_city_map(height=410, show_arcs=True, arc_pairs=True, status_colors=s_clr)

        # Add legend traces for transfer statuses
        for status, clr in s_clr.items():
            fig_rt.add_trace(go.Scattermapbox(
                lat=[None], lon=[None], mode="lines",
                line=dict(color=clr, width=3),
                name=status, showlegend=True,
            ))

        st.plotly_chart(fig_rt, use_container_width=True)

    with col_feed:
        st.markdown('<div class="card-title">📡 Live Transfer Feed — All 18 Shipments</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">Scroll inside the list. Card border colour matches the map line colour.</p>', unsafe_allow_html=True)

        icon_bg = {
            "✅ Delivered": "#F1F8E9", "🚛 In-Transit": "#FFFDE7",
            "📦 Dispatched": "#E3F2FD", "⚠️ Delayed": "#FFEBEE",
        }
        bdr_clr = {
            "✅ Delivered": "#4CAF50", "🚛 In-Transit": "#FFC107",
            "📦 Dispatched": "#2196F3", "⚠️ Delayed": "#F44336",
        }
        pri_clr = {"🔴 HIGH": "#C62828", "🟡 MED": "#E65100", "🔵 LOW": "#1565C0"}
        zone_icon = {"Chandigarh": "🏙️", "Mohali": "🌿", "Panchkula": "🏔️"}

        cards_html = ""
        for _, row in transfers_df.iterrows():
            bc  = bdr_clr.get(row.Status, "#90A4AE")
            bg  = icon_bg.get(row.Status, "#fff")
            pc  = pri_clr.get(row.Priority, "#607D8B")
            fz  = zone_icon.get(row["From Zone"], "")
            tz  = zone_icon.get(row["To Zone"], "")
            cards_html += f"""
            <div class="tx-card" style="border-left:4px solid {bc};background:{bg}">
                <div style="display:flex;justify-content:space-between;font-weight:700;
                            color:#0A3D62;font-size:.8rem">
                    <span>{row.ID}</span><span>{row.Status}</span>
                </div>
                <div style="color:#37474F;margin-top:2px;font-size:.8rem">
                    {fz} <b>{row.From}</b> &nbsp;→&nbsp; {tz} <b>{row.To}</b>
                </div>
                <div style="color:#607D8B;font-size:.76rem;margin-top:1px">
                    💊 {row.Medicine} &nbsp;·&nbsp; {row.Units:,} units
                    &nbsp;·&nbsp; ETA {row['ETA (hrs)']}h
                    &nbsp;·&nbsp; <span style="color:{pc};font-weight:600">{row.Priority}</span>
                </div>
            </div>"""

        st.markdown(
            f'<div style="height:390px;overflow-y:auto;padding-right:4px">{cards_html}</div>',
            unsafe_allow_html=True,
        )

    # Collapsible filter drawer
    st.markdown("")
    with st.expander("🔍 Search & filter all 18 transfers", expanded=False):
        f1, f2, f3 = st.columns(3)
        with f1:
            sf = st.multiselect("Status", list(transfers_df.Status.unique()),
                                default=list(transfers_df.Status.unique()))
        with f2:
            pf = st.multiselect("Priority", ["🔴 HIGH","🟡 MED","🔵 LOW"],
                                default=["🔴 HIGH","🟡 MED","🔵 LOW"])
        with f3:
            mf = st.text_input("Medicine contains…", "")
        filt = transfers_df[transfers_df.Status.isin(sf) & transfers_df.Priority.isin(pf)]
        if mf:
            filt = filt[filt.Medicine.str.contains(mf, case=False)]
        st.dataframe(
            filt[["ID","From","From Zone","To","To Zone","Medicine","Units","ETA (hrs)","Status","Priority"]],
            use_container_width=True, hide_index=True, height=260,
        )
        st.caption(f"Showing {len(filt)} of {len(transfers_df)} transfers")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — INVENTORY CHECK-IN
# ══════════════════════════════════════════════════════════════════════════════
elif "Inventory" in page:
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>📦 Inventory Check-in</h1>
            <p>Add new stock manually, or scan a drug label so the AI fills it in for you.</p>
        </div>
        <div class="live-badge">🔬 OCR Ready</div>
    </div>""", unsafe_allow_html=True)

    col_ocr, col_man = st.columns([1, 1], gap="medium")

    with col_ocr:
        st.markdown('<div class="card-title">📷 Scan a Drug Label (OCR)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert-blue" style="margin-bottom:14px">
            📋 <b>How it works:</b> Upload a photo of any medicine box or invoice.
            The AI reads the label and automatically pulls out the batch number,
            expiry date and quantity — no manual typing needed.
        </div>""", unsafe_allow_html=True)
        up = st.file_uploader("Upload a drug label or invoice image",
                              type=["png","jpg","jpeg","pdf"],
                              help="PNG, JPG or PDF — max 10 MB")
        if up:
            with st.spinner("🔬 Reading the label…"):
                time.sleep(1.8)
            batch  = f"BT-{random.randint(100000,999999)}"
            expiry = (datetime.today()+timedelta(days=random.randint(60,400))).strftime("%d/%m/%Y")
            qty    = random.randint(500, 5000)
            med    = random.choice(["Amoxicillin 500mg","Metformin 850mg","Ceftriaxone 1g","Paracetamol 650mg"])
            mfr    = random.choice(["Cipla Ltd.","Sun Pharma","Dr. Reddy's","Lupin Ltd."])
            conf   = random.randint(92, 99)
            st.success(f"✅ Label scanned — {up.name}")
            st.markdown(f"""
            <div class="card" style="border-left:4px solid #00838F">
                <div class="card-title">🔍 What the AI found on the label:</div>
                <table style="width:100%;font-size:.84rem;border-collapse:collapse">
                    <tr><td style="color:#607D8B;padding:5px 0;width:38%">Medicine</td><td><b>{med}</b></td></tr>
                    <tr><td style="color:#607D8B;padding:5px 0">Batch Number</td>
                        <td><code style="background:#F0F4F8;padding:1px 6px;border-radius:4px">{batch}</code></td></tr>
                    <tr><td style="color:#607D8B;padding:5px 0">Expiry Date</td>
                        <td><b style="color:#E65100">{expiry}</b></td></tr>
                    <tr><td style="color:#607D8B;padding:5px 0">Quantity</td><td><b>{qty:,} units</b></td></tr>
                    <tr><td style="color:#607D8B;padding:5px 0">Manufacturer</td><td>{mfr}</td></tr>
                    <tr><td style="color:#607D8B;padding:5px 0">AI Confidence</td>
                        <td><b style="color:#2E7D32">{conf}% accurate</b></td></tr>
                </table>
            </div>""", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✅ Save to Inventory", use_container_width=True, type="primary"):
                    st.toast("✅ Inventory updated!", icon="✅")
            with b2:
                if st.button("✏️ Edit First", use_container_width=True):
                    st.toast("Opening editor…", icon="✏️")
        else:
            st.markdown("""
            <div style="text-align:center;padding:44px 20px;color:#90A4AE;
                        border:2px dashed #DDE5EF;border-radius:12px;background:#FAFCFF">
                <div style="font-size:2.8rem;margin-bottom:10px">🔬</div>
                <b>No image uploaded yet</b><br>
                <span style="font-size:.8rem">Drag &amp; drop a drug label, invoice or batch sheet above</span>
            </div>""", unsafe_allow_html=True)

    with col_man:
        st.markdown('<div class="card-title">✏️ Add Stock Manually</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">Fill in the fields to log a new medicine delivery.</p>', unsafe_allow_html=True)
        with st.form("manual_entry", clear_on_submit=True):
            hosp_sel = st.selectbox("Which hospital is receiving this?", hospitals.name.tolist())
            med_sel  = st.selectbox("Medicine name", [
                "Amoxicillin 500mg","Metformin 850mg","Atorvastatin 40mg",
                "Paracetamol 650mg","Insulin Glargine","Ceftriaxone 1g",
                "Oseltamivir 75mg","Hydroxychloroquine 200mg"])
            batch_in = st.text_input("Batch number (from the box)", placeholder="e.g. BT-123456")
            q1, q2 = st.columns(2)
            with q1: qty_in = st.number_input("How many units?", min_value=1, max_value=100000, value=1000, step=100)
            with q2: exp_in = st.date_input("Expiry date", min_value=datetime.today())
            supplier_in = st.text_input("Supplier name", placeholder="e.g. Cipla Ltd.")
            storage_in  = st.selectbox("Storage type", ["Normal (room temp)","Cold Chain (2–8°C)","Frozen (-20°C)"])
            notes_in    = st.text_area("Notes", height=68, placeholder="Any special instructions…")
            submitted = st.form_submit_button("📦 Save to Inventory", use_container_width=True, type="primary")
            if submitted:
                if not batch_in:
                    st.error("Please enter a batch number — required for tracking.")
                else:
                    st.toast(f"✅ {qty_in:,} units of {med_sel} added to {hosp_sel.split(' ')[0]}!", icon="📦")
                    st.success("Saved! Entry pending supervisor approval.")

    st.markdown("---")
    col_i1, col_i2 = st.columns([1, 1], gap="medium")

    with col_i1:
        st.markdown('<div class="card-title">📊 How Full is Each Hospital\'s Stock Room?</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">100% = fully stocked. <b style="color:#C62828">Red</b> = below 40% = critical. <b style="color:#F57F17">Orange</b> = 40–65% = watch closely.</p>', unsafe_allow_html=True)
        sh = hospitals.sort_values("stock_pct")
        clrs = ["#C62828" if v<40 else "#F57F17" if v<65 else "#1565C0" for v in sh.stock_pct]
        fig_h = go.Figure(go.Bar(
            x=sh.stock_pct, y=sh.short, orientation="h",
            marker_color=clrs,
            text=[f"{v}%" for v in sh.stock_pct],
            textposition="outside",
            customdata=sh.zone,
            hovertemplate="<b>%{y}</b> (%{customdata})<br>Stock: %{x}%<extra></extra>",
        ))
        fig_h.add_vline(x=40, line_dash="dot", line_color="#C62828",
            annotation_text="Critical (40%)", annotation_font_color="#C62828", annotation_font_size=10)
        fig_h.add_vline(x=65, line_dash="dot", line_color="#F57F17",
            annotation_text="Warning (65%)", annotation_font_color="#F57F17", annotation_font_size=10)
        fig_h.update_layout(**PL, height=340, xaxis_title="Stock Remaining (%)", xaxis_range=[0,115])
        st.plotly_chart(fig_h, use_container_width=True)

    with col_i2:
        st.markdown('<div class="card-title">⏳ Which Hospitals Have the Most Medicine Expiring Soon?</div>', unsafe_allow_html=True)
        st.markdown('<p class="explain">High number = lots of medicine expiring in 30 days. Act on the longest bars to avoid wastage.</p>', unsafe_allow_html=True)
        sh2 = hospitals.sort_values("expiring_30d", ascending=False)
        fig_e = go.Figure(go.Bar(
            y=sh2.short, x=sh2.expiring_30d, orientation="h",
            marker=dict(
                color=sh2.expiring_30d,
                colorscale=[[0,"#C8E6C9"],[0.5,"#FFE082"],[1,"#EF9A9A"]],
                showscale=True, colorbar=dict(title="Units", thickness=12, len=.8),
            ),
            text=sh2.expiring_30d, textposition="outside",
            customdata=sh2.zone,
            hovertemplate="<b>%{y}</b> (%{customdata})<br>Expiring: %{x:,} units<extra></extra>",
        ))
        fig_e.update_layout(**PL, height=340, xaxis_title="Units Expiring in Next 30 Days")
        st.plotly_chart(fig_e, use_container_width=True)

    st.markdown('<div class="card-title">🕐 Recent Check-in History</div>', unsafe_allow_html=True)
    st.markdown('<p class="explain">Last 12 stock entries added to the system.</p>', unsafe_allow_html=True)
    log = []
    for _ in range(12):
        ts = datetime.now() - timedelta(hours=random.randint(0,48), minutes=random.randint(0,59))
        log.append({
            "When":     ts.strftime("%d %b  %H:%M"),
            "Hospital": random.choice(hospitals.short.tolist()),
            "Zone":     random.choice(["Chandigarh","Mohali","Panchkula"]),
            "Medicine": random.choice(["Amoxicillin 500mg","Metformin 850mg","Insulin Glargine","Ceftriaxone 1g"]),
            "Added":    f"{random.randint(200,5000):,} units",
            "How":      random.choice(["📷 OCR Scan","✏️ Manual","🔄 EDI Import"]),
            "Verified": random.choice(["✅ Yes","⏳ Pending","✅ Yes","✅ Yes"]),
        })
    st.dataframe(pd.DataFrame(log).sort_values("When", ascending=False),
                 use_container_width=True, hide_index=True, height=300)
