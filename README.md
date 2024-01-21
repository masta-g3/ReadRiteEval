# ReadRiteEval

***A collection of evaluation datasets related to text understanding.***
 
![ReadRiteEval](logo.png)

```
ReadRiteEval
|--🗺️ spatial_reasoning.csv
|--😶‍🌫️ contextual_dissonance.csv
|--🧩 sequence_logic_puzzle.csv
|--💧 dependency_cascades.csv
|--🔬 hypothesis_testing.csv
```

## Dataset Descriptions

### Spatial Reasoning
Answer questions on how to get from one place to another given a description of a city layout. For example:

**Description**  
Arborville is a coastal city known for its maritime heritage. The city's heart is the Harbor Square, a bustling plaza adjacent to the main docks. Radiating from Harbor Square are three major thoroughfares: Lighthouse Lane (north), which leads to the historic Arborville Lighthouse; Dockside Drive (east), which runs parallel to the coastline; and Shipyard Street (west), which heads towards the industrial shipyards. The city is bordered by the Coastal Highway to the south, connecting to various beach resorts. Notable landmarks include the Maritime Museum at the intersection of Lighthouse Lane and Coastal Highway, and the Seafarer's Market along Dockside Drive. The city also features a canal, Canal Crossway, intersecting Lighthouse Lane and Shipyard Street, with bridges on both streets. However, the bridge on Shipyard Street is currently under maintenance, preventing any crossing at that point.  

**Question**: Find the route from Harbor Square to the Maritime Museum.  

**Answer:** WALK Lighthouse Lane -> REACH Maritime Museum.

---

### Contextual Dissonance
Identify the sentence in a paragraph that is not related to the rest. For example:

**Passage**  
The evolution of renewable energy sources has been a cornerstone in the quest for sustainable development and environmental preservation. From the early harnessing of water and wind power to the modern advancements in solar and geothermal energy, the journey has been marked by continuous innovation and technological breakthroughs. The introduction of solar panels has particularly transformed the energy landscape, allowing for the direct conversion of sunlight into electricity, thereby reducing reliance on fossil fuels and diminishing greenhouse gas emissions.

As the world's energy demands continue to rise, the importance of diversifying energy sources cannot be overstated. Wind turbines have become a common sight in many parts of the world, capitalizing on the natural movement of air to generate power. This shift towards renewable sources is not only environmentally prudent but also economically viable, as the cost of renewable technologies has been steadily decreasing. Interestingly, the growing consumer interest in organic food products has paralleled the rise in renewable energy, reflecting a broader shift towards environmental consciousness and health awareness.

The integration of renewable energy into national grids has been a complex challenge, requiring significant infrastructure changes and regulatory adjustments. However, the benefits of a renewable-based grid are immense, including increased energy security, job creation, and the mitigation of climate change impacts. Energy storage systems, such as batteries and pumped hydro storage, play a critical role in managing the intermittent nature of renewable sources like solar and wind.

Global cooperation and investment are critical to accelerating the adoption of renewable energy technologies. International initiatives, such as the Paris Agreement, have galvanized efforts to reduce carbon emissions and promote clean energy solutions. This global commitment is essential for driving innovation, fostering sustainable economic growth, and ensuring that renewable energy continues to play a pivotal role in the world's energy future.

In conclusion, the evolution of renewable energy sources is an ongoing narrative of human ingenuity and determination to create a more sustainable and resilient energy system. As we look to the future, the continued advancement of renewable technologies and their integration into our daily lives will be instrumental in shaping a cleaner, greener planet for generations to come. The exploration of renewable energy also opens up new avenues for educational programs, inspiring the next generation of scientists and engineers to innovate in the field of sustainable energy.

**Irrelevant Sentence**  
Interestingly, the growing consumer interest in organic food products has paralleled the rise in renewable energy, reflecting a broader shift towards environmental consciousness and health awareness.

---

### Sequence Logic Puzzle
Solve a logic puzzle by determining the correct order of a sequence of items. For example:

**Rules**  
In this puzzle, use the symbols 👶 (Baby), 🍼 (Baby Bottle), 🧸 (Teddy Bear), 🎈 (Balloon), 🎁 (Gift), and 🎂 (Birthday Cake).
1. 👶 cannot be directly before or after 🎁.
2. 🍼 must always precede 🧸 but follow 👶.
3. 🎈 must be immediately after 🧸.
4. The sequence must start with 👶.
5. 🎂 cannot be adjacent to either 👶 or 🍼.
6. The sequence contains exactly one of each symbol.
7. 🎁 must be the last in the sequence.

**Answer**  
👶, 🍼, 🧸, 🎈, 🎂, 🎁

---

### Dependency Cascades

**Events**  
- Coral larvae survival rates improve dramatically.
- Coral cover begins to expand as a result of successful spawning events.
- Biodiversity within the reef ecosystem flourishes, with the return of various fish and marine species.
- The Great Barrier Reef starts to show signs of significant recovery, attracting global attention and conservation efforts.
- A significant increase in water quality around the Great Barrier Reef is observed.

**Correct Order**
1. Event A: A significant increase in water quality around the Great Barrier Reef is observed.
    - "The increase in water quality is essential for any potential revival of the reef ecosystem."
2. Event B: Coral larvae survival rates improve dramatically.
    - "The improvement in water quality is a prerequisite for the higher survival rates of coral larvae."
3. Event C: Coral cover begins to expand as a result of successful spawning events.
    - "The increase in coral larvae survival rates directly leads to more successful coral spawning and growth."
4. Event D: Biodiversity within the reef ecosystem flourishes, with the return of various fish and marine species.
    - "The expansion of coral cover creates a habitat that supports a greater diversity of marine life."
5. Event E: The Great Barrier Reef starts to show signs of significant recovery, attracting global attention and conservation efforts.
    - "The flourishing biodiversity and coral cover are indicators of the reef's recovery, which then draws international focus and support."

---

### Hypothesis Testing


**Hypothesis**  
Regular exercise improves cognitive function in the elderly.

**Evidence**  
A randomized controlled trial found that elderly participants engaging in aerobic exercise had better memory recall than the control group.

**Answer**  
Supports