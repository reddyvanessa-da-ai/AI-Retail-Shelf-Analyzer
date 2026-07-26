import re
import streamlit as st
import pandas as pd
from dotenv import dotenv_values
from google import genai
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
config = dotenv_values(env_path)

# Try loading API key from local .env
api_key = config.get("GEMINI_API_KEY")

# If not available (e.g., Streamlit Cloud), use Streamlit Secrets
if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

def generate_insights():
    df = pd.read_csv("outputs/reports/inventory.csv")

    inventory = df["Product"].value_counts().to_string()

    prompt = f"""
You are a Senior Retail Analytics Consultant preparing a shelf performance report for a supermarket manager.

Analyze ONLY the inventory detected by the AI vision system.

Detected Inventory:

{inventory}

Generate a professional executive report in Markdown.

### *Inventory Summary*

Provide 3–4 concise bullet points.

Include:
- Total number of detected products.
- Total number of product categories.
- Percentage contribution of each category wherever applicable.
- Dominant product category.

### *Shelf Distribution Analysis*

Provide 3 bullet points describing:
- Product concentration.
- Category balance.
- Shelf visibility.
- Overall assortment quality.

Support observations using counts and percentages wherever possible.

### *Category Performance*

For every detected category, provide:
- Product name
- Number of detections
- Percentage of total detections
- Brief business interpretation

Example format:
- Snack Packets — 26 detections (81.3%) — Highest shelf visibility.
- Beverage Cans — 6 detections (18.7%) — Lower shelf representation.
Never place multiple category entries on the same line.

### *Business Recommendations*
Provide exactly five practical recommendations.
Recommendations should focus on:
- Shelf organization
- Product visibility
- Category balance
- Cross-merchandising
- Customer shopping experience
Keep every recommendation short, professional and actionable.

### *Executive Observation*
Provide exactly three concluding bullet points covering:
- Overall shelf condition
- Inventory visibility
- Any limitations of making inventory decisions from a single shelf image

Important Guidelines
- Base every statement strictly on detected products.
- Never invent products.
- Never estimate revenue, sales, customer demand, stock levels or shelf occupancy.
- Never assume products are out of stock.
- Whenever appropriate, support observations using numerical values, percentages or counts.
- Write like a retail consulting report rather than an AI assistant.
- Keep the report between 180 and 220 words.
- Use only Markdown headings and bullet points.

Formatting Rules
- Do not use emojis.
- Do not use decorative icons or symbols.
- Use Markdown heading level 3 (###) for every report section.
- Do not use level 1 (#) or level 2 (##) headings.
- Use bullet points for all content; avoid long paragraphs.
- Maintain consistent spacing between headings and bullet points.
- Write in a professional consulting style similar to McKinsey, Deloitte, or PwC.
"""

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt
    )
    # Get the generated text
    insights = response.text

    # Remove emojis and special characters from the insights
    insights = re.sub(
        r'[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]',
        '',
        insights
    )
    return insights
