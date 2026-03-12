# Intune MCP Server - Gap Analysis & Missing Features

## Executive Summary
This document identifies missing automation capabilities in the Intune MCP Server compared to complete Intune and Entra ID management requirements.

**Total Functions Implemented**: ~183 functions across 16 modules  
**Priority Gaps Identified**: 47 high-priority missing features  
**Estimated Implementation**: Medium to High effort

---

## 1. USER LIFECYCLE MANAGEMENT

### ✅ Currently Implemented:
- User CRUD operations (create, read, update, delete)
- Enable/disable users
- Password reset & session revocation
- License assignment/removal
- User offboarding (comprehensive)
- User search and listing
- Get deleted users & restore

### ❌ MISSING - High Priority:

#### User Onboarding Automation
- [ ] **Bulk user creation from CSV/template** - Critical for mass onboarding
- [ ] **User onboarding workflow** - Complete onboarding with:
  - Create user account
  - Assign licenses automatically based on department/role
  - Add to appropriate groups based on attributes
  - Assign manager
  - Send welcome email with credentials
  - Provision apps automatically
  - Set default devices/policies
- [ ] **Manager assignment** - Set/update manager relationship
- [ ] **Direct reports management** - Get/manage direct reports
- [ ] **User profile photo management** - Upload/update/delete profile photos
- [ ] **Guest user invitation** - Send B2B guest invitations
- [ ] **Bulk license operations** - Assign/remove licenses for multiple users at once

#### User Account Management
- [ ] **User activity reports** - Last login, app usage, device access
- [ ] **Inactive user detection** - Find users who haven't logged in for X days
- [ ] **User license optimization** - Identify unused licenses
- [ ] **User mailbox size report** - Exchange mailbox usage
- [ ] **User OneDrive usage** - Storage consumption per user

---

## 2. GROUP MANAGEMENT

### ✅ Currently Implemented:
- Group CRUD (security, M365, dynamic)
- Add/remove members
- Get group owners
- Add group owners
- Search groups

### ❌ MISSING - High Priority:

#### Advanced Group Operations
- [ ] **Bulk group member operations** - Add/remove multiple members at once
- [ ] **Group membership sync** - Sync with external source
- [ ] **Nested group management** - Add/remove groups as members
- [ ] **Group expiry policy management** - Set/update expiration policies
- [ ] **Group naming policy** - Enforce naming conventions
- [ ] **Group provisioning status** - Check provisioning status for M365 groups
- [ ] **Group-based license assignment** - Manage group-based licensing
- [ ] **Remove group owner** - Currently missing
- [ ] **Update group properties** - Update description, visibility, etc.
- [ ] **Clone group** - Duplicate group with members/settings

---

## 3. DEVICE MANAGEMENT

### ✅ Currently Implemented:
- List/search managed devices
- Get device details
- Sync, restart, remote lock
- Wipe, retire devices
- Autopilot device listing
- Entra device management
- Device compliance reports

### ❌ MISSING - Critical Priority:

#### Device Lifecycle
- [ ] **Device enrollment** - Enroll new devices via API
- [ ] **Bulk device actions** - Sync/restart/retire multiple devices
- [ ] **Device rename** - Change device name remotely
- [ ] **Device ownership change** - Change between corporate/personal
- [ ] **Lost mode (iOS)** - Enable/disable lost mode
- [ ] **Activation lock bypass (iOS)** - Bypass activation lock
- [ ] **BitLocker key rotation** - Rotate BitLocker recovery keys
- [ ] **FileVault key management** - Manage macOS FileVault keys

#### Device Inventory & Reporting
- [ ] **Device hardware inventory** - Detailed hardware specs (CPU, RAM, disk)
- [ ] **Device installed apps inventory** - List all apps on device
- [ ] **Device certificate inventory** - List certificates on device
- [ ] **Device network info** - IP address, MAC, network adapters
- [ ] **Device battery health report** - Battery status for mobile devices
- [ ] **Device disk encryption status** - BitLocker/FileVault status
- [ ] **Device patch compliance** - Missing patches per device
- [ ] **Device location tracking** - Geographic location (if enabled)
- [ ] **Device last logged-in user** - User activity tracking

#### Device Actions
- [ ] **Device screenshot capture** - Capture screen (Android Enterprise)
- [ ] **Fresh start** - Reinstall Windows without user data
- [ ] **Collect diagnostics** - Trigger diagnostic collection
- [ ] **Custom device notifications** - Send notifications to devices
- [ ] **Rotate local admin password** - LAPS rotation

