
from utils import HTMLComponent


img = HTMLComponent('img')
img.set_attribute('src', '/slash')

div = HTMLComponent('div', is_container=True)
div.append(img)
div.append(img)
print(div.render())