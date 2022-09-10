import os
from argparse import ArgumentParser, Namespace

import torch
from pytorch_lightning import Trainer, seed_everything

from registry import read_config


seed_everything(42, workers=True)
torch.set_default_dtype(torch.float32)
print("cuda" if torch.cuda.is_available() else "cpu")

cwd = os.path.dirname(__file__)


def main(args):
    # get config
    config = read_config(args.config)

    # setup data
    dm = config["data"]
    dm.data_properties = {
        "test": [
            {
                "id": os.path.basename(args.output_file).split(".")[0],
                "image": [args.flair01, args.flair02],
            }
        ]
    }
    dm.setup("test")

    # load model
    task_cls, task_params = config["task"]
    if (
        "checkpoint" in config["test"]
        and "checkpoint_path" in config["test"]["checkpoint"]
    ):
        model = task_cls.load_from_checkpoint(
            **config["test"]["checkpoint"], strict=False, **task_params
        )
    else:
        model = task_cls(**task_params)

    model.inferer = config["test"]["inferer"]
    model.inferer.write_dir = os.path.dirname(args.output_file)

    # test
    del config["training"]["gpus"], config["training"]["accelerator"]
    trainer = Trainer(**config["training"])
    trainer.test(model=model, dataloaders=dm.test_dataloader())


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="""Do inference on test data.""", add_help=False
    )
    parser.add_argument("--config", "-c")
    parser.add_argument("--flair01", "-t1", required=True)
    parser.add_argument("--flair02", "-t2", required=True)
    parser.add_argument("--output_file", "-o", required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()  # for running from terminal
    main(args)
