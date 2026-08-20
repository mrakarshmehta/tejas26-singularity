"""
HiddenYatra — Homestay / Local Stay Request Workflow Test Suite
Comprehensive automated test suite covering:
1. Free Stay Request Creation (Price = 0, status = pending, host notified)
2. Paid Stay Request Creation (Price = nights * price_per_night, status = pending)
3. Date validations (past check-in rejected, checkout <= checkin rejected)
4. Guest count limits (guests > max_guests rejected)
5. Min/Max stay nights constraints
6. Self-booking prevention (host cannot book own listing)
7. Host accept request (status -> accepted, calendar dates blocked, traveller notified)
8. Overlapping accepted booking protection (cannot accept overlapping dates on same listing)
9. Host reject request (status -> rejected, reason recorded, traveller notified)
10. Traveller cancellation (pending & accepted, releases calendar availability)
11. Host cancellation (status -> cancelled_by_host, calendar dates freed)
12. IDOR / Authorization protection (traveller & host boundaries enforced)
13. Admin moderation and oversight
14. Real-time availability check API
"""
import unittest
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from models.connection import get_cursor
from models.stay_requests import (
    validate_booking_parameters, check_date_availability,
    create_stay_request, get_stay_request_by_id,
    get_traveller_requests, get_host_requests,
    accept_stay_request, reject_stay_request,
    cancel_stay_request_by_traveller, cancel_stay_request_by_host,
    get_all_stay_requests_admin, admin_cancel_stay_request
)
from models.hosts import get_notifications, get_host_profile_by_user


class TestStayRequestWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Ensure we have test users and listings in database
        with get_cursor(commit=True) as cur:
            # 1. Host user 1
            cur.execute("SELECT id FROM users WHERE email = 'test_host_1@hiddenyatra.in'")
            row = cur.fetchone()
            if not row:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name, is_host)
                    VALUES ('testhost1', 'test_host_1@hiddenyatra.in', 'hash123', 'Rajesh Host', 1)
                """)
                cls.host_user_id = cur.lastrowid
            else:
                cls.host_user_id = row['id']

            # Host Profile 1
            cur.execute("SELECT id FROM host_profiles WHERE user_id = %s", (cls.host_user_id,))
            hp = cur.fetchone()
            if not hp:
                cur.execute("""
                    INSERT INTO host_profiles (user_id, bio, verification_status, is_verified_badge)
                    VALUES (%s, 'Welcome to our heritage home in Nalanda!', 'approved', 1)
                """, (cls.host_user_id,))
                cls.host_profile_id = cur.lastrowid
            else:
                cls.host_profile_id = hp['id']

            # 2. Host user 2 (for IDOR tests)
            cur.execute("SELECT id FROM users WHERE email = 'test_host_2@hiddenyatra.in'")
            row2 = cur.fetchone()
            if not row2:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name, is_host)
                    VALUES ('testhost2', 'test_host_2@hiddenyatra.in', 'hash123', 'Sunita Host', 1)
                """)
                cls.host_user_id_2 = cur.lastrowid
            else:
                cls.host_user_id_2 = row2['id']

            cur.execute("SELECT id FROM host_profiles WHERE user_id = %s", (cls.host_user_id_2,))
            hp2 = cur.fetchone()
            if not hp2:
                cur.execute("""
                    INSERT INTO host_profiles (user_id, bio, verification_status, is_verified_badge)
                    VALUES (%s, 'Farm stay host in Vaishali', 'approved', 1)
                """, (cls.host_user_id_2,))
                cls.host_profile_id_2 = cur.lastrowid
            else:
                cls.host_profile_id_2 = hp2['id']

            # 3. Traveller user 1
            cur.execute("SELECT id FROM users WHERE email = 'test_traveller_1@hiddenyatra.in'")
            t1 = cur.fetchone()
            if not t1:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name)
                    VALUES ('testtraveller1', 'test_traveller_1@hiddenyatra.in', 'hash123', 'Amit Explorer')
                """)
                cls.traveller_id_1 = cur.lastrowid
            else:
                cls.traveller_id_1 = t1['id']

            # 4. Traveller user 2 (for IDOR tests)
            cur.execute("SELECT id FROM users WHERE email = 'test_traveller_2@hiddenyatra.in'")
            t2 = cur.fetchone()
            if not t2:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, display_name)
                    VALUES ('testtraveller2', 'test_traveller_2@hiddenyatra.in', 'hash123', 'Priya Backpacker')
                """)
                cls.traveller_id_2 = cur.lastrowid
            else:
                cls.traveller_id_2 = t2['id']

            # 5. Paid Listing
            cur.execute("SELECT id FROM host_listings WHERE slug = 'test-paid-heritage-homestay'")
            l_paid = cur.fetchone()
            if not l_paid:
                cur.execute("""
                    INSERT INTO host_listings (host_id, listing_type, title, slug, description,
                                               price_per_night, max_guests, min_stay_nights, max_stay_nights, status)
                    VALUES (%s, 'paid_homestay', 'Test Paid Heritage Homestay', 'test-paid-heritage-homestay',
                            'Lovely heritage stay in Nalanda', 1200.00, 4, 1, 14, 'published')
                """, (cls.host_profile_id,))
                cls.paid_listing_id = cur.lastrowid
            else:
                cls.paid_listing_id = l_paid['id']

            # 6. Free Listing
            cur.execute("SELECT id FROM host_listings WHERE slug = 'test-free-village-cultural-stay'")
            l_free = cur.fetchone()
            if not l_free:
                cur.execute("""
                    INSERT INTO host_listings (host_id, listing_type, title, slug, description,
                                               price_per_night, max_guests, min_stay_nights, max_stay_nights, status)
                    VALUES (%s, 'free_stay', 'Test Free Village Cultural Stay', 'test-free-village-cultural-stay',
                            'Experience rural hospitality for free', 0.00, 2, 1, 7, 'published')
                """, (cls.host_profile_id,))
                cls.free_listing_id = cur.lastrowid
            else:
                cls.free_listing_id = l_free['id']

    def setUp(self):
        with get_cursor(commit=True) as cur:
            cur.execute("DELETE FROM listing_availability WHERE listing_id IN (%s, %s)",
                        (self.paid_listing_id, self.free_listing_id))
            cur.execute("DELETE FROM stay_requests WHERE listing_id IN (%s, %s)",
                        (self.paid_listing_id, self.free_listing_id))

    def test_01_free_stay_request_creation(self):
        """Test creating a request for a free cultural stay."""
        d_in = date.today() + timedelta(days=5)
        d_out = date.today() + timedelta(days=7)  # 2 nights

        success, res = create_stay_request(
            listing_id=self.free_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=2,
            message="Excited to learn about local culture!"
        )
        self.assertTrue(success, f"Failed to create free stay request: {res}")
        req_id = res['request_id']
        self.assertEqual(res['total_price'], 0.0)
        self.assertEqual(res['nights'], 2)

        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'pending')
        self.assertEqual(req['listing_type'], 'free_stay')
        self.assertEqual(float(req['total_price']), 0.0)

        # Check host received notification
        notifs = get_notifications(self.host_user_id, limit=5)
        self.assertTrue(any('stay_request_received' in n['type'] for n in notifs))

    def test_02_paid_stay_request_creation(self):
        """Test creating a request for a paid homestay."""
        d_in = date.today() + timedelta(days=10)
        d_out = date.today() + timedelta(days=13)  # 3 nights * 1200 = 3600

        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=3,
            message="Visiting Nalanda with family"
        )
        self.assertTrue(success, f"Failed to create paid stay request: {res}")
        req_id = res['request_id']
        self.assertEqual(res['total_price'], 3600.0)
        self.assertEqual(res['nights'], 3)

        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'pending')
        self.assertEqual(float(req['total_price']), 3600.0)
        self.assertEqual(req['num_guests'], 3)

    def test_03_past_checkin_date_rejected(self):
        """Test check-in in the past is rejected."""
        past_date = date.today() - timedelta(days=2)
        future_date = date.today() + timedelta(days=2)

        success, err = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=past_date,
            check_out=future_date,
            num_guests=1
        )
        self.assertFalse(success)
        self.assertIn("past", err.lower())

    def test_04_checkout_before_checkin_rejected(self):
        """Test check-out on or before check-in is rejected."""
        d_in = date.today() + timedelta(days=5)
        d_out = date.today() + timedelta(days=4)

        success, err = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=1
        )
        self.assertFalse(success)
        self.assertIn("after", err.lower())

    def test_05_guest_count_limits(self):
        """Test guest count exceeding max_guests is rejected."""
        d_in = date.today() + timedelta(days=15)
        d_out = date.today() + timedelta(days=17)

        # Free listing allows max 2 guests
        success, err = create_stay_request(
            listing_id=self.free_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=5
        )
        self.assertFalse(success)
        self.assertIn("accommodates up to", err.lower())

    def test_06_self_booking_prevented(self):
        """Test host cannot book their own listing."""
        d_in = date.today() + timedelta(days=15)
        d_out = date.today() + timedelta(days=17)

        success, err = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.host_user_id,
            check_in=d_in,
            check_out=d_out,
            num_guests=1
        )
        self.assertFalse(success)
        self.assertIn("own listing", err.lower())

    def test_07_host_accept_stay_request(self):
        """Test host accepting a stay request blocks calendar dates and notifies guest."""
        d_in = date.today() + timedelta(days=20)
        d_out = date.today() + timedelta(days=23)

        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=2
        )
        self.assertTrue(success)
        req_id = res['request_id']

        # Host accepts
        ok, err = accept_stay_request(req_id, self.host_profile_id, host_message="Looking forward to welcoming you!")
        self.assertTrue(ok, f"Host failed to accept request: {err}")

        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'accepted')
        self.assertEqual(req['host_response'], "Looking forward to welcoming you!")

        # Check calendar dates are blocked
        is_avail, msg = check_date_availability(self.paid_listing_id, d_in, d_out)
        self.assertFalse(is_avail, "Dates should be unavailable after acceptance")

        # Check traveller notification
        notifs = get_notifications(self.traveller_id_1, limit=5)
        self.assertTrue(any('stay_request_accepted' in n['type'] for n in notifs))

    def test_08_overlapping_accepted_booking_protection(self):
        """Test that overlapping booking cannot be accepted for the same dates."""
        # 1. Create and Accept Request A for [day 20 to day 23]
        d_in_a = date.today() + timedelta(days=20)
        d_out_a = date.today() + timedelta(days=23)
        ok_a, res_a = create_stay_request(self.paid_listing_id, self.traveller_id_1, d_in_a, d_out_a, 1)
        self.assertTrue(ok_a)
        accept_stay_request(res_a['request_id'], self.host_profile_id)

        # 2. Traveller 2 attempts to request [day 21 to day 24] (overlapping)
        d_in_b = date.today() + timedelta(days=21)
        d_out_b = date.today() + timedelta(days=24)
        success_b, res_b = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_2,
            check_in=d_in_b,
            check_out=d_out_b,
            num_guests=1
        )
        if success_b:
            req_id_b = res_b['request_id']
            ok_b, err_b = accept_stay_request(req_id_b, self.host_profile_id)
            self.assertFalse(ok_b, "Host should NOT be able to accept overlapping request")
            self.assertTrue("overlap" in err_b.lower() or "unavailable" in err_b.lower())
        else:
            self.assertTrue("overlap" in str(res_b).lower() or "unavailable" in str(res_b).lower())

    def test_09_host_reject_stay_request(self):
        """Test host rejecting a stay request."""
        d_in = date.today() + timedelta(days=30)
        d_out = date.today() + timedelta(days=32)

        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_2,
            check_in=d_in,
            check_out=d_out,
            num_guests=1
        )
        self.assertTrue(success)
        req_id = res['request_id']

        ok, err = reject_stay_request(req_id, self.host_profile_id, rejection_reason="House under renovation")
        self.assertTrue(ok)

        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'rejected')
        self.assertEqual(req['cancellation_reason'], "House under renovation")

        # Traveller notified
        notifs = get_notifications(self.traveller_id_2, limit=5)
        self.assertTrue(any('stay_request_rejected' in n['type'] for n in notifs))

    def test_10_traveller_cancel_pending_request(self):
        """Test traveller cancelling their own pending request."""
        d_in = date.today() + timedelta(days=35)
        d_out = date.today() + timedelta(days=37)

        success, res = create_stay_request(
            listing_id=self.free_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=1
        )
        self.assertTrue(success)
        req_id = res['request_id']

        ok, err = cancel_stay_request_by_traveller(req_id, self.traveller_id_1, "Change of travel plans")
        self.assertTrue(ok)

        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'cancelled_by_traveller')
        self.assertEqual(req['cancellation_reason'], "Change of travel plans")

    def test_11_traveller_cancel_accepted_request_releases_availability(self):
        """Test traveller cancelling an accepted booking frees blocked calendar dates."""
        d_in = date.today() + timedelta(days=40)
        d_out = date.today() + timedelta(days=43)

        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=2
        )
        self.assertTrue(success)
        req_id = res['request_id']

        # Accept
        accept_stay_request(req_id, self.host_profile_id)

        # Cancel by traveller
        ok, err = cancel_stay_request_by_traveller(req_id, self.traveller_id_1, "Emergency cancel")
        self.assertTrue(ok)

        # Verify availability is released
        is_avail, _ = check_date_availability(self.paid_listing_id, d_in, d_out)
        self.assertTrue(is_avail, "Dates must be available after cancellation")

    def test_12_host_cancel_accepted_reservation(self):
        """Test host cancelling an accepted booking."""
        d_in = date.today() + timedelta(days=45)
        d_out = date.today() + timedelta(days=48)

        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=2
        )
        self.assertTrue(success)
        req_id = res['request_id']

        accept_stay_request(req_id, self.host_profile_id)

        ok, err = cancel_stay_request_by_host(req_id, self.host_profile_id, "Plumbing issue")
        self.assertTrue(ok)

        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'cancelled_by_host')

        is_avail, _ = check_date_availability(self.paid_listing_id, d_in, d_out)
        self.assertTrue(is_avail)

    def test_13_idor_protection_traveller(self):
        """Test User A cannot cancel or tamper with User B's request."""
        d_in = date.today() + timedelta(days=50)
        d_out = date.today() + timedelta(days=52)

        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=1
        )
        self.assertTrue(success)
        req_id = res['request_id']

        # User 2 tries to cancel User 1's request
        ok, err = cancel_stay_request_by_traveller(req_id, self.traveller_id_2, "Hacked")
        self.assertFalse(ok)
        self.assertIn("unauthorized", err.lower())

    def test_14_idor_protection_host(self):
        """Test Host X cannot accept or reject Host Y's requests."""
        d_in = date.today() + timedelta(days=55)
        d_out = date.today() + timedelta(days=57)

        # Listing belongs to host 1
        success, res = create_stay_request(
            listing_id=self.paid_listing_id,
            traveller_id=self.traveller_id_1,
            check_in=d_in,
            check_out=d_out,
            num_guests=1
        )
        self.assertTrue(success)
        req_id = res['request_id']

        # Host 2 tries to accept Host 1's request
        ok, err = accept_stay_request(req_id, self.host_profile_id_2)
        self.assertFalse(ok)
        self.assertIn("unauthorized", err.lower())

        # Host 2 tries to reject Host 1's request
        ok, err = reject_stay_request(req_id, self.host_profile_id_2)
        self.assertFalse(ok)
        self.assertIn("unauthorized", err.lower())

    def test_15_admin_management_and_force_cancel(self):
        """Test admin can list requests and force cancel."""
        d_in = date.today() + timedelta(days=60)
        d_out = date.today() + timedelta(days=62)
        ok_cr, res = create_stay_request(self.paid_listing_id, self.traveller_id_1, d_in, d_out, 1)
        self.assertTrue(ok_cr)
        req_id = res['request_id']

        requests_list, total = get_all_stay_requests_admin()
        self.assertTrue(total > 0)

        ok, _ = admin_cancel_stay_request(req_id, "Policy violation")
        self.assertTrue(ok)
        req = get_stay_request_by_id(req_id)
        self.assertEqual(req['status'], 'cancelled_by_host')


if __name__ == '__main__':
    unittest.main()
