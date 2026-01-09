# Building Agentic Systems with Claude

Reference guide based on [Anthropic's Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) documentation.

## Core Philosophy

The most successful implementations use **simple, composable patterns** rather than complex frameworks. Build the right system for your needs, not the most sophisticated one.

> "Agentic systems often trade latency and cost for better task performance. When increased complexity is warranted, start simple and add complexity only when needed."

## Workflows vs Agents

| Type | Description | Best For |
|------|-------------|----------|
| **Workflows** | LLMs orchestrated through predefined code paths | Well-defined tasks, predictability |
| **Agents** | LLMs dynamically direct their own processes and tool usage | Flexibility, model-driven decisions |

## Six Composable Patterns

### 1. Prompt Chaining
Decompose tasks into sequential steps where each LLM call processes the previous output.

- **Trade-off**: Latency for accuracy
- **Use when**: Task has fixed, well-defined subtasks
- **Example**: Generate outline → Write sections → Edit for consistency

### 2. Routing
Classify inputs and direct them to specialized handlers.

- **Use when**: Distinct categories need different handling
- **Example**: Customer support → Route to billing/technical/general handlers

### 3. Parallelization
Run tasks simultaneously through:
- **Sectioning**: Independent subtasks processed in parallel
- **Voting**: Multiple attempts for higher confidence

### 4. Orchestrator-Workers
Central LLM dynamically breaks down tasks and delegates to specialized workers.

- **Use when**: Subtask requirements are unpredictable
- **Example**: Coding agent that spawns file search, edit, and test workers

### 5. Evaluator-Optimizer
One LLM generates responses while another provides iterative feedback.

- **Use when**: Clear evaluation criteria exist
- **Example**: Code generation with separate review/improvement loop

### 6. Autonomous Agents
LLMs using environmental feedback loops for extended, multi-turn operations.

- **Requires**: High trust, robust error handling
- **Pattern**: Gather context → Take action → Verify work → Repeat

## Tool Development Best Practices

Invest in agent-computer interfaces (ACI) like you would human-computer interfaces:

1. **Provide sufficient context** for the model to "think"
2. **Keep formats natural** to how text appears on the internet
3. **Minimize formatting overhead** in tool inputs/outputs
4. **Use poka-yoke principles** - design tools to prevent mistakes
5. **Return clear errors** that help the model self-correct

## Three Core Principles

1. **Simplicity** - Start with the simplest solution that could work
2. **Transparency** - Use explicit planning steps the user can observe
3. **Documentation and Testing** - Treat agent interfaces like production code

## Model Selection (2025)

| Model | Best For | Latency |
|-------|----------|---------|
| **Claude Sonnet 4.5** | Complex agents, coding tasks | Fast |
| **Claude Haiku 4.5** | High-volume, latency-sensitive | Fastest |
| **Claude Opus 4.5** | Maximum intelligence, reasoning | Moderate |

All models support 200K context, 64K output, extended thinking, and vision.

## Resources

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Agent Skills](https://www.anthropic.com/news/skills)
