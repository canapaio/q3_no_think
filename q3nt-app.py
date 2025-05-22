from cat.mad_hatter.decorators import tool, hook, plugin
import re


@hook(priority=10)
def before_cat_reads_message(user_message_json, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    if settings['No_Think']:
        user_message_json["text"] = "/no_think" + user_message_json["text"]
    return user_message_json

@hook(priority=10)
def before_cat_stores_episodic_memory(doc, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    if settings['No_Think']:
        if doc['page_content'].startswith('/no_think'):
            doc['page_content'] = doc['page_content'][len('/no_think'):]    
    return doc

@hook(priority=10)
def before_cat_sends_message(message, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    if settings['Remove_Think']:
        settings = cat.mad_hatter.get_plugin().load_settings()
        message["content"] = re.sub(r'<think>.*?</think>', '', message["content"], flags=re.DOTALL | re.IGNORECASE)
    return message

@hook(priority=10)
def cat_recall_query(user_message, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    if settings['No_Think']:
        if user_message.startswith('/no_think'):
            user_message = user_message[len('/no_think'):]    
    return new_query