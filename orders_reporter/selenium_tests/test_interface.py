try:

    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    import logging

except ImportError as err:
    print("[!] Please check the following error log:\n=>:{}".format(str(err)))



class SeleniumTest():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.test_login()
        self.add_data()

    def test_login(self):
        username = "rochdi"
        password = "hardtoguess123"

        try:

            self.driver = webdriver.Chrome()
            self.driver.get("http://127.0.0.1:8000/")

            self.driver.find_element("id", "id_username").send_keys(username)
            self.driver.find_element("id","id_password").send_keys(password)
            self.driver.find_element('id','login_btn').click()
            self.driver.implicitly_wait(10)

            WebDriverWait(driver=self.driver, timeout=15).until(
                lambda x: x.execute_script("return document.readyState == 'complete'"))
            
        
            error_message = "correct username and password"

            errors = self.driver.find_elements("css selector",".errorlist.nonfield")

            for e in errors:
                print(e.text)

            if any(error_message in e.text for e in errors):
                print("---LOGIN TEST FAILE----")
            else:
                print("-----LOGIN TEST PASSED----")
        
        except Exception as e:
            error_handler = ErrorHandler(message=str(e))
            error_handler.PrintInfo()


            

    def test_search(self):
        search_q = "Books"
        self.driver.find_element("id","id_search").click()
        self.driver.find_element("name","query").send_keys(search_q)
        self.driver.find_element("id",'id_search').click()
        WebDriverWait(driver=self.driver, timeout=15).until(
            lambda x: x.execute_script("return document.readyState == 'complete'"))
        self.driver.implicitly_wait(5)
        data = self.driver.find_element("id","id_results")
        print(data.text)
        # table = self.driver.find_element('css selector','table')
        # rows = table.find_elements('tag name',"tr")

        # data = []
        # for row in rows:
        #     cols = row.find_elements('tag name','td')
        #     cols = [col.text for col in cols]
        #     data.append(cols)
        
        # self.driver.quit()
        # for row in data:
        #     print(row)


        print("----SEARCH TEST PASSED----")
    
    def add_data(self):

        item = "selenium"
        quantity= 12
        date_of_production = "12-12-2022"
        sku = "1001-000-00001"
        location = "SEL-A1"

        self.driver.find_element(By.ID, "id_form").click()
        self.driver.find_element(By.ID,"id_item").send_keys(item)
        self.driver.find_element(By.ID,"id_quantity").send_keys(quantity)
        self.driver.find_element(By.ID,"id_date_of_production").send_keys(date_of_production)   
        self.driver.find_element(By.ID,"id_sku").send_keys(sku)
        self.driver.find_element(By.ID,"id_location").send_keys(location)
        self.driver.find_element(By.ID,"btn_add").click()
        
        WebDriverWait(driver=self.driver, timeout=15).until(
            lambda x: x.execute_script("return document.readyState == 'complete'"))
        
        print("---data was added ----")
        
    def test_get_data(self):
        self.driver.find_element("name","items_list").click()
        self.driver.find_element("name","manufacturer").click()
        data = self.driver.find_element("name","product_details")
        print("=== DATA EXTRACTED =>\n\t {}".format(data.text))
        print("====> TEST PASSED=======")

SeleniumTest()