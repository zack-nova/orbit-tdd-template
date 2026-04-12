# 八个仓库中与 TDD / 测试规则相关内容整理

本文只整理这 8 个仓库里，和 **TDD、test-first、测试约束、验证流程、spec-first / test-first 方法论** 最相关的说明与文件路径，便于后续快速查阅。

---

## 1. `garrytan/gstack`

仓库地址：`https://github.com/garrytan/gstack`

### 结论
- 这个仓库**强烈强调测试、回归测试、覆盖率审计**。
- 但它更像是 **test-everything / regression-first / coverage-audit**，不属于“默认硬性经典 TDD（先写 failing test 再写实现）”表述最明确的那一类。

### 相关说明
- `README.md` 里明确写到：
  - `/ship` 会做 **coverage audit**。
  - `/qa` 修复 bug 时会自动生成 **regression test**。
  - 总体理念是 **Test everything**。
- `qa/SKILL.md` 更偏执行层规则：
  - 新函数要补测试。
  - 修 bug 要补回归测试。
- `ship/SKILL.md` 更偏发布前规则：
  - 发布前跑测试、看覆盖情况。
  - 对 bug fix 的回归测试要求更硬。

### 相关文件目录
- `README.md`
- `qa/SKILL.md`
- `ship/SKILL.md`

---

## 2. `gsd-build/get-shit-done`

仓库地址：`https://github.com/gsd-build/get-shit-done`

### 结论
- 这个仓库**不是把 TDD 设成全局默认硬规则**。
- 它的主线更像：**discuss → plan → execute → verify → ship**。
- 但仓库里**确实存在专门的 TDD / 测试补充工作流文档**，所以可以认为它是“支持 TDD、但主流程更偏 verification-first”。

### 相关说明
- `README.md` 里最核心的是整体开发流程，重点放在：
  - 先计划与执行。
  - 再通过 `/gsd-verify-work` 做人工验收与验证。
- `get-shit-done/workflows/add-tests.md`：
  - 这是最接近 TDD 的专门文档。
  - 文中有 **TDD classification**、按批准的测试项逐条推进的描述。
- `get-shit-done/workflows/verify-work.md`：
  - 这是主流程中的验收验证文档。
  - 重点是“功能是否真的可用”，而不仅仅是测试是否通过。
- `get-shit-done/workflows/verify-phase.md`：
  - 偏阶段性验证规则。
- `get-shit-done/references/verification-patterns.md`：
  - 偏验证模式和检查结构的参考资料。

### 相关文件目录
- `README.md`
- `get-shit-done/workflows/add-tests.md`
- `get-shit-done/workflows/verify-work.md`
- `get-shit-done/workflows/verify-phase.md`
- `get-shit-done/references/verification-patterns.md`

---

## 3. `bmad-code-org/BMAD-METHOD`

仓库地址：`https://github.com/bmad-code-org/BMAD-METHOD`

### 结论
- 这个仓库**没有把 TDD 写成默认硬规则**。
- 它更偏向 **系统化测试治理 / QA / ATDD**。
- 如果从方法论角度看，它是“测试体系很完整”，但不是“默认一上来就 test-first”。

### 相关说明
- `docs/reference/testing.md`：
  - 这是最核心的测试参考文档。
  - 里面把测试拆成 **built-in QA** 和 **TEA module**。
  - 明确支持 **ATDD**、traceability、release gates 等测试治理能力。
- `docs/reference/modules.md`：
  - 这里能看到测试模块在整套方法里的定位。
  - 更利于理解测试不是孤立功能，而是 BMAD 方法的一部分。

### 相关文件目录
- `docs/reference/testing.md`
- `docs/reference/modules.md`

> 备注：仓库里还有多语言镜像版本，例如：
- `docs/zh-cn/reference/testing.md`
- `docs/zh-cn/reference/modules.md`

---

## 4. `Fission-AI/OpenSpec`

仓库地址：`https://github.com/Fission-AI/OpenSpec`

### 结论
- 这个仓库的核心不是 TDD，而是 **spec-first**。
- 它更强调：**先把需求、变更、设计、任务说明清楚，再开始写代码**。
- 因此如果非要归类，它更适合归到“规格优先”，不是“测试优先”。

