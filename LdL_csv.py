import csv

def main(array_input):
    """Objectives:
        1. Update the Catalogo to have new products
        2. Update price of the older products and save the historical price
        3. Products not available anymore should be marked as such
        4. """







#############################
#         old func          #
#############################


    for item in prodotti:
       print(item)

    fields = ['Url Prodotto','Nome Prodotto','Linea Prodotto','Prezzo Prodotto','Codice Prodotto','Formato prodotto']  

    with open("Catalogo.csv", "w") as f:
    write = csv.writer(f,delimiter = ';')
    write.writerow(fields)
    for row in prodotti:
        write.writerow(row)