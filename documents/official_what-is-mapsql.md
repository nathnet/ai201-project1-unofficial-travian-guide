# What is Map.sql

> Source: Travian: Legends Support  
> URL: https://support.travian.com/en/articles/156-what-is-mapsql

---

### **map.sql** is a file provided daily by Travian: Legends. It contains detailed information about all villages on a game world map.

The file is updated **every 24 hours at midnight (server time)** and is commonly used by external tools and tool creators.

Important:

- The data always reflects the state of the game world **at midnight**, regardless of when you download the file.
- The file may become available **5–20 seconds after midnight**, so avoid requesting it exactly at 00:00:00.

---

### What information the file contains

Each map.sql file includes a full snapshot of all villages on a game world.

A typical entry looks like this:

```
INSERT INTO `x_world` VALUES (22028,173,146,5,31912,'Natars 173|146',1,'Natars',0,"",498,NULL,FALSE,NULL,NULL,NULL);
```
Each value represents specific data about a village.

---

### How to read the data

Each row contains the following fields:

- ID
- Coordinates (X, Y)
- Tribe
- Village ID
- Village name
- Player ID
- Player name
- Alliance ID
- Alliance tag
- Population
- Region
- Capital (TRUE/FALSE)
- City (TRUE/FALSE)
- Harbor (TRUE/FALSE)
- Victory Points

Notes:

- If a feature is not supported on a game world, the value will be **NULL**.
→ For example, regular game worlds may show NULL for region, city, harbor, or Victory Points.
- TRUE/FALSE values indicate statuses such as whether a village is a **capital**.

---

### Tribe values in map.sql

Tribes are represented as numbers:

- 1 – Romans
- 2 – Teutons
- 3 – Gauls
- 4 – Nature (not shown in map.sql)
- 5 – Natars
- 6 – Egyptians
- 7 – Huns
- 8 – Spartans
- 9 – Vikings

---

### How to download map.sql

To download the file, add **/map.sql** to your game world URL.

Example:

- Game world:
`https://ts5.x1.europe.travian.com/`
- map.sql file:
`https://ts5.x1.europe.travian.com/map.sql`

The download starts automatically.

You do **not** need to be registered on that game world to download the file.

---

### How you can use the data

map.sql can be used in several ways:

- Planning operations (e.g. alliance coordination)
- Monitoring player or game world activity
- General data analysis

If you are not familiar with programming:

- Open the file in a text editor (.txt)
- Copy the content into Excel or a similar tool
- Use **comma-separated columns** to filter and search for specific data

---

### Key takeaway

map.sql provides a **daily snapshot of the entire game world**, which you can use to:

- Analyze villages and players
- Support coordination and planning
- Extract specific data using external tools or spreadsheets

Make sure you understand the structure of the data before using it, especially the meaning of each field.
