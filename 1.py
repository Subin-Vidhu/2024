# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 08:11:35 2025

Modified for multi-GPU training using MirroredStrategy
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import segmentation_models as sm
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger, ReduceLROnPlateau
from tensorflow.keras.utils import Sequence
import datetime
import json
import logging
from typing import Tuple, List, Dict, Any
import random
from pathlib import Path
import gc

# Configure logging directory
results_dir = Path("D:/PROTOS/AIRA/Results_FDA/")
results_dir.mkdir(parents=True, exist_ok=True)
log_file_path = results_dir / 'training.log'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MedicalImageTrainer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.history = None
        self._configure_gpu()
        sm.set_framework('tf.keras')

    def _configure_gpu(self):
        try:
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logger.info(f"{len(gpus)} GPUs available: {[gpu.name for gpu in gpus]}")
            else:
                logger.info("No GPUs found, using CPU")
        except RuntimeError as e:
            logger.error(f"Error configuring GPU: {e}")

    def _clear_memory(self):
        tf.keras.backend.clear_session()
        gc.collect()

    def build_model(self, input_shape: Tuple[int, ...]) -> tf.keras.Model:
        try:
            self._clear_memory()
            strategy = tf.distribute.MirroredStrategy()
            with strategy.scope():
                backbone_name = self.config['backbone']
                n_classes = self.config['n_classes']
                activation = self.config.get('activation', 'softmax')

                model = sm.Unet(
                    backbone_name,
                    encoder_weights=self.config.get('encoder_weights', 'imagenet'),
                    input_shape=input_shape,
                    classes=n_classes,
                    activation=activation
                )

                optimizer = tf.keras.optimizers.Adam(learning_rate=self.config['learning_rate'])

                class_weights = np.array(self.config.get('class_weights', [1.0] * n_classes))
                dice_loss = sm.losses.DiceLoss(class_weights=class_weights)
                focal_loss = sm.losses.CategoricalFocalLoss()
                total_loss = dice_loss + self.config.get('focal_loss_weight', 1.0) * focal_loss

                metrics = [
                    'accuracy',
                    sm.metrics.IOUScore(threshold=0.5),
                    sm.metrics.FScore(threshold=0.5)
                ]

                model.compile(optimizer=optimizer, loss=total_loss, metrics=metrics)
                logger.info(f"Model built successfully with {model.count_params():,} parameters")
            return model
        except Exception as e:
            logger.error(f"Error building model: {e}")
            raise

    # Additional methods like load_batch_data, prepare_data, train_model, etc.
    # would be defined below, unchanged except for using this build_model and
    # ensuring logging continues to go to both console and file.

# Configuration

def get_default_config():
    return {
        'batch_directory': 'D:/PROTOS/AIRA/Numpy_Arrays/ALL/FDA/',
        'results_dir': str(results_dir),
        'num_batches': 7,
        'image_filename_template': 'windowing_improved_06122025_image_batch_{batch_idx}.npy',
        'mask_filename_template': 'windowing_improved_06122025_mask_batch_{batch_idx}.npy',
        'test_size': 0.1,
        'val_size': 0.1,
        'random_state': 42,
        'backbone': 'resnet50',
        'n_classes': 4,
        'activation': 'softmax',
        'encoder_weights': None,
        'use_backbone_preprocessing': False,
        'batch_size': 12,  # Adjusted for 3 GPUs
        'epochs': 1000,
        'learning_rate': 0.0001,
        'class_weights': [0.2, 0.5, 0.35, 0.35],
        'focal_loss_weight': 1.0,
        'patience': 100,
        'lr_patience': 30,
        'lr_factor': 0.5,
        'min_lr': 1e-7,
        'save_best_only': True,
        'perform_sanity_check': True,
        'sanity_check_samples': 15
    }

# You would complete the script with the rest of your original pipeline
# (loading data, training, evaluation, etc.) and ensure all logs go through `logger`

if __name__ == "__main__":
    config = get_default_config()
    try:
        trainer = MedicalImageTrainer(config)
        # Remaining training pipeline...
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
