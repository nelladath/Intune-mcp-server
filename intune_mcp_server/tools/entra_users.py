"""
Entra ID (Azure AD) User Management Tools
Comprehensive user management including CRUD, passwords, licenses, and authentication.
"""

from typing import Any
from ..graph_client import get_graph_client


async def list_users(top: int = 50, filter_query: str = "", select_fields: str = "") -> dict[str, Any]:
    """
    List all users in the tenant.
    
    Args:
        top: Maximum number of users to return (default 50, max 999)
        filter_query: OData filter (e.g., "accountEnabled eq true")
        select_fields: Comma-separated fields to return
    
    Returns:
        List of users with their details
    """
    client = get_graph_client()
    
    endpoint = "/users"
    params = [f"$top={min(top, 999)}"]
    if filter_query:
        params.append(f"$filter={filter_query}")
    if select_fields:
        params.append(f"$select={select_fields}")
    else:
        params.append("$select=id,displayName,userPrincipalName,mail,jobTitle,department,accountEnabled,createdDateTime")
    
    endpoint += "?" + "&".join(params)
    
    response = await client.get(endpoint)
    users = response.get("value", [])
    
    return {
        "count": len(users),
        "users": users
    }


async def get_user_details(user_id: str) -> dict[str, Any]:
    """
    Get comprehensive details for a specific user.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Complete user information
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=id,displayName,userPrincipalName,mail,givenName,surname,jobTitle,department,officeLocation,companyName,employeeId,employeeType,mobilePhone,businessPhones,streetAddress,city,state,postalCode,country,accountEnabled,createdDateTime,lastPasswordChangeDateTime,assignedLicenses,assignedPlans")
    
    # Get manager
    try:
        manager = await client.get(f"/users/{user_id}/manager?$select=displayName,userPrincipalName")
        manager_info = {"displayName": manager.get("displayName"), "userPrincipalName": manager.get("userPrincipalName")}
    except:
        manager_info = None
    
    # Get direct reports count
    try:
        reports = await client.get(f"/users/{user_id}/directReports?$count=true&$top=1")
        direct_reports_count = len(reports.get("value", []))
    except:
        direct_reports_count = 0
    
    return {
        "basic_info": {
            "id": user.get("id"),
            "displayName": user.get("displayName"),
            "userPrincipalName": user.get("userPrincipalName"),
            "mail": user.get("mail"),
            "givenName": user.get("givenName"),
            "surname": user.get("surname"),
        },
        "work_info": {
            "jobTitle": user.get("jobTitle"),
            "department": user.get("department"),
            "companyName": user.get("companyName"),
            "officeLocation": user.get("officeLocation"),
            "employeeId": user.get("employeeId"),
            "employeeType": user.get("employeeType"),
        },
        "contact_info": {
            "mobilePhone": user.get("mobilePhone"),
            "businessPhones": user.get("businessPhones"),
            "streetAddress": user.get("streetAddress"),
            "city": user.get("city"),
            "state": user.get("state"),
            "postalCode": user.get("postalCode"),
            "country": user.get("country"),
        },
        "account_info": {
            "accountEnabled": user.get("accountEnabled"),
            "createdDateTime": user.get("createdDateTime"),
            "lastPasswordChangeDateTime": user.get("lastPasswordChangeDateTime"),
        },
        "manager": manager_info,
        "direct_reports_count": direct_reports_count,
        "license_count": len(user.get("assignedLicenses", [])),
    }


async def create_user(
    display_name: str,
    user_principal_name: str,
    mail_nickname: str,
    password: str,
    account_enabled: bool = True,
    force_change_password: bool = True,
    given_name: str = "",
    surname: str = "",
    job_title: str = "",
    department: str = "",
    office_location: str = "",
    mobile_phone: str = ""
) -> dict[str, Any]:
    """
    Create a new user in Entra ID.
    
    Args:
        display_name: User's display name
        user_principal_name: User's UPN (e.g., user@domain.com)
        mail_nickname: Mail alias (without domain)
        password: Initial password
        account_enabled: Whether account is enabled (default True)
        force_change_password: Force password change on first login (default True)
        given_name: First name
        surname: Last name
        job_title: Job title
        department: Department name
        office_location: Office location
        mobile_phone: Mobile phone number
    
    Returns:
        Created user details
    """
    client = get_graph_client()
    
    user_data = {
        "accountEnabled": account_enabled,
        "displayName": display_name,
        "mailNickname": mail_nickname,
        "userPrincipalName": user_principal_name,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": force_change_password,
            "password": password
        }
    }
    
    # Add optional fields if provided
    if given_name:
        user_data["givenName"] = given_name
    if surname:
        user_data["surname"] = surname
    if job_title:
        user_data["jobTitle"] = job_title
    if department:
        user_data["department"] = department
    if office_location:
        user_data["officeLocation"] = office_location
    if mobile_phone:
        user_data["mobilePhone"] = mobile_phone
    
    result = await client.post("/users", json=user_data)
    
    return {
        "status": "success",
        "message": f"User '{display_name}' created successfully",
        "user": {
            "id": result.get("id"),
            "displayName": result.get("displayName"),
            "userPrincipalName": result.get("userPrincipalName"),
        }
    }


async def update_user(
    user_id: str,
    display_name: str = None,
    given_name: str = None,
    surname: str = None,
    job_title: str = None,
    department: str = None,
    office_location: str = None,
    mobile_phone: str = None,
    company_name: str = None,
    employee_id: str = None,
    street_address: str = None,
    city: str = None,
    state: str = None,
    postal_code: str = None,
    country: str = None
) -> dict[str, Any]:
    """
    Update user properties.
    
    Args:
        user_id: The user ID or userPrincipalName
        display_name: New display name
        given_name: First name
        surname: Last name
        job_title: Job title
        department: Department
        office_location: Office location
        mobile_phone: Mobile phone
        company_name: Company name
        employee_id: Employee ID
        street_address: Street address
        city: City
        state: State/Province
        postal_code: Postal/ZIP code
        country: Country
    
    Returns:
        Update status
    """
    client = get_graph_client()
    
    update_data = {}
    
    # Only add fields that were provided
    if display_name is not None:
        update_data["displayName"] = display_name
    if given_name is not None:
        update_data["givenName"] = given_name
    if surname is not None:
        update_data["surname"] = surname
    if job_title is not None:
        update_data["jobTitle"] = job_title
    if department is not None:
        update_data["department"] = department
    if office_location is not None:
        update_data["officeLocation"] = office_location
    if mobile_phone is not None:
        update_data["mobilePhone"] = mobile_phone
    if company_name is not None:
        update_data["companyName"] = company_name
    if employee_id is not None:
        update_data["employeeId"] = employee_id
    if street_address is not None:
        update_data["streetAddress"] = street_address
    if city is not None:
        update_data["city"] = city
    if state is not None:
        update_data["state"] = state
    if postal_code is not None:
        update_data["postalCode"] = postal_code
    if country is not None:
        update_data["country"] = country
    
    if not update_data:
        return {"status": "error", "message": "No fields provided for update"}
    
    # Get user name for confirmation
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.patch(f"/users/{user_id}", json=update_data)
    
    return {
        "status": "success",
        "message": f"User '{user.get('displayName')}' updated successfully",
        "updated_fields": list(update_data.keys())
    }


async def delete_user(user_id: str, confirm: bool = False) -> dict[str, Any]:
    """
    Delete a user from Entra ID. User will be moved to deleted users (recoverable for 30 days).
    
    Args:
        user_id: The user ID or userPrincipalName
        confirm: Must be True to execute deletion
    
    Returns:
        Deletion status
    """
    if not confirm:
        return {
            "status": "confirmation_required",
            "message": "⚠️ DELETE will remove the user! Set confirm=True to proceed.",
            "note": "User will be recoverable from deleted users for 30 days"
        }
    
    client = get_graph_client()
    
    # Get user info before deletion
    user = await client.get(f"/users/{user_id}?$select=displayName,userPrincipalName")
    
    await client.delete(f"/users/{user_id}")
    
    return {
        "status": "success",
        "message": f"User '{user.get('displayName')}' deleted",
        "user_principal_name": user.get("userPrincipalName"),
        "note": "User moved to deleted users, recoverable for 30 days"
    }


async def enable_user(user_id: str) -> dict[str, Any]:
    """
    Enable a user account.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.patch(f"/users/{user_id}", json={"accountEnabled": True})
    
    return {
        "status": "success",
        "message": f"User '{user.get('displayName')}' has been enabled"
    }


