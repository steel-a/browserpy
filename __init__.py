import re
from selenium import webdriver
from selenium.webdriver.common.by import By

class BrowserPy:

    def __init__(self, profile:str='chrome-headless'):
        self.driver = None

        if profile=='chrome-headless':

            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            #chrome_options.add_argument("--disable-extensions")
            #chrome_options.add_argument("--disable-gpu")
            #chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            # chrome_options.headless = True # also works
            self.driver = webdriver.Chrome(options=chrome_options)

        else:
            raise ValueError(profile+' is not a valid value.')

    def __del__(self):
        if self.driver is None:
            self.driver.quit()

    def open(self, url:str, assertText:str=None):
        """
        -> Loads a web page in the current browser session
        :param url: Url to be openned
        :param assertText: After page loads, it should has this text
        :return: True if page is load and have 'assertText' (case this parameter is used). False otherwise.
        """
        if assertText is not None and assertText not in self.getText():
            return False

        return True

    def getText(self, by:str='name', name:str='html', regexPattern:str=None):
        e = self.getElement(by, name)
        if e is None:
            return ''
        
        if regexPattern is None:
            return e.text

        match = re.search(regexPattern, e.text) 
        if match:
            return match.group()
        else:
            return ''            

    def mapBy(self, by):
        if by=="id":
            return By.ID
        elif by=="class":
            return By.CLASS_NAME
        elif by=="css":
            return By.CSS_SELECTOR
        elif by=="link":
            return By.LINK_TEXT
        elif by=="name":
            return By.NAME
        elif by=="partialLink":
            return By.PARTIAL_LINK_TEXT
        elif by=="tag":
            return By.TAG_NAME
        elif by=="xpath":
            return By.XPATH
        else:
            raise ValueError(f'By [{by}] could not be mapped.')

    def getElements(self, by:str, name:str):
        elements = self.driver.find_elements(self.mapBy(by),name)
        if len(elements)>0:
            return elements
        else:
            return None

    def getElement(self, by:str, name:str, text:str=None, textExactMatch:bool=True):
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

    def click(self, by:str, name:str, text:str=None, textExactMatch:bool=True) -> bool:
        el = self.getElement(by, name, text, textExactMatch)
        if el is None:
            return False

        try:
            el.click()
        except:
            return False

        return True

    def sendKeys(self, keys:str, by:str, name:str, text:str=None, textExactMatch:bool=True) -> bool:
        el = self.getElement(by, name, text, textExactMatch)
        if el is None:
            return False

        try:
            el.sendKeys(keys)
        except:
            return False

        return True
