import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import preprocessor,Helper

df = preprocessor.preprocessor()

st.sidebar.title('OLYMPIC ANALYZER')
st.sidebar.image(r"C:\Users\kushw\Downloads\olympic_-rings_-transparent_-background-png-5ssh2hbbi85o1xrw-2-removebg-preview (1) (1).png")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis','Athlete-Wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    year,country = Helper.country_year_select(df)
    selected_year = st.sidebar.selectbox('Select Year',year)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = Helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_country == 'All Countries' and selected_year == 'Overall':
        st.header('Overall Analysis')

    if selected_country != 'All Countries' and selected_year == 'Overall':
        st.header(selected_country +' '+ str(selected_year) + ' Performance')

    if selected_country == 'All Countries' and selected_year != 'Overall':
        st.header('Performance of All Countries in ' + str(selected_year))

    if selected_country != 'All Countries' and selected_year != 'Overall':
        st.header(selected_country +"'s" + " Performance in " +' '+ str(selected_year))

    st.table(medal_tally)



if user_menu == 'Overall Analysis':
    st.title('Top Statistics')


    edition = df['Year'].unique().shape[0]
    host = df['City'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athlete = df['Name'].unique().shape[0]
    countries = df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(edition)
    with col2:
        st.header('Host')
        st.title(host)
    with col3:
        st.header('Sports')
        st.title(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(event)
    with col2:
        st.header('Athletes')
        st.title(athlete)
    with col3:
        st.header('Nations')
        st.title(countries)

    nations_count_per_year = Helper.nations_per_year(df)


    st.title('Participating Nations Over The Years')
    fig = px.line(nations_count_per_year, x='Year', y='count')
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Nations Per Year",
    )
    st.plotly_chart(fig)

    st.title("Events Over The Years")
    events_over_the_years = Helper.events_per_year(df)
    fig = px.line(events_over_the_years, x='Year', y='Events')
    st.plotly_chart(fig)

    st.title("Athletes Over The Years")
    athletes_over_the_years = Helper.athletes_per_year(df)
    fig = px.line(athletes_over_the_years, x='Year', y='Athletes')
    st.plotly_chart(fig)


    st.title("Most Decorated Athletes")
    sport = df['Sport'].unique().tolist()
    sport.sort()
    sport.insert(0, 'Overall')
    select_sport = st.selectbox("Select Sport", sport)
    data = Helper.most_decorated_athlete(df, select_sport)
    st.table(data)

if user_menu== 'Country-Wise Analysis':
    st.title('Country Wise Analysis')
    country_name = Helper.select_country(df)
    selected_country = st.sidebar.selectbox('Select Country', country_name)

    if selected_country == 'None':
        st.header('Select a County to See Their Performance over the Years')

    elif selected_country != 'All Countries':
        st.header('Performance of ' + selected_country +' Over The Years')

        df_copy = df.copy()
        df_copy = df_copy.dropna(subset=['Medal'])
        df_copy = df_copy.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        df_copy['Total'] = df_copy['Gold'] + df_copy['Silver'] + df_copy['Bronze']
        temp_df = df_copy[df_copy['region'] == selected_country]
        temp_df = temp_df.groupby('Year').sum()['Total'].reset_index()
        fig = px.line(temp_df, x='Year', y='Total')
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Medals",
        )
        st.plotly_chart(fig)

        st.title(selected_country + ' Excels in the following Sports')

        heat_df = Helper.country_sport(df, selected_country)
        fig, ax = plt.subplots(figsize = (20,20))
        ax = sns.heatmap(heat_df, annot=True, cmap="Blues")
        st.pyplot(fig)

        st.title('Top 10 Athletes of ' + selected_country)
        athlete_data =  Helper.country_top_athletes(df, selected_country)
        st.table(athlete_data)


if user_menu== 'Athlete-Wise Analysis':
    st.title('Age Distribution')
    x1,x2,x3,x4 = Helper.athlete_age_analysis(df)
    fig = ff.create_distplot([x1, x2, x3, x4],
                             group_labels=['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(
        xaxis_title='Age',
        yaxis_title='Probability',
        title='Distribution of Athlete Ages'
    )
    st.plotly_chart(fig)

    st.title('Age Distribution w.r.t Gold Medalists')
    st.header('(in most popular sports)')
    x, name = Helper.athlete_gold_age_analysis(df)
    fig = ff.create_distplot(x, name, show_rug=False, show_hist=False)
    fig.update_layout(
        xaxis_title='Age',
        yaxis_title='Probability',
    )
    st.plotly_chart(fig)

    st.title('Height vs Weight Analysis in various Sports')
    sport = df['Sport'].unique().tolist()
    sport.sort()
    sport.insert(0, 'Overall')
    select_sport = st.selectbox("Select Sport", sport)

    scatter_data = Helper.scatter_plot_data(df, select_sport)
    fig, ax = plt.subplots(figsize = (5,5))
    sns.scatterplot(data= scatter_data, x='Weight', y='Height', hue='Medal', style='Sex', s=30)
    st.pyplot(fig)

    st.title('Participation of Male and Female Athletes over the Years')
    final_df = Helper.men_women_plot(df)
    fig = px.line(final_df.melt(id_vars='Year', value_vars=['Male', 'Female'], var_name='Gender', value_name='Count'),
                  x='Year', y='Count', color='Gender',
        color_discrete_map = {
        'Male': 'blue',
        'Female': 'hotpink'}
    )
    st.plotly_chart(fig)
