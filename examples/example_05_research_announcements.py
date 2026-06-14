"""
示例 5: 财报三表 + 公告 + 研报
===============================
展示如何获取新浪财报三表、巨潮公告和东财研报。
"""

import sys
sys.path.insert(0, "..")

from a_stock_data.fundamentals import sina_financial_report, eastmoney_stock_info
from a_stock_data.announcements import cninfo_announcements
from a_stock_data.research import eastmoney_reports


def main():
    code = "600519"  # 贵州茅台

    # ===== 个股基本面 =====
    print("=" * 60)
    print("【贵州茅台 600519 基本面】")
    print("=" * 60)
    info = eastmoney_stock_info(code)
    for k, v in info.items():
        print(f"  {k}: {v}")

    # ===== 利润表 =====
    print("\n" + "=" * 60)
    print("【利润表 - 最近3期】")
    print("=" * 60)
    try:
        lrb = sina_financial_report(code, "lrb", num=3)
        for item in lrb:
            print(f"  报告期: {item.get('报告期', '')}")
            # 打印关键科目
            for key in ["净利润", "营业收入", "营业利润"]:
                if key in item:
                    print(f"    {key}: {item[key]}")
    except Exception as e:
        print(f"  财报数据获取失败: {e}")

    # ===== 公告 =====
    print("\n" + "=" * 60)
    print("【最近公告】")
    print("=" * 60)
    try:
        anns = cninfo_announcements(code, page_size=5)
        if anns:
            for a in anns:
                print(f"  {a['date']} | {a['type']} | {a['title'][:60]}")
        else:
            print("  暂无公告")
    except Exception as e:
        print(f"  公告获取失败: {e}")

    # ===== 研报 =====
    print("\n" + "=" * 60)
    print("【研报列表 - 最近5篇】")
    print("=" * 60)
    try:
        reports = eastmoney_reports(code, max_pages=2)
        print(f"  共 {len(reports)} 篇研报")
        for r in reports[:5]:
            print(f"  {r.get('publishDate','')[:10]} | {r.get('orgSName','')} | {r.get('title','')[:60]}")
    except Exception as e:
        print(f"  研报获取失败: {e}")


if __name__ == "__main__":
    main()
