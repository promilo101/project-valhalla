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
| Space | Dash in battle · start the next wave in the shop |
| P / Esc | Pause |
| T | Show or hide power-up tooltips |
| R | Reroll the shop (3 gold) |
| F | Buy 4 XP (5 gold) |
| E | Sell the selected unit |
| Q | Sort the bench |
| G | Heal 30% of the hero's health (10 gold) |

Drag units between the bench and the formation, or right-click a unit to send it across. Drop a unit on the Sell button to sell it.

## Prototype 0.4

- 20 waves in about 15 minutes, with mini-bosses on waves 5, 10 and 15 and Fenrir on wave 20
- 4 classes: Warrior and Archer (physical), Mage and Priest (magic)
- 6 card modifiers: Iron, Frost, Fire, Blood, Lightning and Rune
- Class synergies (2/4) and modifier synergies (2/3)
- Upgrade hints on shop cards and units
- Minimap with power-ups, elites and bosses
- 6 power-ups: Mead Horn, Rune of Fury, Thor's Wrath, Huginn's Call, Dwarven Hoard, Frost Rune
- Shop card locks, rising reroll/XP/heal prices within a shop phase, healing bought in the shop
- In-game feedback form
- Rune Forge with permanent upgrades between raids (saved in the browser)

## Publishing with GitHub Pages

The game is a single file with no build step. In the repository go to **Settings → Pages**, choose *Deploy from a branch*, branch `main`, folder `/ (root)`.
