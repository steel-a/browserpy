import time
import re
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class BrowserPy:
    """
    -> An abstract for selenium on an object.
    ##### Note: To run this class on a Docker container, use one of these params on 'docker run' command: --shm-size=1G or -v /dev/shm:/dev/shm
    """
    keys = Keys
    by = By
    driver = None

    def __init__(self, profile:str='firefox', config:dict=None):
        self.config = config
        self.profile = profile
        self.driver = None


    def __del__(self):
        if self.driver is not None:
            try: self.driver.close()
            except: pass
            finally:
                try: self.driver.quit()
                except: pass


    def __enter__(self):
        return self


    def __exit__(self, type, value, tb):
        if self.driver is not None:
            self.driver.close()
        if tb is not None:
            return False


    def createDriver(self):
        if self.profile=='chrome-headless-docker':
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            # chrome_options.headless = True # also works
            self.driver = webdriver.Chrome(options=chrome_options)
        elif self.profile=='firefox-headless-docker':
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.headless = True
            options.add_argument("-width=1920")
            options.add_argument("-height=1080")
            self.driver = webdriver.Firefox(options=options)
        elif self.profile=='firefox':
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver import FirefoxProfile
            profile = FirefoxProfile("/home/stella/.mozilla/firefox/selenium")

            options = Options()
            options.headless = False
            options.add_argument("-width=1366")
            options.add_argument("-height=768")
            self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
        elif self.profile=='firefox-headless-random':
            import random

            import requests
            r = requests.get('https://gist.githubusercontent.com/fijimunkii/952acac988f2d25bef7e0284bc63c406/raw/190452518c6bcc856b751333a0556588da0daf45/ua.json')
            userAgent = r.json()[random.randint(0,len(r.json())-1)]

            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", userAgent)

            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.headless = True
            options.add_argument("-width="+str(random.randint(1895,1915)))
            options.add_argument("-height="+str(random.randint(1035,1040)))

            self.driver = webdriver.Firefox(options=options, firefox_profile=profile)            
        elif self.profile=='chrome-remote':
            try:
                url = self.config.item['selenium-remote-url']
            except:
                raise Exception("To use chrome-remote parameter, it's necessary to pass a second parameter in BrowserPy instance creation:\na dict with a key named 'selenium-chrome-remote-url' with the url as value.")
            self.driver = webdriver.Remote(
                desired_capabilities=DesiredCapabilities.CHROME,
                command_executor=url,
            )
            self.driver.set_window_size(1920, 1080)
        elif self.profile=='firefox-remote':
            try:
                url = self.config.item['selenium-remote-url']
            except:
                raise Exception("To use chrome-remote parameter, it's necessary to pass a second parameter in BrowserPy instance creation:\na dict with a key named 'selenium-chrome-remote-url' with the url as value.")

            try:
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                options = FirefoxOptions()
                #cloud_options = {}
                #cloud_options['build'] = "build_1"
                #cloud_options['name'] = "test_abc"
                #options.set_capability('cloud:options', cloud_options)
                self.driver = webdriver.Remote(url, options=options)
                self.driver.implicitly_wait(30)
                self.driver.maximize_window() # Note: driver.maximize_window does not work on Linux selenium version v2, instead set window size and window position like driver.set_window_position(0,0) and driver.set_window_size(1920,1080)

            except:
                raise Exception("Couldn't open remote Firefox")

        else:
            raise ValueError(self.profile+' is not a valid value.')


    def open(self, url:str, assertText:str=None, assertAttempts:int=1, assertTime:float=1, numOfRefreshes:int=0):
        """
        -> Loads a web page in the current browser session
        :param url: Url to be openned
        :param assertText: Text that must be in page
        :param assertAttempts: How many tries it will be done
        :param assertTime: Time (in seconds) between tries
        :return: True/False -> True if page is load and have 'assertText' (case this parameter is used). False otherwise.
        """
        if self.driver is None:
            self.createDriver()

        self.driver.get(url)
        for _ in range(numOfRefreshes+1):
            if self.assertText(assertText, assertAttempts, assertTime):
                return True
            self.driver.refresh()
        return False


    def assertText(self, assertText:str, assertAttempts:int=1, assertTime:float=1) -> bool:
        """
        -> Search for a text inside actual page text
        :param assertText: Text that must be in page
        :param assertAttempts: How many tries it will be done
        :param assertTime: Time (in seconds) between tries
        :return: True/False. True if assertText is in actual page text
        """
        if assertText is None:
            return True #1

        if '|' in assertText:
            assertTextSplitted = assertText.split('|')
            for _ in range(assertAttempts):
                for text in assertTextSplitted:
                    if text in self.getText():
                        return True #2
                time.sleep(assertTime)
        else:
            for _ in range(assertAttempts):
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
        :param regexGroup: which regex group will be returned
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


    def el(self, by:str, name:str, text:str=None, textExactMatch:bool=True, attr:str=None, attrText:str=None, attrExactMatch:bool=True):
        """
        -> Get an element described by params 'by' and 'name' with the (optional) text 'text'
        :return: The element of type WebElement or None
        """
        if(text is None and attr is None):
            try:
                el = self.driver.find_element(self.mapBy(by),name)
            except:
                return None #1
            return el #2
        else:
            textFound = True if text is None else False
            attribFound = True if attr is None or attrText is None else False

            elements = self.getElements(by, name)
            if len(elements)==0:
                return None #3
            for e in elements:
                if (not textFound) \
                    and ((textExactMatch==True and text==e.text) \
                        or (textExactMatch==False and text in e.text)):
                    textFound = True
                if (not attribFound) \
                    and ((attrExactMatch==True and attrText==e.get_attribute(attr)) \
                        or (attrExactMatch==False and attrText in e.get_attribute(attr))):
                    attribFound = True
                if textFound and attribFound:
                    return e #4
        return None #5


    def click(self, el:WebElement, assertText:str=None, assertAttempts:int=3, assertTime:float=1, timeSleep:float=0) -> bool:
        """
        -> Click on element 'el' and optionally assert for a text on page after the click
        :return: True/False. True if click and then page has the text, False otherwise
        """
        if el is None:
            return False #1

        try:
            el.click()
        except:
            try:
                webdriver.ActionChains(self.driver).move_to_element(el).click(el).perform()
                self.driver.execute_script("arguments[0].click();", el)
            except: pass
        time.sleep(timeSleep)

        return self.assertText(assertText, assertAttempts, assertTime) #3

    def click2(self, el, timeSleep:float=0):
        webdriver.ActionChains(self.driver).move_to_element(el).click(el).perform()        

    def click3(self, el, timeSleep:float=0):
        self.driver.execute_script("arguments[0].click();", el)        

    def sendKeys(self, el:WebElement, keys, clearBefore:bool=False, assertText:str=None,
                    assertAttempts:int=3, assertTime:float=1, timeSleep:float=0) -> bool:
        """
        -> Send keys to an element and optionally assert for a text on page after the send
        :return: True/False. True if send keys and then page has the text, False otherwise
        """
        if el is None:
            return False #1

        try:
            if clearBefore:
                el.click()
                el.clear()
            if isinstance(keys, str): #->2
                el.send_keys(keys)
            elif isinstance(keys,tuple): #->3
                for k in keys:
                    el.send_keys(k)
            else:
                return False #4
        except:
            return False #5
        time.sleep(timeSleep)
        return self.assertText(assertText, assertAttempts, assertTime) #2 and 3


    def getTextFromPage(self, uri:str, assertText:str, assertAttempts:int=3, assertTime:float=3, numOfRefreshes:int=0):
        self.open(uri,assertText,assertAttempts,assertTime,numOfRefreshes)
        return self.getText()

    def select(self, el:WebElement, valueOrText, selectByVisibleText:bool=True, assertText:str=None,
                    assertAttempts:int=3, assertTime:float=1, timeSleep:float=0):
        if el != None:
            if selectByVisibleText:
                Select(el).select_by_visible_text(valueOrText)
            else:
                Select(el).select_by_value(valueOrText)
        time.sleep(timeSleep)
        return self.assertText(assertText, assertAttempts, assertTime) #2 and 3
