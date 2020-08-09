from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/Keke/.wdm/drivers/chromedriver/win32/84.0.4147.30/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

### NASA Latest Mars News Scaper
def mars_news(browser):

    # Scrape Mars News site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    # Delay for loading page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    try:
        slide_elem = soup.select_one("ul.item_list li.slide")
            # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
            # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError: 
        return None, None

    # Return results
    return news_title,news_p


### NASA JPL Site Scraper
def mars_images(browser):
    #browser = init_browser()

    # Scrape Mars News site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    image= browser.find_by_id("full_image")
    image.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info= browser.links.find_by_partial_text("more info")
    more_info.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    imagesoup = bs(html, "html.parser")

    img_url = imagesoup.select_one("figure.lede a img")
    img= img_url.get("src")
    # Create unique URL
    featured_img_url = f"https://www.jpl.nasa.gov{img}"

    # Close the browser after scraping
    

    return featured_img_url

# Scrape Mars Facts Site
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    df = pd.read_html("https://space-facts.com/mars/")[0]
    #print(df)
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-bordered")


# Scrape USGS Astrogeology Site
def mars_hem(browser):

    #browser = init_browser()
    
    # Visit the USGS Astrogeology site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    itemlink= browser.find_by_css("a.product-item h3")

    for item in range(len(itemlink)):
    
        hemisphere= {}
        #click on to each h3 link
        browser.find_by_css("a.product-item h3")[item].click()
        
        # find sample image tag & extract <href>
        sample = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
        
        # retrieve hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # append to List
        hemisphere_image_urls.append(hemisphere)
        
        # navigate backwards
        browser.back()
    

    return hemisphere_image_urls


def scrape():
    browser = init_browser()

    news_title, news_p = mars_news(browser)
    # news_p = mars_news(browser)
    featured_img_url= mars_images(browser)
    facts = mars_facts()
    hemisphere_image_urls = mars_hem(browser)
    timestamp = dt.datetime.now()

    mars_data= {
        "news_title": news_title,
        "news_paragraph": news_p,
        "mars_image": featured_img_url,
        "mars_facts": facts,
        "mars_hem": hemisphere_image_urls,
        "latest":timestamp
    }

    browser.quit()
    return mars_data
   

if __name__ == "__main__":
    print(scrape())