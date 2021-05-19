# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_data": scrape_hemi_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def scrape_hemi_data(browser):
    # ### Hemispheres

    # BOILERPLATE

    # Import Splinter and BeautifulSoup
    from splinter import Browser
    from bs4 import BeautifulSoup as soup
    from webdriver_manager.chrome import ChromeDriverManager

    # Add'l Dependencies
    import pandas as pd

    # Set up executable path and URL for scraping
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # html = browser.html

    # chal_soup = soup(html, 'html.parser')
    # chal_soup

    # Follow the steps below to use one common approach:

    # Find the HTML tag that holds all the links to the 
    # full-resolution images, or find a common CSS 
    # element for the full-resolution image.
    # "a.product-item h3"
    hemisphere_profile = browser.find_by_css("a.product-item h3")

    # Using a for loop, iterate through the tags or CSS 
    # element.
    for each in range(len(hemisphere_profile)):

    # Create an empty dictionary, hemispheres = {}, 
    # inside the for loop.
        hemispheres = {}

    # Use the for loop to complete the following actions:
        
    # a) click on each hemisphere link, 

        # hemisphere_profile_ext[x].click()
        # CANNOT USE EXTERNAL VARIBLE HERE?

        browser.find_by_css("a.product-item h3")[each].click()

    # b) navigate to the full-resolution image page,
        full_res_page = browser.links.find_by_text("Sample").first
        
    # c) retrieve the full-resolution image URL string and title 
    # for the hemisphere image, and 
        hemispheres['img_url'] = full_res_page['href']
        
        # add title pair

    # DO NOT ASSIGN VARIBLE HERE
    #     title_pair_var = browser.find_by_css("h2.title")
    #     hemispheres['title'] = title_pair_var.text
                
        hemispheres['title'] = browser.find_by_css("h2.title").text
        
        # send to OUTSIDE dictionary
        hemisphere_image_urls.append(hemispheres)
        
    # d) use browser.back() to navigate back to the beginning 
    # to get the next hemisphere image.
        
        browser.back()
        
    ### END FINAL CODE



    # BELOW: PRIOR ATTEMPTS TO SOLVE

    # html = browser.html
    # chal_soup = soup(html, 'html.parser')
    # parent_elem = chal_soup.find('div', 'collapsible results')

    # title = parent_elem.find_all('h3')
    # title

    # hemisphere_image_urls_df = pd.DataFrame(hemisphere_image_urls)
    # hemisphere_image_urls_df
    # hemisphere_image_urls_df = hemisphere_image_urls_df.append(title)
    # hemisphere_image_urls_df

    # html_url_1_base = parent_elem.find_all('a')[0].get('href')
    # html_url_2_base = parent_elem.find_all('a')[2].get('href')
    # html_url_3_base = parent_elem.find_all('a')[4].get('href')
    # html_url_4_base = parent_elem.find_all('a')[6].get('href')

    # html_url_1 = (f"{url}{html_url_1_base}")
    # html_url_2 = (f"{url}{html_url_2_base}")
    # html_url_3 = (f"{url}{html_url_3_base}")
    # html_url_4 = (f"{url}{html_url_4_base}")

    # html_list = [html_url_1, html_url_2, html_url_3, html_url_4]

    # html_series = pd.Series(html_list)
    # html_series_df = pd.DataFrame(html_series)
    # html_series_df['title'] = hemisphere_image_urls_df
    # html_series_df.columns = ['hemisphere_url', 'title']
    # html_series_df

    # parent_elem = chal_soup.find_all('a', class_='itemLink product-item')
    # parent_elem

    # for each in parent_elem:
    #     print(each)

    #     # Hemisphere link ext

    # # WHEN you reach the URL, find tag

    # 4. Print the list that holds the dictionary of each image url and title.
    # hemisphere_image_urls

    hemisphere_image_urls

    ### CHECK

    # # 4. Print the list that holds the dictionary of each image url and title.
    # hemisphere_image_urls
    # [{'img_url': 'https://marshemispheres.com/images/full.jpg',
    #   'title': 'Cerberus Hemisphere Enhanced'},
    #  {'img_url': 'https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg',
    #   'title': 'Schiaparelli Hemisphere Enhanced'},
    #  {'img_url': 'https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg',
    #   'title': 'Syrtis Major Hemisphere Enhanced'},
    #  {'img_url': 'https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg',
    #   'title': 'Valles Marineris Hemisphere Enhanced'}]

    # Note on final output cell:
    # Common URL in check cell does not match the URL given in the module challenge
    # This solution outputs img_url using the given URL
    # If the "check" URL ('https://marshemispheres.com/images/') is necessary,
    # I suggest using a for loop and string replace on the dictionary

    # End the automated browsing session
    browser.quit()





# At the end of the function, return the scraped data as a list of 
# dictionaries with the URL string and title of each hemisphere image.

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())