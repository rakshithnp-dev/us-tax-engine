import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="US Tax Engine | Nexus & Rates", page_icon="🇺🇸", layout="wide")

# --- 1. THE BRAINS (DATA & RULES) ---

# A. Nexus Thresholds (The "Macro" Logic)
NEXUS_RULES = {
    'AL': {'threshold': 250000, 'transactions': 0},
    'CA': {'threshold': 500000, 'transactions': 0},
    'NY': {'threshold': 500000, 'transactions': 100},
    'TX': {'threshold': 500000, 'transactions': 0},
    'WA': {'threshold': 100000, 'transactions': 0},
    'FL': {'threshold': 100000, 'transactions': 0},
    'DEFAULT': {'threshold': 100000, 'transactions': 200}
}

# B. Tax Rate Database (The "Micro" Logic - Simulation)
# In production, this would be an API call to Vertex/Avalara/Taxually
ZIP_RATES = {
    '90210': {'city': 'Beverly Hills', 'state': 'CA', 'rate': 0.095},
    '10001': {'city': 'New York', 'state': 'NY', 'rate': 0.08875},
    '33101': {'city': 'Miami', 'state': 'FL', 'rate': 0.07},
    '73301': {'city': 'Austin', 'state': 'TX', 'rate': 0.0825},
    '98101': {'city': 'Seattle', 'state': 'WA', 'rate': 0.1025},
}

def get_threshold(state_code):
    return NEXUS_RULES.get(state_code, NEXUS_RULES['DEFAULT'])

def calculate_tax(zip_code, amount):
    if zip_code in ZIP_RATES:
        data = ZIP_RATES[zip_code]
        tax_amt = amount * data['rate']
        return data, tax_amt
    return None, 0

# --- 2. THE UI SHELL ---
st.title("🗺️ US Tax Compliance Engine")
st.markdown("### Enterprise Nexus Monitoring & Rate Calculation")

# Create two tabs for the two features
tab1, tab2 = st.tabs(["🗺️ Economic Nexus Monitor", "🧮 Real-Time Rate Calculator"])

# --- TAB 1: THE NEXUS HEATMAP ---
with tab1:
    st.header("Economic Nexus Exposure")
    st.caption("Upload sales data to visualize where you have triggered tax obligations.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Sales CSV", type=['csv'])
        
        # Generator for Demo Data
        if not uploaded_file:
            st.info("👋 Use sample data to see the map action.")
            sample = pd.DataFrame({
                'state_code': ['CA', 'CA', 'NY', 'TX', 'WA', 'FL', 'AL'],
                'amount': [250000, 300000, 40000, 600000, 50, 2000, 260000]
            })
            csv = sample.to_csv(index=False).encode('utf-8')
            st.download_button("Download Sample CSV", csv, "sample_nexus.csv", "text/csv")

    # If data is present, run the logic
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        if 'state_code' not in df.columns or 'amount' not in df.columns:
            st.error("CSV error: Columns 'state_code' and 'amount' required.")
        else:
            # Aggregation Logic
            state_summary = df.groupby('state_code').agg(
                total_revenue=('amount', 'sum'),
                total_transactions=('amount', 'count')
            ).reset_index()

            nexus_data = []
            for _, row in state_summary.iterrows():
                state = row['state_code']
                rev = row['total_revenue']
                tx = row['total_transactions']
                rule = get_threshold(state)
                
                # Check for breach
                breach = (rev >= rule['threshold']) or (rule['transactions'] > 0 and tx >= rule['transactions'])
                
                nexus_data.append({
                    'code': state,
                    'revenue': rev,
                    'status': '⚠️ LIABLE' if breach else '✅ Safe',
                    'color_scale': 1 if breach else 0
                })
            
            map_df = pd.DataFrame(nexus_data)
            
            with col2:
                fig = px.choropleth(
                    map_df,
                    locations='code', 
                    locationmode="USA-states", 
                    color='color_scale',
                    scope="usa",
                    color_continuous_scale=[(0, "#2ecc71"), (1, "#e74c3c")], # Green to Red
                    hover_data=['revenue', 'status'],
                    title="Economic Nexus Risk Map"
                )
                fig.update_layout(coloraxis_showscale=False, margin={"r":0,"t":30,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(map_df[['code', 'status', 'revenue']], use_container_width=True)

# --- TAB 2: THE RATE CALCULATOR ---
with tab2:
    st.header("ZipTax Real-Time Calculator")
    st.caption("Simulate API calls for tax determination based on geolocation.")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        input_zip = st.text_input("Zip Code (Try 90210, 10001, 73301)", max_chars=5)
    with c2:
        input_amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=100.0, step=10.0)
    
    if st.button("Calculate Tax"):
        details, tax_val = calculate_tax(input_zip, input_amount)
        
        if details:
            with c3:
                st.metric(label="Total Tax Due", value=f"${tax_val:.2f}")
            
            st.success(f"✅ Rate Found: {details['city']}, {details['state']}")
            
            # Breakdown Visualization
            st.subheader("Tax Breakdown")
            breakdown_col1, breakdown_col2 = st.columns(2)
            
            with breakdown_col1:
                st.markdown(f"""
                | Jurisdiction | Rate |
                | :--- | :--- |
                | **State ({details['state']})** | {(details['rate']*0.6):.2%} |
                | **City ({details['city']})** | {(details['rate']*0.4):.2%} |
                | **TOTAL** | **{details['rate']:.2%}** |
                """)
            
            with breakdown_col2:
                st.json({
                    "status": "success",
                    "zip": input_zip,
                    "jurisdiction_code": f"{details['state']}-{input_zip}",
                    "tax_collectible": round(tax_val, 2)
                })
                
        else:
            st.error("❌ Zip Code not in demo database. Try 90210 (CA) or 10001 (NY).")