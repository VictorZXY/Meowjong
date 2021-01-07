from evaluation.hand_calculation import tile_constants
from evaluation.hand_calculation.hand_calculator import HandCalculator
from evaluation.hand_calculation.hand_config import HandConfig
from evaluation.hand_calculation.meld import Meld
from evaluation.hand_calculation.tiles import Tiles

if __name__ == '__main__':
    hand_config = HandConfig(
        is_menzen=True,
        is_tsumo=False,
        is_riichi=True,
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
        seat_wind=tile_constants.EAST,
        prevalent_wind=tile_constants.EAST,
        deposit_counter=0,
        honba_counter=1
    )

    dora_indicators = [tile_constants.SEVEN_PIN, tile_constants.WEST]

    tiles = Tiles.string_to_array(
        man="1",
        pin="",
        sou="",
        honours=""
    )

    win_tile = tile_constants.ONE_MAN

    melds = [
        Meld(meld_type=Meld.CHII, tiles="789s"),
        Meld(meld_type=Meld.PON, tiles="666z"),
        Meld(meld_type=Meld.KAN, tiles="5555z"),
        Meld(meld_type=Meld.KAN, tiles="7777z", is_open=False),
        Meld(meld_type=Meld.KITA, tiles="4z")
    ]

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
