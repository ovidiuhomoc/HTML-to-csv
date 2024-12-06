import csv
import os

from bs4 import BeautifulSoup


def parse(table_html: str):
    soup = BeautifulSoup(table_html, 'html.parser')

    data_list = []

    # Find the table (you may need a more specific selector depending on your HTML)
    table = soup.find('table')
    tbody = table.find('tbody')

    # Iterate through each table row
    for tr in tbody.find_all('tr'):
        content_span = tr.find('span', class_='content')
        if content_span:
            # Extract Company Name
            full_company_name = None
            h2_tag = content_span.find('h2')
            if h2_tag and h2_tag.a:
                full_company_name = h2_tag.a.text.strip()

            # Extract Trading Name
            trading_name = None
            trading_b = content_span.find('b', string='Trading as:')
            if trading_b:
                # The trading name should be in the text node following this <b>
                # Something like: <b>Trading as:</b> Some Company Name
                trading_text = trading_b.next_sibling
                if trading_text:
                    # trading_text might start with ':', so we strip it and whitespace
                    trading_name = trading_text.strip(':\n\t ')

            # Extract Phone Number
            # We look for the <b> tag with text 'Phone'
            phone = None
            phone_b = content_span.find('b', string='Phone:')
            if phone_b:
                # The phone number should be in the text node following this <b>
                # Something like: <b>Phone:</b>: (555) XXX-XXXX
                phone_text = phone_b.next_sibling
                if phone_text:
                    # phone_text might start with ':', so we strip it and whitespace
                    phone = phone_text.strip(':\n\t ')

            # Extract Company Website
            company_website = None
            website_b = content_span.find('b', string='Company Website:')
            if website_b:
                # The next link after 'Company Website:' should contain the URL
                website_link = website_b.find_next('a')
                if website_link:
                    company_website = website_link.get('href', '').strip()

            # Create a dictionary for the current entry
            entry_dict = {
                'trading_name': trading_name,
                'full_company_name': full_company_name,
                'phone': phone,
                'company_website': company_website
            }

            # Add it to our list
            data_list.append(entry_dict)

    return data_list

if __name__ == '__main__':
    inputs = [{'in': os.path.join(os.path.dirname(__file__), 'rsrc', 'large_comp_table.html'),
               'out': os.path.join(os.path.dirname(__file__), 'out', 'large_comp.csv')},
              {'in': os.path.join(os.path.dirname(__file__), 'rsrc', 'medium_comp_table.html'),
               'out': os.path.join(os.path.dirname(__file__), 'out', 'medium_comp.csv')}
              ]

    for input in inputs:
        with open(input['int'], 'r') as f:
            html_parent_component = f.read()
        # write the output to a CSV file with CSV DictWriter
        with open(input['out'], 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['trading_name', 'full_company_name', 'phone', 'company_website'])
            writer.writeheader()
            for entry in parse(html_parent_component):
                writer.writerow(entry)
