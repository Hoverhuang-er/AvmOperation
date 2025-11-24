# avmoperation

Azure 虚拟机操作 Python 库，支持启动、停止、查询虚拟机状态，并通过 Webhook 发送通知。

## 功能特性

- 基于 Azure Management SDK 的虚拟机操作
- Service Principal 身份认证
- Webhook 通知集成（支持飞书、企业微信等）
- 同步操作接口
- 虚拟机状态查询
- 类型提示支持

## 依赖要求

- Python 3.11+
- azure-identity >= 1.15.0
- azure-mgmt-compute >= 30.0.0
- requests >= 2.31.0

## 安装

### 使用 pip 从 GitHub 安装

```bash
pip install git+https://github.com/Hoverhuang-er/avmoperation.git
```

### 使用 uv 从 GitHub 安装

```bash
uv add git+https://github.com/Hoverhuang-er/avmoperation.git
```

### 从本地源码安装（开发模式）

```bash
git clone https://github.com/Hoverhuang-er/avmoperation.git
cd avmoperation
pip install -e .
```

## 前置条件

### 创建 Service Principal

使用 Azure CLI 创建具有虚拟机贡献者权限的 Service Principal：

```bash
az ad sp create-for-rbac \
  --name "vm-operator" \
  --role "Virtual Machine Contributor" \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}
```

记录输出的凭证信息：
- `appId` → `AZURE_CLIENT_ID`
- `tenant` → `AZURE_TENANT_ID`
- `password` → `AZURE_CLIENT_SECRET`

## 快速开始

### 基本使用

```python
from avmoperation import AzureVMOperator

# 初始化操作器
operator = AzureVMOperator(
    subscription_id="your-subscription-id",
    vm_name="your-vm-name",
    resource_group="your-resource-group",
    webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
    client_id="your-client-id",
    tenant_id="your-tenant-id",
    client_secret="your-client-secret"
)

# 启动虚拟机
if operator.start_vm():
    print("虚拟机启动成功")

# 查询状态
status = operator.get_status()
print(f"虚拟机状态：{status}")

# 停止虚拟机
if operator.stop_vm():
    print("虚拟机停止成功")
```

### 使用环境变量

```python
import os
from avmoperation import AzureVMOperator

# 从环境变量读取配置
operator = AzureVMOperator(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    vm_name=os.getenv("AZURE_VM_NAME"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    webhook_url=os.getenv("WEBHOOK_URL"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET")
)

operator.start_vm()
```

## API 参考

### AzureVMOperator

主操作类，用于管理 Azure 虚拟机。

#### 初始化参数

```python
AzureVMOperator(
    subscription_id: str,
    vm_name: str,
    resource_group: str,
    webhook_url: str,
    client_id: str,
    tenant_id: str,
    client_secret: str
)
```

**参数说明：**

- `subscription_id` (str): Azure 订阅 ID
- `vm_name` (str): 虚拟机名称
- `resource_group` (str): 资源组名称
- `webhook_url` (str): Webhook 通知 URL
- `client_id` (str): Service Principal 客户端 ID
- `tenant_id` (str): Azure 租户 ID
- `client_secret` (str): Service Principal 客户端密钥

#### 方法

##### start_vm()

启动虚拟机并发送 Webhook 通知。

```python
def start_vm(self) -> bool
```

**返回值：**
- `bool`: 操作成功返回 `True`，失败返回 `False`

**示例：**

```python
success = operator.start_vm()
if success:
    print("虚拟机已启动")
```

##### stop_vm()

停止虚拟机并发送 Webhook 通知。

```python
def stop_vm(self) -> bool
```

**返回值：**
- `bool`: 操作成功返回 `True`，失败返回 `False`

**示例：**

```python
success = operator.stop_vm()
if success:
    print("虚拟机已停止")
```

##### get_status()

查询虚拟机当前电源状态。

```python
def get_status(self) -> Optional[str]
```

**返回值：**
- `Optional[str]`: 返回虚拟机状态字符串（如 `"PowerState/running"`），失败返回 `None`

**示例：**

```python
status = operator.get_status()
if status:
    print(f"当前状态：{status}")
```

## 使用示例

### 示例 1：定时任务管理虚拟机

```python
import schedule
import time
from avmoperation import AzureVMOperator

operator = AzureVMOperator(
    subscription_id="your-subscription-id",
    vm_name="your-vm-name",
    resource_group="your-resource-group",
    webhook_url="your-webhook-url",
    client_id="your-client-id",
    tenant_id="your-tenant-id",
    client_secret="your-client-secret"
)

# 每天早上 8 点启动
schedule.every().day.at("08:00").do(operator.start_vm)

# 每天晚上 6 点停止
schedule.every().day.at("18:00").do(operator.stop_vm)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 示例 2：批量管理多个虚拟机

```python
from avmoperation import AzureVMOperator

vms = [
    {"name": "vm1", "resource_group": "rg1"},
    {"name": "vm2", "resource_group": "rg2"},
]

