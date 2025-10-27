import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# --- Page Configuration --
st.set_page_config(page_title="Olympic Games Analysis", layout="wide")

# --- Database Connection and Data Fetching ---
@st.cache_data(ttl=600) # Cache data for 10 minutes
def fetch_data():
    try:
        engine = create_engine("mysql+pymysql://root:Working123data@localhost/Olympic_Games_History")
        # Using a SQL query to fetch all data from the table
        df = pd.read_sql("SELECT * FROM olympic_history", engine)
        
        # The 'Medal' column contains 'NA' for non-medalists. We'll replace it.
        df['Medal'] = df['Medal'].fillna('No Medal')
        
        return df
    except Exception as err:
        st.error(f"Error connecting to MySQL: {err}")
        return pd.DataFrame() # Return an empty DataFrame on error

df = fetch_data()

if df.empty:
    st.warning("Could not load data from the database. Please check your connection details and ensure the database is running.")
else:
    # --- Sidebar ---
    st.sidebar.title("Olympic Games Analysis")
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/1200px-Olympic_rings_without_rims.svg.png")

    user_menu = st.sidebar.radio(
        'Select an Option',
        ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete Analysis')
    )

    # --- Medal Tally Page ---
    if user_menu == 'Medal Tally':
        st.sidebar.header("Medal Tally Filters")
        years = ['Overall'] + sorted(df['Year'].unique().tolist(), reverse=True)
        countries = ['Overall'] + sorted(df['NOC'].unique().tolist())

        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_country = st.sidebar.selectbox("Select Country", countries)

        # Filter data based on selection
        temp_df = df.copy()
        if selected_year != 'Overall':
            temp_df = temp_df[temp_df['Year'] == selected_year]
        if selected_country != 'Overall':
            temp_df = temp_df[temp_df['NOC'] == selected_country]

        # Calculate medal tally , Only rows with medals
        medal_df = temp_df[temp_df['Medal'] != 'No Medal']
        
        # Group by NOC and count medals
        medal_tally = medal_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        medal_tally = medal_tally.groupby('NOC').agg(
            Gold=('Medal', lambda x: (x == 'Gold').sum()),
            Silver=('Medal', lambda x: (x == 'Silver').sum()),
            Bronze=('Medal', lambda x: (x == 'Bronze').sum())
        ).reset_index()

        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
        medal_tally = medal_tally.sort_values('Total', ascending=False)
        
        st.title("Medal Tally")
        st.header(f"Analysis for: {selected_country} - {selected_year}")
        st.dataframe(medal_tally, use_container_width=True)

    # # --- Overall Analysis Page ---
    if user_menu == 'Overall Analysis':
        editions = df['Year'].unique().shape[0]
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['NOC'].unique().shape[0]

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Editions", editions)
            st.metric("Hosts", cities)
        with col2:
            st.metric("Sports", sports)
            st.metric("Events", events)
        with col3:
            st.metric("Nations", nations)
            st.metric("Athletes", athletes)
            
        st.header("Participation Trends Over the Years")
        nations_over_time = df.drop_duplicates(['Year', 'NOC'])['Year'].value_counts().reset_index().sort_values('Year')
        nations_over_time.rename(columns={'Year':'Edition', 'count':'No. of Countries'}, inplace=True)
        fig = px.line(nations_over_time, x="Edition", y="No. of Countries", title="Participating Nations Over the Years")
        st.plotly_chart(fig, use_container_width=True)

        events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
        events_over_time.rename(columns={'Year':'Edition', 'count':'No. of Events'}, inplace=True)
        fig2 = px.line(events_over_time, x="Edition", y="No. of Events", title="Events Over the Years")
        st.plotly_chart(fig2, use_container_width=True)

    # --- Country-wise Analysis Page ---
    if user_menu == 'Country-wise Analysis':
        st.sidebar.header("Country-wise Filters")
        country_list = sorted(df['NOC'].unique().tolist())
        selected_country = st.sidebar.selectbox('Select a Country', country_list)

        country_df = df[df['NOC'] == selected_country]
        
        st.title(f"Analysis for {selected_country}")
        
        # Medals over time for the selected country
        country_medals = country_df[country_df['Medal'] != 'No Medal']
        medals_over_time = country_medals.groupby('Year')['Medal'].count().reset_index()
        fig = px.line(medals_over_time, x='Year', y='Medal', title=f'Medal Count for {selected_country} Over the Years')
        st.plotly_chart(fig, use_container_width=True)

        # Top sports for the selected country
        st.header(f"Top 10 Sports for {selected_country}")
        top_sports = country_medals['Sport'].value_counts().head(10)
        st.dataframe(top_sports)

    # --- Athlete Analysis Page ---
    if user_menu == 'Athlete Analysis':
        st.title("Distribution of Athlete Attributes")

        # Remember your script drops NA for Age, Height, Weight
        athlete_df = df.drop_duplicates(subset=['Name', 'NOC'])
        
        # Age distribution
        fig_age = px.histogram(athlete_df, x='Age', nbins=40, title="Age Distribution of Athletes")
        st.plotly_chart(fig_age, use_container_width=True)

        # Height vs. Weight
        sport_list = ['Overall'] + sorted(df['Sport'].unique().tolist())
        selected_sport = st.selectbox('Select Sport for Height vs Weight Analysis', sport_list)
        
        plot_df = athlete_df.copy()
        if selected_sport != 'Overall':
            plot_df = plot_df[plot_df['Sport'] == selected_sport]

        st.header("Height vs. Weight by Sex")
        fig_hvsw = px.scatter(plot_df, x='Weight', y='Height', color='Sex',
                                title=f"Height vs. Weight of Athletes ({selected_sport})",
                                labels={'Weight': 'Weight (kg)', 'Height': 'Height (cm)'})
        st.plotly_chart(fig_hvsw, use_container_width=True)
