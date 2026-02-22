import random
import tkinter as tk
from itertools import combinations
from tkinter import ttk

TYPES = [
    "Normal",
    "Fire",
    "Water",
    "Electric",
    "Grass",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
]

TYPE_COLORS = {
    "Normal": "#A8A878",
    "Fire": "#F08030",
    "Water": "#6890F0",
    "Electric": "#F8D030",
    "Grass": "#78C850",
    "Ice": "#98D8D8",
    "Fighting": "#C03028",
    "Poison": "#A040A0",
    "Ground": "#E0C068",
    "Flying": "#A890F0",
    "Psychic": "#F85888",
    "Bug": "#A8B820",
    "Rock": "#B8A038",
    "Ghost": "#705898",
    "Dragon": "#7038F8",
    "Dark": "#705848",
    "Steel": "#B8B8D0",
}

CHIP_WIDTH = 12
CHIP_FONT = ("Segoe UI Semibold", 9)
COMBO_INITIAL_ROWS = 30
COMBO_LOAD_STEP = 10
COMBO_MAX_ROWS = 57
THREE_INITIAL_ROWS = 30
THREE_LOAD_STEP = 10
THREE_MAX_ROWS = 58
FOUR_INITIAL_ROWS = 30
FOUR_LOAD_STEP = 10
FOUR_MAX_ROWS = 142
DEF_INITIAL_ROWS = 30
DEF_LOAD_STEP = 10
DEF_MAX_ROWS = 70

# Official type effectiveness for generations before Fairy existed.
# Only non-neutral matchups are listed; all omitted pairs are neutral (1x).
TYPE_CHART = {
    "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2.0,
        "Ice": 2.0,
        "Bug": 2.0,
        "Rock": 0.5,
        "Dragon": 0.5,
        "Steel": 2.0,
    },
    "Water": {
        "Fire": 2.0,
        "Water": 0.5,
        "Grass": 0.5,
        "Ground": 2.0,
        "Rock": 2.0,
        "Dragon": 0.5,
    },
    "Electric": {
        "Water": 2.0,
        "Electric": 0.5,
        "Grass": 0.5,
        "Ground": 0.0,
        "Flying": 2.0,
        "Dragon": 0.5,
    },
    "Grass": {
        "Fire": 0.5,
        "Water": 2.0,
        "Grass": 0.5,
        "Poison": 0.5,
        "Ground": 2.0,
        "Flying": 0.5,
        "Bug": 0.5,
        "Rock": 2.0,
        "Dragon": 0.5,
        "Steel": 0.5,
    },
    "Ice": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2.0,
        "Ground": 2.0,
        "Flying": 2.0,
        "Dragon": 2.0,
        "Ice": 0.5,
        "Steel": 0.5,
    },
    "Fighting": {
        "Normal": 2.0,
        "Ice": 2.0,
        "Poison": 0.5,
        "Flying": 0.5,
        "Psychic": 0.5,
        "Bug": 0.5,
        "Rock": 2.0,
        "Ghost": 0.0,
        "Dark": 2.0,
        "Steel": 2.0,
    },
    "Poison": {
        "Grass": 2.0,
        "Poison": 0.5,
        "Ground": 0.5,
        "Rock": 0.5,
        "Ghost": 0.5,
        "Steel": 0.0,
    },
    "Ground": {
        "Fire": 2.0,
        "Electric": 2.0,
        "Grass": 0.5,
        "Poison": 2.0,
        "Flying": 0.0,
        "Bug": 0.5,
        "Rock": 2.0,
        "Steel": 2.0,
    },
    "Flying": {
        "Electric": 0.5,
        "Grass": 2.0,
        "Fighting": 2.0,
        "Bug": 2.0,
        "Rock": 0.5,
        "Steel": 0.5,
    },
    "Psychic": {
        "Fighting": 2.0,
        "Poison": 2.0,
        "Psychic": 0.5,
        "Dark": 0.0,
        "Steel": 0.5,
    },
    "Bug": {
        "Fire": 0.5,
        "Grass": 2.0,
        "Fighting": 0.5,
        "Poison": 0.5,
        "Flying": 0.5,
        "Psychic": 2.0,
        "Ghost": 0.5,
        "Dark": 2.0,
        "Steel": 0.5,
    },
    "Rock": {
        "Fire": 2.0,
        "Ice": 2.0,
        "Fighting": 0.5,
        "Ground": 0.5,
        "Flying": 2.0,
        "Bug": 2.0,
        "Steel": 0.5,
    },
    "Ghost": {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Steel": 0.5},
    "Dragon": {"Dragon": 2.0, "Steel": 0.5},
    "Dark": {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Steel": 0.5},
    "Steel": {
        "Fire": 0.5,
        "Water": 0.5,
        "Electric": 0.5,
        "Ice": 2.0,
        "Rock": 2.0,
        "Steel": 0.5,
    },
}


def get_type_multiplier(attacker: str, defender: str) -> float:
    return TYPE_CHART.get(attacker, {}).get(defender, 1.0)


def normalize_selected_types(selected_types: list[str]) -> list[str]:
    active: list[str] = []
    for type_name in selected_types:
        if type_name in TYPES and type_name not in active:
            active.append(type_name)
    return active


def calculate_best_coverage(selected_types: list[str]) -> dict[str, float]:
    active = normalize_selected_types(selected_types)
    if not active:
        return {type_name: 1.0 for type_name in TYPES}

    coverage: dict[str, float] = {}
    for defender in TYPES:
        coverage[defender] = max(get_type_multiplier(attacker, defender) for attacker in active)
    return coverage


def calculate_defensive_profile(selected_types: list[str]) -> dict[str, float]:
    defender_types = normalize_selected_types(selected_types)
    if not defender_types:
        return {type_name: 1.0 for type_name in TYPES}

    profile: dict[str, float] = {}
    for attacker in TYPES:
        multiplier = 1.0
        for defender in defender_types:
            multiplier *= get_type_multiplier(attacker, defender)
        profile[attacker] = multiplier
    return profile


def bucketize_matchups(multiplier_map: dict[str, float]) -> dict[str, list[str]]:
    buckets = {"super": [], "neutral": [], "weak": [], "immune": []}
    for type_name in TYPES:
        multiplier = multiplier_map[type_name]
        if multiplier == 0.0:
            buckets["immune"].append(type_name)
        elif multiplier > 1.0:
            buckets["super"].append(type_name)
        elif multiplier < 1.0:
            buckets["weak"].append(type_name)
        else:
            buckets["neutral"].append(type_name)
    return buckets


def build_combo_rankings() -> list[
    tuple[list[str], int, int, list[str], list[str], dict[str, float], dict[str, float]]
]:
    combos: list[list[str]] = [[type_name] for type_name in TYPES]
    for index, first_type in enumerate(TYPES):
        for second_type in TYPES[index + 1 :]:
            combos.append([first_type, second_type])

    rankings: list[
        tuple[list[str], int, int, list[str], list[str], dict[str, float], dict[str, float]]
    ] = []
    for combo in combos:
        offense_map = calculate_best_coverage(combo)
        defense_map = calculate_defensive_profile(combo)
        offense_super = [type_name for type_name in TYPES if offense_map[type_name] > 1.0]
        defense_super = [type_name for type_name in TYPES if defense_map[type_name] > 1.0]
        offense_super_map = {type_name: offense_map[type_name] for type_name in offense_super}
        defense_super_map = {type_name: defense_map[type_name] for type_name in defense_super}

        rankings.append(
            (
                combo,
                len(offense_super),
                len(defense_super),
                offense_super,
                defense_super,
                offense_super_map,
                defense_super_map,
            )
        )

    rankings.sort(key=lambda row: (-row[1], row[2], row[0]))
    return rankings


def build_four_type_rankings() -> list[tuple[list[str], int, list[str]]]:
    rankings: list[tuple[list[str], int, list[str]]] = []
    for combo in combinations(TYPES, 4):
        coverage_map = calculate_best_coverage(list(combo))
        covered_types = [type_name for type_name in TYPES if coverage_map[type_name] > 1.0]
        rankings.append((list(combo), len(covered_types), covered_types))

    rankings.sort(key=lambda row: (-row[1], row[0]))
    return rankings


def build_three_type_rankings() -> list[tuple[list[str], int, list[str]]]:
    rankings: list[tuple[list[str], int, list[str]]] = []
    for combo in combinations(TYPES, 3):
        coverage_map = calculate_best_coverage(list(combo))
        covered_types = [type_name for type_name in TYPES if coverage_map[type_name] > 1.0]
        rankings.append((list(combo), len(covered_types), covered_types))

    rankings.sort(key=lambda row: (-row[1], row[0]))
    return rankings


def build_defensive_table_rankings() -> list[
    tuple[list[str], list[str], list[str], list[str], list[str], dict[str, float]]
]:
    combos: list[list[str]] = [[type_name] for type_name in TYPES]
    for index, first_type in enumerate(TYPES):
        for second_type in TYPES[index + 1 :]:
            combos.append([first_type, second_type])

    rankings: list[
        tuple[list[str], list[str], list[str], list[str], list[str], dict[str, float]]
    ] = []
    for combo in combos:
        defense_map = calculate_defensive_profile(combo)
        immune: list[str] = []
        resisted: list[str] = []
        neutral: list[str] = []
        super_effective: list[str] = []

        for attacker in TYPES:
            multiplier = defense_map[attacker]
            if multiplier == 0.0:
                immune.append(attacker)
            elif multiplier < 1.0:
                resisted.append(attacker)
            elif multiplier > 1.0:
                super_effective.append(attacker)
            else:
                neutral.append(attacker)

        rankings.append((combo, immune, resisted, neutral, super_effective, defense_map))

    rankings.sort(key=lambda row: (-len(row[2]), -len(row[1]), len(row[4]), row[0]))
    return rankings


def get_readable_fg(hex_color: str) -> str:
    color = hex_color.lstrip("#")
    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    brightness = (red * 299 + green * 587 + blue * 114) / 1000
    return "#232323" if brightness > 165 else "#FFFFFF"


def make_chip_label(
    parent: tk.Widget,
    text: str,
    bg: str,
    fg: str,
) -> tk.Label:
    return tk.Label(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        font=CHIP_FONT,
        width=CHIP_WIDTH,
        height=1,
        padx=0,
        pady=5,
        borderwidth=0,
        anchor="center",
        justify="center",
    )


class MatchupCard(tk.Frame):
    def __init__(self, parent: tk.Widget, title: str, subtitle: str, background: str) -> None:
        super().__init__(
            parent,
            bg=background,
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground="#E8D8B6",
        )
        self.base_title = title
        self.default_border = "#E8D8B6"
        self.hover_border = "#E3A63C"
        self.columns = 5

        self.title_label = tk.Label(
            self,
            text=title,
            bg=background,
            fg="#2D2D2D",
            font=("Segoe UI Semibold", 14),
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self,
            text=subtitle,
            bg=background,
            fg="#645945",
            font=("Segoe UI", 10),
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 10))

        # Keep a fixed chip area height so card size stays stable across updates.
        self.chip_area = tk.Frame(self, bg=background, height=154)
        self.chip_area.pack(fill="x", expand=False)
        self.chip_area.pack_propagate(False)

        self._bind_hover(self)

    def _bind_hover(self, widget: tk.Widget) -> None:
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        for child in widget.winfo_children():
            self._bind_hover(child)

    def _on_enter(self, _event: tk.Event) -> None:
        self.configure(highlightbackground=self.hover_border)

    def _on_leave(self, _event: tk.Event) -> None:
        self.configure(highlightbackground=self.default_border)

    def set_types(self, type_names: list[str], multiplier_map: dict[str, float] | None = None) -> None:
        for child in self.chip_area.winfo_children():
            child.destroy()

        self.title_label.configure(text=f"{self.base_title} ({len(type_names)})")

        if not type_names:
            empty = make_chip_label(
                self.chip_area,
                text="None",
                bg="#EDE3CF",
                fg="#6D665B",
            )
            empty.grid(row=0, column=0, padx=4, pady=4, sticky="w")
            return

        for index, type_name in enumerate(type_names):
            row, column = divmod(index, self.columns)
            color = TYPE_COLORS[type_name]
            multiplier = 1.0 if multiplier_map is None else multiplier_map.get(type_name, 1.0)
            chip_text = f"{type_name} x4" if multiplier >= 3.99 else type_name
            chip = make_chip_label(
                self.chip_area,
                text=chip_text,
                bg=color,
                fg=get_readable_fg(color),
            )
            chip.grid(row=row, column=column, padx=4, pady=4, sticky="w")


class PokemonTypeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Pokemon Type Matchup Studio (Pre-Fairy)")
        self.geometry("1200x760")
        self.minsize(960, 660)

        self.primary_type = tk.StringVar(value="Fire")
        self.secondary_type = tk.StringVar(value="None")
        self.bubbles: list[dict[str, float | int]] = []
        self.combo_rankings = build_combo_rankings()[:COMBO_MAX_ROWS]
        self.defensive_table_rankings = build_defensive_table_rankings()[:DEF_MAX_ROWS]
        self.three_type_rankings = build_three_type_rankings()[:THREE_MAX_ROWS]
        self.four_type_rankings = build_four_type_rankings()[:FOUR_MAX_ROWS]
        self.combo_visible_rows = self.combo_rankings
        self.defensive_visible_rows = self.defensive_table_rankings
        self.three_visible_rows = self.three_type_rankings
        self.four_visible_rows = self.four_type_rankings
        self.combo_filter_types: set[str] = set()
        self.defensive_filter_types: set[str] = set()
        self.three_filter_types: set[str] = set()
        self.four_filter_types: set[str] = set()
        self.ranking_window: tk.Toplevel | None = None
        self.defensive_table_window: tk.Toplevel | None = None
        self.three_type_window: tk.Toplevel | None = None
        self.four_type_window: tk.Toplevel | None = None
        self.combo_rows_host: tk.Frame | None = None
        self.combo_progress_label: tk.Label | None = None
        self.combo_load_button: tk.Button | None = None
        self.combo_filter_button: tk.Button | None = None
        self.combo_rows_rendered = 0
        self.def_table_rows_host: tk.Frame | None = None
        self.def_table_progress_label: tk.Label | None = None
        self.def_table_load_button: tk.Button | None = None
        self.def_table_filter_button: tk.Button | None = None
        self.def_table_rows_rendered = 0
        self.three_rows_host: tk.Frame | None = None
        self.three_progress_label: tk.Label | None = None
        self.three_load_button: tk.Button | None = None
        self.three_filter_button: tk.Button | None = None
        self.three_rows_rendered = 0
        self.four_rows_host: tk.Frame | None = None
        self.four_progress_label: tk.Label | None = None
        self.four_load_button: tk.Button | None = None
        self.four_filter_button: tk.Button | None = None
        self.four_rows_rendered = 0
        self.primary_selector_button: tk.Button | None = None
        self.secondary_selector_button: tk.Button | None = None
        self.active_filter_popup: tk.Toplevel | None = None
        self.active_filter_anchor: tk.Widget | None = None
        self.active_selector_popup: tk.Toplevel | None = None
        self.active_selector_anchor: tk.Widget | None = None

        self._configure_styles()
        self._build_background()
        self._build_interface()
        self.update_matchups()

        self.after(20, lambda: self._maximize_window(self))
        self.after(200, self._animate_bubbles)

    def _maximize_window(self, window: tk.Tk | tk.Toplevel) -> None:
        try:
            window.state("zoomed")
        except tk.TclError:
            try:
                window.attributes("-zoomed", True)
            except tk.TclError:
                pass

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Poke.TCombobox",
            foreground="#2E2A25",
            fieldbackground="#FFFDF8",
            background="#FFC75A",
            bordercolor="#E4B75A",
            darkcolor="#E4B75A",
            lightcolor="#E4B75A",
            arrowsize=16,
            padding=7,
            relief="flat",
        )
        style.map(
            "Poke.TCombobox",
            fieldbackground=[("readonly", "#FFFDF8")],
            foreground=[("readonly", "#2E2A25")],
            background=[("active", "#FFD97E"), ("readonly", "#FFC75A")],
        )
        style.configure("Poke.TNotebook", background="#FFF7E8", borderwidth=0)
        style.configure(
            "Poke.TNotebook.Tab",
            background="#EFDDB2",
            foreground="#5A472D",
            padding=(16, 8),
            font=("Segoe UI Semibold", 10),
            borderwidth=0,
        )
        style.map(
            "Poke.TNotebook.Tab",
            background=[("selected", "#FFE7A8"), ("active", "#F6E5BD")],
            foreground=[("selected", "#2E2415")],
        )
        style.configure(
            "Poke.Treeview",
            background="#FFFDF8",
            fieldbackground="#FFFDF8",
            foreground="#2E2A25",
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Poke.Treeview.Heading",
            background="#FFE4A6",
            foreground="#3A2E1B",
            font=("Segoe UI Semibold", 10),
            relief="flat",
        )
        style.map(
            "Poke.Treeview",
            background=[("selected", "#E8F2FF")],
            foreground=[("selected", "#1A2433")],
        )

    def _build_background(self) -> None:
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)
        self.panel_window = None
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _build_interface(self) -> None:
        self.panel = tk.Frame(
            self.canvas,
            bg="#FFF7E8",
            padx=26,
            pady=22,
            highlightthickness=1,
            highlightbackground="#F3D9A3",
        )
        self.panel_window = self.canvas.create_window(0, 0, window=self.panel, anchor="center")

        heading = tk.Frame(self.panel, bg=self.panel["bg"])
        heading.pack(fill="x", pady=(0, 14))
        heading.grid_columnconfigure(0, weight=1)

        title_block = tk.Frame(heading, bg=heading["bg"])
        title_block.grid(row=0, column=0, sticky="w")

        tk.Label(
            title_block,
            text="Pokemon Type Matchup Studio",
            bg=self.panel["bg"],
            fg="#2B2B2B",
            font=("Segoe UI Semibold", 28),
        ).pack(anchor="w")

        tk.Label(
            title_block,
            text="Build one or two-type offense + defense profiles and view matchups instantly.",
            bg=self.panel["bg"],
            fg="#5B5244",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(4, 0))

        header_actions = tk.Frame(heading, bg=heading["bg"])
        header_actions.grid(row=0, column=1, sticky="ne", padx=(18, 0))

        selectors = tk.Frame(
            self.panel,
            bg="#FFF1CF",
            padx=14,
            pady=12,
            highlightthickness=1,
            highlightbackground="#EEC46E",
        )
        selectors.pack(fill="x", pady=(0, 14))

        tk.Label(
            selectors,
            text="Primary Type",
            bg=selectors["bg"],
            fg="#3A3227",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.primary_selector_button = tk.Button(
            selectors,
            text="",
            command=lambda: self._open_type_selector_popup(
                self,
                self.primary_selector_button,
                self.primary_type,
                TYPES,
            ),
            font=("Segoe UI Semibold", 10),
            width=16,
            padx=10,
            pady=6,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            anchor="center",
        )
        self.primary_selector_button.grid(row=0, column=1, sticky="ew", padx=(0, 16))

        tk.Label(
            selectors,
            text="Secondary Type",
            bg=selectors["bg"],
            fg="#3A3227",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=2, sticky="w", padx=(0, 8))

        self.secondary_selector_button = tk.Button(
            selectors,
            text="",
            command=lambda: self._open_type_selector_popup(
                self,
                self.secondary_selector_button,
                self.secondary_type,
                ["None"] + TYPES,
            ),
            font=("Segoe UI Semibold", 10),
            width=16,
            padx=10,
            pady=6,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            anchor="center",
        )
        self.secondary_selector_button.grid(row=0, column=3, sticky="ew", padx=(0, 12))

        random_button = tk.Button(
            selectors,
            text="Random Pair",
            command=self.pick_random_types,
            bg="#4B8CF6",
            fg="#FFFFFF",
            activebackground="#6A9BF0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
            padx=12,
            pady=6,
            cursor="hand2",
        )
        random_button.grid(row=0, column=4, sticky="e")

        tables_button = tk.Menubutton(
            header_actions,
            text="Tables >",
            bg="#2C9F89",
            fg="#FFFFFF",
            activebackground="#3FB6A0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
            padx=14,
            pady=7,
            cursor="hand2",
            indicatoron=False,
            direction="below",
        )
        tables_button.pack(anchor="e")

        tables_menu = tk.Menu(
            tables_button,
            tearoff=0,
            bg="#FFF7E8",
            fg="#2E2A25",
            activebackground="#E5F4EE",
            activeforeground="#1F3B33",
            relief="flat",
            borderwidth=1,
        )
        tables_menu.add_command(label="Combo Rankings", command=self.open_combo_rankings)
        tables_menu.add_command(label="Defensive Rankings", command=self.open_defensive_table_rankings)
        tables_menu.add_command(label="Best 3-Type Coverage", command=self.open_three_type_rankings)
        tables_menu.add_command(label="Best 4-Type Coverage", command=self.open_four_type_rankings)
        tables_button.configure(menu=tables_menu)

        for column in (1, 3):
            selectors.grid_columnconfigure(column, weight=1)

        self.mode_label = tk.Label(
            selectors,
            text="Offense shows best coverage. Defense shows incoming damage against your selected type(s).",
            bg=selectors["bg"],
            fg="#64553E",
            font=("Segoe UI", 9),
        )
        self.mode_label.grid(row=1, column=0, columnspan=5, sticky="w", pady=(9, 0))

        self.selected_types_label = tk.Label(
            selectors,
            text="Selected Types",
            bg=selectors["bg"],
            fg="#3A3227",
            font=("Segoe UI Semibold", 9),
        )
        self.selected_types_label.grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.selected_types_area = tk.Frame(selectors, bg=selectors["bg"])
        self.selected_types_area.grid(row=2, column=1, columnspan=4, sticky="w", pady=(8, 0))

        self.results_tabs = ttk.Notebook(self.panel, style="Poke.TNotebook")
        self.results_tabs.pack(fill="both", expand=True)

        self.offense_tab = tk.Frame(self.results_tabs, bg=self.panel["bg"], padx=4, pady=8)
        self.defense_tab = tk.Frame(self.results_tabs, bg=self.panel["bg"], padx=4, pady=8)
        self.results_tabs.add(self.offense_tab, text="Offensive Matchups")
        self.results_tabs.add(self.defense_tab, text="Defensive Matchups")

        self.offense_cards = self._build_cards(
            self.offense_tab,
            {
                "super": (
                    "Super Effective",
                    "Targets you hit for boosted damage (2x).",
                    "#FFF8EE",
                ),
                "neutral": (
                    "Neutral",
                    "Targets you hit for standard damage (1x).",
                    "#F8F7FF",
                ),
                "weak": (
                    "Weak Against",
                    "Targets that resist your selected attack types (<1x).",
                    "#FFF2F2",
                ),
                "immune": (
                    "Immunities",
                    "Targets fully immune to your selected attack types (0x).",
                    "#F2FBFF",
                ),
            },
        )
        self.defense_cards = self._build_cards(
            self.defense_tab,
            {
                "super": (
                    "Super Effective Vs You",
                    "Attack types that hit your selected typing for >1x.",
                    "#FFF8EE",
                ),
                "neutral": (
                    "Neutral Vs You",
                    "Attack types that hit your selected typing for 1x.",
                    "#F8F7FF",
                ),
                "weak": (
                    "Weak Vs You",
                    "Attack types your selected typing resists (<1x).",
                    "#FFF2F2",
                ),
                "immune": (
                    "No Effect Vs You",
                    "Attack types that deal no damage to your selected typing.",
                    "#F2FBFF",
                ),
            },
        )

    def _build_cards(
        self,
        parent: tk.Widget,
        config: dict[str, tuple[str, str, str]],
    ) -> dict[str, MatchupCard]:
        card_grid = tk.Frame(parent, bg=self.panel["bg"])
        card_grid.pack(fill="both", expand=True)

        for row in (0, 1):
            card_grid.grid_rowconfigure(row, weight=1, uniform="cardrow", minsize=224)
        for column in (0, 1):
            card_grid.grid_columnconfigure(column, weight=1, uniform="cardcol")

        cards = {
            key: MatchupCard(card_grid, title=title, subtitle=subtitle, background=background)
            for key, (title, subtitle, background) in config.items()
        }
        cards["super"].grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        cards["neutral"].grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))
        cards["weak"].grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(10, 0))
        cards["immune"].grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0))
        return cards

    def _on_selection_changed(self, _event: tk.Event) -> None:
        self.update_matchups()

    def _get_selected_types(self) -> list[str]:
        return normalize_selected_types([self.primary_type.get(), self.secondary_type.get()])

    def _style_selector_button(self, button: tk.Button | None, value: str) -> None:
        if button is None:
            return

        if value == "None":
            bg = "#EDE3CF"
            fg = "#5A5245"
            active_bg = "#E5D8BD"
        else:
            bg = TYPE_COLORS.get(value, "#EDE3CF")
            fg = get_readable_fg(bg)
            active_bg = bg

        button.configure(
            text=f"{value}  [Pick]",
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            highlightthickness=2,
            highlightbackground="#E3C47C",
            highlightcolor="#E3C47C",
        )

    def _open_type_selector_popup(
        self,
        owner_window: tk.Tk | tk.Toplevel,
        anchor_widget: tk.Widget | None,
        target_var: tk.StringVar,
        options: list[str],
    ) -> None:
        if anchor_widget is None or not anchor_widget.winfo_exists():
            return

        # Toggle behavior: clicking the same selector closes its popup.
        if self.active_selector_popup is not None and self.active_selector_popup.winfo_exists():
            if self.active_selector_anchor == anchor_widget:
                self.active_selector_popup.destroy()
                return
            self.active_selector_popup.destroy()

        popup = tk.Toplevel(owner_window)
        popup.title("Pick Type")
        popup.transient(owner_window)
        popup.resizable(False, False)
        popup.configure(bg="#FFF7E8")
        self.active_selector_popup = popup
        self.active_selector_anchor = anchor_widget

        def clear_active_popup(_event: tk.Event | None = None) -> None:
            if self.active_selector_popup == popup:
                self.active_selector_popup = None
                self.active_selector_anchor = None

        popup.bind("<Destroy>", clear_active_popup)
        popup.bind("<Escape>", lambda _event: popup.destroy())

        host = tk.Frame(
            popup,
            bg="#FFF7E8",
            padx=12,
            pady=10,
            highlightthickness=1,
            highlightbackground="#E6D4AE",
        )
        host.pack(fill="both", expand=True)

        tk.Label(
            host,
            text="Choose a type:",
            bg=host["bg"],
            fg="#4F4536",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 8))

        chips = tk.Frame(host, bg=host["bg"])
        chips.pack(fill="x")

        selected_outline = "#2D7DFF"
        current_value = target_var.get()

        def pick_value(type_name: str) -> None:
            target_var.set(type_name)
            self.update_matchups()
            popup.destroy()

        for index, type_name in enumerate(options):
            row, column = divmod(index, 4)
            color = "#EDE3CF" if type_name == "None" else TYPE_COLORS[type_name]
            fg = "#5A5245" if type_name == "None" else get_readable_fg(color)
            is_selected = type_name == current_value

            chip_frame = tk.Frame(
                chips,
                bg=selected_outline if is_selected else host["bg"],
                padx=2,
                pady=2,
                bd=0,
            )
            chip_frame.grid(row=row, column=column, sticky="w", padx=4, pady=4)

            chip = tk.Button(
                chip_frame,
                text=type_name,
                command=lambda current=type_name: pick_value(current),
                bg=color,
                fg=fg,
                activebackground=color,
                activeforeground=fg,
                font=("Segoe UI Semibold", 9),
                width=CHIP_WIDTH,
                padx=0,
                pady=5,
                borderwidth=0,
                highlightthickness=0,
                cursor="hand2",
            )
            chip.pack()

        controls = tk.Frame(host, bg=host["bg"])
        controls.pack(fill="x", pady=(10, 0))

        tk.Button(
            controls,
            text="Cancel",
            command=popup.destroy,
            bg="#ECE2CA",
            fg="#3C3329",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        ).pack(side="right")

        popup.update_idletasks()
        popup_x = anchor_widget.winfo_rootx()
        popup_y = anchor_widget.winfo_rooty() + anchor_widget.winfo_height() + 6
        popup.geometry(f"+{popup_x}+{popup_y}")

    def pick_random_types(self) -> None:
        primary = random.choice(TYPES)
        secondary = random.choice(["None"] + TYPES)
        if secondary == primary:
            secondary = "None"
        self.primary_type.set(primary)
        self.secondary_type.set(secondary)
        self.update_matchups()

    def update_matchups(self) -> None:
        active = self._get_selected_types()
        self._style_selector_button(self.primary_selector_button, self.primary_type.get())
        self._style_selector_button(self.secondary_selector_button, self.secondary_type.get())

        offense_map = calculate_best_coverage(active)
        defense_map = calculate_defensive_profile(active)
        offense_buckets = bucketize_matchups(offense_map)
        defense_buckets = bucketize_matchups(defense_map)

        for key, value in offense_buckets.items():
            self.offense_cards[key].set_types(value, offense_map)
        for key, value in defense_buckets.items():
            self.defense_cards[key].set_types(value, defense_map)

        for child in self.selected_types_area.winfo_children():
            child.destroy()
        self._create_type_chip_grid(
            self.selected_types_area,
            active,
            base_bg=self.selected_types_area["bg"],
            columns=2,
        )

        self.mode_label.configure(
            text="Offense uses best multiplier per target type. Defense shows incoming damage profile."
        )

    def open_combo_rankings(self) -> None:
        if self.ranking_window is not None and self.ranking_window.winfo_exists():
            self.ranking_window.lift()
            self.ranking_window.focus_force()
            return

        self.ranking_window = tk.Toplevel(self)
        self.ranking_window.title("Type Combo Rankings (Pre-Fairy)")
        self.ranking_window.geometry("1220x680")
        self.ranking_window.minsize(980, 540)
        self.ranking_window.configure(bg="#FFF7E8")
        self.ranking_window.protocol("WM_DELETE_WINDOW", self._close_rankings_window)

        header = tk.Frame(
            self.ranking_window,
            bg="#FFF1CF",
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground="#EEC46E",
        )
        header.pack(fill="x", padx=14, pady=(14, 10))

        tk.Label(
            header,
            text="All Type Combo Rankings",
            bg=header["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 17),
        ).pack(anchor="w")
        tk.Label(
            header,
            text=(
                "Sorted by highest offensive super-effective coverage first. "
                "Combo label shows counts as Strong (offense) and Weak (defense). "
                "Showing top 57 entries (down to SE=6)."
            ),
            bg=header["bg"],
            fg="#5B4E3A",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        table_wrap = tk.Frame(
            self.ranking_window,
            bg="#FFF7E8",
            padx=14,
            pady=4,
        )
        table_wrap.pack(fill="both", expand=True)

        header_row = tk.Frame(
            table_wrap,
            bg="#FFE4A6",
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground="#E8C271",
        )
        header_row.pack(fill="x", padx=1, pady=(0, 8))
        header_row.grid_columnconfigure(0, minsize=290, weight=0)
        header_row.grid_columnconfigure(1, weight=1, uniform="rankcol")
        header_row.grid_columnconfigure(2, weight=1, uniform="rankcol")

        self.combo_filter_button = tk.Button(
            header_row,
            text="Combo + Score [Filter]",
            command=lambda: self._open_type_filter_popup(
                self.ranking_window,
                self.combo_filter_button,
                self.combo_filter_types,
                self._apply_combo_filter,
            ),
            bg=header_row["bg"],
            fg="#3A2E1B",
            activebackground="#F2D88F",
            activeforeground="#3A2E1B",
            font=("Segoe UI Semibold", 10),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=4,
            pady=2,
            anchor="w",
        )
        self.combo_filter_button.grid(row=0, column=0, sticky="w", padx=(2, 8))
        self._update_filter_button_text(
            self.combo_filter_button,
            "Combo + Score [Filter]",
            self.combo_filter_types,
        )
        tk.Label(
            header_row,
            text="Super Effective Against",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=1, sticky="w", padx=(10, 8))
        tk.Label(
            header_row,
            text="Super Effective Against This Combo",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=2, sticky="w", padx=(10, 2))

        list_wrap = tk.Frame(
            table_wrap,
            bg="#FFF7E8",
            highlightthickness=1,
            highlightbackground="#E6D4AE",
        )
        list_wrap.pack(fill="both", expand=True)

        rows_canvas = tk.Canvas(
            list_wrap,
            bg="#FFFDF8",
            highlightthickness=0,
            borderwidth=0,
        )
        y_scroll = ttk.Scrollbar(list_wrap, orient="vertical", command=rows_canvas.yview)
        rows_canvas.configure(yscrollcommand=y_scroll.set)

        rows_canvas.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        list_wrap.grid_rowconfigure(0, weight=1)
        list_wrap.grid_columnconfigure(0, weight=1)
        table_wrap.grid_columnconfigure(0, weight=1)

        rows_host = tk.Frame(rows_canvas, bg="#FFFDF8")
        rows_window = rows_canvas.create_window((0, 0), window=rows_host, anchor="nw")

        rows_host.bind(
            "<Configure>",
            lambda _event: rows_canvas.configure(scrollregion=rows_canvas.bbox("all")),
        )
        rows_canvas.bind(
            "<Configure>",
            lambda event: rows_canvas.itemconfigure(rows_window, width=event.width),
        )
        self._bind_scroll_wheel(self.ranking_window, rows_canvas)

        footer = tk.Frame(table_wrap, bg=table_wrap["bg"])
        footer.pack(fill="x", pady=(6, 0))

        self.combo_progress_label = tk.Label(
            footer,
            text="Showing 0/0",
            bg=footer["bg"],
            fg="#6A5B44",
            font=("Segoe UI", 9),
        )
        self.combo_progress_label.pack(side="left")

        self.combo_load_button = tk.Button(
            footer,
            text=f"Load {COMBO_LOAD_STEP} More",
            command=lambda: self._render_more_combo_rows(COMBO_LOAD_STEP),
            bg="#4B8CF6",
            fg="#FFFFFF",
            activebackground="#6A9BF0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        )
        self.combo_load_button.pack(side="right")

        self.combo_visible_rows = self._filter_rows_by_first_column_types(
            self.combo_rankings,
            self.combo_filter_types,
        )
        self.combo_rows_host = rows_host
        self.combo_rows_rendered = 0
        self._render_more_combo_rows(COMBO_INITIAL_ROWS)
        self._maximize_window(self.ranking_window)

    def _add_combo_ranking_row(
        self,
        rows_host: tk.Widget,
        rank: int,
        row: tuple[list[str], int, int, list[str], list[str], dict[str, float], dict[str, float]],
    ) -> None:
        (
            combo_types,
            offense_count,
            defense_count,
            offense_types,
            defense_types,
            offense_super_map,
            defense_super_map,
        ) = row
        row_bg = "#FFFDF8" if rank % 2 else "#FFF8EC"

        row_frame = tk.Frame(
            rows_host,
            bg=row_bg,
            padx=8,
            pady=8,
            highlightthickness=1,
            highlightbackground="#F2E4C5",
        )
        row_frame.pack(fill="x", padx=6, pady=3)
        row_frame.grid_columnconfigure(0, minsize=290, weight=0)
        row_frame.grid_columnconfigure(1, weight=1, uniform="rankdata")
        row_frame.grid_columnconfigure(2, weight=1, uniform="rankdata")

        combo_cell = tk.Frame(row_frame, bg=row_bg)
        combo_cell.grid(row=0, column=0, sticky="nw", padx=(2, 10))
        tk.Label(
            combo_cell,
            text=f"{rank:03}. Strong {offense_count} | Weak {defense_count}",
            bg=row_bg,
            fg="#3A2E1B",
            justify="left",
            anchor="w",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        combo_types_holder = tk.Frame(combo_cell, bg=row_bg)
        combo_types_holder.grid(row=1, column=0, sticky="w")
        self._create_type_chip_grid(
            combo_types_holder,
            combo_types,
            row_bg,
            columns=2,
        )

        offense_cell = tk.Frame(row_frame, bg=row_bg)
        offense_cell.grid(row=0, column=1, sticky="nw", padx=(8, 6))
        self._create_type_chip_grid(
            offense_cell,
            offense_types,
            row_bg,
            multiplier_map=offense_super_map,
        )

        defense_cell = tk.Frame(row_frame, bg=row_bg)
        defense_cell.grid(row=0, column=2, sticky="nw", padx=(8, 2))
        self._create_type_chip_grid(
            defense_cell,
            defense_types,
            row_bg,
            multiplier_map=defense_super_map,
        )

    def _render_more_combo_rows(self, count: int) -> None:
        if self.combo_rows_host is None:
            return

        total = len(self.combo_visible_rows)
        start = self.combo_rows_rendered
        end = min(start + count, total)

        for index in range(start, end):
            self._add_combo_ranking_row(self.combo_rows_host, index + 1, self.combo_visible_rows[index])

        self.combo_rows_rendered = end
        if self.combo_progress_label is not None:
            self.combo_progress_label.configure(text=f"Showing {end}/{total}")
        if self.combo_load_button is not None:
            if total == 0:
                self.combo_load_button.configure(text="No Matches", state="disabled")
            elif end >= total:
                self.combo_load_button.configure(text="All Rows Loaded", state="disabled")
            else:
                remaining = total - end
                self.combo_load_button.configure(state="normal")
                self.combo_load_button.configure(text=f"Load {min(COMBO_LOAD_STEP, remaining)} More")

    def _close_rankings_window(self) -> None:
        if self.ranking_window is not None and self.ranking_window.winfo_exists():
            self.ranking_window.destroy()
        self.ranking_window = None
        self.combo_rows_host = None
        self.combo_progress_label = None
        self.combo_load_button = None
        self.combo_filter_button = None
        self.combo_rows_rendered = 0
        self.combo_filter_types = set()
        self.combo_visible_rows = self.combo_rankings

    def open_defensive_table_rankings(self) -> None:
        if self.defensive_table_window is not None and self.defensive_table_window.winfo_exists():
            self.defensive_table_window.lift()
            self.defensive_table_window.focus_force()
            return

        self.defensive_table_window = tk.Toplevel(self)
        self.defensive_table_window.title("Defensive Rankings (Pre-Fairy)")
        self.defensive_table_window.geometry("1340x760")
        self.defensive_table_window.minsize(1080, 560)
        self.defensive_table_window.configure(bg="#FFF7E8")
        self.defensive_table_window.protocol("WM_DELETE_WINDOW", self._close_defensive_table_window)

        header = tk.Frame(
            self.defensive_table_window,
            bg="#FFF1CF",
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground="#EEC46E",
        )
        header.pack(fill="x", padx=14, pady=(14, 10))

        tk.Label(
            header,
            text="Defensive Type Rankings",
            bg=header["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 17),
        ).pack(anchor="w")
        tk.Label(
            header,
            text=(
                "Top 70 single/dual type combos sorted by incoming types that are "
                "not very effective against them."
            ),
            bg=header["bg"],
            fg="#5B4E3A",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        table_wrap = tk.Frame(self.defensive_table_window, bg="#FFF7E8", padx=14, pady=4)
        table_wrap.pack(fill="both", expand=True)

        header_row = tk.Frame(
            table_wrap,
            bg="#FFE4A6",
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground="#E8C271",
        )
        header_row.pack(fill="x", padx=1, pady=(0, 8))
        header_row.grid_columnconfigure(0, minsize=240, weight=0)
        header_row.grid_columnconfigure(1, minsize=165, weight=0)
        header_row.grid_columnconfigure(2, minsize=220, weight=1, uniform="defcol")
        header_row.grid_columnconfigure(3, minsize=220, weight=1, uniform="defcol")
        header_row.grid_columnconfigure(4, minsize=220, weight=1, uniform="defcol")

        self.def_table_filter_button = tk.Button(
            header_row,
            text="Type / Combo [Filter]",
            command=lambda: self._open_type_filter_popup(
                self.defensive_table_window,
                self.def_table_filter_button,
                self.defensive_filter_types,
                self._apply_defensive_filter,
            ),
            bg=header_row["bg"],
            fg="#3A2E1B",
            activebackground="#F2D88F",
            activeforeground="#3A2E1B",
            font=("Segoe UI Semibold", 10),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=4,
            pady=2,
            anchor="w",
        )
        self.def_table_filter_button.grid(row=0, column=0, sticky="w", padx=(2, 8))
        self._update_filter_button_text(
            self.def_table_filter_button,
            "Type / Combo [Filter]",
            self.defensive_filter_types,
        )
        tk.Label(
            header_row,
            text="No Effect",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=1, sticky="w", padx=(10, 8))
        tk.Label(
            header_row,
            text="Not Very Effective",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=2, sticky="w", padx=(10, 8))
        tk.Label(
            header_row,
            text="Neutral",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=3, sticky="w", padx=(10, 8))
        tk.Label(
            header_row,
            text="Super Effective",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=4, sticky="w", padx=(10, 2))

        list_wrap = tk.Frame(
            table_wrap,
            bg="#FFF7E8",
            highlightthickness=1,
            highlightbackground="#E6D4AE",
        )
        list_wrap.pack(fill="both", expand=True)

        rows_canvas = tk.Canvas(
            list_wrap,
            bg="#FFFDF8",
            highlightthickness=0,
            borderwidth=0,
        )
        y_scroll = ttk.Scrollbar(list_wrap, orient="vertical", command=rows_canvas.yview)
        rows_canvas.configure(yscrollcommand=y_scroll.set)

        rows_canvas.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        list_wrap.grid_rowconfigure(0, weight=1)
        list_wrap.grid_columnconfigure(0, weight=1)

        rows_host = tk.Frame(rows_canvas, bg="#FFFDF8")
        rows_window = rows_canvas.create_window((0, 0), window=rows_host, anchor="nw")

        rows_host.bind(
            "<Configure>",
            lambda _event: rows_canvas.configure(scrollregion=rows_canvas.bbox("all")),
        )
        rows_canvas.bind(
            "<Configure>",
            lambda event: rows_canvas.itemconfigure(rows_window, width=event.width),
        )
        self._bind_scroll_wheel(self.defensive_table_window, rows_canvas)

        footer = tk.Frame(table_wrap, bg=table_wrap["bg"])
        footer.pack(fill="x", pady=(6, 0))

        self.def_table_progress_label = tk.Label(
            footer,
            text="Showing 0/0",
            bg=footer["bg"],
            fg="#6A5B44",
            font=("Segoe UI", 9),
        )
        self.def_table_progress_label.pack(side="left")

        self.def_table_load_button = tk.Button(
            footer,
            text=f"Load {DEF_LOAD_STEP} More",
            command=lambda: self._render_more_defensive_rows(DEF_LOAD_STEP),
            bg="#4B8CF6",
            fg="#FFFFFF",
            activebackground="#6A9BF0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        )
        self.def_table_load_button.pack(side="right")

        self.defensive_visible_rows = self._filter_rows_by_first_column_types(
            self.defensive_table_rankings,
            self.defensive_filter_types,
        )
        self.def_table_rows_host = rows_host
        self.def_table_rows_rendered = 0
        self._render_more_defensive_rows(DEF_INITIAL_ROWS)
        self._maximize_window(self.defensive_table_window)

    def _add_defensive_table_row(
        self,
        rows_host: tk.Widget,
        rank: int,
        row: tuple[list[str], list[str], list[str], list[str], list[str], dict[str, float]],
    ) -> None:
        combo_types, immune_types, resisted_types, neutral_types, weak_types, defense_map = row
        row_bg = "#FFFDF8" if rank % 2 else "#FFF8EC"

        row_frame = tk.Frame(
            rows_host,
            bg=row_bg,
            padx=8,
            pady=8,
            highlightthickness=1,
            highlightbackground="#F2E4C5",
        )
        row_frame.pack(fill="x", padx=6, pady=3)
        row_frame.grid_columnconfigure(0, minsize=240, weight=0)
        row_frame.grid_columnconfigure(1, minsize=165, weight=0)
        row_frame.grid_columnconfigure(2, minsize=220, weight=1, uniform="defdata")
        row_frame.grid_columnconfigure(3, minsize=220, weight=1, uniform="defdata")
        row_frame.grid_columnconfigure(4, minsize=220, weight=1, uniform="defdata")

        combo_cell = tk.Frame(row_frame, bg=row_bg)
        combo_cell.grid(row=0, column=0, sticky="nw", padx=(2, 10))
        tk.Label(
            combo_cell,
            text=f"{rank:03}. Resist {len(resisted_types)} | Immune {len(immune_types)}",
            bg=row_bg,
            fg="#3A2E1B",
            justify="left",
            anchor="w",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        combo_types_holder = tk.Frame(combo_cell, bg=row_bg)
        combo_types_holder.grid(row=1, column=0, sticky="w")
        self._create_type_chip_grid(combo_types_holder, combo_types, row_bg, columns=1)

        immune_cell = tk.Frame(row_frame, bg=row_bg)
        immune_cell.grid(row=0, column=1, sticky="nw", padx=(8, 6))
        self._create_type_chip_grid(immune_cell, immune_types, row_bg, columns=1)

        resisted_cell = tk.Frame(row_frame, bg=row_bg)
        resisted_cell.grid(row=0, column=2, sticky="nw", padx=(14, 8))
        self._create_type_chip_grid(resisted_cell, resisted_types, row_bg, columns=3)

        neutral_cell = tk.Frame(row_frame, bg=row_bg)
        neutral_cell.grid(row=0, column=3, sticky="nw", padx=(14, 8))
        self._create_type_chip_grid(neutral_cell, neutral_types, row_bg, columns=3)

        weak_cell = tk.Frame(row_frame, bg=row_bg)
        weak_cell.grid(row=0, column=4, sticky="nw", padx=(14, 2))
        self._create_type_chip_grid(
            weak_cell,
            weak_types,
            row_bg,
            columns=3,
            multiplier_map=defense_map,
        )

    def _render_more_defensive_rows(self, count: int) -> None:
        if self.def_table_rows_host is None:
            return

        total = len(self.defensive_visible_rows)
        start = self.def_table_rows_rendered
        end = min(start + count, total)

        for index in range(start, end):
            self._add_defensive_table_row(
                self.def_table_rows_host,
                index + 1,
                self.defensive_visible_rows[index],
            )

        self.def_table_rows_rendered = end
        if self.def_table_progress_label is not None:
            self.def_table_progress_label.configure(text=f"Showing {end}/{total}")
        if self.def_table_load_button is not None:
            if total == 0:
                self.def_table_load_button.configure(text="No Matches", state="disabled")
            elif end >= total:
                self.def_table_load_button.configure(text="All Rows Loaded", state="disabled")
            else:
                remaining = total - end
                self.def_table_load_button.configure(state="normal")
                self.def_table_load_button.configure(text=f"Load {min(DEF_LOAD_STEP, remaining)} More")

    def _close_defensive_table_window(self) -> None:
        if self.defensive_table_window is not None and self.defensive_table_window.winfo_exists():
            self.defensive_table_window.destroy()
        self.defensive_table_window = None
        self.def_table_rows_host = None
        self.def_table_progress_label = None
        self.def_table_load_button = None
        self.def_table_filter_button = None
        self.def_table_rows_rendered = 0
        self.defensive_filter_types = set()
        self.defensive_visible_rows = self.defensive_table_rankings

    def open_three_type_rankings(self) -> None:
        if self.three_type_window is not None and self.three_type_window.winfo_exists():
            self.three_type_window.lift()
            self.three_type_window.focus_force()
            return

        self.three_type_window = tk.Toplevel(self)
        self.three_type_window.title("Best 3-Type Coverage (Pre-Fairy)")
        self.three_type_window.geometry("1200x700")
        self.three_type_window.minsize(960, 540)
        self.three_type_window.configure(bg="#FFF7E8")
        self.three_type_window.protocol("WM_DELETE_WINDOW", self._close_three_type_window)

        best_count = self.three_type_rankings[0][1] if self.three_type_rankings else 0

        header = tk.Frame(
            self.three_type_window,
            bg="#FFF1CF",
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground="#EEC46E",
        )
        header.pack(fill="x", padx=14, pady=(14, 10))

        tk.Label(
            header,
            text="3-Type Coverage Leaderboard",
            bg=header["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 17),
        ).pack(anchor="w")
        tk.Label(
            header,
            text=(
                f"Top 58 3-type combinations ranked by super-effective coverage. "
                f"Includes entries down to 10/17. Top coverage = {best_count}/17."
            ),
            bg=header["bg"],
            fg="#5B4E3A",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        table_wrap = tk.Frame(self.three_type_window, bg="#FFF7E8", padx=14, pady=4)
        table_wrap.pack(fill="both", expand=True)

        header_row = tk.Frame(
            table_wrap,
            bg="#FFE4A6",
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground="#E8C271",
        )
        header_row.pack(fill="x", padx=1, pady=(0, 8))
        header_row.grid_columnconfigure(0, minsize=360, weight=0)
        header_row.grid_columnconfigure(1, weight=1)

        self.three_filter_button = tk.Button(
            header_row,
            text="3 Types + Score [Filter]",
            command=lambda: self._open_type_filter_popup(
                self.three_type_window,
                self.three_filter_button,
                self.three_filter_types,
                self._apply_three_filter,
            ),
            bg=header_row["bg"],
            fg="#3A2E1B",
            activebackground="#F2D88F",
            activeforeground="#3A2E1B",
            font=("Segoe UI Semibold", 10),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=4,
            pady=2,
            anchor="w",
        )
        self.three_filter_button.grid(row=0, column=0, sticky="w", padx=(2, 8))
        self._update_filter_button_text(
            self.three_filter_button,
            "3 Types + Score [Filter]",
            self.three_filter_types,
        )
        tk.Label(
            header_row,
            text="What They Cover",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=1, sticky="w", padx=(10, 2))

        list_wrap = tk.Frame(
            table_wrap,
            bg="#FFF7E8",
            highlightthickness=1,
            highlightbackground="#E6D4AE",
        )
        list_wrap.pack(fill="both", expand=True)

        rows_canvas = tk.Canvas(
            list_wrap,
            bg="#FFFDF8",
            highlightthickness=0,
            borderwidth=0,
        )
        y_scroll = ttk.Scrollbar(list_wrap, orient="vertical", command=rows_canvas.yview)
        rows_canvas.configure(yscrollcommand=y_scroll.set)

        rows_canvas.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        list_wrap.grid_rowconfigure(0, weight=1)
        list_wrap.grid_columnconfigure(0, weight=1)

        rows_host = tk.Frame(rows_canvas, bg="#FFFDF8")
        rows_window = rows_canvas.create_window((0, 0), window=rows_host, anchor="nw")

        rows_host.bind(
            "<Configure>",
            lambda _event: rows_canvas.configure(scrollregion=rows_canvas.bbox("all")),
        )
        rows_canvas.bind(
            "<Configure>",
            lambda event: rows_canvas.itemconfigure(rows_window, width=event.width),
        )
        self._bind_scroll_wheel(self.three_type_window, rows_canvas)

        footer = tk.Frame(table_wrap, bg=table_wrap["bg"])
        footer.pack(fill="x", pady=(6, 0))

        self.three_progress_label = tk.Label(
            footer,
            text="Showing 0/0",
            bg=footer["bg"],
            fg="#6A5B44",
            font=("Segoe UI", 9),
        )
        self.three_progress_label.pack(side="left")

        self.three_load_button = tk.Button(
            footer,
            text=f"Load {THREE_LOAD_STEP} More",
            command=lambda: self._render_more_three_rows(THREE_LOAD_STEP),
            bg="#4B8CF6",
            fg="#FFFFFF",
            activebackground="#6A9BF0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        )
        self.three_load_button.pack(side="right")

        self.three_visible_rows = self._filter_rows_by_first_column_types(
            self.three_type_rankings,
            self.three_filter_types,
        )
        self.three_rows_host = rows_host
        self.three_rows_rendered = 0
        self._render_more_three_rows(THREE_INITIAL_ROWS)
        self._maximize_window(self.three_type_window)

    def _add_three_type_ranking_row(
        self,
        rows_host: tk.Widget,
        rank: int,
        row: tuple[list[str], int, list[str]],
    ) -> None:
        combo_types, coverage_count, covered_types = row
        row_bg = "#FFFDF8" if rank % 2 else "#FFF8EC"

        row_frame = tk.Frame(
            rows_host,
            bg=row_bg,
            padx=8,
            pady=8,
            highlightthickness=1,
            highlightbackground="#F2E4C5",
        )
        row_frame.pack(fill="x", padx=6, pady=3)
        row_frame.grid_columnconfigure(0, minsize=360, weight=0)
        row_frame.grid_columnconfigure(1, weight=1)

        types_cell = tk.Frame(row_frame, bg=row_bg)
        types_cell.grid(row=0, column=0, sticky="nw", padx=(2, 10))
        tk.Label(
            types_cell,
            text=f"{rank:04}. Covers {coverage_count}/17",
            bg=row_bg,
            fg="#3A2E1B",
            justify="left",
            anchor="w",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        combo_types_holder = tk.Frame(types_cell, bg=row_bg)
        combo_types_holder.grid(row=1, column=0, sticky="w")
        self._create_type_chip_grid(combo_types_holder, combo_types, row_bg, columns=3)

        coverage_cell = tk.Frame(row_frame, bg=row_bg)
        coverage_cell.grid(row=0, column=1, sticky="nw", padx=(8, 2))
        self._create_type_chip_grid(coverage_cell, covered_types, row_bg, columns=4)

    def _render_more_three_rows(self, count: int) -> None:
        if self.three_rows_host is None:
            return

        total = len(self.three_visible_rows)
        start = self.three_rows_rendered
        end = min(start + count, total)

        for index in range(start, end):
            self._add_three_type_ranking_row(self.three_rows_host, index + 1, self.three_visible_rows[index])

        self.three_rows_rendered = end
        if self.three_progress_label is not None:
            self.three_progress_label.configure(text=f"Showing {end}/{total}")
        if self.three_load_button is not None:
            if total == 0:
                self.three_load_button.configure(text="No Matches", state="disabled")
            elif end >= total:
                self.three_load_button.configure(text="All Rows Loaded", state="disabled")
            else:
                remaining = total - end
                self.three_load_button.configure(state="normal")
                self.three_load_button.configure(text=f"Load {min(THREE_LOAD_STEP, remaining)} More")

    def _close_three_type_window(self) -> None:
        if self.three_type_window is not None and self.three_type_window.winfo_exists():
            self.three_type_window.destroy()
        self.three_type_window = None
        self.three_rows_host = None
        self.three_progress_label = None
        self.three_load_button = None
        self.three_filter_button = None
        self.three_rows_rendered = 0
        self.three_filter_types = set()
        self.three_visible_rows = self.three_type_rankings

    def open_four_type_rankings(self) -> None:
        if self.four_type_window is not None and self.four_type_window.winfo_exists():
            self.four_type_window.lift()
            self.four_type_window.focus_force()
            return

        self.four_type_window = tk.Toplevel(self)
        self.four_type_window.title("Best 4-Type Coverage (Pre-Fairy)")
        self.four_type_window.geometry("1200x700")
        self.four_type_window.minsize(960, 540)
        self.four_type_window.configure(bg="#FFF7E8")
        self.four_type_window.protocol("WM_DELETE_WINDOW", self._close_four_type_window)

        best_count = self.four_type_rankings[0][1] if self.four_type_rankings else 0

        header = tk.Frame(
            self.four_type_window,
            bg="#FFF1CF",
            padx=14,
            pady=10,
            highlightthickness=1,
            highlightbackground="#EEC46E",
        )
        header.pack(fill="x", padx=14, pady=(14, 10))

        tk.Label(
            header,
            text="4-Type Coverage Leaderboard",
            bg=header["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 17),
        ).pack(anchor="w")
        tk.Label(
            header,
            text=(
                f"Top 142 4-type combinations ranked by super-effective coverage. "
                f"Includes entries down to 12/17. Top coverage = {best_count}/17."
            ),
            bg=header["bg"],
            fg="#5B4E3A",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        table_wrap = tk.Frame(self.four_type_window, bg="#FFF7E8", padx=14, pady=4)
        table_wrap.pack(fill="both", expand=True)

        header_row = tk.Frame(
            table_wrap,
            bg="#FFE4A6",
            padx=10,
            pady=8,
            highlightthickness=1,
            highlightbackground="#E8C271",
        )
        header_row.pack(fill="x", padx=1, pady=(0, 8))
        header_row.grid_columnconfigure(0, minsize=360, weight=0)
        header_row.grid_columnconfigure(1, weight=1)

        self.four_filter_button = tk.Button(
            header_row,
            text="4 Types + Score [Filter]",
            command=lambda: self._open_type_filter_popup(
                self.four_type_window,
                self.four_filter_button,
                self.four_filter_types,
                self._apply_four_filter,
            ),
            bg=header_row["bg"],
            fg="#3A2E1B",
            activebackground="#F2D88F",
            activeforeground="#3A2E1B",
            font=("Segoe UI Semibold", 10),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=4,
            pady=2,
            anchor="w",
        )
        self.four_filter_button.grid(row=0, column=0, sticky="w", padx=(2, 8))
        self._update_filter_button_text(
            self.four_filter_button,
            "4 Types + Score [Filter]",
            self.four_filter_types,
        )
        tk.Label(
            header_row,
            text="What They Cover",
            bg=header_row["bg"],
            fg="#3A2E1B",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=1, sticky="w", padx=(10, 2))

        list_wrap = tk.Frame(
            table_wrap,
            bg="#FFF7E8",
            highlightthickness=1,
            highlightbackground="#E6D4AE",
        )
        list_wrap.pack(fill="both", expand=True)

        rows_canvas = tk.Canvas(
            list_wrap,
            bg="#FFFDF8",
            highlightthickness=0,
            borderwidth=0,
        )
        y_scroll = ttk.Scrollbar(list_wrap, orient="vertical", command=rows_canvas.yview)
        rows_canvas.configure(yscrollcommand=y_scroll.set)

        rows_canvas.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        list_wrap.grid_rowconfigure(0, weight=1)
        list_wrap.grid_columnconfigure(0, weight=1)

        rows_host = tk.Frame(rows_canvas, bg="#FFFDF8")
        rows_window = rows_canvas.create_window((0, 0), window=rows_host, anchor="nw")

        rows_host.bind(
            "<Configure>",
            lambda _event: rows_canvas.configure(scrollregion=rows_canvas.bbox("all")),
        )
        rows_canvas.bind(
            "<Configure>",
            lambda event: rows_canvas.itemconfigure(rows_window, width=event.width),
        )
        self._bind_scroll_wheel(self.four_type_window, rows_canvas)

        footer = tk.Frame(table_wrap, bg=table_wrap["bg"])
        footer.pack(fill="x", pady=(6, 0))

        self.four_progress_label = tk.Label(
            footer,
            text="Showing 0/0",
            bg=footer["bg"],
            fg="#6A5B44",
            font=("Segoe UI", 9),
        )
        self.four_progress_label.pack(side="left")

        self.four_load_button = tk.Button(
            footer,
            text=f"Load {FOUR_LOAD_STEP} More",
            command=lambda: self._render_more_four_rows(FOUR_LOAD_STEP),
            bg="#4B8CF6",
            fg="#FFFFFF",
            activebackground="#6A9BF0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        )
        self.four_load_button.pack(side="right")

        self.four_visible_rows = self._filter_rows_by_first_column_types(
            self.four_type_rankings,
            self.four_filter_types,
        )
        self.four_rows_host = rows_host
        self.four_rows_rendered = 0
        self._render_more_four_rows(FOUR_INITIAL_ROWS)
        self._maximize_window(self.four_type_window)

    def _add_four_type_ranking_row(
        self,
        rows_host: tk.Widget,
        rank: int,
        row: tuple[list[str], int, list[str]],
    ) -> None:
        combo_types, coverage_count, covered_types = row
        row_bg = "#FFFDF8" if rank % 2 else "#FFF8EC"

        row_frame = tk.Frame(
            rows_host,
            bg=row_bg,
            padx=8,
            pady=8,
            highlightthickness=1,
            highlightbackground="#F2E4C5",
        )
        row_frame.pack(fill="x", padx=6, pady=3)
        row_frame.grid_columnconfigure(0, minsize=360, weight=0)
        row_frame.grid_columnconfigure(1, weight=1)

        types_cell = tk.Frame(row_frame, bg=row_bg)
        types_cell.grid(row=0, column=0, sticky="nw", padx=(2, 10))
        tk.Label(
            types_cell,
            text=f"{rank:04}. Covers {coverage_count}/17",
            bg=row_bg,
            fg="#3A2E1B",
            justify="left",
            anchor="w",
            font=("Segoe UI Semibold", 10),
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        combo_types_holder = tk.Frame(types_cell, bg=row_bg)
        combo_types_holder.grid(row=1, column=0, sticky="w")
        self._create_type_chip_grid(combo_types_holder, combo_types, row_bg, columns=4)

        coverage_cell = tk.Frame(row_frame, bg=row_bg)
        coverage_cell.grid(row=0, column=1, sticky="nw", padx=(8, 2))
        self._create_type_chip_grid(coverage_cell, covered_types, row_bg, columns=4)

    def _render_more_four_rows(self, count: int) -> None:
        if self.four_rows_host is None:
            return

        total = len(self.four_visible_rows)
        start = self.four_rows_rendered
        end = min(start + count, total)

        for index in range(start, end):
            self._add_four_type_ranking_row(self.four_rows_host, index + 1, self.four_visible_rows[index])

        self.four_rows_rendered = end
        if self.four_progress_label is not None:
            self.four_progress_label.configure(text=f"Showing {end}/{total}")
        if self.four_load_button is not None:
            if total == 0:
                self.four_load_button.configure(text="No Matches", state="disabled")
            elif end >= total:
                self.four_load_button.configure(text="All Rows Loaded", state="disabled")
            else:
                remaining = total - end
                self.four_load_button.configure(state="normal")
                self.four_load_button.configure(text=f"Load {min(FOUR_LOAD_STEP, remaining)} More")

    def _close_four_type_window(self) -> None:
        if self.four_type_window is not None and self.four_type_window.winfo_exists():
            self.four_type_window.destroy()
        self.four_type_window = None
        self.four_rows_host = None
        self.four_progress_label = None
        self.four_load_button = None
        self.four_filter_button = None
        self.four_rows_rendered = 0
        self.four_filter_types = set()
        self.four_visible_rows = self.four_type_rankings

    def _filter_rows_by_first_column_types(self, rows: list, selected_types: set[str]) -> list:
        if not selected_types:
            return rows
        return [row for row in rows if selected_types.issubset(set(row[0]))]

    def _update_filter_button_text(self, button: tk.Button | None, base_text: str, selected_types: set[str]) -> None:
        if button is None:
            return
        if selected_types:
            button.configure(text=f"{base_text} ({len(selected_types)})")
        else:
            button.configure(text=base_text)

    def _open_type_filter_popup(
        self,
        owner_window: tk.Toplevel | None,
        anchor_widget: tk.Widget | None,
        selected_types: set[str],
        apply_callback,
    ) -> None:
        if owner_window is None or not owner_window.winfo_exists():
            return
        if anchor_widget is None or not anchor_widget.winfo_exists():
            return

        # Toggle behavior: clicking the same header closes the currently open filter popup.
        if self.active_filter_popup is not None and self.active_filter_popup.winfo_exists():
            if self.active_filter_anchor == anchor_widget:
                self.active_filter_popup.destroy()
                return
            self.active_filter_popup.destroy()

        popup = tk.Toplevel(owner_window)
        popup.title("Filter Types")
        popup.transient(owner_window)
        popup.resizable(False, False)
        popup.configure(bg="#FFF7E8")
        self.active_filter_popup = popup
        self.active_filter_anchor = anchor_widget

        def clear_active_popup(_event: tk.Event | None = None) -> None:
            if self.active_filter_popup == popup:
                self.active_filter_popup = None
                self.active_filter_anchor = None

        popup.bind("<Destroy>", clear_active_popup)

        host = tk.Frame(
            popup,
            bg="#FFF7E8",
            padx=12,
            pady=10,
            highlightthickness=1,
            highlightbackground="#E6D4AE",
        )
        host.pack(fill="both", expand=True)

        tk.Label(
            host,
            text="Show rows where first-column combo includes all selected types:",
            bg=host["bg"],
            fg="#4F4536",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 8))

        chips = tk.Frame(host, bg=host["bg"])
        chips.pack(fill="x")

        selected_state = {type_name: (type_name in selected_types) for type_name in TYPES}
        chip_frames: dict[str, tk.Frame] = {}
        chip_buttons: dict[str, tk.Button] = {}
        selected_outline = "#2D7DFF"
        default_outline = host["bg"]

        status_label = tk.Label(
            host,
            text="",
            bg=host["bg"],
            fg="#2D5FB4",
            font=("Segoe UI Semibold", 9),
        )
        status_label.pack(anchor="w", pady=(6, 0))

        def refresh_status() -> None:
            chosen = [type_name for type_name in TYPES if selected_state[type_name]]
            if not chosen:
                status_label.configure(text="Selected: none")
            elif len(chosen) <= 4:
                status_label.configure(text=f"Selected: {', '.join(chosen)}")
            else:
                status_label.configure(text=f"Selected: {len(chosen)} types")

        def refresh_chip(type_name: str) -> None:
            frame = chip_frames[type_name]
            chip = chip_buttons[type_name]
            active = selected_state[type_name]
            frame.configure(bg=selected_outline if active else default_outline)
            chip.configure(relief="flat", borderwidth=0, highlightthickness=0)

        def toggle_type(type_name: str) -> None:
            selected_state[type_name] = not selected_state[type_name]
            refresh_chip(type_name)
            refresh_status()

        for index, type_name in enumerate(TYPES):
            row, column = divmod(index, 4)
            color = TYPE_COLORS[type_name]
            chip_frame = tk.Frame(chips, bg=default_outline, padx=2, pady=2, bd=0)
            chip_frame.grid(row=row, column=column, sticky="w", padx=4, pady=4)

            chip = tk.Button(
                chip_frame,
                text=type_name,
                command=lambda current=type_name: toggle_type(current),
                bg=color,
                fg=get_readable_fg(color),
                activebackground=color,
                activeforeground=get_readable_fg(color),
                font=("Segoe UI Semibold", 9),
                width=CHIP_WIDTH,
                padx=0,
                pady=5,
                borderwidth=0,
                highlightthickness=0,
                cursor="hand2",
            )
            chip.pack()
            chip_frame.bind("<Button-1>", lambda _event, current=type_name: toggle_type(current))
            chip_buttons[type_name] = chip
            chip_frames[type_name] = chip_frame
            refresh_chip(type_name)

        refresh_status()

        controls = tk.Frame(host, bg=host["bg"])
        controls.pack(fill="x", pady=(10, 0))

        def set_all(value: bool) -> None:
            for type_name in TYPES:
                selected_state[type_name] = value
                refresh_chip(type_name)
            refresh_status()

        def apply_and_close() -> None:
            chosen = {type_name for type_name, is_on in selected_state.items() if is_on}
            apply_callback(chosen)
            popup.destroy()

        tk.Button(
            controls,
            text="Select All",
            command=lambda: set_all(True),
            bg="#ECE2CA",
            fg="#3C3329",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            controls,
            text="Clear",
            command=lambda: set_all(False),
            bg="#ECE2CA",
            fg="#3C3329",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        ).pack(side="left", padx=(6, 0))

        tk.Button(
            controls,
            text="Cancel",
            command=popup.destroy,
            bg="#ECE2CA",
            fg="#3C3329",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=10,
            pady=5,
            cursor="hand2",
        ).pack(side="right")

        tk.Button(
            controls,
            text="Apply",
            command=apply_and_close,
            bg="#4B8CF6",
            fg="#FFFFFF",
            activebackground="#6A9BF0",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9),
            padx=12,
            pady=5,
            cursor="hand2",
        ).pack(side="right", padx=(0, 6))

        popup.update_idletasks()
        popup_x = anchor_widget.winfo_rootx()
        popup_y = anchor_widget.winfo_rooty() + anchor_widget.winfo_height() + 6
        popup.geometry(f"+{popup_x}+{popup_y}")

    def _apply_combo_filter(self, selected_types: set[str]) -> None:
        self.combo_filter_types = selected_types
        self.combo_visible_rows = self._filter_rows_by_first_column_types(self.combo_rankings, selected_types)
        self._update_filter_button_text(self.combo_filter_button, "Combo + Score [Filter]", selected_types)
        self._reset_combo_rows_view()

    def _apply_defensive_filter(self, selected_types: set[str]) -> None:
        self.defensive_filter_types = selected_types
        self.defensive_visible_rows = self._filter_rows_by_first_column_types(
            self.defensive_table_rankings,
            selected_types,
        )
        self._update_filter_button_text(self.def_table_filter_button, "Type / Combo [Filter]", selected_types)
        self._reset_defensive_rows_view()

    def _apply_three_filter(self, selected_types: set[str]) -> None:
        self.three_filter_types = selected_types
        self.three_visible_rows = self._filter_rows_by_first_column_types(self.three_type_rankings, selected_types)
        self._update_filter_button_text(self.three_filter_button, "3 Types + Score [Filter]", selected_types)
        self._reset_three_rows_view()

    def _apply_four_filter(self, selected_types: set[str]) -> None:
        self.four_filter_types = selected_types
        self.four_visible_rows = self._filter_rows_by_first_column_types(self.four_type_rankings, selected_types)
        self._update_filter_button_text(self.four_filter_button, "4 Types + Score [Filter]", selected_types)
        self._reset_four_rows_view()

    def _reset_combo_rows_view(self) -> None:
        if self.combo_rows_host is None:
            return
        for child in self.combo_rows_host.winfo_children():
            child.destroy()
        self.combo_rows_rendered = 0
        self._render_more_combo_rows(COMBO_INITIAL_ROWS)
        self._scroll_rows_host_to_top(self.combo_rows_host)

    def _reset_defensive_rows_view(self) -> None:
        if self.def_table_rows_host is None:
            return
        for child in self.def_table_rows_host.winfo_children():
            child.destroy()
        self.def_table_rows_rendered = 0
        self._render_more_defensive_rows(DEF_INITIAL_ROWS)
        self._scroll_rows_host_to_top(self.def_table_rows_host)

    def _reset_three_rows_view(self) -> None:
        if self.three_rows_host is None:
            return
        for child in self.three_rows_host.winfo_children():
            child.destroy()
        self.three_rows_rendered = 0
        self._render_more_three_rows(THREE_INITIAL_ROWS)
        self._scroll_rows_host_to_top(self.three_rows_host)

    def _reset_four_rows_view(self) -> None:
        if self.four_rows_host is None:
            return
        for child in self.four_rows_host.winfo_children():
            child.destroy()
        self.four_rows_rendered = 0
        self._render_more_four_rows(FOUR_INITIAL_ROWS)
        self._scroll_rows_host_to_top(self.four_rows_host)

    def _scroll_rows_host_to_top(self, rows_host: tk.Widget | None) -> None:
        if rows_host is None or not rows_host.winfo_exists():
            return
        canvas = rows_host.master
        if isinstance(canvas, tk.Canvas):
            rows_host.update_idletasks()
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.yview_moveto(0.0)
            canvas.after_idle(lambda c=canvas: c.yview_moveto(0.0))

    def _create_type_chip_grid(
        self,
        parent: tk.Widget,
        type_names: list[str],
        base_bg: str,
        columns: int = 4,
        multiplier_map: dict[str, float] | None = None,
    ) -> None:
        if not type_names:
            make_chip_label(
                parent,
                text="None",
                bg="#EDE3CF",
                fg="#6D665B",
            ).grid(row=0, column=0, padx=3, pady=3, sticky="w")
            return

        for index, type_name in enumerate(type_names):
            row, column = divmod(index, columns)
            color = TYPE_COLORS[type_name]
            multiplier = 1.0 if multiplier_map is None else multiplier_map.get(type_name, 1.0)
            chip_text = f"{type_name} x4" if multiplier >= 3.99 else type_name
            make_chip_label(
                parent,
                text=chip_text,
                bg=color,
                fg=get_readable_fg(color),
            ).grid(row=row, column=column, padx=3, pady=3, sticky="w")

    def _bind_scroll_wheel(self, window: tk.Toplevel, canvas: tk.Canvas) -> None:
        def pointer_over_canvas() -> bool:
            x = window.winfo_pointerx() - canvas.winfo_rootx()
            y = window.winfo_pointery() - canvas.winfo_rooty()
            return 0 <= x < canvas.winfo_width() and 0 <= y < canvas.winfo_height()

        def canvas_can_scroll() -> bool:
            bbox = canvas.bbox("all")
            if bbox is None:
                return False
            content_height = max(0, bbox[3] - bbox[1])
            viewport_height = max(1, canvas.winfo_height())
            return content_height > (viewport_height + 1)

        def on_mouse_wheel(event: tk.Event) -> str:
            if not pointer_over_canvas() or not canvas_can_scroll():
                return "break"
            delta = int(getattr(event, "delta", 0))
            if delta == 0:
                return "break"
            step = -1 if delta > 0 else 1
            canvas.yview_scroll(step, "units")
            return "break"

        def on_scroll_up(_event: tk.Event) -> str:
            if not pointer_over_canvas() or not canvas_can_scroll():
                return "break"
            canvas.yview_scroll(-1, "units")
            return "break"

        def on_scroll_down(_event: tk.Event) -> str:
            if not pointer_over_canvas() or not canvas_can_scroll():
                return "break"
            canvas.yview_scroll(1, "units")
            return "break"

        window.bind("<MouseWheel>", on_mouse_wheel)
        window.bind("<Button-4>", on_scroll_up)
        window.bind("<Button-5>", on_scroll_down)

    def _on_canvas_resize(self, event: tk.Event) -> None:
        self._draw_gradient(event.width, event.height)

        if self.panel_window is not None:
            panel_width = max(860, min(1160, event.width - 90))
            self.canvas.itemconfigure(self.panel_window, width=panel_width)
            self.update_idletasks()

            panel_height = self.panel.winfo_reqheight()
            top_margin = 14
            if panel_height + (top_margin * 2) > event.height:
                panel_y = (panel_height / 2) + top_margin
            else:
                panel_y = event.height / 2

            self.canvas.coords(self.panel_window, event.width / 2, panel_y)
            self.canvas.tag_raise(self.panel_window)

        if not self.bubbles:
            self._create_bubbles(event.width, event.height)

    def _draw_gradient(self, width: int, height: int) -> None:
        self.canvas.delete("gradient")

        start = (255, 233, 184)
        end = (177, 230, 255)
        max_y = max(height - 1, 1)

        for y in range(height):
            ratio = y / max_y
            red = int(start[0] + (end[0] - start[0]) * ratio)
            green = int(start[1] + (end[1] - start[1]) * ratio)
            blue = int(start[2] + (end[2] - start[2]) * ratio)
            color = f"#{red:02X}{green:02X}{blue:02X}"
            self.canvas.create_line(0, y, width, y, fill=color, tags=("gradient",))

        self.canvas.tag_lower("gradient")
        self.canvas.tag_raise("bubble")

    def _create_bubbles(self, width: int, height: int) -> None:
        bubble_colors = ["#FFD7A8", "#FFF1B0", "#D5EEFF", "#E8DBFF", "#FFE6F2"]
        for _ in range(11):
            radius = random.randint(28, 74)
            x = random.randint(radius, max(radius + 1, width - radius))
            y = random.randint(radius, max(radius + 1, height - radius))
            bubble = self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=random.choice(bubble_colors),
                outline="",
                tags=("bubble",),
            )
            self.bubbles.append(
                {
                    "id": bubble,
                    "dx": random.uniform(-0.35, 0.35),
                    "dy": random.uniform(-0.28, 0.28),
                }
            )

        self.canvas.tag_lower("bubble", self.panel_window)

    def _animate_bubbles(self) -> None:
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)

        for bubble in self.bubbles:
            item_id = int(bubble["id"])
            coords = self.canvas.coords(item_id)
            if not coords:
                continue
            x1, y1, x2, y2 = coords
            dx = float(bubble["dx"])
            dy = float(bubble["dy"])

            if x1 <= -20 or x2 >= width + 20:
                dx *= -1
                bubble["dx"] = dx
            if y1 <= -20 or y2 >= height + 20:
                dy *= -1
                bubble["dy"] = dy

            self.canvas.move(item_id, dx, dy)

        self.after(35, self._animate_bubbles)


if __name__ == "__main__":
    app = PokemonTypeApp()
    app.mainloop()
