import pytest

from llmcompressor.args import DatasetArguments
from llmcompressor.transformers.finetune.data.data_helpers import (
    get_raw_dataset,
    make_dataset_splits,
)


@pytest.mark.unit
def test_combined_datasets():
    data_args = DatasetArguments(
        dataset="wikitext", dataset_config_name="wikitext-2-raw-v1"
    )
    raw_wikitext2 = get_raw_dataset(data_args)
    datasets = {"all": raw_wikitext2}
    split_datasets = make_dataset_splits(datasets, do_train=True)
    assert split_datasets.get("train") is not None

    split_datasets = make_dataset_splits(datasets, do_train=True)
    assert split_datasets.get("train") is not None


@pytest.mark.unit
def test_separate_datasets():
    splits = {"train": "train[:10%]", "validation": "train[10%:20%]"}
    data_args = DatasetArguments(
        dataset="wikitext", dataset_config_name="wikitext-2-raw-v1"
    )
    datasets = {}
    for split_name, split_str in splits.items():
        raw_wikitext2 = get_raw_dataset(data_args, split=split_str)
        datasets[split_name] = raw_wikitext2

    split_datasets = make_dataset_splits(datasets, do_train=True)
    assert split_datasets.get("train") is not None

    with pytest.raises(ValueError):
        # fails due to no test split specified

        datasets.pop("train")
        split_datasets = make_dataset_splits(datasets, do_train=True)
