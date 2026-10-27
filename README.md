# Project Valhalla

A 2D browser game in Norse dark fantasy. It mixes an auto-battler (cards, synergies, three of a kind for one more star) with horde survival (you steer the hero, your warband fights on its own).

## Play

Play in the browser on GitHub Pages: https://promilo101.github.io/project-valhalla/

You can also download `index.html` and open it in a browser.

## Feedback

Use **Send feedback** in the game (title screen, pause menu or after a raid). It fills in a GitHub issue with your notes and details about your run. Without a GitHub account, press **Copy feedback** and send the text to the developer. You can also open an issue here directly.

## Controls

| Key | Action |
| --- | --- |
| WASD / arrows | Move the hero |
| Space | Dash in battle (uses one dash charge) · start the next wave in the shop |
| P / Esc | Pause |
| 1 · 2 · 3 | Hero abilities, aimed at the mouse cursor |
| T | Show or hide power-up tooltips |
| R | Reroll the shop (3 gold) |
| F | Buy 4 XP (5 gold) |
| E | Sell the selected unit |
| Q | Sort the bench |
| G | Heal 30% of the hero's health (10 gold) |
| B | Open the shop in Endless mode (once every 2 minutes) |

Drag units between the bench and the formation, or right-click a unit to send it across. Drop a unit on the Sell button to sell it.

## Prototype 0.6

- 20 waves in about 15 minutes, with mini-bosses on waves 5, 10 and 15 and Fenrir on wave 20
- Endless mode after Fenrir: waves that keep getting harder, returning bosses every 5 waves that enrage after 75 seconds, and a shop you open yourself at most once every 2 minutes
- Fenrir reworked: new sprite, Gleipnir's Snap (chains that bind and pull) and Devour the Sun (an eclipse with shadow-wolf lunges)
- Warrior throws returning axes and has a new ability, Berserker Leap
- Hero abilities for the Viking: pick 1 of 2 at the start of a raid and 1 of 3 after every boss (new ability or upgrade to II/III); 8 abilities on keys 1-3, aimed with the mouse
- 24 unique unit sprites, one per class and element
- Mini-boss rework: new sprites (two looks each) and new abilities: Draugr Jarl (Axe Hurl, Barrow Rise), Frost Giant (Glacier Hurl, Fimbulwinter Breath), Herald of Hel (Half-Death, Soul Wisps)
- Fenrir is the World-Eater on wave 20 and returns Gleipnir-Bound in Endless mode
- Dash charges: 1 of 3 slots unlocked at the start, the Sleipnir's Stride power-up unlocks more, and the Sleipnir's Hooves rune raises the cap to 5
- 4 classes: Warrior and Archer (physical), Mage and Priest (magic)
- 6 card modifiers: Iron, Frost, Fire, Blood, Lightning and Rune
- Class synergies (2/4) and modifier synergies (2/3)
- Upgrade hints on shop cards and units
- Minimap with power-ups, elites and bosses
- 6 power-ups: Mead Horn, Rune of Fury, Thor's Wrath, Huginn's Call, Dwarven Hoard, Frost Rune
- Shop card locks, rising reroll/XP/heal prices within a shop phase, healing bought in the shop
- Save and quit from the shop, and cloud save with a save code (Supabase)
- In-game feedback form
- Online leaderboard for Endless runs (Supabase); runs where the debug menu was opened can't be submitted
- Rune Forge with permanent upgrades between raids (saved in the browser)

## Ideas for later

- More heroes, each with their own sprite and ability pool (the ability system is already built per hero)
- Android app: touch controls, with abilities aimed by tap or a second thumb stick

## Branches

- `main` is the public build that GitHub Pages serves.
- `dev` is the test build. It shows "DEV build" on the title screen and has a hidden debug menu. A copy is served at `/dev/` on GitHub Pages for testing.

## Publishing with GitHub Pages

The game is a single file with no build step. In the repository go to **Settings → Pages**, choose *Deploy from a branch*, branch `main`, folder `/ (root)`.
