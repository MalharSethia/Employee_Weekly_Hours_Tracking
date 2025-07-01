from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Weekly hours tracking
    current_week_hours = fields.Float(
        string="Current Week Hours",
        compute="_compute_weekly_hours",
        store=False
    )
    
    expected_weekly_hours = fields.Float(
        string="Expected Weekly Hours",
        default=40.0,
        help="Expected number of hours per week based on work schedule"
    )
    
    hours_discrepancy = fields.Float(
        string="Hours Discrepancy",
        compute="_compute_hours_discrepancy",
        store=False,
        help="Difference between logged and expected hours (positive = overtime, negative = undertime)"
    )
    
    discrepancy_status = fields.Selection([
        ('on_track', 'On Track'),
        ('overtime', 'Overtime'),
        ('undertime', 'Undertime'),
        ('critical', 'Critical Discrepancy')
    ], string="Weekly Status", compute="_compute_discrepancy_status", store=False)
    
    weekly_summary_ids = fields.One2many(
        'employee.weekly.summary',
        'employee_id',
        string="Weekly Summaries"
    )

    @api.depends('timesheet_ids.date', 'timesheet_ids.unit_amount')
    def _compute_weekly_hours(self):
        for employee in self:
            # Get current week dates (Monday to Sunday)
            today = fields.Date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            # Sum timesheet hours for current week
            timesheets = self.env['account.analytic.line'].search([
                ('employee_id', '=', employee.id),
                ('date', '>=', start_of_week),
                ('date', '<=', end_of_week),
                ('project_id', '!=', False)
            ])
            
            employee.current_week_hours = sum(timesheets.mapped('unit_amount'))

    @api.depends('current_week_hours', 'expected_weekly_hours')
    def _compute_hours_discrepancy(self):
        for employee in self:
            employee.hours_discrepancy = employee.current_week_hours - employee.expected_weekly_hours

    @api.depends('hours_discrepancy')
    def _compute_discrepancy_status(self):
        for employee in self:
            discrepancy = employee.hours_discrepancy
            if abs(discrepancy) <= 2:  # Within 2 hours tolerance
                employee.discrepancy_status = 'on_track'
            elif discrepancy > 10:  # More than 10 hours overtime
                employee.discrepancy_status = 'critical'
            elif discrepancy > 2:
                employee.discrepancy_status = 'overtime'
            else:
                employee.discrepancy_status = 'undertime'
