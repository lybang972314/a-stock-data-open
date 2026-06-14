"""
示例 2: 批量估值对比
====================
对比多只股票的关键估值指标。
"""

import sys
sys.path.insert(0, "..")

from a_stock_data.market import tencent_quote
from a_stock_data.valuation import full_valuation


def main():
    # 对比多只股票
    stocks = ["688017", "300308", "300476", "002463"]

    print("=" * 80)
    print(f"{'名称':<12} {'代码':<10} {'现价':>8} {'PE(TTM)':>10} {'PB':>8} "
          f"{'PE(前向)':>10} {'PEG':>8} {'消化年':>8} {'分析师数':>8}")
    print("-" * 80)

    for code in stocks:
        try:
            r = full_valuation(code)
            print(f"{r['name']:<12} {code:<10} ¥{r['price']:>7.2f} "
                  f"{r['pe_ttm']:>9.1f}x {r['pb']:>7.2f} "
                  f"{str(r['pe_fwd']):>10} {str(r['peg']):>8} "
                  f"{str(r['digest_years']):>8} {r['analyst_count']:>8}")
        except Exception as e:
            print(f"{code:<10} 失败 - {e}")


if __name__ == "__main__":
    main()
