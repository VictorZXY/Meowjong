from PIL import Image


def concat_tile_images_horizontally(tile_images, filename):
    widths, heights = zip(*(i.size for i in tile_images))

    width = max(widths)
    total_width = sum(widths)
    max_height = max(heights)
    boarder_width = 20
    margin = 60
    triplet_width = (width + margin) * 3

    output_image = Image.new('RGB', (total_width + 15 * margin,
                                     max_height + 2 * margin))

    for x in range(output_image.size[0]):  # for every pixel:
        for y in range(output_image.size[1]):
            if boarder_width <= x < output_image.size[0] - boarder_width \
                    and boarder_width <= y < output_image.size[1] - boarder_width:
                if not (triplet_width + 20 <= x < triplet_width + 40
                        or triplet_width * 2 + 20 <= x < triplet_width * 2 + 40
                        or triplet_width * 3 + 20 <= x < triplet_width * 3 + 40
                        or triplet_width * 4 + 20 <= x < triplet_width * 4 + 40):
                    output_image.putpixel((x, y), (255, 255, 255))

    x_offset = margin
    for image in tile_images:
        output_image.paste(image, (x_offset, margin))
        x_offset += image.size[0] + margin

    output_image.save(filename)


def concat_tile_images_vertically(tile_images, filename):
    widths, heights = zip(*(i.size for i in tile_images))

    total_height = sum(heights)
    max_width = max(widths)
    margin = max(heights) // 8

    output_image = Image.new('RGB', (max_width,
                                     total_height + margin * len(tile_images)))

    for x in range(output_image.size[0]):  # for every pixel:
        for y in range(output_image.size[1]):
            output_image.putpixel((x, y), (255, 255, 255))

    y_offset = margin // 2
    for image in tile_images:
        output_image.paste(image, (0, y_offset))
        y_offset += image.size[1] + margin

    output_image.save(filename)


if __name__ == '__main__':
    hand = [Image.open(x) for x in [
        'tiles\\opaque\\Man1.png',
        'tiles\\opaque\\Man1.png',
        'tiles\\opaque\\Man1.png',
        'tiles\\opaque\\Pin3.png',
        'tiles\\opaque\\Pin4.png',
        'tiles\\opaque\\Pin5.png',
        'tiles\\opaque\\Sou6.png',
        'tiles\\opaque\\Sou7.png',
        'tiles\\opaque\\Sou8.png',
        'tiles\\opaque\\Chun.png',
        'tiles\\opaque\\Chun.png',
        'tiles\\opaque\\Chun.png',
        'tiles\\opaque\\Ton.png',
        'tiles\\opaque\\Ton.png',
    ]]

    concat_tile_images_horizontally(hand, 'hand.png')

    tiles = [Image.open(x) for x in [
        'tiles\\opaque\\Man1.png',
        'tiles\\opaque\\Man2.png',
        'tiles\\opaque\\Man3.png',
        'tiles\\opaque\\Man4.png',
        'tiles\\opaque\\Man5.png',
        'tiles\\opaque\\Man6.png',
        'tiles\\opaque\\Man7.png',
        'tiles\\opaque\\Man8.png',
        'tiles\\opaque\\Man9.png',
        'tiles\\opaque\\Pin1.png',
        'tiles\\opaque\\Pin2.png',
        'tiles\\opaque\\Pin3.png',
        'tiles\\opaque\\Pin4.png',
        'tiles\\opaque\\Pin5.png',
        'tiles\\opaque\\Pin6.png',
        'tiles\\opaque\\Pin7.png',
        'tiles\\opaque\\Pin8.png',
        'tiles\\opaque\\Pin9.png',
        'tiles\\opaque\\Sou1.png',
        'tiles\\opaque\\Sou2.png',
        'tiles\\opaque\\Sou3.png',
        'tiles\\opaque\\Sou4.png',
        'tiles\\opaque\\Sou5.png',
        'tiles\\opaque\\Sou6.png',
        'tiles\\opaque\\Sou7.png',
        'tiles\\opaque\\Sou8.png',
        'tiles\\opaque\\Sou9.png',
        'tiles\\opaque\\Ton.png',
        'tiles\\opaque\\Nan.png',
        'tiles\\opaque\\Shaa.png',
        'tiles\\opaque\\Pei.png',
        'tiles\\opaque\\Front.png',
        'tiles\\opaque\\Hatsu.png',
        'tiles\\opaque\\Chun.png',
    ]]

    concat_tile_images_vertically(tiles, 'tile_indices.png')