### 相关说明
- `README.md`：
  - 明确强调在真正编码之前先对齐 proposal / spec / design / tasks。
- `docs/concepts.md`：
  - 适合看 OpenSpec 的核心概念，理解它为什么是 spec-first。
- `docs/workflows.md`：
  - 展示整体工作流，适合看“从想法到实现”的过程结构。
- `docs/commands.md`：
  - 说明常用命令与工作方式。
- `docs/getting-started.md`：
  - 适合快速查看实际使用路径。

### 相关文件目录
- `README.md`
- `docs/concepts.md`
- `docs/workflows.md`
- `docs/commands.md`
- `docs/getting-started.md`

---

## 5. `Yeachan-Heo/oh-my-claudecode`

仓库地址：`https://github.com/Yeachan-Heo/oh-my-claudecode`

### 结论
- 这几个仓库里，**它对 TDD 的显式表述最直接的一类**。
- 它不是说“所有任务都默认强制 TDD”，但它提供了**非常明确的 TDD keyword / 模式入口**。

### 相关说明
- `docs/REFERENCE.md`：
  - 直接把 `tdd`、`test first`、`red green` 归入 **TDD workflow enforcement**。
  - 这是最重要的一份文档。
- `AGENTS.md`：
  - 说明 keyword mode 会把 TDD 指导注入工作流。
  - 并且将 `tdd` shortcut 映射到 `test-engineer`。

### 相关文件目录
- `docs/REFERENCE.md`
- `AGENTS.md`

---

## 6. `affaan-m/everything-claude-code`

仓库地址：`https://github.com/affaan-m/everything-claude-code`

### 结论
- 这个仓库**明确内置了 TDD 专用 agent、skill 和命令入口**。
- 它属于**显式支持 test-first** 的类型，而且把覆盖率、测试类型和 RED → GREEN → REFACTOR 流程写得比较完整。

### 相关说明
- `agents/tdd-guide.md`：
  - 直接定义了一个 **TDD specialist**。
  - 写明 **tests-before-code**、**Red-Green-Refactor**、**80%+ test coverage**。
  - 还要求覆盖 unit / integration / E2E，以及常见 edge cases。
- `skills/tdd-workflow/SKILL.md`：
  - 这是该仓库里更标准的 TDD workflow skill 入口。
  - 通常应和 agent 配套理解。
- `commands/tdd.md`：
  - 这是 `/tdd` 的兼容入口。
  - 文中明确写了 maintained workflow 在 `skills/tdd-workflow/SKILL.md`。
- `.opencode/prompts/agents/tdd-guide.txt` 与 `.kiro/agents/tdd-guide.md`：
  - 说明它把同一套 TDD 能力适配到了不同宿主 / 运行环境。

### 相关文件目录
- `README.md`
- `agents/tdd-guide.md`
- `skills/tdd-workflow/SKILL.md`
- `commands/tdd.md`
- `.opencode/prompts/agents/tdd-guide.txt`
- `.kiro/agents/tdd-guide.md`

---

## 7. `github/spec-kit`

仓库地址：`https://github.com/github/spec-kit`

### 结论
- 这个仓库**明确支持 test-first / TDD**，但**不是无条件全局强制**。
- 它更准确地说是：
  - 方法论上明显偏 **test-first**；
  - 实现模板支持 **先测后写**；
  - 但任务生成阶段又允许 **Tests are OPTIONAL**，只有在 spec 明确要求测试或用户要求 TDD 时才展开测试任务。

### 相关说明
- `spec-driven.md`：
  - 最清楚地写了 **implementation template enforces test-first development**。
  - 还给出顺序：先 `contracts/`，再 contract → integration → e2e → unit 测试，最后写源码让测试通过。
- `templates/commands/implement.md`：
  - 明确要求执行时 **先执行测试任务，再执行对应实现任务**。
  - 属于执行阶段的 test-first 规则。
- `templates/commands/tasks.md`：
  - 这里非常关键。
  - 文中明确写了 **Tests are OPTIONAL**。
  - 只有 feature spec 明确要求测试，或者用户明确要求 TDD，才生成测试任务。
