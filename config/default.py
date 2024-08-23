from fvcore.common.config import CfgNode_C = CfgNode()_C.NUM_GPUS = 1_C.RNG_SEED = 54# Model Configuration_C.MODEL = CfgNode()_C.MODEL.image_size = 224_C.MODEL.patch_size = 16_C.MODEL.in_channels = 3_C.MODEL.embed_dim = 768_C.MODEL.depth = 12_C.MODEL.num_heads = 12  # 16_C.MODEL.mlp_ratio = 4.0_C.MODEL.scale_factors = (4.0, 2.0, 1.0)_C.MODEL.fpn_output_dim = (256, 512, 1024)_C.MODEL.return_nodes = ["layer1", "layer2", "layer3"]_C.MODEL.mae_pt_ckpt = "/Users/parteeksj/Desktop/MMR_Implementation/mae_visualize_vit_base.pth"_C.MODEL.save_ckpt = "./checkpoints/"_C.MODEL.display_step = 20_C.MODEL.device = "cuda"_C.DATASET = CfgNode()_C.DATASET.aebad_s_dir = "/Users/parteeksj/Desktop/DATASETS/AeBAD/AeBAD_S"# _C.DATASET.aebad_s_dir = "/content/drive/MyDrive/AeBAD/AeBAD_S"_C.DATASET.IMAGENET_MEAN = [0.485, 0.456, 0.406]_C.DATASET.IMAGENET_STD = [0.229, 0.224, 0.225]_C.DATASET.INV_IMAGENET_MEAN = [-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.255]_C.DATASET.INV_IMAGENET_STD = [1 / 0.229, 1 / 0.224, 1 / 0.255]_C.DATASET.DA_low_limit = 0.2_C.DATASET.DA_up_limit = 1.0_C.DATASET.domain_shift_category = "same"_C.TRAIN_SETUPS = CfgNode()_C.TRAIN_SETUPS.batch_size = 64_C.TRAIN_SETUPS.num_workers = 8_C.TRAIN_SETUPS.learning_rate = 0.005_C.TRAIN_SETUPS.epochs = 200_C.TRAIN_SETUPS.weight_decay = 0.05_C.TRAIN_SETUPS.warmup_epochs = 40def get_cfg():    """    Get a copy of the default config.    """    return _C.clone()