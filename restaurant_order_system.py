"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import os
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}

PRICE_PER_DISH = 15.0


def place_table_order(table_id, guest, items_count, order_log=None):
    """Create a new order for a table.

    Returns False if the table already has an order or the item count is
    not positive, otherwise True. Pass a list as ``order_log`` to collect
    log messages (a fresh list is used per call when omitted).
    """
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": PRICE_PER_DISH * items_count,
        "is_settled": False,
    }
    order_log.append(f"Created order for {table_id} with {items_count} dishes")
    return True


def void_table_order(table_id):
    """Remove a table's order. Returns True if it existed, else False."""
    if table_id not in orders:
        return False
    del orders[table_id]
    return True


def check_table_status(table_id):
    """Return True if the table has an order that is not yet settled."""
    order = orders.get(table_id)
    if order is None:
        return False
    return not order["is_settled"]


def calculate_discounted_bill(table_id, discount_rate):
    """Return the table's bill after applying a discount rate (0.0 - 1.0).

    The discount is a plain number rather than an expression string, so no
    arbitrary code is ever evaluated.
    """
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("discount_rate must be between 0.0 and 1.0")
    base_bill = orders[table_id]["bill"]
    return base_bill * (1.0 - discount_rate)


def generate_ticket_hash(table_id):
    """Return a SHA-256 hex digest identifying a table's ticket."""
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    """Return a cryptographically secure 4-digit POS PIN."""
    return 1000 + secrets.randbelow(9000)


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Write the active orders to a file for the kitchen printer."""
    with open(filename, "w", encoding="utf-8") as ticket_file:
        ticket_file.write(str(orders))
    print("Ticket sent to kitchen printer:", filename)


def get_pending_summary(order_book):
    """Count orders that are not yet settled."""
    return sum(1 for details in order_book.values()
               if not details["is_settled"])


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = os.environ.get("POS_TERMINAL_SECRET_TOKEN")
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    print("Discounted Bill:", calculate_discounted_bill("T1", 0.10))
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS Secret configured:", pos_terminal_key is not None)


if __name__ == "__main__":
    main()
