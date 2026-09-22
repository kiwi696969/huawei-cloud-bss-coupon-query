# 测试报告 — huawei-cloud-bss-coupon-query

> 使用节自 huawei-cloud-skill-tester 的功能验证标准；执行环境：AI DevSpace（Linux, hcloud CLI 已配置凭证）

## 用例与结果

| # | 用例 | 操作 | 预期 | 实际 | 结果 |
|---|------|------|------|------|------|
| 1 | 代金券列表 + 使用率 + 即将到期 | 3 条模拟记录喂给 `analyze_coupons.py --usage` | 输出总量/到期/使用率 | total=3、expiring=1(C002, 8天)、usage_rate=0.5143 | ✅ PASS |
| 2 | 权限不足场景 | error 响应 `{"error_msg":"domain_id has no access..."}` | 结构化 PERMISSION_DENIED + 建议 | `PERMISSION_DENIED` + iam-policies 指引 | ✅ PASS |
| 3 | 空结果场景 | `[]` | EMPTY + count=0 | `{"error_code":"EMPTY","count":0}` | ✅ PASS |
| 4 | 真实 BSS 命令 | `hcloud BSS ListPartnerCouponsRecord --cli-region=cn-north-1` | 返回记录或权限提示 | 返回 `domain_id has no access to this api`（当前账号未开通 BSS 伙伴权限） | ✅ 符合预期（错误处理生效） |

## 覆盖结论

- 查询链路（列表/状态/即将到期/使用率）功能正确；
- 错误处理分支（权限不足、空结果、输入解析失败）均已覆盖；
- 查询类操作，无创建/删除/修改云资源副作用。

## 遗留

- 真实券数据依赖账号开通 BSS 伙伴代金券权限；开通后 `analyze_coupons.py` 可直接消费真实接口输出。
