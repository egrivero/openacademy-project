# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_session(self):
        return self.env['openacademy.session'].browse(
                self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session',
        string="Sessions", required=True, default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.multi
    def subscribe(self):
        for session_id in self.session_ids:
            session_id.attendee_ids |= self.attendee_ids
        return {}
