# a-stock-data V3.2.2

> **A股全栈数据工具包** — 零依赖直连 13 数据源，七层数据架构，27+ 端点实测可用。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.2.2-blue)](https://github.com/simonlin1212/a-stock-data)

## 📦 功能概览

| 层级 | 数据源 | 覆盖内容 |
|------|--------|----------|
| **行情层** | mootdx (TCP) / 腾讯财经 / 百度股市通 | K线、五档盘口、实时价、PE/PB/市值、涨跌停、指数、ETF |
| **研报层** | 东财 reportapi / 同花顺一致预期 / iwencai | 研报列表、PDF下载、一致预期EPS、NL语义搜索 |
| **信号层** | 同花顺热点 / 北向资金 / 东财 slist / push2 | 强势股归因、北向资金、概念板块归属、资金流、龙虎榜、解禁、行业排名 |
| **资金面** | 东财 datacenter / push2his | 融资融券、大宗交易、股东户数、分红送转、120日资金流 |
| **新闻层** | 东财 search-api / np-weblist | 个股新闻、7×24全球资讯 |
| **基础数据** | mootdx finance / 东财 push2 / 新浪 | 财务快照(F10)、个股信息、财报三表 |
| **公告层** | 巨潮 cninfo | 公告全文检索+下载 |

### 核心优势

- **零依赖** — 除 `requests` + `pandas` 外无第三方数据封装依赖，直连底层 HTTP API
- **防封设计** — 内置统一节流入口 `em_get()`，东财请求自动限流 + 会话复用
- **27+ 端点** — 所有端点 2026-06 实测可用
- **模块化** — 按功能分层，按需导入，不用的模块零开销

## 🏗 项目结构

```
a-stock-data/
├── a_stock_data/           # 核心模块
│   ├── __init__.py         # 包初始化
│   ├── helpers.py          # 共用 helper（限流、会话、Ticker 归一化）
│   ├── market.py           # 行情层：腾讯行情、百度K线
│   ├── research.py         # 研报层：东财研报、同花顺EPS、iwencai
│   ├── signals.py          # 信号层：热点、板块、资金流、龙虎榜、解禁
│   ├── fundflow.py         # 资金面：两融、大宗、股东户数、分红
│   ├── fundamentals.py     # 基础数据：个股信息、新浪财报三表
│   ├── news.py             # 新闻层：个股新闻、全球资讯
│   ├── announcements.py    # 公告层：巨潮公告
│   └── valuation.py        # 估值工具：前向PE、PEG、PE消化
├── examples/               # 使用示例
│   ├── example_01_quick_valuation.py
│   ├── example_02_batch_valuation.py
│   ├── example_03_market_data.py
│   ├── example_04_signals.py
│   └── example_05_research_announcements.py
├── pyproject.toml          # 项目配置
├── README.md
└── LICENSE
```

## 🚀 安装

```bash
# 安装核心依赖（必选）
pip install requests pandas

# 可选：mootdx（TCP行情，不封IP）
pip install mootdx

# 可选：stockstats（技术指标计算）
pip install stockstats

# 或直接安装本包
pip install .
```

> **注意：** 除 `requests` + `pandas` 外，所有数据源均为免费公开 API，无需 API Key。
> 仅 iwencai 语义搜索需要额外配置 API Key（见下文）。

## 💡 快速开始

### 1. 实时行情

```python
from a_stock_data.market import tencent_quote

# 批量拉取个股行情
quotes = tencent_quote(["688017", "300476", "002463"])
for code, q in quotes.items():
    print(f"{q['name']}({code}): ¥{q['price']} PE={q['pe_ttm']} 市值={q['mcap_yi']}亿")

# 指数 & ETF
index_quotes = tencent_quote(["000001", "000300", "399006"])  # 上证/沪深300/创业板
etf_quotes = tencent_quote(["510050", "510300"])              # 上证50ETF/沪深300ETF
```

### 2. 一键完整估值

```python
from a_stock_data.valuation import full_valuation

result = full_valuation("688017")
# {'name': '绿的谐波', 'price': 224.12, 'pe_ttm': 300.45,
#  'pe_fwd': 280.3, 'cagr_pct': 15.0, 'peg': 1.87, 'digest_years': 2.1}
```

### 3. 概念板块归属

```python
from a_stock_data.signals import eastmoney_concept_blocks

blocks = eastmoney_concept_blocks("600519")
print(blocks["concept_tags"])
# ['食品饮料', '白酒Ⅲ', '白酒Ⅱ', '贵州板块', '酿酒概念', 'HS300_', ...]
```

### 4. 龙虎榜 + 解禁 + 两融

```python
from a_stock_data.signals import dragon_tiger_board, lockup_expiry
from a_stock_data.fundflow import margin_trading

# 龙虎榜
dtb = dragon_tiger_board("002475", "2026-06-14")
print(f"近30日上龙虎榜: {len(dtb['records'])} 次")

# 解禁预警
lockup = lockup_expiry("002475", "2026-06-14")
print(f"未来90天待解禁: {len(lockup['upcoming'])} 批")

# 融资融券
margin = margin_trading("600519")
print(f"最新融资余额: {margin[0]['rzye']/1e8:.2f}亿")
```

### 5. 财报三表

```python
from a_stock_data.fundamentals import sina_financial_report

# 利润表
lrb = sina_financial_report("600519", "lrb", num=5)
for item in lrb[:3]:
    print(f"报告期: {item['报告期']} 净利润: {item.get('净利润', '')}")

# 资产负债表 / 现金流量表
fzb = sina_financial_report("600519", "fzb")
llb = sina_financial_report("600519", "llb")
```

### 6. 公告 & 研报

```python
from a_stock_data.announcements import cninfo_announcements
from a_stock_data.research import eastmoney_reports

# 巨潮公告
anns = cninfo_announcements("688017")
for a in anns[:5]:
    print(f"{a['date']} | {a['type']} | {a['title']}")

# 东财研报
reports = eastmoney_reports("688017")
print(f"共 {len(reports)} 篇研报")
```

### 7. 北向资金 + 热点题材

```python
from a_stock_data.signals import ths_hot_reason, hsgt_realtime

# 当日强势股 + 题材归因
df_hot = ths_hot_reason()
print(df_hot[["代码", "名称", "涨幅%", "题材归因"]].head(10))

# 北向资金分钟流向
df_north = hsgt_realtime()
print(df_north.tail())
```

## 📊 数据源优先级

| 优先级 | 数据源 | 协议 | 封IP风险 | 覆盖 |
|--------|--------|------|----------|------|
| **1（首选）** | **mootdx** | TCP 7709 | **不封** | K线、盘口、逐笔、财务快照 |
| **2** | **腾讯财经** | HTTP GBK | **不封** | 实时价、PE/PB/市值/涨跌停 |
| **3** | 新浪 / 巨潮 / 同花顺 | HTTP | 低 | 财报、公告、热点 |
| **4** | **东财** | HTTP | **有限流** | 龙虎榜、研报、资金流、公告等独有数据 |

> **原则：能用 mootdx / 腾讯，就不用东财。** 东财接口内置了 `em_get()` 自动限流（≥1s间隔 + 随机抖动），直接调用即自带防封。

## 🔑 iwencai 语义搜索（可选）

仅 NL 主题搜索需要 API Key：

```bash
export IWENCAI_API_KEY="your_key_here"
export IWENCAI_BASE_URL="https://openapi.iwencai.com"
```

申请地址：https://www.iwencai.com/skillhub

## 📝 运行示例

```bash
cd examples

# 单票快速估值
python example_01_quick_valuation.py

# 批量估值对比
python example_02_batch_valuation.py

# 实时行情 + K线
python example_03_market_data.py

# 信号层：热点 + 板块 + 资金流
python example_04_signals.py

# 财报 + 公告 + 研报
python example_05_research_announcements.py
```

## 📄 依赖说明

| 依赖 | 版本 | 用途 | 必需 |
|------|------|------|------|
| requests | any | 所有 HTTP API | ✅ |
| pandas | any | 数据处理 | ✅ |
| mootdx | ≥0.10 | TCP行情+财务+F10 | ❌ 可选 |
| stockstats | any | 技术指标计算 | ❌ 可选 |

## ⚠️ 注意事项

1. **东财限流** — 所有东财接口已内置限流，批量调用时可将 `EM_MIN_INTERVAL` 调大到 1.5~2 秒
2. **网络环境** — mootdx 需国内 IP 才稳定；海外环境建议走代理
3. **编码** — 腾讯财经返回 GBK 编码，代码已自动处理
4. **大陆住宅 IP** — 部分住宅 IP 可能被东财间歇风控（HTTP 000/空），隔几分钟重试或换网络即可

## 📚 详细文档

SKILL.md 包含全部 27+ 端点的完整代码、字段说明、踩坑记录和组合用法。

## 🙏 致谢

- 作者：**Simon 林** · 抖音「Simon林」· 公众号「硅基世纪」
- 数据源：通达信、腾讯财经、东方财富、同花顺、百度股市通、新浪财经、巨潮资讯

## 📄 License

[MIT License](LICENSE)

---

> ⭐ Star 是最好的支持！
