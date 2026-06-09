# Game Secrets ~ What is Map.sql?

> Source: Unofficial Travian  
> URL: https://unofficialtravian.com/2025/01/12/game-secrets-what-is-map-sql/  
> Written on June 29, 2023

---

#### **What is map.sql?**

SQL stands for Structured Query Language and it’s a standard language for storing, manipulating and retrieving data in databases.

Map.sql is a file provided by Travian: Legends on a daily basis and used by various external tools and tool creators. The file contains detailed information about villages on the map and is updated **always at midnight server time, every 24 hours.**

**Important note for tool-creators:** The file is generated at midnight server time, however, it’s not recommended to set data extraction exactly at midnight (00:00:00). Due to various processes, the file might become available with 5-20 seconds delay.

#### **What information does map.sql file contain?**

Each map.sql file contains information about every village on a selected gameworld and its state by the time the file was created. It doesn’t matter at which time of the day you downloaded the file – it shows parameters that were saved at midnight server time.

When you open the file you will see the list of the entries that will look something like this:

INSERT INTO `x_world` VALUES (22028,173,146,5,31912,’Natars 173|146′,1,’Natars’,0,”,498,NULL,FALSE,NULL,NULL,NULL);

If you know what each parameter means, you can easily decipher it using the table below:

| **Regular Gameworld** | | | | | | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Field ID | X | Y | Tribe | Village ID | Village name | Player ID | Player name | Alliance ID | Alliance Tag | Population | Region | Capital | City | Harbor | Victory points |
| 22028 | 173 | 146 | 5 | 31912 | Natars 173|146 | 1 | Natars | 0 |  | 498 | NULL | FALSE | NULL | NULL | NULL |
| **Annual Special (random example)** | | | | | | | | | | | | | | | |
| Field ID | X | Y | Tribe | Village ID | Village name | Player ID | Player name | Alliance ID | Alliance Tag | Population | Region | Capital | City | Harbor | Victory points |
| 36772 | 80 | 109 | 2 | 9260 | LilaS | 1744 | ashko | 2 | UU # | 948 | Venedae | TRUE | FALSE | FALSE | 162 |

**Important note:** In the past the file was slightly different for Annual Special gameworlds compared to regular ones, as it included data about cities, capitals and Victory Points. By now it had been unified so that all files will have all data. However, in case the gameworld doesn’t support a specific feature, the data will be set to **NULL**. That’s why on a regular gameworld map.sql will contain **NULL** in the place for the region, city, harbor and Victory Points. This was done for the conveniency of the tool creators.

**TRUE** and **FALSE** are used to define the status of the village (for example, whether a certain village is a capital or not)

**The tribes in map.sql file are shown as a digit.**

- 1 – Romans
- 2 – Teutons
- 3 – Gauls
- 4 – Nature (this tribe is not shown in map.sql)
- 5 –  Natars
- 6 – Egyptians
- 7 – Huns
- 8 – Spartans
- 9 – Vikings

#### **How can I get map.sql file from a certain gameworld?**

To get map.sql file you just need to add map.sql after your gameworld name as in an example:

| Gameworld link | https://ts5.x1.europe.travian.com/ |
| --- | --- |
| Map.sql link | https://ts5.x1.europe.travian.com/map.sql |

The downloading starts automatically. You do not need to be a part of the gameworld to download map.sql file for it.

#### **What for and how can I use this data?**

Map.sql data can be used various ways. Alliance off-coordinators often use this file to plan operations, regular players and game analitics do that to monitor gameworld/players activity and such. If you’re new to programming, consider opening the file using a notepad (.txt format) and pasting it to excel or a similar tool with the comma as a column separator. That way you can use tool filters to search for the data you need.

And that is a wrap! Stay tuned and come back to [**Thursday guides**](https://blog.travian.com/tag/thursday-guides/) to find out another secret about the game!