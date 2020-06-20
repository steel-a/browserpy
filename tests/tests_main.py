from browserpy import BrowserPy

b = BrowserPy()

# Open github.com and Assert that 'Why GitHub?' is in openned page
assert b.open('http://www.github.com','Why GitHub?')

# function assertText
assert b.assertText(None) #1
assert b.assertText('Why GitHub?') #2
assert b.assertText('Why GitHub?',5) #2
assert b.assertText('Why GitHub?',2,5) #2
assert b.assertText('Why GitHub?',0,0) == False #3
assert b.assertText('Loren ipsum') == False #3

# function mapBy
assert b.mapBy(b.by.ID) == b.by.ID #1
assert b.mapBy('id') == b.by.ID #2
assert b.mapBy(b.by.CLASS_NAME) == b.by.CLASS_NAME #3
assert b.mapBy('class') == b.by.CLASS_NAME #4
assert b.mapBy(b.by.CSS_SELECTOR) == b.by.CSS_SELECTOR #5
assert b.mapBy('css') == b.by.CSS_SELECTOR #6
assert b.mapBy(b.by.LINK_TEXT) == b.by.LINK_TEXT #7
assert b.mapBy('link') == b.by.LINK_TEXT #8
assert b.mapBy(b.by.NAME) == b.by.NAME #9
assert b.mapBy('name') == b.by.NAME #10
assert b.mapBy(b.by.PARTIAL_LINK_TEXT) == b.by.PARTIAL_LINK_TEXT #11
assert b.mapBy('partialLink') == b.by.PARTIAL_LINK_TEXT #12
assert b.mapBy(b.by.TAG_NAME) == b.by.TAG_NAME #13
assert b.mapBy('tag') == b.by.TAG_NAME #14
assert b.mapBy(b.by.XPATH) == b.by.XPATH #15
assert b.mapBy('xpath') == b.by.XPATH #16
try:
    b.mapBy('aaaa')
except ValueError:
    assert True #17

# function getElements
assert len(b.getElements('tag','a')) > 0 #1
assert len(b.getElements('tag','aaaaaa')) == 0 #1

# function el
assert b.el('aaa','a') == None #1
assert b.el('tag','a').text != None #2
assert b.el('tag','aaaaa','aaaaa') == None #3
assert b.el('tag','a','Marketplace').text == 'Marketplace' #4
assert b.el('tag','a','aaaaa') == None #5

# function click - I could not test #2 return
assert b.click(b.el('link','aaaaa')) == False #1
assert b.click(b.el(b.by.LINK_TEXT,'Marketplace'),"Loren ipsum") == False #3
assert b.click(b.el(b.by.LINK_TEXT,'Marketplace'),"Extend GitHub") #3

# function sendKeys - I could not test #5 return
assert b.sendKeys(b.el('link','aaaaa'),'keys') == False #1
assert b.sendKeys(b.el(b.by.CLASS_NAME,'header-search-input'),'python') #2
assert b.sendKeys(b.el(b.by.CLASS_NAME,'header-search-input'),b.keys.ENTER,'repository results') #2
assert b.sendKeys(b.el(b.by.CLASS_NAME,'header-search-input'),('python',b.keys.ENTER),'repository results') #3
assert b.sendKeys(b.el(b.by.CLASS_NAME,'header-search-input'),('python',b.keys.ENTER),'Loren ipsum') == False #3
assert b.sendKeys(b.el(b.by.CLASS_NAME,'header-search-input'),list(range(5))) == False #4

# function getText
assert b.getText('tag','aaaaaaa') == '' #1
assert b.getText('tag','html') != '' #2
assert 'repository results' in b.getText(regexPattern='([0-9,]*) repository results') #3
assert 'repository results' in b.getText(regexPattern='[0-9,]* (repository results)', regexGroup=1) #3
assert 'repository results' in b.getText(b.by.TAG_NAME, 'html', '[0-9,]* (repository results)', 1) #3
assert b.getText(b.by.TAG_NAME, 'html', '[0-9,]* (repository results)', 5) == '' #4
assert b.getText(b.by.TAG_NAME, 'html', '[0-9,]* (aaaaaaaaaa)', 1) == '' #5
assert b.getText(b.by.TAG_NAME, 'html', '[0-9,]* (aaaaaaaaaa)') == '' #5