---

## 4. PATCH & UPDATE MANAGEMENT

### ✅ Currently Implemented:
- None

### ❌ MISSING - CRITICAL:

#### Windows Update Management
- [ ] **Windows Update rings** - List/create/update update rings
- [ ] **Update ring assignment** - Assign rings to groups
- [ ] **Feature update policies** - Manage Windows 10/11 feature updates
- [ ] **Quality update policies** - Manage quality updates
- [ ] **Driver update policies** - Manage driver updates
- [ ] **Update compliance report** - Patch status per device
- [ ] **Pending updates report** - Updates waiting to install
- [ ] **Failed updates report** - Update failures with error codes
- [ ] **Pause updates** - Pause updates for specific devices/groups
- [ ] **Expedite updates** - Force install updates immediately

#### iOS/macOS Update Management
- [ ] **iOS update policies** - Manage iOS/iPadOS updates
- [ ] **macOS update policies** - Manage macOS updates
- [ ] **Software update compliance** - OS version compliance

---

## 5. APPLICATION MANAGEMENT

### ✅ Currently Implemented:
- List mobile apps
- Get app details
- Search apps
- Get app installation status
- Get app assignments

### ❌ MISSING - High Priority:

#### App Deployment
- [ ] **App upload/create** - Upload new app packages (Win32, MSI, etc.)
- [ ] **App assignment** - Assign app to groups
- [ ] **App unassignment** - Remove app assignments
- [ ] **App supersedence** - Configure app supersedence relationships
- [ ] **App dependencies** - Set app dependencies
- [ ] **App requirements** - Configure install requirements
- [ ] **App detection rules** - Custom detection rules
- [ ] **App update** - Update existing app packages
- [ ] **App retirement** - Retire/delete apps

#### App Monitoring
- [ ] **App failure logs** - Installation failure details
- [ ] **App inventory per device** - Apps installed on specific device
- [ ] **App usage analytics** - App usage statistics
- [ ] **App version compliance** - Devices with outdated app versions
- [ ] **Managed app logs** - MAM app logs

---

## 6. POLICY & COMPLIANCE MANAGEMENT

### ✅ Currently Implemented:
- List compliance policies
- Get compliance policy details
- List configuration profiles
- Get profile assignments
- Get policy deployment status

### ❌ MISSING - High Priority:

#### Policy Creation & Management
- [ ] **Create compliance policy** - Create new compliance policies
- [ ] **Update compliance policy** - Modify existing policies
- [ ] **Delete compliance policy** - Remove policies
- [ ] **Assign compliance policy** - Assign to groups
- [ ] **Create configuration profile** - Create new config profiles
- [ ] **Update configuration profile** - Modify profiles
- [ ] **Delete configuration profile** - Remove profiles
- [ ] **Assign configuration profile** - Assign to groups
- [ ] **Policy conflict detection** - Identify conflicting policies
- [ ] **Policy precedence management** - Set policy priority

#### Compliance Actions
- [ ] **Noncompliance actions** - Configure actions for noncompliant devices
- [ ] **Compliance notifications** - Send notifications to users
- [ ] **Conditional access integration** - Link to CA policies
- [ ] **Compliance grace period** - Set grace periods

---

## 7. CONDITIONAL ACCESS & SECURITY

### ✅ Currently Implemented:
- List CA policies
- Get CA policy details
- Enable/disable CA policies
- List named locations
- MFA status
- Risky users
- Risk detections
- Sign-in logs
- Audit logs

### ❌ MISSING - High Priority:

#### Conditional Access Management
- [ ] **Create CA policy** - Create new CA policies
- [ ] **Update CA policy** - Modify existing policies
- [ ] **Delete CA policy** - Remove policies
- [ ] **Create named location** - Add IP ranges/countries
- [ ] **Update named location** - Modify locations
- [ ] **Delete named location** - Remove locations
- [ ] **Policy simulation** - Test CA policy impact (What-If)
- [ ] **Policy impact report** - Users affected by policies

#### Authentication & MFA
- [ ] **Force MFA registration** - Require user to register MFA
- [ ] **Reset MFA** - Reset user MFA methods
- [ ] **FIDO2 key management** - Manage hardware keys
- [ ] **Temporary Access Pass** - Generate TAP for users
- [ ] **Authentication strength policies** - Manage auth strengths

---

## 8. REPORTING & ANALYTICS

### ✅ Currently Implemented:
- Device compliance report
- License usage report
- Hardware inventory report
- App installation status
- Configuration/policy status

