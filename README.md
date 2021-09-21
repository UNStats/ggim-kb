# Web Scraping the contents of GGIM Knowledgebase

The scripts and input data contained in this repository allow to create a backup of the public-facing contents of the [UN-GGIM Knowledge Base](http://ggim.un.org/knowledgebase/).

Scripts are written in python, using common libraries such as BeautifulSoup, Mardownify, and json.

Before running the scripts, a map of the hierarchical structure of the knowledgebase was manually created (see [master_data/index.txt](master_data/index.txt). Also the contents of each "Articles" (paginated) table where manually saved as individual html files (see [html_tables](html_tables)).

The outputs of the webscraping process are saved both as a set of .json files and in tab-delimited format under [ouput/](output).

Hosted documentes that are referenced in the articles of the knowledge base are automatically downloaded and saved in a 'docs/' folder (.gitignored).
