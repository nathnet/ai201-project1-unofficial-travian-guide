# Game Secrets ~ Combat Basics (written by kirilloid)

> Source: Unofficial Travian  
> URL: https://unofficialtravian.com/2025/01/12/game-secrets-combat-basics-written-by-kirilloid/

---

***Disclaimer:** This article is entirely the work of [Kirilloid](http://travian.kirilloid.ru/) translated by English users from old travian.com and travian.us forums. Written back in 2009, this article didn’t lose its relevance and gives one of the most advanced explanations on how battle works in Travian: Legends. We’ll publish all parts of this guide with some updates based on recent changes in the game.*

### **Combat basics**

1. **Offense and defense points: unit strength**
2. **Raid/Normal attack: standard combat**
3. **Mixed infantry/cavalry: combat with complicated defense**

#### **a. Offense and defense points**

![](../assets/3c778474c6_AllAttackerRanking.png)
In Travian, every unit has some strength in attack and defense. Its offense points are its attack skill. The more offense points a unit has, the more enemies it will kill, when used in **attack** . The same is true for defense, except there are two types: **defense against infantry** and **defense against cavalry** .

E.g. praetorians (65/35 def) are better against infantry, just as spearmen (35/60 def) are better against cavalry.

***In combat, only the offense points of attacker and defense points of defenders are taken into account.** Attacking with praetorians isn’t effective despite their high defense value. Similarly, clubswingers are worse on defense. So use your troops wisely, only for purposes they’re well-suited. Otherwise you’ll lose easily!*

Even with knowledge about units’ stats, you cannot easily predict combat result, because the combat system is neither simple nor trivial.

**Players with can find a rather good combat simulator in their rally point.** This extended version allows them taking into account almost all values affecting battle result.

**There are several free combat simulators online. One of the [most famous free warsims is mine](http://travian.kirilloid.ru/warsim2.php).** It has an almost equal set of features as the full in-game warsim plus a few: convenient hero use, traps in Gallic village, battles with Natars, some artifacts and two targets for catapults.

Also, my warsim has another useful feature: it tracks which units you have input in the URL. If you copy the URL from the address bar and send it to somebody, after opening this URL, they will go to the simulator’s page, where all troops are already set to the same values as you just done.

#### **b. Raid / normal attack**

![](../assets/06850c73f5_StartDate.png)
Here, I describe common combat without any bonuses like walls, upgrades, etc. As mentioned, **we only take offense points from attacking army and defense points from the defending army**.

First, count total offense and defense points. Total points are just amount of troops multiplied by corresponding unit stat.

**For instance, we attack with 100 imperians and 50 legionnaires.** Their attack values are 70 and 40 respectively, so total offense points will be:

**100 · 70 + 50 · 40 = 9000 (1)**

**Let the defender have 150 phalanx.** As all the attacking troops in our example are infantry, we will use only defense against infantry, 40. In this case total defense points are:

**150 · 40 = 6000 (2)**

![](../assets/ebf956de2c_Recruitement.png)
Consider first **a normal attack, combat will continue until one side is completely destroyed**. We determine the loser by comparing total offense and defense points. In our example, 9000 (1) is more than 6000 (2), so the defender will lose.

**Winner’s casualties are determined by next formula:**

**100% · (loser_points / winner_points)^1.5 (3)**

since the defender loses this battle, loser_points = 6000 and winner_points = 9000.

**100% · (6000 / 9000)^1.5 ≈ 100% · 0.5443 = 54.43%**

So 54.43% of attackers will die. This fraction is the same for all different types of troops. Since the attacker had 100 imperians and 50 legionnaires,  they lost 100 · 0.5443 = 54.43 (54 rounded) imperians and 0.5443 · 50 = 27.21 (27 rounded) legionnaires.

*Amounts are rounded for each type of troops separately, not all up or all down.*

![](../assets/199d513f9f_DefenderRanking.png)
**For raids, the formula changes a bit, losses will be:**

100% · x / (100% + x) where x is determined by formula mentioned above**(3)**.

This calculates the losses of the winner. The loser’s casulaties will be (100% – winner’s losses).

Consider another example: 100 imperians raiding 100 praetorians. Offense points (7000) are greater than defense points (6500), so the attacker wins again.

x = 100% · (6500 / 7000)^1.5 ≈ 89.479%

100% · 89.479% / 189.479% ≈ 47.22%

So 47.22% from 100 or just 47 imperians will die. Defender will lose 100% – 47.22% = 52.78% of his/her army, i.e. 53 praetorians.

**The winner’s casualties formula is actually more complicated, but only applies when large armies take part in combat.** The formula is a bit different and the winner takes more casualties.

Instead of the standard formula (3), another one is used:

**100% · (loser_points / winner_points)^K (4)**

where K depends on how much soldiers were involved in combat. Really, large, immense battles should differ from small battles between hundreds of soldiers.

К is determined by next formula:

**2 · (1.8592 – N^0.015) (5)**

where N is total amount of units taking part in battle (unit count, not their wheat upkeep).

1.2578 ≤ К ≤ 1.5: When the total number of units is one thousand or less K = 1.5, and if the total number is larger than one billion (not exact) K = 1.2578.

E.g., 2000 haeduans attacks 1400 phalanx. N = 2000 + 1400 = 3400

К = 2 · (1.8592 – 3400^0.015) = 2 · (1.8592 – 1.1297) = 2 · 0.7295 = 1.459

So the formula for losses (attacker wins obviously) will look like: 100% · (def_points / off_points)^1.459
2000 haeduans have 2000·140 = 280,000 offense points

1400 phalanx have 1400·50 = 70,000 offense points, since the attackers are cavalry troops, we will use phalanx’s defense against cavalry.

100% · (70,000 / 280,000)^1.459 = 100% · 0.25^1.459 ≈ 13.23%
2000 · 13.23% ≈ 265, i.e. 265 haeduans die.

#### **c. Simple combat with mixed infantry/cavalry**

![](../assets/485bf4645d_Metal.png)
**How do we calculate defense points if the attacker has both infantry and cavalry troops?** Offense points are calculated the same way, but determining of defense points become non-trivial. In such a case, the defense points are calculated proportional to infantry/cavalry offense ratio.

**For instance, 100 theutates thunders and 50 swordsmen are attacking 100 praetorians.**

Offense points are equal:**100 · 100 + 50 · 65 = 10000 + 3250 = 13,250**

From more then thirteen thousand offense points, cavalry part is 10000, and remainder is infantry part. We need to get proportion, so we divide:

**10000 / 13,250 ≈ 0.7547**

and do the same for infantry:

**3250 / 13250 ≈ 0.2453**

Therefore, 75.47% of offense points are cavalry offense points, and 24.53% infantry points (sum should be equal to 100%, if we are not mistaken).

Then we “apply” this infantry/cavalry proportion to defender’s troops. Praetorian has 65 def.points against infantry and 35 def against cavalry, i.e. total army’s defense is:

**100 · 65 = 6500 (infantry)**
**100 · 35 = 3500 (cavalry)**

To get real defense points we need to combine these points by proportion:

**0,7547 · 3500 + 0,2453 · 6500 = 2 641.4 + 1 594,4 ≈ 4 236**

Therefore, praetorians will have **4 236** defense points against such attacking army.

Now we got offense and defense points so could apply formulas we already know: 13250 > 4236, meaning attacker will win and defender will lose all his/her troops:

**100% · (4236 / 13250)^1.5 ≈ 18.08%**

Attacker will lose **18.08%** of all of their own troops, which works out 100 · 0,1808 = 18 theutates thunders and 50 · 0,1807 = 9 swordsmen.

And this is a wrap! Come back next Wednesday for the second part of the battle formula guide.