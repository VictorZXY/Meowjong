import os

from PIL import Image

if __name__ == '__main__':
    tile_image_names = [
        'Man1', 'Man2', 'Man3', 'Man4', 'Man5', 'Man6', 'Man7', 'Man8', 'Man9',
        'Pin1', 'Pin2', 'Pin3', 'Pin4', 'Pin5', 'Pin6', 'Pin7', 'Pin8', 'Pin9',
        'Sou1', 'Sou2', 'Sou3', 'Sou4', 'Sou5', 'Sou6', 'Sou7', 'Sou8', 'Sou9',
        'Ton', 'Nan', 'Shaa', 'Pei', 'Haku', 'Hatsu', 'Chun',
        'Man5-Dora', 'Pin5-Dora', 'Sou5-Dora'
    ]

    image_names_encoded = [
        '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
        '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
        '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
        'east', 'south', 'west', 'north', 'haku', 'hatsu', 'chun',
        '5m-red', '5p-red', '5s-red'
    ]

    background = Image.open('tiles\\transparent\\Front.png')

    for i, img_name in enumerate(tile_image_names):
        tile_image = Image.open(
            os.path.join('tiles\\transparent', img_name + '.png'))

        margin = (48, 64)
        original_size = tile_image.size
        new_size = (original_size[0] - 2 * margin[0],
                    original_size[1] - 2 * margin[1])
        tile_image = tile_image.resize(new_size, Image.ANTIALIAS)
        new_tile_image = Image.new("RGBA", original_size)
        new_tile_image.paste(tile_image, margin)

        new_image = Image.alpha_composite(background, new_tile_image)
        # new_image.save(os.path.join('tiles\\overlay', img_name + '.png'))
        new_image.save(os.path.join('temp', image_names_encoded[i] + '.png'))
