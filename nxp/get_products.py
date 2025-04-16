from selenium import webdriver
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
proxy = "54.173.153.36"
# Configure Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Load links from your JSON file
# with open('/Users/karanhunjan/vscode-workspace/python-scripts/frasers/test.json', 'r') as file:
#     links = json.load(file)

results = []

# links = [
#     "https://www.nxp.com/products/MF3DHx3",
#     "https://www.nxp.com/products/68HC11E9"
# ]
with open('product_urls2.txt') as f:
    links = [line.rstrip('\n') for line in f]
    print(len(links))

for link in links:
    driver.get(link)
    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '#lblProductName'))
    #     )
    # except Exception as e:
    #     print(f"Element not loaded within the expected time: {e}")

    # driver.implicitly_wait(5)

    # Parse page source using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    main_content = soup.select_one('div.iw_viewport-wrapper')
    # Write only the selected section to an HTML file - FOR DEBUGGING
    # if main_content:
    #     with open('output.html', 'w', encoding='utf-8') as file:
    #         file.write(main_content.prettify())

    try:
        product_name = soup.select_one('#hero-title').get_text(
            strip=True) if soup.select_one('#hero-title') else 'N/A'

        product_code = soup.select_one('.sp-hero-others-codeid').get_text(
            strip=True) if soup.select_one('.sp-hero-others-codeid') else 'N/A'

        overview_txt_soup = soup.select('#overview p') if soup.select_one('#overview p') else 'N/A'
        print("the text soup is", overview_txt_soup)
        overview_txt = ''
        for p in overview_txt_soup:
            overview_txt = p.get_text(strip=True)  + ' ' + overview_txt
        product_image_soup = soup.select_one('.img-responsive')
        if product_image_soup:
            product_image_src = "https://www.nxp.com/"+product_image_soup.get('src')
            print(product_image_src)
        else:
            product_image_src = 'https://www.nxp.com/assets/images/en/logos-internal/image-not-available-sillicon.svg'
        overview_li_soup = soup.select('#overview li') if soup.select_one('#overview li') else ''
        overview_li = ''
        print("Overview li soup is ", overview_li_soup)
        if overview_li_soup != '':
            overview_li = ''
            for li in overview_li_soup:
                overview_li = overview_li + li.get_text(strip=True) + ', '
        scraped_bcrumb = soup.select('ul[data-dtmaction="Breadcrumb Click"] li a.dropdown-toggle') if soup.select_one(
            'ul[data-dtmaction="Breadcrumb Click"] li a.dropdown-toggle') else 'N/A'
        if scraped_bcrumb != 'N/A':
            scraped_bcrumb_text = [el.get_text(strip=True) for el in scraped_bcrumb]
            category_string = ''
            for i in range(len(scraped_bcrumb_text)):
                category_string += "|".join(scraped_bcrumb_text[:i + 1]) + ";"

# /*
# 'clickableuri': d
# 'ec_name': data['
# 'ec_product_id':
# # 'ec_short_desc'
# 'ec_type': data['
# 'ec_category': ca
# 'blogimage': data
# 'partial_match':
# 'ec_price': data[
# 'ec_sku': data['o
    except Exception as e:
        print(f"Failed to extract data from {link}: {e}")
        product_name = price = description = 'N/A'
    print("The link is: ", link)
    print("The product code is: ", product_code)
    results.append({
        'clickableuri': link,
        'ec_name': product_name,
        'ec_product_id': product_code,
        'ec_short_desc': overview_txt ,
        'ec_category': category_string,
        'blogimage': product_image_src,
        'partial_match': ";".join([product_code[:i+1] for i in range(3, len(product_code))])
    })

# Close the browser
driver.quit()

# Save data to a JSON file
with open('product_data.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Data extraction complete and written to product_data.json")
print("--- %s seconds ---" % (time.time() - start_time))