# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 10:48:33 2025

@author: aless
"""

import os
import pandas as pd
import streamlit as st
from datetime import date

# ---------------------------
# Page config & basic style
# ---------------------------
st.set_page_config(
    page_title="DATAWORLD • 3D Print Control",
    page_icon="🧩",
    layout="wide"
)

ACCENT = "#6BE26B"  # verde stile pill
PRIMARY_DARK = "#111827"

CUSTOM_CSS = f"""
<style>
/* top heading spacing */
.block-container {{
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}}
/* search bar look */
input[type="text"] {{
    border-radius: 12px !important;
}}
/* green pill */
.pill {{
    display:inline-block;
    background:{ACCENT};
    padding:.55rem 1.2rem;
    border-radius: 999px;
    font-weight:600;
    color:#0f172a;
}}
/* card style */
.card {{
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:16px;
    height:100%;
    background:white;
    box-shadow: 0 1px 2px rgba(0,0,0,.03);
}}
.card h4 {{
    margin: 0 0 .35rem 0;
}}
.badge {{
    display:inline-block;
    border:1px solid #e5e7eb;
    padding:.15rem .5rem;
    border-radius:999px;
    font-size:.8rem;
    color:#374151;
}}
footer {{visibility:hidden;}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------
# Fake dataset (replace later with DATAWORLD)
# ---------------------------
materials = pd.DataFrame([
    {
        "product": "Terrascorata brick",
        "license_iso": "AMCLUSIVE N 12m SLS",
        "manufacturer": "3D Systems Floor",
        "valid_until": date(2026, 6, 30),
        "color": "Orange",
        "characteristics": "SLS, brick-like, architectural",
        "certifications": ["ISO 9001", "REACH"],
        "image": "static/brick.png"
    },
    {
        "product": "Ultrasint® TPU 64D",
        "license_iso": "AMCLUSIVE N 12m SLS",
        "manufacturer": "BASF Forward AM",
        "valid_until": date(2027, 1, 15),
        "color": "Gray",
        "characteristics": "TPU flexible",
        "certifications": ["ISO 10993", "RoHS"],
        "image": "static/tpu.png"
    },
    {
        "product": "Quantum Carbon",
        "license_iso": "3D Systems Floor",
        "manufacturer": "Quantum",
        "valid_until": date(2025, 12, 31),
        "color": "Black",
        "characteristics": "High strength carbon filled",
        "certifications": ["UL 94 V-0"],
        "image": "static/carbon.png"
    },
    {
        "product": "White 3D xiate",
        "license_iso": "Laser Sintering",
        "manufacturer": "Xiate Labs",
        "valid_until": date(2026, 9, 1),
        "color": "White",
        "characteristics": "General purpose nylon",
        "certifications": ["ISO 9001", "FDA Food Contact"],
        "image": "static/white.png"
    },
])

manufacturers = (
    materials[["manufacturer"]]
    .drop_duplicates()
    .assign(website=lambda d: ["https://example.com"] * len(d))
)

certs = (
    materials.explode("certifications")[["product", "manufacturer", "certifications"]]
    .rename(columns={"certifications": "certification"})
)

# ---------------------------
# Header
# ---------------------------
col_logo, col_title, col_cta = st.columns([0.25, 1.2, 0.6])
with col_title:
    st.markdown(f"### **3D PRINT CONTROL**")
    st.markdown('<span class="pill">Fast, affordable and accurate material compliance database.</span>', unsafe_allow_html=True)
with col_cta:
    st.write("")
    st.write("")
    st.markdown("**DATAWORLD** — *Powered by AM Hub*")

st.write("")
st.write("")

# ---------------------------
# Search + language flags
# ---------------------------
c1, c2 = st.columns([1, .15])
with c1:
    query = st.text_input("Search by material or certification…", placeholder="e.g. TPU, ISO 10993, UL 94…")
with c2:
    st.write("Languages")
    st.write("🇬🇧 🇫🇷 🇩🇪 🇮🇹")

st.write("")
st.markdown("#### Enabling responsible AM")

# ---------------------------
# Tabs
# ---------------------------
tab_materials, tab_manuf, tab_certs, tab_faq, tab_contact = st.tabs(
    ["Materials", "Manufacturers", "Certification", "FAQ", "Contact"]
)

# ---------------------------
# Materials Tab
# ---------------------------
with tab_materials:
    left, right = st.columns([0.28, 0.72])

    with left:
        st.markdown("**Filters**")
        colors = ["Black", "Gray", "White", "Orange"]
        f_color = st.multiselect("Color", colors)
        f_manuf = st.multiselect("Manufacturer", materials["manufacturer"].unique().tolist())
        f_cert = st.multiselect("Certification", sorted({c for lst in materials["certifications"] for c in lst}))
        valid_only = st.toggle("Valid only (date in the future)", value=True)

    with right:
        # apply search & filters
        df = materials.copy()

        if query:
            q = query.lower()
            df = df[
                df["product"].str.lower().str.contains(q) |
                df["license_iso"].str.lower().str.contains(q) |
                df["manufacturer"].str.lower().str.contains(q) |
                df["characteristics"].str.lower().str.contains(q) |
                df["certifications"].apply(lambda lst: any(q in c.lower() for c in lst))
            ]

        if f_color:
            df = df[df["color"].isin(f_color)]
        if f_manuf:
            df = df[df["manufacturer"].isin(f_manuf)]
        if f_cert:
            df = df[df["certifications"].apply(lambda lst: any(c in lst for c in f_cert))]
        if valid_only:
            df = df[df["valid_until"] >= date.today()]

        st.caption(f"{len(df)} results")

        # grid of cards (3 per row)
        n_per_row = 3
        rows = [df.iloc[i:i + n_per_row] for i in range(0, len(df), n_per_row)]

        for r in rows:
            cols = st.columns(n_per_row)
            for col, (_, row) in zip(cols, r.iterrows()):
                with col:
                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    # image if present, otherwise colored placeholder
                    if isinstance(row["image"], str) and os.path.exists(row["image"]):
                        st.image(row["image"], use_container_width=True)
                    else:
                        st.markdown(f'<div style="width:100%;height:130px;border-radius:12px;background:{ACCENT}15;border:1px dashed {ACCENT}55;"></div>', unsafe_allow_html=True)

                    st.markdown(f"#### {row['product']}")
                    st.markdown(
                        f'<span class="badge">{row["license_iso"]}</span> '
                        f'<span class="badge">{row["color"]}</span> '
                        f'<span class="badge">Valid until: {row["valid_until"]}</span>',
                        unsafe_allow_html=True
                    )
                    st.write("")
                    st.write(f"**Manufacturer:** {row['manufacturer']}")
                    st.write(row["characteristics"])
                    if row["certifications"]:
                        st.write("**Certifications:** " + ", ".join(row["certifications"]))

                    with st.expander("Show details / request certification"):
                        st.write("Request a copy of the certificate, safety data sheet, or more info.")
                        st.text_input("Your email", key=f"email_{row['product']}")
                        st.text_area("Message", key=f"msg_{row['product']}", height=80, placeholder=f"Hi AM Hub, I’d like the certification for {row['product']}…")
                        st.button("Send request to AM Hub", key=f"send_{row['product']}")

                    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Manufacturers Tab
# ---------------------------
with tab_manuf:
    st.write("Browse manufacturers present in DATAWORLD.")
    st.dataframe(manufacturers, use_container_width=True)

# ---------------------------
# Certification Tab
# ---------------------------
with tab_certs:
    st.write("Link between products, manufacturers and certifications in DATAWORLD.")
    # Search inside certs
    q2 = st.text_input("Search certification…", placeholder="e.g. ISO 9001, UL 94 V-0")
    cert_view = certs.copy()
    if q2:
        cert_view = cert_view[cert_view["certification"].str.lower().str.contains(q2.lower())]
    st.dataframe(cert_view, use_container_width=True)

# ---------------------------
# FAQ Tab
# ---------------------------
with tab_faq:
    st.markdown("### FAQ")
    st.markdown("**What is DATAWORLD?**  \nA smart, fast, and affordable database for material compliance in AM, provided by **AM Hub**.")
    st.markdown("**Can I request certificates?**  \nYes. Open a material card and use *Request certification*.")
    st.markdown("**Do you support multiple languages?**  \nYes (EN/FR/DE/IT).")

# ---------------------------
# Contact Tab
# ---------------------------
with tab_contact:
    st.markdown("### Contact AM Hub")
    c1, c2 = st.columns([0.6, 0.4])
    with c1:
        name = st.text_input("Name")
        email = st.text_input("Email")
        msg = st.text_area("Message", height=120)
        st.button("Send message to AM Hub")
    with c2:
        st.info("AM Hub — Responsible AM\n\nEmail: info@amhub.example\nAddress: Via Example 1, 20100, IT")

# ---------------------------
# Footer badge
# ---------------------------
st.write("")
st.write("---")
st.write("© DATAWORLD — Powered by AM Hub")
