


# MAPS: Motivation-Aware Personalized Search via LLM-Driven Consultation Alignment


This is the official implementation of the paper "MAPS: Motivation-Aware Personalized Search via LLM-Driven Consultation Alignment" based on PyTorch. Please note that the code of this project is still being organized, and the methods are continuously being improved.


## Overview

The main implementation of MAPS can be found in the file `models/cs/TEM_0206_Final.py`.

## Experimental Setting
The settings of can be found in file `utils/const.py`.


## Quick Start

### 1. Download data
Download and unzip the processed data [Amazon](https://drive.google.com/drive/folders/1Gt0Gd-sG91w6734EmVE6na4KoPN5YlCP?usp=drive_link). Place data files in the folder `data`.

### 2. Satisfy the requirements
The requirements can be found in file `requirements.txt`.

### 3. Train and evaluate our model:
Refer to the example in `GO.sh` and customize your hyperparameters and command.

### 4. Check training and evaluation process:
After training, check `./output` for logs and results. For the sake of convenience, you can utilize `results_to_excel.ipynb` to present the performances of all experiments in the form of an excel table.


## Reference

If you find it useful, please consider citing our paper and giving a star :)

```bibtex
@misc{qin2025mapsmotivationawarepersonalizedsearch,
      title={MAPS: Motivation-Aware Personalized Search via LLM-Driven Consultation Alignment}, 
      author={Weicong Qin and Yi Xu and Weijie Yu and Chenglei Shen and Ming He and Jianping Fan and Xiao Zhang and Jun Xu},
      year={2025},
      eprint={2503.01711},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2503.01711}, 
}
```


## License

This project is licensed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) License.

The open-source dataset used in this project is derived from the Amazon data processed by [PersonalWAB](https://github.com/HongruCai/PersonalWAB). We make modifications to it to meet the requirements of this project. Thus, we also we continue to honor and adhere to its licensing terms ([CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)). Finally, we would like to express our sincere gratitude for open-source contributions of [PersonalWAB](https://github.com/HongruCai/PersonalWAB).

```bibtex
@misc{cai2024personalwab,
      title={Large Language Models Empowered Personalized Web Agents}, 
      author={Hongru Cai and Yongqi Li and Wenjie Wang and Fengbin Zhu and Xiaoyu Shen and Wenjie Li and Tat-Seng Chua},
      year={2024},
      eprint={2410.17236},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2410.17236}, 
}
```



