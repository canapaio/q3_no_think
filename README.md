# No Think Plugin for The Cat (Qwen3) v0.0.1.002

This plugin is designed to suppress and clean internal thinking steps (e.g., `Thinking: ...`) from the responses of language models like **Qwen3**, ensuring that users only receive the final result without seeing the model's reasoning process.

It also allows you to prepend a `/no_think` command to user messages, so the LLM avoids generating verbose internal thoughts in the first place.

---

## 🎯 Purpose

This plugin helps:
- Prepend `/no_think` to incoming messages (Qwen3)
- Strip `/no_think` before storing in memory or recalling (Qwen3)
- Remove internal thinking blocks <think> Thinking: ... Result </think> (like `Thinking: ... Result:`) from the final output sent to the user (all R models)

This is especially useful when working with models like **Qwen3**, which may use special patterns or prefixes to indicate internal thought processes.

---

## 🔧 Features

### 1. `before_cat_reads_message`
Prepends `/no_think` to the message text if enabled in settings.

```python
user_message_json["text"] = "/no_think" + user_message_json["text"]
```

### 2. `before_cat_stores_episodic_memory`
Removes the `/no_think` prefix before saving the message into episodic memory.

```python
doc['page_content'] = doc['page_content'][len('/no_think'):]
```

### 3. `before_cat_sends_message`
Strips out any internal thinking blocks using regex from the final response.

```python
message["content"] = re.sub(r'<think>.*?</think>', '', message["content"], flags=re.DOTALL | re.IGNORECASE)
```

> This hides internal steps like:
> ```
> Thinking: I need to find a good joke.
> Result: Why don't scientists trust atoms? Because they make up everything!
> ```

### 4. `cat_recall_query`
Removes `/no_think` before performing memory recall, ensuring clean queries.

```python
user_message = user_message[len('/no_think'):]
```

---

## ⚙️ Settings

In your plugin configuration, define the following boolean settings:
- `No_Think`: If `True`, adds `/no_think` to the start of each user input.
- `Remove_Think`: If `True`, removes internal thinking blocks from the model’s output.

---

## ✅ Example Use Case

With `No_Think=True`, a user message:

```
Tell me a joke
```

Becomes:

```
/no_think Tell me a joke
```

If Qwen3 returns:

```
<think> 
Let me think of a joke...
</think>
Why did the scarecrow win an award? Because he was outstanding in his field!
```

The plugin will send just this to the user:

```
Why did the scarecrow win an award? Because he was outstanding in his field!
```

---

## 🧪 Compatibility

- Tested with **Qwen3**
- Can be adapted for other LLMs that use similar internal thinking markers (e.g., `Thinking:`, `Thought:`, etc.)
