"""
示例 1: 单票快速估值
====================
展示如何用 a-stock-data 对一个股票做完整的估值分析。
"""

import sys
sys.path.insert(0, "..")

from a_stock_data.market import tencent_quote
from a_stock_data.research import ths_eps_forecast
from a_stock_data.signals import eastmoney_concept_blocks, eastmoney_fund_flow_minute
from a_stock_data.valuation import full_valuation


def main():
    code = "688017"  # 绿的谐波

    # ===== 方式一：手动组合 =====
    print("=" * 60)
    print(f"【{code}】手动组合估值")
    print("=" * 60)

    # 1. 实时行情
    quotes = tencent_quote([code])
    q = quotes[code]
    print(f"  名称: {q['name']}")
    print(f"  现价: ¥{q['price']}")
    print(f"  PE(TTM): {q['pe_ttm']}  PB: {q['pb']}")
    print(f"  总市值: {q['mcap_yi']}亿")

    # 2. 机构一致预期
    df = ths_eps_forecast(code)
    if not df.empty:
        print(f"\n  机构一致预期:")
        print(df.to_string(index=False))

    # 3. 概念板块
    blocks = eastmoney_concept_blocks(code)
    print(f"\n  概念板块 ({blocks['total']}个):")
    print(f"  {', '.join(blocks['concept_tags'][:10])}")

    # 4. 资金流
    flow = eastmoney_fund_flow_minute(code)
    if flow:
        total = sum(f["main_net"] for f in flow)
        print(f"\n  当日主力累计净流入: {total/1e4:.0f}万元")

    # ===== 方式二：一键完整估值 =====
    print("\n" + "=" * 60)
    print(f"【{code}】一键完整估值")
    print("=" * 60)
    result = full_valuation(code)
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
