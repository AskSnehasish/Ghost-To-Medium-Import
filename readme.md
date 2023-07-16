# Web Scraping and Data Processing Project

This project consists of a Node.js script and a Python script that work together to extract and categorize URLs from a sitemap, and then automate the process of importing posts to Medium.

## Project Structure

- `index.cjs`: This is the main Node.js script. It processes a Python script using Node.js's `child_process` module, sends a list of data to the Python script, and receives the processed data in return. It also uses Puppeteer to automate some web interactions on the Medium import page.

- `sitemap_reader.py`: This Python script receives a sitemap URL from the Node.js script, extracts all URLs listed in the sitemap, visits each URL to extract the category of the post, and then categorizes each URL based on the extracted category.

## Installation

Make sure you have Node.js and Python installed on your machine. You can download them from their official websites:

- Node.js: https://nodejs.org/
- Python: https://www.python.org/

Then, clone this repository to your local machine:

```bash
git clone https://github.com/AskSnehasish/Ghost-To-Medium-Import.git
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

