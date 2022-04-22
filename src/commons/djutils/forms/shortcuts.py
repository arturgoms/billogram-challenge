def get_form(request, form_cls, instance=None, **kwargs):
    """
    Returns a form instance from a given request.

    Args:
         request (Request, required): Http Request object.
         form_cls (django.forms.ModelForm, required): ModelForm class.
         instance (django.db.models.Model, optional): instance.
         kwargs (dict, optional): extra parameters.

    Returns:
        django.forms.ModelForm
    """
    if instance:
        kwargs["instance"] = instance

    if request.method in ("POST", "PUT"):
        kwargs.update({"data": request.POST, "files": request.FILES})

    return form_cls(**kwargs)
