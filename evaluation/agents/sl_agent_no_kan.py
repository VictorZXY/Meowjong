from evaluation.agents.sl_agent import SLAgent


class NoKanSLAgent(SLAgent):
    def eval_kan(self, target_tile, player1, player2, player3,
                 scores, round_number, honba_number, deposit_number,
                 dora_indicators):
        return 0.0
