# Starvation Mechanics

> Source: Travian: Legends Support  
> URL: https://support.travian.com/en/articles/83-starvation-mechanics

---

All troops, including the hero, consume crop from the village’s granary. If your crop production is too low or the granary empties, **troops begin to starve**. Crop management is essential to avoid losing troops unintentionally.

Buildings also consume crop through population, but buildings themselves do **not** suffer from starvation. However, low crop prevents you from starting new construction.

---

## **When Starvation Begins**

Starvation begins when:

- The **granary has no crop left**, and
- The **village produces less crop than required** to feed its troops and population.

Once starvation starts, troops die in a fixed order based on four groups.

---

## **Starvation Order: The Four Groups**

Troops starve in this order:

1. **Reinforcements from other players**
2. **Your own reinforcing troops** (troops you have stationed in other villages)
3. **Troops in their home village**
4. **Troops on the way**, **forwarded troops**, and **troops in traps**

Troops dying in battle or from starvation **add their recruitment crop cost** back into the granary.
Example:

- A Legionnaire adds **30 crop**
- A Trebuchet adds **90 crop**

This crop can temporarily feed remaining troops but usually isn’t enough to stop starvation fully.

---

## **Starvation Order Within Each Group**

Within each of the four groups, starvation follows additional rules:

### **1. Army with the Most Units Dies First**

An “army” means one row of units in the Rally Point (for example, each reinforcement row or each outgoing attack).

### **2. If Two Armies Have the Same Number of Units**

They alternate—one unit from each army starves in turns.

### **3. Inside One Army Row**

- The unit type with the **highest number** of units dies first
- If tied, units starve **from left to right** (e.g., Phalanxes before Swordsmen)

---

## **Example (from the file)**

Army A:

- 6,000 Clubs
- 3,000 Horses
- 1,000 Catapults
Total: 10,000 units

Army B:

- 1,000 Clubs
- 8,000 Horses
Total: 9,000 units
1. **Army A starves first** → 1,000 Clubs die
2. Both armies now have 9,000 units → they alternate losing units
3. Starvation continues based on the rules above

This process applies to all four starvation groups.

---

## **Oasis Starvation**

Troops in an occupied oasis are treated as if they are in the village itself:

- Reinforcements belonging to the same village starve in **Group 3** (home village troops), not Group 1.

---

## **Starvation with Evasion Active (Capital Only)**

If troop evasion is active **and the hero is set to hide**:

- Troops leave the village
- The hero stays behind and may be the **only unit left**
- The hero can **starve first** if crop is insufficient

The hero’s **6 crop production** is added to village production and does **not** protect the hero from starvation.

To avoid this:

- Disable **hero evasion** so the hero leaves with the troops
