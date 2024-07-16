# Filename: linkedin_profile_scraper.py

from bs4 import BeautifulSoup
import pandas as pd

def extract_profile_info(soup):
    """Extracts basic profile information such as name, location, connections, and headline."""
    name_element = soup.find('h1', class_='text-heading-xlarge')
    name = name_element.get_text(strip=True) if name_element else 'N/A'
    location = extract_location_info(soup)
    connections = extract_connections(soup)
    headline = extract_headline(soup)
    return {
        'Name': name,
        'Location': location,
        'Connections': connections,
        'Headline': headline
    }

def extract_location_info(soup):
    """Extracts the location from the profile."""
    location_element = soup.find('span', class_='text-body-small inline t-black--light break-words')
    return location_element.get_text(strip=True) if location_element else 'No Location Found'

def extract_connections(soup):
    """Extracts the number of connections."""
    connections_element = soup.find('span', class_='t-bold')
    return connections_element.get_text(strip=True) if connections_element else 'No Connections Found'

def extract_headline(soup):
    """Extracts the professional headline from the profile."""
    headline_section = soup.find('div', class_='text-body-medium break-words')
    return headline_section.get_text(strip=True) if headline_section else 'No Headline Found'

def extract_experience(soup):
    """Extracts experience details such as company, position, and duration."""
    experiences = []
    experience_section = soup.find('div', id='experience').parent if soup.find('div', id='experience') else None
    if experience_section:
        blocks = experience_section.find_all('div', {'data-view-name': 'profile-component-entity'})
        for block in blocks:
            company = block.find('div', class_='hoverable-link-text').get_text(strip=True) if block.find('div', class_='hoverable-link-text') else 'No Company Found'
            duration = block.find('span', class_='t-14 t-normal').get_text(strip=True) if block.find('span', class_='t-14 t-normal') else 'No Duration Found'
            location = block.find('span', class_='t-14 t-normal t-black--light').get_text(strip=True) if block.find('span', class_='t-14 t-normal t-black--light') else 'No Location Found'
            experiences.append({'Company': company, 'Duration': duration, 'Location': location})
    return experiences

def extract_education(soup):
    """Extracts education details such as institution, degree, and duration."""
    educations = []
    education_section = soup.find('div', id='education').parent if soup.find('div', id='education') else None
    if education_section:
        blocks = education_section.find_all('div', {'data-view-name': 'profile-component-entity'})
        for block in blocks:
            institution = block.find('div', class_='hoverable-link-text').get_text(strip=True) if block.find('div', class_='hoverable-link-text') else 'No Institution Found'
            degree = block.find('span', class_='t-14 t-normal').get_text(strip=True) if block.find('span', class_='t-14 t-normal') else 'No Degree Found'
            duration = block.find('span', class_='t-14 t-normal t-black--light').get_text(strip=True) if block.find('span', class_='t-14 t-normal t-black--light') else 'No Duration Found'
            educations.append({'Institution': institution, 'Degree': degree, 'Duration': duration})
    return educations

def save_to_excel(profile_data, experiences, educations, filename='linkedin_data.xlsx'):
    """Saves profile data, experiences, and education into an Excel file with multiple sheets."""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        pd.DataFrame([profile_data]).to_excel(writer, sheet_name='Profile')
        pd.DataFrame(experiences).to_excel(writer, sheet_name='Experiences')
        pd.DataFrame(educations).to_excel(writer, sheet_name='Education')
    print(f"Data saved to {filename}.")
