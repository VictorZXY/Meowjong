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

    background = Image.open('tiles\\transparent\\Front.png')

    for img_name in tile_image_names:
        tile_image = Image.open(
            os.path.join('tiles\\transparent', img_name + '.png'))
        new_image = Image.alpha_composite(background, tile_image)
        new_image.save(os.path.join('tiles\\overlay', img_name + '.png'))
