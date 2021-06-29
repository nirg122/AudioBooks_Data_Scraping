import requests
from bs4 import BeautifulSoup
import pandas as pd

# Creating books dict with headings
books = {'Book Number': {'Title': 'Title',
                         'Description': 'Description',
                         'Author': 'Author',
                         'Narrated By': 'Narrated By',
                         'Series': 'Series',
                         'Length': 'Length',
                         'Release Date': 'Release Date',
                         'Language': 'Language',
                         'Ratings': 'Ratings',
                         'Price': 'Price',
                         'Link': 'Link',
                         }}
# Running all through 12 pages, 50 books a page, and inserting into the books dict
book_number = 1
for n in range(1, 13):
    URL = f"https://www.audible.com/search" \
          f"?ref=a_search_c4_pageSize_3&pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=NTQ9RNETMCDMY5B8KJG3" \
          f"&keywords=book&node=18573211011&pageSize=50&page={n}"

    response = requests.get(URL)
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")

    # Every item overall info in a list
    all_audio_books = soup.find_all(name="li", class_="bc-list-item productListItem")  # Item's overall info in a list

    # Creating a dictionary of books

    for i in range(len(all_audio_books) - 1):
        # Creating Vars
        title = all_audio_books[i].find_all(name="a", class_="bc-link bc-color-link")[1].getText()
        # description
        if all_audio_books[i].find(name="span", class_="bc-text bc-size-base bc-color-secondary") is not None:
            description = all_audio_books[i].find(name="span",
                                                  class_="bc-text bc-size-base bc-color-secondary").getText()
        else:
            description = 'None'
        author = all_audio_books[i].find(name="li", class_="bc-list-item authorLabel").getText().strip().strip(
            'By:\n').strip()
        narrated_by = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
            1].getText().strip().strip('Narrated by:').strip()
        # series
        if all_audio_books[i].find(name="li", class_="bc-list-item seriesLabel") is not None:
            series = all_audio_books[i].find(name="li", class_="bc-list-item seriesLabel").getText().strip().strip(
                'Series:\n').strip()
        else:
            series = 'None'
        # length
        if series == 'None':
            length = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
                2].getText().strip('Length: ')
        else:
            length = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
                3].getText().strip('Length: ')

        # release_date
        if series == 'None':
            release_date = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
                3].getText().strip('Release date: ').strip()
        else:
            release_date = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
                4].getText().strip('Release date: ').strip()
        # language
        if series == 'None':
            language = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
                4].getText().strip('Language: ').strip()
        else:
            language = all_audio_books[i].find_all(name="span", class_="bc-text bc-size-small bc-color-secondary")[
                5].getText().strip('Language: ').strip()

        # ratings
        rating_tag = all_audio_books[i].find_all(name="li", class_="bc-list-item ratingsLabel")
        if rating_tag[0].getText().strip() != 'Not rated yet':
            ratings = " ".join(rating_tag[0].getText().strip().split('\n'))
        else:
            ratings = rating_tag[0].getText().strip()

        price = all_audio_books[i].find(name="p",
                                        class_="bc-text buybox-regular-price bc-spacing-none bc-spacing-top-none") \
            .getText().strip().strip('Regular price: ').strip()
        link = f'https://www.audible.com{all_audio_books[i].find(name="a", class_="bc-button-text")["href"]}'
        # inserting into books dict
        try:
            books[f'{book_number}'] = {
                'Title': title,
                'Description': description,
                'Author': author,
                'Narrated By': narrated_by,
                'Series': series,
                'Length': length,
                'Release Date': release_date,
                'Language': language,
                'Ratings': ratings,
                'Price': price,
                'Link': link
            }
        except IndexError:
            pass
        book_number += 1
# Saving in a .CSV file
(pd.DataFrame.from_dict(data=books, orient='index').to_csv('Books.csv', header=False))
