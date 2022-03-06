from PIL import Image, ImageDraw, ImageFilter, ImageFont
import json


async def build_welcome_image(member):

    # Opening JSON file
    with open('welcome_image/frames.json') as json_file:
        data = json.load(json_file)

    print(data)
    

    filename = member.display_name + str(member.id) + '.webp'

    await member.avatar_url.save('temp/' + filename)
    bg_img = Image.open('welcome_image/base_img.jpeg').copy()
    resize_size = (340, 340)
    avatar_img = Image.open('temp/' + filename).resize(resize_size)

    #mask_im = Image.new("L", resize_size, 0)
    #draw = ImageDraw.Draw(mask_im)
    #draw.ellipse(((20, 20),(320,320)), fill=255)
    #mask_im.save('mask_circle.jpg', quality=100)
    mask_im = Image.open('welcome_image/mask_circle.jpg')

    bg_img.paste(avatar_img, (420, 40),
                 mask_im.filter(ImageFilter.GaussianBlur(5)))
    draw = ImageDraw.Draw(bg_img)

    fontsize = 20
    #font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("welcome_image/BlackOpsOne-Regular.ttf",
                              fontsize)
    fullname = '@' + member.name.upper()
    while font.getsize(fullname)[0] < 769 and font.getsize(fullname)[1] < 94:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("welcome_image/BlackOpsOne-Regular.ttf",
                                  fontsize)
    xtext, ytext = font.getsize(fullname)
    xbg_img, ybg_img = bg_img.size
    #draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((226 * 2 + 780 - xtext) / 2, (373 * 2 + 90 - ytext) / 2),
              fullname, (31, 47, 81),
              font=font)

    bg_img.save('temp/edited_' + filename)
    return filename
