import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape
base_url = 'https://medlineplus.gov/lab-tests/'

# Function to extract all <a> tags within the 'main' section
def extract_a_tags(section):
    return [{'text': a.text.strip(), 'href': a.get('href')} for a in section.find_all('a') if a.get('href')]

# Function to extract detailed content from each link
def extract_detailed_content(link_url):
    response = requests.get(link_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find("article")

        if not main_content:
            return None

        title = main_content.find("h1").text if main_content.find("h1") else "No Title"
        footer = soup.find("footer")
        if footer and "Last updated " in footer.text:
            publication_date = footer.text.split("Last updated ")[1].strip()
        else:
            publication_date = "No Date"

        content_data = []

        for section in main_content.find_all("section"):
            heading = section.find("h2").text if section.find("h2") else "No Heading"
            paragraphs = [p.text for p in section.find_all("p")]

            lists = []
            for ul in section.find_all("ul"):
                lists.append([li.text for li in ul.find_all("li")])

            image_links = [img.get("src") for img in section.find_all("img") if img.get("src")]

            content_data.append({
                "heading": heading,
                "paragraphs": paragraphs,
                "lists": lists,
                "image_links": image_links
            })

        return {
            "title": title,
            "publication_date": publication_date,
            "content": content_data
        }
    else:
        print(f"Failed to retrieve the webpage content from {link_url}")
        return None

# Dictionary to store test names and their corresponding unique IDs
test_name_to_id = {}
current_id = 0

# Send a GET request to the page
response = requests.get(base_url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    main_section = soup.find(class_='main')

    if main_section:
        # Extract all <a> tags within the 'main' section
        a_tags = extract_a_tags(main_section)
        print(f"Extracted {len(a_tags)} links from the page.")

        # Open a CSV file for writing with UTF-8 encoding
        with open('lab_tests_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['unique_id', 'test_name', 'test_qns', 'test_ans', 'image_links'])

            for a_tag in a_tags:
                link_text = a_tag['text']
                link_href = a_tag['href']

                if link_href:
                    # Ensure the URL is complete
                    if not link_href.startswith('http'):
                        link_href = f'https://medlineplus.gov{link_href}'

                    print(f"Processing link: {link_text}")
                    print(f"Link URL: {link_href}")

                    detailed_content = extract_detailed_content(link_href)

                    if detailed_content:
                        test_name = link_text
                        publication_date = detailed_content["publication_date"]

                        for section in detailed_content['content']:
                            question = section['heading']
                            formatted_paragraphs = '\n'.join(section['paragraphs'])
                            formatted_lists = '\n'.join(['\n'.join([f'• {item}' for item in lst]) for lst in section['lists']])
                            answer = f'{formatted_paragraphs}\n{formatted_lists}'.strip()
                            image_links = ', '.join(section['image_links']) if section['image_links'] else ''

                            # Generate or retrieve the unique_id
                            if test_name in test_name_to_id:
                                unique_id = test_name_to_id[test_name]
                            else:
                                current_id += 1
                                unique_id = current_id
                                test_name_to_id[test_name] = unique_id

                            csv_writer.writerow([unique_id, test_name, question, answer, image_links])

        print("CSV file created successfully.")
    else:
        print("No element with class 'main' found.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# import requests
# from bs4 import BeautifulSoup
# import csv

# # URL of the page to scrape
# base_url = 'https://medlineplus.gov/lab-tests/'

# # Function to extract all <a> tags within the 'main' section
# def extract_a_tags(section):
#     return [{'text': a.text.strip(), 'href': a.get('href')} for a in section.find_all('a') if a.get('href')]

# # Function to extract detailed content from each link
# def extract_detailed_content(link_url):
#     print(f"Extracting detailed content from {link_url}")
#     response = requests.get(link_url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         main_content = soup.find("article")

#         if not main_content:
#             return None

#         title = main_content.find("h1").text if main_content.find("h1") else "No Title"
#         publication_date = soup.find("footer").text.split("Last updated ")[1].strip() if soup.find("footer") else "No Date"

#         content_data = []

#         for section in main_content.find_all("section"):
#             heading = section.find("h2").text if section.find("h2") else "No Heading"
#             paragraphs = [p.text for p in section.find_all("p")]

#             lists = []
#             for ul in section.find_all("ul"):
#                 lists.append([li.text for li in ul.find_all("li")])

#             image_links = [img.get("src") for img in section.find_all("img") if img.get("src")]

#             content_data.append({
#                 "heading": heading,
#                 "paragraphs": paragraphs,
#                 "lists": lists,
#                 "image_links": image_links
#             })

#         return {
#             "title": title,
#             "publication_date": publication_date,
#             "content": content_data
#         }
#     else:
#         print(f"Failed to retrieve the webpage content from {link_url}")
#         return None

# # Dictionary to store test names and their corresponding unique IDs
# test_name_to_id = {}
# current_id = 0

# # Send a GET request to the page
# response = requests.get(base_url)

# if response.status_code == 200:
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.content, 'html.parser')
#     main_section = soup.find(class_='main')

#     if main_section:
#         # Extract all <a> tags within the 'main' section
#         a_tags = extract_a_tags(main_section)
#         print(f"Extracted {len(a_tags)} links from the page.")

#         # Open a CSV file for writing
#         with open('lab_tests_data.csv', 'w', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file)
#             csv_writer.writerow(['unique_id', 'test_name', 'test_qns', 'test_ans', 'image_links'])

#             for a_tag in a_tags:
#                 link_text = a_tag['text']
#                 link_href = a_tag['href']
#                 print(f"Processing link: {link_text}")
#                 print(f"Link URL: {link_href}")

#                 if link_href:
#                     detailed_content = extract_detailed_content(f'{link_href}')
#                     print(f"Extracted detailed content for {detailed_content}")
#                     if detailed_content:
#                         test_name = link_text
#                         publication_date = detailed_content["publication_date"]

#                         for section in detailed_content['content']:
#                             question = section['heading']
#                             formatted_paragraphs = '\n'.join(section['paragraphs'])
#                             formatted_lists = '\n'.join(['\n'.join([f'• {item}' for item in lst]) for lst in section['lists']])
#                             answer = f'{formatted_paragraphs}\n{formatted_lists}'.strip()
#                             image_links = ', '.join(section['image_links']) if section['image_links'] else ''

#                             # Generate or retrieve the unique_id
#                             if test_name in test_name_to_id:
#                                 unique_id = test_name_to_id[test_name]
#                             else:
#                                 current_id += 1
#                                 unique_id = current_id
#                                 test_name_to_id[test_name] = unique_id

#                             csv_writer.writerow([unique_id, test_name, question, answer, image_links])

#         print("CSV file created successfully.")
#     else:
#         print("No element with class 'main' found.")
# else:
#     print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
