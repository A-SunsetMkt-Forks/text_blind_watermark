# -*- coding: utf-8 -*-

import random


class TextBlindWatermark:
    def __init__(self, password):
        self.password = password
        self.text, self.wm_bin = None, None

    def read_wm(self, watermark):
        random.seed(self.password)
        wm_bin = [format(i ^ random.randint(0, 255), '08b') for i in watermark.encode('utf-8')]  # 8位2进制格式
        self.wm_bin = ''.join(wm_bin)
        return self

    def read_text(self, text):
        self.text = text
        return self

    def embed(self, repeat=False):
        wm_bin, text = self.wm_bin, self.text
        # 打入水印
        len_wm_bin, len_text = len(self.wm_bin), len(self.text)
        assert len_text > len_wm_bin, "文本长度至少{}，实际{}".format(len_wm_bin, len_text)

        # TODO:循环嵌入
        if repeat:
            pass
            # wm_bin = wm_bin * ((len_text - 2) // len_wm_bin)

        # 头尾各放一个1。提取过程中把首尾的0去掉。
        wm_bin = '1' + wm_bin + '1'
        sentence_embed = ""
        for idx in range(len_text):
            sentence_embed += text[idx]
            if idx < len(wm_bin):
                if wm_bin[idx] == "1":
                    sentence_embed += chr(127)

        return sentence_embed

    def extract(self, text_embed):
        wm_extract_bin = ""

        idx = 0
        while idx < len(text_embed):
            if text_embed[idx] != chr(127):
                idx += 1
                wm_extract_bin += '0'
            else:
                idx += 2
                wm_extract_bin += '1'

        first_zero = wm_extract_bin.find("1")
        last_zero = len(wm_extract_bin) - wm_extract_bin[::-1].find("1")
        wm_extract_bin = wm_extract_bin[first_zero + 1:last_zero - 1]

        random.seed(self.password)
        return bytes([int(wm_extract_bin[8 * i:8 * i + 8], base=2) ^ random.randint(0, 255) for i in
                      range(len(wm_extract_bin) // 8)]).decode('utf-8')
