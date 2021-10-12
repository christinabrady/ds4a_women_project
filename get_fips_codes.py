## short script to scrape FIPS codes from an html table
## on a USDA site

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_fips_table():
    '''this function scrapes the
    table of FIPS codes on this website
    https://www.nrcs.usda.gov/wps/portal/nrcs/detail/or/programs/?cid=nrcs143_013697.
    It feeds the get_fips() and get_county() functions
    '''
    link = "https://www.nrcs.usda.gov/wps/portal/nrcs/detail/or/programs/?cid=nrcs143_013697"
    dfs = pd.read_html(link)
    return(dfs[0])

def get_fips(state_list=None, county_list=None):
    fips_table = get_fips_table()
    if state_list:
        if county_list:
            print("Please enter a list of states OR a list of counties, not both")
        else:
            filtered_fips_table = fips_table[fips_table.State.isin(state_list)]
            return(filtered_fips_table)
    else:
        if county_list:
            filtered_fips_table = fips_table[fips_table.Name.isin(county_list)]
            return(filtered_fips_table)
        else:
            print("Please enter a list of states OR a list of counties")


## testing
# get_fips(["AL", "AR"])
# get_fips(county_list = ["Atlantic"])
## to dos: check for a list rather than a string


def get_county(fips_codes_list):
    fips_table = get_fips_table()
    filtered_fips_table = fips_table[fips_table.FIPS.isin(fips_codes_list)]
    return(filtered_fips_table)

## testing
# get_county(["34001"])
