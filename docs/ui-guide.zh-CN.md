# Yohaku UI 使用指南

这份指南面向不想使用命令行的 Codex App 用户，说明如何添加 Yohaku
插件市场、安装 Goal Shaper，并在输入框里调用它。

截图只用于定位界面；版本号和示例按钮文案可能与当前发布略有不同。

## 添加 Yohaku 插件市场

打开 **插件**，添加插件市场，在来源里填写 `gaoguobin/yohaku`。Git 引用和
稀疏路径保持空白，除非你的团队明确要求填写其他值。

![添加插件市场弹窗，来源填写 gaoguobin/yohaku](assets/ui/add-marketplace.png)

如果没有马上看到 Yohaku，重启 Codex App 后再打开 **插件**。

## 安装 Goal Shaper

选择 `Yohaku` 市场，打开 **Goal Shaper**。

![Yohaku 市场中显示 Goal Shaper](assets/ui/yohaku-marketplace.png)

进入详情页后点击 **添加到 Codex**。你可以在详情页确认版本、开发者、网站、
隐私政策和服务条款。示例按钮文案可能随版本变化，判断安装版本时以版本号为准。

![Goal Shaper 详情页](assets/ui/plugin-detail.png)

安装后请新开一个 Codex 会话。

## 使用 Goal Shaper

在新会话里，可以用下面任一种入口。

### `/` 入口

输入 `/`，搜索 `Goal Shaper`，然后选择这个 skill。

![斜杠入口中显示 Goal Shaper](assets/ui/composer-slash.png)

### `@` 入口

输入 `@`，选择已经安装的 Goal Shaper 插件或它包含的能力。

![At 入口中显示 Goal Shaper](assets/ui/composer-at.png)

### `$` 精确调用

如果你知道 skill 名称，可以直接输入 `$goal-shaper`，这是最精确的调用方式。

![Dollar skill mention 中显示 Goal Shaper](assets/ui/composer-dollar.png)

## 更新

如果详情页出现更新或重新安装按钮，直接使用它，然后新开会话。

如果详情页仍显示旧版本，并且没有更新按钮，可以卸载 Goal Shaper；必要时移除并
重新添加 `Yohaku` 市场，再重新安装 Goal Shaper，重启 Codex App，并新开会话。

移除 Yohaku 市场会影响从这个市场安装的所有插件。

## 卸载

打开 **插件**，进入已安装的 Goal Shaper 详情页，选择 **卸载插件**，然后新开
会话。只有当你不再使用任何 Yohaku 插件时，才移除 `Yohaku` 市场。
