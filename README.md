# TPMS Serial Monitor

A Python-based tool for visualizing data from USB TPMS (Tire Pressure Monitoring System) receivers that behave as serial devices.

## Quick Start

1. **Connect your TPMS receiver** to a USB port
2. **Run the batch file** to see available COM ports:
   ```
   run_monitor.bat
   ```
3. **Start monitoring** (replace COM20 with your device's port):
   ```
   python tpms_monitor.py COM20
   ```

## Usage Examples

### Basic monitoring (9600 baud, default):
```bash
python tpms_monitor.py COM20
```

### Try different baud rates:
```bash
python tpms_monitor.py COM20 -b 19200
python tpms_monitor.py COM20 -b 38400
python tpms_monitor.py COM20 -b 115200
```

### Monitor with data logging:
```bash
python tpms_monitor.py COM20 -l tpms_data.log
```

## What You'll See

The monitor displays data in multiple formats:
- **Timestamp** - When data was received
- **HEX** - Raw bytes in hexadecimal format
- **ASCII** - Printable characters (dots for non-printable)
- **RAW** - Decimal byte values
- **TEXT** - Decoded text if available

Example output:
```
[14:32:15.123] Received 8 bytes:
HEX: 55 AA 01 23 45 67 89 AB                        ASCII: [U.....g..]
RAW: 85 170 1 35 69 103 137 171
TEXT: 'U\xaa\x01#Eg\x89\xab'
----------------------------------------
```

## Common TPMS Settings to Try

Most TPMS devices use these settings:
1. **9600-8-N-1** (most common)
2. **19200-8-N-1** (second choice)
3. **38400-8-N-1** (less common)

All use: 8 data bits, no parity, 1 stop bit, no flow control.

## Troubleshooting

### No data appearing?
- Ensure your TPMS sensors are active (drive around or deflate/inflate a tire slightly)
- Try different baud rates
- Check that the correct COM port is being used

### Permission errors?
- Close any other programs that might be using the serial port
- Run PowerShell as administrator if needed

### Finding your device:
```powershell
Get-CimInstance -Class Win32_SerialPort | Select-Object DeviceID, Description
```

## Files Created

- `tpms_monitor.py` - Main monitoring script
- `requirements.txt` - Python dependencies
- `run_monitor.bat` - Quick start helper
- `tpms_data.log` - Data log (if logging enabled)

## Next Steps

Once you capture data:
1. Look for repeating patterns (packet headers/footers)
2. Correlate data changes with tire pressure changes
3. Identify sensor IDs, pressure values, temperatures
4. Create a decoder for the specific protocol

Press **Ctrl+C** to stop monitoring.
