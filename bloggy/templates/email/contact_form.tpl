{% extends "mail_templated/base.tpl" %}

{% block subject %}
Contact form
{% endblock %}

{% block body %}

{% endblock %}

{% block html %}
<p><strong>Name:</strong> {{ name }}</p>
<p><strong>Website:</strong> {{ website }}</p>
<p><strong>Email:</strong> {{email}}</p>
<p><strong>Message:</strong> {{message}}</p>
{% endblock %}