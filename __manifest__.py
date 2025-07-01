{
    'name': 'Employee Weekly Hours Tracking',
    'version': '1.0.0',
    'category': 'Human Resources',
    'summary': 'Track employee weekly hours with manager notifications for discrepancies',
    'description': '''
        This module automatically calculates weekly worked hours based on project timesheets
        and notifies managers when there are discrepancies between logged and assigned hours.
    ''',
    'author': 'Your Company',
    'depends': ['hr', 'project', 'hr_timesheet', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/weekly_summary_views.xml',
        'data/scheduled_actions.xml',
        'data/mail_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
