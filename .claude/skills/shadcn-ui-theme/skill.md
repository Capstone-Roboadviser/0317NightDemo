---
name: shadcn-ui-theme
description: shadcn/ui design system tokens for light and dark mode. Use when applying consistent theming, colors, typography, or component styling to the project UI.
---

# shadcn/ui Design System Tokens

## Font
- **Family**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Weights**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold), 800 (extrabold)
- **Import**: `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap`

## Border Radius
- `--radius: 0.5rem` (8px)

## Light Mode (`:root`)

```css
:root {
  --background: #FFFFFF;
  --foreground: #0F172A;
  --card: #FFFFFF;
  --card-foreground: #0F172A;
  --muted: #F1F5F9;
  --muted-foreground: #64748B;
  --border: #E2E8F0;
  --input: #E2E8F0;
  --primary: #0F172A;
  --primary-foreground: #F8FAFC;
  --secondary: #F1F5F9;
  --secondary-foreground: #0F172A;
  --accent: #F1F5F9;
  --accent-foreground: #0F172A;
  --destructive: #EF4444;
  --ring: #94A3B8;
  --radius: 0.5rem;
  --chart-bg: #F8FAFC;
  --chart-grid: #E2E8F0;
  --chart-label: #94A3B8;
  --chart-line: #0F172A;
  --chart-scatter: rgba(15,76,129,0.2);
  --chart-text: #0F172A;
}
```

## Dark Mode (`.dark`)

```css
.dark {
  --background: #020817;
  --foreground: #F8FAFC;
  --card: #0F172A;
  --card-foreground: #F8FAFC;
  --muted: #1E293B;
  --muted-foreground: #94A3B8;
  --border: #1E293B;
  --input: #1E293B;
  --primary: #F8FAFC;
  --primary-foreground: #0F172A;
  --secondary: #1E293B;
  --secondary-foreground: #F8FAFC;
  --accent: #1E293B;
  --accent-foreground: #F8FAFC;
  --destructive: #7F1D1D;
  --ring: #334155;
  --chart-bg: #1E293B;
  --chart-grid: #334155;
  --chart-label: #64748B;
  --chart-line: #F8FAFC;
  --chart-scatter: rgba(96,165,250,0.3);
  --chart-text: #F8FAFC;
}
```

## Slate Color Palette Reference

| Name      | Hex       | Usage                        |
|-----------|-----------|------------------------------|
| slate-50  | `#F8FAFC` | Light primary-foreground      |
| slate-100 | `#F1F5F9` | Muted backgrounds, accents   |
| slate-200 | `#E2E8F0` | Borders, inputs              |
| slate-300 | `#CBD5E1` | Subtle borders               |
| slate-400 | `#94A3B8` | Muted text (dark), ring      |
| slate-500 | `#64748B` | Muted text (light)           |
| slate-600 | `#475569` | Secondary text               |
| slate-700 | `#334155` | Dark borders, ring (dark)    |
| slate-800 | `#1E293B` | Dark card/muted backgrounds  |
| slate-900 | `#0F172A` | Light primary, dark card bg  |
| slate-950 | `#020817` | Dark background              |

## Asset Chart Colors

| Asset        | Hex       |
|--------------|-----------|
| US Equity    | `#0F4C81` |
| Global Bonds | `#5B8E7D` |
| REIT         | `#C97C5D` |
| Gold         | `#C6A700` |
| Cash         | `#7A7A7A` |
| Accent/Selected | `#F97316` (orange-500) |

## Component Patterns

### Card
```css
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}
```

### Button (Primary)
```css
.btn-primary {
  background: var(--primary);
  color: var(--primary-foreground);
  border-radius: var(--radius);
  height: 40px;
  font-size: 14px;
  font-weight: 500;
}
```

### Input
```css
input, select {
  height: 40px;
  border: 1px solid var(--input);
  border-radius: var(--radius);
  padding: 0 12px;
  font-size: 14px;
  background: var(--background);
  color: var(--foreground);
}
```

### Badge
```css
.badge {
  padding: 2px 10px;
  border-radius: 9999px;
  border: 1px solid var(--border);
  font-size: 12px;
  font-weight: 500;
  color: var(--muted-foreground);
  background: var(--muted);
}
```

## Dark Mode Toggle Implementation

### Flash prevention (inline in `<head>` before CSS):
```html
<script>
(function(){
  var t = localStorage.getItem('theme');
  if (t === 'dark' || (t === null && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }
})()
</script>
```

### Toggle logic:
```javascript
toggle.addEventListener('click', function() {
  var isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});
```

## Typography Scale

| Element | Size  | Weight | Letter-spacing |
|---------|-------|--------|----------------|
| h1      | 42px  | 800    | -0.025em       |
| h2/title| 18px  | 600    | -0.01em        |
| body    | 14px  | 400    | normal         |
| label   | 14px  | 500    | normal         |
| small   | 13px  | 400    | normal         |
| caption | 12px  | 600    | 0.05em         |
| metric  | 30px  | 800    | -0.02em        |
