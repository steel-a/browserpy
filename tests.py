from browserpy import BrowserPy

b = BrowserPy()

# Open github.com and Assert that 'Why GitHub?' is in openned page
b.open('http://www.github.com','Why GitHub?')

# Click link 'Marketplace'
if not b.click(b.el(b.by.LINK_TEXT,'Marketplace'),"Extend GitHub"):
    print("Error clicking in the link 'Marketplace'")

# Send Keys 'python'and then 'ENTER' to selected element
if not b.sendKeys(b.el(b.by.CLASS_NAME,'header-search-input'),('python',b.keys.ENTER),'repository results'):
    print("Error senging keys to element'")

# Click on selected element and check for 'repository results' in page
print(b.getText(regexPattern='([0-9,]*) repository results'))
print(b.getText(regexPattern='([0-9,]*) repository results', regexGroup=1))