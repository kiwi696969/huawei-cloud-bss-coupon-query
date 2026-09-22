# 验证方法

| 场景 | 执行命令 | 预期结果 | 通过标准 |
|------|----------|----------|----------|
| 代金券列表 | `hcloud BSS ListPartnerCouponsRecord --cli-region=cn-north-1` | 返回 record 数组（或结构化权限提示） | 命令执行无语法错误，输出可解析 JSON |
| 券配额记录 | `hcloud BSS ListCouponQuotasRecords --cli-region=cn-north-1` | 返回 quota 记录数组 | 同上 |
| 权限不足场景 | 同上（普通账号） | `domain_id has no access to this api` 结构化提示 | 技能能识别并给出权限开通建议 |
| 即将到期分析 | 基于 expire_time 字段的脚本解析 | 输出 30 天内到期券列表 | 日期解析正确、按到期日排序 |
| 使用率分析 | 基于 face_value/used_amount 计算 | 输出发放/已用/剩余/使用率 | 计算正确 |

## 测试记录（本作品实测）

```bash
$ hcloud BSS ListPartnerCouponsRecord --cli-region=cn-north-1
{ "error_msg": "domain_id has no access to this api." }

$ hcloud BSS ListIssuedPartnerCoupons --cli-region=cn-north-1
{ "error_msg": "domain_id has no access to this api." }
```

- 结论：当前测试账号未开通 BSS 伙伴/企业代金券接口权限。
- 处置：技能在权限不足时返回结构化错误（`PERMISSION_DENIED`）并提供 IAM 策略指引，
  见 `iam-policies.md`；账号开通对应权限后即可查询真实代金券数据。
