"""Models for the Firewall plugin."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import PROTECT
from django.template.defaultfilters import add, slugify
from django.urls import reverse
from nautobot.core.models import BaseModel
from nautobot.extras.models.change_logging import ChangeLoggedModel
from nautobot.extras.models.tags import TaggedItem
from nautobot.extras.utils import extras_features
from nautobot.ipam.fields import VarbinaryIPField
from netaddr import IPAddress
from taggit.managers import TaggableManager

from nautobot_plugin_firewall_model import choices


@extras_features("custom_validators", "relationships", "graphql")
class IPRange(BaseModel, ChangeLoggedModel):
    """IPRange model to track ranges of IPs in firewall rules."""

    start_address = VarbinaryIPField(
        null=False,
        db_index=True,
        help_text="IPv4 or IPv6 host address",
    )
    end_address = VarbinaryIPField(
        null=False,
        db_index=True,
        help_text="IPv4 or IPv6 host address",
    )
    vrf = models.ForeignKey(
        to="ipam.VRF", on_delete=models.PROTECT, related_name="ip_ranges", blank=True, null=True, verbose_name="VRF"
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )
    size = models.PositiveIntegerField(editable=False)

    class Meta:
        """Meta class."""

        ordering = ["start_address"]
        verbose_name_plural = "IP Ranges"
        constraints = [
            UniqueConstraint(fields=["start_address", "end_address", "vrf"], name="unique_with_vrf"),
            UniqueConstraint(fields=["start_address", "end_address"], condition=Q(vrf=None), name="unique_without_vrf"),
        ]

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:iprange", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return f"{self.start_address}-{self.end_address}"

    def save(self, *args, **kwargs):
        """Overloads to inject size attr."""
        # Record the range's size (number of IP addresses)
        self.size = int(IPAddress(self.end_address) - IPAddress(self.start_address)) + 1

        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """Overloads to validate attr for form verification."""
        if not hasattr(self, "start_address") or not hasattr(self, "end_address"):
            raise ValidationError("Must have `start_address` and `end_address`.")
        elif IPAddress(self.start_address) > IPAddress(self.end_address) or IPAddress(self.start_address) == IPAddress(
            self.end_address
        ):
            raise ValidationError("`end_address` must be higher than `start_address`.")

        super().clean(*args, **kwargs)


@extras_features("custom_validators", "relationships", "graphql")
class FQDN(BaseModel, ChangeLoggedModel):
    """FQDN model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "FQDNs"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:fqdn", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class AddressObject(BaseModel, ChangeLoggedModel):
    """FQDN model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    fqdn = models.ForeignKey(to=FQDN, on_delete=models.PROTECT, null=True)
    ip_range = models.ForeignKey(to=IPRange, on_delete=models.PROTECT, null=True)
    ip_address = models.ForeignKey(to="ipam.IPAddress", on_delete=models.PROTECT, null=True)
    prefix = models.ForeignKey(to="ipam.Prefix", on_delete=models.PROTECT, null=True)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Address Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:addressobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name

    def clean(self, *args, **kwargs):
        """Overloads to validate attr for form verification."""
        address_types = ["fqdn", "ip_range", "ip_address", "prefix"]
        address_count = 0
        for i in address_types:
            if hasattr(self, i) and getattr(self, i) != None:
                address_count += 1
        if address_count != 1:
            raise ValidationError(f"Must specify only one address from type {address_types}, {address_count} found.")

        super().clean(*args, **kwargs)

    @property
    def address(self):
        """Returns the assigned address object."""
        for i in ["fqdn", "ip_range", "ip_address", "prefix"]:
            if getattr(self, i):
                return getattr(self, i)


@extras_features("custom_validators", "relationships", "graphql")
class AddressObjectGroup(BaseModel, ChangeLoggedModel):
    """AddressObjectGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    address_objects = models.ManyToManyField(
        to=AddressObject,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Address Object Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:addressobjectgroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class AddressPolicyObject(BaseModel, ChangeLoggedModel):
    """AddressPolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    address_objects = models.ManyToManyField(
        to=AddressObject,
        blank=True,
    )
    address_object_groups = models.ManyToManyField(
        to=AddressObjectGroup,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Address Policy Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:addresspolicyobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class UserObject(BaseModel, ChangeLoggedModel):
    """UserObject model."""

    username = models.CharField(
        max_length=50,
        unique=True,
    )
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        """Meta class."""

        ordering = ["username"]
        verbose_name_plural = "User Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:userobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.username


@extras_features("custom_validators", "relationships", "graphql")
class UserObjectGroup(BaseModel, ChangeLoggedModel):
    """UserObjectGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    user_objects = models.ManyToManyField(
        to=UserObject,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "User Object Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:userobjectgroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class UserPolicyObject(BaseModel, ChangeLoggedModel):
    """UserPolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    user_objects = models.ManyToManyField(
        to=UserObject,
        blank=True,
    )
    user_object_groups = models.ManyToManyField(
        to=UserObjectGroup,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "User Policy Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:userpolicyobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class Zone(BaseModel, ChangeLoggedModel):
    """Zone model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    vrfs = models.ManyToManyField(
        to="ipam.VRF",
        blank=True,
    )
    interfaces = models.ManyToManyField(
        to="dcim.Interface",
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Zones"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:zone", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class ServiceObject(BaseModel, ChangeLoggedModel):
    """ServiceObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False)
    port = models.IntegerField()
    ip_protocol = models.CharField(choices=choices.IP_PROTOCOL_CHOICES, null=True, blank=True, max_length=20)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Objects"
        constraints = [
            UniqueConstraint(fields=["slug", "port", "ip_protocol"], name="unique_with_ip_protocol"),
            UniqueConstraint(fields=["slug", "port"], condition=Q(ip_protocol=None), name="unique_without_ip_protocol"),
        ]

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:serviceobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        if self.ip_protocol:
            return f"{self.slug}:{self.port}:{self.ip_protocol}"
        return f"{self.slug}:{self.port}"

    def save(self, *args, **kwargs):
        """Overloads to enforce use of slugify."""
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)


@extras_features("custom_validators", "relationships", "graphql")
class ServiceObjectGroup(BaseModel, ChangeLoggedModel):
    """ServiceGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    service_objects = models.ManyToManyField(
        to=ServiceObject,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Object Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:serviceobjectgroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class ServicePolicyObject(BaseModel, ChangeLoggedModel):
    """ServicePolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    service_objects = models.ManyToManyField(
        to=ServiceObject,
        blank=True,
    )
    service_object_groups = models.ManyToManyField(
        to=ServiceObjectGroup,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Policy Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:servicepolicyobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class Source(BaseModel, ChangeLoggedModel):
    """Source model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    address = models.ForeignKey(to=AddressPolicyObject, on_delete=PROTECT)
    service = models.ForeignKey(to=ServicePolicyObject, on_delete=PROTECT)
    user = models.ForeignKey(to=UserPolicyObject, on_delete=PROTECT)
    zone = models.ForeignKey(to=Zone, on_delete=models.CASCADE)

    class Meta:
        """Meta class."""

        ordering = ["description"]
        verbose_name_plural = "Sources"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:source", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        # TODO: Need to determine better __str__
        return self.description


@extras_features("custom_validators", "relationships", "graphql")
class Destination(BaseModel, ChangeLoggedModel):
    """Destination model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    address = models.ForeignKey(to=AddressPolicyObject, on_delete=PROTECT)
    service = models.ForeignKey(to=ServicePolicyObject, on_delete=PROTECT)
    zone = models.ForeignKey(to=Zone, on_delete=models.CASCADE)

    class Meta:
        """Meta class."""

        ordering = ["description"]
        verbose_name_plural = "Destinations"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:destination", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        # TODO: Need to determine better __str__
        return self.description


@extras_features("custom_validators", "relationships", "graphql")
class PolicyRule(BaseModel, ChangeLoggedModel):
    """PolicyRule model."""

    tags = TaggableManager(through=TaggedItem)
    index = models.IntegerField()
    source = models.ForeignKey(to=Source, on_delete=models.PROTECT)
    destination = models.ForeignKey(to=Destination, on_delete=models.PROTECT)
    action = models.CharField(choices=choices.ACTION_CHOICES, max_length=20)
    log = models.BooleanField(default=False)

    class Meta:
        """Meta class."""

        ordering = ["index"]
        verbose_name_plural = "Policy Rules"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:policyrule", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return f"{self.index} - {self.source} - {self.destination} - {self.action}"


@extras_features("custom_validators", "relationships", "graphql")
class Policy(BaseModel, ChangeLoggedModel):
    """Policy model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    policy_rules = models.ManyToManyField(to=PolicyRule)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Policies"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:policy", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name
