import yaml

from torch import nn, optim
import pytorch_lightning as pl
import monai

import xunet

# from torch import nn, optim
# from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint
# from pytorch_lightning.loggers import TensorBoardLogger
# from monai.losses import DiceCELoss, DiceFocalLoss


# from xunet.datasets import MSSEG2DataModule, MSSEG2Inferer
# from xunet.utils.lightning import SemanticSegmentation
# from xunet.utils.losses import DeepSuprLoss
# from xunet.utils.metrics import (
#     DiceMetric,
#     HausdorffDistanceMetric,
#     SensitivityMetric,
#     SpecificityMetric,
# )
# from xunet.utils.schedulers import WarmupCosineSchedule
# from xunet.utils.helpers import SaveValResults, Ensemble


def lambda_constructor(loader, node):
    lambda_expr = "lambda " + loader.construct_scalar(node)
    return eval(lambda_expr)


def get_constructor(obj):
    """Get constructor for an object."""

    def constructor(loader, node):
        if isinstance(node, yaml.nodes.ScalarNode):
            if node.value:
                out = obj(loader.construct_scalar(node))
            else:
                out = obj
        elif isinstance(node, yaml.nodes.SequenceNode):
            out = obj(*loader.construct_sequence(node, deep=True))
        elif isinstance(node, yaml.nodes.MappingNode):
            out = obj(**loader.construct_mapping(node, deep=True))

        return out

    return constructor


def add_attributes(obj, prefix=""):
    for attr_name in dir(obj):
        if not attr_name.startswith("_"):
            Loader.add_constructor(
                f"!{prefix}{attr_name}",
                get_constructor(getattr(obj, attr_name)),
            )


Loader = yaml.SafeLoader


# general
Loader.add_constructor("!eval", get_constructor(eval))
Loader.add_constructor("!lambda", lambda_constructor)


# pytorch
add_attributes(nn, "nn.")
add_attributes(optim, "optim.")


# pytorch lightning
add_attributes(pl.callbacks, "pl.")
add_attributes(pl.loggers, "pl.")


# monai
add_attributes(monai.losses, "monai.")
add_attributes(monai.networks.nets, "monai.")


# xunet
add_attributes(xunet, "xunet.")
Loader.add_constructor(
    "!xunet.load_checkpoint",
    get_constructor(xunet.SemanticSegmentation.load_from_checkpoint),
)


def read_config(path):
    with open(path, "rb") as file:
        config = yaml.load(file, Loader)

    return config
