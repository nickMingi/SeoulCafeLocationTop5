import pandas as pd
import matplotlib.pyplot as plt
import folium
from geopy.distance import geodesic

data = pd.read_csv('data/서울교통공사_역별 일별 시간대별 승하차인원 정보_23.11_24.01.csv', encoding='cp949')

stationdata = data[data['날짜'].str.contains('2024-01-31')]

top5 = stationdata.iloc[:, 6:]
top5['total'] = top5.apply(sum, axis=1)

stationdata['total'] = top5['total']

stationdata = stationdata.sort_values(by='total', ascending=False)
stationdata = stationdata.reset_index()
stationdata = stationdata.drop(columns='index', axis=1)

grouped_df = stationdata.groupby('역명')['total'].sum().reset_index()
grouped_df = grouped_df.sort_values(by='total', ascending=False)

top10 = grouped_df.head(10)
print(top10)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

stations = top10["역명"]
population = top10["total"]

plt.figure(figsize=(10,6))
plt.bar(stations,population,color="skyblue")
plt.title("역별 유동인구")
plt.xlabel("역명")
plt.ylabel("유동인구")
plt.savefig("./SeoulCafeLocationTopFive/src/main/webapp/img/stationMovePopulation.png")

seoulStationDF = pd.read_csv("./data/seoulStation.csv")

seoulStationCafe = seoulStationDF[seoulStationDF["상권업종소분류명"] == "카페"]

# 지도의 중심을 설정합니다
map = folium.Map(location=[37.5558, 126.9723], zoom_start=17)

# 원을 그릴 위치의 위도와 경도를 설정합니다
circle_lat_lon = [37.5558, 126.9723]

# 원을 추가합니다
folium.Circle(
    location=circle_lat_lon,
    radius=200,  # 원의 반지름 (미터 단위)
    color='crimson',
    fill=True,
    fill_color='crimson'
).add_to(map)

# 중복된 위치에 마커를 찍기 위한 작은 변화량
delta = 0.00001
count = 0
mapCopied = map
for index, row in seoulStationCafe.iterrows():
    location = (row['위도']+ delta * count, row['경도']+ delta * count)
    print(location)
    count += 1
    folium.Marker(location = location,
                  popup=row["상호명"],
              tooltip=row["상호명"]).add_to(mapCopied)

mapCopied.save("./SeoulCafeLocationTopFive/src/main/webapp/seoulStationCafe.html")