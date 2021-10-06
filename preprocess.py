#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Preprocess datasets

"""

import pandas as pd 

def get_restaurants_usa(yelp_business):
    """Extract restaurant business located in the U.S.
    
       yelp_business: a pd dataframe of yelp business dataset
       return a dataframe of restaurants in the U.S.
    """
    
    # identify key words in 'categories'
    include_restaurant = yelp_business['categories'].str.contains('Restaurants', na = False)
    include_hotels = yelp_business['categories'].str.contains('Hotels', na = False)
    
    # extract restaurants from the business dataset
    # include entries that has key word 'Restaurants' but exclude entries that has key word 'Hotels'
    restaurants_df = yelp_business[include_restaurant & ~include_hotels]

    # non US states in Yelp business dataset
    non_us_states = ["ABE", "BC"]
    
    # extract US restaruants
    restaurants_us = restaurants_df[~restaurants_df['state'].isin(non_us_states)]
    
    return restaurants_us


def get_top_cities(yelp_restaurants, n = 5):
    """Get top n cities with most number of restaurants
   
       yelp_restaurants: pd data frame containing yelp restaurants
       n: an integer, number of top cities
       return a list containing names of top n cities
    """
    # by state and city: calculate the number of restaurants
    counted_by_city = yelp_restaurants.groupby(["state", "city"], as_index = False) \
    .agg({'business_id': 'count'}).sort_values(by = 'business_id', ascending = False)

    counted_by_city.columns = ['state', 'city','number_of_restaurants']

    # get the top n cities in the US
    top_n = counted_by_city.sort_values('number_of_restaurants', ascending = False).head(5)['city'].str.upper().tolist()

    return top_n



def get_ids_reviews_pre_covid(yelp_reviews):
    """Get business_ids of reviews posted before pandemic
    
       Cutoff of pre-pandemic period: Feb 1, 2020
       yelp_reviews: pd data frame containing yelp reviews
       return a data frame containing business ids that have at least one review before pandemic
    """

    yelp_reviews['date'] = pd.to_datetime(yelp_reviews['date'], format = '%Y-%m-%d')
    assert yelp_reviews['date'].dtype == 'datetime64[ns]'
   
    # filter the reviews by Feb 1, 2020
    filtered_df = yelp_reviews.loc[yelp_reviews['date'] <= '2020-02-01'] 

    # for this filtered reviews, get their business_ids
    ids_reviews_pre_covid = filtered_df.drop_duplicates(subset = 'business_id')[['business_id']]
   
    return ids_reviews_pre_covid 