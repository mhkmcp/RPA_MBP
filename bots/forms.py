from django import forms


class EmailConfigForm(forms.Form):
    email_config = forms.EmailField(label="Email Address")


class NidConfigForm(forms.Form):
    nid_url = forms.URLField()
    nid_username = forms.CharField()
    nid_password = forms.CharField()


class CbsConfigForm(forms.Form):
    cbs_url = forms.URLField()
    cbs_username = forms.CharField()
    cbs_password = forms.CharField()
