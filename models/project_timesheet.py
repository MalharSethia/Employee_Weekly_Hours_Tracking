from odoo import models, fields, api

class ProjectTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    @api.model_create_multi
    def create(self, vals_list):
        """Trigger weekly summary update when new timesheet entries are created"""
        records = super().create(vals_list)
        
        # Get unique employees from created records
        employees = records.mapped('employee_id')
        if employees:
            # Trigger weekly summary check for affected employees
            self.env['employee.weekly.summary']._check_weekly_discrepancies(employees)
        
        return records

    def write(self, vals):
        """Trigger weekly summary update when timesheet entries are modified"""
        result = super().write(vals)
        
        if any(field in vals for field in ['unit_amount', 'date', 'employee_id']):
            employees = self.mapped('employee_id')
            if employees:
                self.env['employee.weekly.summary']._check_weekly_discrepancies(employees)
        
        return result
