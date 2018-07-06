from wagtail.documents.models import (
    Document as WagtailDocument, AbstractDocument)


class CustomDocument(AbstractDocument):
    admin_form_fields = WagtailDocument.admin_form_fields
