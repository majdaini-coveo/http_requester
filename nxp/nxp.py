from traceback import print_tb

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

start_time = time.time()

# Configure Chrome WebDriver

# Configure Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

results = []

# links = [
#     "https://www.nxp.com/products/MF3DHx3",
#     "https://www.nxp.com/products/68HC11E9"
# ]

with open('product_urls2.txt') as f:
    links = [line.rstrip('\n') for line in f]

i = 0
for link in links:
    driver.get(link)
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//script[@type='application/ld+json']"))
        )
    except TimeoutException:
        print(f"Timeout waiting for ld+json script on: {driver.current_url}")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    scraped_bcrumb = soup.select('ul[data-dtmaction="Breadcrumb Click"] li a.dropdown-toggle') if soup.select_one(
        'ul[data-dtmaction="Breadcrumb Click"] li a.dropdown-toggle') else 'N/A'
    if scraped_bcrumb != 'N/A':
        scraped_bcrumb_text = [el.get_text(strip=True) for el in scraped_bcrumb]
        category_string = ''
        for i in range(len(scraped_bcrumb_text)):
            category_string += "|".join(scraped_bcrumb_text[:i + 1]) + ";"

    script_tags = soup.select('script[type="application/ld+json"]')

    ld_json_data = []
    clickableuri = ''
    ec_name = ''
    ec_product_id = ''
    ec_short_desc = ''
    ec_type = ''
    ec_category = ''
    blogimage = ''
    partial_match = ''
    ec_price = ''
    ec_sku = ''
    ec_description = ''
    if not script_tags:
        print(f"[No ld+json found] Skipping: {driver.current_url}")
        element = (
                soup.select_one('[data-dtmaction="Overview Section Click"]') or
                soup.select_one('[data-dtmname="Overview Section"]')
        )

        if element:
            ec_description = element.get_text(separator="|", strip=True)

        clickableuri = link
        ec_name = (
                soup.select_one('h1.title') or
                soup.select_one('h1.sp-hero-title')
        ).get_text(strip=True) if soup.select_one('h1.title') or soup.select_one('h1.sp-hero-title') else 'N/A'
        ec_short_desc = ec_description
        ec_type = 'WebPage'
        blogimage = 'https://www.nxp.com/assets/images/en/logos-internal/image-not-available-sillicon.svg'
        ec_product_id = soup.select_one('.sp-hero-others-codeid').get_text(
            strip=True) if soup.select_one('.sp-hero-others-codeid') else 'N/A'
        if clickableuri:
            results.append({
                'title': ec_name,
                'documentid': f'https://www.nxp.com/{ec_product_id}',
                'clickableuri': clickableuri,
                'ec_name': ec_name,
                'ec_product_id': ec_product_id,
                'ec_description': ec_description,
                'ec_type': ec_type,
                'category': category_string,
                'blogimage': blogimage,
                'filetype': 'txt'
            })
        continue
    for script_tag in script_tags:

        try:
            json_data = json.loads(script_tag.get_text(strip=True))
        except json.decoder.JSONDecodeError:
            print("wrong json data")
            continue
        ld_json_data.append(json_data)

        with open('ldjson.json', 'w') as f:
            json.dump(ld_json_data, f, indent=4)

        if json_data.get('@type') == 'Product':

            element = soup.select_one('[data-dtmname="Overview Section"]')
            if element:
                ec_short_desc = element.get_text(separator="|", strip=True)

            scraped_bcrumb = soup.select(
                'ul[data-dtmaction="Breadcrumb Click"] li a.dropdown-toggle') if soup.select_one(
                'ul[data-dtmaction="Breadcrumb Click"] li a.dropdown-toggle') else 'N/A'
            if scraped_bcrumb != 'N/A':
                scraped_bcrumb_text = [el.get_text(strip=True) for el in scraped_bcrumb]
                category_string = ''
                for i in range(len(scraped_bcrumb_text)):
                    category_string += "|".join(scraped_bcrumb_text[:i + 1]) + ";"

            ec_product_id = json_data['mpn']
            ec_name = json_data['name']
            ec_description = ec_short_desc
            clickableuri = json_data['url']
            ec_type = json_data['@type']
            ec_price = json_data['offers'][0]['price']
            ec_sku = [offer['sku'].replace('/', '|') for offer in json_data['offers']]

        elif isinstance(json_data.get('@type'), list) and 'Product' in json_data['@type']:
            if 'image' in json_data and isinstance(json_data['image'], list) and json_data['image']:
                url_data = json_data['image'][0].get('url')
                if isinstance(url_data, list):
                    blogimage = url_data[0]
                else:
                    blogimage = url_data
            elif 'offers' in json_data and isinstance(json_data['offers'], list) and json_data['offers']:
                offer_image_data = json_data['offers'][0].get('image')
                if isinstance(offer_image_data, list) and offer_image_data:
                    url_data = offer_image_data[0].get('url')
                    if isinstance(url_data, list):
                        blogimage = url_data[0]
                    else:
                        blogimage = url_data
                else:
                    blogimage = 'https://www.nxp.com/assets/images/en/logos-internal/image-not-available-sillicon.svg'
            else:
                blogimage = 'https://www.nxp.com/assets/images/en/logos-internal/image-not-available-sillicon.svg'


        elif isinstance(json_data.get('@type'), list) and 'WebPage' in json_data['@type']:
            element = soup.select_one('[data-dtmname="Overview Section"]')
            ec_description = ''
            if element:
                ec_description = element.get_text(separator="|", strip=True)
            fallback_image = 'https://www.nxp.com/assets/images/en/logos-internal/image-not-available-sillicon.svg'
            try:
                about = json_data.get('about', [])
                if about and isinstance(about, list):
                    image_list = about[0].get('image', [])
                    if image_list and isinstance(image_list, list):
                        url_data = image_list[0].get('url')
                        if isinstance(url_data, list) and url_data:
                            blogimage = url_data[0]
                        elif isinstance(url_data, str):
                            blogimage = url_data
                        else:
                            blogimage = fallback_image
                    else:
                        blogimage = fallback_image
                else:
                    blogimage = fallback_image
            except Exception:
                blogimage = fallback_image

            clickableuri = link
            ec_name = json_data.get('name')
            ec_product_id = soup.select_one('.sp-hero-others-codeid').get_text(
                strip=True) if soup.select_one('.sp-hero-others-codeid') else 'N/A'
            ec_short_desc = ec_description
            ec_type = 'WebPage'
            partial_match = ''
            ec_price = ''
            ec_sku = ''

        elif isinstance(json_data.get('@type'), list) and 'Organization' in json_data['@type']:
            continue

    if clickableuri:
        results.append({
            'title': ec_name,
            'documentid': f'https://www.nxp.com/{ec_product_id}',
            'clickableuri': clickableuri,
            'ec_name': ec_name,
            'ec_product_id': ec_product_id,
            'ec_description': ec_description,
            'ec_type': ec_type,
            'category': category_string,
            'blogimage': blogimage,
            'partial_match': ";".join([ec_product_id[:i + 1] for i in range(3, len(ec_product_id))]),
            'ec_price': ec_price,
            'ec_sku': ec_sku,
            'filetype': 'txt'
        })

driver.quit()

with open('nxp_data.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Data extraction complete and written to product_data.json")
print("--- %s seconds ---" % (time.time() - start_time))
