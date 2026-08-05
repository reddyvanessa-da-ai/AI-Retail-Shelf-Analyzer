import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.gemini_insights import generate_insights

# -------------------- Title --------------------

st.set_page_config(
    page_title="RetailSense AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    font-size:3.2rem;
    font-weight:800;
    color:#F8FAFC;
    margin-bottom:0;
}

.sub-title{
    color:#94A3B8;
    font-size:1.15rem;
    margin-top:-8px;
    margin-bottom:28px;
}

.stMetric{
    border:1px solid #334155;
    border-radius:12px;
    padding:14px;
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<div class="main-title">
RetailSense AI
</div>

<div class="sub-title">
Intelligent Retail Shelf Analytics powered by Computer Vision and Generative AI.
</div>
""",
unsafe_allow_html=True
)

st.info("Detect products from retail shelf images, analyze inventory distribution, and generate AI-powered merchandising insights for retail decision-making.")

# -------------------- Images --------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Original Shelf Image")
    st.image("data/raw/shelf.jpg", use_container_width=True)

with col2:
    st.markdown("### Detected Inventory")
    detected_image = Path("outputs/images/detected_shelf.jpg")
    if detected_image.exists():
        st.image(str(detected_image), use_container_width=True)
    else:
        st.info("Run the detection to view the annotated shelf image.")

st.caption("""
    **Detection Model:** YOLO-World | **Computer Vision:** OpenCV | **Analytics:** Pandas + Plotly | **Generative AI:** Google Gemini 3.5 Flash
    """)

st.divider()

# -------------------- Inventory --------------------

inventory_file = Path("outputs/reports/inventory.csv")

if inventory_file.exists():
    df = pd.read_csv(inventory_file)
else:
    st.warning("Please upload and analyze a shelf image to generate the inventory report.")
    st.stop()
    
st.markdown("## Inventory Analysis")

with st.expander("View Complete Inventory"):
    st.dataframe(df, use_container_width=True)

# -------------------- Shelf Performance Metrics --------------------

st.markdown("## Shelf Performance Metrics")

total_products = len(df)
unique_categories = df["Product"].nunique()
avg_confidence = df["Confidence"].mean() * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Products",
        value=total_products
    )

with col2:
    st.metric(
        label="Product Categories",
        value=unique_categories
    )

with col3:
    st.metric(
        label="Average Detection Confidence",
        value=f"{avg_confidence:.1f}%"
    )


# -------------------- Category Summary --------------------

summary = (
    df["Product"]
    .value_counts()
    .reset_index()
)

summary.columns = ["Product", "Count"]
summary["Shelf Share (%)"] = (
    summary["Count"] / summary["Count"].sum() * 100
).round(1)

st.markdown("### Category Summary")
st.dataframe(summary, use_container_width=True, hide_index=True)


# -------------------- Product Count Chart --------------------

counts=(df["Product"].value_counts().reset_index())
counts.columns=["Product","Count"]

fig=px.bar(
    counts,
    x="Product",
    y="Count",
    text="Count",
    color="Product",
    color_discrete_sequence=["#2563EB","#059669","#F59E0B","#7C3AED","#DC2626","#0891B2"]
)

fig.update_layout(
    plot_bgcolor="#111827",
    paper_bgcolor="#111827",
    font=dict(color="white"),
    xaxis_title="Product Category",
    yaxis_title="Number of Detected Items",
    showlegend=False
)

fig.update_traces(textposition="outside",marker_line_width=0)
st.markdown(
    "<h3 style='text-align:center;'>Inventory Distribution by Product Category</h3>",
    unsafe_allow_html=True
)
st.plotly_chart(fig,use_container_width=True)

# -------------------- AI Insights --------------------

st.markdown("## Executive Retail Intelligence Report")

try:
    with st.spinner("Generating retail intelligence report..."):
        insights = generate_insights()

    st.markdown(insights, unsafe_allow_html=True)

except Exception as e:
    error_message = str(e)

    if "503" in error_message or "UNAVAILABLE" in error_message:
        st.warning(
            """
### AI Report Temporarily Unavailable

The Generative AI service is currently experiencing high request volume.  
Please try generating the report again in a few moments.

Inventory detection and analytics remain fully functional.
"""
        )
    else:
        st.error("Unable to generate the Executive Retail Intelligence Report.")
        st.caption(error_message)

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#94A3B8;font-size:14px;">
RetailSense AI • Powered by YOLO-World • OpenCV • Streamlit • Plotly • Google Gemini
</div>
""",unsafe_allow_html=True)
