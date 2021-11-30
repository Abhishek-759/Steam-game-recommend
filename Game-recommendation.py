import pandas as pd
import datetime
import os
import streamlit as st
import operator
from scipy import spatial

files = ['Dataset/1.csv', 'Dataset/2.csv', 'Dataset/3.csv', 'Dataset/4.csv', 'Dataset/5.csv', 'Dataset/6.csv',
         'Dataset/7.csv', 'Dataset/8.csv', 'Dataset/9.csv', 'Dataset/10.csv', 'Dataset/11.csv']

def data_analysis(file):
    df = pd.concat(map(pd.read_csv, file))

    df.drop(['review', 'unix_timestamp_created'], axis=1, inplace=True)
    df.rename(
        {'steamid': 'ID', 'appid': 'Game', 'voted_up': 'Positive', 'votes_up': 'Upvote', 'votes_funny': 'Downvote',
         'weighted_vote_score': 'Helpfulness', 'num_games_owned': 'Games owned', 'unix_timestamp_updated': 'Updated',
         'playtime_forever': 'Playtime'}, axis=1, inplace=True)
    df['ID'] = df['ID'].apply(str).str.replace('7656119', '')

    def datetoyear(unix):
        return int(datetime.datetime.fromtimestamp(int(unix)).strftime('%Y'))

    df.Updated = df.Updated.apply(datetoyear)

    df.drop(df[df['Games owned'] == 0].index, inplace=True)
    df.drop(df[df['Playtime'] == 0].index, inplace=True)

    bins = [0, 50, 100, 250, 500, 1000, 2000, 5000, 10000, 15000, 25000]
    labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    df['Gamer Rating'] = pd.cut(df['Games owned'], bins=bins, labels=labels)

    df['Played'] = df[['Playtime', 'playtime_at_review']].mean(axis=1)

    df.drop(['Games owned', 'Playtime', 'playtime_at_review'], axis=1, inplace=True)

    df["Positive"] = df["Positive"].astype(int)

    def minus(x):
        if x == 0:
            return x - 1
        else:
            return x

    df.Positive = df.Positive.apply(minus)

    df['Overall Rating'] = ((df['Upvote'] / (df['Upvote'] + df['Downvote'])) * df['Positive']) * df['Helpfulness']
    df.drop(['Positive', 'Upvote', 'Downvote', 'Helpfulness', 'num_reviews'], axis=1, inplace=True)

    df1 = df.groupby(['ID', 'Game']).max('Played')['Played']
    df1 = pd.DataFrame(df1)
    df1.reset_index(inplace=True)
    df1.drop(['ID'], axis=1, inplace=True)

    df_all_time = df1.groupby(['Game'])['Played'].sum()
    df_all_time = pd.DataFrame(df_all_time)
    df_all_time.reset_index(inplace=True)
    df_all_time = df_all_time.sort_values(by=['Played'], ascending=False)
    df_all_time.drop(['Played'], axis=1, inplace=True)

    df2 = df[df.Updated >= 2020].drop(['ID', 'Gamer Rating', 'Played', 'Overall Rating', 'Updated'], axis=1)
    df_trending = df2.pivot_table(index=['Game'], aggfunc='size')
    df_trending = pd.DataFrame(df_trending)
    df_trending = df_trending.sort_values(by=[0], ascending=False)
    df_trending.reset_index(inplace=True)
    df_trending.drop([0], axis=1)

    df_3 = df[df['Gamer Rating'] > '6']
    df_3.drop(['ID', 'Updated', 'Gamer Rating', 'Overall Rating'], axis=1)
    df_crit = pd.DataFrame(df_3.groupby(['Game'])['Played'].sum().reset_index()).sort_values(by='Played',
                                                                                             ascending=False).drop(
        ['Played'], axis=1)

    df4 = df.drop(['ID', 'Updated', 'Gamer Rating', 'Played'], axis=1)
    df_rating = pd.DataFrame(df4.groupby(['Game'])['Overall Rating'].sum().reset_index()).sort_values(
        by='Overall Rating',
        ascending=False).drop(
        ['Overall Rating'], axis=1)

    df_rating.to_csv('Output/Highest Rated.csv', index=False)
    df_trending.to_csv('Output/Trending.csv', index=False)
    df_all_time.to_csv('Output/All-time Hit.csv', index=False)
    df_crit.to_csv('Output/Critics Favorite.csv', index=False)


