# 山西综合广播FM904 shortcut wrapper 参考

## 背景

用户在 Redmi Pad 桌面看到一个绿色图标快捷方式，名称是“山西综合广播”。最初误判为已安装 App `net.joydao.radio`，其 APK label 实际是“听听广播”，用户纠正“听听广播是别的应用”。

关键教训：桌面图标可能是 pinned shortcut，不是独立 APK。

## 正确识别方法

用：

```bash
adb shell dumpsys shortcut | grep -i -A 12 -B 8 '山西\|综合\|广播\|joydao\|qingting\|fm'
```

查到：

```text
Package: com.miui.fm
Pinned: radioPlayViewShortcut:20491
ShortcutInfo {id=radioPlayViewShortcut:20491, flags=0x8a [PinIc-fStr]
  packageName=com.miui.fm
  activity=ComponentInfo{com.miui.fm/fm.qingting.qtradio.WelcomeActivity}
  shortLabel=山西综合广播FM904
  intents=[Intent { act=android.intent.action.VIEW xflg=0x4 pkg=com.miui.fm cmp=com.miui.fm/fm.qingting.qtradio.ShortcutsActivity }/PersistableBundle[{shortcuts_select_page=false, shortcuts_scheme=qingtingfm://app.qingting.fm/playingview?channel_id=20491&type=live, shortcuts_type=pin_common}]]
  bitmapPath=/data/system_ce/0/shortcut_service/bitmaps/com.miui.fm/1782089474588.png
}
```

宿主 App：

```bash
adb shell pm path com.miui.fm
# package:/product/data-app/MiRadio/MiRadio.apk
```

## Wrapper APK 参数

独立包名：

```text
com.enwan.shanxiradio
```

桌面名称：

```text
山西综合广播
```

启动 Intent：

```java
Intent intent = new Intent(Intent.ACTION_VIEW);
intent.setPackage("com.miui.fm");
intent.setClassName("com.miui.fm", "fm.qingting.qtradio.ShortcutsActivity");
intent.putExtra("shortcuts_select_page", false);
intent.putExtra("shortcuts_scheme", "qingtingfm://app.qingting.fm/playingview?channel_id=20491&type=live");
intent.putExtra("shortcuts_type", "pin_common");
intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
startActivity(intent);
finish();
```

图标：用户明确说是绿色图标。无法直接读取 bitmapPath 时，生成绿色广播图标作为 launcher icon。

## 验收命令

```bash
apksigner verify --verbose ~/Desktop/hermes/pad-apk/山西综合广播-绿色快捷方式.apk
aapt dump badging ~/Desktop/hermes/pad-apk/山西综合广播-绿色快捷方式.apk | grep -E "package:|application:|application-icon"
adb install -r ~/Desktop/hermes/pad-apk/山西综合广播-绿色快捷方式.apk
adb shell cmd package resolve-activity --brief com.enwan.shanxiradio
adb shell monkey -p com.enwan.shanxiradio -c android.intent.category.LAUNCHER 1
```

成功结果包含：

```text
application-label:'山西综合广播'
application: label='山西综合广播' icon='res/mipmap-mdpi-v4/ic_launcher.png'
Performing Incremental Install
Success
com.enwan.shanxiradio/.MainActivity
Events injected: 1
```

## 用户沟通注意

- 不要说“听听广播就是山西综合广播”。用户已明确纠正不是。
- 如果只是从已安装 App 提取 APK，必须说明“这是宿主 App，不一定是桌面那个快捷方式”。
- 最终回复只给可用结论：已安装、包名、图标、点击打开目标、APK 文件路径。
