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


def get_subaxis_for_axis(axis: str) -> list:
    subaxis_tuples = settings.SUBAXIS_OPTIONS.get(axis)
    if subaxis_tuples:
        subaxis_list = [x[0] for x in subaxis_tuples]
    return subaxis_list