### ❌ MISSING - Medium Priority:

#### Advanced Reports
- [ ] **Executive dashboard** - High-level summary for management
- [ ] **Compliance trend report** - Compliance over time
- [ ] **Device enrollment report** - New devices per day/week
- [ ] **User sign-in analytics** - Sign-in patterns and anomalies
- [ ] **Application usage report** - Most/least used apps
- [ ] **Policy effectiveness report** - Policy success rates
- [ ] **Security posture report** - Overall security score
- [ ] **Cost optimization report** - License waste, unused devices
- [ ] **Change audit report** - Who changed what and when
- [ ] **Device aging report** - Old devices needing replacement
- [ ] **Stale device cleanup** - Devices not synced in X days

---

## 9. AUTOPILOT & PROVISIONING

### ✅ Currently Implemented:
- List Autopilot devices
- List Autopilot profiles
- Get Autopilot device details

### ❌ MISSING - High Priority:

#### Autopilot Management
- [ ] **Import Autopilot devices** - Bulk import from CSV
- [ ] **Delete Autopilot device** - Remove device identity
- [ ] **Assign Autopilot profile** - Assign profile to device
- [ ] **Unassign Autopilot profile** - Remove profile assignment
- [ ] **Create Autopilot profile** - Create new deployment profile
- [ ] **Update Autopilot profile** - Modify existing profile
- [ ] **Delete Autopilot profile** - Remove profile
- [ ] **Sync Autopilot devices** - Sync from Store for Business
- [ ] **Autopilot deployment status** - Track deployment progress

---

## 10. ROLE-BASED ACCESS CONTROL (RBAC)

### ✅ Currently Implemented:
- List directory roles
- Get role members
- Add directory role member (user)
- Remove directory role member
- Assign directory role (user/group) - **JUST ADDED**

### ❌ MISSING - High Priority:

#### Intune RBAC
- [ ] **List Intune roles** - Built-in and custom roles
- [ ] **Create custom Intune role** - Create role with specific permissions
- [ ] **Update Intune role** - Modify role permissions
- [ ] **Delete Intune role** - Remove custom role
- [ ] **Assign Intune role** - Assign role to users/groups
- [ ] **Role scope tags** - Manage scope tags
- [ ] **Role assignment report** - Who has what permissions

---

## 11. TENANT ADMINISTRATION

### ✅ Currently Implemented:
- Organization info
- Tenant domains
- Service health
- Service issues
- Directory roles
- Subscriptions
- Security defaults status

### ❌ MISSING - Medium Priority:

#### Tenant Configuration
- [ ] **Tenant branding** - Update login page branding
- [ ] **Company information** - Update company details
- [ ] **Mobile device management authority** - Set MDM authority
- [ ] **Data retention policies** - Configure retention
- [ ] **Diagnostic settings** - Configure logging
- [ ] **Custom domain management** - Add/verify/remove domains
- [ ] **Certificate management** - Upload/manage certificates

---

## 12. MOBILE APPLICATION MANAGEMENT (MAM)

### ✅ Currently Implemented:
- List app protection policies

### ❌ MISSING - High Priority:

#### MAM Policy Management
- [ ] **Create app protection policy** - iOS/Android/Windows
- [ ] **Update app protection policy** - Modify policies
- [ ] **Delete app protection policy** - Remove policies
- [ ] **Assign app protection policy** - Assign to users/groups
- [ ] **App config policies** - Managed app configuration
- [ ] **MAM policy compliance** - Check user compliance
- [ ] **Selective wipe** - Wipe corporate data only
- [ ] **MAM app logs** - Get app logs from users

---

## 13. CORPORATE IDENTIFIERS & ENROLLMENT

### ✅ Currently Implemented:
- Enrollment restrictions listing

### ❌ MISSING - High Priority:

#### Enrollment Management
- [ ] **Corporate identifiers** - Add/remove IMEI/serial numbers
- [ ] **Device enrollment manager** - Manage DEM accounts
- [ ] **Enrollment restrictions** - Create/update restrictions
- [ ] **Terms and conditions** - Manage T&C for enrollment
- [ ] **Apple DEP tokens** - Manage Apple Business Manager tokens
- [ ] **Apple VPP tokens** - Manage Volume Purchase Program
- [ ] **Android Enterprise binding** - Manage Android Enterprise
- [ ] **Enrollment profiles (iOS)** - Apple DEP profiles

---

## 14. PARTNER INTEGRATION & COMPLIANCE

### ✅ Currently Implemented:
- None

