import time
import re
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class BrowserPy:
    """
    -> An abstract for selenium on an object.
    ##### Note: To run this class on a Docker container, use one of these params on 'docker run' command: --shm-size=1G or -v /dev/shm:/dev/shm
    """
    keys = Keys
    by = By
    driver = None

    def __init__(self, profile:str='chrome-headless-docker'):

        if profile=='chrome-headless-docker':

            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            # chrome_options.headless = True # also works
            self.driver = webdriver.Chrome(options=chrome_options)

        else:
            raise ValueError(profile+' is not a valid value.')


    def __del__(self):
        if self.driver is not None:
            self.driver.close()


    def __enter__(self):
        return self


    def __exit__(self, type, value, tb):
        if self.driver is not None:
            self.driver.close()
        if tb is not None:
            return False


    def open(self, url:str, assertText:str=None, assertAttemps:int=1, assertTime:float=1):
        """
        -> Loads a web page in the current browser session
        :param url: Url to be openned
        :param assertText: Text that must be in page
        :param assertAtemps: How many tries it will be done
        :param assertTime: Time (in secons) between tries
        :return: True/False -> True if page is load and have 'assertText' (case this parameter is used). False otherwise.
        """
        self.driver.get(url)
        return self.assertText(assertText, assertAttemps, assertTime)


    def assertText(self, assertText:str, assertAttemps:int=1, assertTime:float=1) -> bool:
        """
        -> Search for a text inside actual page text
        :param assertText: Text that must be in page
        :param assertAtemps: How many tries it will be done
        :param assertTime: Time (in secons) between tries
        :return: True/False. True if assertText is in actual page text
        """
        if assertText is None:
            return True #1

        for _ in range(assertAttemps):
            if assertText in self.getText():
                return True #2
            time.sleep(assertTime)

        return False #3


    def getText(self, by:str='tag', name:str='html', regexPattern:str=None, regexGroup:int=0):
        """
        -> Get the text of an element
        :param by: What type of element will be searched
        :param name: Param to search the element
        :param regexPattern: a regex expression to be searched inside the text of the element
        :param regexGroup: wich regex group will be returnet
        :return: Text found or '' otherwise
        """        
        e = self.el(by, name)
        if e is None:
            return '' #1
        
        if regexPattern is None:
            return e.text #2

        match = re.search(regexPattern, e.text) 
        if match:
            try:
                return match.group(regexGroup) #3
            except:
                pass #->4

        return '' #4, 5


    def mapBy(self, by:str):
        if by=="id" or by==By.ID:
            return By.ID #1,2
        elif by=="class" or by==By.CLASS_NAME:
            return By.CLASS_NAME #3,4
        elif by=="css" or by==By.CSS_SELECTOR:
            return By.CSS_SELECTOR #5,6
        elif by=="link" or by==By.LINK_TEXT:
            return By.LINK_TEXT #7,8
        elif by=="name" or by==By.NAME:
            return By.NAME #9,10
        elif by=="partialLink" or by==By.PARTIAL_LINK_TEXT:
            return By.PARTIAL_LINK_TEXT #11,12
        elif by=="tag" or by==By.TAG_NAME:
            return By.TAG_NAME #13,14
        elif by=="xpath" or by==By.XPATH:
            return By.XPATH #15,16
        else:
            raise ValueError(f'By [{by}] could not be mapped.') #17


    def getElements(self, by:str, name:str):
        """
        -> Gets all elements with type 'by' and 'name'
        :return: List of elements or a empty list
        """
        return self.driver.find_elements(self.mapBy(by),name) #1


    def el(self, by:str, name:str, text:str=None, textExactMatch:bool=True):
        """
        -> Get an element described by params 'by' and 'name' with the (optional) text 'text'
        :return: The element of type WebElement or None
        """
        if(text is None):
            try:
                el = self.driver.find_element(self.mapBy(by),name)
            except:
                return None #1
            return el #2
        else:
            elements = self.getElements(by, name)
            if len(elements)==0:
                return None #3
            for e in elements:
                if(textExactMatch==True and text==e.text) or \
                    (textExactMatch==False and text in e.text):
                    return e #4
        return None #5


    def click(self, el:WebElement, assertText:str=None, assertAttemps:int=3, assertTime:float=1) -> bool:
        """
        -> Click on element 'el' and optionally assert for a text on page after the click
        :return: True/False. True if click and then page has the text, False otherwise
        """
        if el is None:
            return False #1

        try:
            el.click()
        except:
            return False #2

        return self.assertText(assertText, assertAttemps, assertTime) #3


    def sendKeys(self, el:WebElement, keys, assertText:str=None, assertAttemps:int=3, assertTime:float=1) -> bool:
        """
        -> Send keys to an element and optionally assert for a text on page after the send
        :return: True/False. True if send keys and then page has the text, False otherwise
        """
        if el is None:
            return False #1

        try:
            if isinstance(keys, str): #->2
                el.send_keys(keys)
            elif isinstance(keys,tuple): #->3
                for k in keys:
                    el.send_keys(k)
            else:
                return False #4
        except:
            return False #5

        return self.assertText(assertText, assertAttemps, assertTime) #2 and 3


    def getTextFromPage(self, uri:str, assertText:str):
        self.open(uri,assertText)
        return self.getText()
