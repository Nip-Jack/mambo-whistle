# 📚 Documentation

Documentation for **Mambo Whistle** - Real-time neural vocal synthesis engine.

---

## 📖 Current Documentation

### Latest Updates (2025-11-25)

- **[BORDER_FIX_AND_ONBOARDING.md](BORDER_FIX_AND_ONBOARDING.md)** - 乐器卡片边框修复 + 用户引导优化
- **[BUTTON_REDESIGN_APPLE_GOOGLE_STYLE.md](BUTTON_REDESIGN_APPLE_GOOGLE_STYLE.md)** - Start Engine 按钮重新设计 (Apple/Google 风格)

---

## 🗄️ Archive

Historical documentation and development records are archived in [`.archive/`](.archive/) folder.

These include:
- AI Integration documentation
- Performance analysis reports
- Architecture overviews
- Session records
- Test scripts

---

## 🚀 Quick Start

### Run Development Server
```bash
npm run dev
# Open http://localhost:3000
```

### Test in Browser Console
```javascript
window.app.getLatencyStats()           // Check latency metrics
window.container.get('audioIO').mode   // Check audio mode
window.themeManager.getCurrentTheme()  // Check theme (dark/light)
```

---

## 🎨 Design System

**The Great Wave Theme**
- **Primary**: `#1d4ed8` (Deep Indigo)
- **Secondary**: `#93c5fd` (Seafoam Blue)
- **Fonts**: Playfair Display (headings) + Outfit (body)
- **Border Radius**: 20px (cards), 16px (buttons)

---

## 📝 Contributing

When adding new documentation:
1. Create file in `docs/` root
2. Use descriptive filename with date prefix if needed
3. Update this README with link
4. Move outdated docs to `.archive/`

---

**Last Updated**: 2025-11-25
**Version**: v2.0.0 (The Great Wave)
