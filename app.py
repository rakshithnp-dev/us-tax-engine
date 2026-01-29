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
# Expanded database covering 50+ major US cities across all states
ZIP_RATES = {
    # Original Demo Cities
    '90210': {'city': 'Beverly Hills', 'state': 'CA', 'rate': 0.095},
    '10001': {'city': 'New York', 'state': 'NY', 'rate': 0.08875},
    '33101': {'city': 'Miami', 'state': 'FL', 'rate': 0.07},
    '73301': {'city': 'Austin', 'state': 'TX', 'rate': 0.0825},
    '98101': {'city': 'Seattle', 'state': 'WA', 'rate': 0.1025},
    
    # Major Metro Areas
    '60601': {'city': 'Chicago', 'state': 'IL', 'rate': 0.1025},
    '02101': {'city': 'Boston', 'state': 'MA', 'rate': 0.0625},
    '80201': {'city': 'Denver', 'state': 'CO', 'rate': 0.0881},
    '30301': {'city': 'Atlanta', 'state': 'GA', 'rate': 0.089},
    '19101': {'city': 'Philadelphia', 'state': 'PA', 'rate': 0.08},
    '85001': {'city': 'Phoenix', 'state': 'AZ', 'rate': 0.083},
    '92101': {'city': 'San Diego', 'state': 'CA', 'rate': 0.0775},
    '75201': {'city': 'Dallas', 'state': 'TX', 'rate': 0.0825},
    '77001': {'city': 'Houston', 'state': 'TX', 'rate': 0.0825},
    
    # State Capitals
    '36101': {'city': 'Montgomery', 'state': 'AL', 'rate': 0.10},
    '99501': {'city': 'Anchorage', 'state': 'AK', 'rate': 0.00},
    '72201': {'city': 'Little Rock', 'state': 'AR', 'rate': 0.095},
    '95814': {'city': 'Sacramento', 'state': 'CA', 'rate': 0.0825},
    '06101': {'city': 'Hartford', 'state': 'CT', 'rate': 0.0635},
    '19901': {'city': 'Dover', 'state': 'DE', 'rate': 0.00},
    '32301': {'city': 'Tallahassee', 'state': 'FL', 'rate': 0.07},
    '96801': {'city': 'Honolulu', 'state': 'HI', 'rate': 0.045},
    '83701': {'city': 'Boise', 'state': 'ID', 'rate': 0.06},
    '46201': {'city': 'Indianapolis', 'state': 'IN', 'rate': 0.07},
    '50301': {'city': 'Des Moines', 'state': 'IA', 'rate': 0.07},
    '66601': {'city': 'Topeka', 'state': 'KS', 'rate': 0.095},
    '40601': {'city': 'Frankfort', 'state': 'KY', 'rate': 0.06},
    '70801': {'city': 'Baton Rouge', 'state': 'LA', 'rate': 0.0945},
    '04330': {'city': 'Augusta', 'state': 'ME', 'rate': 0.055},
    '21401': {'city': 'Annapolis', 'state': 'MD', 'rate': 0.06},
    '48901': {'city': 'Lansing', 'state': 'MI', 'rate': 0.06},
    '55101': {'city': 'St. Paul', 'state': 'MN', 'rate': 0.0775},
    '39201': {'city': 'Jackson', 'state': 'MS', 'rate': 0.07},
    '65101': {'city': 'Jefferson City', 'state': 'MO', 'rate': 0.0823},
    '59601': {'city': 'Helena', 'state': 'MT', 'rate': 0.00},
    '68501': {'city': 'Lincoln', 'state': 'NE', 'rate': 0.075},
    '89501': {'city': 'Reno', 'state': 'NV', 'rate': 0.0825},
    '03301': {'city': 'Concord', 'state': 'NH', 'rate': 0.00},
    '08601': {'city': 'Trenton', 'state': 'NJ', 'rate': 0.06625},
    '87501': {'city': 'Santa Fe', 'state': 'NM', 'rate': 0.0838},
    '27601': {'city': 'Raleigh', 'state': 'NC', 'rate': 0.0725},
    '58501': {'city': 'Bismarck', 'state': 'ND', 'rate': 0.07},
    '43201': {'city': 'Columbus', 'state': 'OH', 'rate': 0.0775},
    '73101': {'city': 'Oklahoma City', 'state': 'OK', 'rate': 0.0875},
    '97301': {'city': 'Salem', 'state': 'OR', 'rate': 0.00},
    '02901': {'city': 'Providence', 'state': 'RI', 'rate': 0.07},
    '29201': {'city': 'Columbia', 'state': 'SC', 'rate': 0.09},
    '57501': {'city': 'Pierre', 'state': 'SD', 'rate': 0.06},
    '37201': {'city': 'Nashville', 'state': 'TN', 'rate': 0.0975},
    '84101': {'city': 'Salt Lake City', 'state': 'UT', 'rate': 0.0725},
    '05601': {'city': 'Montpelier', 'state': 'VT', 'rate': 0.06},
    '23218': {'city': 'Richmond', 'state': 'VA', 'rate': 0.06},
    '98501': {'city': 'Olympia', 'state': 'WA', 'rate': 0.09},
    '25301': {'city': 'Charleston', 'state': 'WV', 'rate': 0.07},
    '53701': {'city': 'Madison', 'state': 'WI', 'rate': 0.055},
    '82001': {'city': 'Cheyenne', 'state': 'WY', 'rate': 0.05},
}

def get_threshold(state_code):
    return NEXUS_RULES.get(state_code, NEXUS_RULES['DEFAULT'])

def calculate_tax(zip_code, amount):
    # Check if there are custom uploaded zip codes in session state
    if 'custom_zips' in st.session_state and zip_code in st.session_state.custom_zips:
        data = st.session_state.custom_zips[zip_code]
        tax_amt = amount * data['rate']
        return data, tax_amt
    
    # Fall back to built-in ZIP_RATES
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
    
    # CSV Upload Feature
    with st.expander("📁 Upload Custom Zip Codes (CSV)", expanded=False):
        st.markdown("Upload a CSV file with your own zip codes to expand the database.")
        st.markdown("**Format:** `zip_code,city,state,rate` (rate as decimal, e.g., 0.0825 for 8.25%)")
        
        uploaded_csv = st.file_uploader("Choose CSV file", type=['csv'], key="zip_upload")
        
        if uploaded_csv is not None:
            try:
                custom_df = pd.read_csv(uploaded_csv)
                
                # Validate columns
                required_cols = ['zip_code', 'city', 'state', 'rate']
                if all(col in custom_df.columns for col in required_cols):
                    # Convert to dictionary format and store in session state
                    custom_zips = {}
                    for _, row in custom_df.iterrows():
                        custom_zips[str(row['zip_code'])] = {
                            'city': row['city'],
                            'state': row['state'],
                            'rate': float(row['rate'])
                        }
                    
                    st.session_state.custom_zips = custom_zips
                    st.success(f"✅ Loaded {len(custom_zips)} custom zip codes!")
                    st.info(f"Total available: {len(ZIP_RATES)} built-in + {len(custom_zips)} custom = {len(ZIP_RATES) + len(custom_zips)} zip codes")
                else:
                    st.error(f"❌ CSV must have columns: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"❌ Error reading CSV: {e}")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        input_zip = st.text_input("Zip Code (Try 60601, 90210, 10001, or 50+ more)", max_chars=5)
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
            st.error(f"❌ Zip Code '{input_zip}' not in database. Upload a CSV or try: 60601 (Chicago), 90210 (Beverly Hills), 10001 (NYC).")