async def disable_user(user_id: str) -> dict[str, Any]:
    """
    Disable a user account (blocks sign-in).
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.patch(f"/users/{user_id}", json={"accountEnabled": False})
    
    return {
        "status": "success",
        "message": f"User '{user.get('displayName')}' has been disabled (sign-in blocked)"
    }


async def reset_user_password(
    user_id: str,
    new_password: str,
    force_change_on_next_login: bool = True
) -> dict[str, Any]:
    """
    Reset a user's password.
    
    Args:
        user_id: The user ID or userPrincipalName
        new_password: The new password
        force_change_on_next_login: Whether to force password change (default True)
    
    Returns:
        Status of password reset
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.patch(
        f"/users/{user_id}",
        json={
            "passwordProfile": {
                "forceChangePasswordNextSignIn": force_change_on_next_login,
                "password": new_password
            }
        }
    )
    
    return {
        "status": "success",
        "message": f"Password reset for user '{user.get('displayName')}'",
        "force_change_on_login": force_change_on_next_login
    }


async def revoke_user_sessions(user_id: str) -> dict[str, Any]:
    """
    Revoke all refresh tokens for a user (forces re-authentication).
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.post(f"/users/{user_id}/revokeSignInSessions")
    
    return {
        "status": "success",
        "message": f"All sessions revoked for user '{user.get('displayName')}'",
        "note": "User will need to sign in again on all devices"
    }


async def get_user_sign_in_activity(user_id: str) -> dict[str, Any]:
    """
    Get sign-in activity information for a user.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Sign-in activity details
    """
    client = get_graph_client()
    
    # Need beta endpoint for sign-in activity
    user = await client.get(
        f"/users/{user_id}?$select=displayName,userPrincipalName,signInActivity",
        use_beta=True
    )
    
    sign_in = user.get("signInActivity", {})
    
    return {
        "user": {
            "displayName": user.get("displayName"),
            "userPrincipalName": user.get("userPrincipalName"),
        },
        "sign_in_activity": {
            "lastSignInDateTime": sign_in.get("lastSignInDateTime"),
            "lastSignInRequestId": sign_in.get("lastSignInRequestId"),
            "lastNonInteractiveSignInDateTime": sign_in.get("lastNonInteractiveSignInDateTime"),
        }
    }


async def assign_manager(user_id: str, manager_id: str) -> dict[str, Any]:
    """
    Assign a manager to a user.
    
    Args:
        user_id: The user ID or userPrincipalName
        manager_id: The manager's user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName,id")
    manager = await client.get(f"/users/{manager_id}?$select=displayName,id")
    
    await client.patch(
        f"/users/{user['id']}/manager/$ref",
        json={"@odata.id": f"https://graph.microsoft.com/v1.0/users/{manager['id']}"}
    )
    
    return {
        "status": "success",
        "message": f"Manager '{manager.get('displayName')}' assigned to user '{user.get('displayName')}'"
    }


