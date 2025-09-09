#!/usr/bin/env python3
"""
TPMS Temperature Correlation Analyzer
"""

import re
from collections import defaultdict

def analyze_temperature_correlation(log_file, actual_temp_f):
    """Analyze temperature correlation with known ambient temperature"""
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Extract packets
    hex_pattern = r'HEX: ([0-9A-F\s]+?)\s+ASCII:'
    matches = re.findall(hex_pattern, content)
    
    packets = []
    for match in matches:
        hex_bytes = match.strip().split()
        if len(hex_bytes) == 8:
            packet = [int(b, 16) for b in hex_bytes]
            packets.append(packet)
    
    print(f"🌡️  TEMPERATURE CORRELATION ANALYSIS")
    print(f"=" * 50)
    print(f"Actual ambient temperature: {actual_temp_f}°F")
    print()
    
    # Group by sensor ID and temperature value
    sensor_temps = defaultdict(list)
    
    for packet in packets:
        sensor_id = packet[3]  # Byte 3
        temp_value = packet[5]  # Byte 5
        sensor_temps[sensor_id].append(temp_value)
    
    print("📊 SENSOR READINGS:")
    print("-" * 30)
    
    for sensor_id in sorted(sensor_temps.keys()):
        temps = sensor_temps[sensor_id]
        avg_temp = sum(temps) / len(temps)
        temp_diff = avg_temp - actual_temp_f
        
        print(f"Sensor ID 0x{sensor_id:02X} ({sensor_id:2d}): ", end="")
        print(f"Value {int(avg_temp):3d} ", end="")
        print(f"(Δ{temp_diff:+.1f}°F from ambient)", end="")
        
        # Assess correlation
        if abs(temp_diff) <= 5:
            print(" ✅ LIKELY TEMPERATURE")
        elif abs(temp_diff) <= 15:
            print(" ⚠️  POSSIBLE TEMPERATURE (with offset)")
        else:
            print(" ❌ UNLIKELY TEMPERATURE")
    
    print(f"\n🔍 ANALYSIS:")
    print("-" * 20)
    
    all_temps = []
    for temps in sensor_temps.values():
        all_temps.extend(temps)
    
    unique_temps = sorted(set(all_temps))
    print(f"Unique temperature values: {unique_temps}")
    
    # Check if values cluster around ambient
    close_temps = [t for t in unique_temps if abs(t - actual_temp_f) <= 15]
    if close_temps:
        print(f"Values within ±15°F of ambient: {close_temps}")
        print("✅ Strong indication that Byte 5 = Temperature in °F")
    else:
        print("❌ No values close to ambient temperature")
        print("💡 Temperature might be in different units or byte position")
    
    print(f"\n🎯 CONCLUSIONS:")
    print("-" * 25)
    if len(close_temps) >= len(unique_temps) * 0.5:
        print("✅ Byte 5 appears to contain temperature data in Fahrenheit")
        print("✅ Different sensors may have slight calibration differences")
        print("💡 Variations could be due to:")
        print("   - Sensor location (sun exposure, engine heat)")
        print("   - Internal electronics heating") 
        print("   - Calibration offsets")
    else:
        print("❓ Temperature correlation unclear")
        print("💡 May need more data or different conditions")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python temperature_analyzer.py <log_file> <ambient_temp_f>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    ambient_temp = float(sys.argv[2])
    analyze_temperature_correlation(log_file, ambient_temp)
