# Towards a Competitive 3-Player Mahjong AI using Deep Reinforcement Learning

[Paper](https://victorzxy.github.io/publication/2022-meowjong-auxiliary/Towards_a_Competitive_3-Player_Mahjong_AI_using_Deep_Reinforcement_Learning.pdf) | [Dissertation](https://victorzxy.github.io/project/meowjong/BA-Dissertation-Meowjong.pdf)

## Abstract

Mahjong is a multi-player imperfect-information game with challenging features for AI research. Sanma, being a 3-player variant of Japanese Riichi Mahjong, possesses unique characteristics and a more aggressive playing style than the 4-player game. It is thus challenging and of research interest in its own right, but has not been explored. We present Meowjong, the first ever AI for Sanma using deep reinforcement learning (RL). We define a 2-dimensional data structure for encoding the observable information in a game. We pre-train 5 convolutional neural networks (CNNs) for Sanma’s 5 actions—discard, Pon, Kan, Kita and Riichi, and enhance the major (discard) action’s model via self-play reinforcement learning. Meowjong demonstrates potential for becoming the state-of-the-art in Sanma, by achieving test accuracies comparable with AIs for 4-player Mahjong through supervised learning, and gaining a significant further enhancement from reinforcement learning.

## Prerequisites

All the required environments are in [`requirements.txt`](./requirements.txt).

## How to run

### Preparing the datasets

To download Sanma game logs from [Tenhou.net](https://tenhou.net/) and extract the raw data from the game logs, run the following command (remember to comment out the `assert False` first):

```
python data_processing/prepare_dataset.py
```

To convert the raw data into TensorFlow tensors, run:

```
python data_processing/prepare_dataset_tensors.py [--dataset_path DATASET_PATH] [--action_type ACTION_TYPE] [--year YEAR] [--scaled SCALED]
```

### SL pre-training the action models

To pre-train an action model using SL, run:

```
python training/[ACTION_MODEL].py [--dataset_path DATASET_PATH] [--logs_path LOGS_PATH] [--cnn_path CNN_PATH] [--kernel_size KERNEL_SIZE]
```

### RL fine-tuning of the discard model

To fine-tune the pre-trained discard model using RL, run:

```
python training/reinforce.py [--discard_model_path DISCARD_MODEL_PATH] [--pon_model_path PON_MODEL_PATH] [--kan_model_path KAN_MODEL_PATH] [--kita_model_path KITA_MODEL_PATH] [--riichi_model_path RIICHI_MODEL_PATH] [--reinforce_models_dir REINFORCE_MODELS_DIR]
```

### Evaluation

There are a number of evaluations in [`evaluation`](./evaluation).

## Cite this project

```bibtex
@inproceedings{Zhao2022Meowjong,
    title={Towards a Competitive 3-Player {Mahjong AI} using Deep Reinforcement Learning},
    author={Xiangyu Zhao and Sean B. Holden},
    booktitle={2022 IEEE Conference on Games (CoG)}, 
    year={2022}
}
```
