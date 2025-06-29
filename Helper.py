import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally=medal_tally.groupby('NOC')[['Gold','Silver','Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Bronze'] + medal_tally['Gold'] + medal_tally['Silver']
    return medal_tally

def country_year_select(df):
    year = df['Year'].sort_values().unique().tolist()
    year.insert(0, 'Overall')

    country = df['region'].sort_values().unique().tolist()
    country.insert(0, 'All Countries')

    return year, country


def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'All Countries':
        temp_df = medal_df
    elif year == 'Overall' and country != 'All Countries':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'All Countries':
        year = int(year)
        temp_df = medal_df[medal_df['Year'] == year]
    elif year != 'Overall' and country != 'All Countries':
        year = int(year)
        temp_df = medal_df[(medal_df['Year'] == year)&(medal_df['region'] == country)]
    if flag == 1:
         x= temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year', ascending = True).reset_index()

    else:
        x= temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending = False).reset_index()

    x['Total']= x['Bronze'] + x['Gold'] + x['Silver']

    return x



def nations_per_year(df):
    country_per_year = df.drop_duplicates(subset=['Year', 'region'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    return country_per_year

def events_per_year(df):
    events_over_years = df.drop_duplicates(subset=['Year', 'Event'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    events_over_years.rename(columns={'count': 'Events'}, inplace=True)

    return events_over_years

def athletes_per_year(df):
    athletes_over_years = df.drop_duplicates(subset=['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    athletes_over_years.rename(columns={'count': 'Athletes'}, inplace=True)

    return athletes_over_years

def most_decorated_athlete(df, sport):

    df_medals = df.dropna(subset=['Medal'])
    df_medals = df_medals[['Name', 'Gold', 'Silver', 'Bronze', 'Sport', 'region']]

    if sport != 'Overall':
        df_medals = df_medals[df_medals['Sport'] == sport]

    grouped = df_medals.groupby('Name').agg({
        'Gold': 'sum',
        'Silver': 'sum',
        'Bronze': 'sum',
        'Sport': 'first',
        'region': 'first'
    }).reset_index()
    grouped['Total'] = grouped['Gold'] + grouped['Silver'] + grouped['Bronze']
    grouped = grouped.sort_values(by = ['Gold','Silver','Bronze'], ascending=False)
    grouped['Rank'] = range(1, len(grouped) + 1)
    grouped.set_index('Rank', inplace=True)
    cols = grouped.columns.tolist()
    cols.remove('Total')
    b_indx = cols.index('Bronze')
    cols.insert(b_indx+1, 'Total')
    grouped = grouped[cols]
    return grouped.head(20)

def select_country(df):
    country = df['region'].sort_values().unique().tolist()
    country.insert(0, 'None')
    return country

def country_sport(df,country):
    country_medals = df.dropna(subset=['Medal'])
    country_medals = country_medals.drop_duplicates(subset=['Name', 'Gold', 'Silver', 'Bronze', 'Sport', 'region'])
    country_medals = country_medals[country_medals['region'] == country]
    country_medals = country_medals.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return country_medals



def country_top_athletes(df,country):
    df_copy = df.copy()
    df_copy = df_copy.dropna(subset=['Medal'])
    df_copy = df_copy[df_copy['region'] == country]
    df_copy = df_copy.groupby('Name').agg({'Sport': 'first', 'Gold': 'sum',
                                           'Silver': 'sum',
                                           'Bronze': 'sum'}).reset_index()
    df_copy['Total'] = df_copy['Gold'] + df_copy['Silver'] + df_copy['Bronze']
    df_copy = df_copy.sort_values(by=['Gold', 'Silver', 'Bronze'], ascending=False)
    df_copy['Sr. No.'] = range(1, len(df_copy) + 1)
    df_copy.set_index('Sr. No.', inplace=True)

    return df_copy.head(10)

def athlete_age_analysis(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    return x1, x2, x3, x4

def athlete_gold_age_analysis(df):
    famous_sports = df['Sport'].value_counts().reset_index().head(10)['Sport'].tolist()
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        name.append(sport)
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    return x, name

def scatter_plot_data(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    if sport != 'Overall':
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        temp_df = temp_df.dropna(subset=['Height', 'Weight'])
        temp_df['Medal'].fillna('No Medal', inplace=True)
        return temp_df
    else:
        return athlete_df

def men_women_plot(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    male_df = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female_df = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    male_df.rename(columns={'Name': 'Male'}, inplace=True)
    female_df.rename(columns={'Name': 'Female'}, inplace=True)

    final_df = pd.merge(male_df, female_df, on='Year', how='left')
    final_df['Female'] = final_df['Female'].fillna(0).astype(int)
    final_df.sort_values('Year', inplace=True)
    return final_df
