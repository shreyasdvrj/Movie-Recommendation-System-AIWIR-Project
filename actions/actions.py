# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP

import numpy as np

import webbrowser
import time

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionMovieGenre(Action):

    def name(self):
        #type: () -> Text
        return "action_movie_genre"

    def run(self, dispatcher, tracker, domain):
            #tracker: Tracker
           # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        
        data = pd.read_csv('./movieEnglish.csv', low_memory=False)
        g=data['Genre']
        g.array
        m=data['Movie']
        m.array
        r=data['IMDb']
        r.array
        lg=[]
        lm=[]
        l3=[]
        d={}
        sorted_d={}
        for i in g:
            lg.append(i)
            
        for j in m:
            lm.append(j)
            
        given = tracker.latest_message["intent"].get("name")

        gen=''
        c=0
        reqd=[]
        for i in g:
            
            #print(i)
            gen=i.split(',')
            for k in gen:
                if given in k:
                    d[m[c]]=r[c]
                
            c+=1
       
        sorted_d = dict(sorted(d.items(),key=lambda kv: kv[1],reverse=True)[:10])
        key_list = list(sorted_d.keys())  
        val_list = list(sorted_d.values())
        '''sent_str = ""
        arr_length=len(key_list)
        for i in range(arr_length):
            sent_str += str(key_list[i]) + "   " + str(val_list[i]) + ">"
            k+=1
            
        sent_str = sent_str.split(">")'''
        index=0
        dispatcher.utter_message("Movies for genre {} are :\n".format(given))
        for i in key_list:
            dispatcher.utter_message("{} : {}\n".format(i,val_list[index]))
            index+=1

        return []

#-----------------------FOR PLOT BASED ------------------------

class ActionMoviePlot(Action):

    def name(self):
        #type: () -> Text
        return "action_movie_plot"

    def run(self, dispatcher, tracker, domain):
            #tracker: Tracker
           # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        metadata = pd.read_csv('./movieEnglish.csv', low_memory=False)

        
        tfidf = TfidfVectorizer(stop_words='english')
        metadata['Description'] = metadata['Description'].fillna('')
        tfidf_matrix = tfidf.fit_transform(metadata['Description'])

        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(metadata.index, index=metadata['Movie']).drop_duplicates()

        def get_recommendations(title, cosine_sim=cosine_sim):
            idx = indices[title]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]
            movie_indices = [i[0] for i in sim_scores]
            return metadata['Movie'].iloc[movie_indices]

        movie=tracker.latest_message.get('text')
        #print("Workssssssssss")
        
        '''sent_str = ""
        arr_length=len(key_list)
        for i in range(arr_length):
            sent_str += str(key_list[i]) + "   " + str(val_list[i]) + ">"
            k+=1
            
        sent_str = sent_str.split(">")'''
        obj=get_recommendations(movie)
        count=1
        dispatcher.utter_message("The recommendations for {} are :".format(movie))
        for i in obj.array:
            dispatcher.utter_message("{}. {}\n".format(count,i))
            count+=1

        return []

#----------------------------RATINGS------------------

class ActionMovieRatings(Action):

    def name(self):
        #type: () -> Text
        return "action_movie_ratings"

    def run(self, dispatcher, tracker, domain):
            #tracker: Tracker
           # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        
        data = pd.read_csv('./movieEnglish.csv', low_memory=False)
        dr={} 
        g=data['Genre']
        g.array
        m=data['Movie']
        m.array
        r=data['IMDb']
        r.array
        c=0
        for i in r:
            dr[m[c]]=r[c]
            c+=1
    
        sorted_rate =dict(sorted(dr.items(),key=lambda kv: kv[1],reverse=True)[:10])


        key_list = list(sorted_rate.keys()) 
        val_list = list(sorted_rate.values())

        k=0
        s=''
        final=[]
        print("In action")
        '''sent_str = ""
        arr_length=len(key_list)
        for i in range(arr_length):
            sent_str += str(key_list[i]) + "   " + str(val_list[i]) + ">"
            k+=1
            
        sent_str = sent_str.split(">")'''
        index=0
        for i in key_list:
            dispatcher.utter_message("{} : {}\n".format(i,val_list[index]))
            index+=1

        return []

