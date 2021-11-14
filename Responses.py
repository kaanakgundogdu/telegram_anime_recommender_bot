from datetime import date, datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
df = pd.read_csv('rating.csv')
anime = pd.read_csv('anime.csv')


anime["name"] = anime["name"].str.lower()

df = pd.merge(df,anime.drop('rating',axis=1),on='anime_id')
df.groupby('name')['rating'].mean().sort_values(ascending=False).head(10)
df.groupby('name')['rating'].count().sort_values(ascending=False).head(10)
ratings = pd.DataFrame(df.groupby('name')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('name')['rating'].count())

genre_dict = pd.DataFrame(data=anime[['name','genre']])
genre_dict.set_index('name',inplace=True)


def sample_Responses(input_text):
    user_message=str(input_text).lower()

    boolean_findings = anime['name'].str.contains(str(user_message))
    total_occurence = boolean_findings.sum()
    print(total_occurence)
    if(total_occurence > 0):
        print("recom")
        return get_recommendation(user_message)

    if user_message in ("sa","sa.","!sa","s.a.", "hi", "hello","sup"):
        return "As. kardes As."
    if user_message in ("kimsin sen", "sen kimsin","kimsin sen?", "sen kimsin?" ):
        return "Sa.ben anime önerme botuyum."
    
    if user_message in ("saat", "saat kaç", "tarih","time","time?"):
        now = datetime.now()
        date_time=now.strftime("%d/%m/%y, %H:%M:%S")
        return str(date_time)



    return "Bilemem kardeş bilemem!!!"



def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False
    
def get_recommendation(name):
    #generating list of anime with the same genre with target
    name=str(name)
    anime_genre = genre_dict.loc[name].values[0].split(', ')
    cols = anime[anime['genre'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['name'].tolist()
    
    #create matrix based on generated list
    animemat = df[df['name'].isin(cols)].pivot_table(
        index='user_id',columns='name',values='rating')
       
    #create correlation table
    anime_user_rating = animemat[name]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(ratings['num of ratings'])
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings']>5000].sort_values(
        'correlation',ascending=False)
        
    return str( corr_anime["correlation"].head(5))

    #return corr_anime.head(5)




#print(get_recommendation('naruto'))
