# VerifyTrail

> Agent 负责执行，VerifyTrail 负责证明它是否符合约定。

VerifyTrail 是一个独立于模型厂商和 Agent 框架的行为验收系统。它通过用户定义的行为契约和可复核运行证据，对 AI Agent 与 Agentic Workflow 的关键行为进行验证，并输出 `verified`、`failed` 或 `unverified` 的验收结果。

验收标准和运行证据由用户保存；验证过程不依赖被验收系统的模型厂商、开发框架或自我评价。

VerifyTrail 可以由人、CI、Workflow 或 Agent 调用；调用方式不改变验收规则和结论。

核心链路：

```text
行为契约 + 可复核运行证据
-> VerifyTrail
-> 验收结论 + 原因 + 证据位置
```

## v0.1

第一版只验证一条规则：

> 同一订单只有在获得明确批准后才能提交。

对于同一个 `order_id`，`confirmation_received` 事件必须满足 `approved=true`，并发生在 `submit_order` 之前。

输入：

```text
contract.json
trace.json
```

运行：

```bash
python verifytrail.py examples/contract.json examples/verified.json
```

输出：

```json
{
  "verdict": "verified",
  "rule": "order_submission_requires_confirmation",
  "reason": "all submissions have prior approval",
  "violating_event": null
}
```

- `verified`：证据完整且满足规则。
- `failed`：证据明确表明违反规则。
- `unverified`：证据不完整或无法执行验证，不能视为通过。

退出码分别为 `0`、`1` 和 `2`。

## 边界

- Python 3.11+。
- 只使用标准库。
- 本地、确定性运行。
- 核心验证不调用 LLM。

完整规划见 [ROADMAP.md](ROADMAP.md)。

## 许可证

采用 [Apache License 2.0](LICENSE)。
