import subprocess
import psutil
import time

def get_current_power_plan():
    result = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True, text=True)
    output = result.stdout.strip()
    return output.split(": ")[-1]

def set_power_plan(plan_guid):
    subprocess.run(["powercfg", "/setactive", plan_guid])

def main():
    threshold_high_gb = 6.0  # 6GB
    threshold_low_gb = 4.0   # 4GB
    balanced_plan_guid = '381b4222-f694-41f0-9685-ff5bb260df2e'  # GUID for Balanced power plan
    high_performance_plan_guid = '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'  # GUID for High Performance power plan
    power_saver_plan_guid = 'a1841308-3541-4fab-bc81-f71556f20b4a'  # GUID for Power Saver power plan

    current_power_plan = get_current_power_plan()

    while True:
        used_memory_gb = psutil.virtual_memory().used / (1024 ** 3)  # Convert bytes to gigabytes

        if used_memory_gb > threshold_high_gb and current_power_plan != high_performance_plan_guid:
            print("O uso de memória excedeu 6GB, alternando para o plano de energia: Alto desempenho.")
            set_power_plan(high_performance_plan_guid)
            current_power_plan = high_performance_plan_guid
        elif used_memory_gb > threshold_low_gb and used_memory_gb <= threshold_high_gb and current_power_plan != balanced_plan_guid:
            print("O uso de memória excedeu 4GB, alternando para o plano de energia: Equilibrado.")
            set_power_plan(balanced_plan_guid)
            current_power_plan = balanced_plan_guid
        elif used_memory_gb <= threshold_low_gb and current_power_plan != power_saver_plan_guid:
            print("O uso de memória está abaixo de 4GB, alternando para o plano de energia: Economia de energia.")
            set_power_plan(power_saver_plan_guid)
            current_power_plan = power_saver_plan_guid

        time.sleep(60)  # Sleep for 60 seconds before checking again

if __name__ == "__main__":
    main()
