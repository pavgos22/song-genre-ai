import os

import pandas as pd

def merge_databases(lyrics_database, artists_database):
    lyrics_database = lyrics_database[lyrics_database['language'] == 'en']
    merged = pd.merge(lyrics_database, artists_database, left_on='ALink', right_on='Link')
    columns_to_drop = ['SLink', 'language', 'Songs', 'Popularity']
    merged = merged.drop(columns=columns_to_drop)
    desired_columns = ['ALink', 'Link', 'SName', 'Lyric', 'Artist', 'Genres']
    merged = merged[desired_columns]
    columns_to_drop = ['ALink', 'Link']
    merged = merged.drop(columns=columns_to_drop)

    os.makedirs('csv', exist_ok=True)

    merged.to_csv('csv/merged.csv', index=False)
    print(merged)


def split_database(df, version):
    dataframes = [pd.DataFrame(columns=df.columns) for _ in range(2)]

    for i, row in df.iterrows():
        file_index = i % 10
        if file_index == 4:
            file_index = 1
        elif file_index == 9:
            file_index = 1
        else:
            file_index = 0

        dataframes[file_index] = dataframes[file_index]._append(row)

    os.makedirs('csv', exist_ok=True)

    for i, df_file in enumerate(dataframes):
        if i == 0:
            df_file.to_csv(f'csv/training_database_{version}.csv', index=False)
        elif i == 1:
            df_file.to_csv(f'csv/test_database_{version}.csv', index=False)


def drop_nan_lyrics(database, dname, version):
    df = database.dropna(subset=['Genres'])
    os.makedirs('csv', exist_ok=True)
    df.to_csv(f'csv/{dname}_database_{version}.csv', index=False)


if __name__ == '__main__':
    database = pd.read_csv('csv/database_v36.csv')
    database1 = pd.read_csv('csv/training_database_v36.csv')
    database2 = pd.read_csv('csv/test_database_v36.csv')
    print(database1)
    print(database2)
