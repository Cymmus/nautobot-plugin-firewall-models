"""Unit tests for views."""
# flake8: noqa: F403,405
from nautobot.extras.models.statuses import Status
from nautobot.utilities.testing import ViewTestCases

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import
from .fixtures import create_env, create_fqdn, create_ip_range, create_role


class IPRangeUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the IPRange viewsets."""
    model = IPRange
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"start_address": "10.0.0.1", "end_address": "10.0.0.3", "status": status}
        create_ip_range()

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class FQDNUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Protocol viewsets."""
    model = FQDN
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "test.local", "status": status}
        create_fqdn()

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class AddressObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the AddressObject viewsets."""
    model = AddressObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        ip_range = IPRange.objects.first()
        status = Status.objects.get(slug="active").id

        cls.form_data = {"name": "obj1", "ip_range": ip_range.id, "status": status}

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class AddressObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the AddressObjectGroup viewsets."""
    model = AddressObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        status = Status.objects.get(slug="active").id
        addr_obj = AddressObject.objects.first()
        cls.form_data = {"name": "test1", "address_objects": [addr_obj.id], "status": status}

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class AddressPolicyObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the AddressPolicyObject viewsets."""
    model = AddressPolicyObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        status = Status.objects.get(slug="active").id
        addr_obj = AddressObject.objects.first()
        addr_grp = AddressObjectGroup.objects.first()
        cls.form_data = {
            "name": "test1",
            "address_objects": [addr_obj.id],
            "address_object_groups": [addr_grp.id],
            "status": status,
        }

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class ServiceObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceObject viewsets."""
    model = ServiceObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "HTTP", "port": 80, "status": status}
        create_env()

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass

    def test_service_object_str(self):
        """testing str of service object."""
        svc = ServiceObject.objects.first()
        svc.ip_protocol = "TCP"

        self.assertEqual(str(svc), f"{svc.slug}:{svc.port}:TCP")

        svc.ip_protocol = None

        self.assertEqual(str(svc), f"{svc.slug}:{svc.port}")


class ServiceGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceGroup viewsets."""
    model = ServiceObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = ServiceObject.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "test1", "service_objects": [svc_obj.id], "status": status}

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class ServicePolicyObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the ServicePolicyObject viewsets."""
    model = ServicePolicyObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = ServiceObject.objects.first()
        svc_grp = ServiceObjectGroup.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {
            "name": "test3",
            "service_objects": [svc_obj.id],
            "service_object_groups": [svc_grp.id],
            "status": status,
        }

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class UserObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the User viewsets."""
    model = UserObject
    bulk_edit_data = {"name": "User Name 123"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"username": "test1", "name": "Foo", "status": status}
        create_env()

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class UserObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the UserGroup viewsets."""
    model = UserObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        user = UserObject.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "test1", "user_objects": [user.id], "status": status}

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class UserPolicyObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the UserPolicyObject viewsets."""
    model = UserPolicyObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        usr_obj = UserObject.objects.first()
        usr_grp = UserObjectGroup.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {
            "name": "test3",
            "user_objects": [usr_obj.id],
            "user_object_groups": [usr_grp.id],
            "status": status,
        }

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class ZoneUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Zone viewsets."""
    model = Zone
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "trust", "status": status}
        create_env()

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class SourceDestinationUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Source viewsets."""
    model = SourceDestination
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        usr = UserPolicyObject.objects.first()
        svc = ServicePolicyObject.objects.first()
        addr = AddressPolicyObject.objects.first()
        zone = Zone.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {"address": addr.id, "service": svc.id, "user": usr.id, "zone": zone.id, "status": status}

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass

    def test_source_str(self):
        """Testing proper str."""
        src = SourceDestination.objects.first()

        self.assertEqual(str(src), f"{src.address} - {src.service} - {src.user} - {src.zone}")

        src.user = None

        self.assertEqual(str(src), f"{src.address} - {src.service} - {src.zone}")


class PolicyRuleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the PolicyRule viewsets."""
    model = PolicyRule
    bulk_edit_data = {"log": False}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src = SourceDestination.objects.first()
        dest = SourceDestination.objects.last()
        status = Status.objects.get(slug="active").id
        cls.form_data = {
            "source": src.id,
            "destination": dest.id,
            "action": "Deny",
            "log": True,
            "index": 4,
            "name": "test rule",
            "status": status,
        }

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass

    def test_policy_str(self):
        """Checks conditional on __str__."""
        pol_rule = PolicyRule.objects.first()

        self.assertEqual(str(pol_rule), pol_rule.name)

        pol_rule.name = None

        self.assertEqual(
            str(pol_rule), f"{pol_rule.index} - {pol_rule.source} - {pol_rule.destination} - {pol_rule.action}"
        )


class PolicyUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Policy viewsets."""
    model = Policy
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        pol_rule = PolicyRule.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {
            "name": "test 2",
            "policy_rules": [pol_rule.id],
            "description": "Test desc",
            "status": status,
        }

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass


class RoleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Policy viewsets."""
    model = Role
    bulk_edit_data = {"description": "test update description"}
    form_data = {"name": "test 2", "slug": "test-2", "weight": 1000}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_role()

    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    def test_bulk_import_objects_with_permission(self):
        pass

    def test_bulk_import_objects_without_permission(self):
        pass