subscription_id = "your-subscription-id"
webhook_url = "your-webhook-url"
client_id = "your-client-id"
tenant_id = "your-tenant-id"
client_secret = "your-client-secret"

for vm in vms:
    operator = AzureVMOperator(
        subscription_id=subscription_id,
        vm_name=vm["name"],
        resource_group=vm["resource_group"],
        webhook_url=webhook_url,
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret
    )
    operator.start_vm()
```

### 示例 3：集成到 Flask 应用

```python
from flask import Flask, jsonify
from avmoperation import AzureVMOperator
import os

app = Flask(__name__)

operator = AzureVMOperator(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    vm_name=os.getenv("AZURE_VM_NAME"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    webhook_url=os.getenv("WEBHOOK_URL"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET")
)

@app.route("/vm/start", methods=["POST"])
def start_vm():
    success = operator.start_vm()
    return jsonify({"success": success})

@app.route("/vm/stop", methods=["POST"])
def stop_vm():
    success = operator.stop_vm()
    return jsonify({"success": success})

@app.route("/vm/status", methods=["GET"])
def vm_status():
    status = operator.get_status()
    return jsonify({"status": status})

if __name__ == "__main__":
    app.run()
```


## Webhook 集成

库支持通过 Webhook 发送虚拟机操作通知，默认支持飞书格式。

### 飞书（Lark）集成

```python
from avmoperation import AzureVMOperator

operator = AzureVMOperator(
    subscription_id="your-subscription-id",
    vm_name="your-vm-name",
    resource_group="your-resource-group",
    webhook_url="https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
    client_id="your-client-id",
    tenant_id="your-tenant-id",
    client_secret="your-client-secret"
)

# 操作成功后会自动发送通知
operator.start_vm()
```

### 通知消息格式

```
[Azure VM START]
VM: your-vm-name
Resource Group: your-resource-group
Status: Success
Message: VM 'your-vm-name' started successfully
Time: 2025-11-24 14:30:00 UTC
```

### 自定义 Webhook 格式

如需集成其他 Webhook 服务（如 Slack、Discord、企业微信），可以继承 `AzureVMOperator` 类并重写 `_send_webhook` 方法：

```python
from avmoperation import AzureVMOperator
import requests

class CustomWebhookOperator(AzureVMOperator):
    def _send_webhook(self, action: str, status: str, message: str):
        """自定义 Webhook 消息格式"""
        payload = {
            "text": f"{action}: {message}",
            "status": status
        }
        try:
            requests.post(self.webhook_url, json=payload, timeout=10)
        except Exception as e:
            print(f"Webhook 发送失败: {e}")
```

## 命令行工具

库安装后会提供 `avmop` 命令行工具。

### 使用方法

```bash
# 启动虚拟机
avmop start --subscription-id <id> --vm-name <name> --resource-group <rg> \
  --client-id <id> --tenant-id <id> --client-secret <secret> \
  --webhook-url <url>

# 停止虚拟机
avmop stop --subscription-id <id> --vm-name <name> --resource-group <rg> \
  --client-id <id> --tenant-id <id> --client-secret <secret> \
  --webhook-url <url>

# 查询状态
avmop status --subscription-id <id> --vm-name <name> --resource-group <rg> \
  --client-id <id> --tenant-id <id> --client-secret <secret> \
  --webhook-url <url>
```

### 使用环境变量

```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_VM_NAME="your-vm-name"
export AZURE_RESOURCE_GROUP="your-resource-group"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export WEBHOOK_URL="https://webhook-url"

# 直接执行命令
avmop start
avmop status
avmop stop
```

## 高级用法

### 异常处理

```python
from avmoperation import AzureVMOperator

operator = AzureVMOperator(...)

try:
    if not operator.start_vm():
        print("虚拟机启动失败")
except Exception as e:
    print(f"操作异常: {e}")
```

### 状态监控

```python
import time
from avmoperation import AzureVMOperator

operator = AzureVMOperator(...)

# 启动虚拟机
operator.start_vm()

# 等待虚拟机完全启动
while True:
    status = operator.get_status()
    if status and "running" in status.lower():
        print("虚拟机已就绪")
        break
    time.sleep(10)
```

### 上下文管理器模式

```python
from avmoperation import AzureVMOperator
import time

class VMContext:
    def __init__(self, operator: AzureVMOperator):
        self.operator = operator
    
    def __enter__(self):
        print("启动虚拟机...")
        self.operator.start_vm()
        time.sleep(30)  # 等待启动完成
        return self.operator
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("停止虚拟机...")
        self.operator.stop_vm()

# 使用上下文管理器
operator = AzureVMOperator(...)
with VMContext(operator):
    # 在此区块内虚拟机保持运行
    print("执行业务逻辑...")
# 退出时自动停止虚拟机
```

## 故障排查

### 身份认证失败

验证 Service Principal 凭证是否正确：

```python
from azure.identity import ClientSecretCredential

try:
    credential = ClientSecretCredential(
        tenant_id="your-tenant-id",
        client_id="your-client-id",
        client_secret="your-client-secret"
    )
    # 测试凭证
    token = credential.get_token("https://management.azure.com/.default")
    print("认证成功")
except Exception as e:
    print(f"认证失败: {e}")
```

### 权限不足

确保 Service Principal 具有必要权限：

```bash
# 使用 Azure CLI 授予虚拟机贡献者角色
az role assignment create \
  --assignee <client-id> \
  --role "Virtual Machine Contributor" \
  --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group}
```

或者在 Azure Portal 中：
1. 进入资源组或订阅
2. 选择"访问控制(IAM)"
3. 点击"添加角色分配"
4. 选择"虚拟机参与者"角色
5. 分配给 Service Principal

### Webhook 通知失败

检查 Webhook URL 是否正确，测试连通性：

```python
import requests

response = requests.post(
    "your-webhook-url",
    json={"msg_type": "text", "content": {"text": "测试消息"}},
    timeout=10
)
print(response.status_code)
```

### 导入错误

如果遇到导入问题，确认库已正确安装：

```bash
pip show avmoperation
python -c "from avmoperation import AzureVMOperator; print('导入成功')"
```

## 开发指南

### 从源码构建

```bash
git clone https://github.com/Hoverhuang-er/avmoperation.git
cd avmoperation

# 使用 uv 开发
uv sync
uv run python -m pytest  # 运行测试

# 或使用传统方式
pip install -e .
```

### 运行测试

```bash
# 使用 uv
uv run pytest

# 使用 pip
pytest
```

### 代码格式化

```bash
# 使用 black
black .

# 使用 ruff
ruff check .
```

## 安全最佳实践

### 1. 凭证管理

切勿在代码中硬编码凭证：

```python
# 不推荐
operator = AzureVMOperator(
    client_secret="hardcoded-secret",  # 危险！
    ...
)

# 推荐
import os
operator = AzureVMOperator(
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    ...
)
```

### 2. 使用密钥管理服务

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# 从 Azure Key Vault 读取密钥
credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
client_secret = client.get_secret("vm-operator-secret").value

operator = AzureVMOperator(
    client_secret=client_secret,
    ...
)
```

### 3. 最小权限原则

仅授予 Service Principal 必要的权限，限定资源范围。

### 4. 定期轮换凭证

```bash
# 重置 Service Principal 密钥
az ad sp credential reset --id <client-id>
```

### 5. 版本管理

在 `.gitignore` 中排除敏感文件：

```
.env
*.secret
credentials.json
```

## 性能优化

### 并发操作多个虚拟机

```python
from concurrent.futures import ThreadPoolExecutor
from avmoperation import AzureVMOperator

def start_vm(vm_config):
    operator = AzureVMOperator(**vm_config)
    return operator.start_vm()

vm_configs = [
    {"subscription_id": "...", "vm_name": "vm1", ...},
    {"subscription_id": "...", "vm_name": "vm2", ...},
]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(start_vm, vm_configs)
    for result in results:
        print(f"结果: {result}")
```

### 复用操作器实例

避免频繁创建新实例：

```python
# 不推荐：每次操作都创建新实例
for i in range(10):
    operator = AzureVMOperator(...)
    operator.get_status()

# 推荐：复用同一实例
operator = AzureVMOperator(...)
for i in range(10):
    operator.get_status()
```

## 项目结构

```
avmoperation/
├── main.py              # 主模块和命令行入口
├── pyproject.toml       # 项目配置和依赖
├── README.md            # 本文档
├── requirements.txt     # 依赖列表
└── tests/               # 测试文件（如有）
```

## 版本兼容性

- Python 3.11+
- azure-identity 1.15.0+
- azure-mgmt-compute 30.0.0+
- requests 2.31.0+

## 变更日志

### v0.1.0 (2025-11-24)

- 初始版本发布
- 支持虚拟机启动/停止操作
- Service Principal 身份认证
- Webhook 通知功能
- 命令行工具
- 状态查询功能

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License

## 技术支持

如有问题或建议：

1. 查阅[故障排查](#故障排查)部分
2. 查看 [Azure CLI 文档](https://docs.microsoft.com/zh-cn/cli/azure/)
3. 在 GitHub 仓库提交 Issue
4. 联系维护者

## 相关资源

- [Azure SDK for Python 文档](https://learn.microsoft.com/zh-cn/python/api/overview/azure/)
- [Azure Identity 库](https://learn.microsoft.com/zh-cn/python/api/overview/azure/identity-readme)
- [Azure Compute Management 库](https://learn.microsoft.com/zh-cn/python/api/overview/azure/mgmt-compute-readme)
- [Azure 虚拟机文档](https://docs.microsoft.com/zh-cn/azure/virtual-machines/)
- [Service Principal 文档](https://docs.microsoft.com/zh-cn/azure/active-directory/develop/app-objects-and-service-principals)
- [飞书开放平台](https://open.feishu.cn/)
