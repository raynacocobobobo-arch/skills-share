---
name: android-adb-apk-shortcuts
display_name: Android ADB APK 与桌面快捷方式封装
description: Android/Redmi Pad 通过 ADB 识别设备、核对已安装 App 与桌面 pinned shortcut、提取 APK、或把系统桌面快捷方式封装成独立可安装 APK 的工作流。
triggers:
  - Android APK
  - adb install
  - Redmi Pad
  - 平板 APK
  - 做成apk
  - 桌面快捷方式
  - pinned shortcut
  - 山西综合广播
  - 小米收音机
---

# Android ADB APK 与桌面快捷方式封装

## 适用场景

用户要求给 Android 平板/Redmi Pad 做 APK、安装 APK、提取已安装应用，或把桌面上的某个**快捷方式**做成一个可安装 APK。

典型语句：

- “继续给 pad 做 apk”
- “我不是连了一个 Redmi Pad 吗”
- “把这个快捷方式做成 apk”
- “这个图标是绿色的”
- “安装到 pad 上”

## 核心原则

1. **先区分 App 和快捷方式。** Android 桌面上的图标不一定是一个独立 App，可能是某个 App 发布的 pinned shortcut。
2. **不要只看 `pm list packages` 或 APK label 就下结论。** 用户说“这是别的应用”时，优先查 `dumpsys shortcut`。
3. **安装前后必须验证。** `adb install` 返回 `Success` 才能说装上；装完用 `cmd package resolve-activity` 或 `monkey` 验证可启动。
4. **如果用户说的是快捷方式，正确做法通常是做一个“包装 APK”。** 这个 APK 自己有桌面入口和图标，点击后用 Intent 打开原 shortcut 指向的目标 Activity/deeplink。
5. **图标描述要以用户视觉为准。** 如果用户明确说“绿色图标”，包装 APK 的 launcher icon 就做成绿色，避免装出来像另一个应用。

## 标准流程

### 1. 确认设备连接

```bash
adb devices -l
```

确认状态是 `device`。小米/Redmi 设备型号可能不直接显示品牌名，ADB 能列出 device 即可继续。

### 2. 判断这是 App 还是 pinned shortcut

先粗查包名：

```bash
adb shell pm list packages | grep -i -E 'radio|fm|ting|shanxi|sx|launcher'
adb shell dumpsys package <package>
```

但**如果用户说的是桌面快捷方式**，必须查 shortcut：

```bash
adb shell dumpsys shortcut | grep -i -A 12 -B 8 '山西\|综合\|广播\|关键词\|包名'
```

重点提取：

- `packageName=`：发布 shortcut 的真实包
- `activity=`：宿主 Activity
- `shortLabel=`：桌面显示名
- `intents=[Intent ...]`：点击快捷方式时实际启动的 Intent
- `PersistableBundle[...]`：shortcut 参数 / scheme / type
- `bitmapPath=`：如果有自定义图标，说明桌面图标可能不是 APK 默认图标

### 3. 如果只是提取已安装 App APK

查路径并 pull：

```bash
adb shell pm path <package>
adb pull <base.apk路径> ~/Desktop/hermes/pad-apk/<应用名>.apk
```

验证：

```bash
aapt dump badging ~/Desktop/hermes/pad-apk/<应用名>.apk | head -30
adb install -r ~/Desktop/hermes/pad-apk/<应用名>.apk
```

注意：这种方式提取的是**宿主 App**，不等于桌面上的具体频道/页面快捷方式。

### 4. 如果要把快捷方式做成 APK

做一个独立 wrapper APK：

- `AndroidManifest.xml`：独立包名，例如 `com.enwan.<shortcut>`，`MAIN + LAUNCHER`
- `MainActivity`：`onCreate()` 里组装原 shortcut 的 Intent，然后 `startActivity()`，最后 `finish()`
- 图标：按用户描述生成/替换 launcher icon，例如绿色广播图标
- label：用用户说的快捷方式名，而不是宿主 App 名

MainActivity 模式：

```java
Intent intent = new Intent(Intent.ACTION_VIEW);
intent.setPackage("<shortcut packageName>");
intent.setClassName("<shortcut packageName>", "<shortcut activity class>");
intent.putExtra("shortcuts_select_page", false);
intent.putExtra("shortcuts_scheme", "<shortcut deeplink>");
intent.putExtra("shortcuts_type", "pin_common");
intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
startActivity(intent);
finish();
```

保留 fallback：如果目标宿主 App 被禁用/缺失，打开宿主 App 或 Toast 提示。

### 5. 构建与签名

可用 Android command line tools：

```bash
# 发现工具路径
find /opt/homebrew /Library/Android ~/Library/Android -name aapt -o -name apksigner -o -name zipalign -o -name d8 -o -name android.jar 2>/dev/null | head
```

构建步骤：

```bash
aapt package -f -m -J build/generated -M AndroidManifest.xml -S res -I "$ANDROID_JAR"
javac -source 8 -target 8 -bootclasspath "$ANDROID_JAR" -d build/classes $(find src build/generated -name '*.java')
d8 --lib "$ANDROID_JAR" --output build/dex $(find build/classes -name '*.class')
aapt package -f -M AndroidManifest.xml -S res -I "$ANDROID_JAR" -F build/unsigned.apk build/dex
zipalign -f 4 build/unsigned.apk build/aligned.apk
apksigner sign --ks build/debug.keystore --ks-pass pass:android --key-pass pass:android --out <最终.apk> build/aligned.apk
apksigner verify --verbose <最终.apk>
```

如果系统 `/usr/bin/java` 不可用，但 Homebrew OpenJDK 存在，可以在单次命令里设置：

```bash
export JAVA_HOME=/opt/homebrew/Cellar/openjdk/<version>/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"
```

这不是硬编码规则；每次以实际机器上的 Java 路径为准。

### 6. 安装与验收

```bash
adb install -r <最终.apk>
adb shell cmd package resolve-activity --brief <wrapper包名>
adb shell monkey -p <wrapper包名> -c android.intent.category.LAUNCHER 1
```

对用户只说最终状态：

- APK 文件路径
- App 名 / 包名
- 图标特征
- 安装结果 `Success`
- 点击后打开的目标

不要把大量构建日志贴给用户，除非失败需要排障。

## 常见坑

1. **把宿主 App 当成快捷方式。** 例如用户说桌面“山西综合广播”快捷方式，真实是 `com.miui.fm` 发布的 pinned shortcut；不要误提取 `net.joydao.radio` 这种名字像广播的第三方 App。
2. **APK label 和用户看到的桌面名不一致。** `aapt dump badging` 看到 `听听广播`，不代表用户说的 `山西综合广播` 就是这个 APK。
3. **shortcut 图标可能来自 bitmapPath。** 无 root 时未必能 pull `/data/system_ce/.../shortcut_service/bitmaps/...`，此时按用户描述自制相近图标更可靠。
4. **`adb install` 被用户限制拦截。** 小米设备可能返回 `INSTALL_FAILED_USER_RESTRICTED`，这通常需要在平板上确认允许安装；不能说已经装上。
5. **用户说“停止”必须立刻停。** 不继续解释、不继续执行后台排障。

## 已沉淀参考

- `references/shanxi-radio-shortcut-wrapper.md`：Redmi Pad 上“山西综合广播FM904”pinned shortcut 识别、绿色 wrapper APK 封装与验证细节。
