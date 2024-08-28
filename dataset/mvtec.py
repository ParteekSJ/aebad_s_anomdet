import syssys.path.append("../")import osimport PIL.Image as PIL_Imageimport torchfrom torchvision import transformsfrom fvcore.common.config import CfgNodefrom torchvision.datasets.folder import default_loaderfrom torchvision.transforms.functional import InterpolationModefrom config.default import get_cfg_CLASSNAMES = [    "bottle",    "cable",    "capsule",    "carpet",    "grid",    "hazelnut",    "leather",    "metal_nut",    "pill",    "screw",    "tile",    "toothbrush",    "transistor",    "wood",    "zipper",]class MVTecDataset(torch.utils.data.Dataset):    """    PyTorch Dataset for MVTec.    """    def __init__(        self,        source: str,        classname: str,        resize: int = 256,        imagesize: int = 224,        split: str = "train",        cfg: CfgNode = None,        **kwargs    ):        super().__init__()        self.source = source        self.split = split        self.classnames_to_use = [classname] if classname is not None else _CLASSNAMES        self.cfg = cfg        self.imgpaths_per_class, self.data_to_iterate = self.get_image_data()        # for test        self.transform_img = [            transforms.Resize((resize, resize)),            transforms.CenterCrop(imagesize),            transforms.ToTensor(),        ]        self.transform_img.append(            transforms.Normalize(                mean=cfg.DATASET.IMAGENET_MEAN,                std=cfg.DATASET.IMAGENET_STD,            )        )        self.transform_img = transforms.Compose(self.transform_img)        # for train        self.transform_img_MMR = transforms.Compose(            [                transforms.RandomResizedCrop(                    imagesize,                    scale=(cfg.DATASET.DA_low_limit, cfg.DATASET.DA_up_limit),                    interpolation=InterpolationMode.BICUBIC,                ),                transforms.RandomHorizontalFlip(),                transforms.ToTensor(),                transforms.Normalize(                    mean=cfg.DATASET.IMAGENET_MEAN,                    std=cfg.DATASET.IMAGENET_STD,                ),            ]        )        transform_mask = [            transforms.Resize((resize, resize)),            transforms.CenterCrop(imagesize),            transforms.ToTensor(),        ]        self.transform_mask = transforms.Compose(transform_mask)        self.imagesize = (3, imagesize, imagesize)    def __getitem__(self, idx):        classname, anomaly, image_path, mask_path = self.data_to_iterate[idx]        image = default_loader(image_path)        if self.split == "train":            image = self.transform_img_MMR(image)        else:            image = self.transform_img(image)        if self.split == "test" and mask_path is not None:            mask = PIL_Image.open(mask_path)            mask = self.transform_mask(mask)            # avoid erasing the abnormal mask via center crop            if torch.max(mask) == 0:                mask = torch.zeros([1, *image.size()[1:]])                anomaly = "good"            else:                mask = mask / torch.max(mask)        else:            mask = torch.zeros([1, *image.size()[1:]])        # image name need to be replaced        return {            "image": image,            "mask": mask,            "classname": classname,            "anomaly": anomaly,            "is_anomaly": int(anomaly != "good"),            "image_name": "/".join(image_path.split("/")[-4:]),            "image_path": image_path,        }    def __len__(self):        return len(self.data_to_iterate)        # return 600    def get_image_data(self):        imgpaths_per_class = {}        maskpaths_per_class = {}        for classname in self.classnames_to_use:            classpath = os.path.join(self.source, classname, self.split.value)            maskpath = os.path.join(self.source, classname, "ground_truth")            anomaly_types = [                i for i in os.listdir(classpath) if os.path.isdir(os.path.join(classpath, i))            ]            imgpaths_per_class[classname] = {}            maskpaths_per_class[classname] = {}            for anomaly in anomaly_types:                anomaly_path = os.path.join(classpath, anomaly)                if os.path.isdir(anomaly_path):                    anomaly_files = sorted(os.listdir(anomaly_path))                    imgpaths_per_class[classname][anomaly] = [                        os.path.join(anomaly_path, x) for x in anomaly_files                    ]                    if self.split == "test" and anomaly != "good":                        anomaly_mask_path = os.path.join(maskpath, anomaly)                        # use the filename in anomaly file                        maskpaths_per_class[classname][anomaly] = [                            os.path.join(anomaly_mask_path, x.split(".")[0] + "_mask.png")                            for x in anomaly_files                        ]                    else:                        maskpaths_per_class[classname]["good"] = None        # Unrolls the data dictionary to an easy-to-iterate list.        data_to_iterate = []        for classname in sorted(imgpaths_per_class.keys()):            for anomaly in sorted(imgpaths_per_class[classname].keys()):                for i, image_path in enumerate(imgpaths_per_class[classname][anomaly]):                    data_tuple = [classname, anomaly, image_path]                    if self.split == "test" and anomaly != "good":                        data_tuple.append(maskpaths_per_class[classname][anomaly][i])                    else:                        data_tuple.append(None)                    data_to_iterate.append(data_tuple)        return imgpaths_per_class, data_to_iterateif __name__ == "__main__":    cfg = get_cfg()    m = MVTecDataset(        source="/Users/parteeksj/Desktop/DATASETS/MVTec", classname="capsule", cfg=cfg    )    print("dataset loaded.")