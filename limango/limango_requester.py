import json

import requests


def extract_json(pageNum,color):
    url = f"https://shop-frontend-api.limango.com/v2/search?color={color}&page={pageNum}&alias=&landing-page-id=&offset={108 * pageNum}&limit=108&householdCondition%5Ball-eq%5D=&price=&campaign=&search=&preOwned=1&referer=%2Fshop%2Fproducts%3Fpage%3D2&testGroup=20210706_ProductGateway&shop-type=&data-type=grouped-filters%7Ccategories%7Cproducts%7Cseo%7Cbreadcrumbs%7Cprofile&sort=osranking-desc&apply-profile=size"
    # url = f"https://shop-frontend-api.limango.com/v2/search?color={color}&page={pageNum}&alias=&landing-page-id=&offset={108*pageNum}&limit=1&householdCondition%5Ball-eq%5D=&price=&campaign=&search=&preOwned=1&referer=%2Fshop%2Fproducts%3Fpage%3D2&testGroup=20210706_ProductGateway&shop-type=&data-type=grouped-filters%7Ccategories%7Cproducts%7Cseo%7Cbreadcrumbs%7Cprofile&sort=osranking-desc&apply-profile=size"

    payload = {}
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
        'auth-device-token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIydXI4SndXRFg1N1FxdTUyakx1bkFMakNScGIifQ.Fq7MU4PIecqmGlm83JvDfGqTeiNudaRN42KZi-LtGTZ4l-CfbmYQdFdBq3Ov5xqZitNkg_ur7iAuqW_7jA8tnHB0GLTxTH6B9c78TmFYgsuqz8W6iR1cN7MDIgAmrOlEW16jdkBY5CtrCiU7ju_ILCufVzsPbvJHsFai5O6NrJa76prLRKHtpfhitDA9rKndG3bkXYk-3dL8f-vHZyDVh_FHPF5wmKqDr1lvkP0pLrxkWFSukRPwcI0fHAJIJkp2NxTzm0HHQDMnJC4-jtBwLgzuAH_Mg41h-EDNW4gBbZpiiUn4dGrSR-mM75SOs5P4r3HSATZibY9luZJlSquOXg',
        'authorization': '',
        'origin': 'https://www.limango.de',
        'priority': 'u=1, i',
        'referer': 'https://www.limango.de/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-accept-version': '1.1.3',
        'x-api-country': 'DE',
        'x-api-device-id': '2ur8JwWDX57Qqu52jLunALjCRpb',
        'x-api-key': 'jlk6fH4161Gc6434fe7Fg23dv620713fCDh64e8f512E2h2V116c255f6f4356vk'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def generate_hierarchy(path: str):
    elements = path.split('|')
    return ['|'.join(elements[:i+1]) for i in range(len(elements))]

def transform_categories(categories):
    transformed = dict()
    for path in categories:
        parts = path.split('/')
        transformed_path = parts[0].capitalize()
        for part in parts[1:]:
            transformed_path += '|' + part.capitalize()
        for item in generate_hierarchy(transformed_path):
            transformed[item] = None
    return list(transformed.keys())


if __name__ == '__main__':

    num_pages = 8
    all_products = []
    filtered_products = []


    colors=['blue','colorful','pink','black','white','gray','green','red','brown','beige'
        ,'yellow','silver','uncolored']

    for color in colors:

        for pageNum in range(num_pages):

            data = extract_json(pageNum, color)
            products_data = data.get("data", {}).get("products", {}).get("data", [])

            if products_data:
                all_products.extend(products_data)
                for product in products_data:
                    all_variant = []
                    all_sizes = []
                    picture_variants = product.get("images").get("default", []).get("variants")

                    sizes = product.get("variants", [])

                    for size in sizes:
                        size_labels = size.get("sizeLabels", [])
                        all_sizes.extend(size_labels)

                    for variant in picture_variants:
                        variant_id = variant.get("id")
                        all_variant.append(
                            product.get("images", {}).get("default", "No image").get("url", "No url").replace("{format}",
                                                                                                              "t_product-original").replace(
                                "{dpr}", "").replace("{variant}", variant_id), )
                    product_info = {
                        "ec_name": product.get("name", "No name"),
                        "title": product.get("name", "No name"),
                        "documentId": "https://www.limango.de/shop/"+product.get("brand", "No brand").get("name", "No brand")+ product.get("id").replace("_","-"),
                        "ec_product_id": product.get("id", "No ID"),
                        "ec_price": product.get("retailPrice", "No price").get("amount"),
                        "ec_in_stock": True if int(product.get("totalStockAvailable", "0")) > 0 else False,
                        "ec_brand": product.get("brand", "No brand").get("name", "No brand"),
                        "ec_subCategoryName": product.get("subCategoryName", "No subCategory"),
                        "ec_images": all_variant[0],
                        "ec_category": transform_categories(product.get("treePaths", "No category")),
                        "ec_variants": all_variant,
                        "ec_sizes": all_sizes,
                        "ec_color": color,
                        "objecttype": "Product",
                        "filetype": "txt"

                    }
                    filtered_products.append(product_info)

    with open("all_products.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4)

    with open("filtered_products.json", "w", encoding="utf-8") as f:
        json.dump(filtered_products, f, indent=4)

    output_file = "products_all.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4)
