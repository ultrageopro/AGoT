# Prompt Pipeline

The term **"use for prompting"** implies that each function—$T_\emptyset$, $T_0$, $T_e$, $C$, $Eval$, and $Φ$—within the AGoT algorithm represents a distinct invocation of the LLM with a specific prompt that instructs it on the required task. Below is an overview of the process:

### 1. Thought-generation functions (`t_empty`, `t_0`, `t_general`)
- A prompt is formulated, such as:
  *“Given the task: {q}. Formulate up to {nmax} key sub-tasks and describe (briefly) how to solve them.”*
- The LLM responds with a list of sub-tasks and a concise strategy.
- These sub-tasks are then converted into graph nodes.

### 2. Complexity check (`is_complex`)
- A separate prompt is used:
  *“Here is a sub-task `{thought}`. Is it complex enough to require its own nested graph? Answer 1 (yes) or 0 (no).”*
- Alternatively, the LLM may be prompted to analyze its response, potentially indicating the need for further decomposition.

### 3. Thought evaluation (`evaluate_thought`)
- A prompt is structured as:
  *“Here is your current sub-task: `{thought}`. Using the context {a snippet or link to the current state of the graph}, formulate a brief answer.”*
- The LLM generates a response that serves as a solution to the sub-task, which is then stored in the corresponding graph node.

### 4. Final thought selection (`final_thought_selector`)
- A prompt or internal logic is used:
  *“Out of all the nodes {…}, which thought is ‘final’ in the context of the original question?”*
  Alternatively, the process determines which node ultimately resolves the task.

### 5. Main function (`AGoT`)
- This function orchestrates the execution of all LLM sub-functions with appropriate prompts, builds the graph, recursively initiates nested graphs (if a thought is complex), and ultimately returns the final answer.

Article: [AGoT](https://arxiv.org/pdf/2502.05078v1)
