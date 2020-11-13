from hand_calculation import tile_constants
from hand_calculation.hand_calculator import HandCalculator
from hand_calculation.hand_config import HandConfig
from hand_calculation.meld import Meld
from hand_calculation.tiles import Tiles

if __name__ == '__main__':
    hand_config = HandConfig(
        is_menzen=False,
        is_tsumo=False,
        is_riichi=False,
        is_ippatsu=False,
        is_rinshan=False,
        is_chankan=False,
        is_haitei=False,
        is_houtei=False,
        is_double_riichi=False,
        is_nagashi_mangan=False,
        is_tenhou=False,
        is_chiihou=False,
        is_sanma=True,
        seat_wind=None,
        prevalent_wind=tile_constants.EAST,
        deposit_number=0,
        honba_number=0
    )

    tiles = Tiles.string_to_array(
        man="34",
        pin="406",
        sou="11",
        honours=""
    )

    win_tile = tile_constants.RED_FIVE_MAN

    melds = [
        Meld(meld_type=Meld.PON, tiles="111z"),
        Meld(meld_type=Meld.PON, tiles="777z"),
        Meld(meld_type=Meld.KITA, tiles="4444z")
    ]

    dora_indicators = []

    result = HandCalculator.calculate_hand_score(
        tiles, win_tile, melds=melds, hand_config=hand_config,
        dora_indicators=dora_indicators
    )

    for yaku in result['han_details']:
        print(yaku)
    print()
    for fu in result['fu_details']:
        print(fu)
    print()
    print('{} han, {} fu'.format(result['han'], result['fu']))
    print(result['split_scores'])
    if result['yaku_level'] != '':
        print(result['yaku_level'])
