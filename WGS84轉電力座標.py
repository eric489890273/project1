import os
import pandas as pd
import glob
from pyproj import Proj, Transformer

# init object array
taiGridArr = [
    {'taiCode': 'A', 'taiGrid': [170000, 2750000]},
    {'taiCode': 'B', 'taiGrid': [250000, 2750000]},
    {'taiCode': 'C', 'taiGrid': [330000, 2750000]},
    {'taiCode': 'D', 'taiGrid': [170000, 2700000]},
    {'taiCode': 'E', 'taiGrid': [250000, 2700000]},
    {'taiCode': 'F', 'taiGrid': [330000, 2700000]},
    {'taiCode': 'G', 'taiGrid': [170000, 2650000]},
    {'taiCode': 'H', 'taiGrid': [250000, 2650000]},
    {'taiCode': 'J', 'taiGrid': [90000, 2600000]},
    {'taiCode': 'K', 'taiGrid': [170000, 2600000]},
    {'taiCode': 'L', 'taiGrid': [250000, 2600000]},
    {'taiCode': 'M', 'taiGrid': [90000, 2550000]},
    {'taiCode': 'N', 'taiGrid': [170000, 2550000]},
    {'taiCode': 'O', 'taiGrid': [250000, 2550000]},
    {'taiCode': 'P', 'taiGrid': [90000, 2500000]},
    {'taiCode': 'Q', 'taiGrid': [170000, 2500000]},
    {'taiCode': 'R', 'taiGrid': [250000, 2500000]},
    {'taiCode': 'T', 'taiGrid': [170000, 2450000]},
    {'taiCode': 'U', 'taiGrid': [250000, 2450000]},
    {'taiCode': 'V', 'taiGrid': [170000, 2400000]},
    {'taiCode': 'W', 'taiGrid': [250000, 2400000]},
    {'taiCode': 'X', 'taiGrid': [275000, 2614000]},
    {'taiCode': 'Y', 'taiGrid': [275000, 2564000]}
]

# init Proj
wgs84 = Proj('EPSG:4326')  # WGS84
twd67_TM2_taiwan = Proj('EPSG:3828'+' +title=二度分帶：TWD67 TM2 台灣 +proj=tmerc  +towgs84=-752,-358,-179,-.0000011698,.0000018398,.0000009822,.00002329 +lat_0=0 +lon_0=121 +x_0=250000 +y_0=0 +k=0.9999 +ellps=aust_SA', preserve_units=False)  # 二度分帶：TWD67 TM2 台灣

# Transformer for converting between WGS84 and TWD67 TM2
t = Transformer.from_proj(wgs84, twd67_TM2_taiwan)

def read_csv_file():
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for f in csv_files:
        print(f)
        df = pd.read_csv(f, encoding='utf-8')
    return df

def convertT67ToTai(t67_x, t67_y):
    # Find the matching grid in taiGridArr
    for grid in taiGridArr:
        t1x, t1y = grid['taiGrid']

        # Calculate the difference from the grid origin
        dx = t67_x - t1x
        dy = t67_y - t1y

        if 0 <= dx < 80000 and 0 <= dy < 50000:
            # Determine the indices for the grid
            digit2_x = int(dx // 800)
            digit2_y = int(dy // 500)

            # Determine the letters for the 100m x 100m block
            letter_x = chr(int(dx % 800 // 100) + ord('A'))
            letter_y = chr(int(dy % 500 // 100) + ord('A'))

            # The last digits
            digit5_x = int(dx % 100 // 10)
            digit5_y = int(dy % 100 // 10)

            # The extra digits
            digit6_x = int(dx % 10)
            digit6_y = int(dy % 10)

            return f"{grid['taiCode']}{digit2_x:02}{digit2_y:02}{letter_x}{letter_y}{digit5_x}{digit5_y}{digit6_x}{digit6_y}"

    return None

def main():
    # 讀寫單一檔案
    df = read_csv_file()

    # 將 WGS84 座標轉換為 TWD67 TM2 座標
    df['TW67_X'], df['TW67_Y'] = t.transform(df['lon'], df['lat'])

    # 四捨五入至個位
    df['TW67_X'] = df['TW67_X'].round()
    df['TW67_Y'] = df['TW67_Y'].round()

    # 將 TWD67 TM2 座標轉換為電力座標
    df['電力座標'] = df.apply(lambda row: convertT67ToTai(row['TW67_X'], row['TW67_Y']), axis=1)

    # Save the new dataframe with the converted coordinates
    df.to_csv('wgs84_to_power_grid.csv', index=False)

if __name__ == '__main__':
    main()
