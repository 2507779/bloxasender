import random

class TemplateManager:
    def __init__(self):
        self.templates = {}

    def add_template(self, name, content):
        self.templates[name] = content

    def get_randomized_message(self, template_name, recipient_data):
        template = self.templates.get(template_name, "")
        try:
            return template.format(name=recipient_data.get("name", ""), tags=",".join(recipient_data.get("tags", [])))
        except KeyError:
            return template
