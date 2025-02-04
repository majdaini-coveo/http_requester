import time

import requests
import json


def get_json(url):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,fr;q=0.8",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ2OCI6dHJ1ZSwidG9rZW5JZCI6InNueGFwbHhoMjVndjJ1bDU1a29kZWJzZHhpIiwib3JnYW5pemF0aW9uIjoiaGVpZGVsYmVyZ2VyZHJ1Y2ttYXNjaGluZW5hZ3Byb2R1Y3Rpb25zeDhremNmbSIsInVzZXJJZHMiOlt7InR5cGUiOiJVc2VyIiwibmFtZSI6InM0NTBAaGVpZGVsYmVyZy5jb20iLCJwcm92aWRlciI6IkVtYWlsIFNlY3VyaXR5IFByb3ZpZGVyIn1dLCJyb2xlcyI6WyJxdWVyeUV4ZWN1dG9yIl0sImlzcyI6IlNlYXJjaEFwaSIsImV4cCI6MTczODc2NDAyNSwiaWF0IjoxNzM4NjkyMDI1fQ.d54wjron-jMbg0jgAanCSA2jbKx0fhkZbsrYuNM48uk",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://eshop.heidelberg.com",
        "priority": "u=1, i",
        "referer": "https://eshop.heidelberg.com",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    data = f"actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22product%22%2C%22time%22%3A%22%5C%222025-02-04T21%3A14%3A09.337Z%5C%22%22%7D%2C%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22product%22%2C%22time%22%3A%22%5C%222025-02-04T21%3A12%3A41.284Z%5C%22%22%7D%5D&referrer=https%3A%2F%2Feshop.heidelberg.com%2Fgb&analytics=%7B%22clientId%22%3A%22aa7b4cdb-49a7-8832-952f-20e093f37d5f%22%2C%22documentLocation%22%3A%22https%3A%2F%2Feshop.heidelberg.com%2Fgb%2Fccrz__CCPage%3FpageKey%3DSearchResults%23q%3Dproduct%26first%3D192%26sort%3Drelevancy%26layout%3Dcard%26numberOfResults%3D48%22%2C%22documentReferrer%22%3A%22https%3A%2F%2Feshop.heidelberg.com%2Fgb%22%2C%22pageId%22%3A%22%22%2C%22originContext%22%3A%22Search%22%7D&visitorId=aa7b4cdb-49a7-8832-952f-20e093f37d5f&isGuestUser=false&q=product&cq=%40source%3DS220-en_GB&dq=(%40source%3D%3D'S220-en_GB')(%5B%5B%40productmastername%5D(%24query)%20(%24originalQuery)(%24facetsFilter)%20%40availabilityid%3D'S220'%20%40splitpartnumber%3D('product')%5D)&searchHub=S220-ProductSearch-en_GB&locale=en&firstResult={i}&numberOfResults=48&excerptLength=200&enableDidYouMean=true&sortCriteria=relevancy&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&facets=%5B%7B%22facetId%22%3A%22%40categories%22%2C%22field%22%3A%22categories%22%2C%22type%22%3A%22hierarchical%22%2C%22injectionDepth%22%3A1000%2C%22delimitingCharacter%22%3A%22%7C%22%2C%22filterFacetCount%22%3Atrue%2C%22basePath%22%3A%5B%5D%2C%22filterByBasePath%22%3Afalse%2C%22currentValues%22%3A%5B%5D%2C%22preventAutoSelect%22%3Afalse%2C%22numberOfValues%22%3A5%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40packaginginfo%22%2C%22field%22%3A%22packaginginfo%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22Piece%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%2225%20l%20canister%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%221%20l%20bottle%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Roll%20of%2030%20m%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%2225%20kg%20canister%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%2220%20kg%20canister%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Pack%20of%2015%20pieces%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Pack%20of%20100%20pieces%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40suitable_equipment%22%2C%22field%22%3A%22suitable_equipment%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22ALL%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22SM102%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22CD102%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22XL105%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22SM74%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22SX102%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22XL106%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22CS92%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40mainapplication%22%2C%22field%22%3A%22mainapplication%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22Chemfree%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22All%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Conventional%20Low%20Migration%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Narrow%20web%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22UV-Curing%20Low%20Migration%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Conventional%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Narrow%20web%20Low%20Migration%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Premium%20Low%20Chemistry%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40saphiraeco%22%2C%22field%22%3A%22saphiraeco%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22No%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Yes%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40hda_uv_suitable%22%2C%22field%22%3A%22hda_uv_suitable%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22No%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Not%20specified%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Yes%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40hda_anicolor_suitable%22%2C%22field%22%3A%22hda_anicolor_suitable%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22No%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Not%20specified%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Yes%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40hda_coatingunit_suitable%22%2C%22field%22%3A%22hda_coatingunit_suitable%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%7B%22value%22%3A%22No%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Not%20specified%22%2C%22state%22%3A%22idle%22%7D%2C%7B%22value%22%3A%22Yes%22%2C%22state%22%3A%22idle%22%7D%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40brand%22%2C%22field%22%3A%22brand%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%2C%7B%22facetId%22%3A%22%40saphiralowmigration%22%2C%22field%22%3A%22saphiralowmigration%22%2C%22type%22%3A%22specific%22%2C%22injectionDepth%22%3A1000%2C%22filterFacetCount%22%3Atrue%2C%22currentValues%22%3A%5B%5D%2C%22numberOfValues%22%3A8%2C%22freezeCurrentValues%22%3Afalse%2C%22preventAutoSelect%22%3Afalse%2C%22isFieldExpanded%22%3Afalse%7D%5D&facetOptions=%7B%7D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=America%2FToronto&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&context=%7B%22AccountGroupContext%22%3A%22en_GB%22%7D&allowQueriesWithoutKeywords=true"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request was successful!")
        try:
            response_json = response.json()
            res = json.dumps(response_json, indent=4)
            test = json.loads(res)
            raw_contents = [article['raw'] for article in test['results'] if 'raw' in article]
            return json.dumps(raw_contents)
        except ValueError:
            print("Response is not in valid JSON format.")
            print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    data = []

    with open("output.json", "w") as f:
        for i in range(336, 2001, 48):
            output = get_json("https://platform.cloud.coveo.com/rest/search/v2?tab=All")
            output_data = json.loads(output)
            data.extend(output_data)

        json.dump(data, f, indent=4)
