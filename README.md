# Serial TPMS Receiver - Complete Protocol Analysis

Reverse engineering of serial data from a USB TPMS (Tire Pressure Monitoring System) receiver. This project includes real-time monitoring tools, protocol documentation, and customizable sensor mappings.

These devices are found on sites like AliExpress
https://www.aliexpress.us/item/3256805902381155.html
https://www.aliexpress.us/item/3256806718424409.html

The sensors I've seen operate on 433.92MHz. Others may use other frequencies. All you need to know, though, is how to read the serial data.

## 📊 **Protocol Specification**

**Confirmed 8-byte packet structure:**
```
[55 AA] [08] [SENSOR_ID] [PRESSURE_PSI] [TEMP_°F] [00] [XOR_CHECKSUM]
```

- **Communication:** 19200 baud, 8-N-1, USB Serial
- **Update Rate:** ~400-600ms per sensor cycle
- **Pressure:** Direct PSI values (0-255 range)
- **Temperature:** Direct Fahrenheit values
- **Validation:** XOR checksum of bytes 0-6

## 🚗 **Confirmed Sensor Mapping**

My sample sensors:

| Sensor ID | Location 
|-----------|----------
| **0** | Front Left (FL)
| **1** | Front Right (FR)
| **16** | Rear Left (RL) 
| **17** | Rear Right (RR)
| **5** | Internal Reference

## 🚀 **Quick Start**

### Prerequisites
```bash
pip install pyserial
```

### Real-time Monitoring
```bash
# Basic monitoring with decoded output
python tpms_monitor.py COM21 -b 19200

# With data logging
python tpms_monitor.py COM21 -b 19200 -l tpms_data.log
```

### Protocol Analysis
```bash
# Analyze captured data
python tpms_decoder.py tpms_data.log

# Temperature correlation analysis  
python temperature_analyzer.py tpms_data.log 71
```

## 📁 **Project Files**

- **`tpms_monitor.py`** - Real-time monitoring with decoded TPMS output
- **`tpms_decoder.py`** - Protocol analyzer and packet decoder
- **`temperature_analyzer.py`** - Temperature correlation analysis
- **`TPMS_SYSTEM_COMPLETE.md`** - Complete technical documentation
- **`requirements.txt`** - Python dependencies
- **`run_monitor.bat`** - Windows quick-start script

## 🔍 **Key Discoveries**

1. **Sensor Activation:** Sensors only transmit when pressurized (>0 PSI)
2. **Data Accuracy:** Pressure readings match actual tire pressures exactly
3. **Temperature Monitoring:** Realistic ambient temperature readings in °F
4. **Internal Sensor:** Receiver has built-in temperature reference (~10°F warmer)
5. **Protocol Reliability:** Perfect XOR checksums, consistent timing

## 📈 **Sample Decoded Output**

```
🎯 DECODED TPMS DATA:
   Sensor ID: 0 (0x00)
   💨 Pressure: 21 PSI
   🌡️ Temperature: 73°F
   📍 Location: Front Left (FL) 🎯
   Status: ✅ Normal pressure
   Temp Status: 🌡️ Normal
   Checksum: ✓ Valid
```

## 🛠️ **Hardware Setup**

1. Connect USB TPMS receiver to computer
2. Install TPMS sensors on tires (or test with pressurized sensors)
3. Identify COM port using Device Manager or `run_monitor.bat`
4. Run monitoring software at 19200 baud

## 📚 **Technical Documentation**

See **`TPMS_SYSTEM_COMPLETE.md`** for comprehensive protocol documentation, testing methodology, and complete technical specifications.
