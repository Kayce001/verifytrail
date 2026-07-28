# VerifyTrail

面向 Tool-calling Agent 的行为回归验证工具。

修改模型或 Prompt 后，VerifyTrail 用运行证据判断 Agent 的关键行为是否发生危险退化。

核心链路：

```text
记录运行
-> 可控重放
-> 验证不变量
-> 比较行为
-> 定位关键分叉
```

项目目前处于 `v0.1` 设计与最小原型阶段。第一版只验证一个问题：

> Agent 是否在未获得确认的情况下执行了提交操作？

第一版接收 JSON Trace，检查关键工具调用的先后关系，并输出：

- `verified`
- `failed`
- `unverified`

## 实现

- Python 3.11+
- JSON 数据边界
- 本地优先

完整规划见 [ROADMAP.md](ROADMAP.md)。

## 许可证

采用 [Apache License 2.0](LICENSE)。
