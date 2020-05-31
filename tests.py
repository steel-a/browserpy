from browserpy import BrowserPy

b = BrowserPy()
b.open('http://www.github.com','Why GitHub?')
b.click(b.el('link','Marketplace'))

