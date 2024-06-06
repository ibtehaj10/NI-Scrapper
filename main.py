from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request, jsonify
# import schedule
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


app = Flask(__name__)



@app.route('/scrape', methods=['POST'])
def VMBot():
    print("running .. ")
    def scrape_data():
        # Path to geckodriver executable
        #geckodriver_path = "geckodriver.exe"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # URL of the webpage
        url = "https://x.taostats.io/validator/5HNQURvmjjYhTSksi8Wfsw676b4owGwfLR2BFAQzG7H3HhYf#performance"

        # Setup Firefox webdriver with Selenium
        #options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')  # Run the browser in headless mode
        #driver = webdriver.Firefox(service=Service(geckodriver_path), options=options)

        # Load the webpage
        driver.get(url)

        time.sleep(5)

        def extract_data(product_container):
            vtrust_below_090 = []
            updated_above_500 = []

            # Get the HTML content of the element
            for data in product_container:
                SN = data.find_element(By.CLASS_NAME, "css-9wjxum").text
                Vali = data.find_elements(By.CLASS_NAME, "css-flded9")
                for i in Vali[1:2]:
                    try:
                        Updated = int(i.find_element(By.CLASS_NAME, "css-sxb40e").text)
                    except:
                        Updated = int(i.find_element(By.CLASS_NAME, "css-w2v")
        try:
            product_container = driver.find_elements(By.CLASS_NAME, "css-fwdaki")
            vtrust_below_090, updated_above_500 = extract_data(product_container)
        except Exception as e:
            print("Error extracting data:", e)
            vtrust_below_090, updated_above_500 = [], []

        try:
            product_container = driver.find_elements(By.CLASS_NAME, "css-1347uem")
            data1, data2 = extract_data(product_container)
            vtrust_below_090.extend(data1)
            updated_above_500.extend(data2)
        except Exception as e:
            print("Error extracting data:", e)

        # Close the browser session
        driver.quit()

        return vtrust_below_090, updated_above_500

    # Call the function to execute the scraping
    vtrust_below_090, updated_above_500 = scrape_data()
    print("here 2")
    # Prepare strings to hold the table contents
    vtrust_table = ""
    updated_table = ""

    # Populate the table strings
    if vtrust_below_090:
        vtrust_table += "The following validators have Vtrust values below 0.90:\n"
        vtrust_table += generate_table(vtrust_below_090)
        vtrust_table += "\n"

    if updated_above_500:
        updated_table += "The following validators have Updated values above 500:\n"
        updated_table += generate_table(updated_above_500)

    return [vtrust_table, updated_table]

def generate_table(data):
    table = "+----+---------+---------+\n"
    table += "| SN | Updated |  Vtrust |\n"
    table += "+----+---------+---------+\n"
    for row in data:
        table += f"| {row[0]:<2} | {row[1]:^7} | {row[2]:.5f} |\n"
    table += "+----+---------+---------+\n"
    print("generation done")
    return table


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5088)
xhz").text)
                    Vtrust = float(i.find_element(By.CLASS_NAME, "css-1yk0z1b").text)

                    if Vtrust < 0.90:
                        vtrust_below_090.append((SN, Updated, Vtrust))
                    if Updated > 500:
                        updated_above_500.append((SN, Updated, Vtrust))

            return vtrust_below_090, updated_above_500
