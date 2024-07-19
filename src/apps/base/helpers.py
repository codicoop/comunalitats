def add_justification_required_text_to_field(
        field,
        text="Dada necessària per la justificació.",
):
    if hasattr(field, 'help_text') and field.help_text:
        text = f"{field.help_text} {text}"
    field.help_text = text
    return field
