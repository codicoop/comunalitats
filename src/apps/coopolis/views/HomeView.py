from apps.cc_users.views import LoginSignupContainerView


class HomeView(LoginSignupContainerView):
    template_name = "home.html"
