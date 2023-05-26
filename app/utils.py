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
        draw.text((x, y), lines[0], fill='white', font=myFont, stroke_width=2 , stroke_fill=(0, 0, 0))
    else:
        y = 10
        line_width, line_height = myFont.getsize(lines[0])
        x = (image_width-line_width)//2
        draw.text((x, y), lines[0], fill='white', font=myFont, stroke_width=2 , stroke_fill=(0, 0, 0))
        y = image_height - (len(lines)-1) * char_height - 10
        for line in lines[1:]:
            line_width, line_height = myFont.getsize(line)
            x = (image_width-line_width)//2
            draw.text((x, y), line, fill='white', font=myFont, stroke_width=2 , stroke_fill=(0, 0, 0))
            y += line_height
    return image_to_byte_array(image)


def dem_gen(payload, meme_text):
    if "\n" in meme_text:
        lines = meme_text.split("\n")
    else:
        lines = textwrap.wrap(meme_text, width=30)

    image = Image.open(io.BytesIO(payload))

    width, height = 1080, 1080

    image = image.resize((width-100, height-300))

    meme_image = Image.new('RGB', (width, height), 'black')
    meme_white = Image.new('RGB', (width - 80, height-280), 'white')
    meme_b_on_w = Image.new('RGB', (width - 90, height-290), 'black')

    image_position = ((width - image.width) // 2, ((height - image.height) // 2)-90)
    image_position_w = ((width - meme_white.width) // 2, ((height - meme_white.height) // 2)-90)
    image_position_b_on_w = ((width - meme_b_on_w.width) // 2, ((height - meme_b_on_w.height) // 2)-90)

    meme_image.paste(meme_white, image_position_w)
    meme_image.paste(meme_b_on_w, image_position_b_on_w)
    meme_image.paste(image, image_position)
    #meme_image.show()
    draw = ImageDraw.Draw(meme_image)

    font_path = "Impact.ttf"
    title_font = ImageFont.truetype(font_path, 60)
    subtitle_font = ImageFont.truetype(font_path, 40)

    title_bbox = draw.textbbox((0, 0), lines[0], font=title_font)
    title_position = ((width - title_bbox[2]) // 2, height - 160)
    draw.text(title_position, lines[0], font=title_font, fill='white')
    if len(lines) > 1:
        subtitle_bbox = draw.textbbox((0, 0), lines[1], font=subtitle_font)
        subtitle_position = ((width - subtitle_bbox[2]) // 2, height - 60)
        draw.text(subtitle_position, lines[1], font=subtitle_font, fill='white')

    #image.show()
    return image_to_byte_array(meme_image)
