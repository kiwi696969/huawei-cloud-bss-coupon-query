# Skill · 如何写好一个调用华为云服务的技能

ICT 大赛云赛道赛题 1.10：使用技能三件套（creator/tester/audit）从零完成一个华为云 Skill 的创建、测试、审计与发布闭环。本例为 **huawei-cloud-bss-coupon-query（BSS 代金券查询）**，全程查询类操作，不创建云资源、不产生费用。

## 作品内容

```
huawei-cloud-bss-coupon-query/
├── SKILL.md                      # 技能主文件（frontmatter + 功能 + 错误处理）
├── references/
│   ├── cli-installation-guide.md # hcloud 安装与 AK/SK 配置
│   ├── iam-policies.md           # BSS 代金券查询所需权限
│   └── verification-method.md    # 验证方法（用例与预期）
├── scripts/
│   └── analyze_coupons.py        # 代金券分析（列表/状态/即将到期/使用率）
├── TEST_REPORT.md                # 功能测试报告（4 用例全 PASS）
└── SECURITY_AUDIT_REPORT.md      # 安全审计报告（审计通过）
```

## 技能三件套闭环

| 阶段 | 工具 | 交付物 |
|------|------|--------|
| 创建 | huawei-cloud-skill-creator | SKILL.md + references + scripts（结构规范） |
| 测试 | huawei-cloud-skill-tester | TEST_REPORT.md（功能正确） |
| 审计 | huawei-cloud-skill-audit | SECURITY_AUDIT_REPORT.md（安全合规） |

**三项质量标准**：结构规范（SKILL.md frontmatter/目录）→ 功能正确（测试用例真实通过）→ 安全合规（审计 Gate PASS）。

## 功能与实测

| 能力 | 说明 | 实测 |
|------|------|------|
| coupon_list | 代金券列表（hcloud BSS 命令） | ✅ 命令链可用 |
| coupon_status | 券状态分类汇总 | ✅ |
| coupon_expiring | 30 天内即将到期识别 | ✅ C002(8天) 被识别 |
| coupon_usage | 使用率分析 | ✅ 51.43% |

## 可复用方法论（任意华为云服务技能）

1. **需求分析**：明确要封装哪些接口、能力边界（查询类优先，零成本）；
2. **技术调研**：CLI → SDK → OpenAPI 三级降级探测可用命令；
3. **脚手架**：SKILL.md（name/description/triggers）+ references + scripts；
4. **测试**：真实命令 + 模拟用例 + 错误分支（权限/空结果/解析失败）；
5. **审计**：密钥扫描 + 危险命令 + 权限检查，Gate 通过才发布。
