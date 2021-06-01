"""Enumeration of error sources returned by ShipEngine API."""
from enum import Enum


class ErrorCode(Enum):
    """ErrorCode enumeration that provides members used for Error Codes."""

    """
    Only certain carriers support pre-paid balances. So you can only add funds
    to those carriers. If you attempt to add funds to a carrier that doesn't
    support it, then you'll get this error code.
    """
    AUTO_FUND_NOT_SUPPORTED = "auto_fund_not_supported"

    """
    Once a batch has started processing, it cannot be modified. Attempting to
    modify it will cause this error.
    """
    BATCH_CANNOT_BE_MODIFIED = "batch_cannot_be_modified"

    """
    You attempted to perform an operation on multiple shipments from different
    carriers. Try performing separate operations for each carrier instead.
    """
    CARRIER_CONFLICT = "carrier_conflict"

    """
    This error means that you're trying to use a carrier that hasn't been setup
    yet. You can setup carriers from your ShipEngine dashboard, or via the API.
    """
    CARRIER_NOT_CONNECTED = "carrier_not_connected"

    """
    The operation you are performing isn't supported by the specified carrier.
    """
    CARRIER_NOT_SUPPORTED = "carrier_not_supported"

    """
    Some forms of delivery confirmation aren't supported by some carriers.
    This error means that the combination of carrier and delivery confirmation
    are not supported.
    """
    CONFIRMATION_NOT_SUPPORTED = "confirmation_not_supported"

    """
    This error means that two or more fields in your API request are mutually
    exclusive or contain conflicting values. The error will include a fields
    array that lists the conflicting fields.
    """
    FIELD_CONFLICT = "field_conflict"

    """
    A required field is missing or empty. The field_name property indicates
    which field is missing. Note that some fields are conditionally required,
    based on the values of other fields or the type of operation being performed.
    """
    FIELD_VALUE_REQUIRED = "field_value_required"

    """
    You attempted to perform an operation that you don't have permissions to do.
    Check your API key to ensure that you're using the correct one. Or contact
    our support team to ensure that your account has the necessary permissions.
    """
    FORBIDDEN = "forbidden"

    """
    A few parts of the ShipEngine API allow you to provide your own ID for resources.
    These IDs must be unique; otherwise, you'll get this error code.
    """
    IDENTIFIER_CONFLICT = "identifier_conflict"

    """
    When updating a resource (such as a shipment or warehouse), the ID in the URL
    and in the request body must match.
    """
    IDENTIFIER_MUST_MATCH = "identifiers_must_match"

    """
    When creating a return label, you can optionally pair it to an outbound_label_id.
    The outbound label must be from the same carrier as the return label.
    """
    INCOMPATIBLE_PAIRED_LABELS = "incompatible_paired_labels"

    """
    The mailing address that you provided is invalid. Try using our address
    validation API to verify addresses before using them.
    """
    INVALID_ADDRESS = "invalid_address"

    """
    You attempted to perform an operation that isn't allowed for your billing plan.
    Contact our sales team for assistance.
    """
    INVALID_BILLING_PLAN = "invalid_billing_plan"

    """
    When creating a label or creating a return label, if you set the charge_event
    field to a value that isn't offered by the carrier, then you will receive this
    error. You can leave the charge_event field unset, or set it to carrier_default
    instead.
    """
    INVALID_CHARGE_EVENT = "invalid_charge_event"

    """
    One of the fields in your API request has an invalid value. The field_name
    property indicates which field is invalid.
    """
    INVALID_FIELD_VALUE = "invalid_field_value"

    """
    This error is similar to invalid_field_value, but is specifically for ID
    fields, such as label_id, shipmentId, carrierId, etc. The field_name
    property indicates which field is invalid.
    """
    INVALID_IDENTIFIER = "invalid_identifier"

    """
    The operation you're attempting to perform is not allowed because the resource
    public constis in the wrong status. For example, if a label's status is "voided"; then
    it cannot be included in a manifest.
    """
    INVALID_STATUS = "invalid_status"

    """
    A string field in your API request is either too short or too long. The
    field_name property indicates which field is invalid, and the min_length
    and max_length properties indicate the allowed length.
    """
    INVALID_STRING_LENGTH = "invalid_string_length"

    """
    Not all carriers allow you to add custom images to labels. You can only set
    the label_image_id for supported carriers.
    """
    LABEL_IMAGES_NOT_SUPPORTED = "label_images_not_supported"

    """
    This error indicates a problem with your FedEx account. Please contact
    FedEx to resolve the issue.
    """
    METER_FAILURE = "meter_failure"

    """The ShipEngine API endpoint that was requested does not exist."""
    NOT_FOUND = "not_found"

    PARTIALLY_VERIFIED_TO_PREMISE_LEVEL = "partially_verified_to_premise_level"

    """
    You have exceeded a rate limit. Check the the error_source field to determine
    whether the rate limit was imposed by ShipEngine or by a third-party, such
    as a carrier. If the rate limit is from ShipEngine, then consider using bulk
    operations to reduce the number of API calls, or contact our support team
    about increasing your rate limit.
    """
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

    """
    The API call requires a JSON request body. See the corresponding documentation
    page for details about the request structure.
    """
    REQUEST_BODY_REQUIRED = "request_body_required"

    """
    You may receive this error if you attempt to schedule a pickup for a return
    label.
    """
    RETURN_LABEL_NOT_SUPPORTED = "return_label_not_supported"

    """
    You may receive this error if you attempt to perform an operation that
    requires a subscription. Please contact our sales department to discuss a
    ShipEngine enterprise contract.
    """
    SUBSCRIPTION_INACTIVE = "subscription_inactive"

    """
    Some carriers require you to accept their terms and conditions before you
    can use them via ShipEngine. If you get this error, then please login to
    the ShipEngine dashboard to read and accept the carrier's terms.
    """
    TERMS_NOT_ACCEPTED = "terms_not_accepted"

    """
    An API call timed out because ShipEngine did not respond within the allowed
    timeframe.
    """
    TIMEOUT = "timeout"

    """
    This error will occur if you attempt to track a package for a carrier that
    doesn't offer that service.
    """
    TRACKING_NOT_SUPPORTED = "tracking_not_supported"

    """
    You may receive this error if your free trial period has expired and you
    have not upgraded your account or added billing information.
    """
    TRIAL_EXPIRED = "trial_expired"

    """
    Your API key is incorrect, expired, or missing. Check our authentication
    guide to learn more about authentication with ShipEngine.
    """
    UNAUTHORIZED = "unauthorized"

    """
    This error has not yet been assigned a code. See the notes above about how
    to handle these.
    """
    UNSPECIFIED = "unspecified"

    """
    When verifying your account (by email, SMS, phone call, etc.) this error
    indicates that the verification code is incorrect. Please re-start the
    verification process to get a new code.
    """
    VERIFICATION_FAILURE = "verification_failure"

    """
    You attempted to perform an operation on multiple shipments from different
    warehouses. Try performing separate operations for each warehouse instead.
    """
    WAREHOUSE_CONFLICT = "warehouse_conflict"

    """
    ShipEngine only allows you to have one webhook of each type. If you would
    like to replace a webhook with a new one, please delete the old one first.
    """
    WEBHOOK_EVENT_TYPE_CONFLICT = "webhook_event_type_conflict"
