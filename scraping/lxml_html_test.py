from lxml import etree

with open('tables.html') as f:
    html = f.read()

tree = etree.HTML(html)
xpath = '/html/body/div[6]/div[1]/div/header/div[3]/ul/li[1]/a/p'

csss_l0 = 'div.u-size6of12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3)'
csss_l1 = 'div.u-size6of12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3) > button:nth-child(1)'
csss_l2 = 'div.u-size6of12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3) > div:nth-child(2)'
ff = 'div.u-size6of12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1)'
chrome = '#sbprodgrid > div > div:nth-child(3) > div > div > a > div.ProductCard-imageWrap > div > div > img' 