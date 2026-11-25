# System Info

Print CPU, memory, disk and OS information.

## Requirements

- Python 3.8+
- Standard library only — no third-party packages

## Usage

```bash
python3 main.py
python3 main.py --json
python3 main.py --disk /home
```

## Example

```bash
$ python3 main.py
OS:        Linux 6.8.0-31-generic (x86_64)
Version:   #31-Ubuntu SMP PREEMPT_DYNAMIC
Python:    3.12.3
CPU:       AMD Ryzen 5 5600G with Radeon Graphics
Cores:     12
Load avg:  0.42, 0.35, 0.31
Memory:    2.1 GB used / 15.5 GB total (13.5%), 13.4 GB available
Disk /: 18.2 GB used / 100.0 GB total (18.2%), 81.8 GB free
```

## License

MIT — see [LICENSE](LICENSE).
