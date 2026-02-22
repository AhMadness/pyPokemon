# Pokemon Type Matchup Studio (Pre-Fairy)

A cute, modern Python desktop app for exploring **Pokemon type matchups** using the official **pre-Fairy (17-type)** chart.

Pick one or two types and instantly view both:
- **Offensive matchups** (what your selected type(s) hit for strong/neutral/weak/no effect damage)
- **Defensive matchups** (what hits your selected type(s) for super-effective/neutral/resisted/no effect damage)

The UI is designed to feel playful and polished with:
- Soft gradients and rounded cards
- Type-color chip boxes throughout the app
- Smooth, consistent layouts
- Filterable ranking tables for advanced analysis

## Features

- Main matchup view with fixed-size cards (no jumpy resizing)
- Offensive + defensive tabs
- `x4` indicator on type chips when applicable
- Random type pair generator
- Tables menu with:
  - Combo Rankings
  - Defensive Rankings
  - Best 3-Type Coverage
  - Best 4-Type Coverage
- Table filters (by first-column type combo) with chip-based selection
- Pagination for faster table loading

## Requirements

- Python 3.10+ (recommended)
- Tkinter (usually included with standard Python on Windows)

## Run

```bash
python main.py
```

## Notes

- Type chart is **pre-Fairy** by design.
- All type displays in matchups/tables are shown as type chips for readability.

