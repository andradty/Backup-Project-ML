"""Modern SaaS AgriTech UI Styling, Custom SVG Illustrations, and Navigation Helpers."""

import streamlit as st

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    scroll-behavior: smooth;
}

/* Constrain main container so it NEVER looks stretched or gepeng on ultrawide screens */
.block-container {
    max-width: 1180px !important;
    padding-top: 2.2rem !important;
    padding-bottom: 4rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Override Streamlit default red primary button to emerald green pill */
button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(74, 222, 128, 0.45) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.25rem !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 18px rgba(22, 163, 74, 0.28) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 24px rgba(34, 197, 94, 0.4) !important;
}

button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.7) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(148, 163, 184, 0.3) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.65rem !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    transition: all 0.25s ease !important;
}
button[kind="secondary"] p {
    white-space: nowrap !important;
    font-size: 0.88rem !important;
}
button[kind="secondary"]:hover {
    border-color: #4ade80 !important;
    color: #4ade80 !important;
    transform: translateY(-2px) !important;
}

/* Compact Burger Button in Top Right */
[data-testid="stPopover"] > div > button {
    border: 1px solid rgba(74, 222, 128, 0.45) !important;
    background: rgba(20, 83, 45, 0.45) !important;
    color: #f8fafc !important;
    border-radius: 10px !important;
    padding: 0.48rem 1.1rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
}
[data-testid="stPopover"] > div > button:hover {
    border-color: #4ade80 !important;
    background: rgba(22, 163, 74, 0.65) !important;
    transform: translateY(-2px) !important;
}

/* Keyframe Animations */
@keyframes pageFadeSlide {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes floatSlow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes scanBeam {
    0% { transform: translateY(-60px); opacity: 0.2; }
    50% { transform: translateY(60px); opacity: 0.85; }
    100% { transform: translateY(-60px); opacity: 0.2; }
}

.page-anim-wrap {
    animation: pageFadeSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Clean Top Header Bar */
.top-nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.brand-logo-box {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    border-radius: 11px;
    background: linear-gradient(135deg, #16a34a 0%, #14532d 100%);
    border: 1px solid rgba(74, 222, 128, 0.45);
    color: #ffffff !important;
    box-shadow: 0 6px 16px rgba(22, 163, 74, 0.3);
}
.brand-title {
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: -0.4px;
    color: var(--text-color, #f8fafc);
    line-height: 1.15;
}
.brand-subtitle {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: #4ade80;
}

/* 2-Column Split Hero Banner (Tall, Proportional, Never Gepeng) */
.hero-split {
    display: grid;
    grid-template-columns: 1.25fr 0.95fr;
    gap: 2.4rem;
    align-items: center;
    background: radial-gradient(circle at 85% 20%, rgba(22, 163, 74, 0.24) 0%, rgba(15, 41, 30, 0.85) 45%, #09131c 100%);
    border: 1px solid rgba(74, 222, 128, 0.28);
    border-radius: 22px;
    padding: 3.2rem 3.0rem;
    margin-top: 0.5rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
    color: #ffffff !important;
}
@media (max-width: 900px) {
    .hero-split {
        grid-template-columns: 1fr;
        padding: 2.2rem 1.8rem;
    }
}
.hero-badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(34, 197, 94, 0.16);
    border: 1px solid rgba(74, 222, 128, 0.4);
    color: #86efac !important;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 1.15rem;
}
.hero-main-title {
    font-size: 2.65rem;
    font-weight: 800;
    line-height: 1.16;
    letter-spacing: -0.9px;
    color: #ffffff !important;
    margin-bottom: 1.05rem;
}
.hero-highlight {
    background: linear-gradient(90deg, #4ade80, #a7f3d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-size: 1.02rem;
    line-height: 1.7;
    color: #cbd5e1 !important;
    margin-bottom: 1.75rem;
}
.hero-mini-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.hero-tag-chip {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.25);
    color: #e2e8f0 !important;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.82rem;
    font-weight: 600;
}

/* Right Side Visual Showcase inside Hero */
.hero-visual-panel {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 18px;
    padding: 1.6rem;
    position: relative;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1), 0 16px 32px rgba(0, 0, 0, 0.3);
    animation: floatSlow 5s ease-in-out infinite;
}
.visual-svg-box {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.5rem 0 1.0rem 0;
}
.visual-kpi-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
.visual-kpi-box {
    background: rgba(9, 19, 28, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 12px;
    padding: 0.85rem 1.0rem;
    text-align: left;
}
.visual-kpi-val {
    font-size: 1.35rem;
    font-weight: 800;
    color: #4ade80 !important;
    line-height: 1.15;
}
.visual-kpi-lbl {
    font-size: 0.76rem;
    color: #94a3b8 !important;
    margin-top: 4px;
    line-height: 1.3;
}

/* Scroll Indicator */
.scroll-cue {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: #4ade80;
    margin: 1.2rem 0 2.4rem 0;
    animation: floatSlow 2.6s ease-in-out infinite;
}

/* Section Banner on Long Scroll */
.scroll-section {
    padding: 2.2rem 0 1.2rem 0;
    text-align: center;
}
.sec-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: #4ade80 !important;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.32);
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 0.65rem;
}
.sec-heading {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text-color, inherit);
    margin-bottom: 0.45rem;
}
.sec-lead {
    font-size: 0.98rem;
    color: var(--text-color, inherit);
    opacity: 0.78;
    max-width: 720px;
    margin: 0 auto 1.2rem auto;
    line-height: 1.65;
}

/* Tall Proportional Cards (Never Gepeng) */
.anim-card {
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    color: var(--text-color, inherit) !important;
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 16px;
    padding: 1.65rem 1.55rem;
    min-height: 225px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
}
.anim-card:hover {
    transform: translateY(-6px);
    border-color: rgba(74, 222, 128, 0.55);
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.26), 0 0 20px rgba(34, 197, 94, 0.12);
}
.anim-card-accent {
    border-top: 3px solid #22c55e;
}
.anim-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.85rem;
}
.icon-box {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(34, 197, 94, 0.16);
    border: 1px solid rgba(74, 222, 128, 0.38);
    color: #4ade80 !important;
    font-weight: 800;
    flex-shrink: 0;
}
.anim-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-color, inherit) !important;
    line-height: 1.3;
}
.anim-card-body {
    font-size: 0.92rem;
    line-height: 1.65;
    color: var(--text-color, inherit) !important;
    opacity: 0.88;
}