async def remove_manager(user_id: str) -> dict[str, Any]:
    """
    Remove the manager assignment from a user.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.delete(f"/users/{user_id}/manager/$ref")
    
    return {
        "status": "success",
        "message": f"Manager removed from user '{user.get('displayName')}'"
    }


async def get_deleted_users(top: int = 50) -> dict[str, Any]:
    """
    List deleted users (recoverable within 30 days).
    
    Args:
        top: Maximum number of users to return
    
    Returns:
        List of deleted users
    """
    client = get_graph_client()
    
    response = await client.get(f"/directory/deletedItems/microsoft.graph.user?$top={top}")
    users = response.get("value", [])
    
    return {
        "count": len(users),
        "deleted_users": [
            {
                "id": u.get("id"),
                "displayName": u.get("displayName"),
                "userPrincipalName": u.get("userPrincipalName"),
                "deletedDateTime": u.get("deletedDateTime"),
            }
            for u in users
        ]
    }


async def restore_deleted_user(user_id: str) -> dict[str, Any]:
    """
    Restore a deleted user.
    
    Args:
        user_id: The deleted user's ID
    
    Returns:
        Status of the restoration
    """
    client = get_graph_client()
    
    result = await client.post(f"/directory/deletedItems/{user_id}/restore")
    
    return {
        "status": "success",
        "message": f"User '{result.get('displayName')}' restored successfully",
        "user": {
            "id": result.get("id"),
            "displayName": result.get("displayName"),
            "userPrincipalName": result.get("userPrincipalName"),
        }
    }


async def get_user_licenses(user_id: str) -> dict[str, Any]:
    """
    Get detailed license information for a user.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        License assignment details
    """
    client = get_graph_client()
    
    user = await client.get(
        f"/users/{user_id}?$select=displayName,userPrincipalName,assignedLicenses,licenseAssignmentStates"
    )
    
    # Get subscribed SKUs for friendly names
    skus = await client.get("/subscribedSkus")
    sku_map = {s.get("skuId"): s.get("skuPartNumber") for s in skus.get("value", [])}
    
    licenses = []
    for lic in user.get("assignedLicenses", []):
        sku_id = lic.get("skuId")
        licenses.append({
            "skuId": sku_id,
            "skuName": sku_map.get(sku_id, "Unknown"),
            "disabledPlans": lic.get("disabledPlans", [])
        })
    
    return {
        "user": {
            "displayName": user.get("displayName"),
            "userPrincipalName": user.get("userPrincipalName"),
        },
        "license_count": len(licenses),
        "licenses": licenses,
        "license_states": user.get("licenseAssignmentStates", [])
    }


async def assign_license(user_id: str, sku_id: str, disabled_plans: list = None) -> dict[str, Any]:
    """
    Assign a license to a user.
    
    Args:
        user_id: The user ID or userPrincipalName
        sku_id: The SKU ID of the license to assign
        disabled_plans: Optional list of service plan IDs to disable
    
    Returns:
        Status of the license assignment
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    license_data = {
        "addLicenses": [
            {
                "skuId": sku_id,
                "disabledPlans": disabled_plans or []
            }
        ],
        "removeLicenses": []
    }
    
    await client.post(f"/users/{user_id}/assignLicense", json=license_data)
    
    return {
        "status": "success",
        "message": f"License assigned to user '{user.get('displayName')}'",
        "sku_id": sku_id
    }


