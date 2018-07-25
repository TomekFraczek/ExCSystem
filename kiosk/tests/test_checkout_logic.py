from django.test import TestCase
from django.utils.timezone import timedelta
from django.core.exceptions import ValidationError

from core.models.MemberModels import Member
from core.models.DepartmentModels import Department
from core.models.GearModels import Gear
from core.models.TransactionModels import Transaction
from kiosk.CheckoutLogic import do_checkout, do_checkin

from buildPermissions import build_all as build_permissions

ADMIN_RFID = '0000000000'
MEMBER_RFID = '0000000001'


class CheckoutLogicTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        build_permissions()

    def setUp(self):
        Member.objects.create_superuser(
            'john@bro.com',
            ADMIN_RFID,
            'pass'
        )

        member = Member.objects.create_member(
            email='testemail@test.com',
            rfid=MEMBER_RFID,
            membership_duration=timedelta(days=7),
            password='password'
        )

        member.status = 3
        member.save()

        department = Department.objects.create(name='Camping', description='oops')

        _, gear = Transaction.objects.add_gear(
            authorizer_rfid=ADMIN_RFID,
            gear_rfid='0123456789', 
            gear_name='testbag', 
            gear_department=department
        )

    def test_checkout_gear(self):
        gear = Gear.objects.get(rfid='0123456789')
        self.assertEqual(gear.is_available(), True)
        do_checkout(ADMIN_RFID, MEMBER_RFID, gear.rfid)
        gear = Gear.objects.get(rfid='0123456789')
        self.assertEqual(gear.is_rented_out(), True)

    def test_checkout_to_unauthorized_member(self):
        member = Member.objects.get(rfid=MEMBER_RFID)
        member.status = 0
        member.save()
        gear = Gear.objects.get(rfid='0123456789')
        self.assertEqual(gear.is_available(), True)
        with self.assertRaises(ValidationError):
            do_checkout(ADMIN_RFID, MEMBER_RFID, gear.rfid)
        gear = Gear.objects.get(rfid='0123456789')
        self.assertEqual(gear.is_rented_out(), False)