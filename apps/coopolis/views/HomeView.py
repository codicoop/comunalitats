from coopolis.views import LoginSignupContainerView


class HomeView(LoginSignupContainerView):
    template_name = "home.html"
    extra_context = {
        'courses_title': "Formació i activitats",
        'courses_text': "TEXT D'INTRODUCCIÓ A LES FORMACIONS QUE FEM",
        'projects_title': "Acompanyament de projectes",
        'projects_text': "TEXT D'INTRODUCCIÓ A L'ACOMPANYAMENT DE PROJECTES"
    }
