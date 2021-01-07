from evaluation.hand_calculation import EAST
from evaluation.hand_calculation import YakuConfig


class HandConfig:
    """
    Special class to pass various settings to the hand calculator object.
    """
    yaku = None

    is_menzen = False
    is_tsumo = False
    is_riichi = False
    is_ippatsu = False
    is_rinshan = False
    is_chankan = False
    is_haitei = False
    is_houtei = False
    is_double_riichi = False
    is_nagashi_mangan = False
    is_tenhou = False
    is_chiihou = False

    is_sanma = False
    seat_wind = None
    prevalent_wind = None
    is_dealer = False

    deposit_counter = 0  # 1000-point
    honba_counter = 0  # 100-point

    def __init__(self,
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
                 is_sanma=False,
                 seat_wind=None,
                 prevalent_wind=None,
                 deposit_counter=0,
                 honba_counter=0):
        self.yaku = YakuConfig()

        self.is_menzen = is_menzen or is_tenhou or is_chiihou
        self.is_tsumo = is_tsumo or is_tenhou or is_chiihou
        self.is_riichi = is_riichi
        self.is_ippatsu = is_ippatsu
        self.is_rinshan = is_rinshan
        self.is_chankan = is_chankan
        self.is_haitei = is_haitei
        self.is_houtei = is_houtei
        self.is_double_riichi = is_double_riichi
        self.is_nagashi_mangan = is_nagashi_mangan
        self.is_tenhou = is_tenhou
        self.is_chiihou = is_chiihou

        self.is_sanma = is_sanma
        self.seat_wind = seat_wind
        self.prevalent_wind = prevalent_wind
        self.is_dealer = (seat_wind == EAST) or is_tenhou

        self.deposit_counter = deposit_counter
        self.honba_counter = honba_counter
