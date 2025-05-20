from cat.mad_hatter.decorators import tool, hook, plugin
import re


@hook(priority=-10)
def before_cat_reads_message(user_message, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    user_message["text"] = "/no_think" + user_message["text"]
    return user_message

@hook(priority=-10)
def before_cat_sends_message(message, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    message = re.sub(r'<think>.*?</think>', '', message["content"])
    return message
