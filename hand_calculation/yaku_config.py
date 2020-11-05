from hand_calculation.yaku_list import MenzenTsumo, Riichi, Ippatsu, Chankan, \
    RinshanKaihou, HaiteiRaoyue, HouteiRaoyui, East, South, West, North, Haku, \
    Hatsu, Chun, Tanyao, Iipeikou, Pinfu, Chanta, Ikkitsuukan, SanshokuDoujun, \
    SanshokuDoukou, DoubleRiichi, Toitoihou, Sankantsu, Sanankou, Shousangen, \
    Honroutou, Chiitoitsu, Junchan, Honitsu, Ryanpeikou, Chinitsu, NagashiMangan
from hand_calculation.yaku_list.yakuman import Tenhou, Chiihou, Daisangen, \
    Suuankou, KokushiMusou


class YakuConfig:
    def __init__(self):
        # 1 fan yaku
        self.menzen_tsumo = MenzenTsumo()
        self.riichi = Riichi()
        self.ippatsu = Ippatsu()
        self.chankan = Chankan()
        self.rinshan_kaihou = RinshanKaihou()
        self.haitei_raoyue = HaiteiRaoyue()
        self.houtei_raoyui = HouteiRaoyui()
        self.east = East()
        self.south = South()
        self.west = West()
        self.north = North()
        self.haku = Haku()
        self.hatsu = Hatsu()
        self.chun = Chun()
        self.tanyao = Tanyao()
        self.iipeikou = Iipeikou()
        self.pinfu = Pinfu()

        # 2 fan yaku
        self.chanta = Chanta()
        self.ikkitsuukan = Ikkitsuukan()
        self.sanshoku_doujun = SanshokuDoujun()
        self.sanshoku_doukou = SanshokuDoukou()
        self.double_riichi = DoubleRiichi()
        self.toitoihou = Toitoihou()
        self.sankantsu = Sankantsu()
        self.sanankou = Sanankou()
        self.shousangen = Shousangen()
        self.honroutou = Honroutou()
        self.chiitoitsu = Chiitoitsu()

        # 3 fan yaku
        self.junchan = Junchan()
        self.honitsu = Honitsu()
        self.ryanpeikou = Ryanpeikou()

        # 6 fan yaku
        self.chinitsu = Chinitsu()

        # Nagashi mangan
        self.nagashi_mangan = NagashiMangan()

        # Yakuman
        self.tenhou = Tenhou()
        self.chiihou = Chiihou()
        self.daisangen = Daisangen()
        self.suuankou = Suuankou()
        self.kokushi_musou = KokushiMusou()
