class AutoReply:
    def __init__(self):
        self.enabled = False
        self.welcome_text = None
        self.filters: dict[str,str] = {}

    def should_reply(self, chat_type: str, text: str | None) -> str | None:
        if not self.enabled:
            return None
        if chat_type == "private" and text:
            for k, v in self.filters.items():
                if k.lower() in text.lower():
                    return v
            return self.welcome_text
        return None
