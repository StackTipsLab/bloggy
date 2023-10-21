from django.shortcuts import render


def handler_404(request, exception):
    context = {
        'seo_title': "404 Page not found",
        'errorCode': '404.',
        'errorMessage': "Oops! That's an error.",
        'errorDescription': "The requested URL was not found on this server."
    }
    return render(request, 'errors/404.html', context)


def handler_500(request):
    context = {
        'seo_title': "500 Server error",
        'errorCode': '500.',
        'errorMessage': "Oops! That's an error.",
        'errorDescription': "The server encountered an error and couldn't complete your request."
    }
    return render(request, 'errors/500.html', context)
