const { spawn } = require("child_process");
const puppeteer = require('puppeteer');

const PYTHON_SCRIPT_PATH = "./sitemap_reader.py";
const BROWSER_URL = 'http://localhost:9222';
const MEDIUM_IMPORT_URL = 'https://medium.com/p/import';

// Converts a string to CamelCase
function convertToCamelCase(str) {
  return str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
}

// Sanitizes a string by removing special characters and trailing spaces
function sanitizeString(str) {
  return str
    .replace(/[^a-zA-Z0-9\s]/g, "") 
    .trim(); 
}

// Processes the python script and returns the processed data
async function processPythonScript() {
  return new Promise((resolve, reject) => {
    const python = spawn("python3", [PYTHON_SCRIPT_PATH]);
    const list = ["https://blog.snehasish.dev/sitemap-posts.xml"];

    // Send data to python script
    python.stdin.write(JSON.stringify(list));
    python.stdin.end();

    // Receive data from python script
    python.stdout.on("data", (tableData) => {
      try {
        console.log(tableData.toString().replaceAll("'", '"'));
        const tables = JSON.parse(tableData.toString().replaceAll("'", '"'));
        resolve(tables);
      } catch (error) {
        reject(new Error("Error parsing JSON: " + error));
      }
    });

    python.stderr.on("data", (data) => {
      reject(new Error(`Python Error: ${data}`));
    });

    python.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`Python process closed with code ${code}`));
      }
    });
  });
}

// Automates the process of importing an article to Medium
async function importToMedium(urlData) {
  const browser = await puppeteer.connect({browserURL: BROWSER_URL, headless: false});
  
  // Use the connected browser
  const page = await browser.newPage();
  await page.goto(MEDIUM_IMPORT_URL);
  await page.type('.defaultValue', urlData.url); 
  await page.waitForSelector('[data-action="import-url"]');
  await page.click('[data-action="import-url"]');
  await page.waitForSelector('[data-action="overlay-close"]');
  await page.click('[data-action="overlay-close"]');
  await page.waitForSelector('[data-action="show-prepublish"]');
  await page.click('[data-action="show-prepublish"]');
  await page.waitForSelector('.tags-input');
  await page.click('.tags-input');
  await page.type('.tags-input', urlData.category); 
  
  await page.waitForSelector('[data-action-value='+urlData.category+']');
  await page.click('[data-action-value='+urlData.category+']');

  await page.waitForSelector('[data-action="publish"]');
  await page.click('[data-action="publish"]');
}

// Main function
async function main() {
  try {
    const result = await processPythonScript();
    for (const urlData of result) {
      await importToMedium(urlData);
    }
  } catch (error) {
    console.error(error);
  }
}

main();
