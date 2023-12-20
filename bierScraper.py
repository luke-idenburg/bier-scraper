import requests
import json
from bs4 import BeautifulSoup

url = "https://www.nederlandsebiercultuur.nl/nederlandse-bierwereld/evenementen"
page = requests.get(url=url)

soup = BeautifulSoup(page.content, "html.parser")

h3_elements = soup.find_all('h3')

for i in range(1, len(h3_elements) - 3):

    start_h3 = h3_elements[i]
    end_h3 = h3_elements[i + 1]

    current_element = start_h3.find_next_sibling()
    closest_h2 = start_h3.find_previous('h2')

    event = {
        "year": closest_h2.string.strip() if closest_h2 else "",
        "month": start_h3.string if start_h3 else "",
        "name": "",
        "date": "",
        "location": "",
        "description": "",
        "url": ""
    }

    while current_element and current_element.name != 'h3' and current_element != end_h3:

        # This gets the event title
        if current_element.name == 'b' and current_element.find_next_sibling('br'):
            if event["name"]:
                print(json.dumps(event))

            event["name"] = current_element.get_text(strip=True)

        # This gets the event date
        if current_element.string == "Datum:":
            next_element = current_element.find_next_sibling(string=True)
            event_date = ' '.join(next_element.get_text().split())
            event["date"] = event_date

        # This gets the event location
        if current_element.string == "Locatie:":
            next_element = current_element.find_next_sibling(string=True)
            event_location = ' '.join(next_element.get_text().split())
            event["location"] = event_location

        # This gets the event link
        if "senb-blockquote-indent" in current_element.get("class", []):
            for child_element in current_element.findChildren():
                if child_element.string == "Meer informatie...":
                    # Use 'href' to get the URL from the anchor tag
                    event_link = child_element.get('href')
                    event["url"] = event_link

        # Move to the next sibling
        current_element = current_element.find_next_sibling()
