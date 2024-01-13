from django.forms import ClearableFileInput
class NonClearableFileInput(ClearableFileInput):
    template_name = 'forms/widgets/non_clearable_imagefield.html'
