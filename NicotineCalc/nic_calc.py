def estimate_nicotine_from_pod(nic_strength_mgml, puffs_per_day, puff_volume_ml=0.001, absorption_rate=0.5):
    """
    Calculate estimated nicotine absorbed from a pod device.
    """
    total_liquid_ml = puff_volume_ml * puffs_per_day
    total_nicotine = total_liquid_ml * nic_strength_mgml
    absorbed_nicotine = total_nicotine * absorption_rate
    return absorbed_nicotine

def estimate_nicotine_from_cigarettes(nicotine_per_cigarette, num_cigarettes):
    """
    calculate estimated nicotine absorbed from cigarettes.
    """
    return nicotine_per_cigarette * num_cigarettes

def main():
    print("__::::: Calculate Nicotine Absorption from Pods or Cigarettes :::::__")

    # Get Pod/Vape/Podmod Details
    device_type = input("Device Type: (pod / vape / podmod): ").lower()
    coil_resistance = float(input("OHM of Cartridge or Coil (example: 0.9): "))
    wattage = float(input("Wattage (example: 10): "))
    nic_strength = float(input("Nicotine in Salt Liquid(mg/ml): "))
    puffs_per_day = int(input("Puff per day: "))

    # Get Cigarette Details
    prev_nic_per_cig = float(input("Nicotine of Cigarettes(mg/cigarette): "))
    prev_cigarettes = int(input("Cigarettes per day: "))

    # Puff volume which set per device type
    if device_type == 'pod':
        puff_volume = 0.0008  # ml
    elif device_type == 'vape':
        puff_volume = 0.0015
    elif device_type == 'podmod':
        puff_volume = 0.0012
    else:
        puff_volume = 0.001  # Default value

    # Nicotine Calculating
    pod_nicotine = estimate_nicotine_from_pod(nic_strength, puffs_per_day, puff_volume)
    cig_nicotine = estimate_nicotine_from_cigarettes(prev_nic_per_cig, prev_cigarettes)

    percent_of_cig = (pod_nicotine / cig_nicotine) * 100 if cig_nicotine else 0

    print("\n📊 Results:\n")
    print(f"- Nicotine from Pod/Vape/Podmod: {pod_nicotine:.2f} mg/day")
    print(f"- Nicotine from Cigarettes: {cig_nicotine:.2f} mg/day\n")
    print(f"✅ You now smoking {percent_of_cig:.1f} % of old cigarettes.")

    # If using Nicotine more than cigarettes
    if percent_of_cig > 100:
        print("⚠️ Warning: You are using more nicotine than cigarettes!")
    elif percent_of_cig < 30:
        print("👍🏼 You are using less nicotine than cigarettes!")

if __name__ == "__main__":
    main()
