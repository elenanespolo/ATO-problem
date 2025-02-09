import pandas as pd # type: ignore
import csv

## COMPONENTS
components_prices = {
    "Central Processing Unit (CPU)": 150,
    "Graphics Processing Unit (GPU) Intel": 240,
    "Graphics Processing Unit (GPU) NVIDIA": 320,
    "Motherboard": 30,
    "Random Access Memory (RAM) 16GB": 30,
    "Random Access Memory (RAM) 32GB": 50,
    "Storage Drive SSD 1TB": 60,
    "Storage Drive SSD 512GB": 40,
    "Storage Drive Hard Disk Drive": 25,
    "Battery": 20,
    "Cooling System (Intake Fans)": 20,
    "Cooling System (Exhaust Fans)": 18,
    "Cooling System (Heat Sinks)": 15,
    "Wi-Fi Card": 10,
    "Bluetooth Card": 10,
    "Sound Card": 15,
    "Screen": 70,
    "Keyboard": 20,
    "Backlit Keyboard": 30,
    "Touchpad": 20,
    "Webcam": 10,
    "Microphone": 10,
    "Fingerprint Reader": 20,
    "USB-B Port": 3,  # Integrated into motherboard, but if purchased separately
    "USB-C Port": 3,  # Integrated into motherboard, but if purchased separately
    "HDMI": 2,  # Integrated into motherboard, but if purchased separately
    "Audio Jack": 2,  # Integrated into motherboard, but if purchased separately
    "Ethernet Port": 2,  # Integrated into motherboard, but if purchased separately
    "SD Card Reader": 2,  # Integrated into motherboard, but if purchased separately
    "Laptop Chassis": 30,
    "Hinges": 10,
    "Speakers": 10,
    "Charging Port": 5
}

file_path = 'data/'

## ITEMS
products = ["Computer_A", "Computer_B"]

a = [[1,1], [0,1], [1,0], [1,1], [0,1], [1,0], [1,0], [0,1], [0,1], [1,1], [1,0], [0,1], [1,1], [1,1], [1,1], [1,1], [1,1], [0,1], [1,0], [1,1], [1,1], [1,1], [1,0], [1,1], [1,0], [1,1], [1,1], [0,1], [0,1], [1,1], [1,1], [1,1], [1,1]]
data = pd.DataFrame(a, columns=products, index=list(components_prices.keys()))

products_selling_price = {
    products[0]: 1800, 
    products[1]: 1600
}

## MACHINES
machines = [
    "Wave Soldering Machine",
    "Assembly Robot",
    "Pick-and-Place Machine",
    "Test Bench",
   "Presses and Case Molding Machine",
    "Laser or Plasma Cutting Machine",
    "Burn-in Machine (Stress Testing)",
    "Packaging Machine"
]

machine_daily_time = {
    "Wave Soldering Machine": 16*60*3,          # 16 hours per day
    "Assembly Robot": 24*60*2,                  # 24 hours per day (continuous operation)
    "Pick-and-Place Machine": 24*60*3,          # 24 hours per day (continuous operation)
    "Test Bench": 16*60*4,                      # 16 hours per day
    "Presses and Case Molding Machine": 16*60, # 16 hours per day
    "Laser or Plasma Cutting Machine": 16*60*3,  # 16 hours per day
    "Burn-in Machine (Stress Testing)": 24*60*5, # 24 hours per day (continuous operation)
    "Packaging Machine": 24*60             # 16 hours per day
}

processing_times = {
    "Central Processing Unit (CPU)": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 6,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Graphics Processing Unit (GPU) Intel": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 7,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Graphics Processing Unit (GPU) NVIDIA": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 10,
        "Pick-and-Place Machine": 3,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Motherboard": {
        "Wave Soldering Machine": 20,
        "Assembly Robot": 3,
        "Pick-and-Place Machine": 8,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Random Access Memory (RAM) 16GB": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Random Access Memory (RAM) 32GB": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Storage Drive SSD 1TB": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 5,
        "Pick-and-Place Machine": 6,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Storage Drive SSD 512GB": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 3,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Storage Drive Hard Disk Drive": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 1,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Battery": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Cooling System (Intake Fans)": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Cooling System (Exhaust Fans)": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 1,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Cooling System (Heat Sinks)": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Wi-Fi Card": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Bluetooth Card": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Sound Card": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Screen": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 5,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 30,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Keyboard": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 15,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Backlit Keyboard": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 3,
        "Pick-and-Place Machine": 4,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 20,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Touchpad": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Webcam": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Microphone": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Fingerprint Reader": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "USB-B Port": {
        "Wave Soldering Machine": 5,
        "Assembly Robot": 0.5,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "USB-C Port": {
        "Wave Soldering Machine": 5,
        "Assembly Robot": 0.5,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "HDMI": {
        "Wave Soldering Machine": 5,
        "Assembly Robot": 0.5,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Audio Jack": {
        "Wave Soldering Machine": 2,
        "Assembly Robot": 0.3,
        "Pick-and-Place Machine": 1,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Ethernet Port": {
        "Wave Soldering Machine": 5,
        "Assembly Robot": 0.5,
        "Pick-and-Place Machine": 1,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "SD Card Reader": {
        "Wave Soldering Machine": 5,
        "Assembly Robot": 0.5,
        "Pick-and-Place Machine": 1,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Laptop Chassis": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 0.1,
        "Pick-and-Place Machine": 1,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 10,
        "Laser or Plasma Cutting Machine": 20,
        "Burn-in Machine (Stress Testing)": 6,        
        "Packaging Machine": 0.02
    },
    "Hinges": {
        "Wave Soldering Machine": 0,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 10,
        "Laser or Plasma Cutting Machine": 5,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Speakers": {
        "Wave Soldering Machine": 10,
        "Assembly Robot": 2,
        "Pick-and-Place Machine": 2,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    },
    "Charging Port": {
        "Wave Soldering Machine": 5,
        "Assembly Robot": 1,
        "Pick-and-Place Machine": 15,
        "Test Bench": 3,
        "Presses and Case Molding Machine": 0,
        "Laser or Plasma Cutting Machine": 0,
        "Burn-in Machine (Stress Testing)": 6,
        "Packaging Machine": 0.02
    }
}

df = pd.DataFrame.from_dict(processing_times, orient='index', columns=machines)
df = pd.concat([df, data], axis=1)
df['price'] = df.index.map(components_prices)

df.to_csv(f"{file_path}components_data.csv")

with open(f'{file_path}products_machines.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([len(products), len(machines)])
    for prod in products:
        writer.writerow([prod, products_selling_price[prod]])
    for mac in machines:
        writer.writerow([mac, machine_daily_time[mac]])


    
