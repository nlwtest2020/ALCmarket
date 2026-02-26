# ALC Presentation - Strategic Overview

A modern, interactive presentation template built with React, Vite, and Tailwind CSS. Designed with a dark theme featuring cyan, purple, and magenta accents to showcase strategic market analysis and course positioning.

## Design System

### Colors
- **Primary Dark**: `#0f1419` (Background)
- **Navy**: `#1a1f2e` (Cards, sections)
- **Purple**: `#8b5cf6` (Gradient, accents)
- **Magenta**: `#bb88ff` (Button, gradient text)
- **Cyan**: `#7fe5e0` (Accents, hover states)
- **Light Blue**: `#8dd3f0` (Headers, highlights)

### Typography
- **Font Family**: Inter, Helvetica Neue (system-ui fallback)
- **Headings**: Bold, large sizes with gradient text effect
- **Body**: Regular weight, 1.6 line height

### Components

#### `Button`
Reusable button component with variants and sizes.

```jsx
<Button variant="primary" size="lg">Click Me</Button>
```

**Variants**: `primary`, `secondary`, `accent`, `outline`
**Sizes**: `sm`, `md`, `lg`

#### `Card`
Content card with optional icon, title, and hover effects.

```jsx
<Card icon="🎯" title="Feature Title" hoverable>
  Card content here
</Card>
```

#### `Hero`
Large hero section with title, subtitle, description, and CTA buttons.

```jsx
<Hero
  title="Main Title"
  subtitle="Subtitle"
  description="Description text"
  buttons={[{ label: 'Action', variant: 'primary' }]}
/>
```

#### `Navigation`
Tab-based navigation bar.

```jsx
<Navigation
  tabs={[{ id: 'tab1', label: 'Tab 1' }]}
  activeTab={activeTab}
  onTabChange={setActiveTab}
/>
```

#### `Section`
Container section with optional title and accent line.

```jsx
<Section title="Section Title" withAccentLine>
  Section content
</Section>
```

## Project Structure

```
alc-presentation/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Hero.jsx
│   │   ├── Navigation.jsx
│   │   ├── Section.jsx
│   │   └── index.js
│   ├── App.jsx             # Main app component
│   ├── App.css             # Global app styles
│   ├── index.css           # Tailwind directives + global styles
│   └── main.jsx            # Entry point
├── index.html
├── tailwind.config.js      # Tailwind configuration with theme
├── postcss.config.js       # PostCSS configuration
└── vite.config.js          # Vite configuration
```

## Getting Started

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```

Visit `http://localhost:5173` to see the presentation.

### Build
```bash
npm run build
```

## Customization Guide

### Changing Colors
Edit `tailwind.config.js` to modify the color palette:

```js
colors: {
  'alc-dark': '#0f1419',
  'alc-navy': '#1a1f2e',
  // ... add or modify colors
}
```

### Adding New Components
1. Create a new file in `src/components/`
2. Export the component in `src/components/index.js`
3. Import and use in your sections

### Styling Guidelines
- Use Tailwind utility classes for responsive design
- Use component variants for consistent styling
- Leverage the custom color names from the theme

### Adding New Sections
Wrap content in `<Section>` component with appropriate titles and styling:

```jsx
<Section title="My Section" withAccentLine>
  <div className="grid gap-6 md:grid-cols-2">
    {/* Content */}
  </div>
</Section>
```

## Features

✨ **Modern Design**: Dark theme with vibrant accent colors
⚡ **Fast Development**: Vite + React for instant HMR
🎨 **Tailwind CSS**: Utility-first styling with custom theme
📱 **Responsive**: Mobile-first design that works on all devices
🖱️ **Interactive**: Tab navigation, hover effects, smooth transitions
♿ **Accessible**: Semantic HTML, proper ARIA attributes

## Next Steps

1. **Edit Content**: Modify `App.jsx` to add your presentation content
2. **Add Sections**: Use the `Section` component to organize content
3. **Customize Colors**: Adjust the Tailwind theme to match your brand
4. **Add Images**: Import and use images in Hero or Card components
5. **Create Pages**: Expand with multiple pages or modal overlays

## License

© 2026 ALC Presentation. All rights reserved.
