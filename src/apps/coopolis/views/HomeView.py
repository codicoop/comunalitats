from apps.coopolis.views import LoginSignupContainerView


class HomeView(LoginSignupContainerView):
    template_name = "home.html"
