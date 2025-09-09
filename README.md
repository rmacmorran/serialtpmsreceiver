# Serial TPMS Receiver - Complete Protocol Analysis

🏆 **FULLY DECODED USB TPMS RECEIVER PROTOCOL**

A complete reverse engineering project that successfully decoded a USB TPMS (Tire Pressure Monitoring System) receiver's serial protocol. This project includes real-time monitoring tools, protocol documentation, and validated sensor mappings.

## 🎯 **Project Achievement**

✅ **Complete protocol reverse engineering**  
✅ **All 4 tire sensors identified and mapped**  
✅ **Real-time pressure monitoring** (validated: 21 PSI FL, 30 PSI FR)  
✅ **Real-time temperature monitoring** in Fahrenheit  
✅ **Protocol documentation** with XOR checksum validation  
✅ **Professional monitoring tools** with decoded output  

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

| Sensor ID | Location | Validated Reading |
|-----------|----------|------------------|
| **0** | Front Left (FL) | 21 PSI, 73°F ✅ |
| **1** | Front Right (FR) | 30 PSI, 75°F ✅ |
| **16** | Rear Left (RL) | 0-23 PSI, 73-75°F ✅ |
| **17** | Rear Right (RR) | 0-37 PSI, 73°F ✅ |
| **5** | Internal Reference | 0 PSI, 81°F ✅ |

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

## 🏆 **Project Status: COMPLETE**

This project successfully achieved complete reverse engineering of a USB TPMS receiver protocol with validated real-world testing and comprehensive documentation.

---

*This project demonstrates systematic protocol reverse engineering, real-time data analysis, and hardware validation techniques.*
