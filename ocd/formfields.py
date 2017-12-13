from django import forms


class HTMLArea(forms.Textarea):
    template_name = 'floppyforms/htmlarea.html'

    def __init__(self, attrs=None):
        default_attrs = {'cols': '40', 'rows': '4'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class OCSplitDateTime(forms.SplitDateTimeWidget):
    template_name = 'ocforms/widgets/splitdatetime.html'


class OCCheckboxSelectMultiple(forms.SelectMultiple):
    template_name = 'floppyforms/oc_checkbox_select.html'


class OCIssueRadioButtons(forms.RadioSelect):
    template_name = 'floppyforms/oc_issue_radio_buttons.html'


class OCProposalRadioButtons(forms.RadioSelect):
    template_name = 'floppyforms/oc_proposal_radio_buttons.html'


class OCTextInput(forms.TextInput):
    template_name = 'ocforms/widgets/text.html'

    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class OCDateInput(forms.DateInput):
    template_name = 'ocforms/widgets/date.html'


class OCTimeInput(forms.TimeInput):
    template_name = 'ocforms/widgets/time.html'


class OCSelect(forms.Select):
    template_name = 'ocforms/widgets/select.html'
