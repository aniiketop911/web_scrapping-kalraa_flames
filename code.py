import requests
import pandas as pd
baseurl = 'https://www.karlaaflames.com/'
headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}
r = requests.get('https://www.karlaaflames.com/collections/all')
soup = BeautifulSoup(r.text,'lxml')
box = soup.find('div',class_="collection page-width")
#productlist = soup.find_all('div', class_='item')
print(r)
np = soup.find("a",class_ = "pagination__item pagination__item--prev pagination__item-arrow link motion-reduce").get("href")
cnp = "https://www.karlaaflames.com"+np
Product_name = []
Prices = []
Description = []
while True:
  np = soup.find("a",class_ = "pagination__item pagination__item--prev pagination__item-arrow link motion-reduce")
  if np is None: 
    break 
  np = np.get("href") 
  cnp = "https://www.karlaaflames.com"+np
  url = cnp
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  names = box.find_all('h3',class_="card__heading h5")
  for p in names:
    name = p.get_text(strip=True)
    Product_name.append(name)
  price = box.find_all('span',class_='price-item price-item--sale price-item--last')
  for s in price:
    price = s.get_text(strip=True)
  Prices.append(price)
df = pd.DataFrame({"Product name":Product_name,"Prices":Prices})
df.to_excel("karlaa_Flames_Lighters.xlsx", sheet_name="sheet5", index=False)
print(df)