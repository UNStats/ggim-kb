from selenium import webdriver
import time
import io

driver = webdriver.Firefox(executable_path=r'c:\temp\geckodriver.exe')
driver.get("https://www.wcotradetools.org/en/harmonized-system/2022/en")

time.sleep(5)
banner =  driver.find_elements_by_class_name("eu-cookie-compliance-default-button")
banner[0].click()
time.sleep(3)
#before executing the next line, do a manual click on the bottom of the page to remove the 'banner'

section_code = '21'

section_name = driver.find_element_by_xpath("//h2[@id='hs-code:"+ section_code +"']")
time.sleep(5)

section_name.click()

#wait for few seconds before executing the following code just to allow the page to open the block
time.sleep(5)

list_links = driver.find_elements_by_class_name("chapter-item")
for i in list_links:
    i.click()
    driver.implicitly_wait(3)

time.sleep(10)

list_links = driver.find_elements_by_class_name("heading-item")
for i in list_links:
    i.click()
    driver.implicitly_wait(3)

time.sleep(10)

list_links = driver.find_elements_by_class_name("subheading-5")
for i in list_links:
    i.click()
    driver.implicitly_wait(3)

time.sleep(10)

list_links = driver.find_elements_by_class_name("subheading-item")
for i in list_links:
    i.click()
    driver.implicitly_wait(3)

time.sleep(10)

list_labels = driver.find_elements_by_xpath("//h2")
for i in list_labels:
    codeId = i.get_attribute('id')
    if 'hs-code:'+section_code in codeId:
        value = i.get_attribute('data-tippy-content')
        with io.open("c:\\temp\\outputWCO"+section_code+".txt", "a", encoding="utf-8") as f:
            f.write(codeId + '|'+ value + '\n')

time.sleep(5)


driver.quit()
