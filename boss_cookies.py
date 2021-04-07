import random
from urllib import parse

import execjs
import requests


class BossCookieSpider:

    def __init__(self):
        self.core = """
                var window = {
    navigator: {
        userAgent: ""
    },
    moveTo: function () {
    },
    moveBy: function () {
    },
    screen: {
        availHeight: 1040,
        availWidth: 1920
    },
    open: function () {
        [nativecode]

    }
};
var document = {
    getElementById: function () {
        glcanvaxs = {}
    },
    createElement: function () {
        caption = {
            tagName: "CAPTION",
        };
        return caption
    },
    title: ""
};
var top = {
    location: {
        href: "https://www.zhipin.com/web/common/security-check.html"
    },
};
var nativecode = "";

function setInterval() {
    [nativecode]
};
var sessionStorage = {};
delete global;
delete Buffer;
function encryption(seed, ts) {
    var code = new ABC().z(seed, parseInt(ts) + (480 + new Date().getTimezoneOffset()) * 60 * 1000);
    return encodeURIComponent(code)
}
        """

    def main(self):
        headers = {
            "user-agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/{random.randint(1, 999)}.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }
        url = f"https://www.zhipin.com/job_detail/"
        response = requests.get(url, headers=headers)
        self.cookies_generate(response)

    def cookies_generate(self, response):
        query_str = parse.urlparse(response.url).query
        query_dict = {i.split("=")[0]: i.split("=")[1] for i in query_str.split("&")}
        js_name = query_dict.get("name")
        js_url = f"https://www.zhipin.com/web/common/security-js/{js_name}.js"
        js_res = requests.get(js_url)
        js_text = js_res.text
        seed = parse.unquote(query_dict.get("seed"))
        ts = query_dict.get("ts")
        new_js_text = self.core + js_text
        new_js = execjs.compile(new_js_text)
        code = new_js.call("encryption", seed, ts)
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "cookie": f"__zp_stoken__={code};"
        }
        url = "https://www.zhipin.com/c100010000-p110101/?page=2&ka=page-2"
        response = requests.get(url, headers=headers)
        print(response.text)
        pass


if __name__ == '__main__':
    boss_zhipin_cookie = BossCookieSpider()
    boss_zhipin_cookie.main()
