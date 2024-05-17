FOOTER_QUICK_LINKS = [

    {"name": "Home", "link": "/", "is_protected": False},
    {"name": "Products", "link": "/products", "is_protected": False},
    {"name": "Orders", "link": "/orders", "is_protected": True},
    {"name": "About Us", "link": "/aboutus", "is_protected": False},
    # Add more links as needed
]

FOOTER_SUPPORT_LINKS = [

    {"name": "Privacy Policy", "link": "/privacyPolicy"},
    {"name": "Return & Refund Policy", "link": "/refund"},
    {"name": "FAQ", "link": "/faq"},
    # Add more "link"s as needed
]


USER_SIDEBAR_LINKS = [

    {"name": "home", "link": "/", "is_protected": 0, "icon_name": "home"},
    {"name": "products", "link": "/products", "is_protected": 0, "icon_name": "products"},
    {"name": "orders", "link": "/orders", "is_protected": 1, "icon_name": "orders"},
    {"name": "cart", "link": "/aboutus", "is_protected": 0, "icon_name": "cart"},
    {"name": "saved", "link": "/aboutus", "is_protected": 0, "icon_name": "saved"},
    {"name": "notification", "link": "/aboutus", "is_protected": 1, "icon_name": "notifications"},
    {"name": "measurements", "link": "/aboutus", "is_protected": 1, "icon_name": "measurements"},
    {"name": "messages", "link": "/aboutus", "is_protected": 1, "icon_name": "messages"},
    {"name": "account", "link": "/aboutus", "is_protected": 1, "icon_name": "account"},
    {"name": "about us", "link": "/aboutus", "is_protected": 0, "icon_name": "aboutus"},
    {"name": "logout", "link": "/aboutus", "is_protected": 0, "icon_name": "logout"},
    {"name": "login", "link": "/aboutus", "is_protected": 0, "icon_name": "login"},
    # Add more "link"s as needed
]
USER_SIDEBAR_VISITORS = [

    {"name": "home", "link": "/", "is_protected": 0, "icon_name": "home"},
    {"name": "products", "link": "/products", "is_protected": 0, "icon_name": "products"},
    {"name": "cart", "link": "/aboutus", "is_protected": 0, "icon_name": "cart"},
    {"name": "saved", "link": "/aboutus", "is_protected": 0, "icon_name": "saved"},
    {"name": "How it works", "link": "/howitworks", "is_protected": 0, "icon_name": "howitworks"},
    {"name": "about us", "link": "/aboutus", "is_protected": 0, "icon_name": "aboutus"},
    {"name": "login", "link": "/aboutus", "is_protected": 0, "icon_name": "login"},
    # Add more "link"s as needed
]

ADMIN_NAV_LINKS = [

    {"name": "Privacy Policy", "link": "/privacyPolicy"},
    {"name": "Return & Refund Policy", "link": "/refund"},
    {"name": "FAQ", "link": "/faq"},
    # Add more "link"s as needed
]

AdminNavLinks = [
    {"name": "Dashboard", "link": "/dashboard"},
    {"name": "Upload product", "link": "/uploadProduct"},
    {"name": "Manage orders", "link": "/adminOrders"},
    {"name": "Contacts", "link": "/#contactUs"},
]


measurement_names = [
    "chest_burst", "stomach", "top_length", "shoulder",
    "sleeve_length", "neck", "muscle", "waist", "laps", "knee",
]


default_measurement = {
    name: 0.0 for name in measurement_names
}
