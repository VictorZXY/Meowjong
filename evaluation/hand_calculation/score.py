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
                split_scores = [double_rounded]
                if hand_config.is_sanma:
                    total_score = 2 * double_rounded
                else:
                    total_score = 3 * double_rounded
            else:
                split_scores = [six_rounded]
                total_score = six_rounded
        else:
            if hand_config.is_tsumo:
                split_scores = [double_rounded, rounded]
                if hand_config.is_sanma:
                    total_score = double_rounded + rounded
                else:
                    total_score = double_rounded + 2 * rounded
            else:
                split_scores = [four_rounded]
                total_score = four_rounded

        total_score += hand_config.deposit_counter * 1000

        if hand_config.is_sanma:
            total_score += hand_config.honba_counter * 200
            if hand_config.is_tsumo:
                for i in range(len(split_scores)):
                    split_scores[i] += hand_config.honba_counter * 100
            else:
                assert len(split_scores) == 1
                split_scores[0] += hand_config.honba_counter * 200
        else:
            total_score += hand_config.honba_counter * 300
            if hand_config.is_tsumo:
                for i in range(len(split_scores)):
                    split_scores[i] += hand_config.honba_counter * 100
            else:
                assert len(split_scores) == 1
                split_scores[0] += hand_config.honba_counter * 300

        return {
            'split_scores': split_scores,
            'total_score': total_score,
            'yaku_level': yaku_level
        }

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
            if hand_config.is_tsumo:
                split_scores = [len(yakuman_list) * 16000]
                if hand_config.is_sanma:
                    total_score = len(yakuman_list) * 32000
                else:
                    total_score = len(yakuman_list) * 48000
            else:
                split_scores = [len(yakuman_list) * 48000]
                total_score = len(yakuman_list) * 48000
        else:
            if hand_config.is_tsumo:
                split_scores = [len(yakuman_list) * 16000,
                                len(yakuman_list) * 8000]
                if hand_config.is_sanma:
                    total_score = len(yakuman_list) * 24000
                else:
                    total_score = len(yakuman_list) * 32000
            else:
                split_scores = [len(yakuman_list) * 32000]
                total_score = len(yakuman_list) * 32000

        total_score += hand_config.deposit_counter * 1000

        if hand_config.is_sanma:
            total_score += hand_config.honba_counter * 200
            if hand_config.is_tsumo:
                for i in range(len(split_scores)):
                    split_scores[i] += hand_config.honba_counter * 100
            else:
                assert len(split_scores) == 1
                split_scores[0] += hand_config.honba_counter * 200
        else:
            total_score += hand_config.honba_counter * 300
            if hand_config.is_tsumo:
                for i in range(len(split_scores)):
                    split_scores[i] += hand_config.honba_counter * 100
            else:
                assert len(split_scores) == 1
                split_scores[0] += hand_config.honba_counter * 300

        return {
            'split_scores': split_scores,
            'total_score': total_score,
            'yaku_level': yaku_level
        }
