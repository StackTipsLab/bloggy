# import logging
#
# from django.urls import reverse
# from django.utils.text import slugify
# from django.views.generic import RedirectView
#
# logger = logging.getLogger(__name__)
#
#
# class OldTutorialsHomeRedirectView(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         self.permanent = True
#         return "/articles"
#
#
# class OldTagArchiveRedirectView(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         self.permanent = True
#         return reverse("categories")
#
#
# class OldCategoryDetailsRedirectView(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         self.permanent = True
#         return reverse("categories_single", kwargs={"slug": kwargs["category"]})
#
#
# class AuthorRedirectView(RedirectView):
#     def format_username(self, username):
#         username = slugify(username.replace(".", "_").lower())
#         return username.replace("-", "_")
#
#     def get_redirect_url(self, *args, **kwargs):
#         self.permanent = True
#         username = self.format_username(kwargs["user"])
#         return reverse("user_profile", kwargs={"username": username})
