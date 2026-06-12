# Goal Shaper v0 设计说明

日期：2026-06-12
状态：已讨论的 v0 设计稿

## 目标

Goal Shaper v0 是一个 Codex Skill，用来把普通用户的一句简短需求，通过自适应采访，整理成符合 Codex Goal mode 最佳实践的 `/goal` 产物包。

它不负责执行 goal，也不负责控制 Codex 的 goal runtime。它的边界是：澄清意图，生成可审查、可复制、可运行的 goal package，然后停止。

## 目标用户

第一版默认用户是已经能使用 Codex Goal mode、但不擅长把模糊需求写成高质量 `/goal` 的普通 Codex 用户。

典型场景：

- 用户只有一句自然语言需求，例如“帮我把这个项目的测试补好”。
- 用户知道想让 Codex 长时间推进，但不知道如何定义完成条件。
- 用户需要一个可验证、带边界、带暂停条件的 goal prompt。
- 用户的需求可能太小、太大或缺少验证方式，需要先判断是否适合 Goal mode。

## 已确认决策

- MVP 入口：Codex Skill。
- 产物边界：默认输出文本包，复杂任务可选写 support spec。
- 采访强度：自适应采访。
- 输出语言：双语。中文面向用户解释，英文面向 Codex 执行。
- support spec 默认位置：`.goal-shaper/specs/`。
- skill 内部形态：Seed 风格，但拆出 schema、rubric、templates。
- 写文件策略：写 support spec 前必须确认；需要 ignore 规则时单独提示，不自动修改用户仓库规则。

## 核心流程

1. 接收用户的简短需求。
2. 判断是否适合 Goal mode。
3. 抽取 goal canonical fields。
4. 对缺失字段做影响评估。
5. 只追问会影响成功、验证、安全或范围的关键缺口。
6. 判断复杂度，选择 compact goal 或 support spec。
7. 生成双语 goal package。
8. 按 rubric 自审。
9. 展示最终产物，等待用户复制或确认写 spec。
10. 停止，不自动运行 `/goal`。

## Goal 适用性判断

推荐使用 Goal mode 的请求应同时满足：

- 目标比一个普通 prompt 大。
- 目标比一个开放 backlog 小。
- 有可验证完成状态。
- 路径可能需要多步探索、修复、验证或迭代。

不推荐使用 Goal mode 的请求：

- 一句话解释。
- 单行修改。
- 很短的 code review。
- 没有可信验证面的任务。
- 多个无关目标堆在一起的 backlog。

当请求太小时，skill 应建议普通 prompt。当请求太大时，skill 应建议拆分为更小的 goal，而不是生成一个巨大的 `/goal`。

## Canonical Fields

第一版使用一套统一字段，不为 bug、性能、研究、迁移分别写特殊流程。

必需字段：

- `outcome`：完成后具体成立的状态。
- `verification_surface`：证明完成的测试、命令、产物、日志、报告或人工验收。
- `constraints`：执行期间不能破坏的约束。
- `boundaries`：允许使用或修改的文件、工具、环境、数据和资源。
- `iteration_policy`：每轮尝试后如何选择下一步。
- `blocked_stop_condition`：什么情况下停止并向用户报告。
- `initial_materials`：开始前必须先读的文件、issue、日志、计划或参考。
- `validation_and_review`：完成前必须执行的验证和审查。
- `checkpoint_policy`：进度 checkpoint 和短日志要求。
- `pause_triggers`：必须暂停或确认的高风险动作。

支持字段：

- `domain`
- `target_environment`
- `repos_or_files`
- `allowed_tools`
- `forbidden_actions`
- `risk_level`
- `final_artifact`
- `uncertainty_policy`
- `budget_or_time_limit`
- `durable_guidance_bucket`
- `support_spec_required`
- `complexity_level`

## 自适应采访策略

采访不是固定问卷。skill 先从用户原始需求中抽取已有信息，再只问真正影响结果的问题。

追问优先级：

1. 验证面。
2. 成功阈值。
3. 范围边界或目标环境。
4. 安全约束或禁止动作。
5. blocked stop condition。
6. 初始阅读材料和 checkpoint 策略。

问题形式应尽量是 2 到 3 个选项，并给出简短取舍。每次只问一个问题。

默认行为：

- 如果 outcome 和 verification 已经足够清晰，直接出草稿。
- 如果缺失会导致追错目标、错误验收或高风险操作，必须追问。
- 如果只是低影响偏好，直接写成假设，不继续打断用户。

## 复杂度分级

v0 使用四级复杂度：

- `small`：输出 compact goal。
- `medium`：输出 compact goal 加 evidence checklist。
- `large`：输出 compact goal 加 support spec。
- `too_broad`：建议拆分，不生成单一 goal。

复杂度判断依据：

- 是否跨多个子系统。
- 是否需要长上下文。
- 是否需要恢复、checkpoint 或 decision log。
- 是否涉及高风险操作。
- `/goal` 是否会接近或超过 4,000 字符。

## 输出产物

### Compact Goal Package

用于 small 和 medium 请求。

内容：

