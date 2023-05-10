
import io

import textwrap

from PIL import Image, ImageDraw, ImageFont

def image_to_byte_array(in_image) -> bytes:
    imgByteArr = io.BytesIO()
    in_image.save(imgByteArr, format="jpeg")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def pic_gen(payload, meme):
    image = Image.open(io.BytesIO(payload))
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    if image_width < image_height:
        font_size = int(image_width/10)
    else:
        font_size = int(image_height/10)

    myFont = ImageFont.truetype(font='Impact.ttf', size=font_size)

    char_width, char_height = myFont.getsize('A')
    chars_per_line = image_width//char_width
    lines = textwrap.wrap(meme, width=chars_per_line)
    if len(lines) == 1:
        line_width, line_height = myFont.getsize(lines[0])
        y = image_height - line_height - 10
        x = (image_width-line_width)//2
        draw.text((x, y), lines[0], fill='white', font=myFont)
    else:
        y = 10
        line_width, line_height = myFont.getsize(lines[0])
        x = (image_width-line_width)//2
        draw.text((x, y), lines[0], fill='white', font=myFont)
        y = image_height - (len(lines)-1) * char_height - 10
        for line in lines[1:]:
            line_width, line_height = myFont.getsize(line)
            x = (image_width-line_width)//2
            draw.text((x, y), line, fill='white', font=myFont)
            y += line_height
    return image_to_byte_array(image)