def binary(genre_list):
    binaryList = []

    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


def binary_category(categorie_list):
    binaryList = []

    for category in categories:
        if category in categorie_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


def Similarity(Id1, Id2):
    gameId1 = df_game_desc[df_game_desc['Game'] == Id1].index.values[0]
    gameId2 = df_game_desc[df_game_desc['Game'] == Id2].index.values[0]
    a = df_game_desc.iloc[gameId1]
    b = df_game_desc.iloc[gameId2]

    genresA = a['genres_bin']
    genresB = b['genres_bin']

    genreDistance = spatial.distance.cosine(genresA, genresB)

    catA = a['category_bin']
    catB = b['category_bin']
    categDistance = spatial.distance.cosine(catA, catB)

    return genreDistance + categDistance


df_game_desc = pd.DataFrame()
genreList = []
categories = []


def KNN_recommend():
    global df_game_desc
    df_desc = pd.read_csv('steam.csv')
    ratings = pd.read_csv('Output/Highest Rated.csv')
    df_game_desc = ratings.merge(df_desc, how='left', on='Game')

    for index, row in df_game_desc.iterrows():
        cat = row["categories"]
        cat = cat.split(";")
        for categ in cat:
            if categ not in categories:
                categories.append(categ)

    for index, row in df_game_desc.iterrows():
        genres = row["genres"]
        genres = genres.split(";")
        for genre in genres:
            if genre not in genreList:
                genreList.append(genre)

    df_game_desc['genres_bin'] = df_game_desc['genres'].apply(lambda x: binary(x))
    df_game_desc['category_bin'] = df_game_desc['categories'].apply(lambda x: binary_category(x))


def getNeighbors(baseGame, K):
    distances = []

    for index, Game in df_game_desc.iterrows():
        if Game['Game'] != baseGame['Game'].values[0]:
            dist = Similarity(baseGame['Game'].values[0], Game['Game'])
            distances.append((Game['Game'], dist))

    distances.sort(key=operator.itemgetter(1))
    neighbors = []

    for x in range(K):
        neighbors.append(distances[x])
    return neighbors


def predict_score(names):
    new_game = df_game_desc[df_game_desc['name'].str.contains(names)].iloc[0].to_frame().T
    st.markdown('Selected Game: ' + new_game.name.values[0])
    K = 10
    neighbors = getNeighbors(new_game, K)
    st.markdown('\nRecommended Games: \n')
    for neighbor in neighbors:
        st.markdown(list(df_game_desc[df_game_desc.Game == neighbor[0]]['name'])[0])


KNN_recommend()
df_game_desc.name = df_game_desc.name.str.lower()

flag = 0
if os.path.exists('Output/Highest Rated.csv') is False:
    flag = 1
if os.path.exists('Output/Trending.csv') is False:
    flag = 1
if os.path.exists('Output/All-time Hit.csv') is False:
    flag = 1
if os.path.exists('Output/Critics Favorite.csv') is False:
    flag = 1

if flag == 1:
    data_analysis(files)

label1 = "Select your preference for recommendation"
options1 = ['', 'Highest Rated', 'Trending', 'All-time Hit', 'Critics Favorite']

label2 = "Show top:"

st.title('Game Recommendation for Steam')
preference = st.selectbox(label1, options1)
Number = st.number_input(label2, min_value=10, max_value=50, step=10)

if preference != '':
    string = 'Showing top ' + str(Number) + ' ' + preference + ' Games'
    st.markdown(string)
    path = preference + '.csv'
    df = pd.read_csv(path)
    for i in range(Number):
        game_id = df.iloc[i]['Game']
        url = 'https://steamdb.info/app/' + str(df.iloc[i]['Game']) + '/'
        name = list(df_game_desc[df_game_desc['Game'] == game_id].name)[0]
        link = f'[{name}]({url})'
        st.markdown(link, unsafe_allow_html=True)
else:
    st.markdown('Please select a preference or search below.')
    game_name = st.text_input("Search the game name", placeholder='ex: Counter-strike, Counter, Strike...')
    game_name = game_name.lower()
    if game_name == '':
        st.markdown('Please enter valid game id.')
    else:
        try:
            named = df_game_desc[df_game_desc['name'].str.contains(game_name)].iloc[0].to_frame().T
            if df_game_desc['name'].str.contains(named.name.values[0]).any():
                predict_score(game_name)
        except IndexError:
            st.markdown('Please enter valid game.')


