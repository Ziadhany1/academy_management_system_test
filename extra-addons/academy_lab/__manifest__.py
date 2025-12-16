{
    "name": "Academy Lab",
    "version": "18.0.1.0.0",
    "depends": ["base", "mail", "contacts"],
    "author": "Ziad",
    "category": "Education",
    "summary": "Training Academy Management System",
    "description": "Manage courses, enrollments, categories, and partners with role-based access.",
    "installable": True,
    "application": True,
    "data": [
        "security/academy_security.xml",
        "security/ir.model.access.csv",  
        "views/academy_course_views.xml",
        "views/academy_course_category_views.xml",
        "views/academy_enrollment_views.xml",
        "views/res_partner_views.xml",
        "views/academy_course_menu.xml"
    ]
}
