from typing import Any, Dict

import seaborn as sns
from matplotlib.font_manager import FontProperties
from pandas import DataFrame

from utils.tmpFile import tmpFile

FONT_PATH = "./data/font.otf"
sns.set(font=FontProperties(fname=FONT_PATH).get_name())


class DataFrameMaker:
    def __init__(self, index: Dict[str, object]):
        self._index = index
        self._frame = DataFrame(index=[*index.keys()])

    def update(self, data: Dict[str, Any]) -> int:
        frameData = {k: data[k] for k in self._index.keys()}
        self._frame = self._frame.append(frameData, ignore_index=True)
        return self._frame.size

    def read(self) -> DataFrame:
        for k, v in self._index.items():
            self._frame[k] = self._frame[k].astype(v)
        return self._frame


class Chart:
    @staticmethod
    def _toImage(grid: sns.FacetGrid) -> bytes:
        with tmpFile(ext=".png") as tmpFileName:
            grid.savefig(tmpFileName)
            with open(tmpFileName, "rb") as f:
                fileRead = f.read()
        return fileRead

    @classmethod
    def chatFrequency(cls, data: DataFrame):
        assert "date" in data
        assert "time" in data
        image = sns.catplot(x="date", y="time", data=data)
        return cls._toImage(image)
