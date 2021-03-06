# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class GlobalTestOpenAcademySession(TransactionCase):
    '''
    This create global test to sessions
    '''
    # Seudo-constructor method
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.course = self.env.ref('openacademy.course1')
        self.partner_vauxoo = self.env.ref('base.res_partner_23')
        self.partner_1 = self.env.ref('base.res_partner_1')

    # Generic methods

    # Test methods
    def test_10_instructor_is_attendee(self):
        '''
        Check that raise of 'A session's instructor can't be an attendee'
        '''
        with self.assertRaisesRegexp(
            ValidationError,
            "A session's instructor can't be an attendee"
        ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                'course_id': self.course.id
            })

    def test_20_wkf_done(self):
        '''
        Check that the workflow work fine!
        '''
        session_test = self.session.create({
            'name': 'Session test 1',
            'seats': 2,
            'instructor_id': self.partner_vauxoo.id,
            'attendee_ids': [(6, 0, [self.partner_1.id])],
            'course_id': self.course.id
        })
        # Check initial state
        self.assertEqual(
            session_test.state, 'draft', 'Initial state should be in "draft"')

        # Change next state and check it
        session_test.signal_workflow('button_confirm')
        self.assertEqual(
            session_test.state, 'confirmed',
            "Signal confirm don't work fine!")

        # Change next state and check it
        session_test.signal_workflow('button_done')
        self.assertEqual(
            session_test.state, 'done', "Signal done don't work fine!")
