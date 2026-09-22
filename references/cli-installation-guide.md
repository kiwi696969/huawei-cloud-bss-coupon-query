# hcloud CLI 安装与认证指南

## 1. 安装 KooCLI（hcloud）

```bash
# Linux/macOS 一键安装
curl -sSL https://cn-north-4-hcs-cloudpublist.obs.cn-north-4.myhuaweicloud.com/cloudpublist/../cli/install.sh | bash
# 验证
hcloud version
```

也可到华为云开发者工具页面下载对应平台的安装包。

## 2. 配置 AK/SK

```bash
hcloud configure set --cli-access-key=<AK> --cli-secret-key=<SK>
# 或使用环境变量（推荐，避免明文落盘）
export HW_ACCESS_KEY=<AK>
export HW_SECRET_KEY=<SK>
export HW_CLI_REGION=cn-north-1
hcloud configure list   # 只读检查，不回显密钥
```

> 安全提示：AK/SK 是长期凭证，请勿写入代码仓库；SK 仅在创建时显示一次，遗失需重新创建。
