# Portfolio website

Mark Elamatha's design portfolio. A plain static site served by GitHub Pages from the `main` branch. No build step.

## Files

- `index.html`: home page (hero, point of view, list of work)
- `operating-model.html`, `theming.html`, `ai-prototyping.html`: case studies
- `leading.html`: how I lead
- `styles.css`: all styles and design tokens (colours, type, spacing) at the top in `:root`
- `fonts/`: Atkinson Hyperlegible Next, self-hosted (licence in `fonts/OFL.txt`)
- `images/`: screenshots and diagrams for the case studies

## Adding an image

Each case study has grey boxes marked "Image to add". To replace one:

1. Save the image in `images/` with a short, lowercase name, such as `prioritization-framework.png`. Keep files under about 500 KB.
2. Replace the `<div class="slot">...</div>` inside that `<figure>` with:
   `<img src="images/prioritization-framework.png" alt="Describe what the image shows" style="width:100%;height:auto;border-radius:6px">`
3. Keep or update the `<figcaption>`.

Never include real names, case details, SINs or internal screenshots that aren't public.

## Writing rules

- Plain language, sentence case, Canadian spelling.
- Every number must match the resume and the evidence Mark has supplied. Don't round up or invent metrics.
- The MCP server was built by the design system team. Mark set its direction and wrote the skill files.
- WCAG 2.2 AA applies to the design system itself, not to the products that use it.
- No em dashes, no all-caps labels, no arrows after links.

## Every page

The header nav and footer are repeated in each HTML file. If you change one, change all five. Each page marks its own nav link with `aria-current="page"`.