- `docs/quickstart.md`：
  - 示例 constitution 中有 **We use TDD strictly**。
  - 这表示 TDD 可以通过 constitution 被项目级强制化。
- `templates/commands/constitution.md`：
  - 用来维护 constitution，也就是项目自己的原则源头。
  - 说明 testing discipline 这类原则可以通过 constitution 进入整个流程。
- `README.md`：
  - 更偏整体使用说明与命令入口。
  - 适合作为总入口文件保留。

### 相关文件目录
- `README.md`
- `spec-driven.md`
- `templates/commands/implement.md`
- `templates/commands/tasks.md`
- `templates/commands/constitution.md`
- `docs/quickstart.md`

---

## 8. `obra/superpowers`

仓库地址：`https://github.com/obra/superpowers/`

### 结论
- 这是这批仓库里**TDD 规则写得最“铁”**的一类。
- 它不是泛泛谈测试，而是直接把 **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST** 写成核心规则。
- 可以视为**严格 TDD skill**。

### 相关说明
- `skills/test-driven-development/SKILL.md`：
  - 明确说明使用场景是：**before writing implementation code**。
  - 文中写了：
    - **Write the test first. Watch it fail. Write minimal code to pass.**
    - **The Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**
    - 严格的 **Red-Green-Refactor** 循环。
  - 还列出大量反例与“如果你先写了代码就删掉重来”的强规则。
- `README.md`：
  - 可作为 skill 总入口保留，便于结合仓库整体结构查看。

### 相关文件目录
- `README.md`
- `skills/test-driven-development/SKILL.md`

---

# 汇总判断

| 仓库 | 更接近哪类 | 是否有明确 TDD 入口 |
|---|---|---|
| `garrytan/gstack` | 强测试 / 回归测试 / 覆盖率审计 | 有测试硬约束，但不是最典型的 TDD 明文 |
| `gsd-build/get-shit-done` | verification-first，附带 TDD 相关工作流 | 有，但不是全局默认主线 |
| `bmad-code-org/BMAD-METHOD` | QA / ATDD / 测试治理 | 有测试体系，但不是默认 TDD |
| `Fission-AI/OpenSpec` | spec-first | 不是以 TDD 为核心 |
| `Yeachan-Heo/oh-my-claudecode` | 明确支持 TDD workflow | 是 |
| `affaan-m/everything-claude-code` | 内置 TDD agent / skill / command | 是，而且很完整 |
| `github/spec-kit` | test-first + constitution 可强化 + tests optional | 是，但是否强制取决于 spec / constitution / 用户要求 |
| `obra/superpowers` | 严格 TDD skill | 是，而且规则非常硬 |

---


# 一键下载这些相关文档原文（最新版）

下面这条命令会**自动查询每个仓库当前默认分支**，然后下载这些文件在默认分支上的**最新版本**到本地目录 `repo-docs-latest/`。

