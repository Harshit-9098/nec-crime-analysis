import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Crime Rate Analysis Dashboard", page_icon="📊", layout="wide")
@st.cache_data
def load_data():
    return pd.read_csv("01_District_wise_crimes_committed_IPC_2001_2012.csv")
df = load_data()
st.title("📊 Crime Rate Analysis Dashboard")
st.markdown("**Statistical Data Analysis of Recorded IPC Crimes in India (2001–2012)**")
st.divider()
crime_columns = [
    "MURDER", "ATTEMPT TO MURDER", "RAPE", "KIDNAPPING & ABDUCTION",
    "ROBBERY", "BURGLARY", "THEFT", "RIOTS", "ARSON", "DOWRY DEATHS"
]
st.sidebar.header("🔎 Dashboard Filters")
years = sorted(df["YEAR"].unique())
states = sorted(df["STATE/UT"].unique())

selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)
selected_states = st.sidebar.multiselect("Select State/UT", states, default=[])
selected_crime = st.sidebar.selectbox("Select Crime Category", crime_columns)

filtered_df = df[df["YEAR"].isin(selected_years)].copy()

if selected_states:
    filtered_df = filtered_df[filtered_df["STATE/UT"].isin(selected_states)]

total_crimes = int(filtered_df["TOTAL IPC CRIMES"].sum())
records = len(filtered_df)
state_count = filtered_df["STATE/UT"].nunique()
average = filtered_df["TOTAL IPC CRIMES"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Recorded IPC Crimes", f"{total_crimes:,}")
c2.metric("District-Year Records", f"{records:,}")
c3.metric("States/UTs", f"{state_count:,}")
c4.metric("Average Crimes / Record", f"{average:,.0f}")

st.divider()

# Year-wise trend
st.subheader("📈 Year-wise Crime Trend")
yearly = filtered_df.groupby("YEAR")["TOTAL IPC CRIMES"].sum()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(yearly.index, yearly.values, marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("Total Recorded IPC Crimes")
ax.set_title("Year-wise Total Recorded IPC Crimes")
ax.grid(True, alpha=0.3)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# Top states and selected crime
c1, c2 = st.columns(2)

with c1:
    st.subheader("🏛️ Top 10 States/UTs")
    state_totals = filtered_df.groupby("STATE/UT")["TOTAL IPC CRIMES"].sum().sort_values(ascending=False).head(10).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    state_totals.plot(kind="barh", ax=ax)
    ax.set_xlabel("Total Recorded IPC Crimes")
    ax.set_title("Top 10 States/UTs")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
with c2:
    st.subheader(f"🔍 {selected_crime} — Top 10 States/UTs")
    crime_state = filtered_df.groupby("STATE/UT")[selected_crime].sum().sort_values(ascending=False).head(10).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    crime_state.plot(kind="barh", ax=ax)
    ax.set_xlabel("Recorded Cases")
    ax.set_title(f"Top 10 States/UTs — {selected_crime}")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
# Crime categories
st.subheader("📊 Crime Category Distribution")
category_totals = filtered_df[crime_columns].sum().sort_values()
fig, ax = plt.subplots(figsize=(11, 5))
category_totals.plot(kind="barh", ax=ax)
ax.set_xlabel("Total Recorded Cases")
ax.set_title("Recorded Cases by Crime Category")
st.pyplot(fig, use_container_width=True)
plt.close(fig)
# Selected crime trend
st.subheader(f"📉 Year-wise Trend — {selected_crime}")
selected_yearly = filtered_df.groupby("YEAR")[selected_crime].sum()
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(selected_yearly.index, selected_yearly.values, marker="o")
ax.set_xlabel("Year")
ax.set_ylabel("Recorded Cases")
ax.set_title(f"Year-wise {selected_crime} Cases")
ax.grid(True, alpha=0.3)
st.pyplot(fig, use_container_width=True)
plt.close(fig)
# Correlation
st.subheader("🔗 Crime Category Correlation")
corr = filtered_df[crime_columns].corr()
fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap of Crime Categories")
st.pyplot(fig, use_container_width=True)
plt.close(fig)
# Data table
st.subheader("📋 Filtered Dataset")
cols = ["STATE/UT", "DISTRICT", "YEAR", selected_crime, "TOTAL IPC CRIMES"]
st.dataframe(
    filtered_df[cols].sort_values("TOTAL IPC CRIMES", ascending=False),
    use_container_width=True,
    height=350
)
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data", csv, "filtered_crime_data.csv", "text/csv")
st.divider()
st.caption("Crime Rate Analysis Using Statistical Data Analysis and Python | Historical descriptive analysis, 2001–2012 | No prediction.")