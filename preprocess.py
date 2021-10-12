#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Preprocess datasets

"""

import pandas as pd 



def gen_categories_hotels(yelp_business):
    """Generate a list of categories that have keywords Hotels
    
       yelp_business: a pd dataframe of yelp business dataset
       return a list 
    """

    # identify businesses that tag themselves in 'Hotels' category
    include_categ_hotels = yelp_business['categories'].str.contains('Hotels', na = False)
    
    # extract those businesses
    hotels_df = yelp_business[include_categ_hotels]
    
    # create a raw version of the list
    hotels_categories_raw = []

    for item in hotels_df['categories']:
        my_list = item.split(',')
        for element in my_list:
            cleaned_element = element.strip()
            if not(cleaned_element in hotels_categories_raw):
                hotels_categories_raw.append(cleaned_element)

    # create a clean version of the list
    hotels_categories_clean = []

    for item in hotels_categories_raw:
        status = 'Hotels' in item
        if status:
            hotels_categories_clean.append(item)
            
    return hotels_categories_clean            
    
    
    
def check_categories(item, reference_list):
    """Check whether a category is within a list
    
       item: a string that contains elements separated by commas
       reference_list: a list containing reference elements
       return a boolean
    """
    
    a_list = item.split(',')
    for item in a_list:
        status = item.strip() in reference_list
        if status == True:
            return True
    return False



def get_restaurants_usa(yelp_business, category_tagged):
    """Extract restaurant business located in the U.S.
    
       yelp_business: a pd dataframe of yelp business dataset
       category_tagged: a string, the name of a csv file that contains a list of categories
       and an indicator whether the category will be excluded
       return a dataframe of restaurants in the U.S.
    """
    
    # identify businesses that tag themselves in 'Restaurant' category
    include_categ_restaurant = yelp_business['categories'].str.contains('Restaurants', na = False)
    
    # extract those businesses
    restaurant_raw_df = yelp_business[include_categ_restaurant]
    
    # load the category file
    category_df = pd.read_csv(category_tagged)
    
    # create a list of categories to exclude (note that 'Hotels' is not yet included)
    category_excluded = list(category_df[category_df['exclude'] == 1]['category'])
    
    # get a list of categories with keywords 'Hotels'
    hotel_categories = gen_categories_hotels(yelp_business)
    
    # append hotel categories to the list of categories to be excluded
    for category in hotel_categories:
        category_excluded.append(category)
        
    # create a new column to tag whether the businesses should be excluded
    condition = restaurant_raw_df.categories.apply(check_categories, args = (category_excluded,))
    restaurant_raw_df.loc[condition, 'not_restaurant'] = True
    restaurant_raw_df.loc[~condition, 'not_restaurant'] = False
    
    # subset only for businesses that are not tagged as non-restaurants
    restaurant_clean_by_categories = restaurant_raw_df[restaurant_raw_df['not_restaurant'] == False]
    restaurants_df = restaurant_clean_by_categories.drop('not_restaurant', axis = 1)

    # non US states in Yelp business dataset
    non_us_states = ["ABE", "BC"]
    
    # extract US restaurants
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