```bash
bash -lc '
set -euo pipefail
base="repo-docs-latest"
mkdir -p "$base"

get_default_branch() {
  local repo="$1"
  curl -fsSL "https://api.github.com/repos/$repo" \
    | sed -n '\''s/.*"default_branch": *"\([^"]*\)".*/\1/p'\''
}

dl_latest() {
  local repo="$1"
  local path="$2"
  local branch="$3"
  local out="$base/${repo//\//__}/$path"
  mkdir -p "$(dirname "$out")"
  curl -fsSL "https://raw.githubusercontent.com/$repo/$branch/$path" -o "$out"
  echo "saved $out"
}

repos=(
  "garrytan/gstack"
  "gsd-build/get-shit-done"
  "bmad-code-org/BMAD-METHOD"
  "Fission-AI/OpenSpec"
  "Yeachan-Heo/oh-my-claudecode"
  "affaan-m/everything-claude-code"
  "github/spec-kit"
  "obra/superpowers"
)

declare -A branches
for repo in "${repos[@]}"; do
  branches["$repo"]="$(get_default_branch "$repo")"
  echo "branch $repo -> ${branches[$repo]}"
done

# garrytan/gstack
repo="garrytan/gstack"; b="${branches[$repo]}"
dl_latest "$repo" "README.md" "$b"
dl_latest "$repo" "qa/SKILL.md" "$b"
dl_latest "$repo" "ship/SKILL.md" "$b"

# gsd-build/get-shit-done
repo="gsd-build/get-shit-done"; b="${branches[$repo]}"
dl_latest "$repo" "README.md" "$b"
dl_latest "$repo" "get-shit-done/workflows/add-tests.md" "$b"
dl_latest "$repo" "get-shit-done/workflows/verify-work.md" "$b"
dl_latest "$repo" "get-shit-done/workflows/verify-phase.md" "$b"
dl_latest "$repo" "get-shit-done/references/verification-patterns.md" "$b"

# bmad-code-org/BMAD-METHOD
repo="bmad-code-org/BMAD-METHOD"; b="${branches[$repo]}"
dl_latest "$repo" "docs/reference/testing.md" "$b"
dl_latest "$repo" "docs/reference/modules.md" "$b"

# Fission-AI/OpenSpec
repo="Fission-AI/OpenSpec"; b="${branches[$repo]}"
dl_latest "$repo" "README.md" "$b"
dl_latest "$repo" "docs/concepts.md" "$b"
dl_latest "$repo" "docs/workflows.md" "$b"
dl_latest "$repo" "docs/commands.md" "$b"
dl_latest "$repo" "docs/getting-started.md" "$b"

# Yeachan-Heo/oh-my-claudecode
repo="Yeachan-Heo/oh-my-claudecode"; b="${branches[$repo]}"
dl_latest "$repo" "docs/REFERENCE.md" "$b"
dl_latest "$repo" "AGENTS.md" "$b"

# affaan-m/everything-claude-code
repo="affaan-m/everything-claude-code"; b="${branches[$repo]}"
dl_latest "$repo" "README.md" "$b"
dl_latest "$repo" "agents/tdd-guide.md" "$b"
dl_latest "$repo" "skills/tdd-workflow/SKILL.md" "$b"
dl_latest "$repo" "commands/tdd.md" "$b"
dl_latest "$repo" ".opencode/prompts/agents/tdd-guide.txt" "$b"
dl_latest "$repo" ".kiro/agents/tdd-guide.md" "$b"

# github/spec-kit
repo="github/spec-kit"; b="${branches[$repo]}"
dl_latest "$repo" "README.md" "$b"
dl_latest "$repo" "spec-driven.md" "$b"
dl_latest "$repo" "templates/commands/implement.md" "$b"
dl_latest "$repo" "templates/commands/tasks.md" "$b"
dl_latest "$repo" "templates/commands/constitution.md" "$b"
dl_latest "$repo" "docs/quickstart.md" "$b"

# obra/superpowers
repo="obra/superpowers"; b="${branches[$repo]}"
dl_latest "$repo" "README.md" "$b"
dl_latest "$repo" "skills/test-driven-development/SKILL.md" "$b"

echo
find "$base" -type f | sort
'
```

---

# 使用建议

- 如果你只想快速判断“谁最偏严格 TDD”，优先看：
  - `obra/superpowers/skills/test-driven-development/SKILL.md`
  - `affaan-m/everything-claude-code/agents/tdd-guide.md`
  - `Yeachan-Heo/oh-my-claudecode/docs/REFERENCE.md`
- 如果你想看“test-first 但是否强制取决于项目规则”，优先看：
  - `github/spec-kit/spec-driven.md`
  - `github/spec-kit/templates/commands/tasks.md`
  - `github/spec-kit/docs/quickstart.md`
- 如果你想看“强测试但不完全等于 TDD”的做法，优先看：
  - `garrytan/gstack/qa/SKILL.md`
  - `garrytan/gstack/ship/SKILL.md`
- 如果你想看“验证优先 / 验收优先”的流程，优先看：
  - `gsd-build/get-shit-done/get-shit-done/workflows/add-tests.md`
  - `gsd-build/get-shit-done/get-shit-done/workflows/verify-work.md`
- 如果你想看“测试不是核心，规格才是核心”，优先看：
  - `Fission-AI/OpenSpec/README.md`
  - `Fission-AI/OpenSpec/docs/workflows.md`

