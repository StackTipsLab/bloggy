import os
from urllib import request

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, FormView

from bloggy.forms.edit_profile_form import EditProfileForm
from bloggy.models import MyUser
from bloggy.templatetags.custom_widgets import sanitize_url


class EditProfileView(FormView):
    template_name = "profile/edit_profile.html"
    model = MyUser
    form_class = EditProfileForm

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        context['seo_title'] = "Update Profile"
        context['seo_description'] = "Update my profile. You need a StackTips account to sign in and view your profile."
        context['seo_image'] = "https://media.stacktips.com/static/media/logo.png"
        return context

    def get_initial(self):
        initial = super(EditProfileView, self).get_initial()
        username = self.request.user.username
        user = get_object_or_404(MyUser, username=username)

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
            MyUser.objects.filter(username=self.request.user.username).update(
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
            MyUser.objects.filter(username=self.request.user.username).update(
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
        file_path = f'media/' + media_path

        # if settings.USE_SPACES:
        #     # if image_type == 'private':
        #     #     upload = UploadPrivate(file=image_file)
        #     # else:
        #     upload = Media(file=image)
        #     upload.save()
        #     image_url = upload.file.url
        # else:
        if not os.path.exists(file_path):
            # This will ensure that the path is created properly and will raise exception if the directory
            # already exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Create image save path with title
        with open(file_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        return media_path
