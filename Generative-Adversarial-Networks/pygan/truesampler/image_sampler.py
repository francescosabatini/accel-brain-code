# -*- coding: utf-8 -*-
import numpy as np
from pygan.true_sampler import TrueSampler
from pydbm.cnn.featuregenerator.image_generator import ImageGenerator


class ImageSampler(TrueSampler):
    '''
    Sampler which draws samples from the `true` distribution of images.
    '''

    def __init__(
        self,
        batch_size,
        image_dir,
        seq_len=None,
        gray_scale_flag=True,
        wh_size_tuple=(100, 100),
        norm_mode="z_score"
    ):
        '''
        Init.

        Args:
            training_image_dir:             Dir path which stores image files for training.
            test_image_dir:                 Dir path which stores image files for test.
            seq_len:                        The length of one sequence.
            gray_scale_flag:                Gray scale or not(RGB).
            wh_size_tuple:                  Tuple(`width`, `height`).
            norm_mode:                      How to normalize pixel values of images.
                                            - `z_score`: Z-Score normalization.
                                            - `min_max`: Min-max normalization.
                                            - `tanh`: Normalization by tanh function.

        '''
        self.__feature_generator = ImageGenerator(
            epochs=1,
            batch_size=batch_size,
            training_image_dir=image_dir,
            test_image_dir=image_dir,
            seq_len=seq_len,
            gray_scale_flag=gray_scale_flag,
            wh_size_tuple=wh_size_tuple,
            norm_mode=norm_mode
        )

    def draw(self):
        '''
        Draws samples from the `true` distribution.
        
        Returns:
            `np.ndarray` of samples.
        '''
        return self.__feature_generator.generate()[0]
