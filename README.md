No Think Plugin for Cat (Qwen3) v0.0.1.002

This plugin is designed to interact with The Cat AI framework , specifically to handle and modify messages before they are processed by or returned from the Qwen3 language model . 
🎯 Purpose 

This plugin allows you to: 

    Prepend /no_think to user input 
    Strip /no_think from memory storage 
    Remove internal thinking blocks (Thinking: ... or similar markers) from the final response 
    Modify query before recalling memories 
     

It is particularly useful when working with models like Qwen3 , which may use special tokens or patterns (like /think or Thinking:) to indicate internal reasoning steps that should not be shown to the user. 
🔧 Features 
1. before_cat_reads_message 

Adds /no_think at the beginning of a message if enabled in settings. This tells the model (e.g., Qwen3) not to generate internal thinking steps. 
python
 
 
1
user_message_json["text"] = "/no_thinking" + user_message_json["text"]
 
 
2. before_cat_stores_episodic_memory 

Removes the /no_think prefix before storing the message into memory, so it doesn't pollute history. 
python
 
 
1
doc['page_content'] = doc['page_content'][len('/no_think'):]
 
 
3. before_cat_sends_message 

Strips out any internal thinking blocks from the final response using regex, ensuring the user never sees them. 
python
 
 
1
message["content"] = re.sub(r'Thinking:.*?Result:', '', message["content"], flags=re.DOTALL)
 
 

    This hides internal reasoning steps like: 
     

     
    1
    2
    Thinking: Let me see...
    Result: Hello!
     
     
     

4. cat_recall_query 

Removes /no_think before performing memory recall, so the actual query is clean and effective. 
python
 
 
1
user_message = user_message[len('/no_think'):]
 
 
⚙️ Settings 

Make sure to define these two boolean settings in your plugin configuration: 

    No_Think: If True, prepends /no_think to the input.
    Remove_Think: If True, removes internal thinking blocks from the output.
     

✅ Example Use Case 

With No_Think=True, a user message like: 
 
 
1
Tell me a joke
 
 

Becomes: 
 
 
1
/no_think Tell me a joke
 
 

And if Qwen3 returns: 
 
 
1
2
Thinking: I need to find a good joke.
Result: Why don't scientists trust atoms? Because they make up everything!
 
 

The plugin will return just: 
 
 
1
Why don't scientists trust atoms? Because they make up everything!
 
 
🧪 Compatibility 

This plugin was tested with Qwen3 , but can be adapted for other LLMs that support similar "thinking suppression" via special tokens or prefixes. 
📦 Installation 

To install this plugin: 

    Place it inside your Cat AI plugins folder .
    Enable it through the Cat dashboard.
    Configure the settings accordingly.
     

