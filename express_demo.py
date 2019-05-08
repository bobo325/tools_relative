#!/usr/bin/env python
# encoding:utf-8

"""
@Author: BOBO
@Time: 2018/10/11 15:38
"""

import requests
import json


class Express100(object):
    # 先通过company_url 获取公司的comCode，然后再通过trace_url查出company中符合express_code 的快递物流信息。
    company_url = "http://www.kuaidi100.com/autonumber/autoComNum"
    trace_url = "http://www.kuaidi100.com/query"

    @classmethod
    def get_json_data(cls, url, payload):
        r = requests.get(url=url, params=payload)
        return r.json()

    @classmethod
    def get_company_info(cls, express_code):
        """
        {
            comCode: "",
            num: "3351419285305",
            auto: [
                {
                    comCode: "shentong",
                    id: "",
                    noCount: 13852,
                    noPre: "33514",
                    startTime: ""
                }
            ]
        }
        """
        payload = {'text': express_code}
        data = cls.get_json_data(cls.company_url, payload)
        return data

    @classmethod
    def get_express_info(cls, express_code):
        """
        {
            message: "ok",
            nu: "3351419285305",
            ischeck: "0",
            condition: "00",
            com: "shentong",
            status: "200",
            state: "0",
            data: [
                {
                    time: "2018-01-21 22:19:45",
                    ftime: "2018-01-21 22:19:45",
                    context: "淄博市 山东淄博公司-已发往-辽宁盘锦中转部",
                    location: ""
                },
                ......
            ]
        }
        """

        company_info = cls.get_company_info(express_code)
        company_code = ""
        if company_info.get("auto"):
            company_code = company_info.get("auto")[0].get("comCode", "")  # 这里直接取了所有符合express_code 的第一个
        payload = {'type': company_code, 'postid': express_code, 'id': 1}
        data = cls.get_json_data(cls.trace_url, payload)
        data.update(company_info)
        return data


if __name__ == "__main__":
    while True:
        express_code = input("请输入快递单号:")
        res = Express100.get_express_info(str(express_code).strip())
        print(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4))

# 可以直接选择输入comCode，从而省去第一次亲求
# 并通过comCode和express_code直接查找出物流信息

