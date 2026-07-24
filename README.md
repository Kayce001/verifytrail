# VerifyTrail

面向 AI Agent 的证据优先验证框架。

Agent 可以声称成功，VerifyTrail 让它提供证据。

VerifyTrail 将 Agent 的每项主张与可执行证据关联，并给出以下四种结论之一：

- `verified`
- `failed`
- `unverified`
- `needs_review`

最小模型：

```text
主张 -> 证据 -> 验证器 -> 结论
```

## 实现

VerifyTrail 使用 Python 3.11+ 开发，并以 JSON 作为语言无关的数据边界。

项目有意保持精简。贡献者与 Agent 指引见 [AGENTS.md](AGENTS.md)。
