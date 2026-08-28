# Rebocap Blender Plugin (Beta 11.7)

Official Blender Addon for the Rebocap Motion Capture System.

[![Release](https://img.shields.io/badge/Release-Beta_11.7-blue.svg)](https://github.com/rebocapofficial/rebocap_blender_plugin/releases)
[![Blender](https://img.shields.io/badge/Blender-3.6_%7C_4.2_LTS_%7C_5.x-orange.svg)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-GPL_v3-green.svg)](LICENSE)

---

## 🚀 Key Features in Beta 11.7:

1. **🛡️ Dual Physical Button Layout (Anti-Misfire Protection)**:
   - Separated `[ 🔴 Start Record ]` and `[ ⏹️ Stop Record ]` into dual independent physical buttons.
   - Dynamic state locking completely eliminates accidental double-click take truncations.

2. **🌐 Complete 9-Language Localization (i18n)**:
   - Full native localization for **English**, **简体中文**, **繁體中文**, **日本語**, **Español**, **Français**, **Italiano**, **한국어**, and **Русский**.
   - Persistent language selection with cross-session memory and smart English fallback.
   - Comprehensive translation coverage across all UI panels, modal operators, dialogs, unit scales, and tooltips.

3. **⚡ Viewport FPS Throttling (`按场景帧率显示动捕`)**:
   - Decoupled high-speed 60Hz internal mocap evaluation from 3D viewport rendering.
   - Optional toggle to synchronize viewport redraw rate with scene FPS (e.g. 24/30 FPS), drastically reducing GPU load during live streaming and complex scene animation.

4. **🎬 Unified FPS Retiming Pipeline**:
   - Resample and mount raw 60 FPS mocap takes to 24/30/60 FPS or custom FPS in 1:1 perfect lockstep.
   - Synchronized Pelvis translation and 24-joint rotation curves.
   - Quick Scene FPS editor operator directly accessible in the connection panel.

5. **👤 Interactive Viewport Puppet Canvas HUD**:
   - Maya HumanIK-style viewport overlay mannequin with 22 glowing node sockets.
   - Real-time mapping feedback (Green: mapped, Red: unmapped).
   - One-click navigation: click any mapped green node on the HUD to immediately select and focus that bone in Blender's 3D Viewport POSE mode.

6. **📊 Clean History Table & Unread Notification**:
   - Modern take management list with dynamic unread badges `[ 1 ] 🔴`.
   - Double-click inline renaming for take items.
   - Native confirmation modal popup prevents accidental take deletions.

---

## 📦 Installation
1. Download the latest `rebocap_blender_plugin_Beta11_7.zip` from [Releases](https://github.com/rebocapofficial/rebocap_blender_plugin/releases).
2. In Blender, navigate to `Edit` ➔ `Preferences` ➔ `Add-ons` ➔ `Install...` (or `Get Extensions` ➔ `Install from Disk...` in Blender 4.2+).
3. Select the `.zip` file and enable **Rebocap Motion Capture**.