#----------------------------Movies based on mood---------------
class ActionMovieRMood(Action):

    def name(self):
        #type: () -> Text
        return "action_movie_mood"

    def run(self, dispatcher, tracker, domain):
            #tracker: Tracker
           # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # Main Function for scraping
        def main(emotion):
            # IMDb Url for Comedy Drama genre of
            # movie against emotion Sad
            if (emotion == "Sad"):
                urlhere = 'https://www.imdb.com/search/title/?title_type=feature&genres=comedy&sort=boxoffice_gross_us,desc&explore=genres'

            # IMDb Url for feel good genre of
            # movie against emotion Happy.
            elif (emotion == "Happy"):
                urlhere = 'https://www.imdb.com/list/ls068773014/?sort=user_rating,desc&st_dt=&mode=detail&page=1'

            # IMDb Url for Action and SciFi genre of
            # movie against emotion Excitement.
            elif (emotion == "Excitement"):
                urlhere = 'https://www.imdb.com/search/title/?count=100&genres=action&release_date=2019,2019&title_type=feature'

            # IMDb Url for Musical genre of
            # movie against emotion Disgust
            elif (emotion == "Disgust"):
                urlhere = 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter, asc'

            # IMDb Url for Family genre of
            # movie against emotion Anger
            elif (emotion == "Anger"):
                urlhere = 'https://www.imdb.com/list/ls076036380/?sort=user_rating,desc&st_dt=&mode=detail&page=1'

            # IMDb Url for Sport genre of
            # movie against emotion Fear
            elif (emotion == "Fear"):
                urlhere = 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter, asc'

            # IMDb Url for Thriller genre of
            # movie against emotion Enjoyment
            elif (emotion == "Enjoyment"):
                urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

            # IMDb Url for Top Rated Movies.
            # movie against no emotion entered.
            elif (emotion == ""):
                urlhere = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'

            # IMDb Url for Western genre of
            # movie against emotion Trust
            elif (emotion == "Trust"):
                urlhere = 'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter, asc'

            # IMDb Url for Film_noir genre of
            # movie against emotion Surprise
            elif (emotion == "Surprise"):
                urlhere = 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter, asc'

            # HTTP request to get the data of
            # the whole page
            response = HTTP.get(urlhere)
            data = response.text

            # Parsing the data using
            # BeautifulSoup
            soup = SOUP(data, "lxml")

            # Extract movie titles from the
            # data using regex
            title = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})
            return title


        # Driver Function


        emotion = tracker.latest_message["intent"].get("name")
        a = main(emotion)
        count = 0
        key_list=[]
        for i in a:
            tmp = str(i).split('>')

            if (len(tmp) == 3):
                key_list.append(tmp[1][:-3])

            if (count > 100):
                break
            count += 1

        index=0
        for i in key_list:
            dispatcher.utter_message("{}".format(i))
            index+=1
            if index>10:
                break
            
        return []      

#------------------------------Out of Scope ------------------

class ActionCustomFallBack(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_default")


    

        return []

#------------------------------------DETAILS------------------------------
class ActionMovieDetails(Action):

    def name(self):
        #type: () -> Text
        return "action_give_details"

    def run(self, dispatcher, tracker, domain):
            #tracker: Tracker
           # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("\n\n\n\n in movie details \n\n\n")
        given=tracker.latest_message.get('text')
        
        data = pd.read_csv('./movieEnglish.csv', low_memory=False)

        print("\n\n\naccepted here\n\n given is \t")
        #print(given)

        genre=data['Genre']
        genre.array
        movie=data['Movie']
        movie.array
        rating=data['IMDb']
        rating.array
        year=data['Year']
        year.array
        description=data['Description']
        description.array
        duration=data['Duration']
        duration.array
        director=data['Director']
        director.array
        cast=data['Cast']
        cast.array
        stream=data['Streaming']
        stream.array

        given_genre=[]
        given_rating=[]
        given_year=[]
        given_description=[]
        given_duration=[]
        given_director=[]
        given_cast=[]
        given_stream=[]

        l_genre=[]
        l_movie=[]
        l_rating=[]
        l_year=[]
        l_description=[]
        l_duration=[]
        l_director=[]
        l_cast=[]
        l_stream=[]

        for i in genre:
            l_genre.append(i)

        for i in movie:
            l_movie.append(i)

        for i in rating:
            l_rating.append(i)

        for i in year:
            l_year.append(i)

        for i in description:
            l_description.append(i)
            
        for i in duration:
            l_duration.append(i)

        for i in director:
            l_director.append(i)

        for i in cast:
            l_cast.append(i)

        for i in stream:
            l_stream.append(i)
        
        count=0
        x=0
        #print("\n\n\n\t x is assigned")
    
        for i in l_movie:
            #print("\n\n\t in loop")
            if ( i == given):
                given_genre.append(l_genre[x])
                given_rating.append(l_rating[x])
                given_year.append(l_year[x])
                given_description.append(l_description[x])
                given_duration.append(l_duration[x])
                given_director.append(l_director[x])
                given_cast.append(l_cast[x])
                given_stream.append(l_stream[x])

                dispatcher.utter_message("\t\t {} : \n".format(given))
                dispatcher.utter_message("\t Genre: {}  ".format(given_genre))
                dispatcher.utter_message("\t\t\t Ratings: {} \n".format(given_rating))
                dispatcher.utter_message("\t Release year:  {} \n".format(given_year[0]))
                dispatcher.utter_message("\t Description: {} \n".format(given_description[0]))
                dispatcher.utter_message("\tDuration:  {} minutes  \n".format(given_duration)[0])
                dispatcher.utter_message("\tDirector: {}  \n".format(given_director))
                dispatcher.utter_message("\tCast: {}  \n".format(given_cast))
                dispatcher.utter_message("\tStream: {}  \n".format(given_stream[0]))
                time.sleep(8)
                webbrowser.open_new_tab(given_stream[0])

                count=1
                
            if(count==1):
                break

            x+=1

        if(count!=1):
           dispatcher.utter_message(text="I'm sorry, I don't have that movie in my database :(") 
                
        return[]