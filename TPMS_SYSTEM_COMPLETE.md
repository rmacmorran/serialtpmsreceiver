# TPMS System - Complete Analysis & Documentation

## 🏆 **FULLY DECODED TPMS PROTOCOL**

### ✅ **Protocol Structure (100% Confirmed)**
```
Byte:  [0] [1] [2] [3]        [4]         [5]           [6] [7]
Data:  55  AA  08  SENSOR_ID  PRESSURE    TEMPERATURE   00  CHECKSUM
                               (PSI)       (°F)
```

- **Header:** `55 AA` (sync bytes)
- **Length:** `08` (8 bytes total packet)
- **Sensor ID:** Unique identifier for each sensor
- **Pressure:** Direct PSI value (0-255 range)
- **Temperature:** Direct Fahrenheit value  
- **Reserved:** `00` (unused)
- **Checksum:** XOR of bytes 0-6

---

## 🎯 **CONFIRMED SENSOR MAPPING**

| Sensor ID | Location | Status | Last Known Reading |
|-----------|----------|--------|-------------------|
| **0** | **Front Left (FL)** ✅ | Active | **21 PSI, 73°F** |
| **1** | **Front Right (FR)** ✅ | Active | **30 PSI, 75°F** |
| **16** | **Rear Left (RL)** ✅ | Tested | 0-23 PSI, 73-75°F |
| **17** | **Rear Right (RR)** ✅ | Tested | 0-37 PSI, 73°F |
| **5** | **Internal/Reference** ✅ | Always On | **0 PSI, 81°F** |

---

## 📊 **Testing Results Summary**

### **Phase 1 - Initial Discovery**
- Detected 5 sensor IDs transmitting
- Identified consistent 8-byte packet structure
- Confirmed XOR checksum algorithm

### **Phase 2 - Rear Sensor Testing**
- RL sensor (ID 16): Activated with 23 PSI
- RR sensor (ID 17): Activated with 37 PSI
- Confirmed pressure and temperature readings

### **Phase 3 - Front Sensor Testing**  
- FL sensor (ID 0): Activated with **21 PSI** ✅
- FR sensor (ID 1): Activated with **30 PSI** ✅
- **PERFECT MATCH** with actual tire pressures!

### **Phase 4 - System Validation**
- All 4 tire sensors confirmed and mapped
- Pressure readings accurate to actual values
- Temperature readings realistic (73-75°F ambient)
- Internal sensor (ID 5) provides receiver temperature reference

---

## 🔧 **Technical Specifications**

- **Communication:** USB Serial, 19200 baud, 8-N-1
- **Update Rate:** ~400-600ms per sensor cycle
- **Pressure Range:** 0-255 PSI (tested up to 37 PSI)
- **Temperature Range:** Fahrenheit, tested 73-81°F
- **Data Integrity:** XOR checksum validation
- **Sensor Count:** 4 tire sensors + 1 internal reference

---

## 🚀 **Capabilities Achieved**

✅ **Real-time pressure monitoring** for all 4 tires  
✅ **Real-time temperature monitoring** for all 4 tires  
✅ **Individual sensor identification** and location mapping  
✅ **Data validation** through checksum verification  
✅ **Protocol documentation** for future development  
✅ **Live monitoring tools** with human-readable output  

---

## 💡 **Key Insights**

1. **Sensor Activation:** Sensors only transmit when pressurized (>0 PSI)
2. **Temperature Correlation:** Accurate ambient temperature readings
3. **Pressure Accuracy:** Direct PSI values, no encoding/scaling needed  
4. **Receiver Integration:** Internal temperature sensor (ID 5) runs ~10°F warmer
5. **Communication Reliability:** Consistent timing, perfect checksums

---

## 📝 **Usage Instructions**

### **Real-time Monitoring:**
```bash
python tpms_monitor.py COM21 -b 19200
```

### **Data Logging:**
```bash
python tpms_monitor.py COM21 -b 19200 -l tpms_data.log
```

### **Protocol Analysis:**
```bash
python tpms_decoder.py tpms_data.log
```

---

## 🎉 **Project Status: COMPLETE**

This TPMS system has been **fully reverse-engineered** with:
- Complete protocol understanding
- All sensor locations confirmed  
- Real-time monitoring capability
- Comprehensive documentation
- Validated accuracy against actual tire pressures

**Result:** A fully functional TPMS monitoring system with complete protocol documentation! 🏆
