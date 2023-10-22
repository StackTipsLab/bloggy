from django.http import HttpRequest

from bloggy import settings


def seo_attrs(request: HttpRequest):
    """returns seo attributes to be merged into the context
    Arguments:
        request {HttpRequest} -- request object
    """

    seo = {
        'seo_site_name': settings.SITE_TITLE,
        'seo_title': settings.SITE_TAGLINE,
        'seo_description': 'Elevate your coding skills with StackTips. Learn through articles, courses, and quizzes on StackTips',
        'seo_keywords': 'stacktips, stack tips, python course, java tutorials, spring tutorials, spring boot tutorials, maven course for bignners, practice quiz, aws practice quiz, aws practice test',
        'og_image': '',
        'seo_image': settings.SITE_LOGO
    }

    if request.path == "/quizzes":
        seo["seo_title"] = "Interactive Quizzes"
        seo['seo_description'] = "Use bloggy to test your coding skills and gauge your learning progress in a fun way"
        seo['seo_keywords'] = 'stacktips quizzes, stack tips bloggy, quizlzet, take a quiz, practice test, aws quiz, python test, advance python test, aws practitioner test, CLF-C01 AWS test, aws CLF-C01 quiz'

    elif request.path == "/courses":
        seo["seo_title"] = "Courses"
        seo['seo_description'] = "StackTips offers free Programming Courses to teach you the fundamentals of popular programming languages such as Java, Python, HTML, JavaScript and CSS"
        seo['seo_keywords'] = 'stacktips courses, stack tips courses, free courses, learn python for free, python course, maven for beginner, maven courses, maven basics courrse'

    elif request.path == "/articles":
        seo["seo_title"] = "Tutorials"
        seo['seo_description'] = "Learn from beginner basics to advanced tutorials on Java, Spring, Python, Android and Git."
        seo['seo_keywords'] = 'stacktips tutorials, stack tips, free tutorials, java tutorials, spring tutorials, spring boot tutorials, django tutorials, python tutorials, git tutorials, maven tutorials, android tutorials '

    elif request.path == "/topics":
        seo["seo_title"] = "Categories"
        seo['seo_description'] = "Browse from collection of tutorials and courses organized by categories to make learning easy and accessible."
        seo['seo_keywords'] = "stacktips categories, stack tips topics, browse by topics, stacktips categories, tutorial categories, tutorial categories, all tutorials by category, android, django, python, django, spring, spring boot, git"

    elif request.path == "/cookie-policy":
        seo["seo_title"] = "Cookie policy"
        seo['seo_description'] = "Our Cookies Policy explains what Cookies are and how We use them."

    elif request.path == "/privacy":
        seo["seo_title"] = "Privacy policy"
        seo['seo_description'] = "This page explains our privacy policy"

    elif request.path == "/terms-of-service":
        seo["seo_title"] = "Terms of service"
        seo['seo_description'] = "This page outlines the legal terms of stacktips.com, its sub-domains, and all associated web and/or mobile apps."

    elif request.path == "/comment-policy":
        seo["seo_title"] = "Comment policy"
        seo['seo_description'] = "This page lists some of the simple ground rules for commenting on this site"

    elif request.path == "/contact":
        seo["seo_title"] = "Get in touch"
        seo['seo_description'] = "If you have any questions or have suggestions to improve the quality, let us know."

    elif request.path == "/about":
        seo["seo_title"] = "About us"
        seo['seo_description'] = "We aim to provide developer-friendly ways to learn programming. With articles, programming course, and quizzes, we aim to teach in the ways developers learn best."

    elif request.path == "/guestbook":
        seo["seo_title"] = "Guestbook"
        seo['seo_description'] = "You have a chance to be creative. Indulge me by leaving a greeting below."

    elif request.path == "/newsletter":
        seo["seo_title"] = "Newsletter"
        seo['seo_description'] = "Get access to our fortnightly newsletter with articles, courses, and quizzes. You may unsubscribe at any time using the link in our newsletter."

    elif request.path == "/login":
        seo["seo_title"] = "Login"
        seo['seo_description'] = "To keep connected with us, please log in with your email address and account password."
        seo['seo_keywords'] = "stacktips account, login to stacktips, join stacktips, your stack tips account, join for free, login, sign in, login stack tips, signin to stacktips.com, login to stacktips"

    elif request.path == "/register":
        seo["seo_title"] = "Create your free account!"
        seo['seo_description'] = "Register to get exclusive access to articles, live-demos, or courses, We aim to teach in the ways developers learn best."
        seo['seo_keywords'] = "stacktips account, create free stacktips account, signup new account, free account, stack tips account free, join stacktips, stacktips free account, register free account, new account stack tips"

    elif request.path == "/authors":
        seo["seo_title"] = "Our Authors @ StackTips"
        seo['seo_description'] = "List of the authors on StackTips website."

    return seo


def app_settings(request: HttpRequest):
    return {
        "DEVELOPMENT_MODE": settings.DEVELOPMENT_MODE,
        "ASSETS_DOMAIN": settings.ASSETS_DOMAIN
    }
