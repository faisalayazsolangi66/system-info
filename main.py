#!/usr/bin/env python3
"""Print CPU, memory, disk and OS information (stdlib only)."""
import argparse
import json
import os
import platform
import shutil


def fmt_bytes(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def read_meminfo():
    info = {}
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    info[parts[0].rstrip(":")] = int(parts[1]) * 1024
    except OSError:
        pass
    return info


def cpu_info():
    model = "unknown"
    count = os.cpu_count() or 0
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    load = None
    try:
        load = os.getloadavg()
    except OSError:
        pass
    return {"model": model, "cores": count, "load_average": load}


def main():
    p = argparse.ArgumentParser(description="Print CPU, memory, disk and OS information.")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--disk", default="/", help="Path whose disk usage to report (default: /)")
    args = p.parse_args()

    mem = read_meminfo()
    total = mem.get("MemTotal", 0)
    avail = mem.get("MemAvailable", mem.get("MemFree", 0))
    used = total - avail if total else 0
    disk = shutil.disk_usage(args.disk)
    data = {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "cpu": cpu_info(),
        "memory": {
            "total": total, "used": used, "available": avail,
            "total_human": fmt_bytes(total), "used_human": fmt_bytes(used),
            "available_human": fmt_bytes(avail),
        },
        "disk": {
            "path": args.disk, "total": disk.total, "used": disk.used,
            "free": disk.free, "total_human": fmt_bytes(disk.total),
            "used_human": fmt_bytes(disk.used), "free_human": fmt_bytes(disk.free),
        },
    }
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print(f"OS:        {data['os']} {data['os_release']} ({data['machine']})")
    print(f"Version:   {data['os_version']}")
    print(f"Python:    {data['python']}")
    cpu = data["cpu"]
    print(f"CPU:       {cpu['model']}")
    print(f"Cores:     {cpu['cores']}")
    if cpu["load_average"]:
        print("Load avg:  " + ", ".join(f"{v:.2f}" for v in cpu["load_average"]))
    m = data["memory"]
    pct = (m["used"] / m["total"] * 100) if m["total"] else 0
    print(f"Memory:    {m['used_human']} used / {m['total_human']} total "
          f"({pct:.1f}%), {m['available_human']} available")
    d = data["disk"]
    dpct = (d["used"] / d["total"] * 100) if d["total"] else 0
    print(f"Disk {d['path']}: {d['used_human']} used / {d['total_human']} total "
          f"({dpct:.1f}%), {d['free_human']} free")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