- 中文摘要：说明目标、验证方式、关键假设。
- 英文 `/goal`：用户可直接复制到 Codex。
- Evidence checklist：完成前应看到的证据。
- Assumptions：低风险但未确认的假设。
- Durable guidance candidates：不应塞进一次性 goal 的长期规则。

英文 `/goal` 模板：

```text
/goal <outcome>, verified by <evidence>, while preserving <constraints>. Use <boundaries>. Between iterations, <iteration policy>. If blocked, stop and report <blocked evidence and next input needed>.
```

### Goal With Support Spec

用于 large 请求。

内容：

- 中文摘要。
- 英文短 `/goal`，引用 support spec。
- support spec 文件建议路径。
- support spec 内容预览。
- 写文件确认提示。

英文 `/goal` 模板：

```text
/goal Complete <outcome> according to <support spec path>, verified by <evidence summary>, while preserving <constraints summary>. If blocked, stop with attempted paths, evidence gathered, blocker, and next input needed.
```

support spec 应包含：

- context
- objective
- acceptance checks
- boundaries
- constraints
- initial materials
- milestones or checkpoints
- iteration policy
- blocker policy
- safety and permission policy
- decision log
- recovery notes
- final report format

## Skill 文件形态

v0 建议实现为 repo skill：

```text
.agents/skills/goal-shaper/
  SKILL.md
  references/
    goal-schema.md
    rubric.md
    examples.md
  templates/
    goal-package.md
    support-spec.md
```

职责划分：

- `SKILL.md`：触发条件、工作流、采访规则、停止规则。
- `references/goal-schema.md`：字段定义、复杂度分类、适用性判断。
- `references/rubric.md`：质量评分、自审清单、反例。
- `references/examples.md`：bug、性能、研究、迁移、too small、too broad 示例。
- `templates/goal-package.md`：最终对话输出模板。
- `templates/support-spec.md`：可选 support spec 模板。

v0 不加入 CLI、Web App、脚本 eval 或多 harness 生成器。

## 安全与权限规则

skill 必须显式区分一次性 goal 约束和长期工作规则。

长期规则应进入 `durable_guidance_bucket`，提示用户可迁移到：

- `AGENTS.md`
- skill
- Codex config
- team docs

必须暂停或确认的动作包括：

- 生产环境变更。
- 凭据、token、密钥、cookie 相关操作。
- 网络访问或外部写入。
- 删除、迁移、覆盖、权限变更。
- 写 workspace 外路径。
- destructive app、MCP 或 shell 操作。
- 可能 rewrite history 或影响共享分支的 git 操作。

Goal Shaper v0 只生成这些规则，不替用户执行相关动作。

## 自审 Rubric

最终输出前必须检查：

- outcome 是否具体。
- verification_surface 是否可执行或可审查。
- constraints 是否写清楚。
- boundaries 是否足够限制工作范围。
- iteration_policy 是否避免“随便继续试”。
- blocked_stop_condition 是否明确。
- initial_materials 是否存在或已说明无。
- validation_and_review 是否包含最小相关验证。
- pause_triggers 是否覆盖高风险动作。
- durable_guidance_bucket 是否没有被误塞进一次性 goal。
- `/goal` 是否非空且低于 4,000 字符。
- support spec 是否只在复杂任务中使用。

评分：

- `0`：缺失。
- `1`：存在但模糊。
- `2`：具体且可审查。

outcome 和 verification_surface 必须为 `2`。其他字段可以为 `1`，但必须在 assumptions 中明示。

## 初始验收场景

v0 设计应覆盖这些样例：

1. Bug fix：模糊 bug 描述被改写为先复现、再修复、再验证的 goal。
2. Performance：明确指标、benchmark、连续运行次数和不回归约束。
3. Research：最终报告区分 confirmed、approximate、blocked、unknown。
4. Too small：建议普通 prompt，而不是硬生成 goal。
5. Too broad：建议拆分子目标。
6. High risk：先追问环境、边界、rollback 或暂停条件。
7. Long context：输出短 `/goal` 加 support spec。
8. Durable guidance：把长期规则列为 `AGENTS.md` 或 skill 候选。

## 非目标

v0 不做：

- Web App。
- Local CLI。
- 服务端。
- 多用户账号。
- 自动运行 `/goal`。
- 内部 create_goal runtime 调用。
- 自动修改 `.gitignore`。
- 自动创建 git commit。
- 脚本化 eval。
- 多 agent harness 适配。

## 设计风险

- 如果模板太重，用户会觉得它像表单系统。缓解方式：自适应采访，默认只问关键缺口。
- 如果模板太轻，输出会退化成普通 prompt。缓解方式：outcome 和 verification 必须达到评分 `2`。
- 如果可选写 spec 太积极，会污染用户仓库。缓解方式：写前确认，并默认放在 `.goal-shaper/specs/`。
- 如果英文 `/goal` 和中文解释不一致，会误导用户。缓解方式：自审时检查中文摘要和英文 goal 是否表达同一目标。

## 终止条件

当 skill 交付最终 goal package 后必须停止。它可以提示用户复制 `/goal` 或确认写 support spec，但不能继续进入实现计划，也不能替用户启动 Goal mode。
