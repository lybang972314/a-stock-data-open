"""
示例 4: 信号层 - 热点 + 板块 + 资金流
=======================================
展示同花顺热点、概念板块归属、个股资金流的组合用法。
"""

import sys
sys.path.insert(0, "..")

from a_stock_data.signals import (
    ths_hot_reason,
    eastmoney_concept_blocks,
    eastmoney_fund_flow_minute,
    industry_comparison,
)
from collections import Counter


def main():
    # ===== 当日强势股 + 题材归因 =====
    print("=" * 60)
    print("【当日强势股 Top 10】")
    print("=" * 60)
    try:
        df_hot = ths_hot_reason()
        if not df_hot.empty:
            print(f"  共 {len(df_hot)} 只强势股")
            print(df_hot[["代码", "名称", "涨幅%", "题材归因"]].head(10).to_string(index=False))

            # 词频统计题材关键词
            all_tags = []
            for reason in df_hot["题材归因"].dropna():
                tags = [t.strip() for t in str(reason).split("+") if t.strip()]
                all_tags.extend(tags)
            cnt = Counter(all_tags)
            print(f"\n  当日 TOP 10 题材热度:")
            for tag, n in cnt.most_common(10):
                print(f"    {tag}: {n} 只")
    except Exception as e:
        print(f"  热点数据获取失败: {e}")

    # ===== 概念板块归属 =====
    print("\n" + "=" * 60)
    print("【概念板块归属 - 贵州茅台 600519】")
    print("=" * 60)
    try:
        blocks = eastmoney_concept_blocks("600519")
        print(f"  共 {blocks['total']} 个板块")
        for b in blocks["boards"][:10]:
            print(f"    {b['name']} (BK:{b['code']}) 涨跌={b['change_pct']}% 龙头={b['lead_stock']}")
    except Exception as e:
        print(f"  板块数据获取失败: {e}")

    # ===== 个股资金流 =====
    print("\n" + "=" * 60)
    print("【个股资金流 - 贵州茅台 600519】")
    print("=" * 60)
    try:
        flow = eastmoney_fund_flow_minute("600519")
        if flow:
            print(f"  共 {len(flow)} 个分钟数据点")
            last = flow[-1]
            signal = "bullish" if last["main_net"] > 0 else "bearish"
            print(f"  最新主力净流入: {last['main_net']/1e4:.0f}万元 → {signal}")
            total = sum(f["main_net"] for f in flow)
            print(f"  全天主力累计: {total/1e4:.0f}万元")
    except Exception as e:
        print(f"  资金流数据获取失败: {e}")

    # ===== 行业板块排名 =====
    print("\n" + "=" * 60)
    print("【行业板块排名】")
    print("=" * 60)
    try:
        comp = industry_comparison(10)
        print(f"  共 {comp['total']} 个行业")
        print("  TOP 5 涨幅:")
        for r in comp["top"][:5]:
            print(f"    {r['rank']}. {r['name']}: {r['change_pct']}% "
                  f"涨{r['up_count']}跌{r['down_count']} 领涨{r['leader']}")
    except Exception as e:
        print(f"  行业数据获取失败: {e}")


if __name__ == "__main__":
    main()
