from PIL import Image
from image import DrawImage

img = DrawImage(Image.open("fidologo.bmp"))
img.draw_image()
