import unittest
from .models import *
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

except ImportError as err:
    print("[!] Please check the following error log:\n=>:{}".format(str(err)))

class TestManufacturer(unittest.TestCase):
    """Manufacturer test class to test models's acceptance of new data"""

    def setUp(self):

        """
        Initiates pre-defined variables for other functions usage.
        """

        add_data = Manufacturer.objects.create(item="test", quantity=3,
                                               date_of_production='2022-12-12',
                                               sku='1000-000-0000', location='TEST-12')
        self.data = Manufacturer.objects.get(item='test')
    
    def tearDown(self):

        """
        Delete all added data through  Setup method and other test me
        thods.
        """

        self.data.delete()

    def test_data_added(self):

        self.assertEqual(self.data.item, "test")
        self.assertEqual(self.data.quantity, 3)
        self.assertEqual(self.data.sku, '1000-000-0000')
        self.assertEqual(self.data.location, 'TEST-12')


class TestConnection(unittest.TestCase):

    """
    TestConnnection Class:
         -Tests the connection through requests to check the status codes
         -Tests that the pages are accessible.
    """
    
    def setUp(self):

        self.root_url = "http://127.0.0.1:8000/inventory/"
        self.req = requests.get(self.root_url)
        self.list_urls = ['list/','graph/','manufacturer/1/','search/','myforms/','edit_manufacturer/1/']
    
    #testing the home page root page
    def test_home_page(self):
        self.assertEqual(self.req.status_code, 200)

    #testing all the pages
    def test_all_pages(self):

        for url in self.list_urls:
            self.req = requests.get(self.root_url + '/' + url)
            self.assertEqual(self.req.status_code, 200)

class SeleniumTest(unittest.TestCase):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.test_login()
        #self.add_data()
        self.get_data()

    def test_login(self):
        username = "rochdi"
        password = "hardtoguess123"

        self.driver = webdriver.Chrome()

        self.driver.get("http://127.0.0.1:8000/inventory/")

        self.driver.find_element("id", "id_username").send_keys(username)
        self.driver.find_element("id","id_password").send_keys(password)

        self.driver.find_element('id','login_btn').click()

        WebDriverWait(driver=self.driver, timeout=15).until(
            lambda x: x.execute_script("return document.readyState == 'complete'"))
        
    
        error_message = "correct username and password"

        errors = self.driver.find_elements("css selector",".errorlist.nonfield")

        for e in errors:
            print(e.text)

        if any(error_message in e.text for e in errors):
            print("Login Failed")
        else:
            print("Login was successful")
    
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
        self.driver.close()
        
    def test_get_data(self):
        self.driver.find_element("name","items_list").click()
        self.driver.find_element("name","manufacturer").click()
        data = self.driver.find_element("name","product_details")
        if data:
            print("====WE WERE ABLE TO RETRIEVE DATA===")
            print(data.text)

        
        self.assertIn("SKU", data.text)
        print("====> TEST PASSED")
        self.driver.close()

SeleniumTest()






