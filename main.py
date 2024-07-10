import requests
import concurrent.futures


def findProductsPerPage():
    pageNr = 1
    nSales = 0
    minimumDiscount = 30

    style = """
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; border-top: 1px solid #ddd; }
        tr:nth-child(even) {background-color: #f9f9f9;}
        tr:nth-child(odd) {background-color: #ffffff;}
        img { height: 150px; }
    </style>
    """

    responsePage = f"<html><head>{style}</head><body><h1>Products</h1><table><tr><th>Item</th><th>Image</th><th>URL</th></tr>"

    while pageNr < 334:
        print(f"Checking page {pageNr}")

        url = f"https://www.tigros.it/ebsn/api/products?page={pageNr}"
        base = "https://www.tigros.it"
        response = requests.get(url).json()

        for product in response["data"]["products"]:
            if "warehousePromo" in product and \
                ((product["warehousePromo"]["warehousePromoTypeId"] == 5 and product["warehousePromo"].get("discountPerc", 0) >= minimumDiscount) or \
                (product["warehousePromo"]["warehousePromoTypeId"] == 6)):
                
                itemUrl = product["itemUrl"]
                name = product["name"]
                imageUrl = product["mediaURLMedium"]
                nSales += 1
                print(f"Found {nSales} items on sale")
                responsePage += f"<tr><td>{name}</td><td><img src='{imageUrl}'></td><td><a href='{base + itemUrl}'>{base + itemUrl}</a></td></tr>"

        pageNr += 1
    
    responsePage += "</table></body></html>"
    with open("products.html", "w") as file:
        file.write(responsePage)


def checkPromo(url):
    base = "https://www.tigros.it"
    response = requests.get(url).json()

    if "warehousePromo" in response["data"]:
        itemUrl = response["data"]["itemUrl"]
        name = response["data"]["name"]
        print("*** Item on sale ***")
        print(f"Item: {name}")
        print(f"URL: {base + itemUrl}")

findProductsPerPage()
