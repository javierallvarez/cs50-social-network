-La clase e id comment-div esta definida en models.py/forms

-Me deshago de bootstrap:
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

-Cambié el form class PostForm(ModelForm): por PostForm(forms.Form): tras experimentar ValueError: ModelForm has no model class specified.

-I added 'django.contrib.humanize' to my apps and {% load humanize %} to my template to get see the timestamp differently (ej. 'yesterday' or '2 hours ago')