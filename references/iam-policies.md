# BSS 代金券查询所需权限

BSS（Business Support System）代金券/余额类接口按账号类型区分权限：

| 接口 | 权限要求 | 适用账号 |
|------|----------|----------|
| ListPartnerCouponsRecord | 伙伴代金券查询权限（bss:coupon:listPartnerCouponsRecord） | 伙伴账号 |
| ListIssuedCouponQuotas | 发放券配额查询 | 伙伴账号 |
| ListCouponQuotasRecords | 券配额记录查询 | 伙伴账号 |
| 费用账单/余额类（Balance/Dashboard） | 账号基本查询权限 | 所有实名账号 |

## 最小权限建议

若使用 IAM 子用户，建议最小授权策略（示例）：

```json
{
  "Version": "1.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:coupon:listPartnerCouponsRecord",
        "bss:coupon:listIssuedCouponQuotas",
        "bss:coupon:listCouponQuotasRecords",
        "bss:balance:view"
      ],
      "Resource": ["*"]
    }
  ]
}
```

> 访问 BSS 接口时统一使用 `--cli-region=cn-north-1`。
