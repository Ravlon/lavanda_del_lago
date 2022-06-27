#test for git pull

import requests
from bs4 import BeautifulSoup as bs
import csv

def manipol_linea(lista):
    url = []
    nome = []
    for item in lista:
        s_item = str(item)
        url_base="/it/store/"
        pos = int(s_item.find(url_base))
        stringa = s_item[pos+len(url_base):]
        a,b = stringa.split('">')
        url.append(a)
        nome.append(b[:-4])
    return url,nome

def manipol_prodotto(nome,prezzo,linea):
    url = []
    name = []
    for item in nome:
        s_item = str(item)
        url_base="/it/store"
        pos = int(s_item.find(url_base))
        stringa = s_item[pos+len(url_base):]
        a = stringa.split('"')
        url.append(a[0])
        name.append(a[-1])
    for item in range(len(name)):
        a = name[item].split("<")
        stringa = a[0]
        stringa = str(stringa[3:])
        stringa = str(stringa[:stringa.find("\r")])
        name[item] = stringa[24:]
    for item in range(len(prezzo)):
        a = str(prezzo[item]).split('">')
        a = a[-1].split("<")
        st_prezzo = str(a[0]).strip()
        pos_euro= st_prezzo.find("€")
        prezzo[item]= st_prezzo[:pos_euro+1]
    result = []
    for i in range(len(name)):
        result.append([url[i],name[i],linea,prezzo[i]])
    return result

def linea_scraper(l_url,l_nome,url):
    prodotto = [] 
    for num in range(len(l_url)):
        print("Collezione Prodotti della Linea ",l_nome[num])
        pagina = 1
        while True:
            #print("Pagina ",pagina)
            complete_url = url+l_url[num]+"?page="+str(pagina)
            try:
                linea = requests.get(complete_url)
            except:
                #print("Exception raised")
                if pagina>1:
                    print("Linea ",l_nome[num]," scannerizzata fino a pagina ",pagina-1)
                else:
                    print("###\tLinea ",l_nome[num],": errore URL")
                break
            else:
                soup = bs(linea.content,"html.parser")
                items = soup.find(class_="item item-page")
                s_name = items.find_all("h3", class_="portfolio-member-title uk-text-center")
                s_price = items.find_all("a", class_="uk-button uk-button-success uk-button")
                if not(s_name): break
                prodotto.extend(manipol_prodotto(s_name,s_price,l_nome[num]))
            pagina+=1
    return prodotto
            
def prodotti_scraper(products,url):
    for item in range(len(products)):
        print("Collezione specifiche per prodotto n°",item+1,"di ",len(products), end='\r')
        complete_url = url+products[item][0]
        page = requests.get(complete_url)
        soup = bs(page.content,"html.parser")
        code = str(soup.find(class_="code"))
        pos_cod_iniziale = code.find("Cod.")+5
        code = code[pos_cod_iniziale:]
        pos_cod_finale = code.find("\r")
        code = code[:pos_cod_finale]
        formato = soup.find(class_= "spot") #pane-body ws-content
        if formato is None:
            formato = 'n/a'
        l_formato = str(formato).split("\n")
        quant = "Quantità:"
        for line in l_formato:
            if quant in line:
                pos_quant = line.find(quant)+len(quant)+1
                formato = str(line[pos_quant:-1])
        products[item].extend([code,formato])
    return products
        


URL = "https://www.lavandadellago.it/it/store/"
page = requests.get(URL)

#f = open("C://Users//lucas//Desktop//LdL_html.txt", mode='w')
#f = open("C://Users//lucas//Desktop//LdL_html.txt", mode='x')
#f.write(page.text)

soup = bs(page.content, "html.parser")
html_lines = soup.find(id="categories")
linee = html_lines.find_all("a",class_="btn-category")

url_linea,nome_linea = manipol_linea(linee)
url_linea.pop(0) #remove main store page url
nome_linea.pop(0) #remove "Tutti" category

prodotti = linea_scraper(url_linea,nome_linea,URL)
prodotti = prodotti_scraper(prodotti,URL)    

# for item in prodotti:
    # print(item[1:])
# input()

fields = ['Url Prodotto','Nome Prodotto','Linea Prodotto','Prezzo Prodotto','Codice Prodotto','Formato prodotto']  

with open("C://Users//lucas//Desktop//Catalogo.csv", "w") as f:
    write = csv.writer(f,delimiter = ';')
    write.writerow(fields)
    for row in prodotti:
        write.writerow(row)