async def remove_license(user_id: str, sku_id: str) -> dict[str, Any]:
    """
    Remove a license from a user.
    
    Args:
        user_id: The user ID or userPrincipalName
        sku_id: The SKU ID of the license to remove
    
    Returns:
        Status of the license removal
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    license_data = {
        "addLicenses": [],
        "removeLicenses": [sku_id]
    }
    
    await client.post(f"/users/{user_id}/assignLicense", json=license_data)
    
    return {
        "status": "success",
        "message": f"License removed from user '{user.get('displayName')}'",
        "sku_id": sku_id
    }


async def list_available_licenses() -> dict[str, Any]:
    """
    List all available licenses (SKUs) in the tenant with availability.
    
    Returns:
        List of subscribed SKUs with license counts
    """
    client = get_graph_client()
    
    response = await client.get("/subscribedSkus")
    skus = response.get("value", [])
    
    return {
        "count": len(skus),
        "licenses": [
            {
                "skuId": s.get("skuId"),
                "skuPartNumber": s.get("skuPartNumber"),
                "capabilityStatus": s.get("capabilityStatus"),
                "consumed": s.get("consumedUnits"),
                "total": s.get("prepaidUnits", {}).get("enabled", 0),
                "available": s.get("prepaidUnits", {}).get("enabled", 0) - s.get("consumedUnits", 0),
            }
            for s in skus
        ]
    }


async def offboard_user(user_id: str) -> dict[str, Any]:
    """
    Comprehensive user offboarding process for Entra ID.
    
    This function performs a complete offboarding without deleting the user:
    1. Blocks user sign-in
    2. Revokes all active sessions
    3. Removes from all groups
    4. Removes all app assignments
    5. Removes all licenses
    6. Generates detailed access checklist
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Detailed offboarding report including actions taken and access checklist
    """
    client = get_graph_client()
    
    # Get user information
    user = await client.get(f"/users/{user_id}?$select=id,displayName,userPrincipalName,accountEnabled")
    user_object_id = user.get("id")
    display_name = user.get("displayName")
    upn = user.get("userPrincipalName")
    
    offboarding_report = {
        "user": {
            "id": user_object_id,
            "displayName": display_name,
            "userPrincipalName": upn,
        },
        "actions": {},
        "access_checklist": {},
        "status": "success",
        "message": f"User '{display_name}' offboarding completed"
    }
    
    # ===== STEP 1: BLOCK SIGN-IN =====
    try:
        if user.get("accountEnabled"):
            await client.patch(f"/users/{user_object_id}", json={"accountEnabled": False})
            offboarding_report["actions"]["sign_in_blocked"] = {
                "status": "success",
                "message": "User sign-in blocked"
            }
        else:
            offboarding_report["actions"]["sign_in_blocked"] = {
                "status": "skipped",
                "message": "User account was already disabled"
            }
    except Exception as e:
        offboarding_report["actions"]["sign_in_blocked"] = {
            "status": "error",
            "message": f"Failed to block sign-in: {str(e)}"
        }
    
    # ===== STEP 2: REVOKE ACTIVE SESSIONS =====
    try:
        await client.post(f"/users/{user_object_id}/revokeSignInSessions")
        offboarding_report["actions"]["sessions_revoked"] = {
            "status": "success",
            "message": "All active sessions revoked"
        }
    except Exception as e:
        offboarding_report["actions"]["sessions_revoked"] = {
            "status": "error",
            "message": f"Failed to revoke sessions: {str(e)}"
        }
    
    # ===== STEP 3: REMOVE FROM ALL GROUPS =====
    groups_removed = []
    groups_failed = []
    try:
        groups_response = await client.get(f"/users/{user_object_id}/memberOf")
        groups = groups_response.get("value", [])
        
        for group in groups:
            group_id = group.get("id")
            group_name = group.get("displayName")
            try:
                await client.delete(f"/groups/{group_id}/members/{user_object_id}/$ref")
                groups_removed.append(group_name)
            except Exception as e:
                groups_failed.append({"name": group_name, "error": str(e)})
        
        offboarding_report["actions"]["group_removal"] = {
            "status": "success" if not groups_failed else "partial",
            "message": f"Removed from {len(groups_removed)} groups",
            "groups_removed": groups_removed,
            "groups_failed": groups_failed if groups_failed else None,
            "total_groups": len(groups)
        }
    except Exception as e:
        offboarding_report["actions"]["group_removal"] = {
            "status": "error",
            "message": f"Failed to process group removal: {str(e)}"
        }
    
    # ===== STEP 4: REMOVE ALL APP ASSIGNMENTS =====
    apps_removed = []
    apps_failed = []
    try:
        app_assignments_response = await client.get(f"/users/{user_object_id}/appRoleAssignments")
        app_assignments = app_assignments_response.get("value", [])
        
        for app in app_assignments:
            app_assignment_id = app.get("id")
            app_name = app.get("resourceDisplayName")
            try:
                await client.delete(f"/users/{user_object_id}/appRoleAssignments/{app_assignment_id}")
                apps_removed.append(app_name)
            except Exception as e:
                apps_failed.append({"name": app_name, "error": str(e)})
        
        offboarding_report["actions"]["app_removal"] = {
            "status": "success" if not apps_failed else "partial",
            "message": f"Removed {len(apps_removed)} app assignments",
            "apps_removed": apps_removed,
            "apps_failed": apps_failed if apps_failed else None,
            "total_apps": len(app_assignments)
        }
    except Exception as e:
        offboarding_report["actions"]["app_removal"] = {
            "status": "error",
            "message": f"Failed to process app removal: {str(e)}"
        }
    
    # ===== STEP 5: REMOVE ALL LICENSES =====
    licenses_removed = []
    try:
        licenses_response = await client.get(f"/users/{user_object_id}/licenseDetails")
        licenses = licenses_response.get("value", [])
        license_sku_ids = [lic.get("skuId") for lic in licenses]
        
        if license_sku_ids:
            # Get SKU names for reporting
            skus_response = await client.get("/subscribedSkus")
            sku_map = {s.get("skuId"): s.get("skuPartNumber") for s in skus_response.get("value", [])}
            licenses_removed = [sku_map.get(sku_id, sku_id) for sku_id in license_sku_ids]
            
            # Remove all licenses
            await client.post(
                f"/users/{user_object_id}/assignLicense",
                json={
                    "addLicenses": [],
                    "removeLicenses": license_sku_ids
                }
            )
            
            offboarding_report["actions"]["license_removal"] = {
                "status": "success",
                "message": f"Removed {len(license_sku_ids)} licenses",
                "licenses_removed": licenses_removed
            }
        else:
            offboarding_report["actions"]["license_removal"] = {
                "status": "skipped",
                "message": "No licenses assigned"
            }
    except Exception as e:
        offboarding_report["actions"]["license_removal"] = {
            "status": "error",
            "message": f"Failed to remove licenses: {str(e)}"
        }
    
    # ===== ACCESS CHECKLIST: DIRECTORY ROLES =====
    try:
        role_assignments_response = await client.get(
            f"/roleManagement/directory/roleAssignments?$filter=principalId eq '{user_object_id}'"
        )
        role_assignments = role_assignments_response.get("value", [])
        
        directory_roles = []
        for role in role_assignments:
            try:
                role_def = await client.get(f"/roleManagement/directory/roleDefinitions/{role.get('roleDefinitionId')}")
                directory_roles.append({
                    "roleName": role_def.get("displayName"),
                    "roleId": role.get("roleDefinitionId"),
                    "assignmentId": role.get("id")
                })
            except:
                pass
        
        offboarding_report["access_checklist"]["directory_roles"] = {
            "count": len(directory_roles),
            "roles": directory_roles if directory_roles else None,
            "note": "⚠️ Directory role assignments still exist - manual review required" if directory_roles else "None"
        }
    except Exception as e:
        offboarding_report["access_checklist"]["directory_roles"] = {
            "status": "error",
            "message": f"Failed to check directory roles: {str(e)}"
        }
    
    # ===== ACCESS CHECKLIST: GROUP MEMBERSHIPS (REMAINING) =====
    try:
        remaining_groups_response = await client.get(f"/users/{user_object_id}/memberOf")
        remaining_groups = remaining_groups_response.get("value", [])
        
        group_list = []
        for group in remaining_groups:
            group_type = "Security" if group.get("securityEnabled") else "M365/Distribution"
            group_list.append({
                "displayName": group.get("displayName"),
                "id": group.get("id"),
                "type": group_type
            })
        
        offboarding_report["access_checklist"]["group_memberships"] = {
            "count": len(group_list),
            "groups": group_list if group_list else None,
            "note": "⚠️ Some groups could not be removed - manual review required" if group_list else "All groups removed"
        }
    except Exception as e:
        offboarding_report["access_checklist"]["group_memberships"] = {
            "status": "error",
            "message": f"Failed to check remaining groups: {str(e)}"
        }
    
    # ===== ACCESS CHECKLIST: ENTERPRISE APPLICATION ACCESS (REMAINING) =====
    try:
        remaining_apps_response = await client.get(f"/users/{user_object_id}/appRoleAssignments")
        remaining_apps = remaining_apps_response.get("value", [])
        
        app_list = []
        for app in remaining_apps:
            app_list.append({
                "displayName": app.get("resourceDisplayName"),
                "resourceId": app.get("resourceId"),
                "appRoleId": app.get("appRoleId")
            })
        
        offboarding_report["access_checklist"]["enterprise_applications"] = {
            "count": len(app_list),
            "applications": app_list if app_list else None,
            "note": "⚠️ Some app assignments could not be removed - manual review required" if app_list else "All app assignments removed"
        }
    except Exception as e:
        offboarding_report["access_checklist"]["enterprise_applications"] = {
            "status": "error",
            "message": f"Failed to check remaining apps: {str(e)}"
        }
    
    # ===== ACCESS CHECKLIST: APP REGISTRATIONS OWNED =====
    try:
        owned_objects_response = await client.get(f"/users/{user_object_id}/ownedObjects")
        owned_objects = owned_objects_response.get("value", [])
        
        owned_apps = [
            {
                "displayName": obj.get("displayName"),
                "id": obj.get("id"),
                "appId": obj.get("appId")
            }
            for obj in owned_objects
            if obj.get("@odata.type") == "#microsoft.graph.application"
        ]
        
        offboarding_report["access_checklist"]["app_registrations_owned"] = {
            "count": len(owned_apps),
            "applications": owned_apps if owned_apps else None,
            "note": "⚠️ User owns app registrations - reassign ownership before full offboarding" if owned_apps else "None"
        }
    except Exception as e:
        offboarding_report["access_checklist"]["app_registrations_owned"] = {
            "status": "error",
            "message": f"Failed to check owned apps: {str(e)}"
        }
    
    return offboarding_report


# ============== MANAGER & ORGANIZATIONAL HIERARCHY ==============

async def assign_manager(user_id: str, manager_id: str) -> dict[str, Any]:
    """
    Assign a manager to a user.
    
    Args:
        user_id: The user ID or userPrincipalName
        manager_id: The manager's user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    # Get user and manager details
    user = await client.get(f"/users/{user_id}?$select=displayName,userPrincipalName")
    manager = await client.get(f"/users/{manager_id}?$select=displayName,userPrincipalName")
    
    # Assign manager
    await client.put(
        f"/users/{user_id}/manager/$ref",
        json={"@odata.id": f"https://graph.microsoft.com/v1.0/users/{manager_id}"}
    )
    
    return {
        "status": "success",
        "message": f"Manager '{manager.get('displayName')}' assigned to user '{user.get('displayName')}'",
        "user": {
            "id": user.get("id"),
            "displayName": user.get("displayName"),
            "userPrincipalName": user.get("userPrincipalName")
        },
        "manager": {
            "id": manager.get("id"),
            "displayName": manager.get("displayName"),
            "userPrincipalName": manager.get("userPrincipalName")
        }
    }


