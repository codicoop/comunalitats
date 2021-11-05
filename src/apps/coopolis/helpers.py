from django.conf import settings


def get_subaxis_choices():
    choices = [
        (None, '---------')
    ]
    for axis in sorted(settings.SUBAXIS_OPTIONS):
        for subaxis in sorted(settings.SUBAXIS_OPTIONS[axis]):
            choices.append(
                (subaxis[0], subaxis[1])
            )
    return choices
