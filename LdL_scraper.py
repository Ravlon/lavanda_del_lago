import requests
from bs4 import BeautifulSoup as bs
import csv
#from lavanda_del_lago.functools import *
from string import whitespace

def white_strip(sentence:str)->str:
    """Strip single string of all whitespace characters"""
    returned_sentence = ""
    for char in sentence:
        if not char in whitespace:
            returned_sentence += char
    return returned_sentence

def setURL(*query_inputs):
    """create URL address with query for specific categories or products
    Special attention is paid to ensure that the '/it/store' string isn't duplicated"""
    url_query=list(query_inputs)
    for i in range(len(url_query)):
        if "/it/store/" in url_query[i]:
            url_query[i]=url_query[i].replace("/it/store/","")
    return URL + ''.join(url_query)

def elementi(soup_array):
    """Set a dictionary for each product category with it's name and specific url query address for later use"""
    categories = []
    for linea in soup_array:
        categories.append({'name':linea.get_text(),'url_query':linea.get("href")})
    return categories

def product_fields(url_query='',name='',category='',price='',code='',formato=''):
    """Set a dictionary for all the fields necessary for a product
    You can specify the value of any of the fields when you call it, everything else will be by default empy
    Use the keys for later specification as needed."""
    return {'url_query':url_query,'name':name,'category':category,'price':price,'code':code,'formato':formato}

def category_scraper(Linee_array):
    """Retrieve all products of each category through their url query.
    This operation is needed as the product pages do not containg the category info.
    While doing this we are able to retrieve for each product the value of the following fields:
            a.  name of product
            b.  url query specific to product
            c.  price of product
            d.  category of product"""
    catalogo = [] 
    for linea in Linee_array:
        print("Reperimento Prodotti della Linea ",linea['name'])
        page = 1
        while True:
            #print("Pagina ",pagina)
            category_query = setURL(linea['url_query'],"?page=",str(page))
            try:
                product_page = requests.get(category_query)
            except:
                #print("Exception raised")
                if page>1:
                    print("###\tERRORE: \tLinea ",linea['name']," scannerizzata fino a pagina ", page-1)
                else:
                    print("###\tERRORE: \tLinea ",linea['name'],": errore URL")
                break
            else:
                soup = bs(product_page.content,"lxml")
                products = []
                prod_info = soup.find_all("h3",class_="uk-text-center")
                prod_price = soup.find_all("a",class_="uk-button")
                prod_price = prod_price[:len(prod_info)]
                if len(prod_info)==len(prod_price):
                    for i in range(len(prod_info)):
                        products.append(product_fields( name=prod_info[i].a.get("title"),
                                                        category=linea['name'],
                                                        url_query=prod_info[i].a.get("href"),
                                                        price=white_strip(prod_price[i])))
                else:(
                    print(len(prod_info),"-",len(prod_price))
                    #print("="*30,"\n"," "*12,"Errore"," "*12,"\n","="*30))
                )
                if not(products): break
                catalogo.extend(products)
            page+=1
    return catalogo

def product_scraper(catalogo):
    """Retrieve the remaining info of a product from their specific url page.
    Info that is collected is the following:
            a.  product code
            b.  product size
    Product Size is at the moment limited to the products that have a specialised class for it, called spot. Other classes are at the moment ignored."""
    catalogo_size = len(catalogo)
    for (i,item) in enumerate(catalogo):
        print("Reperimento info del prodotto n°",i+1,"di ",catalogo_size, end='\r')
        product_query = setURL(item['url_query'])
        
        page = requests.get(product_query)
        soup = bs(page.content,"lxml")
        
        try:
            item['code'] = white_strip(soup.find(class_="code").get_text()).replace("Cod.","")
        except Exception:
            try:
                item['code'] = white_strip(soup.find(class_="h4").get_text()).replace("Cod.","")
            except Exception:
                item['code'] = 'n/a'
                print("ERRORE PRODOTTO SENZA CODICE: ", item['name'], "  \tquery: ", product_query)
        try: 
            item['formato'] = white_strip(soup.find(class_="spot").get_text()).replace("Quantità:","") #pane-bodu ws-content
        except Exception:
            item['formato'] = 'n/a'
        
    return catalogo
        
def main():
    
    global URL 
    URL = "https://www.lavandadellago.it/it/store/"

    #use requests and bs4 to retrieve the product categories and their url query
    store_page = requests.get(URL)
    soup = bs(store_page.content, "lxml")
    LdL_linee = soup.find_all(class_="btn-category")

    LdL_linee = elementi(LdL_linee) #list of all product categories with dictionary {name:'',url_query:''}    
    LdL_linee.pop(0) #remove "Tutti" category
    
    catalogue = (category_scraper(LdL_linee))
    prodotti = product_scraper(catalogue)
    ######################################
    #         Current Position           #
    ######################################

    # for item in prodotti:
    #     print(item)
    # input()

    #fields = ['Url Prodotto','Nome Prodotto','Linea Prodotto','Prezzo Prodotto','Codice Prodotto','Formato prodotto']  

    # with open("Catalogo.csv", "w") as f:
    #     write = csv.writer(f,delimiter = ';')
    #     write.writerow(fields)
    #     for row in prodotti:
    #         write.writerow(row)

if __name__ == "__main__":
    main()