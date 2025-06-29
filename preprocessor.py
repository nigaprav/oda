import pandas as pd



def preprocessor():
    df = pd.read_csv(r"C:\Users\kushw\Downloads\athlete_events.csv\athlete_events.csv")
    reigon_df = pd.read_csv(r"C:\Users\kushw\Downloads\noc_regions.csv")


    df = df[df['Season'] == 'Summer']
    df = df.merge(reigon_df, on='NOC', how = 'left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype='int64')], axis=1)

    return df


