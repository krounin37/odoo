# Odoo 项目安装与运行指南

<p align="center">
  <a href="README.md"><b>English</b></a> |
  <a href="README.vi.md"><b>Tiếng Việt</b></a> |
  <a href="README.zh.md"><b>简体中文</b></a>
</p>

---

## 📌 项目概述

本仓库包含 **Odoo** 开源企业管理系统源码，并附带 Docker Compose 配置文件，便于快速在本地部署运行与二次开发。

---

## 🚀 方式一：使用 Docker 快速启动（推荐）

通过 **Docker Compose** 启动 Odoo 及其 PostgreSQL 数据库是最简单、快捷且环境隔离的方式。

### 前置条件
- 已安装并启动 [Docker](https://docs.docker.com/get-docker/)（或 Docker Desktop）
- [Docker Compose](https://docs.docker.com/compose/install/)（Docker Desktop 默认自带）

### 1. 启动容器服务
在项目根目录下执行以下命令：

```bash
docker compose up -d
```

该命令将启动两个服务：
- **web**: Odoo Web 应用服务，映射在端口 `8069`
- **db**: PostgreSQL 16 数据库服务

### 2. 访问 Odoo
打开浏览器并访问：
```
http://localhost:8069
```

首次访问时需填写数据库初始化表单：
- **Master Password**: 主管理密码（用于备份、恢复、删除数据库，请妥善保管）
- **Database Name**: 数据库名称（例如：`odoo_db`）
- **Email / Password**: 管理员登录邮箱与密码
- **Language / Country**: 选择语言（如：简体中文 / Chinese (Simplified)）与国家
- **Demo data**: 如需加载演示测试数据，请勾选此项

### 3. 常用 Docker 操作命令

- **查看 Web 服务实时日志**：
  ```bash
  docker compose logs -f web
  ```
- **停止容器服务**：
  ```bash
  docker compose down
  ```
- **停止容器并删除数据卷（重置数据库）**：
  ```bash
  docker compose down -v
  ```
- **重启服务**：
  ```bash
  docker compose restart
  ```

---

## 🛠️ 方式二：本地 Python 原生环境运行（开发调试模式）

如果您希望直接在本地 Python 环境中运行 Odoo：

### 前置要求
- Python 3.10、3.11 或 3.12
- 本地安装并运行 PostgreSQL 14+
- `wkhtmltopdf`（推荐安装，用于生成 PDF 报表）

### 1. 创建并激活虚拟环境

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. 安装依赖包

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. 配置 PostgreSQL 数据库用户

```bash
createuser -s odoo
createdb -O odoo odoo_db
```

### 4. 创建配置文件 (`odoo.conf`)
在项目根目录下创建 `odoo.conf` 文件：

```ini
[options]
addons_path = addons
admin_passwd = admin_secret_password
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
http_port = 8069
```

### 5. 启动 Odoo 服务

```bash
# 使用配置文件启动
python odoo-bin -c odoo.conf

# 或通过命令行参数直接启动
python odoo-bin --addons-path=addons -d odoo_db --db_user=odoo --db_password=odoo
```

---

## 💡 常用开发命令

- **开启开发者热重载模式（Python 代码与前端资源自动刷新）**：
  ```bash
  python odoo-bin -c odoo.conf --dev=all
  ```
- **安装新模块**：
  ```bash
  python odoo-bin -c odoo.conf -d odoo_db -i <module_name>
  ```
- **升级/更新现有模块**：
  ```bash
  python odoo-bin -c odoo.conf -d odoo_db -u <module_name>
  ```

---

## 🇻🇳 越南本地化扩展模块 (`custom_addons/`)

本项目已内置开发并集成针对越南企业实际业务场景的核心扩展模块：

| 模块名称 | 功能说明 | 状态 |
| :--- | :--- | :---: |
| **`l10n_vn_tax_lookup`** | **税号自动查询企业信息**：输入企业税号（MST）时，自动调用官方数据接口，快速填充企业法定全称、注册地址及纳税人正常经营状态。 | ✅ 已就绪 |
| **`l10n_vn_vietqr_sale`** | **报价单/销售订单动态 VietQR**：自动生成 NAPAS 247 动态银行转账二维码（含精准金额与订单备注），支持界面显示与 PDF 打印。 | ✅ 已就绪 |
| **`l10n_vn_address`** | **越南三级行政区划**：省/直辖市 → 县/区/市 → 坊/镇/社 级联筛选与地址自动标准化，适配电子发票与越南主流物流对接。 | ✅ 已就绪 |

### 如何在 Odoo 中启用扩展模块：
1. 进入 **Apps (应用中心)**。
2. 在设置中开启开发者模式 (**Developer Mode**)。
3. 点击顶部 **Update Apps List (更新应用列表)**。
4. 搜索模块名 (`l10n_vn_tax_lookup`、`l10n_vn_vietqr_sale` 或 `l10n_vn_address`)，点击 **Activate (安装)** 即可。

---

## 📄 开源许可
Odoo 遵循 LGPLv3 / Odoo Enterprise License 开源协议，详情请参见 `LICENSE` 文件。
