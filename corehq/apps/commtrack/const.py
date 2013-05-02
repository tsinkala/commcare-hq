
COMMTRACK_USERNAME = 'commtrack-system'


COMMTRACK_SUPPLY_POINT_XMLNS = 'http://openrosa.org/commtrack/supply_point'
COMMTRACK_SUPPLY_POINT_PRODUCT_XMLNS = 'http://openrosa.org/commtrack/supply_point_product'
COMMTRACK_REPORT_XMLNS = 'http://openrosa.org/commtrack/stock_report'

def is_commtrack_form(form):
    return form.xmlns in [
        COMMTRACK_SUPPLY_POINT_XMLNS,
        COMMTRACK_SUPPLY_POINT_PRODUCT_XMLNS,
        COMMTRACK_REPORT_XMLNS,
    ]


SUPPLY_POINT_CASE_TYPE = 'supply-point'
SUPPLY_POINT_PRODUCT_CASE_TYPE = 'supply-point-product'
REQUISITION_CASE_TYPE = 'commtrack-requisition'

def is_commtrack_case(case):
    return case.type in [
        SUPPLY_POINT_CASE_TYPE,
        SUPPLY_POINT_PRODUCT_CASE_TYPE,
        REQUISITION_CASE_TYPE,
    ]

ALL_PRODUCTS_TRANSACTION_TAG = '_all_products'

# supply point products --> supply points and sp product --> requisitions
PARENT_CASE_REF = 'parent'

# http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
def enum(**enums):
    return type('Enum', (), enums)

RequisitionActions = enum(
    REQUEST='request',
    APPROVAL='approval',
    FILL='fill',
    RECEIPTS='requisition-receipts',
)

class RequisitionStatus(object):
    """a const for our requisition status choices"""
    REQUESTED = "requested"
    APPROVED = "approved"
    FILLED = "filled"
    RECEIVED = "received"
    CANCELED = "canceled"
    CHOICES = [REQUESTED, APPROVED, FILLED, RECEIVED, CANCELED]
    CHOICES_PENDING = [REQUESTED, APPROVED, FILLED]
    CHOICES_CLOSED = [RECEIVED, CANCELED]

    @classmethod
    def by_action_type(cls, type):
        return {
            RequisitionActions.REQUEST: cls.REQUESTED,
            RequisitionActions.APPROVAL: cls.APPROVED,
            RequisitionActions.FILL: cls.FILLED,
            RequisitionActions.RECEIPTS: cls.RECEIVED,
        }[type]