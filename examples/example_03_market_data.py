"""
示例 3: 实时行情 + K线
=======================
展示如何拉取实时行情、腾讯估值数据和百度K线。
"""

import sys
sys.path.insert(0, "..")

from a_stock_data.market import tencent_quote, baidu_kline_with_ma


def main():
    # ===== 实时行情 =====
    print("=" * 60)
    print("【实时行情】")
    print("=" * 60)

    # 个股
    quotes = tencent_quote(["688017", "300476", "002463"])
    for code, q in quotes.items():
        print(f"  {q['name']}({code}): ¥{q['price']} "
              f"PE={q['pe_ttm']} PB={q['pb']} "
              f"市值={q['mcap_yi']}亿 换手={q['turnover_pct']}%")

    # 指数
    print("\n【指数行情】")
    index_quotes = tencent_quote(["000001", "000300", "399006"])
    for code, q in index_quotes.items():
        print(f"  {q['name']}({code}): ¥{q['price']} 涨跌={q['change_pct']}%")

    # ETF
    print("\n【ETF行情】")
    etf_quotes = tencent_quote(["510050", "510300"])
    for code, q in etf_quotes.items():
        print(f"  {q['name']}({code}): ¥{q['price']} PE={q['pe_ttm']}")

    # ===== 百度K线（带MA均线） =====
    print("\n" + "=" * 60)
    print("【百度K线 - 绿的谐波 688017】")
    print("=" * 60)
    data = baidu_kline_with_ma("600519")  # 贵州茅台
    print(f"  K线字段: {data['keys'][:10]}")
    print(f"  最近5根K线:")
    for row in data["rows"][-5:]:
        print(f"    {row}")


if __name__ == "__main__":
    main()
