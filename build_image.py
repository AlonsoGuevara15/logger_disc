import PIL.Image
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import json

welcome_dir = 'welcome_image/'
base_img_filename = 'base_img.png'
mask_circle_filename = 'mask_circle.png'
temp_dir = 'temp/'
bg_color_filename = 'bg_{}.png'
bg_color_dir = welcome_dir + 'bg_colors/'


async def build_welcome_image(member):
    # Opening JSON file
    with open(welcome_dir + 'frames.json') as json_file:
        data = json.load(json_file)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    filename = member.display_name + str(member.id) + '.webp'

    await member.avatar_url.save(temp_dir + filename)

    square_size, ellipse, tl_corner_photo, gaussian_blur_radius, bg_colors = process_json_data(data, data_type='photo')

    bg_img = Image.open(welcome_dir + base_img_filename).copy()
    resize_size = square_size
    avatar_img = Image.open(temp_dir + filename).resize(resize_size, PIL.Image.ANTIALIAS)

    full_mask_circle_filename = welcome_dir + mask_circle_filename
    if not os.path.exists(full_mask_circle_filename) or not os.getenv('DEPLOY', None):
        mask_im = Image.new("L", resize_size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((ellipse[0], ellipse[1]),
                     fill=255)
        mask_im.save(full_mask_circle_filename, quality=100, subsampling=0)

    mask_im = Image.open(full_mask_circle_filename)

    for bc in bg_colors:
        str_rgb = ''.join(str(i) for i in bc.get('rgb'))

        full_bg_filename = bg_color_dir + bg_color_filename.format(str_rgb)
        if not os.path.exists(bg_color_dir):
            os.makedirs(bg_color_dir)

        if not os.path.exists(full_bg_filename) or not os.getenv('DEPLOY', None):
            bg_color = Image.new("RGB", resize_size, bc.get('rgb'))
            bg_color.save(full_bg_filename, quality=100, subsampling=0)

        bg_color = Image.open(full_bg_filename)

        bg_img.paste(bg_color, (tl_corner_photo[0] + bc.get('x_offset'), tl_corner_photo[1]), mask_im.filter(ImageFilter.GaussianBlur(gaussian_blur_radius)))

    bg_img.paste(avatar_img, tl_corner_photo, mask_im.filter(ImageFilter.GaussianBlur(gaussian_blur_radius)))
    draw = ImageDraw.Draw(bg_img)

    max_size, sum_borders, text_colors = process_json_data(data, data_type='name')

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
    for c in text_colors:
        draw.text((((sum_borders.get("x") - xtext) / 2) + c.get("x_offset"), (sum_borders.get("y") - ytext) / 2), fullname, fill=c.get("rgb"), font=font, anchor="lt", **c.get("border"))
    bg_img.save(temp_dir + 'edited_' + filename, quality=100, subsampling=0)
    return filename


def process_json_data(data, data_type=''):
    if data_type == 'photo':
        photo_measures = data.get("photo")
        square_size = (photo_measures.get("side_size"),) * 2
        ellipse = [(photo_measures.get("padding"),) * 2,
                   (photo_measures.get("side_size") - photo_measures.get("padding"),) * 2]
        tl_corner = tuple(photo_measures.get("tl_corner"))
        gaussian_blur_radius = photo_measures.get("gaussian_blur_radius")

        colors = photo_measures.get("bg_colors", [])
        for idx, item in enumerate(colors):
            item.update({"rgb": tuple(item.get("rgb"))})
            colors[idx] = item
        bg_colors = sorted(colors, key=lambda i: i['z_index'])
        return square_size, ellipse, tl_corner, gaussian_blur_radius, bg_colors
    elif data_type == 'name':
        name_measures = data.get("name")
        sum_borders = {}
        max_size = {}
        for axis in ["x", "y"]:
            sum_borders.update({axis: name_measures.get(axis)[1] + name_measures.get(axis)[0]})
            max_size.update({axis: name_measures.get(axis)[1] - name_measures.get(axis)[0] - name_measures.get("padding")})
        colors = name_measures.get("colors")
        for idx, item in enumerate(colors):
            item.update({"rgb": tuple(item.get("rgb"))})
            border = item.get("border")
            if border:
                border.update({'stroke_fill': tuple(border.get('stroke_fill'))})
            else:
                border = {}
            item.update({"border": border})
            colors[idx] = item

        text_colors = sorted(colors, key=lambda i: i['z_index'])
        return max_size, sum_borders, text_colors
    return None
