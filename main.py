import src.scraping_cities as cities
import src.scraping_companies as companies
import src.scraping_data as data

data.get(companies.get(cities.get()))