### ❌ MISSING - Medium Priority:

#### Third-Party Integration
- [ ] **Mobile Threat Defense** - MTD connector management
- [ ] **Compliance partners** - Jamf, SOTI, etc.
- [ ] **Certificate connectors** - SCEP, PFX connectors
- [ ] **Telecom expense management** - TEM integration
- [ ] **Partner compliance status** - Partner device compliance

---

## 15. NOTIFICATION & COMMUNICATION

### ✅ Currently Implemented:
- None

### ❌ MISSING - High Priority:

#### User Communication
- [ ] **Send custom notifications** - Notify specific users
- [ ] **Email templates** - Manage notification templates
- [ ] **Company portal branding** - Customize Company Portal
- [ ] **Welcome email** - Send onboarding emails
- [ ] **Compliance notifications** - Auto-notify noncompliant users

---

## 16. BACKUP & DISASTER RECOVERY

### ✅ Currently Implemented:
- None

### ❌ MISSING - Medium Priority:

#### Configuration Backup
- [ ] **Export configuration** - Backup all policies/profiles
- [ ] **Import configuration** - Restore from backup
- [ ] **Policy versioning** - Track policy changes
- [ ] **Rollback policies** - Revert to previous version
- [ ] **Configuration drift detection** - Detect manual changes

---

## PRIORITY IMPLEMENTATION ROADMAP

### Phase 1 - CRITICAL (Immediate Need)
1. **User onboarding workflow** - Complete automation
2. **Patch management** - Windows Update rings & compliance
3. **Policy creation/assignment** - Compliance & config profiles
4. **Bulk operations** - Users, devices, groups
5. **App deployment** - Upload & assign apps

### Phase 2 - HIGH (Next Quarter)
6. **Device inventory** - Hardware, apps, certificates
7. **MAM policy management** - App protection policies
8. **Conditional Access management** - Create/update CA policies
9. **Autopilot management** - Import, assign, deploy
10. **Advanced reporting** - Executive dashboards

### Phase 3 - MEDIUM (Future)
11. **RBAC management** - Intune roles
12. **Enrollment management** - Corporate identifiers, DEP/VPP
13. **Backup & recovery** - Configuration export/import
14. **Partner integrations** - MTD, compliance partners
15. **Notification system** - Custom user communications

---

## IMPLEMENTATION ESTIMATES

| Feature Category | Functions Needed | Estimated Effort | Business Impact |
|-----------------|------------------|------------------|-----------------|
| User Onboarding | 8 functions | 2-3 weeks | CRITICAL |
| Patch Management | 10 functions | 3-4 weeks | CRITICAL |
| Policy Management | 12 functions | 3-4 weeks | CRITICAL |
| Device Inventory | 15 functions | 2-3 weeks | HIGH |
| App Deployment | 10 functions | 3-4 weeks | HIGH |
| Bulk Operations | 6 functions | 1-2 weeks | HIGH |
| MAM Management | 8 functions | 2 weeks | HIGH |
| CA Management | 8 functions | 2 weeks | HIGH |
| Reporting | 12 functions | 2-3 weeks | MEDIUM |
| Other | 20+ functions | 4-6 weeks | MEDIUM |

**Total Estimated Effort**: 25-35 weeks (with 1 developer)

---

## RECOMMENDED NEXT STEPS

1. **Immediate Actions**:
   - Implement user onboarding workflow (most requested)
   - Add patch management capabilities (compliance requirement)
   - Create policy management functions (blocking many use cases)

2. **Quick Wins** (< 1 week each):
   - Manager assignment/direct reports
   - Bulk group member operations
   - Device rename
   - Remove group owner
   - User profile photos

3. **Customer Delivery Considerations**:
   - Document limitations clearly
   - Provide workarounds for missing features
   - Create priority list based on customer needs
   - Plan incremental releases

---

## CONCLUSION

The current MCP server has **excellent coverage** for:
- ✅ User management (80% complete)
- ✅ Group basics (70% complete)
- ✅ Device monitoring (75% complete)
- ✅ Reporting (60% complete)
- ✅ Security & authentication (70% complete)

**Critical gaps** exist in:
- ❌ User onboarding automation (20% complete)
- ❌ Patch management (0% complete)
- ❌ Policy creation/assignment (20% complete)
- ❌ App deployment (30% complete)
- ❌ Bulk operations (10% complete)

**Recommendation**: Focus on Phase 1 critical features before customer delivery to ensure the MCP can handle complete Intune management workflows, not just monitoring and basic operations.
