from corehq.apps.app_manager.models import get_app, ApplicationBase, Form

def get_form_list(domain):
    form_list = []
    for app in ApplicationBase.view("app_manager/applications_brief", startkey=[domain], endkey=[domain, {}]):
        latest_app = get_app(domain, app._id, latest=True)
        if latest_app.doc_type == "Application":
            lang = latest_app.langs[0]
            for m in latest_app.get_modules():
                for f in m.get_forms():
                    try:
                        module_name = m.name[lang]
                    except Exception:
                        module_name = m.name.items()[0][1]
                    try:
                        form_name = f.name[lang]
                    except Exception:
                        form_name = f.name.items()[0][1]
                    form_list.append({"code" :  f.unique_id, "name" : app.name + "/" + module_name + "/" + form_name})
    return form_list

def get_sample_list(domain):
    #Circular import
    from corehq.apps.reminders.models import SurveySample
    
    sample_list = []
    for sample in SurveySample.view("reminders/sample_by_domain", startkey=[domain], endkey=[domain, {}], include_docs=True):
        sample_list.append({"code" : sample._id, "name" : sample.name})
    return sample_list

def get_form_name(form_unique_id):
    form = Form.get_form(form_unique_id)
    app = form.get_app()
    module = form.get_module()
    lang = app.langs[0]
    try:
        module_name = module.name[lang]
    except Exception:
        module_name = module.name.items()[0][1]
    try:
        form_name = form.name[lang]
    except Exception:
        form_name = form.name.items()[0][1]
    return app.name + "/" + module_name + "/" + form_name


# form django 1.3, removed in 1.5
class DotExpandedDict(dict):
    """
    A special dictionary constructor that takes a dictionary in which the keys
    may contain dots to specify inner dictionaries. It's confusing, but this
    example should make sense.

    >>> d = DotExpandedDict({'person.1.firstname': ['Simon'], \
            'person.1.lastname': ['Willison'], \
            'person.2.firstname': ['Adrian'], \
            'person.2.lastname': ['Holovaty']})
    >>> d
    {'person': {'1': {'lastname': ['Willison'], 'firstname': ['Simon']}, '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}}
    >>> d['person']
    {'1': {'lastname': ['Willison'], 'firstname': ['Simon']}, '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}
    >>> d['person']['1']
    {'lastname': ['Willison'], 'firstname': ['Simon']}

    # Gotcha: Results are unpredictable if the dots are "uneven":
    >>> DotExpandedDict({'c.1': 2, 'c.2': 3, 'c': 1})
    {'c': 1}
    """
    def __init__(self, key_to_list_mapping):
        for k, v in key_to_list_mapping.items():
            current = self
            bits = k.split('.')
            for bit in bits[:-1]:
                current = current.setdefault(bit, {})
                # Now assign value to current position
            try:
                current[bits[-1]] = v
            except TypeError: # Special-case if current isn't a dict.
                current = {bits[-1]: v}
