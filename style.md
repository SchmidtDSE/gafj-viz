# GAFJ Viz Style Guide

This style guide defines the visual design standards for the GAFJ visualization project, aligned with the aesthetic of the Rooted in Justice report at https://story.futureoffood.org/rooted-in-justice/index.html.

## Colors

### Background Colors
- **Primary Background**: `rgb(248, 236, 212)` - A warm, light beige tone
  - May darken slightly on hover or active states for interactive elements (suggest `rgb(240, 225, 195)` for hover)
  
### Highlight Colors  
- **Highlight Background**: `rgb(234, 237, 252)` - A soft, light blue
  - Used for elements with `.highlight` class
  - Also used for header backgrounds where appropriate

### Text Colors
- **Button Text**: Always white (`#FFFFFF` or `rgb(255, 255, 255)`)
  - Must remain white regardless of button state (normal, hover, active)
  - Ensures consistent visibility and accessibility

## Typography

### Font Families

#### Interactive Elements
- **Font**: IBM Plex Mono
- **Weight**: 400 (Regular)
- **Usage**: Buttons, form controls, navigation elements, and any interactive UI components
- **Source**: Already integrated (https://github.com/IBM/plex)
- **Fallback Stack**: `'IBM Plex Mono', 'Courier New', monospace`

#### Body Text
- **Font**: IBM Plex Sans  
- **Weights**: 400 (Regular), 700 (Bold)
- **Usage**: Paragraphs, descriptions, labels, and general content text
- **Source**: https://github.com/IBM/plex
- **Fallback Stack**: `'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif`

#### Headers
- **Font**: Cormorant
- **Weights**: 400 (Regular), 700 (Bold)
- **Usage**: H1-H6 headings, titles, and display text
- **Source**: https://github.com/CatharsisFonts/Cormorant
- **Fallback Stack**: `'Cormorant', Georgia, serif`

## Implementation Details

### Web Font Integration

#### @font-face Declarations
```css
/* IBM Plex Mono - already exists */
@font-face {
    font-family: 'IBMPlexMono';
    src: url('/third_party_web/IBMPlexMono-Regular.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
}

/* IBM Plex Sans */
@font-face {
    font-family: 'IBMPlexSans';
    src: url('/third_party_web/IBMPlexSans-Regular.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
}

@font-face {
    font-family: 'IBMPlexSans';
    src: url('/third_party_web/IBMPlexSans-Bold.ttf') format('truetype');
    font-weight: 700;
    font-style: normal;
}

/* Cormorant */
@font-face {
    font-family: 'Cormorant';
    src: url('/third_party_web/Cormorant-Regular.otf') format('opentype');
    font-weight: 400;
    font-style: normal;
}

@font-face {
    font-family: 'Cormorant';
    src: url('/third_party_web/Cormorant-Bold.otf') format('opentype');
    font-weight: 700;
    font-style: normal;
}
```

### CSS Implementation

#### Base Styles
```css
html {
    background-color: rgb(248, 236, 212);
    font-family: 'IBMPlexSans', 'Helvetica Neue', Arial, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Cormorant', Georgia, serif;
}

button, .button, input, select, [role="tab"] {
    font-family: 'IBMPlexMono', 'Courier New', monospace;
}

.highlight {
    background-color: rgb(234, 237, 252);
}

button, .button {
    color: white !important; /* Ensure white text always */
}
```

### Desktop (Python/Sketchingpy)
- Update const.py with new color definitions (note: Sketchingpy uses hex colors):
  - `BACKGROUND_COLOR = '#F8ECD4'` (rgb(248, 236, 212) converted to hex)
  - `HIGHLIGHT_COLOR = '#EAEDFC'` (rgb(234, 237, 252) converted to hex)
  - `BACKGROUND_HOVER = '#F0E1C3'` (rgb(240, 225, 195) converted to hex for hover state)
- Configure font loading for desktop rendering using the downloaded font files
- Apply consistent styling across all visualization components

## Accessibility Considerations
- Maintain sufficient contrast ratios between text and backgrounds
- Ensure interactive elements have clear visual states
- Keep button text consistently white for predictable user experience
- Test with screen readers to ensure proper font rendering