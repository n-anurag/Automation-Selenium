from bs4 import BeautifulSoup
import os
import pandas as pd

# Initialize dictionary to store scraped data
d = {'title': [], 'price': [], 'link': []}

for file in os.listdir("data"):
    with open(f"data/{file}", encoding="utf-8", errors="ignore") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    # Extract product title from <h2>
    t = soup.find("h2", class_="a-size-medium")
    title = t.get_text(strip=True) if t else "No title"

    # Extract link from <a> tag (globally)
    l = soup.find("a", href=True)

    # Extract link safely
    link = l['href'] if l else "No link"


    # Fix relative Amazon links
    if link.startswith("/"):
        link = "https://amazon.in/" + link

    # Extract price from <span class='a-price-whole'>
    p = soup.find("span", attrs={"class": "a-price-whole"})
    price = p.get_text(strip=True) if p else "No price"

    # Store extracted data
    d['title'].append(title)
    d['link'].append(link)
    d['price'].append(price)
    # print(link)

# Convert dictionary to DataFrame
df = pd.DataFrame(d)

# Save to CSV
df.to_csv("scraped_data.csv", index=False)

print("✅ Scraping completed! Data saved to 'scraped_data.csv'.")
