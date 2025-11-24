"""
Example usage of avmoperation library

This file demonstrates how to use the three main methods:
- start_vm(): Start an Azure VM
- stop_vm(): Stop an Azure VM
- check_status(): Check VM power state
"""

import os
from avmoperation import start_vm, stop_vm, check_status, AvmOperation


def example_basic_usage():
    """Example 1: Basic usage with direct function calls"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Azure credentials
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "your-subscription-id")
    vm_name = os.getenv("AZURE_VM_NAME", "your-vm-name")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP", "your-resource-group")
    client_id = os.getenv("AZURE_CLIENT_ID", "your-client-id")
    tenant_id = os.getenv("AZURE_TENANT_ID", "your-tenant-id")
    client_secret = os.getenv("AZURE_CLIENT_SECRET", "your-client-secret")
    webhook_url = os.getenv("WEBHOOK_URL", "")
    mode = os.getenv("MODE", "dev")  # Default to dev mode
    
    print(f"\nRunning in {mode.upper()} mode")
    print(f"Notifications will be: {'printed locally' if mode.lower() in ('', 'dev') else 'sent to webhook'}")
    
    # Check current status
    print("\n1. Checking VM status...")
    status = check_status(
        subscription_id=subscription_id,
        vm_name=vm_name,
        resource_group=resource_group,
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
    )
    
    if status:
        print(f"   Current status: {status}")
    else:
        print("   Failed to get VM status")
        return
    
    # Start VM
    print("\n2. Starting VM...")
    success = start_vm(
        subscription_id=subscription_id,
        vm_name=vm_name,
        resource_group=resource_group,
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
        webhook_url=webhook_url,
        mode=mode,
    )
    
    if success:
        print("   VM started successfully!")
    else:
        print("   Failed to start VM")
    
    # Check status again
    print("\n3. Checking VM status after start...")
    status = check_status(
        subscription_id=subscription_id,
        vm_name=vm_name,
        resource_group=resource_group,
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
    )
    print(f"   Current status: {status}")
    
    # Stop VM
    print("\n4. Stopping VM...")
    success = stop_vm(
        subscription_id=subscription_id,
        vm_name=vm_name,
        resource_group=resource_group,
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
        webhook_url=webhook_url,
        mode=mode,
    )
    
    if success:
        print("   VM stopped successfully!")
    else:
        print("   Failed to stop VM")


def example_class_usage():
    """Example 2: Using AvmOperation class for multiple operations"""
    print("\n" + "=" * 60)
    print("Example 2: Using AvmOperation Class")
    print("=" * 60)
    
    mode = os.getenv("MODE", "dev")
    print(f"\nRunning in {mode.upper()} mode")
    
    # Initialize operator once for multiple operations
    operator = AvmOperation(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID", "your-subscription-id"),
        vm_name=os.getenv("AZURE_VM_NAME", "your-vm-name"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP", "your-resource-group"),
        webhook_url=os.getenv("WEBHOOK_URL", ""),
        client_id=os.getenv("AZURE_CLIENT_ID", "your-client-id"),
        tenant_id=os.getenv("AZURE_TENANT_ID", "your-tenant-id"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET", "your-client-secret"),
        mode=mode,
    )
    
    # Check status
    print("\n1. Getting VM status...")
    status = operator.get_status()
    print(f"   Status: {status}")
    
    # Start VM
    print("\n2. Starting VM...")
    if operator.start_vm():
        print("   VM started!")
    
    # Stop VM
    print("\n3. Stopping VM...")
    if operator.stop_vm():
        print("   VM stopped!")


def example_batch_operations():
    """Example 3: Batch operations on multiple VMs"""
    print("\n" + "=" * 60)
    print("Example 3: Batch Operations on Multiple VMs")
    print("=" * 60)
    
    # List of VMs to manage
    vms = [
        {
            "name": "vm1",
            "resource_group": "rg1",
        },
        {
            "name": "vm2",
            "resource_group": "rg2",
        },
    ]
    
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "your-subscription-id")
    client_id = os.getenv("AZURE_CLIENT_ID", "your-client-id")
    tenant_id = os.getenv("AZURE_TENANT_ID", "your-tenant-id")
    client_secret = os.getenv("AZURE_CLIENT_SECRET", "your-client-secret")
    webhook_url = os.getenv("WEBHOOK_URL", "")
    
    print("\nStarting all VMs...")
    for vm in vms:
        print(f"\n  Starting {vm['name']}...")
        success = start_vm(
            subscription_id=subscription_id,
            vm_name=vm["name"],
            resource_group=vm["resource_group"],
            client_id=client_id,
            tenant_id=tenant_id,
            client_secret=client_secret,
            webhook_url=webhook_url,
        )
        print(f"    Result: {'Success' if success else 'Failed'}")


def example_error_handling():
    """Example 4: Proper error handling"""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling")
    print("=" * 60)
    
    try:
        # Attempt to get status
        status = check_status(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID", "invalid-sub-id"),
            vm_name="nonexistent-vm",
            resource_group="nonexistent-rg",
            client_id=os.getenv("AZURE_CLIENT_ID", "invalid-client-id"),
            tenant_id=os.getenv("AZURE_TENANT_ID", "invalid-tenant-id"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET", "invalid-secret"),
        )
        
        if status:
            print(f"VM Status: {status}")
        else:
            print("Failed to get VM status - VM might not exist or credentials are invalid")
    
    except Exception as e:
        print(f"Error occurred: {e}")


def example_conditional_start():
    """Example 5: Conditional start - only start if VM is stopped"""
    print("\n" + "=" * 60)
    print("Example 5: Conditional Start")
    print("=" * 60)
    
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "your-subscription-id")
    vm_name = os.getenv("AZURE_VM_NAME", "your-vm-name")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP", "your-resource-group")
    client_id = os.getenv("AZURE_CLIENT_ID", "your-client-id")
    tenant_id = os.getenv("AZURE_TENANT_ID", "your-tenant-id")
    client_secret = os.getenv("AZURE_CLIENT_SECRET", "your-client-secret")
    webhook_url = os.getenv("WEBHOOK_URL", "")
    
    # Check current status
    print("\nChecking VM status...")
    status = check_status(
        subscription_id=subscription_id,
        vm_name=vm_name,
        resource_group=resource_group,
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
    )
    
    if status:
        print(f"Current status: {status}")
        
        # Only start if VM is not running
        if "running" not in status.lower():
            print("VM is not running, starting it...")
            start_vm(
                subscription_id=subscription_id,
                vm_name=vm_name,
                resource_group=resource_group,
                client_id=client_id,
                tenant_id=tenant_id,
                client_secret=client_secret,
                webhook_url=webhook_url,
            )
        else:
            print("VM is already running, no action needed")
    else:
        print("Could not determine VM status")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Azure VM Operation Examples")
    print("=" * 60)
    print("\nMake sure to set the following environment variables:")
    print("  - AZURE_SUBSCRIPTION_ID")
    print("  - AZURE_VM_NAME")
    print("  - AZURE_RESOURCE_GROUP")
    print("  - AZURE_CLIENT_ID")
    print("  - AZURE_TENANT_ID")
    print("  - AZURE_CLIENT_SECRET")
    print("  - WEBHOOK_URL (optional, required in production mode)")
    print("  - MODE (optional: 'dev' or empty for local logging, other values for webhook)")
    print("\nOr modify the code to use hardcoded values for testing.")
    print("=" * 60)
    
    # Uncomment the example you want to run
    
    # example_basic_usage()
    # example_class_usage()
    # example_batch_operations()
    # example_error_handling()
    # example_conditional_start()
    
    print("\n\nTo run an example, uncomment the corresponding line at the bottom of this file.")
