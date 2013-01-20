from django import forms

class UserSettingsForm(forms.Form):
    """ Enables user to customize settings
    """
    LANGUAGE_RANGES = (
            ('en', 'English'),
            ('el', 'Greek'),
    )
    preferred_language = forms.ChoiceField(choices=LANGUAGE_RANGES)
