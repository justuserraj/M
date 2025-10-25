# sys_monitor.py
import psutil

def get_cpu_usage():
    """Returns the current system-wide CPU utilization percentage."""
    # interval=1 makes this a blocking call for 1 second, giving a more accurate average.
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"{cpu_percent:.1f}%"

def get_ram_usage():
    """Returns the current system-wide RAM utilization details."""
    v_mem = psutil.virtual_memory()
    total_gb = v_mem.total / (1024**3)
    used_gb = v_mem.used / (1024**3)
    percent = v_mem.percent
    
    report = (
        f"RAM Usage: {percent:.1f}% used\n"
        f"Total: {total_gb:.2f} GB\n"
        f"Used: {used_gb:.2f} GB"
    )
    return report

def get_disk_usage(path='/'):
    """Returns the disk usage for a specified path (defaults to root)."""
    try:
        disk = psutil.disk_usage(path)
        total_gb = disk.total / (1024**3)
        used_gb = disk.used / (1024**3)
        percent = disk.percent
        
        report = (
            f"Disk Usage ({path}): {percent:.1f}% used\n"
            f"Total: {total_gb:.2f} GB\n"
            f"Used: {used_gb:.2f} GB"
        )
        return report
    except Exception as e:
        return f"Could not retrieve disk usage for {path}. Error: {e}"

def get_system_report():
    """Generates a comprehensive system health report."""
    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()
    
    report = f"System Health Report:\n\nCPU Utilization: {cpu}\n\n{ram}\n\n{disk}"
    
    return report