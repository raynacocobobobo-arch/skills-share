# HermesTodo 真机部署

## 设备信息（已连接过）
- **名称**: 张三
- **型号**: iPhone 16 Pro (iPhone17,1)
- **UDID**: `00008140-001E34122111801C`
- **CoreDevice ID**: `F5305800-2B7D-5905-8238-207B0DBB6FBE`

## 部署流程

### 1. 前置条件
- Xcode 中已登录 Apple ID（免费账号即可，每7天重签一次）
- iPhone 用数据线连 Mac，解锁并"信任此电脑"

### 2. 开启开发者模式（iOS 16+）
命令行无法触发，必须在 Xcode **GUI** 中操作：
1. Xcode → Window → Devices and Simulators
2. 左侧选设备，等同步完成（安装 DDI）
3. iPhone 上：设置 → 隐私与安全性 → 最底部 → 开发者模式 → 开启
4. iPhone 重启后解锁，弹出"启用"确认对话框 → 输入密码

### 3. 签名配置
- 项目 → Signing & Capabilities → Team 下拉选 Apple ID
- 或命令行传 Team ID（不推荐——`-allowProvisioningUpdates` 也能自动处理）

### 4. 编译到真机
```bash
cd ${HERMES_TODO_ROOT}
env -u TMPDIR xcodebuild \
  -scheme HermesTodo \
  -destination 'platform=iOS,id=00008140-001E34122111801C' \
  -allowProvisioningUpdates \
  build
```

### 5. 安装到真机
```bash
xcrun devicectl device install app --device F5305800-2B7D-5905-8238-207B0DBB6FBE \
  /path/to/HermesTodo.app
```
或用 Xcode GUI：顶部选"张三" → ⌘R 直接 Run。

## 常见阻碍

| 错误 | 原因 | 解决 |
|------|------|------|
| `Developer Mode disabled` | iOS 16+ 安全机制 | Xcode Devices 窗口同步 + 手机设置开启 |
| `no DDI` | Developer Disk Image 没装 | Xcode Devices 窗口选设备等同步 |
| `Timed out waiting for destinations` | 设备未就绪 | 确保手机解锁 + 信任 + 开发者模式已开 |
| `requires a development team` | 项目没选 Team | Signing & Capabilities 下拉选 Apple ID |
| `0 valid identities found` | 还没用 Xcode 连过设备 | 首次连设备时 Xcode 自动生成证书 |

## 命令行工具速查

```bash
# 设备列表
xcrun xctrace list devices
xcrun devicectl list devices

# 设备详情
xcrun devicectl device info F5305800-2B7D-5905-8238-207B0DBB6FBE

# 签名证书
security find-identity -v -p codesigning

# 安装 App（iOS 17+）
xcrun devicectl device install app --device <id> <app_path>
```