async def remove_manager(user_id: str) -> dict[str, Any]:
    """
    Remove the manager assignment from a user.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        Status of the operation
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName")
    
    await client.delete(f"/users/{user_id}/manager/$ref")
    
    return {
        "status": "success",
        "message": f"Manager removed from user '{user.get('displayName')}'"
    }


async def get_direct_reports(user_id: str) -> dict[str, Any]:
    """
    Get all direct reports for a user.
    
    Args:
        user_id: The user ID or userPrincipalName
    
    Returns:
        List of direct reports
    """
    client = get_graph_client()
    
    user = await client.get(f"/users/{user_id}?$select=displayName,userPrincipalName")
    
    reports = await client.get(
        f"/users/{user_id}/directReports?$select=id,displayName,userPrincipalName,mail,jobTitle,department"
    )
    report_list = reports.get("value", [])
    
    return {
        "manager": {
            "displayName": user.get("displayName"),
            "userPrincipalName": user.get("userPrincipalName")
        },
        "direct_reports_count": len(report_list),
        "direct_reports": [
            {
                "id": r.get("id"),
                "displayName": r.get("displayName"),
                "userPrincipalName": r.get("userPrincipalName"),
                "mail": r.get("mail"),
                "jobTitle": r.get("jobTitle"),
                "department": r.get("department")
            }
            for r in report_list
        ]
    }


# ============== USER ONBOARDING ==============

async def onboard_user(
    display_name: str,
    user_principal_name: str,
    password: str,
    given_name: str = "",
    surname: str = "",
    job_title: str = "",
    department: str = "",
    office_location: str = "",
    mobile_phone: str = "",
    manager_id: str = None,
    license_skus: list[str] = None,
    group_ids: list[str] = None,
    send_welcome_email: bool = False
) -> dict[str, Any]:
    """
    Complete user onboarding workflow.
    
    This function automates the entire onboarding process:
    1. Create user account
    2. Assign manager (if provided)
    3. Assign licenses (if provided)
    4. Add to groups (if provided)
    5. Optionally send welcome email
    
    Args:
        display_name: User's display name
        user_principal_name: User's UPN (e.g., user@domain.com)
        password: Initial password
        given_name: First name
        surname: Last name
        job_title: Job title
        department: Department name
        office_location: Office location
        mobile_phone: Mobile phone number
        manager_id: Manager's user ID (optional)
        license_skus: List of license SKU IDs to assign (optional)
        group_ids: List of group IDs to add user to (optional)
        send_welcome_email: Send welcome email with credentials (optional)
    
    Returns:
        Complete onboarding report
    """
    client = get_graph_client()
    
    onboarding_report = {
        "user": None,
        "actions": {
            "user_created": {"status": "pending"},
            "manager_assigned": {"status": "pending"},
            "licenses_assigned": {"status": "pending"},
            "groups_added": {"status": "pending"},
            "welcome_email_sent": {"status": "pending"}
        },
        "status": "in_progress"
    }
    
    # Step 1: Create user
    try:
        mail_nickname = user_principal_name.split("@")[0]
        user_result = await create_user(
            display_name=display_name,
            user_principal_name=user_principal_name,
            mail_nickname=mail_nickname,
            password=password,
            account_enabled=True,
            force_change_password=True,
            given_name=given_name,
            surname=surname,
            job_title=job_title,
            department=department,
            office_location=office_location,
            mobile_phone=mobile_phone
        )
        
        user_id = user_result.get("user", {}).get("id")
        onboarding_report["user"] = user_result.get("user")
        onboarding_report["actions"]["user_created"] = {
            "status": "success",
            "message": f"User '{display_name}' created successfully"
        }
    except Exception as e:
        onboarding_report["actions"]["user_created"] = {
            "status": "error",
            "message": f"Failed to create user: {str(e)}"
        }
        onboarding_report["status"] = "failed"
        return onboarding_report
    
    # Step 2: Assign manager
    if manager_id:
        try:
            manager_result = await assign_manager(user_id, manager_id)
            onboarding_report["actions"]["manager_assigned"] = {
                "status": "success",
                "message": manager_result.get("message"),
                "manager": manager_result.get("manager")
            }
        except Exception as e:
            onboarding_report["actions"]["manager_assigned"] = {
                "status": "error",
                "message": f"Failed to assign manager: {str(e)}"
            }
    else:
        onboarding_report["actions"]["manager_assigned"] = {
            "status": "skipped",
            "message": "No manager provided"
        }
    
    # Step 3: Assign licenses
    if license_skus:
        licenses_assigned = []
        licenses_failed = []
        
        for sku_id in license_skus:
            try:
                await assign_license(user_id, sku_id)
                licenses_assigned.append(sku_id)
            except Exception as e:
                licenses_failed.append({"sku_id": sku_id, "error": str(e)})
        
        if licenses_assigned:
            onboarding_report["actions"]["licenses_assigned"] = {
                "status": "success" if not licenses_failed else "partial",
                "message": f"Assigned {len(licenses_assigned)} licenses",
                "licenses_assigned": licenses_assigned,
                "licenses_failed": licenses_failed if licenses_failed else None
            }
        else:
            onboarding_report["actions"]["licenses_assigned"] = {
                "status": "error",
                "message": "All license assignments failed",
                "licenses_failed": licenses_failed
            }
    else:
        onboarding_report["actions"]["licenses_assigned"] = {
            "status": "skipped",
            "message": "No licenses provided"
        }
    
    # Step 4: Add to groups
    if group_ids:
        groups_added = []
        groups_failed = []
        
        for group_id in group_ids:
            try:
                await client.post(
                    f"/groups/{group_id}/members/$ref",
                    json={"@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"}
                )
                groups_added.append(group_id)
            except Exception as e:
                groups_failed.append({"group_id": group_id, "error": str(e)})
        
        if groups_added:
            onboarding_report["actions"]["groups_added"] = {
                "status": "success" if not groups_failed else "partial",
                "message": f"Added to {len(groups_added)} groups",
                "groups_added": groups_added,
                "groups_failed": groups_failed if groups_failed else None
            }
        else:
            onboarding_report["actions"]["groups_added"] = {
                "status": "error",
                "message": "All group additions failed",
                "groups_failed": groups_failed
            }
    else:
        onboarding_report["actions"]["groups_added"] = {
            "status": "skipped",
            "message": "No groups provided"
        }
    
    # Step 5: Send welcome email (if requested)
    if send_welcome_email:
        try:
            # Note: This requires Microsoft Graph mail send permissions
            email_body = f"""
            <html>
            <body>
                <h2>Welcome to the Organization!</h2>
                <p>Hello {given_name or display_name},</p>
                <p>Your account has been created with the following details:</p>
                <ul>
                    <li><strong>Username:</strong> {user_principal_name}</li>
                    <li><strong>Temporary Password:</strong> {password}</li>
                </ul>
                <p>Please sign in and change your password on first login.</p>
                <p>Best regards,<br>IT Team</p>
            </body>
            </html>
            """
            
            # This requires Mail.Send permission
            await client.post(
                f"/users/{user_id}/sendMail",
                json={
                    "message": {
                        "subject": "Welcome - Your New Account",
                        "body": {
                            "contentType": "HTML",
                            "content": email_body
                        },
                        "toRecipients": [
                            {
                                "emailAddress": {
                                    "address": user_principal_name
                                }
                            }
                        ]
                    }
                }
            )
            
            onboarding_report["actions"]["welcome_email_sent"] = {
                "status": "success",
                "message": "Welcome email sent successfully"
            }
        except Exception as e:
            onboarding_report["actions"]["welcome_email_sent"] = {
                "status": "error",
                "message": f"Failed to send welcome email: {str(e)}"
            }
    else:
        onboarding_report["actions"]["welcome_email_sent"] = {
            "status": "skipped",
            "message": "Welcome email not requested"
        }
    
    onboarding_report["status"] = "completed"
    return onboarding_report


# ============== BULK OPERATIONS ==============

async def bulk_create_users(users_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Create multiple users in bulk.
    
    Args:
        users_data: List of user dictionaries with keys:
            - display_name (required)
            - user_principal_name (required)
            - password (required)
            - given_name, surname, job_title, department, etc. (optional)
    
    Returns:
        Bulk creation report
    """
    results = {
        "total": len(users_data),
        "successful": [],
        "failed": []
    }
    
    for user_data in users_data:
        try:
            mail_nickname = user_data.get("user_principal_name", "").split("@")[0]
            user_result = await create_user(
                display_name=user_data.get("display_name"),
                user_principal_name=user_data.get("user_principal_name"),
                mail_nickname=mail_nickname,
                password=user_data.get("password"),
                account_enabled=user_data.get("account_enabled", True),
                force_change_password=user_data.get("force_change_password", True),
                given_name=user_data.get("given_name", ""),
                surname=user_data.get("surname", ""),
                job_title=user_data.get("job_title", ""),
                department=user_data.get("department", ""),
                office_location=user_data.get("office_location", ""),
                mobile_phone=user_data.get("mobile_phone", "")
            )
            
            results["successful"].append({
                "user_principal_name": user_data.get("user_principal_name"),
                "user_id": user_result.get("user", {}).get("id"),
                "display_name": user_data.get("display_name")
            })
        except Exception as e:
            results["failed"].append({
                "user_principal_name": user_data.get("user_principal_name"),
                "display_name": user_data.get("display_name"),
                "error": str(e)
            })
    
    return {
        "status": "completed",
        "summary": {
            "total": results["total"],
            "successful": len(results["successful"]),
            "failed": len(results["failed"])
        },
        "results": results
    }


