import http.client
import json


def http_request():
    conn = http.client.HTTPSConnection("help.prsformusic.com")
    payload = "message=%7B%22actions%22%3A%5B%7B%22id%22%3A%22470%3Ba%22%2C%22descriptor%22%3A%22aura%3A%2F%2FApexActionController%2FACTION%24execute%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22namespace%22%3A%22%22%2C%22classname%22%3A%22CP_KnowledgeDataSource%22%2C%22method%22%3A%22getFilteredArticles%22%2C%22params%22%3A%7B%22categoryName%22%3A%22%22%2C%22orderBy%22%3A%22POPULAR%22%7D%2C%22cacheable%22%3Afalse%2C%22isContinuation%22%3Afalse%7D%7D%5D%7D&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22c1ItM3NYNWFUOE5oQkUwZk1sYW1vQWg5TGxiTHU3MEQ5RnBMM0VzVXc1cmcxMS4zMjc2OC4z%22%2C%22app%22%3A%22siteforce%3AcommunityApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fsiteforce%3AcommunityApp%22%3A%221233_vZx87dHGHIhS0MXRTe4D5w%22%2C%22COMPONENT%40markup%3A%2F%2Fforce%3AoutputField%22%3A%22961_boz4cYMH0Vbm82lrUXviEw%22%2C%22COMPONENT%40markup%3A%2F%2FforceSearch%3AresultsFilters%22%3A%22511_CJi1fmSOev7Y2DQ7R_HEhw%22%2C%22COMPONENT%40markup%3A%2F%2FforceSearch%3AresultsList%22%3A%221310_EnO7sUpcfSUmDpcJs8bmow%22%2C%22COMPONENT%40markup%3A%2F%2Finstrumentation%3Ao11ySecondaryLoader%22%3A%22387_xvXc6AnLRgqK6TofLxISPw%22%2C%22COMPONENT%40markup%3A%2F%2Flightning%3AbuttonStateful%22%3A%22398_YGDtMeLbOMFVN_TiCVhDdQ%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Afalse%7D&aura.pageURI=%2Fs%2Fall-articles&aura.token=null"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://help.prsformusic.com',
        'priority': 'u=1, i',
        'referer': 'https://help.prsformusic.com/s/all-articles',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-b3-sampled': '0',
        'x-b3-spanid': '8b746adfc277ed26',
        'x-b3-traceid': '717dc1cfcacc3ec6',
        'x-sfdc-lds-endpoints': 'ApexActionController.execute:CP_KnowledgeDataSource.getFilteredArticles',
        'x-sfdc-page-scope-id': '5b36944a-c66c-4876-810d-c34807a7bc0a',
        'x-sfdc-request-id': '49261090000d431ec1',
        'Cookie': 'renderCtx=%7B%22pageId%22%3A%227e18ad50-b87a-406e-aa37-995317c6abce%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%224acc9c02-d30c-4627-a3db-0d29fe929589%22%2C%22audienceIds%22%3A%22%22%7D; TAsessionID=b9a88e4f-5a47-42cf-913f-f47f3126e57d|NEW; notice_preferences=0:; notice_gdpr_prefs=0:; cmapi_gtm_bl=ga-ms-ua-ta-asp-bzi-sp-awct-cts-csm-img-flc-fls-mpm-mpr-m6d-tc-tdc; cmapi_cookie_privacy=permit 1 required; notice_behavior=expressed,us; CookieConsentPolicy=1:1; LSKey-c$CookieConsentPolicy=1:1; pctrk=68d1b92c-bec2-4a0c-8a2f-94685271e2d8; idccsrf=3382906447001401751174222082258221261872307430547'
    }
    conn.request("POST", "/s/sfsites/aura?r=28&aura.ApexAction.execute=1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    all_cases = []

    f = open('response.json', "a")
    output = data.decode("utf-8")
    response_data = json.loads(output)
    actions = response_data.get('actions', [])

    for action in actions:
        return_value = action.get('returnValue', [])
        with open('returnValues.json', 'w') as f:
            json.dump(return_value, f, indent=4)
        cases = return_value.get('returnValue', {})
        case_categories = []

        for case in cases:
            case_category = case.get('category', {}).get('label', '')  # Access category label
            data = case.get('description', '')
            title = case.get('title', '')
            id = case.get('id', '')
            object_type = "Cases"
            soup = BeautifulSoup(data, 'html.parser')
            case_description = soup.get_text(separator="\n", strip=True)

            case_info = {
                "case_category": case_category,
                "case_description": case_description,
                "data": "<html>" + data + "</html>",
                "documentId": "https://help.prsformusic.com/s/article/" + title.replace(" ", "-").replace("?", ""),
                "objecttype": object_type,
                "title": title
            }
            all_cases.append(case_info)

        with open('all_cases.json', 'w') as f:
            json.dump(all_cases, f, indent=4)

    f.close()


if __name__ == '__main__':
    http_request()
