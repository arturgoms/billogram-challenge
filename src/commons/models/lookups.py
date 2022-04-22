from django.db.models import Transform


class RemovePunctuation(Transform):  # noqa
    bilateral = True
    lookup_name = "remove_punctuation"
    function = "REGEXP_REPLACE"
    template = "%(function)s(%(expressions)s, '[^\\w\\s]', '', 'g')"
