from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

# The destination URL to be scraped (This is newegg graphics cards)
myURL = "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics+cards"

uClient = uRequest(myURL)	# Opening the connection to the website, grabbing the page
pageHTML = uClient.read()	# Loading page contents into variable
uClient.close()				    # Close the connection 

# Parsing the webpage data with BS
pageSoup = soup(pageHTML, "html.parser")	

# Store each desired item to a list
containers = pageSoup.findAll("div", {"class":"item-cell"})

# Creating a new csv file to store data
fileName = "products.csv"      
f = open(fileName, 'w')

# Setting the headers for columns
headers = "brand, productName, price, shipPrice\n"

# Adding the headers to the csv file
f.write(headers)

# Loop through each item
for container in containers:
	# Getting the brand of the product
	brand = container.div.div.a.img["title"]

	# Getting the title of the product (Eg. NVIDIA 2080 SUPER)
	titleContainer = container.findAll("a", {"class":"item-title"})
	prodName = titleContainer[0].text

	# Getting the price information and stripping extras away
	priceContainer = container.findAll("li", {"class":"price-current"})
	dollar = priceContainer[0].strong.text.strip()  # Pulling Dollar amount
	cent = priceContainer[0].sup.text.strip()       # Pulling cent amount
	price = dollar + cent                           # Combine the price

	# Getting the shipping price
	shippingContainer = container.findAll("li", {"class":"price-ship"})
	shipPrice = shippingContainer[0].text.strip()

	# Printing the aquired data to the console 
	print("Brand: " +  brand)
	print("Name: " +  prodName.replace(",", " "))
	print("Price: " +  price)
	print("Shipping: " + shipPrice.replace("Shipping", "").replace("$", "").replace("Free", "0") + "\n")

	# Writing data to the csv file and cleaning the data
	f.write(brand + "," 
		+ prodName.replace(",", " ") + "," 
		+ price + "," 
		+ shipPrice.replace("Shipping", "").replace("$", "").replace("Free", "0") 
		+ "\n")

# Closing the csv file
f.close()	
