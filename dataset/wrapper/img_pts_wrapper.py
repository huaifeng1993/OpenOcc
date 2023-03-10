import numpy as np

from .base_wrapper import BaseWrapper
from . import OPENOCC_WRAPPER
from ..transform import TransformCompose
from ..modal import PointCloud

@OPENOCC_WRAPPER.register_module()
class ImagePointWrapper(BaseWrapper):
    def __init__(self, loader, 
                 img_transforms=None,
                 pointcloudModal=None):
        super().__init__(loader)

        self.img_transforms = None
        self.pointcloudModal = None

        if img_transforms is not None:
            self.img_transforms = TransformCompose(img_transforms)
        if pointcloudModal is not None:
            self.pointcloudModal = PointCloud(**pointcloudModal)

    def __getitem__(self, index):
        data = self.loader[index]
        imgs, metas, xyz, labels = data

        # deal with img augmentations
        if self.img_transforms is not None:
            metas.update({'img': imgs})
            metas = self.img_transforms(metas)
            imgs = metas.pop('img')
        
        grid_ind_float, _, processed_label = self.pointcloudModal.to_voxel(xyz, labels)

        processed_label = processed_label.astype(np.int)
        labels = labels.astype(np.int)

        # data_tuple = (imgs, metas, processed_label, grid_ind_float, labels)

        data_dict = {
            'imgs': imgs,
            'metas': metas,
            'processed_label': processed_label,
            'grid_ind_float': grid_ind_float,
            'labels': labels
        }

        return data_dict
