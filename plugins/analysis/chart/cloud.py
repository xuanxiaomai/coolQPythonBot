from typing import Dict, List

import jieba
from wordcloud import WordCloud

from utils.objects import convertImageFormat
from utils.tmpFile import tmpFile

FONT_PATH = "./data/font.otf"
CACHE_LENGTH = 1000

FreqDict = Dict[str, int]
JIEBA_INIT = False


class WordcloudMaker:
    def __init__(self):
        global JIEBA_INIT
        if not JIEBA_INIT:
            jieba.initialize()
            JIEBA_INIT = True

        self._wordcloud = WordCloud(
            font_path=FONT_PATH, width=1920, height=1080, background_color="white"
        )
        self._wordFreqency: FreqDict = {}
        self._messageStorage = ""

    def updateFreqency(self, data: FreqDict) -> FreqDict:
        for k, v in data.items():
            if k in self._wordFreqency:
                self._wordFreqency[k] += v
            else:
                self._wordFreqency[k] = v
        return self._wordFreqency.copy()

    def update(self, text: str, force: bool = False) -> FreqDict:
        if (len(self._messageStorage) <= CACHE_LENGTH) and not force:
            self._messageStorage += f"\n{text}"
            return self._wordFreqency.copy()
        else:
            text = self._messageStorage + f"\n{text}"
            self._messageStorage = ""
        cutText: List[str] = [i for i in jieba.cut(text) if not i.isascii()]
        freqDict = self._wordcloud.process_text(" ".join(cutText))
        return self.updateFreqency(freqDict)

    def save(self) -> bytes:
        if self._messageStorage:
            self.update(self._messageStorage, force=True)
        wordcloud = self._wordcloud.generate_from_frequencies(self._wordFreqency)
        with tmpFile(ext=".png") as tmpFileName:
            wordcloud.to_file(tmpFileName)
            with open(tmpFileName, "rb") as f:
                fileRead = f.read()
        return convertImageFormat(fileRead)
