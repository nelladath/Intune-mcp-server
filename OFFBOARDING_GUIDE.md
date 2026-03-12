# Entra ID User Offboarding Guide

## Overview

The MCP server now includes comprehensive user offboarding capabilities for Entra ID (Azure AD). This feature automates the complete offboarding process while **NOT deleting the user account**, allowing for proper audit trails and potential account recovery.

## Features

### What the Offboarding Does

1. **Blocks User Sign-In** - Disables the account to prevent authentication
2. **Revokes Active Sessions** - Forces sign-out from all devices and applications
3. **Removes Group Memberships** - Removes user from all Entra ID groups
4. **Removes App Assignments** - Removes all enterprise application assignments
5. **Removes Licenses** - Removes all assigned Microsoft 365 licenses
6. **Generates Access Checklist** - Provides detailed report of:
   - Directory role assignments
   - Remaining group memberships (if any failed to remove)
   - Enterprise application access
   - App registrations owned by the user

### What the Offboarding Does NOT Do

- ❌ **Does NOT delete the user** - User account remains in Entra ID (disabled)
- ❌ **Does NOT remove directory role assignments** - These require manual review and removal
- ❌ **Does NOT reassign app registration ownership** - Owned apps must be manually reassigned

## Usage

### Via MCP Tool

```python
# Using the MCP tool directly
result = await offboard_user(user_id="john.doe@contoso.com")
```

### Via Test Script

```bash
# From C:\MCP directory
python test_offboarding.py john.doe@contoso.com
```

### Via MCP Server (from AI Assistant)

When using the MCP server with Claude or another AI assistant:

```
Can you offboard the user john.doe@contoso.com?
```

## Example Output

```
================================================================================
ENTRA ID USER OFFBOARDING TEST
================================================================================

Offboarding user: john.doe@contoso.com

✓ Connected to tenant: Contoso Corporation
  Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Starting offboarding process...

================================================================================
OFFBOARDING COMPLETED
================================================================================

User: John Doe
UPN:  john.doe@contoso.com
ID:   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

--------------------------------------------------------------------------------
ACTIONS TAKEN
--------------------------------------------------------------------------------

✓ SIGN IN BLOCKED
  Status: success
  User sign-in blocked

✓ SESSIONS REVOKED
  Status: success
  All active sessions revoked

✓ GROUP REMOVAL
  Status: success
  Removed from 12 groups
  Groups removed: HR Team, Finance Users, All Employees, Marketing, Sales

✓ APP REMOVAL
  Status: success
  Removed 8 app assignments
  Apps removed: Office 365, Salesforce, ServiceNow, Adobe Creative Cloud

✓ LICENSE REMOVAL
  Status: success
  Removed 2 licenses
  Licenses: ENTERPRISEPACK, POWER_BI_PRO

--------------------------------------------------------------------------------
ACCESS CHECKLIST
--------------------------------------------------------------------------------

[1] DIRECTORY ROLES: 0
    ✓ None

[2] GROUP MEMBERSHIPS: 0
    ✓ All groups removed

[3] ENTERPRISE APPLICATION ACCESS: 0
    ✓ All app assignments removed

[4] APP REGISTRATIONS OWNED: 1
    ⚠️  User owns app registrations - reassign ownership before full offboarding
    - Contoso Mobile App

================================================================================
✓ OFFBOARDING CHECKLIST COMPLETE
================================================================================

Status: success
Message: User 'John Doe' offboarding completed
```

## Important Notes

### Manual Steps Required After Offboarding

1. **Directory Roles**: If the user has directory role assignments (e.g., Global Administrator, User Administrator), these must be manually reviewed and removed as they are highly privileged.

2. **App Registration Ownership**: If the user owns any app registrations, ownership should be reassigned to another user or service account before full decommissioning.

3. **OneDrive/Mailbox**: This offboarding process does NOT handle:
   - OneDrive data retention/transfer
   - Exchange mailbox conversion to shared mailbox
   - Teams chat history
   
   These should be handled separately according to your organization's data retention policies.

4. **Manager/Direct Reports**: The offboarding does not update the user's manager or reassign direct reports. Update these relationships as needed.

### Error Handling

The offboarding function is designed to be resilient:
- If one step fails, it continues with the remaining steps
- Each action includes a status indicating success, partial success, or failure
- Failed operations are logged with specific error messages
- The access checklist shows what couldn't be removed

### Comparison to PowerShell Script

This implementation matches the functionality of the provided PowerShell script:

| Feature | PowerShell Script | MCP Implementation | Status |
|---------|------------------|-------------------|---------|
| Block Sign-In | ✓ | ✓ | Implemented |
| Revoke Sessions | ✓ | ✓ | Implemented |
| Remove Groups | ✓ | ✓ | Implemented |
| Remove App Assignments | ✓ | ✓ | Implemented |
| Remove Licenses | ✓ | ✓ | Implemented |
| Directory Roles Check | ✓ | ✓ | Implemented |
| Group Membership Check | ✓ | ✓ | Implemented |
| App Access Check | ✓ | ✓ | Implemented |
| Owned Apps Check | ✓ | ✓ | Implemented |
| Does NOT Delete User | ✓ | ✓ | Implemented |

## API Permissions Required

The MCP server must have the following Microsoft Graph API permissions:

### Required Permissions
- `User.ReadWrite.All` - Read and write user accounts
- `Group.ReadWrite.All` - Manage group memberships
- `Directory.ReadWrite.All` - Read directory roles and app assignments
- `AppRoleAssignment.ReadWrite.All` - Manage app role assignments

### Recommended Additional Permissions
- `RoleManagement.Read.All` - Read directory role assignments
- `Application.Read.All` - Read app registrations

## Security Considerations

1. **Audit Trail**: The user account is NOT deleted, maintaining a complete audit trail
2. **Reversible**: Most actions can be reversed if needed (except session revocation)
3. **Detailed Logging**: The function provides comprehensive logging of all actions
4. **Privileged Operation**: This is a privileged operation - ensure proper access controls

## Testing

Before using in production:

1. Test with a test user account first
2. Review the access checklist carefully
3. Verify all groups, apps, and licenses were removed
4. Confirm the user cannot sign in

## Troubleshooting

### Common Issues

**Issue**: Group removal fails for certain groups
- **Solution**: Some groups may be system-managed or have removal restrictions. Review the failed groups list and remove manually if needed.

**Issue**: License removal fails
- **Solution**: Ensure the service account has proper permissions and the licenses are not being inherited from group-based licensing.

**Issue**: App assignments remain
- **Solution**: Some app assignments may be managed through groups. Remove group memberships first.

### Verification

To verify offboarding was successful:

```bash
# Check user status
python test_offboarding.py john.doe@contoso.com

# Look for:
# - Account Enabled: False
# - All groups removed
# - All licenses removed
# - All app assignments removed
```

## Support

For issues or questions:
1. Check the error messages in the offboarding report
2. Verify API permissions are correctly configured
3. Review the access checklist for items requiring manual intervention
4. Consult the Microsoft Graph API documentation for specific errors

## Future Enhancements

Potential improvements:
- [ ] OneDrive data transfer automation
- [ ] Mailbox conversion to shared mailbox
- [ ] Automatic directory role removal (with confirmation)
- [ ] Bulk offboarding support
- [ ] Scheduled offboarding
- [ ] Integration with HR systems
