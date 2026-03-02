# 字体目录（assets/fonts/）

将字体文件放在此目录，程序会**优先**使用这里的字体，无需修改 `config.yaml`。

---

## Windows 本地

无需任何操作，程序自动使用系统自带的**微软雅黑**（`C:\Windows\Fonts\msyh.ttc`）。

---

## Linux 服务器（无 sudo 权限）

在项目根目录执行一次即可：

```bash
python scripts/download_fonts.py
```

脚本会按顺序尝试：

| 步骤 | 动作 |
|------|------|
| 1 | `assets/fonts/` 已有字体 → 直接用，无需操作 |
| 2 | 扫描 `/usr/share/fonts`（无需 sudo，只读）→ 找到就复制过来 |
| 3 | 以上都没有 → 自动下载 **WQY MicroHei**（文泉驿微米黑，~4.6 MB）到此目录 |

完成后 **`config.yaml` 不用改**，运行时自动识别。

---

## 手动放置字体

如需使用其他字体，直接把字体文件复制到本目录即可，支持 `.ttf` / `.ttc` / `.otf`。

推荐免费字体：

| 字体 | 文件名 | 来源 |
|------|--------|------|
| WQY MicroHei（文泉驿微米黑） | `wqy-microhei.ttc` | `python scripts/download_fonts.py` 自动下载 |
| Noto Sans CJK | `NotoSansCJK-Regular.ttc` | 系统安装：`sudo apt install fonts-noto-cjk` |

> 如需指定某个字体，在 `config.yaml` 的 `subtitle.font` 填写**不含扩展名的文件名**，例如：
> ```yaml
> subtitle:
>   font: "NotoSansCJK-Regular"
> ```
