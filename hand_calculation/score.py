class Score:
    MANGAN = 'Mangan'
    HANEMAN = 'Haneman'
    BAIMAN = 'Baiman'
    SANBAIMAN = 'Sanbaiman'
    KAZOE_YAKUMAN = 'Kazoe Yakuman'
    YAKUMAN = 'Yakuman'
    DOUBLE_YAKUMAN = 'Double Yakuman'
    TRIPLE_YAKUMAN = 'Triple Yakuman'

    @staticmethod
    def calculate_score(han, fu, hand_config):
        if han >= 13:
            yaku_level = Score.KAZOE_YAKUMAN
            base_points = 8000
        elif 11 <= han <= 12:
            yaku_level = Score.SANBAIMAN
            base_points = 6000
        elif 8 <= han <= 10:
            yaku_level = Score.BAIMAN
            base_points = 4000
        elif 6 <= han <= 7:
            yaku_level = Score.HANEMAN
            base_points = 3000
        elif han == 5 or (han == 4 and fu >= 40) or (han == 3 and fu >= 70):
            yaku_level = Score.MANGAN
            base_points = 2000
        else:
            yaku_level = ''
            base_points = fu * pow(2, 2 + han)

        rounded = (base_points + 99) // 100 * 100
        double_rounded = (2 * base_points + 99) // 100 * 100
        four_rounded = (4 * base_points + 99) // 100 * 100
        six_rounded = (6 * base_points + 99) // 100 * 100

        if hand_config.is_dealer:
            if hand_config.is_tsumo:
                if hand_config.is_sanma:
                    score = 2 * double_rounded
                else:
                    score = 3 * double_rounded
            else:
                score = six_rounded
        else:
            if hand_config.is_tsumo:
                if hand_config.is_sanma:
                    score = double_rounded + rounded
                else:
                    score = double_rounded + 2 * rounded
            else:
                score = four_rounded

        score += hand_config.deposit_number * 1000

        if hand_config.is_sanma:
            score += hand_config.honba_number * 200
        else:
            score += hand_config.honba_number * 300

        return {'score': score, 'yaku_level': yaku_level}

    @staticmethod
    def calculate_yakuman_score(yakuman_list, hand_config):
        if len(yakuman_list) == 1:
            yaku_level = Score.YAKUMAN
        elif len(yakuman_list) == 2:
            yaku_level = Score.DOUBLE_YAKUMAN
        elif len(yakuman_list) == 3:
            yaku_level = Score.TRIPLE_YAKUMAN
        else:
            yaku_level = str(len(yakuman_list)) + 'x Yakuman'

        if hand_config.is_dealer:
            if hand_config.is_sanma and hand_config.is_tsumo:
                score = len(yakuman_list) * 32000
            else:
                score = len(yakuman_list) * 48000
        else:
            if hand_config.is_sanma and hand_config.is_tsumo:
                score = len(yakuman_list) * 24000
            else:
                score = len(yakuman_list) * 32000

        score += hand_config.deposit_number * 1000

        if hand_config.is_sanma:
            score += hand_config.honba_number * 200
        else:
            score += hand_config.honba_number * 300

        return {'score': score, 'yaku_level': yaku_level}
