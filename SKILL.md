---
name: huawei-cloud-bss-coupon-query
description: >-
  Query Huawei Cloud BSS (Business Support System) coupons: coupon list, coupon
  status, expiring-soon detection, and usage analysis. Use this skill when users
  want to check their coupon/quota balances, list coupons, see which coupons are
  about to expire, or analyze coupon usage rate on Huawei Cloud. Trigger when
  users mention 代金券/coupon/quota、查询代金券/list coupons、即将到期/expiring、
  使用率/usage rate、华为云 BSS/账单/优惠券、华为云/Huawei Cloud.
---

# Huawei Cloud BSS Coupon Query（BSS 代金券查询）

## 1. Overview

基于 hcloud CLI（KooCLI）封装华为云 BSS 代金券查询能力，提供四类查询：

| 能力 | 说 明 |
|------|-------|
| `coupon_list` | 代金券列表（ListIssuedPartnerCoupons / ListPartnerCouponsRecord） |
| `coupon_status` | 券状态查询（unused/used/expired，从列表字段解析） |
| `coupon_expiring` | 识别即将到期代金券（到期日在 N 天内，默认 30 天） |
| `coupon_usage` | 代金券使用率分析（发放/使用/剩余金额统计） |

## 2. Prerequisites

1. **hcloud CLI (KooCLI)**：已安装并配置华为云 AK/SK（见 `references/cli-installation-guide.md`）。
2. **BSS 域region**：BSS 接口固定区域为 `cn-north-1`，执行时统一加 `--cli-region=cn-north-1`。
3. **账号权限**：伙伴/企业代金券类接口需要对应权限（`domain_id has no access to this api` 时按 5.3 错误处理）。

## 3. Core Commands

```bash
# 代金券列表（伙伴代金券记录）
hcloud BSS ListPartnerCouponsRecord --cli-region=cn-north-1

# 代金券配额记录
hcloud BSS ListCouponQuotasRecords --cli-region=cn-north-1

# 发放的代金券配额
hcloud BSS ListIssuedCouponQuotas --cli-region=cn-north-1

# 按订单ID查代金券
hcloud BSS ListOrderCouponsByOrderId --cli-region=cn-north-1
```

## 4. Query & Analysis

### 4.1 代金券列表（coupon_list）
执行 `ListPartnerCouponsRecord` 并展示 coupon_id、coupon_type、status、face_value、expire_time 等核心字段；对复杂 JSON 用 `--output json` + jq/python 精简。

### 4.2 券状态查询（coupon_status）
按 `status` 字段汇总：`unused`（未使用）、`used`（已使用）、`expired`（已过期），输出分类统计。

### 4.3 即将到期识别（coupon_expiring）
对 `expire_time`（YYYY-MM-DD）与当前日期比较，筛选 30 天内到期且未使用的券，按到期日升序展示并给出使用建议。

### 4.4 使用率分析（coupon_usage）
基于 `face_value`（面额）与 `used_amount`（已用金额）计算使用率：`usage_rate = used_amount / face_value`；汇总总发放、总已用、总剩余与整体使用率。

## 5. Error Handling

| 场景 | 错误信号 | 处置 |
|------|----------|------|
| 未配置/失效 AK/SK | hcloud 提示认证失败 | 引导用户按 cli-installation-guide 配置后重试 |
| 区域不支持 | `cli-region 的值不支持` | 强制 `--cli-region=cn-north-1` |
| 无接口权限 | `domain_id has no access to this api` | 结构化返回：账号需开通对应 BSS 权限（伙伴/企业账号），说明所需 IAM 策略（见 iam-policies.md） |
| 参数错误/检索为空 | 空数组 / USE_ERROR | 提示调整查询条件后重试 |

## 6. Quality Checklist

- [ ] 所有命令统一 `--cli-region=cn-north-1`
- [ ] 查询类操作，不创建/修改任何云资源
- [ ] 不打印或要求输入 AK/SK 明文
- [ ] 错误场景有结构化中文提示与处理建议

## 7. References

- `references/cli-installation-guide.md` — hcloud 安装与 AK/SK 配置
- `references/iam-policies.md` — BSS 代金券查询所需权限说明
- `references/verification-method.md` — 验证方法（各命令预期输出与通过标准）