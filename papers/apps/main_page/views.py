# -*- coding: utf-8 -*-


from django.shortcuts import render_to_response, \
    get_object_or_404, HttpResponse
from django.template import RequestContext
from .base import ContactBaseView, ContactParamsValidatorMixin
from .models import Agency, Contact, ContactSettings
from settings import CONTACT_ORG_QUERY


class ContactView(ContactBaseView, ContactParamsValidatorMixin):

    """ Class for view contact page.
    """

    CONTACT_ORG_QUERY = CONTACT_ORG_QUERY

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'org_requisite_s': None,
            'agency_s': None
        }
        super(ContactView, self).__init__(*args, **kwargs)

    def _get_org_requisite_s(self):
        self.org_requisite_s = self.CONTACT_ORG_QUERY.all()

    def _get_agency_s(self):
        self._agency_s = Agency.objects.all()

    def _get_contact(self):
        self._contact = Contact.objects.all()

    def get(self, *args, **kwargs):
        self._get_org_requisite_s()
        self._get_agency_s()
        self._get_contact()
        self._aggregate()
        return render_to_response(
            '',
            self.output_context,
            context_instance=RequestContext(self.request), )