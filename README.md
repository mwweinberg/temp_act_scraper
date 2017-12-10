# temp_act_scraper

Use the superscraper.py.  We combined temp-act-reconcile 9https://github.com/mwweinberg/temp-act-reconcile) into the old scraper, thus  making it super.

A script to scrape the registration websites for foreign NGOs registered for temporary activities in China


Oliver did most of this but he's not on github as far as I know.  In addition to the libraries you'll need to install chrome driver (https://sites.google.com/a/chromium.org/chromedriver/getting-started, specific instructions for Ubuntu here: https://christopher.su/2015/selenium-chromedriver-ubuntu/#selenium-version (don't forget to update the version number in the wget link)).

You  need to manually check to see how many pages are in the current list and change the variable on line 58 as of this writing (it is the "max_page" variable).  Also that variable value must be one more than the number of pages.