/* Pipeline Step Timeline Card */
.pipe-step {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-left: 4px solid #22c55e;
    border-radius: 13px;
    padding: 1.15rem 1.3rem;
    margin-bottom: 0.95rem;
    transition: all 0.25s ease;
}
.pipe-step:hover {
    transform: translateX(6px);
    border-color: #4ade80;
    box-shadow: 0 10px 22px rgba(0, 0, 0, 0.18);
}
.pipe-num {
    display: inline-block;
    font-size: 0.74rem;
    font-weight: 800;
    color: #4ade80;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

/* Disease Profile Card */
.disease-card {
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.88) 100%);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 16px;
    padding: 1.55rem 1.6rem;
    margin-bottom: 1.15rem;
    min-height: 255px;
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
}
.disease-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.25);
}

/* Result Banner on Scanner Page */
.result-banner {
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
    color: #ffffff !important;
    margin-bottom: 1.15rem;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.26);
    animation: pageFadeSlide 0.45s ease-out;
}
.result-banner * {
    color: #ffffff !important;
}

.section-hdr {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.18rem;
    font-weight: 700;
    color: var(--text-color, inherit);
    margin: 0.6rem 0 0.85rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.22);
}
.section-hdr svg {
    color: #4ade80;
    flex-shrink: 0;
}

.sub-hdr {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--text-color, inherit);
    margin: 1.0rem 0 0.55rem 0;
}
.sub-hdr svg {
    color: #4ade80;
    flex-shrink: 0;
}
</style>
"""

# Rich Custom SVG Vector Illustration for the Hero Right Panel
HERO_SCANNER_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="210" height="150" viewBox="0 0 240 165" fill="none">
  <!-- Outer Scanner Frame Corners -->
  <path d="M22 40V22H40" stroke="#4ade80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M218 40V22H200" stroke="#4ade80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M22 125V143H40" stroke="#4ade80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M218 125V143H200" stroke="#4ade80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Subtle Grid Background -->
  <line x1="35" y1="55" x2="205" y2="55" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>
  <line x1="35" y1="82" x2="205" y2="82" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>
  <line x1="35" y1="110" x2="205" y2="110" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>
  <!-- Stylized Rice Leaf Vector -->
  <path d="M55 128C65 82 110 42 185 32C175 88 135 122 55 128Z" fill="rgba(34, 197, 94, 0.22)" stroke="#22c55e" stroke-width="2.5"/>
  <path d="M55 128C95 98 138 66 185 32" stroke="#4ade80" stroke-width="2" stroke-linecap="round"/>
  <!-- Feature Extraction Nodes on Leaf -->
  <circle cx="105" cy="92" r="5" fill="#f59e0b" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="135" cy="68" r="6" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="155" cy="54" r="4.5" fill="#22c55e" stroke="#ffffff" stroke-width="1.5"/>
  <!-- Callout Lines -->
  <polyline points="135,68 162,96 198,96" stroke="#94a3b8" stroke-width="1.3" fill="none"/>
  <rect x="155" y="102" width="52" height="18" rx="4" fill="#0f172a" stroke="#4ade80" stroke-width="1"/>
  <text x="181" y="114" fill="#4ade80" font-size="9" font-family="sans-serif" font-weight="bold" text-anchor="middle">GLCM + HSV</text>
</svg>
"""

ICONS = {
    "leaf": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
    "burger": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/></svg>',
    "camera": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>',
    "scan": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/><path d="m16 16-1.9-1.9"/></svg>',
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>',
    "sliders": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/></svg>',
    "shield": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
    "cpu": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>',
    "users": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "book": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>',
    "layers": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    "grid": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>',
    "arrow_down": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>',
}


def inject_css():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def section_header(icon_name: str, title: str):
    svg = ICONS.get(icon_name, ICONS["leaf"])
    st.markdown(f'<div class="section-hdr">{svg}<span>{title}</span></div>', unsafe_allow_html=True)


def sub_header(icon_name: str, title: str):
    svg = ICONS.get(icon_name, ICONS["leaf"])
    st.markdown(f'<div class="sub-hdr">{svg}<span>{title}</span></div>', unsafe_allow_html=True)


def scroll_section_banner(tag: str, title: str, lead: str):
    st.markdown(
        f"""
        <div class="scroll-section">
            <div class="sec-tag">{ICONS["leaf"]}<span>{tag}</span></div>
            <div class="sec-heading">{title}</div>
            <div class="sec-lead">{lead}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
