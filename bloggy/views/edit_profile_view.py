import os

from django.shortcuts import get_object_or_404
from django.template.context_processors import static
from django.views.generic import FormView

from bloggy import settings
from bloggy.forms.edit_profile_form import EditProfileForm
from bloggy.models import User
from bloggy.templatetags.custom_widgets import sanitize_url


class EditProfileView(FormView):
    template_name = "profile/edit_profile.html"
    model = User
    form_class = EditProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = "Update Profile"
        context[
            'meta_description'] = f"Update my profile. You need a {settings.SITE_TITLE}  account to sign in and view your profile."
        context['meta_image'] = static('static/media/logo.png')
        return context

    def get_initial(self):
        initial = super().get_initial()
        username = self.request.user.username
        user = get_object_or_404(User, username=username)

        # update initial field defaults with custom set default values:
        initial.update({
            'profile_photo': user.profile_photo,
            'username': user.username,
            'name': user.name,
            'bio': user.bio,
            'website': user.website,
            'linkedin': user.linkedin,
            'twitter': user.twitter,
            'youtube': user.youtube,
            'github': user.github,
        })

        return initial

    def get_success_url(self):
        return self.request.get_full_path()

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        if self.request.FILES.get("profile_photo", None) is not None:
            # file_path = self.save_media_file(self.request.FILES["profile_photo"])
            User.objects.filter(username=self.request.user.username).update(
                profile_photo=self.request.FILES["profile_photo"],
                name=form.cleaned_data["name"],
                bio=form.cleaned_data["bio"],
                website=sanitize_url(form.cleaned_data["website"]),
                twitter=sanitize_url(form.cleaned_data["twitter"]),
                youtube=sanitize_url(form.cleaned_data["youtube"]),
                linkedin=sanitize_url(form.cleaned_data["linkedin"]),
                github=sanitize_url(form.cleaned_data["github"])
            )
        else:
            User.objects.filter(username=self.request.user.username).update(
                name=form.cleaned_data["name"],
                bio=form.cleaned_data["bio"],
                website=sanitize_url(form.cleaned_data["website"]),
                twitter=sanitize_url(form.cleaned_data["twitter"]),
                youtube=sanitize_url(form.cleaned_data["youtube"]),
                linkedin=sanitize_url(form.cleaned_data["linkedin"]),
                github=sanitize_url(form.cleaned_data["github"])
            )

        return super().form_valid(form)

    def save_media_file(self, image):
        # This will generate random folder for saving your image using UUID
        media_path = f'uploads/user/{self.request.user.username}/{image.name}'
        file_path = f'media/{media_path}'

        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Create image save path with title
        with open(file_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        return media_path
