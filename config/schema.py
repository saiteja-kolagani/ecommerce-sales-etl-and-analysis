CUSTOMER_COLUMNS = {
    "customer_id",
    "name",
    "age",
    "gender",
    "state",
    "signup_date",
    "email",
    "phone_number",
    "subscribe"
}

TRANSACTION_COLUMNS = {
    "transaction_id",
    "customer_id",
    "transaction_date",
    "product_id",
    "quantity",
    "unit_price",
    "payment_method",
    "discount_applied",
    "transaction_status",
    "review_text",
}

EXPECTED_SCHEMAS = {
    "customers": CUSTOMER_COLUMNS,
    "transactions": TRANSACTION_COLUMNS,
}