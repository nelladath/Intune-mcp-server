# Microsoft Intune & Entra ID MCP Server

A comprehensive Model Context Protocol (MCP) server for managing Microsoft Intune and Entra ID (Azure AD) through the Microsoft Graph API. This server enables AI assistants to perform device management, user administration, security configuration, and more -- **134 tools** across **16 categories**.

## Features

### **Core**
- Test Graph API connectivity and get tenant info
- Intune overview with device counts and compliance summary

### **Intune Device Management**
- List, search, and manage devices with filters
- Compliance monitoring and non-compliant device reporting
- Remote actions (sync, restart, lock, wipe, retire, rename)
- Bulk device sync
- Hardware inventory, installed apps, and network info
- Stale device detection
- Autopilot device and profile management
- Device configuration profiles and compliance policies

### **App Management**
- List, search, and inspect mobile apps
- Assign apps to groups (required, available, uninstall)
- Remove all app assignments

### **Entra ID (Azure AD) User Management**
- Full user CRUD operations
- User onboarding with manager, licenses, and group assignment
- User offboarding (block sign-in, revoke sessions, remove groups/apps/licenses)
- Password management and reset
- License assignment and management
- Manager assignment and direct reports
- Bulk operations (create users, assign licenses, add to groups)
- Sign-in activity tracking
- Deleted user recovery

### **Entra ID Device Management**
- List, search, and inspect Entra ID devices
- Delete devices from Entra ID, Intune, or both
- Enable/disable Entra devices

### **Group Management**
- Security groups (static and dynamic)
- Microsoft 365 groups
- Member and owner management
- Dynamic membership rules
- Search and delete groups

### **Conditional Access**
- Policy listing and inspection
- Enable/disable policies
- Named locations management

### **Authentication & Identity Protection**
- MFA status monitoring
- Authentication methods management
- Sign-in logs with filtering
- Risky user detection and dismissal
- Risk detections and alerts
- Directory audit logs

### **App Registrations & Enterprise Apps**
- List and search app registrations
- Credential expiry monitoring
- Enterprise app management (enable/disable)
- App permission inspection
- Delete app registrations

### **Windows 365 Cloud PC**
- List and manage Cloud PCs
- Provisioning policies
- Restart, reprovision actions
- Gallery images
- Cloud PC overview

### **Tenant Administration**
- Organization and domain information
- Service health monitoring and issue tracking
- Directory roles and membership
- Global admin listing
- License/subscription management
- Security defaults status
- Role assignment

### **Scripts & Remediations**
- PowerShell script management and deployment status
- Proactive remediation scripts and status summaries

### **Security & Compliance**
- Security baselines and deployed profiles
- App protection policies (MAM)
- Enrollment restrictions
- Device categories
- Windows malware reports
- Device protection overview and threat state
- Per-device malware detection

### **Reports**
- Device compliance summary
- Configuration profile deployment status
- Compliance policy deployment status
- App installation status
- License usage reports
- Hardware inventory reports

## Prerequisites

- Python 3.11+
- Microsoft Entra ID (Azure AD) tenant
- App registration with appropriate permissions

## Required API Permissions

Add these permissions to your app registration in Azure Portal:

### Intune
```
DeviceManagementManagedDevices.ReadWrite.All
DeviceManagementConfiguration.ReadWrite.All
DeviceManagementApps.ReadWrite.All
DeviceManagementServiceConfig.ReadWrite.All
```

### Entra ID
```
User.ReadWrite.All
Group.ReadWrite.All
Directory.ReadWrite.All
RoleManagement.ReadWrite.Directory
Policy.ReadWrite.ConditionalAccess
IdentityRiskyUser.ReadWrite.All
IdentityRiskEvent.Read.All
AuditLog.Read.All
UserAuthenticationMethod.ReadWrite.All
```

### Windows 365
```
CloudPC.ReadWrite.All
```

