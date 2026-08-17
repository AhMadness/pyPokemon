# Pokemon Type Matchup Studio

A Python and Tkinter desktop application for exploring modern 18-type matchup logic, dual-type defense, and multi-type offensive coverage.

## Features

- Compare offensive and defensive matchups for one or two selected types
- Identify 4x weaknesses, resistances, and immunities
- Rank single- and dual-type combinations by coverage and defensive profile
- Analyze the best three- and four-type offensive combinations
- Filter and paginate larger ranking tables

## Screenshots

![Main matchup view](https://github.com/user-attachments/assets/c3463940-ea48-4380-b05c-a18fb290eb90)
![Defensive matchup view](https://github.com/user-attachments/assets/7c2c80f2-d85d-4e2c-8cbc-3d9dec3c7435)
![Coverage ranking table](https://github.com/user-attachments/assets/0a83a30a-d173-4e5b-a952-63481233a4c8)
![Defensive ranking table](https://github.com/user-attachments/assets/3c989b2c-03fe-4658-8def-e59ac2368fb5)
![Filtered table view](https://github.com/user-attachments/assets/c25bacb7-660f-409e-abb4-3fc2feb1fe3f)

## Run Locally

Requirements: Python 3.10+ with Tkinter.

```bash
python main.py
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Build for Windows

Install PyInstaller and build from the included specification:

```bash
python -m pip install pyinstaller
pyinstaller pyPokemon.spec
```

## License

The application code is available under the [MIT License](LICENSE).

Pokemon and related names are trademarks of their respective owners. This is an independent fan-made utility and is not affiliated with or endorsed by Nintendo, Game Freak, or The Pokemon Company.
