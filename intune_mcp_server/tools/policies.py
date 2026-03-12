"""Policy and Compliance Management Tools for Intune MCP Server."""

from typing import Any
from mcp.server import Server

from ..graph_client import get_graph_client


def register_policy_tools(server: Server):
    """Register all policy management tools with the MCP server."""
    
    @server.tool()
    async def list_compliance_policies() -> dict[str, Any]:
        """
        List all device compliance policies.
        
        Returns:
            List of compliance policies
        """
        client = get_graph_client()
        
        response = await client.get("/deviceManagement/deviceCompliancePolicies")
        policies = response.get("value", [])
        
        return {
            "count": len(policies),
            "policies": [
                {
                    "id": p.get("id"),
                    "displayName": p.get("displayName"),
                    "description": p.get("description"),
                    "policyType": p.get("@odata.type", "").replace("#microsoft.graph.", ""),
                    "createdDateTime": p.get("createdDateTime"),
                    "lastModifiedDateTime": p.get("lastModifiedDateTime"),
                    "version": p.get("version"),
                }
                for p in policies
            ]
        }
    
    @server.tool()
    async def get_compliance_policy_details(policy_id: str) -> dict[str, Any]:
        """
        Get detailed information about a compliance policy.
        
        Args:
            policy_id: The compliance policy ID
        
        Returns:
            Policy details including settings and assignments
        """
        client = get_graph_client()
        
        # Get policy details
        policy = await client.get(f"/deviceManagement/deviceCompliancePolicies/{policy_id}")
        
        # Get assignments
        try:
            assignments = await client.get(
                f"/deviceManagement/deviceCompliancePolicies/{policy_id}/assignments"
            )
            assignment_list = assignments.get("value", [])
        except Exception:
            assignment_list = []
        
        # Get device status overview
        try:
            status = await client.get(
                f"/deviceManagement/deviceCompliancePolicies/{policy_id}/deviceStatusOverview"
            )
        except Exception:
            status = {}
        
        return {
            "policy": {
                "id": policy.get("id"),
                "displayName": policy.get("displayName"),
                "description": policy.get("description"),
                "policyType": policy.get("@odata.type", "").replace("#microsoft.graph.", ""),
                "createdDateTime": policy.get("createdDateTime"),
                "lastModifiedDateTime": policy.get("lastModifiedDateTime"),
            },
            "device_status_overview": {
                "pendingCount": status.get("pendingCount"),
                "notApplicableCount": status.get("notApplicableCount"),
                "successCount": status.get("successCount"),
                "errorCount": status.get("errorCount"),
                "failedCount": status.get("failedCount"),
                "lastUpdateDateTime": status.get("lastUpdateDateTime"),
            },
            "assignments": [
                {
                    "id": a.get("id"),
                    "targetType": a.get("target", {}).get("@odata.type", "").replace("#microsoft.graph.", ""),
                    "groupId": a.get("target", {}).get("groupId"),
                }
                for a in assignment_list
            ]
        }
    
    @server.tool()
    async def list_configuration_profiles() -> dict[str, Any]:
        """
        List all device configuration profiles.
        
        Returns:
            List of configuration profiles
        """
        client = get_graph_client()
        
        response = await client.get("/deviceManagement/deviceConfigurations")
        configs = response.get("value", [])
        
        return {
            "count": len(configs),
            "profiles": [
                {
                    "id": c.get("id"),
                    "displayName": c.get("displayName"),
                    "description": c.get("description"),
                    "profileType": c.get("@odata.type", "").replace("#microsoft.graph.", ""),
                    "createdDateTime": c.get("createdDateTime"),
                    "lastModifiedDateTime": c.get("lastModifiedDateTime"),
                    "version": c.get("version"),
                }
                for c in configs
            ]
        }
    
    @server.tool()
    async def get_configuration_profile_details(profile_id: str) -> dict[str, Any]:
        """
        Get detailed information about a configuration profile.
        
        Args:
            profile_id: The configuration profile ID
        
        Returns:
            Profile details including assignments and status
        """
        client = get_graph_client()
        
        profile = await client.get(f"/deviceManagement/deviceConfigurations/{profile_id}")
        
        # Get assignments
        try:
            assignments = await client.get(
                f"/deviceManagement/deviceConfigurations/{profile_id}/assignments"
            )
            assignment_list = assignments.get("value", [])
        except Exception:
            assignment_list = []
        
        # Get status overview
        try:
            status = await client.get(
                f"/deviceManagement/deviceConfigurations/{profile_id}/deviceStatusOverview"
            )
        except Exception:
            status = {}
        
        return {
            "profile": {
                "id": profile.get("id"),
                "displayName": profile.get("displayName"),
                "description": profile.get("description"),
                "profileType": profile.get("@odata.type", "").replace("#microsoft.graph.", ""),
                "createdDateTime": profile.get("createdDateTime"),
                "lastModifiedDateTime": profile.get("lastModifiedDateTime"),
            },
            "device_status_overview": {
                "pendingCount": status.get("pendingCount"),
                "notApplicableCount": status.get("notApplicableCount"),
                "successCount": status.get("successCount"),
                "errorCount": status.get("errorCount"),
                "failedCount": status.get("failedCount"),
            },
            "assignments": [
                {
                    "id": a.get("id"),
                    "targetType": a.get("target", {}).get("@odata.type", "").replace("#microsoft.graph.", ""),
                    "groupId": a.get("target", {}).get("groupId"),
                }
                for a in assignment_list
            ]
        }
    
    @server.tool()
    async def assign_compliance_policy(
        policy_id: str,
        group_id: str
    ) -> dict[str, Any]:
        """
        Assign a compliance policy to a group.
        
        Args:
            policy_id: The compliance policy ID
            group_id: The Azure AD group ID
        
        Returns:
            Status of the assignment
        """
        client = get_graph_client()
        
        policy = await client.get(
            f"/deviceManagement/deviceCompliancePolicies/{policy_id}?$select=displayName"
        )
        group = await client.get(f"/groups/{group_id}?$select=displayName")
        
        assignment_body = {
            "assignments": [
                {
                    "target": {
                        "@odata.type": "#microsoft.graph.groupAssignmentTarget",
                        "groupId": group_id
                    }
                }
            ]
        }
        
        await client.post(
            f"/deviceManagement/deviceCompliancePolicies/{policy_id}/assign",
            json=assignment_body
        )
        
        return {
            "status": "success",
            "message": f"Policy '{policy.get('displayName')}' assigned to group '{group.get('displayName')}'",
            "policy_id": policy_id,
            "group_id": group_id
        }
    
    @server.tool()
    async def assign_configuration_profile(
        profile_id: str,
        group_id: str
    ) -> dict[str, Any]:
        """
        Assign a configuration profile to a group.
        
        Args:
            profile_id: The configuration profile ID
            group_id: The Azure AD group ID
        
        Returns:
            Status of the assignment
        """
        client = get_graph_client()
        
        profile = await client.get(
            f"/deviceManagement/deviceConfigurations/{profile_id}?$select=displayName"
        )
        group = await client.get(f"/groups/{group_id}?$select=displayName")
        
        assignment_body = {
            "assignments": [
                {
                    "target": {
                        "@odata.type": "#microsoft.graph.groupAssignmentTarget",
                        "groupId": group_id
                    }
                }
            ]
        }
        
        await client.post(
            f"/deviceManagement/deviceConfigurations/{profile_id}/assign",
            json=assignment_body
        )
        
        return {
            "status": "success",
            "message": f"Profile '{profile.get('displayName')}' assigned to group '{group.get('displayName')}'",
            "profile_id": profile_id,
            "group_id": group_id
        }
    
    @server.tool()
    async def list_conditional_access_policies() -> dict[str, Any]:
        """
        List all Conditional Access policies.
        
        Returns:
            List of Conditional Access policies
        """
        client = get_graph_client()
        
        response = await client.get("/identity/conditionalAccess/policies")
        policies = response.get("value", [])
        
        return {
            "count": len(policies),
            "policies": [
                {
                    "id": p.get("id"),
                    "displayName": p.get("displayName"),
                    "state": p.get("state"),
                    "createdDateTime": p.get("createdDateTime"),
                    "modifiedDateTime": p.get("modifiedDateTime"),
                }
                for p in policies
            ]
        }
    
    @server.tool()
    async def get_conditional_access_policy(policy_id: str) -> dict[str, Any]:
        """
        Get details of a Conditional Access policy.
        
        Args:
            policy_id: The policy ID
        
        Returns:
            Policy details including conditions and grant controls
        """
        client = get_graph_client()
        
        policy = await client.get(f"/identity/conditionalAccess/policies/{policy_id}")
        
        return {
            "id": policy.get("id"),
            "displayName": policy.get("displayName"),
            "state": policy.get("state"),
            "conditions": {
                "users": policy.get("conditions", {}).get("users", {}),
                "applications": policy.get("conditions", {}).get("applications", {}),
                "platforms": policy.get("conditions", {}).get("platforms", {}),
                "locations": policy.get("conditions", {}).get("locations", {}),
                "clientAppTypes": policy.get("conditions", {}).get("clientAppTypes", []),
            },
            "grantControls": policy.get("grantControls", {}),
            "sessionControls": policy.get("sessionControls", {}),
        }
    
    @server.tool()
    async def get_policy_compliance_report() -> dict[str, Any]:
        """
        Get an overall compliance report across all policies.
        
        Returns:
            Summary of compliance status across all policies
        """
        client = get_graph_client()
        
        # Get all compliance policies
        policies = await client.get("/deviceManagement/deviceCompliancePolicies")
        policy_list = policies.get("value", [])
        
        report = []
        for policy in policy_list:
            try:
                status = await client.get(
                    f"/deviceManagement/deviceCompliancePolicies/{policy['id']}/deviceStatusOverview"
                )
                report.append({
                    "policy_name": policy.get("displayName"),
                    "policy_id": policy.get("id"),
                    "success": status.get("successCount", 0),
                    "pending": status.get("pendingCount", 0),
                    "failed": status.get("failedCount", 0),
                    "error": status.get("errorCount", 0),
                    "not_applicable": status.get("notApplicableCount", 0),
                })
            except Exception:
                report.append({
                    "policy_name": policy.get("displayName"),
                    "policy_id": policy.get("id"),
                    "status": "Unable to retrieve"
                })
        
        return {
            "total_policies": len(report),
            "policy_reports": report
        }
    
    @server.tool()
    async def list_windows_update_rings() -> dict[str, Any]:
        """
        List Windows Update for Business rings.
        
        Returns:
            List of Windows Update rings
        """
        client = get_graph_client()
        
        response = await client.get("/deviceManagement/deviceConfigurations?$filter=isof('microsoft.graph.windowsUpdateForBusinessConfiguration')")
        rings = response.get("value", [])
        
        return {
            "count": len(rings),
            "update_rings": [
                {
                    "id": r.get("id"),
                    "displayName": r.get("displayName"),
                    "description": r.get("description"),
                    "qualityUpdatesDeferralPeriodInDays": r.get("qualityUpdatesDeferralPeriodInDays"),
                    "featureUpdatesDeferralPeriodInDays": r.get("featureUpdatesDeferralPeriodInDays"),
                    "automaticUpdateMode": r.get("automaticUpdateMode"),
                }
                for r in rings
            ]
        }
    
    @server.tool()
    async def list_security_baselines() -> dict[str, Any]:
        """
        List security baseline profiles (using beta endpoint).
        
        Returns:
            List of security baselines
        """
        client = get_graph_client()
        
        # Security baselines are in beta
        response = await client.get(
            "/deviceManagement/templates?$filter=templateType eq 'securityBaseline'",
            use_beta=True
        )
        baselines = response.get("value", [])
        
        return {
            "count": len(baselines),
            "baselines": [
                {
                    "id": b.get("id"),
                    "displayName": b.get("displayName"),
                    "description": b.get("description"),
                    "versionInfo": b.get("versionInfo"),
                    "publishedDateTime": b.get("publishedDateTime"),
                }
                for b in baselines
            ]
        }
    
    # ============== POLICY CREATION & ASSIGNMENT ==============
    
    @server.tool()
    async def create_compliance_policy(
        display_name: str,
        description: str = "",
        platform: str = "windows10",
        settings: dict[str, Any] = None
    ) -> dict[str, Any]:
        """
        Create a new device compliance policy.
        
        Args:
            display_name: Policy display name
            description: Policy description
            platform: Platform type - "windows10", "iOS", "android", "macOS"
            settings: Policy settings as dictionary (platform-specific)
        
        Returns:
            Created policy details
        """
        client = get_graph_client()
        
        # Map platform to Graph API type
        platform_types = {
            "windows10": "windows10CompliancePolicy",
            "ios": "iosCompliancePolicy",
            "android": "androidCompliancePolicy",
            "macos": "macOSCompliancePolicy"
        }
        
        policy_type = platform_types.get(platform.lower(), "windows10CompliancePolicy")
        
        # Default settings if none provided
        if settings is None:
            if platform.lower() == "windows10":
                settings = {
                    "passwordRequired": True,
                    "passwordMinimumLength": 8,
                    "osMinimumVersion": "10.0.19041",
                    "defenderEnabled": True,
                    "defenderVersion": None,
                    "signatureOutOfDate": False,
                    "rtpEnabled": True,
                    "antivirusRequired": True,
                    "antiSpywareRequired": True,
                    "deviceThreatProtectionEnabled": False,
                    "configurationManagerComplianceRequired": False,
                    "tpmRequired": False,
                    "bitLockerEnabled": False,
                    "secureBootEnabled": False,
                    "codeIntegrityEnabled": False
                }
        
        policy_data = {
            "@odata.type": f"#microsoft.graph.{policy_type}",
            "displayName": display_name,
            "description": description,
            **settings
        }
        
        policy = await client.post("/deviceManagement/deviceCompliancePolicies", json=policy_data)
        
        return {
            "status": "success",
            "message": f"Compliance policy '{display_name}' created successfully",
            "policy": {
                "id": policy.get("id"),
                "displayName": policy.get("displayName"),
                "description": policy.get("description"),
                "createdDateTime": policy.get("createdDateTime")
            }
        }
    
    @server.tool()
    async def assign_compliance_policy(policy_id: str, group_ids: list[str], include_exclude: str = "include") -> dict[str, Any]:
        """
        Assign a compliance policy to groups.
        
        Args:
            policy_id: The compliance policy ID
            group_ids: List of group IDs to assign
            include_exclude: "include" or "exclude" (default: "include")
        
        Returns:
            Assignment status
        """
        client = get_graph_client()
        
        policy = await client.get(f"/deviceManagement/deviceCompliancePolicies/{policy_id}?$select=displayName")
        
        assignments = []
        for group_id in group_ids:
            target_type = "groupAssignmentTarget" if include_exclude == "include" else "exclusionGroupAssignmentTarget"
            assignments.append({
                "target": {
                    "@odata.type": f"#microsoft.graph.{target_type}",
                    "groupId": group_id
                }
            })
        
        # Assign policy
        result = await client.post(
            f"/deviceManagement/deviceCompliancePolicies/{policy_id}/assign",
            json={"assignments": assignments}
        )
        
        return {
            "status": "success",
            "message": f"Compliance policy '{policy.get('displayName')}' assigned to {len(group_ids)} groups",
            "policy_id": policy_id,
            "groups_assigned": len(group_ids)
        }
    
    @server.tool()
    async def create_configuration_profile(
        display_name: str,
        description: str = "",
        platform: str = "windows10",
        settings: dict[str, Any] = None
    ) -> dict[str, Any]:
        """
        Create a new device configuration profile.
        
        Args:
            display_name: Profile display name
            description: Profile description
            platform: Platform type - "windows10", "iOS", "android", "macOS"
            settings: Profile settings as dictionary (platform-specific)
        
        Returns:
            Created profile details
        """
        client = get_graph_client()
        
        # Map platform to Graph API type
        platform_types = {
            "windows10": "windows10GeneralConfiguration",
            "ios": "iosGeneralDeviceConfiguration",
            "android": "androidGeneralDeviceConfiguration",
            "macos": "macOSGeneralDeviceConfiguration"
        }
        
        profile_type = platform_types.get(platform.lower(), "windows10GeneralConfiguration")
        
        # Default settings if none provided
        if settings is None:
            if platform.lower() == "windows10":
                settings = {
                    "defenderBlockEndUserAccess": False,
                    "defenderRequireRealTimeMonitoring": True,
                    "defenderRequireBehaviorMonitoring": True,
                    "defenderRequireNetworkInspectionSystem": True,
                    "defenderScanDownloads": True,
                    "defenderScanScriptsLoadedInInternetExplorer": True,
                    "defenderSignatureUpdateIntervalInHours": 4,
                    "defenderMonitorFileActivity": "monitorAllFiles",
                    "defenderDaysBeforeDeletingQuarantinedMalware": 30,
                    "defenderScanMaxCpu": 50,
                    "defenderScanArchiveFiles": True,
                    "defenderScanIncomingMail": True,
                    "defenderScanRemovableDrivesDuringFullScan": True,
                    "defenderScanMappedNetworkDrivesDuringFullScan": False,
                    "defenderScanNetworkFiles": True,
                    "defenderRequireCloudProtection": True,
                    "defenderPromptForSampleSubmission": "promptBeforeSendingPersonalData",
                    "defenderScheduledQuickScanTime": "02:00:00.0000000",
                    "defenderScanType": "userDefined",
                    "defenderSystemScanSchedule": "userDefined",
                    "defenderScheduledScanTime": "02:00:00.0000000"
                }
        
        profile_data = {
            "@odata.type": f"#microsoft.graph.{profile_type}",
            "displayName": display_name,
            "description": description,
            **settings
        }
        
        profile = await client.post("/deviceManagement/deviceConfigurations", json=profile_data)
        
        return {
            "status": "success",
            "message": f"Configuration profile '{display_name}' created successfully",
            "profile": {
                "id": profile.get("id"),
                "displayName": profile.get("displayName"),
                "description": profile.get("description"),
                "createdDateTime": profile.get("createdDateTime")
            }
        }
    
    @server.tool()
    async def assign_configuration_profile(profile_id: str, group_ids: list[str], include_exclude: str = "include") -> dict[str, Any]:
        """
        Assign a configuration profile to groups.
        
        Args:
            profile_id: The configuration profile ID
            group_ids: List of group IDs to assign
            include_exclude: "include" or "exclude" (default: "include")
        
        Returns:
            Assignment status
        """
        client = get_graph_client()
        
        profile = await client.get(f"/deviceManagement/deviceConfigurations/{profile_id}?$select=displayName")
        
        assignments = []
        for group_id in group_ids:
            target_type = "groupAssignmentTarget" if include_exclude == "include" else "exclusionGroupAssignmentTarget"
            assignments.append({
                "target": {
                    "@odata.type": f"#microsoft.graph.{target_type}",
                    "groupId": group_id
                }
            })
        
        # Assign profile
        result = await client.post(
            f"/deviceManagement/deviceConfigurations/{profile_id}/assign",
            json={"assignments": assignments}
        )
        
        return {
            "status": "success",
            "message": f"Configuration profile '{profile.get('displayName')}' assigned to {len(group_ids)} groups",
            "profile_id": profile_id,
            "groups_assigned": len(group_ids)
        }
    
    @server.tool()
    async def delete_compliance_policy(policy_id: str, confirm: bool = False) -> dict[str, Any]:
        """
        Delete a compliance policy.
        
        Args:
            policy_id: The compliance policy ID
            confirm: Must be True to execute
        
        Returns:
            Deletion status
        """
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "⚠️ This will permanently delete the compliance policy! Set confirm=True to proceed."
            }
        
        client = get_graph_client()
        
        policy = await client.get(f"/deviceManagement/deviceCompliancePolicies/{policy_id}?$select=displayName")
        
        await client.delete(f"/deviceManagement/deviceCompliancePolicies/{policy_id}")
        
        return {
            "status": "success",
            "message": f"Compliance policy '{policy.get('displayName')}' deleted successfully"
        }
    
    @server.tool()
    async def delete_configuration_profile(profile_id: str, confirm: bool = False) -> dict[str, Any]:
        """
        Delete a configuration profile.
        
        Args:
            profile_id: The configuration profile ID
            confirm: Must be True to execute
        
        Returns:
            Deletion status
        """
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "⚠️ This will permanently delete the configuration profile! Set confirm=True to proceed."
            }
        
        client = get_graph_client()
        
        profile = await client.get(f"/deviceManagement/deviceConfigurations/{profile_id}?$select=displayName")
        
        await client.delete(f"/deviceManagement/deviceConfigurations/{profile_id}")
        
        return {
            "status": "success",
            "message": f"Configuration profile '{profile.get('displayName')}' deleted successfully"
        }
    
    # ============== PATCH MANAGEMENT / WINDOWS UPDATE ==============
    
    @server.tool()
    async def create_update_ring(
        display_name: str,
        description: str = "",
        automatic_update_mode: str = "autoInstallAtMaintenanceTime",
        quality_update_deferral_days: int = 0,
        feature_update_deferral_days: int = 0,
        driver_updates_behavior: str = "allow"
    ) -> dict[str, Any]:
        """
        Create a Windows Update ring (Windows 10/11 update policy).
        
        Args:
            display_name: Update ring display name
            description: Update ring description
            automatic_update_mode: Update mode - "autoInstallAtMaintenanceTime", "autoInstallAndRebootAtMaintenanceTime", "autoInstallAndRebootAtScheduledTime", "userDefinedAutoInstall"
            quality_update_deferral_days: Days to defer quality updates (0-30)
            feature_update_deferral_days: Days to defer feature updates (0-365)
            driver_updates_behavior: "allow" or "block" driver updates
        
        Returns:
            Created update ring details
        """
        client = get_graph_client()
        
        update_ring_data = {
            "@odata.type": "#microsoft.graph.windowsUpdateForBusinessConfiguration",
            "displayName": display_name,
            "description": description,
            "automaticUpdateMode": automatic_update_mode,
            "microsoftUpdateServiceAllowed": True,
            "driversExcluded": driver_updates_behavior == "block",
            "qualityUpdatesDeferralPeriodInDays": quality_update_deferral_days,
            "featureUpdatesDeferralPeriodInDays": feature_update_deferral_days,
            "deliveryOptimizationMode": "httpOnly",
            "prereleaseFeatures": "settingsOnly",
            "automaticUpdateDaysOfWeek": [],
            "automaticUpdateHour": 0,
            "automaticUpdateMinute": 0,
            "businessReadyUpdatesOnly": "userDefined",
            "skipChecksBeforeRestart": False,
            "updateWeeks": None,
            "installationSchedule": {
                "@odata.type": "#microsoft.graph.windowsUpdateInstallScheduleType"
            }
        }
        
        update_ring = await client.post("/deviceManagement/deviceConfigurations", json=update_ring_data)
        
        return {
            "status": "success",
            "message": f"Windows Update ring '{display_name}' created successfully",
            "update_ring": {
                "id": update_ring.get("id"),
                "displayName": update_ring.get("displayName"),
                "description": update_ring.get("description"),
                "createdDateTime": update_ring.get("createdDateTime")
            }
        }
    
    @server.tool()
    async def get_update_compliance_report() -> dict[str, Any]:
        """
        Get Windows Update compliance report for all managed devices.
        
        Returns:
            Update compliance summary
        """
        client = get_graph_client()
        
        # Get all Windows devices
        devices = await client.get(
            "/deviceManagement/managedDevices?$filter=operatingSystem eq 'Windows'&$select=deviceName,osVersion,lastSyncDateTime,complianceState&$top=999"
        )
        device_list = devices.get("value", [])
        
        # Windows 10/11 version mapping
        os_versions = {}
        compliance_summary = {
            "total_devices": len(device_list),
            "compliant": 0,
            "noncompliant": 0,
            "unknown": 0
        }
        
        for device in device_list:
            os_version = device.get("osVersion", "Unknown")
            compliance = device.get("complianceState", "unknown")
            
            # Count by OS version
            os_versions[os_version] = os_versions.get(os_version, 0) + 1
            
            # Count by compliance
            if compliance == "compliant":
                compliance_summary["compliant"] += 1
            elif compliance == "noncompliant":
                compliance_summary["noncompliant"] += 1
            else:
                compliance_summary["unknown"] += 1
        
        return {
            "summary": compliance_summary,
            "os_version_distribution": os_versions,
            "compliance_percentage": round((compliance_summary["compliant"] / compliance_summary["total_devices"] * 100), 2) if compliance_summary["total_devices"] > 0 else 0
        }
    
    @server.tool()
    async def get_pending_updates_report(top: int = 100) -> dict[str, Any]:
        """
        Get devices with pending Windows updates.
        
        Args:
            top: Maximum number of devices to return
        
        Returns:
            List of devices with pending updates
        """
        client = get_graph_client()
        
        # Note: This requires additional reporting endpoints or custom detection
        # For now, we'll check devices that are noncompliant
        devices = await client.get(
            f"/deviceManagement/managedDevices?$filter=operatingSystem eq 'Windows' and complianceState eq 'noncompliant'&$select=deviceName,userPrincipalName,osVersion,lastSyncDateTime,complianceState&$top={top}"
        )
        device_list = devices.get("value", [])
        
        return {
            "count": len(device_list),
            "devices_with_pending_updates": [
                {
                    "deviceName": d.get("deviceName"),
                    "userPrincipalName": d.get("userPrincipalName"),
                    "osVersion": d.get("osVersion"),
                    "lastSyncDateTime": d.get("lastSyncDateTime"),
                    "complianceState": d.get("complianceState")
                }
                for d in device_list
            ],
            "note": "Devices showing noncompliant status may have pending updates or other compliance issues"
        }
    
    @server.tool()
    async def pause_updates_for_device(device_id: str, pause_days: int = 7) -> dict[str, Any]:
        """
        Pause Windows updates for a specific device.
        
        Args:
            device_id: The Intune device ID
            pause_days: Number of days to pause updates (1-35)
        
        Returns:
            Status of the operation
        """
        client = get_graph_client()
        
        device = await client.get(f"/deviceManagement/managedDevices/{device_id}?$select=deviceName")
        
        # Note: This would typically be done through a configuration profile or update ring
        # For immediate action, you might need to use a custom PowerShell script
        return {
            "status": "info",
            "message": f"To pause updates for device '{device.get('deviceName')}', create a configuration profile with update deferral settings and assign it to the device or its group.",
            "note": "Direct API pause is not available. Use update rings or configuration profiles instead.",
            "recommended_action": f"Set quality_update_deferral_days to {pause_days} in an update ring"
        }

