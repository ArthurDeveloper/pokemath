# Simple script to generate numbers from 0 to 100
from PIL import Image, ImageDraw, ImageFont

for i in range(101):
    # Create a new image with a white background
    img = Image.new("RGB", (177, 177), (255, 255, 255))

    # Get a drawing context
    draw = ImageDraw.Draw(img)

    # Draw a border around the image
    draw.rectangle([(0, 0), (176, 176)], outline=(0, 0, 0), width=5)

    # Get a font
    font = ImageFont.truetype("res/PublicSans-VariableFont_wght.ttf", 128)

    # Draw the number in the center of the image
    w, h = draw.textsize(str(i), font=font)
    draw.text(((177 - w) / 2, (177 - h - 20) / 2), str(i), font=font, fill=(0, 0, 0))

    # Save the image to a file
    img.save("res/square_{}.jpg".format(i))

