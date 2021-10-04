#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Preprocess datasets

"""

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