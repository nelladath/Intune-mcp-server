# User Offboarding - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Option 1: Via AI Assistant (Easiest)

If your MCP server is configured in Cursor/Claude:

```
You: Offboard user john.doe@contoso.com

AI: I'll perform a comprehensive offboarding for that user...
```

The AI will automatically call the `offboard_user` tool and provide a detailed report.

---

### Option 2: Via Test Script

```bash
cd C:\MCP
python test_offboarding.py john.doe@contoso.com
```

This will:
1. Connect to your tenant
2. Perform complete offboarding
3. Display a formatted report with all actions taken

---

### Option 3: Programmatic

```python
import asyncio
from intune_mcp_server.tools.entra_users import offboard_user

async def main():
    result = await offboard_user("john.doe@contoso.com")
    print(result)

asyncio.run(main())
```

---

## 📋 What Happens During Offboarding?

### Automatic Actions (All Completed Automatically)

1. **🚫 Block Sign-In**
   - User account is disabled
   - Cannot authenticate to any service

2. **🔄 Revoke Sessions**
   - All active sessions terminated
   - User signed out of all devices

3. **👥 Remove Groups**
   - Removed from all Entra ID groups
   - Includes security groups and M365 groups

4. **📱 Remove Apps**
   - All enterprise app assignments removed
   - Access to SaaS apps revoked

5. **📄 Remove Licenses**
   - All M365 licenses removed
   - License freed for reassignment

6. **✅ Generate Report**
   - Detailed checklist of actions
   - Lists any remaining access

### Manual Review Required

After offboarding, you may need to manually:

- **Directory Roles**: Remove any admin role assignments
- **App Ownership**: Reassign owned app registrations
- **OneDrive**: Transfer or archive data
- **Mailbox**: Convert to shared mailbox if needed

---

## 📊 Example Output

```
================================================================================
OFFBOARDING COMPLETED
================================================================================

User: John Doe
UPN:  john.doe@contoso.com

--------------------------------------------------------------------------------
ACTIONS TAKEN
--------------------------------------------------------------------------------

✓ SIGN IN BLOCKED
  Status: success

✓ SESSIONS REVOKED
  Status: success

✓ GROUP REMOVAL
  Status: success
  Removed from 12 groups

✓ APP REMOVAL
  Status: success
  Removed 8 app assignments

✓ LICENSE REMOVAL
  Status: success
  Removed 2 licenses

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
    ⚠️  User owns app registrations - reassign ownership

================================================================================
✓ OFFBOARDING COMPLETE
================================================================================
```

---

## ⚡ Common Scenarios

### Scenario 1: Employee Leaving

```
offboard user employee@company.com
```

Result: Account disabled, all access removed, ready for final cleanup.

### Scenario 2: Testing New Employee Onboarding

```
# Create test user
create user "Test User" test.user@company.com

# Later, offboard
offboard user test.user@company.com
```

### Scenario 3: Contractor End of Engagement

```
offboard user contractor@company.com
```

Account remains for audit purposes but has no access.

---

## ❓ FAQ

### Q: Will this delete the user?
**A:** No! The user account is disabled but NOT deleted. It remains for audit purposes.

### Q: Can I reverse the offboarding?
**A:** Mostly yes. You can re-enable the account, reassign groups, licenses, and apps. Session revocation cannot be reversed (user just signs in again).

### Q: What if offboarding fails partway through?
**A:** The function is resilient - it continues even if one step fails. You'll get a detailed report showing what succeeded and what failed.

### Q: How long does it take?
**A:** Usually 10-30 seconds depending on the number of groups, apps, and licenses.

### Q: What permissions do I need?
**A:** Your app registration needs:
- `User.ReadWrite.All`
- `Group.ReadWrite.All`
- `Directory.ReadWrite.All`
- `AppRoleAssignment.ReadWrite.All`

---

## 🔗 More Information

- **Detailed Guide**: See [OFFBOARDING_GUIDE.md](OFFBOARDING_GUIDE.md)
- **Implementation Details**: See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Main README**: See [README.md](README.md)

---

## 🆘 Troubleshooting

### Error: "User not found"
- Check the UPN is correct
- Verify the user exists in Entra ID

### Error: "Insufficient permissions"
- Check app registration permissions in Azure Portal
- Ensure admin consent is granted

### Error: "Could not remove from group X"
- Some groups may have removal restrictions
- Remove manually or check group settings

---

## ✅ Verification Steps

After offboarding:

1. **Try to sign in as the user** → Should fail
2. **Check groups** → Should have 0 groups
3. **Check licenses** → Should have 0 licenses
4. **Check app access** → Should have 0 apps
5. **Check account status** → Should be "Disabled"

---

## 📞 Need Help?

1. Read the detailed guide: `OFFBOARDING_GUIDE.md`
2. Check the implementation summary: `IMPLEMENTATION_SUMMARY.md`
3. Review API permissions in Azure Portal
4. Check the error messages in the offboarding report
