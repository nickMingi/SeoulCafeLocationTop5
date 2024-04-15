import pandas as pd
import matplotlib.pyplot as plt
import mpld3

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
plt.show()
