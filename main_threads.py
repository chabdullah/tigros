import requests
import concurrent.futures

ignoredProducts = []
with open("ignoreProducts.txt", "r") as file:
    for line in file:
        ignoredProducts.append(line.strip())

def isItemIgnored(productUrl):
    return productUrl in ignoredProducts


def findProductsOnPage(pageNr, base, minimumDiscount):
    print(f"Checking page {pageNr}")
    url = f"{base}/ebsn/api/products?page={pageNr}"
    response = requests.get(url).json()
    pageContent = ""

    for product in response["data"]["products"]:
        if "warehousePromo" in product:
            itemUrl = product["itemUrl"]
            if isItemIgnored(base+itemUrl):
                continue
            name = product["name"]
            imageUrl = product["mediaURLMedium"]
            pageContent += f"<tr><td>{name}</td><td><img src='{imageUrl}'></td><td><a href='{base + itemUrl}'>{base + itemUrl}</a></td><td><button onclick='deleteRow(this, \"{base + itemUrl}\")'>X</button></td></tr>"

    return pageContent

def findProductsPerPage():
    pageNr = 1
    nPages = 334
    minimumDiscount = 30
    base = "https://www.tigros.it"
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
    script = """
    <script>
        function deleteRow(button, itemUrl) {
            // Navigate up to the parent row and remove it
            var row = button.parentNode.parentNode;
            row.parentNode.removeChild(row);
            console.log(itemUrl);
        }
        function filterProducts() {
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById("searchBar");
            filter = input.value.toUpperCase();
            table = document.getElementById("productsTable");
            tr = table.getElementsByTagName("tr");

            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td")[2]; // Column index for product name
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }       
            }
        }
    </script>
    """
    responsePage = f"<html><head>{style}{script}</head><body><h1>Products</h1>"
    responsePage += 'Cerca <input type="text" id="searchBar" onkeyup="filterProducts()" placeholder="Nome prodotto...">'
    responsePage += "<table id='productsTable'><tr><th>Item</th><th>Image</th><th>URL</th><th>Action</th></tr>"

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(findProductsOnPage, pageNr + i, base, minimumDiscount) for i in range(nPages)]
        for future in concurrent.futures.as_completed(futures):
            responsePage += future.result()

    responsePage += "</table></body></html>"
    with open("products.html", "w") as file:
        file.write(responsePage)

findProductsPerPage()
