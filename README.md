# covid19_dashboard

A module which contains a personalised Covid-19 dashboard which maps up-to-date Covid-19 data to a web template, and using event driven architecture can schedule updates to the data.

**Made using Python 3.9.9**

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install covid19_dashboard_max.

```bash
pip install covid19_dashboard_max
```

## Usage

```python
import covid19_dashboard


covid19_dashboard.run()
```
Firstly import the module, secondly call the function run() as above, which will open the dashboard using your loopback IP address,in your webbrowser.


## How-to-use (web-app)


## License
[Unlicense](https://choosealicense.com/licenses/unlicense/)

## Developer documentation
The package itself is made up of 4 python files:
1. The first of which, covid_data_handler, contains several functions which are used to read data from a csv file, containing COVID-19 data, named "nation_2021-10-28.csv". It also contains a function used to schedule the events on the web-app, and another function which using the Public Health England uk_covid19 modules creates an API request for up to date covid data. Note that the default location of the data is Exeter, if you want data about another location you need to change the default parameters of the function
2. The second, covid_news_handling, contains all the necessary functions to create an API request to [NewsAPI.org](https://newsapi.org/) and extract the data, as well as function to store what news the user has removed in order to not show the user this news again
3. The third file contains the decorators for the web-app, using the flask module this file starts up the web-server and decorates the web page with the correct data and uses event driven architecture to allow the user to schedule updates whenever they want to the data
4. The final file contains useful functions for working with times and how to convert them
The package also includes a html template which, while bland, creates an interface for the user to see the data and schedule their own updates to it.

Finally, the package contains a folder named test which contains a file for each of the data handler files to test all functions in the code using the built-in python assert function

##### All code was written by Max Bennett, for the purpose of education