"""
a-stock-data 公告层
===================
巨潮公告全文检索
"""

import requests
from datetime import datetime


# 巨潮 股票→orgId 映射（模块级缓存，首次调用时拉取一次，全程复用）
_CNINFO_ORGID_MAP = {}


def _cninfo_ts_to_date(ts):
    """巨潮 announcementTime 返回 Unix 毫秒整数，需转换为日期字符串。"""
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
    return str(ts)[:10] if ts else ""


def _cninfo_orgid(code: str) -> str:
    """查股票真实 orgId。优先动态查官方映射表，查不到再回退硬编码。"""
    global _CNINFO_ORGID_MAP
    if not _CNINFO_ORGID_MAP:
        try:
            r = requests.get("http://www.cninfo.com.cn/new/data/szse_stock.json",
                             headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            _CNINFO_ORGID_MAP = {s["code"]: s["orgId"]
                                 for s in r.json().get("stockList", [])}
        except Exception as e:
            print(f"[WARN] 巨潮 orgId 映射表拉取失败，回退硬编码规则: {e}")
    org = _CNINFO_ORGID_MAP.get(code)
    if org:
        return org
    # fallback：老格式（仅部分老股票如 600519/600036 适用）
    if code.startswith("6"):
        return f"gssh0{code}"
    elif code.startswith("8") or code.startswith("4"):
        return f"gsbj0{code}"
    return f"gssz0{code}"


def cninfo_announcements(code: str, page_size: int = 30) -> list[dict]:
    """
    巨潮公告全文检索。
    返回: [{title, type, date, url}]
    """
    from .helpers import normalize_code
    code = normalize_code(code)
    url = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
    org_id = _cninfo_orgid(code)

    payload = {
        "stock": f"{code},{org_id}",
        "tabName": "fulltext",
        "pageSize": str(page_size),
        "pageNum": "1",
        "column": "",
        "category": "",
        "plate": "",
        "seDate": "",
        "searchkey": "",
        "secid": "",
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true",
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.cninfo.com.cn/new/disclosure",
        "Origin": "https://www.cninfo.com.cn",
    }
    r = requests.post(url, data=payload, headers=headers, timeout=15)
    d = r.json()

    rows = []
    for item in d.get("announcements", []) or []:
        rows.append({
            "title": item.get("announcementTitle", ""),
            "type": item.get("announcementTypeName", ""),
            "date": _cninfo_ts_to_date(item.get("announcementTime")),
            "url": f"https://www.cninfo.com.cn/new/disclosure/detail?annoId={item.get('announcementId', '')}",
        })
    return rows
