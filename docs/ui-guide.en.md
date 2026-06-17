# Yohaku UI Guide

This guide is for Codex App users who prefer not to use the command line. It
shows how to add the Yohaku marketplace, install Goal Shaper, and invoke it
from the composer.

Screenshots are for orientation; version numbers and starter prompt text may
differ slightly from the current release.

## Add The Yohaku Marketplace

Open **Plugins**, add a marketplace, and enter `gaoguobin/yohaku` as the
source. Keep the Git ref and sparse path empty unless your organization gives
you a different value.

![Add marketplace dialog with gaoguobin/yohaku as the source](assets/ui/add-marketplace.png)

If Yohaku does not appear immediately, restart Codex App and open **Plugins**
again.

## Install Goal Shaper

Select the `Yohaku` marketplace and open **Goal Shaper**.

![Yohaku marketplace with Goal Shaper available](assets/ui/yohaku-marketplace.png)

Open the plugin details page, then select **Add to Codex**. Confirm the
version and developer details on the page. Starter prompt text can change
between releases, so use the version field as the source of truth.

![Goal Shaper details page](assets/ui/plugin-detail.png)

Start a new Codex thread after installation.

## Use Goal Shaper

In a new thread, use one of these entrypoints.

### Slash Command List

Type `/`, search for `Goal Shaper`, then select the skill.

![Slash entrypoint showing Goal Shaper](assets/ui/composer-slash.png)

### Plugin Mention

Type `@` and select the installed Goal Shaper plugin or its bundled capability.

![At mention entrypoint showing Goal Shaper](assets/ui/composer-at.png)

### Explicit Skill Mention

Type `$goal-shaper` when you want the most precise skill invocation.

![Dollar skill mention showing Goal Shaper](assets/ui/composer-dollar.png)

## Update

If Codex App shows an update or reinstall action on the plugin details page,
use it and then start a new thread.

If the page still shows an older version and no update action appears, uninstall
Goal Shaper, remove and re-add the `Yohaku` marketplace if needed, reinstall
Goal Shaper, restart Codex App, and start a new thread.

Removing the marketplace affects every plugin installed from Yohaku.

## Uninstall

Open **Plugins**, open the installed Goal Shaper details page, select
**Uninstall plugin**, and start a new thread. Remove the `Yohaku` marketplace
only when you no longer use any plugins from it.
