select *
from 台北市youbike

drop table 台北市youbike

delete from 台北市youbike

INSERT INTO 台北市youbike (站點名稱, 行政區, 更新時間, 地址, 總車輛數, 可借, 可還) 
VALUES ('YouBike2.0_捷運科技大樓站','大安區','2023-11-10 09:55:09','復興南路二段235號前',100,100,100)
ON CONFLICT (站點名稱,更新時間) DO UPDATE 
  SET 總車輛數 = 100, 
      可借 = 100,
	  可還 = 100;

select * 
from 台北市youbike
where 站點名稱='YouBike2.0_捷運科技大樓站'


INSERT INTO 台北市youbike (站點名稱, 行政區, 更新時間, 地址, 總車輛數, 可借, 可還) 
VALUES ('YouBike2.0_一壽橋','文山區','2023-11-08 10:43:16','樟新街64號前方',0,0,0)
ON CONFLICT (站點名稱,更新時間) DO NOTHING


SELECT 站點名稱,MAX(更新時間) AS 更新時間,行政區,地址,總車輛數,可借,可還
    FROM 台北市youbike
    GROUP BY 站點名稱,行政區,地址,總車輛數,可借,可還
	
	
SELECT *
FROM 台北市youbike
WHERE (更新時間,站點名稱) IN (
	SELECT MAX(更新時間),站點名稱
	FROM 台北市youbike
	GROUP BY 站點名稱
) 

SELECT *
FROM 台北市youbike
WHERE (更新時間,站點名稱) IN (
	SELECT MAX(更新時間),站點名稱
	FROM 台北市youbike
	GROUP BY 站點名稱
) AND 站點名稱 like '%台北%'







SELECT 站點名稱,MAX(更新時間)
	FROM 台北市youbike
	GROUP BY 站點名稱



SELECT COUNT(id) as 筆數
FROM 台北市youbike
