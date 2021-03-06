import mmcv
from torch import nn

from .registry import (BACKBONES, GLOBALPOOLING, ROIPOOLING, CONCATS,
                       EMBEDEXTRACTOR, ATTRPREDICTOR, PREDICTOR, RETRIEVER,
                       LANDMARKFEATUREEXTRACTOR, VISIBILITYCLASSIFIER,
                       LANDMARKREGRESSION, LANDMARKDETECTOR, LOSSES)


def _build_module(cfg, registry, default_args):
    assert isinstance(cfg, dict) and 'type' in cfg
    assert isinstance(default_args, dict) or default_args is None
    args = cfg.copy()
    obj_type = args.pop('type')
    if mmcv.is_str(obj_type):
        if obj_type not in registry.module_dict:
            raise KeyError('{} is not in the {} registry'.format(
                obj_type, registry.name))
        obj_type = registry.module_dict[obj_type]
    elif not isinstance(obj_type, type):
        raise TypeError('type must be a str or valid type, but got {}'.format(
            type(obj_type)))
    if default_args is not None:
        for name, value in default_args.items():
            args.setdefault(name, value)
    return obj_type(**args)


def build(cfg, registry, default_args=None):
    if isinstance(cfg, list):
        modules = [_build_module(cfg_, registry, default_args) for cfg_ in cfg]
        return nn.Sequential(*module)
    else:
        return _build_module(cfg, registry, default_args)


def build_backbone(cfg):
    return build(cfg, BACKBONES)


def build_global_pool(cfg):
    return build(cfg, GLOBALPOOLING)


def build_roi_pool(cfg):
    return build(cfg, ROIPOOLING)


def build_concat(cfg):
    return build(cfg, CONCATS)


def build_attr_predictor(cfg):
    return build(cfg, ATTRPREDICTOR)


def build_embed_extractor(cfg):
    return build(cfg, EMBEDEXTRACTOR)


def build_landmark_feature_extractor(cfg):
    return build(cfg, LANDMARKFEATUREEXTRACTOR)


def build_visibility_classifier(cfg):
    return build(cfg, VISIBILITYCLASSIFIER)


def build_landmark_regression(cfg):
    return build(cfg, LANDMARKREGRESSION)


def build_landmark_detector(cfg):
    return build(cfg, LANDMARKDETECTOR)


def build_loss(cfg):
    return build(cfg, LOSSES)


def build_predictor(cfg):
    return build(cfg, PREDICTOR)


def build_retriever(cfg):
    return build(cfg, RETRIEVER)