### Service Health & Reports
```
ServiceHealth.Read.All
Reports.Read.All
```

### Other
```
Organization.Read.All
Domain.Read.All
Application.Read.All
```

## Installation

1. **Clone or download the repository**

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file or set environment variables:
```env
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

## Configuration for Cursor

Add to your Cursor MCP configuration (`~/.cursor/mcp.json` on Windows: `%USERPROFILE%\.cursor\mcp.json`):

```json
{
  "mcpServers": {
    "intune": {
      "command": "C:\\MCP\\venv\\Scripts\\python.exe",
      "args": ["C:\\MCP\\intune_mcp_server\\server.py"],
      "env": {
        "TENANT_ID": "your-tenant-id",
        "CLIENT_ID": "your-client-id",
        "CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

## Configuration for VS Code
VS Code supports MCP servers via GitHub Copilot (agent mode) and other MCP-compatible extensions.

### Option 1 - User-level configuration with envFile (recommended)

Use this to keep secrets out of `mcp.json` and centralize credentials in a local `.env` file.

Windows user config path:
- `%APPDATA%\Code\User\mcp.json`

```json
{
  "servers": {
    "intune": {
      "type": "stdio",
      "command": "E:\\MCP\\intune-mcp-server\\.venv\\Scripts\\intune-mcp-server.exe",
      "args": [],
      "envFile": "E:\\MCP\\intune-mcp-server\\.env"
    }
  },
  "inputs": []
}
```

### Option 2 - Workspace configuration with inline env

Create or edit `.vscode/mcp.json` in your workspace folder:

```json
{
  "servers": {
    "intune": {
      "type": "stdio",
      "command": "C:\\MCP\\venv\\Scripts\\python.exe",
      "args": ["C:\\MCP\\intune_mcp_server\\server.py"],
      "env": {
        "TENANT_ID": "your-tenant-id",
        "CLIENT_ID": "your-client-id",
        "CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Option 3 - User-level configuration with inline env

You can also put the same inline `env` configuration in `%APPDATA%\\Code\\User\\mcp.json`.

### Option 4 - VS Code settings.json

Alternatively, add the server directly inside your VS Code `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "intune": {
        "type": "stdio",
        "command": "C:\\MCP\\venv\\Scripts\\python.exe",
        "args": ["C:\\MCP\\intune_mcp_server\\server.py"],
        "env": {
          "TENANT_ID": "your-tenant-id",
          "CLIENT_ID": "your-client-id",
          "CLIENT_SECRET": "your-client-secret"
        }
      }
    }
  }
}
```

### Enabling MCP in VS Code

1. Install the GitHub Copilot extension (v1.156+) or another MCP-compatible extension.
2. Open the Command Palette (`Ctrl+Shift+P`) and run `MCP: List Servers` to verify the server is detected.
3. In GitHub Copilot Chat, switch to Agent mode (the sparkle icon) to use MCP tools.

### Configuration Comparison

| Setting | Cursor | VS Code |
|---------|--------|---------|
| Config file | `%USERPROFILE%\.cursor\mcp.json` | `.vscode/mcp.json` or `%APPDATA%\Code\User\mcp.json` |
| Root key | `mcpServers` | `servers` |
| Type field | Not required | `"type": "stdio"` required |
| Scope | Global | Workspace or user-level |

## Available Tools (134)

### Core (2 tools)

| Tool | Description |
|------|-------------|
| `test_connection` | Test Microsoft Graph API connection and return tenant info |
| `get_intune_overview` | Intune overview with device counts and compliance summary |

### Intune Device Management (9 tools)

| Tool | Description |
|------|-------------|
| `list_managed_devices` | List all Intune managed devices (supports filters, pagination) |
| `get_device_details` | Get comprehensive device information by device ID |
| `search_devices` | Search devices by name, user, or serial number |
| `get_noncompliant_devices` | List non-compliant devices |
| `sync_device` | Trigger device sync |
| `restart_device` | Remotely restart a device |
| `remote_lock_device` | Remotely lock a device |
| `wipe_device` | Wipe a device -- destructive, requires `confirm=True` |
| `retire_device` | Retire a device (remove company data), requires `confirm=True` |

### Device Inventory & Advanced Management (6 tools)

| Tool | Description |
|------|-------------|
| `get_device_hardware_inventory` | Hardware inventory for a specific device |
| `get_device_installed_apps` | List installed apps on a device |
| `rename_device` | Rename a managed device remotely |
| `bulk_sync_devices` | Sync multiple devices at once |
| `get_device_network_info` | Network information for a device |
| `get_stale_devices_report` | Devices inactive for a given number of days |

### Autopilot (2 tools)

| Tool | Description |
|------|-------------|
| `list_autopilot_devices` | List Windows Autopilot devices |
| `list_autopilot_profiles` | List Windows Autopilot deployment profiles |

### Policy Management (2 tools)

| Tool | Description |
|------|-------------|
| `list_compliance_policies` | List device compliance policies |
| `list_configuration_profiles` | List device configuration profiles |

### App Management (5 tools)

| Tool | Description |
|------|-------------|
| `list_mobile_apps` | List mobile apps in Intune |
| `get_app_details` | Get details for a specific app |
| `search_apps` | Search apps by name |
| `assign_app_to_group` | Assign an app to a group (required, available, or uninstall) |
| `remove_all_app_assignments` | Remove all assignments for an app, requires `confirm=True` |

### Entra ID User Management (25 tools)

| Tool | Description |
|------|-------------|
| `list_users` | List tenant users (supports filters, pagination) |
| `get_user` | Get user details by ID or UPN |
| `search_users` | Search users by name |
| `create_user` | Create a new Entra ID user |
| `update_user` | Update user properties (name, job title, department, etc.) |
| `delete_user` | Delete a user, requires `confirm=True` |
| `enable_user` | Enable a user account |
| `disable_user` | Disable a user account (block sign-in) |
| `reset_user_password` | Reset user password |
| `revoke_user_sessions` | Revoke all refresh tokens for a user |
| `get_user_devices` | List managed devices for a user |
| `get_user_licenses` | Get license assignments for a user |
| `assign_license` | Assign a license to a user |
| `remove_license` | Remove a license from a user |
| `list_available_licenses` | List available license SKUs in the tenant |
| `get_deleted_users` | List recently deleted users (recoverable within 30 days) |
| `restore_deleted_user` | Restore a deleted user |
| `assign_manager` | Assign a manager to a user |
| `remove_manager` | Remove a user's manager |
| `get_direct_reports` | List direct reports for a user |
| `onboard_user` | Onboard a new user (create account, assign manager, licenses, groups) |
| `offboard_user` | Offboard a user (block sign-in, revoke sessions, remove groups/apps/licenses) |
| `bulk_create_users` | Create multiple users in a single operation |
| `bulk_assign_licenses` | Assign a license to multiple users |
| `bulk_add_to_group` | Add multiple users to a group |

### Entra ID Device Management (8 tools)

| Tool | Description |
|------|-------------|
| `list_entra_devices` | List devices in Entra ID (supports filters, pagination) |
| `search_entra_devices` | Search Entra devices by display name |
| `get_entra_device` | Get details for an Entra ID device |
| `delete_entra_device` | Delete a device from Entra ID, requires `confirm=True` |
| `delete_intune_device` | Delete a device from Intune, requires `confirm=True` |
| `delete_device_from_all` | Delete a device from both Intune and Entra ID, requires `confirm=True` |
| `disable_entra_device` | Disable a device in Entra ID |
| `enable_entra_device` | Enable a device in Entra ID |

### Group Management (12 tools)

| Tool | Description |
|------|-------------|
| `list_groups` | List Azure AD groups |
| `search_groups` | Search groups by name |
| `get_group` | Get group details |
| `create_security_group` | Create a security group |
| `create_microsoft365_group` | Create a Microsoft 365 group |
| `create_dynamic_security_group` | Create a dynamic security group with a membership rule |
| `delete_group` | Delete a group, requires `confirm=True` |
| `get_group_members` | List members of a group |
| `add_group_member` | Add a member to a group |
| `remove_group_member` | Remove a member from a group |
| `get_group_owners` | List owners of a group |
| `add_group_owner` | Add an owner to a group |

### Conditional Access (5 tools)

| Tool | Description |
|------|-------------|
| `list_conditional_access_policies` | List all Conditional Access policies |
| `get_conditional_access_policy` | Get details for a specific CA policy |
| `enable_conditional_access_policy` | Enable a Conditional Access policy |
| `disable_conditional_access_policy` | Disable a Conditional Access policy |
| `list_named_locations` | List named locations used in CA policies |

### Authentication & Identity Protection (7 tools)

| Tool | Description |
|------|-------------|
| `get_user_authentication_methods` | List authentication methods for a user |
| `get_user_mfa_status` | Check MFA status and registered methods for a user |
| `get_sign_in_logs` | Get sign-in logs (filter by user, status, date range) |
| `get_risky_users` | List risky users from Identity Protection |
| `get_risk_detections` | Get risk detections from Identity Protection |
| `dismiss_risky_user` | Dismiss risk for a user |
| `get_directory_audit_logs` | Get directory audit logs (filter by category, date range) |

### App Registrations & Enterprise Apps (11 tools)

| Tool | Description |
|------|-------------|
| `list_app_registrations` | List app registrations with credential expiry info |
| `get_app_registration` | Get app registration details (permissions, credentials) |
| `search_app_registrations` | Search app registrations by name |
| `list_enterprise_apps` | List enterprise apps (service principals) |
| `get_enterprise_app` | Get enterprise app details |
| `search_enterprise_apps` | Search enterprise apps by name |
| `get_app_permissions` | Get permissions granted to an enterprise app |
| `enable_enterprise_app` | Enable an enterprise app |
| `disable_enterprise_app` | Disable an enterprise app |
| `get_credentials_expiring_soon` | List app registrations with credentials expiring within N days |
| `delete_app_registration` | Delete an app registration, requires `confirm=True` |

### Windows 365 Cloud PC (7 tools)

| Tool | Description |
|------|-------------|
| `list_cloud_pcs` | List all Cloud PCs |
| `get_cloud_pc_details` | Get details for a Cloud PC |
| `restart_cloud_pc` | Restart a Cloud PC |
| `reprovision_cloud_pc` | Reprovision a Cloud PC, requires `confirm=True` |
| `list_provisioning_policies` | List Cloud PC provisioning policies |
| `list_gallery_images` | List gallery images available for provisioning |
| `get_cloud_pc_overview` | Get Cloud PC overview and summary |

### Tenant Administration (10 tools)

| Tool | Description |
|------|-------------|
| `get_organization_info` | Get organization/tenant information |
| `get_tenant_domains` | List domains for the tenant |
| `get_service_health` | Get Microsoft 365 service health status |
| `get_service_issues` | Get current and recent service issues (filter by service) |
| `list_directory_roles` | List active directory roles |
| `get_directory_role_members` | List members of a directory role |
| `get_global_admins` | List Global Administrator role members |
| `get_subscriptions` | List subscribed SKUs (licenses) |
| `get_security_defaults_status` | Check security defaults status |
| `assign_directory_role` | Assign a directory role to a user or group |

### Scripts & Remediations (6 tools)

| Tool | Description |
|------|-------------|
| `list_device_management_scripts` | List PowerShell scripts in Intune |
| `get_device_management_script` | Get details for a PowerShell script |
| `get_script_device_status` | Get deployment status for a script |
| `list_device_health_scripts` | List proactive remediation scripts |
| `get_device_health_script` | Get details for a proactive remediation script |
| `get_device_health_script_status` | Get status summary for a proactive remediation script |

### Security & Compliance (11 tools)

| Tool | Description |
|------|-------------|
| `list_security_baselines` | List security baseline templates |
| `list_security_baseline_profiles` | List deployed security baseline profiles |
| `get_security_baseline_status` | Get deployment status for a security baseline |
| `list_app_protection_policies` | List mobile app protection policies (MAM) |
| `list_enrollment_restrictions` | List device enrollment restrictions |
| `list_device_categories` | List device categories |
| `create_device_category` | Create a device category |
| `get_windows_malware_report` | Get Windows malware report |
| `get_device_protection_overview` | Get device protection status overview |
| `get_device_threat_state` | Get threat state for managed Windows devices |
| `get_detected_malware_on_device` | Get detected malware for a specific device |

### Reports (6 tools)

| Tool | Description |
|------|-------------|
| `get_device_compliance_report` | Device compliance summary |
| `get_device_configuration_status` | Deployment status for a configuration profile |
| `get_compliance_policy_status` | Deployment status for a compliance policy |
| `get_app_installation_status` | Installation status for an app |
| `get_license_usage_report` | License usage summary |
| `get_hardware_inventory_report` | Hardware inventory summary |

## Security Considerations

1. **Client Secret Protection**: Never commit client secrets to version control
2. **Least Privilege**: Grant only required permissions
3. **Audit Logging**: Monitor API usage through Azure AD logs
4. **Destructive Actions**: All destructive operations require `confirm=True`

## Example Usage

Once configured, you can ask your AI assistant:

**Device Management**
- "List all Windows devices in my tenant"
- "Show me non-compliant devices"
- "Sync all devices for user john.doe"
- "Show stale devices inactive for 90 days"
- "Rename device X to Y"

**User Management**
- "Create a new user john.doe@company.com"
- "Onboard user with manager, licenses, and group membership"
- "Offboard user john.doe@company.com"
- "Reset password for user X"
- "Show direct reports for manager Y"
- "Bulk create users from this list"

**App & License Management**
- "List all mobile apps"
- "Assign app X to group Y as required"
- "Show me license usage"
- "List available licenses"
- "Show app registrations with expiring credentials"

**Security & Compliance**
- "List all Conditional Access policies"
- "Show MFA status for user X"
- "List risky users"
- "Show Windows malware report"
- "List security baseline profiles"

**Cloud & Infrastructure**
- "Get Cloud PC overview"
- "List all Entra devices"
- "Delete device from both Intune and Entra"
- "Show service health status"
- "List Global Administrators"

### User Offboarding

The `offboard_user` tool provides comprehensive automated offboarding:

```
offboard user john.doe@company.com
```

This will:
1. Block user sign-in
2. Revoke all active sessions
3. Remove from all groups
4. Remove all app assignments
5. Remove all licenses
6. Generate detailed access checklist

The user account is NOT deleted -- it remains disabled for audit purposes.

See [OFFBOARDING_GUIDE.md](OFFBOARDING_GUIDE.md) for detailed documentation.

### User Onboarding

The `onboard_user` tool provides automated onboarding:

```
onboard user with display name "John Doe", UPN john.doe@company.com, manager ID ..., license SKUs [...], group IDs [...]
```

This will:
1. Create the user account
2. Assign a manager
3. Assign specified licenses
4. Add to specified groups
5. Optionally send a welcome email

## Troubleshooting

### Connection Issues
- Verify TENANT_ID, CLIENT_ID, and CLIENT_SECRET are correct
- Check app registration permissions in Azure Portal
- Ensure admin consent is granted for permissions

### Permission Errors
- Review required permissions above
- Grant admin consent in Azure Portal
- Some features require specific licenses (e.g., Entra ID P1/P2)

### Beta API Features
- Some features use Microsoft Graph beta endpoints
- Beta APIs may change without notice

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.
