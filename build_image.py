from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import json

welcome_dir = 'welcome_image/'
base_img_filename = 'base_img.png'
mask_circle_filename = 'mask_circle.jpg'
temp_dir = 'temp/'


async def build_welcome_image(member):
    # Opening JSON file
    with open(welcome_dir + 'frames.json') as json_file:
        data = json.load(json_file)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    filename = member.display_name + str(member.id) + '.webp'

    await member.avatar_url.save(temp_dir + filename)

    square_size, ellipse, tl_corner_photo, gaussian_blur_radius = process_json_data(data, data_type='photo')

    bg_img = Image.open(welcome_dir + base_img_filename).copy()
    resize_size = square_size
    avatar_img = Image.open(temp_dir + filename).resize(resize_size)

    full_mask_circle_filename = welcome_dir + mask_circle_filename
    if not os.path.exists(full_mask_circle_filename) or not os.getenv('DEPLOY', None):
        mask_im = Image.new("L", resize_size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((ellipse[0], ellipse[1]),
                     fill=255)
        mask_im.save(full_mask_circle_filename, quality=100)

    mask_im = Image.open(full_mask_circle_filename)

    bg_img.paste(avatar_img, tl_corner_photo, mask_im.filter(ImageFilter.GaussianBlur(gaussian_blur_radius)))
    draw = ImageDraw.Draw(bg_img)

    max_size, sum_borders, rgb_name, border = process_json_data(data, data_type='name')

    fontsize = 20
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font_filename = None
    for file in os.listdir(welcome_dir):
        if file.endswith(".ttf") or file.endswith(".otf"):
            font_filename = file
            break
    full_font_filename = welcome_dir + font_filename

    font = ImageFont.truetype(full_font_filename, fontsize)
    fullname = '@' + member.name.upper()
    bounds = font.getbbox(fullname)  # (left, top, right, bottom)
    while bounds[2] - bounds[0] < max_size.get("x") and bounds[3] - bounds[1] < max_size.get("y"):
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(full_font_filename,
                                  fontsize)
        bounds = font.getbbox(fullname)
    font = ImageFont.truetype(full_font_filename, fontsize - 1)

    (xtext, ytext) = (bounds[2] - bounds[0], bounds[3] - bounds[1])

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((sum_borders.get("x") - xtext) / 2, (sum_borders.get("y") - ytext) / 2), fullname, fill=rgb_name, font=font, anchor="lt", **border)
    bg_img.save(temp_dir + 'edited_' + filename)
    return filename


def process_json_data(data, data_type=''):
    if data_type == 'photo':
        photo_measures = data.get("photo")
        square_size = (photo_measures.get("side_size"),) * 2
        ellipse = [(photo_measures.get("padding"),) * 2,
                   (photo_measures.get("side_size") - photo_measures.get("padding"),) * 2]
        tl_corner = tuple(photo_measures.get("tl_corner"))
        gaussian_blur_radius = photo_measures.get("gaussian_blur_radius")

        return square_size, ellipse, tl_corner, gaussian_blur_radius
    elif data_type == 'name':
        name_measures = data.get("name")
        sum_borders = {}
        max_size = {}
        for axis in ["x", "y"]:
            sum_borders.update({axis: name_measures.get(axis)[1] + name_measures.get(axis)[0]})
            max_size.update({axis: name_measures.get(axis)[1] - name_measures.get(axis)[0] - name_measures.get("padding")})
        rgb_name = tuple(name_measures.get("rgb"))
        border = name_measures.get("border")
        if border:
            border.update({'stroke_fill': tuple(border.get('stroke_fill'))})
        else:
            border = {}
        return max_size, sum_borders, rgb_name, border
    return None
