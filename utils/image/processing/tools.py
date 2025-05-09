from PIL import ImageChops, Image as pilImage


def crop_white_borders_with_padding(image: pilImage.Image, padding: int = 20) -> pilImage.Image:
    bg = pilImage.new(image.mode, image.size, (255, 255, 255))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()

    if not bbox:
        return image
    
    cropped = image.crop(bbox)

    new_width = cropped.width + 2 * padding
    new_height = cropped.height + 2 * padding

    new_img = pilImage.new(image.mode, (new_width, new_height), (255, 255, 255))
    new_img.paste(cropped, (padding, padding))

    return new_img