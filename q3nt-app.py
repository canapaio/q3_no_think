from cat.mad_hatter.decorators import tool, hook, plugin
import re


@hook(priority=10)
def before_cat_reads_message(user_message_json, cat):
    """
    Hook executed before the cat reads a user message.
    Adds '/no_think' prefix to user messages when No_Think setting is enabled.
    This prevents the message content from being stored in the vector database.
    Supports dynamic override with :n1: (enable) and :n0: (disable) commands.
    """
    settings = cat.mad_hatter.get_plugin().load_settings()
    message_text = user_message_json["text"]
    
    # Check for dynamic override commands
    no_think_override = None
    if ":n1:" in message_text:
        no_think_override = True
        message_text = message_text.replace(":n1:", "")
    elif ":n0:" in message_text:
        no_think_override = False
        message_text = message_text.replace(":n0:", "")
    
    # Apply no_think logic based on override or settings
    should_apply_no_think = no_think_override if no_think_override is not None else settings['No_Think']
    
    if should_apply_no_think:
        user_message_json["text"] = "/no_think" + message_text
    else:
        user_message_json["text"] = message_text
    
    return user_message_json

@hook(priority=10)
def before_cat_stores_episodic_memory(doc, cat):
    """
    Hook executed before storing episodic memory.
    Removes '/no_think' prefix from document content before storing in memory
    to ensure clean storage without the control prefix.
    Also removes any remaining :n0: or :n1: commands from stored content.
    """
    if doc.page_content.startswith('/no_think'):
        doc.page_content = doc.page_content[len('/no_think'):]
    
    # Clean up any remaining override commands
    doc.page_content = doc.page_content.replace(":n1:", "").replace(":n0:", "")
    
    return doc

@hook(priority=10)
def before_cat_sends_message(message, cat):
    """
    Hook executed before the cat sends a message to the user.
    Removes <think>...</think> tags from the message content when Remove_Think setting is enabled.
    This ensures thinking processes are not visible in the final response.
    """
    settings = cat.mad_hatter.get_plugin().load_settings()
    if settings['Remove_Think']:
        message.content = re.sub(r'<think>.*?</think>', '', message.content, flags=re.DOTALL | re.IGNORECASE)
    return message

@hook(priority=10)
def cat_recall_query(user_message, cat):
    """
    Hook executed during memory recall queries.
    Removes '/no_think' prefix from user messages during recall operations
    to ensure proper matching with stored memories.
    Also cleans up any override commands for proper recall matching.
    """
    if user_message.startswith('/no_think'):
        user_message = user_message[len('/no_think'):]
    
    # Clean up any override commands for proper recall
    user_message = user_message.replace(":n1:", "").replace(":n0:", "")
    
    return user_message