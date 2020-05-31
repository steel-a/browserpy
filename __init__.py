import time
import re
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class BrowserPy:
    keys = Keys
    by = By

    def __init__(self, profile:str='chrome-headless'):
        self.driver = None


        if profile=='chrome-headless':

            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            # chrome_options.headless = True # also works
            #chrome_options.add_argument("--disable-dev-shm-usage") # or in docker run command: --shm-size=1G or -v /dev/shm:/dev/shm
            self.driver = webdriver.Chrome(options=chrome_options)

        else:
            raise ValueError(profile+' is not a valid value.')


    def __del__(self):
        if self.driver is None:
            self.driver.quit()


    def open(self, url:str, assertText:str=None, assertAttemps:int=1, assertTime:float=1):
        """
        -> Loads a web page in the current browser session
        :param url: Url to be openned
        :param assertText: After page loads, it should has this text
        :return: True if page is load and have 'assertText' (case this parameter is used). False otherwise.
        """
        self.driver.get(url)
        return self.assertText(assertText, assertAttemps, assertTime)


    def assertText(self, assertText:str, assertAttemps:int=1, assertTime:float=1) -> bool:
        if assertText is None:
            return True

        for _ in range(assertAttemps):
            if assertText in self.getText():
                return True
            time.sleep(assertTime)

        return True        


    def getText(self, by:str='tag', name:str='html', regexPattern:str=None, regexGroup:int=0):
        e = self.el(by, name)
        if e is None:
            return ''
        
        if regexPattern is None:
            return e.text

        match = re.search(regexPattern, e.text) 
        if match:
            try:
                return match.group(regexGroup)
            except:
                pass

        return ''            


    def mapBy(self, by:str):
        if by=="id" or by==By.ID:
            return By.ID
        elif by=="class" or by==By.CLASS_NAME:
            return By.CLASS_NAME
        elif by=="css" or by==By.CSS_SELECTOR:
            return By.CSS_SELECTOR
        elif by=="link" or by==By.LINK_TEXT:
            return By.LINK_TEXT
        elif by=="name" or by==By.NAME:
            return By.NAME
        elif by=="partialLink" or by==By.PARTIAL_LINK_TEXT:
            return By.PARTIAL_LINK_TEXT
        elif by=="tag" or by==By.TAG_NAME:
            return By.TAG_NAME
        elif by=="xpath" or by==By.XPATH:
            return By.XPATH
        else:
            raise ValueError(f'By [{by}] could not be mapped.')


    def getElements(self, by:str, name:str):
        elements = self.driver.find_elements(self.mapBy(by),name)
        if len(elements)>0:
            return elements
        else:
            return None


    def el(self, by:str, name:str, text:str=None, textExactMatch:bool=True):
        if(text is None):
            try:
                el = self.driver.find_element(self.mapBy(by),name)
            except:
                return None
            return el
        else:
            elements = self.getElements(by, name)
            if elements is None:
                return None
            for e in elements:
                if(textExactMatch==True and text==e.text) or \
                    (textExactMatch==False and text in e.text):
                    return e
        return None


    def click(self, el:WebElement, assertText:str=None, assertAttemps:int=3, assertTime:float=1) -> bool:
        if el is None:
            return False

        try:
            el.click()
        except:
            return False

        return self.assertText(assertText, assertAttemps, assertTime)


    def sendKeys(self, el:WebElement, keys, assertText:str=None, assertAttemps:int=3, assertTime:float=1) -> bool:
        if el is None:
            return False

        try:
            if isinstance(keys, str):
                el.send_keys(keys)
            elif isinstance(keys,tuple):
                for k in keys:
                    el.send_keys(k)
        except: # Exception as inst:
            return False

        return self.assertText(assertText, assertAttemps, assertTime)

