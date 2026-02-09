import requests
# requests is used to send HTTP requests to the website

import pandas as pd
# pandas is used to store, manipulate, and export data in tabular form

from bs4 import BeautifulSoup
# BeautifulSoup is used to parse and extract data from HTML

# Base URL of the website
baseurl = 'https://www.karlaaflames.com/'

# Headers to mimic a real browser request (helps avoid blocking)
headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}

# Send a GET request to the "All Products" page
r = requests.get('https://www.karlaaflames.com/collections/all')

# Parse the HTML content using lxml parser
soup = BeautifulSoup(r.text, 'lxml')

# Find the main container that holds the product cards
box = soup.find('div', class_="collection page-width")

# Print the HTTP response status (200 means success)
print(r)

# Find the previous page pagination link
np = soup.find(
    "a",
    class_="pagination__item pagination__item--prev pagination__item-arrow link motion-reduce"
).get("href")

# Create a complete URL for the pagination link
cnp = "https://www.karlaaflames.com" + np

# Empty lists to store scraped data
Product_name = []
Prices = []
Description = []

# Loop through all paginated pages
while True:
    # Find the pagination link on the current page
    np = soup.find(
        "a",
        class_="pagination__item pagination__item--prev pagination__item-arrow link motion-reduce"
    )

    # If no pagination link is found, stop the loop
    if np is None:
        break

    # Extract the href value of the pagination link
    np = np.get("href")

    # Construct the full URL for the next page
    cnp = "https://www.karlaaflames.com" + np
    url = cnp

    # Send request to the next page
    r = requests.get(url)

    # Parse the new page HTML
    soup = BeautifulSoup(r.text, 'lxml')

    # Find all product name elements
    names = box.find_all('h3', class_="card__heading h5")

    # Extract and store product names
    for p in names:
        name = p.get_text(strip=True)
        Product_name.append(name)

    # Find all product price elements
    price = box.find_all(
        'span',
        class_='price-item price-item--sale price-item--last'
    )

    # Extract price text
    for s in price:
        price = s.get_text(strip=True)

    # Store price in the Prices list
    Prices.append(price)

# Create a DataFrame from the scraped data
df = pd.DataFrame({
    "Product name": Product_name,
    "Prices": Prices
})

# Export the DataFrame to an Excel file
df.to_excel(
    "karlaa_Flames_Lighters.xlsx",
    sheet_name="sheet5",
    index=False
)

# Print the DataFrame to verify output
print(df)
