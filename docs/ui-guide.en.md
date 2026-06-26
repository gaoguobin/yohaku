# Yohaku UI Guide

This guide is for Codex App users who prefer not to use the command line. It
shows how to add the Yohaku marketplace, install a Yohaku plugin, and invoke
installed plugins from the composer.

Screenshots are for orientation; version numbers and starter prompt text may
differ slightly from the current release.

## Add The Yohaku Marketplace

Open **Plugins**, add a marketplace, and enter `gaoguobin/yohaku` as the
source. Keep the Git ref and sparse path empty unless your organization gives
you a different value.

![Add marketplace dialog with gaoguobin/yohaku as the source](assets/ui/add-marketplace.png)

If Yohaku does not appear immediately, restart Codex App and open **Plugins**
again.

## Install A Plugin

Select the `Yohaku` marketplace and open the plugin you want to install, such
as **Goal Shaper** or **Seed**.

![Yohaku marketplace with installable plugins](assets/ui/yohaku-marketplace.png)

Open the plugin details page, then select **Add to Codex**. Confirm the
version and developer details on the page. Starter prompt text can change
between releases, so use the version field as the source of truth.

![Plugin details page](assets/ui/plugin-detail.png)

Start a new Codex thread after installation.

## Use An Installed Plugin

In a new thread, use one of these entrypoints.

### Slash Command List

Type `/`, search for the skill provided by the plugin, such as `Goal Shaper` or
`Seed`, then select it.

![Slash entrypoint example](assets/ui/composer-slash.png)

### Plugin Mention

Type `@` and select the installed Yohaku plugin or one of its bundled
capabilities.

![At mention entrypoint example](assets/ui/composer-at.png)

### Explicit Skill Mention

Type `$goal-shaper` or `$seed` when you want the most precise skill invocation.

![Dollar skill mention example](assets/ui/composer-dollar.png)

## Update

Restart Codex App after a Yohaku update, open the plugin details page, and
confirm the version. If the version is still old after restart, use the CLI
update flow in `UPDATE.md`.

## Uninstall

Open **Plugins**, open the installed plugin details page, select **Uninstall
plugin**, and start a new thread. Remove the `Yohaku` marketplace only when you
no longer use any plugins from it.
