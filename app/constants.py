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

Login_fields = [
        {"label": "Email", "placeholder": "example@gmail.com",  "type": "email"},
        {"label": "Password", "placeholder": "password",  "type": "password"},


        ]
Password_reset_fields = [
        {"label": "Email", "placeholder": "example@gmail.com", "type": "email"}
        ]

Reset_fields = [

        {"label": "Password", "placeholder": "New Password", "type": "password"},
        {"label": "Confirm_password", "placeholder": "Confirm Password", "type": "password"}


            ]
Create_user_fields = [

        {"label": "Name", "placeholder": "Okereke Uzochukwu", "type": "text"},
        {"label": "Email", "placeholder": "example@gmail.com", "type": "email"},
        {"label": "Phone_number", "placeholder": "07033734183", "type": "number"},
        {"label": "Password", "placeholder": "password",  "type": "password"}

            ]
Create_tailor_fields = [

         {"label": "Name", "placeholder": "Okereke Uzochukwu", "type": "text"},
         {"label": "Email ", "placeholder":"example@gmail.com", "type": "email"},
         {"label": "Phone_nNumber ", "placeholder": "07033734183", "type": "number"},
         {"label": "Password", "placeholder": "password",  "type": "password"}


            ]
Tailor_address_fields = [

         {"label": "Street", "placeholder": "#1 Danosa Street, Benin auchi road", "type": "text"},
         {"label": "City", "placeholder": "Benin City", "type": "text"},
         {"label": "State", "placeholder": "Edo", "type": "text"}

            ]

Tailor_verification_fields = [

         {"label": "NIN", "placeholder": "12345678909", "type": "number"},
         {"label": "Upload_NIN_Slip", "placeholder": "Benin City", "type": "file"},
         {"label": "Upload_your_photo", "placeholder": "Edo", "type": "file"}

            ]


auth_top = {
        "login":[ "Welcome back", "Sign in to continue"],
        "password_reset":["Forgot Password", "Enter the email associated with your account and we will send an email instruction to reset your password"],
        "reset":[ "Reset", "Now, let's set up your new password. "],
        "create_user": ["Create an account", "Signup to get started"],
        "create_tailor": ["Create an account", "Signup to get started"],
        "tailor_address": ["Address", " "],
        "tailor_verification": ["Verification", " "]


        }

