import requests
from bs4 import BeautifulSoup as bs
from lavanda_del_lago.functools import *
       
def scraper():
    
    global URL 
    URL = "https://www.lavandadellago.it/it/store/"

    #use requests and bs4 to retrieve the product categories and their url query
    store_page = requests.get(URL)
    soup = bs(store_page.content, "lxml")
    LdL_linee = soup.find_all(class_="btn-category")

    LdL_linee = elementi(LdL_linee) #list of all product categories with dictionary {name:'',url_query:''}    
    LdL_linee.pop(0) #remove "Tutti" category
    
    catalogue = (category_scraper(LdL_linee))
    return product_scraper(catalogue)