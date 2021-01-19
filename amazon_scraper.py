import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'Host': 'www.amazon.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}
# get method: introduce the url wanted.
r = requests.get('https://www.amazon.com/AmazonBasics-Performance-Alkaline-Batteries-Count/dp/B00LH3DMUO/ref=sxin_3_ac_d_rm?ac_md=0-0-YW1hem9uYmFzaWNz-ac_d_rm&cv_ct_cx=amazonbasics&dchild=1&keywords=amazonbasics&pd_rd_i=B00LH3DMUO&pd_rd_r=ef8a3adc-4ea7-4599-a8bc-ccece0e64df3&pd_rd_w=ixItm&pd_rd_wg=K5Fe8&pf_rd_p=9349ffb9-3aaa-476f-8532-6a4a5c3da3e7&pf_rd_r=KDBKF2Q1Y984249CR30N&qid=1607012986&sr=1-1-12d4272d-8adb-4121-8624-135149aa9081&th=1', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# initialize a data frame, add or remove the variables wanted.
df = pd.DataFrame(columns=['stars', 'title', 'date', 'text', 'purchase'])

# retreiving product rating
try:
    rating = soup.find("i", attrs={
                       'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
except AttributeError:
    try:
        rating = soup.find(
            "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
    except:
        rating = "NA"

print("Rating = ", rating)
# saving the rating in the dataframe
df.stars = pd.Series(rating)

# retreiving product title
try:
    # Outer Tag Object
    title = soup.find("span",
                      attrs={"id": 'productTitle'})

    # Inner NavigableString Object
    title_value = title.string

    # Title as a string value
    title_string = title_value.strip().replace(',', '')

except AttributeError:
    title_string = "NA"

print("Product title = ", title_string)
# saving the title in the dataframe
df.title = pd.Series(title_string)

# retriving the date
try:
    date = soup.find("div", attrs={'id': 'deliveryMessageMirId'})
    date = date.find("b").string.strip().replace(',', '')

        #div id="deliveryMessageMirId" class="a-section a-spacing-mini a-spacing-top-micro"
except AttributeError:
    available = "NA"

print("Date = ", date)
# saving the title in the dataframe
df.date = pd.Series(date)

# retreiving product features
try:
    features = []
    for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
        features.append(li.get_text().strip())
except AttributeError:
    features = "NA"

features = "".join(features)
print("Product features = ", features)
# saving the features in the dataframe
df.text = pd.Series(features)

# retreiving the purchase
try:
    purchase = soup.find(
        "span", attrs={'class': 'a-size-mini a-color-state a-text-bold'}).string.strip().replace(',', '')
    # we are omitting unnecessary spaces
except AttributeError:
    price = "NA"

print("Purchase = ", purchase)
# saving the purchase in the dataframe
df.purchase = pd.Series(purchase)

# check the data frame  
df.head()
