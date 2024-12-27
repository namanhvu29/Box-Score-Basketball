import os
import pandas as pd
image_path = "/home/namanh/Vu_Nam_Anh/Box Score Basketball Code/Image/e37b1750b2a80ff656b9.jpg"

data = {
    "Player" : ["Phuong", "Linh"],
    "PTS" : [15, 10],
    "REB" : [3, 2],
}

df = pd.DataFrame(data)
df.to_excel("basketball_stats.xlxs", index = False, engine='openpyxl')
print("file exel da dc tao")