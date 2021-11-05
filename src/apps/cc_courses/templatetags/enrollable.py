from django import template


def is_enrolled(enrollable, individual):
    return individual in enrollable.enrolled.all()


register = template.Library()
register.filter('is_enrolled', is_enrolled)
