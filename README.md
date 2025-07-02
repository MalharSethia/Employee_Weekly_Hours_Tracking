# Employee Weekly Hours Tracking Module

## Overview

The Employee Weekly Hours Tracking module is a comprehensive Odoo add-on designed to automatically monitor employee work hours, detect discrepancies between expected and logged hours, and notify managers when intervention may be needed. This module integrates seamlessly with Odoo's existing HR, Project, and Timesheet modules to provide real-time insights into workforce productivity and compliance.

## Key Features

### 📊 Real-Time Hours Tracking
- **Current Week Monitoring**: Automatically calculates hours logged by each employee for the current week
- **Dynamic Updates**: Hours are recalculated in real-time as employees log timesheet entries
- **Project Integration**: Only counts hours logged against actual projects (excludes administrative time)

### 🎯 Discrepancy Detection
- **Intelligent Status System**: Categorizes employees into four status levels:
  - **On Track**: Within 2 hours of expected weekly hours
  - **Overtime**: 2-10 hours over expected hours
  - **Undertime**: More than 2 hours under expected hours
  - **Critical**: More than 10 hours over expected hours
- **Configurable Thresholds**: Expected weekly hours can be customized per employee
- **Tolerance Settings**: Built-in tolerance levels prevent unnecessary alerts for minor variations

### 📧 Automated Manager Notifications
- **Smart Alerting**: Automatically notifies managers when significant discrepancies occur
- **Timing Logic**: Sends alerts on Thursday/Friday for current week issues (allowing time for correction)
- **Duplicate Prevention**: Ensures managers aren't spammed with multiple alerts for the same issue
- **Rich Email Templates**: Professional email notifications with detailed hour breakdowns

### 📈 Historical Tracking
- **Weekly Summaries**: Maintains complete historical records of weekly hour summaries
- **Trend Analysis**: Track patterns in employee work habits over time
- **Audit Trail**: Records when managers were notified and for what reasons

## Module Components

### Models

#### 1. HR Employee Extensions (`hr_employee.py`)
Extends the standard employee record with weekly hours tracking capabilities.

**New Fields:**
- `current_week_hours`: Computed field showing total hours for current week
- `expected_weekly_hours`: Configurable expected hours (default: 40)
- `hours_discrepancy`: Difference between logged and expected hours
- `discrepancy_status`: Current status (on_track, overtime, undertime, critical)
- `weekly_summary_ids`: One-to-many relationship to historical summaries

**Key Methods:**
- `_compute_weekly_hours()`: Calculates current week hours from timesheet entries
- `_compute_hours_discrepancy()`: Determines variance from expected hours
- `_compute_discrepancy_status()`: Categorizes employee status based on discrepancy

#### 2. Project Timesheet Extensions (`project_timesheet.py`)
Adds automatic triggers to the timesheet system for real-time monitoring.

**Functionality:**
- **Create Trigger**: When new timesheet entries are created, automatically checks for discrepancies
- **Update Trigger**: When existing entries are modified, recalculates affected employee summaries
- **Smart Processing**: Only triggers checks for employees whose records were actually affected

#### 3. Weekly Summary Model (`weekly_summary.py`)
Central model for managing weekly hour summaries and notifications.

**Fields:**
- `employee_id`: Reference to the employee
- `week_start_date` / `week_end_date`: Week period (Monday to Sunday)
- `logged_hours`: Actual hours worked during the week
- `expected_hours`: Expected hours for the employee
- `discrepancy`: Calculated difference
- `status`: Computed status based on discrepancy
- `manager_notified`: Flag indicating if manager was alerted
- `notification_date`: Timestamp of notification
- `notes`: Free-text field for additional comments

**Key Methods:**
- `_generate_weekly_summaries()`: Scheduled method to create end-of-week summaries
- `_check_weekly_discrepancies()`: Real-time discrepancy checking for current week
- `_notify_manager()`: Handles manager notification logic and email sending

### Views and User Interface

#### 1. Enhanced Employee Views
- **Status Bar**: Visual status indicator at the top of employee forms
- **Weekly Hours Tab**: Dedicated section showing:
  - Current week statistics
  - Expected vs. actual hours
  - Discrepancy calculations
  - Historical weekly summaries
- **Tree View Enhancements**: Quick status overview in employee lists

#### 2. Weekly Summary Management
- **Dedicated Views**: Separate interface for reviewing all weekly summaries
- **Filtering Options**: Easy filtering by employee, date range, or status
- **Notification Tracking**: Clear indication of which summaries triggered manager alerts

#### 3. Visual Status Indicators
- **Color-Coded Badges**: Green (on track), Yellow (undertime), Orange (overtime), Red (critical)
- **Status Bars**: Progress-style indicators showing current employee status
- **Quick Identification**: Managers can quickly spot issues at a glance

### Security and Access Control

#### Access Levels:
- **All Users**: Read access to weekly summaries
- **HR Users**: Full access to create and modify summaries
- **HR Managers**: Complete administrative control including deletions

#### Security Groups:
- Integration with standard Odoo HR security groups
- Respects existing employee access restrictions
- Managers only see their direct reports' data

### Automation and Scheduling

