# price sniper

This is a web application built with python flask. It is designed to serve data to the user from a Postgresql database built by the price-sniper web scraper, the repo for which can be found here:

[price-sniper repo](https://github.com/ccleary93/price-sniper)

The project came about when I wanted to find a programmatic way of identifying ebay auctions where the item was underpriced relative to its average sale price, so I could purchase videogames for resale.

This web frontend leverages the scraped data to deliver useful insights in a user-friendly manner.


## Dependencies

As discussed above, to make use of this web app it is necessary to have access to a database of sold items in the format described in the price-sniper readme.

The program has the following additional dependencies:

- An ebay developer account with API key (https://developer.ebay.com/).
- Ebaysdk interface for interacting with the API https://pypi.org/project/ebaysdk/.
- Psycopg2 for connecting to the Postgresql database https://www.psycopg.org/docs/.

## How it works

Main handles app routes and serves the homepage initially:

![homepage](https://i.ibb.co/f0K8hj0/homepage.png)

Based on the user's input other app routes are triggered and / or other HTML pages are loaded.

The program is modularised and makes extensive use of classes. Functions are separated out into the MatchGame, SnipeUpcoming, TitleMatcher and DataCleanser classes.

The user can use the snipe auctions feature to search for upcoming underpriced auctions based on their desired parameters:

![parameters page](https://i.ibb.co/2qqnKHX/params.png)

A set of results is displayed, each including the item description, current bid + postage, the item's mean/median sale price, number of sales logged on file, a link to the auction, and a dropdown menu allowing the user to view all historical sales of the item:

![enter image description here](https://i.ibb.co/r0QgCWQ/results.png)
