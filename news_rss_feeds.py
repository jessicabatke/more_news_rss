import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime

url_dict = {
    "NPR":" https://www.npr.org/tags/127994355/china",
    "AP": "https://apnews.com/hub/china",
    "RoW_China": "https://restofworld.org/region/china/",
    "RoW_OutChina": "https://restofworld.org/series/china-outside-china/"
}



def scrape(website, website_url):
    print(website_url)
    if website == "NPR" or "RoW" in website:
        feature = "h2"
    else:
        feature = "h3"
    items = []
    response = requests.get(website_url)
    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)
    # Find all h2 elements
    titles = soup.find_all(feature)    
    for title in titles:
        # print(title)
        # Find the <a> tag within each h2
        link_tag = title.find('a')
        if link_tag:  # Check if <a> exists
            link = link_tag.get('href')
            title_text = link_tag.get_text().strip()
            print(f"Link: {link}")
            print(f"Title: {title_text}")
            items.append({
                    'title': title_text,
                    'link': link
                })
    return items
    print("")

# Function to create RSS feed
def create_rss_feed(site_name, items, filename):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = f'{site_name} China News'
    ET.SubElement(channel, 'link').text = f'https://github.com/jessicabatke/more_news_rss'
    ET.SubElement(channel, 'description').text = f'China news from {site_name}'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    for article in items:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = article['title']
        ET.SubElement(item, 'link').text = article['link']
        ET.SubElement(item, 'description').text = article['title']
        ET.SubElement(item, 'pubDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        ET.SubElement(item, 'guid').text = article['link']
    
    tree = ET.ElementTree(rss)
    ET.indent(tree, space='  ')
    tree.write(filename, encoding='unicode', xml_declaration=True)
    
    print(f"Generated {filename} with {len(items)} articles")


for key,value in url_dict.items():
    print("")
    print("")
    print("")
    print("")
    items = scrape(key, url_dict[key])
    filename = f'{key.lower()}_china_feed.xml'
    create_rss_feed(key, items, filename)