#### 1. Weekly Summary Generation
- **Scheduled Action**: Runs automatically every Monday at 9:00 AM
- **Previous Week Processing**: Generates summaries for the completed week
- **Bulk Processing**: Handles all active employees in a single run
- **Duplicate Prevention**: Skips employees who already have summaries for the period

#### 2. Real-Time Monitoring
- **Timesheet Triggers**: Automatic checks when timesheets are created/modified
- **Threshold-Based Alerts**: Only sends notifications for significant discrepancies (>5 hours)
- **Timing Logic**: Mid-week alerts only sent Thursday/Friday to allow correction time

### Email Notifications

#### Template Features:
- **Professional Formatting**: Clean, branded email layout
- **Detailed Information**: Complete breakdown of hours and discrepancies
- **Context Awareness**: Personalized with manager and employee names
- **Actionable Data**: Clear indication of what action may be needed

#### Notification Logic:
- **Manager Hierarchy**: Uses Odoo's built-in manager relationships
- **Email Validation**: Checks for valid manager email addresses
- **Error Handling**: Graceful handling of missing managers or email addresses
- **Audit Trail**: Records all notification attempts and outcomes

## Installation and Setup

### Prerequisites
- Odoo 17.0+
- Required modules: `hr`, `project`, `hr_timesheet`, `mail`

### Installation Steps
1. Copy the module to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the "Employee Weekly Hours Tracking" module
4. Configure expected weekly hours for each employee
5. Set up manager relationships in employee records

### Initial Configuration
1. **Employee Setup**: Set expected weekly hours for each employee (default: 40)
2. **Manager Assignment**: Ensure all employees have managers assigned
3. **Email Configuration**: Verify manager email addresses are correct
4. **Timesheet Integration**: Ensure employees are logging time to projects

## Usage Guide

### For HR Administrators
1. **Monitor Dashboard**: Use the employee tree view to quickly identify status issues
2. **Review Summaries**: Access the Weekly Hours Summary menu for detailed analysis
3. **Configure Settings**: Adjust expected hours per employee as needed
4. **Audit Notifications**: Track which managers have been notified about issues

### For Managers
1. **Receive Alerts**: Automatic email notifications for team member discrepancies
2. **Review Team Status**: Check employee forms for current week status
3. **Historical Analysis**: Review weekly summary history for patterns
4. **Take Action**: Follow up with team members based on alert information

### For Employees
1. **Status Visibility**: See current week status on employee record
2. **Hour Tracking**: View logged vs. expected hours in real-time
3. **Historical View**: Access personal weekly summary history
4. **Transparency**: Clear understanding of hour expectations and performance

## Customization Options

### Configurable Thresholds
- **Expected Hours**: Adjustable per employee (supports part-time, contractors)
- **Tolerance Levels**: Modify the 2-hour tolerance in the code if needed
- **Critical Thresholds**: Adjust the 10-hour overtime critical level
- **Alert Timing**: Change Thursday/Friday alert timing if desired

### Email Templates
- **Branding**: Customize email templates with company branding
- **Content**: Modify notification content and formatting
- **Recipients**: Add CC recipients or modify notification logic
- **Languages**: Support for multi-language email templates

### Status Categories
- **Custom Statuses**: Add additional status categories if needed
- **Color Schemes**: Modify visual indicators and color coding
- **Calculation Logic**: Adjust discrepancy calculation methods
- **Reporting Periods**: Modify weekly period definitions (currently Monday-Sunday)

## Technical Details

### Database Structure
- **New Tables**: `employee_weekly_summary`
- **Extended Tables**: `hr_employee` (computed fields only)
- **Relationships**: Maintains referential integrity with existing HR data

### Performance Considerations
- **Computed Fields**: Efficiently calculated using database queries
- **Batch Processing**: Weekly summaries generated in bulk
- **Indexing**: Proper database indexes on date and employee fields
- **Caching**: Leverages Odoo's built-in field caching

### Integration Points
- **Timesheet System**: Seamless integration with `account.analytic.line`
- **HR Module**: Extends existing employee management
- **Project Module**: Respects project-based time tracking
- **Mail System**: Uses Odoo's email infrastructure

## Troubleshooting

### Common Issues
1. **Missing Notifications**: Check manager assignments and email addresses
2. **Incorrect Hours**: Verify timesheet entries are linked to projects
3. **Status Not Updating**: Ensure scheduled actions are running properly
4. **Access Issues**: Check security group assignments

### Logging and Debugging
- **System Logs**: Module logs activities to Odoo's logging system
- **Error Handling**: Graceful error handling with informative messages
- **Debug Mode**: Additional logging available in debug mode

## Support and Maintenance

### Regular Maintenance
- **Weekly Reviews**: Monitor the weekly summary generation process
- **Email Deliverability**: Ensure notification emails are being delivered
- **Data Cleanup**: Periodic cleanup of old summary records if needed
- **Performance Monitoring**: Watch for any performance impacts

### Upgrade Considerations
- **Data Migration**: Summaries are preserved during module updates
- **Configuration Backup**: Export employee expected hours before major updates
- **Testing**: Test notification functionality after upgrades

## Version History

### Version 1.0.0
- Initial release
- Basic weekly hours tracking
- Manager notification system
- Historical summary generation
- Employee status categorization

---

## License and Support

This module is provided as-is for educational and business use. For support, customization requests, or bug reports, please contact your system administrator or module developer.
