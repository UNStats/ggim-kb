# Web Scraping the contents of GGIM Knowledgebase

## Intro

The scripts and input data contained in this repository allow to create a backup of the public-facing contents of the [UN-GGIM Knowledge Base](http://ggim.un.org/knowledgebase/).

Scripts are written in python, using common libraries such as BeautifulSoup, Mardownify, and json.

## Preliminary manual steps

Before running the scripts, a map of the hierarchical structure of the knowledgebase was manually created (see [master_data/index.txt](master_data/index.txt). Also the contents of each "Articles" (paginated) table where manually saved as
individual html files (see [html_tables](html_tables)).

These manual steps are good candidates for further automation.

## Running the scripts

To produce the full backup of the public contents of the knowledge base, run the following scripts in order:

- [scripts/script01.py](scripts/script01.py): Converts the hierarchical structure of the knowledge base into a tree-like nested json file.
- [scripts/script02.py](scripts/script02.py): Uses the output of the previous script to loop through all the pages of the knowledge base and scrape the contents of category pages and the contents of the corresponding (locally-saved) html tables.
- [scripts/script03.py](scripts/script03.py): "Flattens" the results of the previous step into tab-delimited text files, and downloads to a local 'docs' folder all the hosted files referenced in the knowledge base articles.

## Outputs

The outputs of the webscraping process are saved both as a set of .json files and in tab-delimited format under [ouput/](output).

Hosted documentes that are referenced in the articles of the knowledge base are automatically downloaded and saved in a 'docs/' folder (.gitignored).
