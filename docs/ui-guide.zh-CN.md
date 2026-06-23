# Yohaku UI 使用指南

这份指南面向不想使用命令行的 Codex App 用户，说明如何添加 Yohaku
插件市场、安装其中的插件，并在输入框里调用它们。

截图只用于定位界面；版本号和示例按钮文案可能与当前发布略有不同。

## 添加 Yohaku 插件市场

打开 **插件**，添加插件市场，在来源里填写 `gaoguobin/yohaku`。Git 引用和
稀疏路径保持空白，除非你的团队明确要求填写其他值。

![添加插件市场弹窗，来源填写 gaoguobin/yohaku](assets/ui/add-marketplace.png)

如果没有马上看到 Yohaku，重启 Codex App 后再打开 **插件**。

## 安装插件

选择 `Yohaku` 市场，打开你要安装的插件，例如 **Goal Shaper** 或
**Seed**。

![Yohaku 市场中显示可安装插件](assets/ui/yohaku-marketplace.png)

进入详情页后点击 **添加到 Codex**。你可以在详情页确认版本、开发者、网站、
隐私政策和服务条款。示例按钮文案可能随版本变化，判断安装版本时以版本号为准。

![插件详情页](assets/ui/plugin-detail.png)

安装后请新开一个 Codex 会话。

## 使用已安装插件

在新会话里，可以用下面任一种入口。

### `/` 入口

输入 `/`，搜索插件提供的 skill，例如 `Goal Shaper` 或 `Seed`，然后选择它。

![斜杠入口示例](assets/ui/composer-slash.png)

### `@` 入口

输入 `@`，选择已经安装的 Yohaku 插件或它包含的能力。

![At 入口示例](assets/ui/composer-at.png)

### `$` 精确调用

如果你知道 skill 名称，可以直接输入 `$goal-shaper` 或 `$seed`，这是最精确的调用方式。

![Dollar skill mention 示例](assets/ui/composer-dollar.png)

## 更新

重启 Codex App，打开插件详情页确认版本。如果版本仍然是旧的，使用 `UPDATE.md`
里的 CLI 更新流程。

## 卸载

打开 **插件**，进入已安装插件的详情页，选择 **卸载插件**，然后新开会话。
只有当你不再使用任何 Yohaku 插件时，才移除 `Yohaku` 市场。
