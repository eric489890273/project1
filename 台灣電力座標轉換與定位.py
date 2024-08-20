"""
電力轉標轉換邏輯為，將電力座標(EX: Q0445DD4116)
先轉換成 二度分帶：TWD67 TM2 台灣座標
再轉換成 WGS84
pyproj==3.3.0
"""
import os
import pandas as pd
import glob
from pyproj import Proj, transform, Transformer

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
# https://garyliao-13743.medium.com/coordinate-system-transformation-efa943d3ddcd
wgs84 = Proj('EPSG:4326')  # TWD97/WGS84
twd67 = Proj('EPSG:3821'+' +title=經緯度：TWD67 +proj=longlat  +towgs84=-752,-358,-179,-.0000011698,.0000018398,.0000009822,.00002329 +ellps=aust_SA +no_defs')  # 經緯度：TWD67

twd97_TM2_taiwan = Proj('EPSG:3826'+' +title=二度分帶：TWD97 TM2 台灣 +proj=tmerc  +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +no_defs', preserve_units=False)  # 二度分帶：TWD97 TM2 台灣
twd97_TM2_punhu = Proj('EPSG:3825'+' +title=二度分帶：TWD97 TM2 澎湖 +proj=tmerc  +lat_0=0 +lon_0=119 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +no_defs', preserve_units=False)  # 二度分帶：TWD97 TM2 澎湖
twd67_TM2_taiwan = Proj('EPSG:3828'+' +title=二度分帶：TWD67 TM2 台灣 +proj=tmerc  +towgs84=-752,-358,-179,-.0000011698,.0000018398,.0000009822,.00002329 +lat_0=0 +lon_0=121 +x_0=250000 +y_0=0 +k=0.9999 +ellps=aust_SA',preserve_units=False)  #二度分帶：TWD67 TM2 台灣
twd67_TM2_punhu = Proj('EPSG:3827'+' +title=二度分帶：TWD67 TM2 澎湖 +proj=tmerc  +towgs84=-752,-358,-179,-.0000011698,.0000018398,.0000009822,.00002329 +lat_0=0 +lon_0=119 +x_0=250000 +y_0=0 +k=0.9999 +ellps=aust_SA',preserve_units=False)  #二度分帶：TWD67 TM2 澎湖

inProj = twd67_TM2_taiwan
outProj = wgs84
t = Transformer.from_proj(inProj, outProj)

def read_csv_file():
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for f in csv_files:
        print(f)
        df = pd.read_csv(f, encoding='utf-8')
    return df

# read csv file
def read_multiple_csv_files():
    path = os.getcwd()
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df = pd.concat((pd.read_csv(f) for f in all_files))
    return df

# find taicode in taiGridArr equal taiGrid fist char
def findTaiCode(taiGrid):
    # assert taiGrid is string
    assert isinstance(taiGrid, str)
    taiGrid = taiGrid.strip().upper()
    for i in range(len(taiGridArr)):
        if taiGridArr[i]['taiCode'] == taiGrid[0]:
            return taiGridArr[i]

def convertTaiT67(taiGrid):
    taiGrid = taiGrid.strip()
    taiXY = findTaiCode(taiGrid)

    t1x = taiXY['taiGrid'][0]; ## digi(0) 字母，大區塊原點 (80km×50km)
    t1y = taiXY['taiGrid'][1]; ## digi(1) 字母，大區塊原點 (80km×50km)

    # substring from taiGrid
    t2x = int(taiGrid[1:3]) * 800 ## digi(1-2)(3-4) 數字區塊 (800m×500m)
    t2y = int(taiGrid[3:5]) * 500

    # get char at index 5 from taiGrid
    # transfer it into UTF-16 code
    t3x = int(ord(taiGrid[5]) - ord('A')) *100;  # digi(5-6) 字母區塊(100m×100m)
    t3y = int(ord(taiGrid[6]) - ord('A')) *100;  # 首位字母 Unicode 编码

    # if taiGrid is 9
    if len(taiGrid) == 9:
        t99x = 0
        t99y = 0
    else:
        t99x = int(taiGrid[9]) * 1
        t99y = int(taiGrid[10]) * 1

    t5x = int(taiGrid[7])*10 + t99x
    t5y = int(taiGrid[8])*10 + t99y

    return [t1x + t2x + t3x + t5x, t1y + t2y + t3y + t5y]

def main():
    # 讀寫單一檔案
    df = read_csv_file()

    # 轉換圖號座標
    df[['TW67_X', 'TW67_Y']] = df['圖號座標'].transform(convertTaiT67).to_list()

    # 轉換 WGS84 座標
    lon, lat = t.transform(df['TW67_X'], df['TW67_Y'])
    df['lon'] = lon
    df['lat'] = lat

    # save csv file
    df.to_csv('twd67_to_wgs84.csv', index=False)

if __name__ == '__main__':
    main()