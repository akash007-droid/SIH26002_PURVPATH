import base64
from pathlib import Path

import streamlit as st

from config.settings import APP_NAME, APP_ICON

_LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "purv_path_logo.jpeg"
try:
    _LOGO_B64 = base64.b64encode(_LOGO_PATH.read_bytes()).decode("ascii")
    _LOGO_HTML = f'<img src="data:image/jpeg;base64,{_LOGO_B64}" alt="Purv Path logo" />'
except Exception:
    _LOGO_HTML = "<span>✦</span>"


def inject_theme():
    """Premium SIH-style visual system shared by all pages."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --pp-bg: #07111f;
            --pp-panel: rgba(15, 30, 48, .82);
            --pp-panel-2: rgba(18, 38, 58, .72);
            --pp-border: rgba(125, 211, 252, .16);
            --pp-text: #e7f6ff;
            --pp-muted: #91a9bb;
            --pp-cyan: #39d5ff;
            --pp-green: #55e6a5;
            --pp-amber: #ffbd59;
            --pp-red: #ff5f6d;
        }

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        /* Keep Streamlit itself in the same dark visual language as पूर्वपथ. */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #06101d !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 8%, rgba(57,213,255,.11), transparent 25%),
                radial-gradient(circle at 92% 12%, rgba(85,230,165,.08), transparent 22%),
                linear-gradient(135deg, #06101d 0%, #091827 48%, #06111d 100%);
            color: var(--pp-text);
        }

        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: rgba(5, 14, 25, .96);
            border-right: 1px solid var(--pp-border);
        }

        h1, h2, h3, .pp-title {
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -.025em;
        }

        .pp-topbar {
            display:flex; align-items:center; justify-content:space-between;
            padding: 0 0 1.15rem 0;
        }
        .pp-brand {
            display:flex; align-items:center; gap:.8rem;
        }
        .pp-logo {
            width:42px; height:42px; display:grid; place-items:center;
            border-radius:13px;
            background: linear-gradient(135deg, rgba(57,213,255,.22), rgba(85,230,165,.16));
            border:1px solid rgba(57,213,255,.35);
            box-shadow: 0 0 28px rgba(57,213,255,.10);
            font-size: 1.25rem;
        }
        .pp-brand-name { font-size:1.25rem; font-weight:700; color:#fff; }
        .pp-brand-sub { font-size:.72rem; color:var(--pp-muted); margin-top:2px; }

        .pp-live {
            display:inline-flex; align-items:center; gap:.5rem;
            padding:.42rem .75rem; border-radius:999px;
            border:1px solid rgba(85,230,165,.22);
            background:rgba(85,230,165,.07); color:#b9f8d9;
            font-size:.72rem; font-weight:600;
        }
        .pp-dot {
            width:7px; height:7px; border-radius:50%;
            background:var(--pp-green); box-shadow:0 0 10px var(--pp-green);
            animation: ppPulse 1.7s infinite;
        }
        @keyframes ppPulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.45;transform:scale(.72)} }

        .pp-emergency {
            position:relative; overflow:hidden;
            padding:1rem 1.2rem; border-radius:16px;
            background:linear-gradient(100deg, rgba(255,95,109,.12), rgba(255,189,89,.08));
            border:1px solid rgba(255,95,109,.30);
            box-shadow:0 12px 38px rgba(255,95,109,.06);
        }
        .pp-emergency:after {
            content:""; position:absolute; width:160px; height:160px; right:-80px; top:-90px;
            border-radius:50%; background:rgba(255,95,109,.12); filter:blur(12px);
        }
        .pp-emergency-label { color:#ff8f99; font-size:.7rem; text-transform:uppercase; letter-spacing:.12em; font-weight:700; }
        .pp-emergency-text { color:#fff; font-size:1rem; font-weight:600; margin-top:.2rem; }

        .pp-card {
            background:linear-gradient(145deg, rgba(17,35,54,.90), rgba(8,22,36,.80));
            border:1px solid var(--pp-border); border-radius:18px;
            padding:1.15rem; box-shadow:0 12px 42px rgba(0,0,0,.20);
            transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
        }
        .pp-card:hover {
            transform:translateY(-3px); border-color:rgba(57,213,255,.34);
            box-shadow:0 18px 52px rgba(0,0,0,.30);
        }

        .pp-kpi-label { color:var(--pp-muted); font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; }
        .pp-kpi-value { color:#fff; font-family:'Space Grotesk'; font-size:1.7rem; font-weight:700; margin-top:.25rem; }
        .pp-kpi-note { color:#79dcb4; font-size:.72rem; margin-top:.18rem; }

        .pp-section {
            display:flex; align-items:end; justify-content:space-between;
            margin:1.3rem 0 .75rem;
        }
        .pp-section-title { font-family:'Space Grotesk'; font-size:1.02rem; font-weight:700; color:#fff; }
        .pp-section-sub { font-size:.72rem; color:var(--pp-muted); }

        .pp-climate {
            min-height:160px;
            background:
              radial-gradient(circle at 82% 20%, rgba(57,213,255,.13), transparent 24%),
              linear-gradient(145deg, rgba(14,39,58,.94), rgba(7,22,37,.82));
        }
        .pp-weather-icon { font-size:2.1rem; }
        .pp-temp { font-family:'Space Grotesk'; font-size:2.6rem; font-weight:700; color:#fff; line-height:1; }
        .pp-weather-row { display:flex; gap:1.4rem; margin-top:1rem; }
        .pp-weather-item small { color:var(--pp-muted); display:block; font-size:.65rem; }
        .pp-weather-item b { color:#dff7ff; font-size:.83rem; }

        .pp-nav-card {
            display:flex; align-items:center; gap:.8rem; padding:.82rem .9rem;
            border-radius:13px; border:1px solid rgba(125,211,252,.10);
            background:rgba(10,27,43,.62); margin-bottom:.55rem;
        }
        .pp-nav-icon { width:34px; height:34px; display:grid; place-items:center; border-radius:10px; background:rgba(57,213,255,.08); }
        .pp-nav-title { color:#f2fbff; font-weight:600; font-size:.84rem; }
        .pp-nav-desc { color:var(--pp-muted); font-size:.67rem; margin-top:2px; }

        .pp-map-preview {
            min-height:365px; position:relative; overflow:hidden;
            border-radius:18px; border:1px solid var(--pp-border);
            background:
              linear-gradient(rgba(57,213,255,.035) 1px, transparent 1px),
              linear-gradient(90deg, rgba(57,213,255,.035) 1px, transparent 1px),
              radial-gradient(circle at 55% 48%, rgba(57,213,255,.12), transparent 23%),
              #071725;
            background-size:34px 34px,34px 34px,auto,auto;
        }
        .pp-map-preview:before {
            content:""; position:absolute; inset:0;
            background:linear-gradient(120deg, transparent 46%, rgba(57,213,255,.07) 47%, transparent 48%),
                       linear-gradient(35deg, transparent 56%, rgba(85,230,165,.06) 57%, transparent 58%);
        }
        .pp-map-title { position:absolute; left:1rem; top:1rem; z-index:3; }
        .pp-map-title b { color:#fff; font-family:'Space Grotesk'; }
        .pp-map-title span { display:block; color:var(--pp-muted); font-size:.7rem; margin-top:3px; }
        .pp-node {
            position:absolute; width:12px; height:12px; border-radius:50%; z-index:2;
            background:var(--pp-green); box-shadow:0 0 18px rgba(85,230,165,.85);
            animation:ppFloat 2.8s ease-in-out infinite;
        }
        .pp-node.red { background:var(--pp-red); box-shadow:0 0 18px rgba(255,95,109,.9); }
        .pp-node.amber { background:var(--pp-amber); box-shadow:0 0 18px rgba(255,189,89,.85); }
        .pp-route { position:absolute; height:2px; transform-origin:left center; z-index:1; opacity:.75; background:linear-gradient(90deg,var(--pp-cyan),transparent); }
        .pp-map-legend { position:absolute; right:1rem; bottom:1rem; display:flex; gap:.8rem; z-index:3; padding:.55rem .7rem; border-radius:10px; background:rgba(5,16,27,.78); border:1px solid rgba(125,211,252,.10); font-size:.65rem; color:var(--pp-muted); }
        .pp-legend-dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:4px; }
        @keyframes ppFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }

        .stButton > button, .stPageLink > a {
            border-radius:10px !important; border:1px solid rgba(57,213,255,.18) !important;
            background:rgba(15,40,59,.70) !important; color:#dff8ff !important;
            font-weight:600 !important; transition:all .2s ease !important;
        }
        .stButton > button:hover, .stPageLink > a:hover {
            border-color:rgba(57,213,255,.55) !important;
            box-shadow:0 0 20px rgba(57,213,255,.10) !important;
            transform:translateY(-1px);
        }
        [data-testid="stMetric"] {
            background:rgba(12,29,45,.65); border:1px solid rgba(125,211,252,.10);
            padding:.7rem .85rem; border-radius:13px;
        }
        div[data-testid="stDataFrame"] { border:1px solid rgba(125,211,252,.10); border-radius:12px; overflow:hidden; }

        /* -----------------------------------------------------------------
           Reference dashboard layout
           ----------------------------------------------------------------- */
        .block-container { max-width: 100% !important; width:100% !important; padding: .45rem 1.35rem 2rem !important; box-sizing:border-box; }
        [data-testid="stSidebar"] { display:none !important; }
        .pp-dashboard-header { height:72px; display:flex; align-items:center; justify-content:space-between; gap:1.1rem; border-bottom:1px solid rgba(57,213,255,.12); margin-bottom:1.35rem; }
        .pp-shared-header { margin-bottom:.65rem !important; }
        .pp-shared-header-note { color:#789db2; font-size:.76rem; text-align:right; }
        .pp-shared-header-rule { height:1px; background:rgba(57,213,255,.12); margin:.15rem 0 1.25rem; }
        .pp-page-subtitle { color:#91a9bb; margin-top:-.55rem; margin-bottom:1rem; font-size:.88rem; line-height:1.5; }

        .pp-dashboard-brand { display:flex; align-items:center; min-width:285px; gap:.72rem; }
        .pp-brand-mark { width:54px; height:54px; display:grid; place-items:center; border-radius:14px; overflow:hidden; background:#061827; border:1px solid rgba(57,213,255,.28); box-shadow:0 0 25px rgba(57,213,255,.10); flex:0 0 54px; }
        .pp-brand-mark img { width:100%; height:100%; object-fit:cover; display:block; }
        .pp-dashboard-name { font:700 1.18rem/1.1 'DM Sans', sans-serif; color:#e8fbff; white-space:nowrap; }
        .pp-dashboard-tagline { margin-top:.27rem; font-size:.65rem; color:#39c9f4; }
        .pp-top-navigation { display:flex; align-self:stretch; align-items:center; gap:1.55rem; }
        .pp-top-nav { height:100%; display:flex; align-items:center; color:#8eabc0; font-size:.76rem; border-bottom:3px solid transparent; white-space:nowrap; }
        .pp-top-nav.active { color:#54ddff; border-bottom-color:#24d8f1; }
        .pp-header-actions { display:flex; align-items:center; gap:.75rem; min-width:280px; justify-content:flex-end; }
        .pp-bell { position:relative; color:#d9f6ff; font-size:1.15rem; }
        .pp-bell i { position:absolute; right:-9px; top:-8px; width:17px; height:17px; border-radius:50%; display:grid; place-items:center; background:#ef3e59; color:white; font:700 .58rem 'DM Sans'; font-style:normal; }
        .pp-help { display:flex; align-items:center; gap:.55rem; color:#fff; text-decoration:none; padding:.52rem .78rem; border-radius:24px; background:linear-gradient(100deg,#b82035,#e84051); box-shadow:0 0 22px rgba(235,57,78,.2); font-size:.78rem; }
        .pp-help span { font-size:.6rem; line-height:1.25; color:#ffe9eb; } .pp-help b { color:#fff; font-size:.7rem; }
        .pp-avatar { width:39px; height:39px; border-radius:50%; display:grid; place-items:center; color:#39d5ff; background:rgba(21,100,130,.45); border:1px solid rgba(57,213,255,.25); }
        .pp-panel { background:linear-gradient(145deg,rgba(7,28,47,.96),rgba(5,20,35,.91)); border:1px solid rgba(57,213,255,.14); border-radius:17px; }
        .pp-input-panel, .pp-output-panel { border-bottom-left-radius:0; border-bottom-right-radius:0; border-bottom:0; }
        .pp-panel-heading { display:flex; align-items:center; gap:.7rem; }
        .pp-panel-icon { width:38px; height:38px; display:grid; place-items:center; border-radius:50%; background:radial-gradient(circle,rgba(57,213,255,.25),rgba(57,213,255,.04)); border:1px solid rgba(57,213,255,.18); color:#baf3ff; font-size:1.1rem; box-shadow:0 0 20px rgba(57,213,255,.12); }
        .pp-panel-title { color:#c5f2ff; font:700 1.1rem 'Space Grotesk'; }
        .pp-panel-sub { color:#789db2; font-size:.67rem; margin-top:.2rem; }
        .pp-input-panel { padding:1.15rem 1.25rem .25rem; border:0; background:transparent; box-shadow:none; }
        .pp-output-panel { padding:1.15rem 1.25rem .45rem; border:0; background:transparent; box-shadow:none; }

        /* The Streamlit widgets sit beside the HTML header blocks.  Give the
           whole column the visual panel so the header, controls, cards and
           results share one clean boundary. */
        div[data-testid="column"]:has(.pp-input-panel),
        div[data-testid="column"]:has(.pp-output-panel) {
            border:1px solid rgba(57,213,255,.14);
            border-radius:17px;
            background:linear-gradient(145deg,rgba(7,28,47,.96),rgba(5,20,35,.91));
            box-sizing:border-box;
            overflow:hidden;
            min-width:0;
        }
        div[data-testid="column"]:has(.pp-input-panel) > div,
        div[data-testid="column"]:has(.pp-output-panel) > div {
            padding-left:0 !important;
            padding-right:0 !important;
        }
        div[data-testid="column"]:has(.pp-input-panel) [data-testid="stTextInput"],
        div[data-testid="column"]:has(.pp-input-panel) [data-testid="stButton"],
        div[data-testid="column"]:has(.pp-output-panel) [data-testid="stButton"] {
            box-sizing:border-box;
        }
        .pp-output-heading { display:flex; align-items:center; justify-content:space-between; }
        .pp-contact { color:#bcefff; background:rgba(19,80,110,.34); border:1px solid rgba(57,213,255,.16); padding:.53rem .75rem; border-radius:20px; text-decoration:none; font-size:.68rem; font-weight:700; }
        .pp-location-stats { display:grid; grid-template-columns:1fr 1fr 1.1fr; gap:.72rem; margin:.55rem 0 .95rem; }
        .pp-location-stat { min-height:57px; padding:.62rem .72rem; border:1px solid rgba(57,213,255,.13); border-radius:10px; background:rgba(8,30,49,.72); display:grid; grid-template-columns:22px 1fr; column-gap:.35rem; align-items:center; }
        .pp-location-stat span { grid-row:span 2; color:#20dfbd; font-size:1rem; } .pp-location-stat small { color:#8ba8ba; font-size:.59rem; } .pp-location-stat b { color:#43e5cc; font-size:.71rem; }
        .pp-location-stat.detected span { color:#8b83ff; } .pp-location-stat.detected b { color:#75a7ff; }
        .pp-query-heading { display:flex; gap:.65rem; align-items:center; border-top:1px solid rgba(57,213,255,.08); padding:1rem 0 .55rem; }
        .pp-query-icon { width:37px; height:37px; border-radius:10px; display:grid; place-items:center; color:#c5f3ff; background:rgba(24,130,177,.18); border:1px solid rgba(57,213,255,.14); }
        .pp-query-row { min-height:57px; display:flex; align-items:center; gap:.7rem; margin:.38rem 0; padding:.45rem .65rem; border:1px solid rgba(57,213,255,.10); border-radius:10px; background:rgba(6,26,43,.66); box-sizing:border-box; width:100%; }
        .pp-query-icon-small { width:34px; height:34px; flex:0 0 34px; display:grid; place-items:center; border-radius:50%; color:#c8f6ff; background:rgba(22,111,150,.24); border:1px solid rgba(57,213,255,.16); font-size:.92rem; }
        .pp-query-title { color:#c6edfa; font-size:.75rem; font-weight:700; } .pp-query-desc { color:#7394a9; font-size:.61rem; margin-top:.16rem; }
        div[data-testid="stPageLink"] { height:57px; display:flex; align-items:center; justify-content:center; margin:.38rem 0; }
        div[data-testid="stPageLink"] a { width:100%; min-height:57px !important; padding:0 !important; border:0 !important; background:transparent !important; box-shadow:none !important; color:#8adff8 !important; font-size:1.25rem !important; }
        div[data-testid="stPageLink"] a:hover { transform:none !important; color:#fff !important; }
        .pp-audio-box { margin-top:.85rem; padding:.78rem .9rem; border-radius:15px; display:flex; align-items:center; gap:.65rem; background:linear-gradient(100deg,rgba(54,42,179,.55),rgba(11,166,147,.62)); border:1px solid rgba(94,224,255,.24); }
        .pp-audio-icon { width:35px; height:35px; display:grid; place-items:center; border-radius:50%; background:rgba(88,69,255,.7); color:white; font-size:1.05rem; } .pp-audio-box b { color:#e9faff; font-size:.75rem; display:block; } .pp-audio-box small { color:#a8d4e5; font-size:.6rem; display:block; margin-top:.12rem; }
        .pp-audio-action { margin-left:auto; padding:.55rem .8rem; border-radius:14px; background:linear-gradient(90deg,#15a8ff,#15c998); color:white; font-size:.67rem; font-weight:700; }
        .pp-output-card { min-height:88px; padding:.72rem .75rem; border-radius:13px; border:1px solid rgba(80,180,255,.18); margin:.25rem 0 .65rem; background:rgba(9,29,49,.82); display:flex; flex-direction:column; gap:.15rem; }
        .pp-output-card small { color:#c6e6f5; font-size:.6rem; } .pp-output-card strong { font:700 1.35rem 'Space Grotesk'; color:#c8f4ff; } .pp-output-card span { color:#83a5b7; font-size:.58rem; }
        .pp-output-card.amber { border-color:rgba(255,189,89,.25); } .pp-output-card.amber strong { color:#ffda76; }
        .pp-output-card.red { border-color:rgba(255,95,109,.25); } .pp-output-card.red strong { color:#ff6876; }
        .pp-output-card.green { border-color:rgba(41,219,177,.25); } .pp-output-card.green strong { color:#66ebd0; }
        .pp-map-wrap { position:relative; overflow:hidden; border:1px solid rgba(57,213,255,.16); border-radius:14px; background:#061823; }
        .pp-map-wrap iframe { border-radius:13px !important; filter:saturate(.82) brightness(.72) hue-rotate(155deg); }
        .pp-map-overlay { position:absolute; z-index:5; top:.65rem; left:.65rem; padding:.58rem .72rem; border-radius:9px; background:rgba(3,21,34,.85); border:1px solid rgba(57,213,255,.12); pointer-events:none; }
        .pp-map-overlay b { display:block; color:#e8fbff; font-size:.67rem; } .pp-map-overlay span { color:#78a4b9; font-size:.57rem; }
        .pp-ai-result { margin-top:.75rem; display:flex; gap:.72rem; padding:.85rem .9rem; border:1px solid rgba(57,213,255,.20); border-radius:13px; background:rgba(6,31,51,.72); }
        .pp-ai-badge { width:35px; height:35px; flex:0 0 35px; display:grid; place-items:center; border-radius:50%; background:linear-gradient(145deg,#15a8ff,#0d72bb); color:white; font-weight:800; }
        .pp-ai-result b { color:#bfefff; font-size:.73rem; } .pp-ai-result p { color:#86b2c6; font-size:.62rem; line-height:1.55; margin:.25rem 0 0; } .pp-ai-result strong { color:#b9e9f8; } .pp-ai-result mark { color:#ffd35b; background:rgba(255,189,89,.14); border:1px solid rgba(255,189,89,.2); border-radius:8px; padding:.1rem .28rem; }
        .pp-enhance-box { margin-top:.55rem; display:flex; gap:.65rem; align-items:center; padding:.72rem .9rem; border-radius:13px; border:1px solid #19c9ee; background:linear-gradient(90deg,rgba(10,89,132,.5),rgba(5,57,81,.52)); box-shadow:0 0 20px rgba(25,201,238,.08); }
        .pp-enhance-icon { color:#c9f7ff; font-size:1.35rem; } .pp-enhance-box b { color:#61e6ff; font-size:.7rem; display:block; } .pp-enhance-box small { color:#75a9bd; font-size:.57rem; display:block; margin-top:.1rem; }
        .pp-prompt-bar { display:flex; align-items:center; min-height:78px; margin-top:1.3rem; padding:.8rem 1.2rem; border:1px solid rgba(57,213,255,.11); border-radius:16px 16px 0 0; background:rgba(5,24,40,.82); }
        .pp-prompt-label { display:flex; gap:.65rem; align-items:center; } .pp-prompt-icon { width:35px; height:35px; border-radius:50%; display:grid; place-items:center; background:rgba(22,115,173,.25); color:#8ce8ff; } .pp-prompt-label b { color:#44ddff; font-size:.8rem; display:block; } .pp-prompt-label small { color:#789db1; font-size:.58rem; display:block; margin-top:.12rem; }
        .pp-prompt-bar + div [data-testid="stTextInput"] { margin-top:-78px; margin-left:44%; width:52%; position:relative; z-index:3; }
        .pp-prompt-bar + div [data-testid="stTextInput"] input { height:47px !important; }
        [data-testid="stTextInput"] input { background:rgba(7,31,50,.88) !important; border:1px solid rgba(57,213,255,.18) !important; color:#cdeef8 !important; border-radius:11px !important; font-size:.68rem !important; }
        [data-testid="stTextInput"] label { color:#7296aa !important; }
        .pp-input-panel + div [data-testid="stButton"] button { height:40px !important; font-size:.65rem !important; }
        @media (max-width:1100px) { .pp-top-navigation { gap:.7rem; } .pp-top-nav { font-size:.65rem; } .pp-dashboard-brand{min-width:220px}.pp-header-actions{min-width:230px} }
        @media (max-width:850px) { .pp-dashboard-header{height:auto; padding:.7rem 0; flex-wrap:wrap}.pp-top-navigation{order:3;width:100%;justify-content:space-between}.pp-header-actions{min-width:auto}.pp-dashboard-brand{min-width:auto}.pp-map-wrap iframe{height:420px !important} }


        /* -----------------------------------------------------------------
           Readability / alignment pass
           ----------------------------------------------------------------- */
        .block-container {
            max-width: 1600px !important;
            width: 100% !important;
            margin: 0 auto !important;
            padding: 1rem 1.75rem 2.5rem !important;
        }

        .pp-dashboard-header {
            height: 92px !important;
            margin-bottom: 1.45rem !important;
            gap: 1.5rem !important;
        }
        .pp-dashboard-brand {
            min-width: 330px !important;
            gap: .9rem !important;
        }
        .pp-brand-mark {
            width: 58px !important;
            height: 58px !important;
            border-radius: 16px !important;
            font-size: 1.45rem !important;
        }
        .pp-dashboard-name {
            font-size: 1.72rem !important;
        }
        .pp-dashboard-tagline {
            font-size: .76rem !important;
        }
        .pp-top-navigation {
            gap: 1.7rem !important;
        }
        .pp-top-nav {
            font-size: .9rem !important;
        }
        .pp-header-actions {
            min-width: 320px !important;
            gap: .9rem !important;
        }
        .pp-bell {
            font-size: 1.35rem !important;
        }
        .pp-help {
            font-size: .82rem !important;
            padding: .62rem .9rem !important;
        }
        .pp-help span { font-size: .68rem !important; }
        .pp-help b { font-size: .78rem !important; }
        .pp-avatar {
            width: 45px !important;
            height: 45px !important;
        }

        /* The two main columns are equal, padded cards rather than narrow
           content floating inside a full-width column. */
        div[data-testid="column"]:has(.pp-input-panel),
        div[data-testid="column"]:has(.pp-output-panel) {
            padding: 0 !important;
            min-width: 0 !important;
            align-self: stretch !important;
        }
        div[data-testid="column"]:has(.pp-input-panel) > div,
        div[data-testid="column"]:has(.pp-output-panel) > div {
            padding: 0 1.15rem 1.15rem !important;
            min-width: 0 !important;
        }
        .pp-input-panel,
        .pp-output-panel {
            padding: 1.15rem 0 .35rem !important;
        }

        .pp-panel-title {
            font-size: 1.18rem !important;
        }
        .pp-panel-sub {
            font-size: .75rem !important;
        }
        .pp-panel-icon {
            width: 44px !important;
            height: 44px !important;
            font-size: 1.25rem !important;
        }

        [data-testid="stTextInput"] input {
            height: 46px !important;
            min-height: 46px !important;
            font-size: .82rem !important;
            padding: 0 .9rem !important;
        }
        .pp-input-panel + div [data-testid="stButton"] button,
        div[data-testid="column"]:has(.pp-input-panel) [data-testid="stButton"] button {
            height: 46px !important;
            min-height: 46px !important;
            font-size: .78rem !important;
        }

        .pp-location-stats {
            gap: .85rem !important;
            margin: .7rem 0 1rem !important;
        }
        .pp-location-stat {
            min-height: 68px !important;
            padding: .75rem .85rem !important;
        }
        .pp-location-stat small {
            font-size: .68rem !important;
        }
        .pp-location-stat b {
            font-size: .82rem !important;
        }

        .pp-query-heading {
            padding: 1.1rem 0 .7rem !important;
        }
        .pp-query-heading .pp-panel-title {
            font-size: 1.1rem !important;
        }
        .pp-query-row {
            min-height: 64px !important;
            margin: .42rem 0 !important;
            padding: .55rem .8rem !important;
        }
        .pp-query-icon-small {
            width: 40px !important;
            height: 40px !important;
            flex-basis: 40px !important;
            font-size: 1rem !important;
        }
        .pp-query-title {
            font-size: .84rem !important;
        }
        .pp-query-desc {
            font-size: .68rem !important;
        }
        div[data-testid="stPageLink"] {
            height: 64px !important;
            margin: .42rem 0 !important;
        }
        div[data-testid="stPageLink"] a {
            min-height: 64px !important;
            font-size: 1.35rem !important;
        }

        .pp-audio-box {
            margin-top: 1rem !important;
            min-height: 64px !important;
            padding: .8rem 1rem !important;
        }
        .pp-audio-box b { font-size: .82rem !important; }
        .pp-audio-box small { font-size: .67rem !important; }
        .pp-audio-action { font-size: .72rem !important; }

        .pp-output-card {
            min-height: 92px !important;
            padding: .8rem .85rem !important;
        }
        .pp-output-card small { font-size: .67rem !important; }
        .pp-output-card strong { font-size: 1.45rem !important; }
        .pp-output-card span { font-size: .64rem !important; }

        .pp-map-wrap iframe {
            min-height: 360px !important;
        }
        .pp-map-overlay {
            padding: .65rem .8rem !important;
        }
        .pp-map-overlay b { font-size: .74rem !important; }
        .pp-map-overlay span { font-size: .63rem !important; }

        .pp-ai-result {
            margin-top: .8rem !important;
            padding: .9rem 1rem !important;
        }
        .pp-ai-result b { font-size: .8rem !important; }
        .pp-ai-result p {
            font-size: .68rem !important;
            line-height: 1.6 !important;
        }
        .pp-enhance-box {
            padding: .8rem 1rem !important;
        }
        .pp-enhance-box b { font-size: .76rem !important; }
        .pp-enhance-box small { font-size: .63rem !important; }

        /* Prompt is a normal aligned row; never overlap the input using
           negative margins. */
        .pp-prompt-label-inline {
            min-height: 48px;
            display: flex !important;
            align-items: center !important;
            gap: .7rem !important;
        }
        .pp-prompt-label-inline .pp-prompt-icon {
            flex: 0 0 38px;
        }
        .pp-prompt-label-inline b { font-size: .86rem !important; }
        .pp-prompt-label-inline small {
            font-size: .62rem !important;
            white-space: nowrap;
        }
        .pp-prompt-bar + div [data-testid="stTextInput"] {
            margin: 0 !important;
            width: 100% !important;
            position: static !important;
        }
        .pp-prompt-bar + div [data-testid="stTextInput"] input {
            height: 48px !important;
        }

        @media (max-width: 1150px) {
            .pp-dashboard-brand { min-width: 250px !important; }
            .pp-top-navigation { gap: .85rem !important; }
            .pp-top-nav { font-size: .76rem !important; }
            .pp-header-actions { min-width: 240px !important; }
        }
        @media (max-width: 850px) {
            .block-container { padding: .7rem .8rem 2rem !important; }
            .pp-dashboard-header { height: auto !important; }
            .pp-dashboard-brand { min-width: auto !important; }
            .pp-header-actions { min-width: auto !important; }
        }

        /* -----------------------------------------------------------------
           High-visibility pass — make the dashboard readable at 100% zoom
           ----------------------------------------------------------------- */
        .block-container {
            max-width: 1700px !important;
            padding: 1.25rem 2rem 3rem !important;
        }

        .pp-dashboard-header {
            min-height: 104px !important;
            height: 104px !important;
            margin-bottom: 1.6rem !important;
            gap: 2rem !important;
        }
        .pp-dashboard-brand { min-width: 360px !important; gap: 1rem !important; }
        .pp-brand-mark { width: 68px !important; height: 68px !important; font-size: 1.7rem !important; }
        .pp-dashboard-name { font-size: 2rem !important; line-height: 1.05 !important; }
        .pp-dashboard-tagline { font-size: .9rem !important; margin-top: .3rem !important; }
        .pp-top-navigation { gap: 2rem !important; }
        .pp-top-nav { font-size: 1rem !important; padding: 1rem .2rem !important; }
        .pp-header-actions { min-width: 360px !important; gap: 1rem !important; }
        .pp-bell { font-size: 1.55rem !important; }
        .pp-help { font-size: .9rem !important; padding: .75rem 1rem !important; }
        .pp-help span { font-size: .75rem !important; }
        .pp-help b { font-size: .85rem !important; }
        .pp-avatar { width: 52px !important; height: 52px !important; }

        /* Give both halves a clear visual boundary and identical geometry. */
        div[data-testid="column"]:has(.pp-input-panel),
        div[data-testid="column"]:has(.pp-output-panel) {
            background: linear-gradient(145deg, rgba(8,27,45,.88), rgba(5,19,33,.82)) !important;
            border: 1px solid rgba(57,213,255,.16) !important;
            border-radius: 20px !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            box-shadow: 0 12px 45px rgba(0,0,0,.18) !important;
        }
        div[data-testid="column"]:has(.pp-input-panel) > div,
        div[data-testid="column"]:has(.pp-output-panel) > div {
            padding: 0 1.35rem 1.35rem !important;
        }
        .pp-input-panel, .pp-output-panel { padding-top: 1.35rem !important; }

        .pp-panel-title { font-size: 1.45rem !important; line-height: 1.15 !important; }
        .pp-panel-sub { font-size: .88rem !important; margin-top: .25rem !important; }
        .pp-panel-icon { width: 52px !important; height: 52px !important; font-size: 1.45rem !important; }

        [data-testid="stTextInput"] input {
            height: 54px !important;
            min-height: 54px !important;
            font-size: .95rem !important;
            padding: 0 1rem !important;
        }
        div[data-testid="column"]:has(.pp-input-panel) [data-testid="stButton"] button {
            height: 54px !important;
            min-height: 54px !important;
            font-size: .9rem !important;
        }

        .pp-location-stats { gap: 1rem !important; margin: .85rem 0 1.15rem !important; }
        .pp-location-stat {
            min-height: 82px !important;
            padding: .85rem 1rem !important;
            border-radius: 12px !important;
            grid-template-columns: 28px 1fr !important;
        }
        .pp-location-stat span { font-size: 1.25rem !important; }
        .pp-location-stat small { font-size: .78rem !important; }
        .pp-location-stat b { font-size: .95rem !important; }

        .pp-query-heading { padding: 1.25rem 0 .85rem !important; gap: .8rem !important; }
        .pp-query-heading .pp-panel-title { font-size: 1.35rem !important; }
        .pp-query-icon { width: 48px !important; height: 48px !important; font-size: 1.25rem !important; }
        .pp-query-row {
            min-height: 76px !important;
            margin: .5rem 0 !important;
            padding: .7rem .9rem !important;
            border-radius: 12px !important;
        }
        .pp-query-icon-small { width: 48px !important; height: 48px !important; flex-basis: 48px !important; font-size: 1.15rem !important; }
        .pp-query-title { font-size: .98rem !important; }
        .pp-query-desc { font-size: .78rem !important; margin-top: .22rem !important; }
        div[data-testid="stPageLink"] { height: 76px !important; margin: .5rem 0 !important; }
        div[data-testid="stPageLink"] a { min-height: 76px !important; font-size: 1.6rem !important; }

        .pp-audio-box { margin-top: 1.2rem !important; min-height: 76px !important; padding: .95rem 1.1rem !important; border-radius: 16px !important; }
        .pp-audio-icon { width: 44px !important; height: 44px !important; font-size: 1.25rem !important; }
        .pp-audio-box b { font-size: .95rem !important; }
        .pp-audio-box small { font-size: .76rem !important; }
        .pp-audio-action { font-size: .82rem !important; padding: .7rem 1rem !important; }

        .pp-output-heading { gap: 1rem !important; }
        .pp-contact { font-size: .82rem !important; padding: .7rem .95rem !important; }
        .pp-output-card {
            min-height: 112px !important;
            padding: .95rem 1rem !important;
            border-radius: 14px !important;
            margin: .25rem 0 .8rem !important;
        }
        .pp-output-card small { font-size: .78rem !important; }
        .pp-output-card strong { font-size: 1.7rem !important; margin: .15rem 0 !important; }
        .pp-output-card span { font-size: .72rem !important; }
        .pp-map-wrap iframe { min-height: 390px !important; }
        .pp-map-overlay { padding: .75rem .9rem !important; }
        .pp-map-overlay b { font-size: .82rem !important; }
        .pp-map-overlay span { font-size: .7rem !important; }
        .pp-ai-result { margin-top: .9rem !important; padding: 1rem 1.1rem !important; gap: .85rem !important; }
        .pp-ai-badge { width: 42px !important; height: 42px !important; flex-basis: 42px !important; }
        .pp-ai-result b { font-size: .9rem !important; }
        .pp-ai-result p { font-size: .76rem !important; line-height: 1.65 !important; }
        .pp-enhance-box { padding: .9rem 1.1rem !important; }
        .pp-enhance-box b { font-size: .84rem !important; }
        .pp-enhance-box small { font-size: .7rem !important; }

        /* Prompt stays a real three-column row and remains readable. */
        .pp-prompt-label-inline b { font-size: .95rem !important; }
        .pp-prompt-label-inline small { font-size: .7rem !important; }
        .pp-prompt-label-inline .pp-prompt-icon { width: 44px !important; height: 44px !important; flex-basis: 44px !important; }
        .pp-prompt-bar + div [data-testid="stTextInput"] input { height: 54px !important; font-size: .88rem !important; }

        @media (max-width: 1250px) {
            .pp-dashboard-brand { min-width: 280px !important; }
            .pp-top-navigation { gap: 1rem !important; }
            .pp-top-nav { font-size: .85rem !important; }
            .pp-header-actions { min-width: 280px !important; }
        }
        @media (max-width: 850px) {
            .block-container { padding: .75rem .75rem 2rem !important; }
            .pp-dashboard-header { height: auto !important; min-height: 0 !important; }
            .pp-dashboard-name { font-size: 1.55rem !important; }
            .pp-top-navigation { gap: .55rem !important; }
            .pp-top-nav { font-size: .75rem !important; }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle=None):
    """Render the shared Purv Path header on every Streamlit page."""
    inject_theme()

    st.markdown(
        f"""
        <div class="pp-dashboard-header pp-shared-header">
          <div class="pp-dashboard-brand">
            <div class="pp-brand-mark">{_LOGO_HTML}</div>
            <div>
              <div class="pp-dashboard-name">पूर्वपथ</div>
              <div class="pp-dashboard-tagline">Safer Roads&nbsp;&nbsp; Stronger Communities</div>
            </div>
          </div>
          <div class="pp-shared-header-note">AI-Powered Logistics Accessibility Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Compact navigation is shared by every page so the branded header remains
    # visible while still allowing users to move between the multipage app.
    nav_cols = st.columns([1.05, 1, 1, 1, 1, 1, 1.25], gap="small")
    nav_items = [
        ("Home", "Home.py", "⌂"),
        ("Risk Map", "pages/1_Risk_Map.py", "◉"),
        ("Routes", "pages/2_Route_Optimizer.py", "↗"),
        ("Fleet", "pages/3_Fleet_Tracking.py", "▣"),
        ("Reports", "pages/4_Field_Reports.py", "▤"),
        ("Alerts", "pages/5_Alerts.py", "⚠"),
        ("Analytics", "pages/6_Analytics.py", "▥"),
    ]
    for col, (label, path, icon) in zip(nav_cols, nav_items):
        with col:
            st.page_link("pages/6_Analytics.py", label="Analytics")


    st.markdown("<div class='pp-shared-header-rule'></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='pp-title'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f"<div class='pp-page-subtitle'>{subtitle}</div>",
            unsafe_allow_html=True,
        )


def feature_card(container, icon, title, description, page_path, button_label="Open"):
    with container:
        st.markdown(
            f"""<div class="pp-card" style="height:190px">
                <div style="font-size:1.5rem">{icon}</div>
                <div style="font-family:'Space Grotesk';font-weight:700;color:#fff;margin-top:.5rem">{title}</div>
                <div style="font-size:.72rem;color:#91a9bb;line-height:1.45;margin-top:.35rem">{description}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.page_link(page_path, label=button_label)