async def bulk_assign_licenses(user_ids: list[str], sku_id: str) -> dict[str, Any]:
    """
    Assign a license to multiple users in bulk.
    
    Args:
        user_ids: List of user IDs or UPNs
        sku_id: License SKU ID to assign
    
    Returns:
        Bulk assignment report
    """
    results = {
        "total": len(user_ids),
        "successful": [],
        "failed": []
    }
    
    for user_id in user_ids:
        try:
            await assign_license(user_id, sku_id)
            results["successful"].append(user_id)
        except Exception as e:
            results["failed"].append({"user_id": user_id, "error": str(e)})
    
    return {
        "status": "completed",
        "sku_id": sku_id,
        "summary": {
            "total": results["total"],
            "successful": len(results["successful"]),
            "failed": len(results["failed"])
        },
        "results": results
    }


async def bulk_add_to_group(user_ids: list[str], group_id: str) -> dict[str, Any]:
    """
    Add multiple users to a group in bulk.
    
    Args:
        user_ids: List of user IDs or UPNs
        group_id: Group ID
    
    Returns:
        Bulk addition report
    """
    client = get_graph_client()
    
    results = {
        "total": len(user_ids),
        "successful": [],
        "failed": []
    }
    
    # Get group details
    group = await client.get(f"/groups/{group_id}?$select=displayName")
    
    for user_id in user_ids:
        try:
            await client.post(
                f"/groups/{group_id}/members/$ref",
                json={"@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"}
            )
            results["successful"].append(user_id)
        except Exception as e:
            results["failed"].append({"user_id": user_id, "error": str(e)})
    
    return {
        "status": "completed",
        "group": {
            "id": group_id,
            "displayName": group.get("displayName")
        },
        "summary": {
            "total": results["total"],
            "successful": len(results["successful"]),
            "failed": len(results["failed"])
        },
        "results": results
    }
