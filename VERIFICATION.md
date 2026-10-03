# Verification

Rechecked locally October 2, 2026 after the requested content update.

- Quarto 1.10.18 renders all six pages successfully, including the publication-generation step.
- All 15 supplied publication entries are on one page, each with a loaded thumbnail.
- Eleven thumbnails are extracted paper figures; four are explicitly labeled original conceptual schematics.
- Five literal asterisks identify documented co-first authors across two papers. Riley's name is bold throughout.
- The site's pronoun labels have been removed.
- Internal page links, fragments, local images, image alt text, and the current CV download pass.
- Browser checks cover Home, Research, Publications, CV, and Contact at 390, 768, and 1440 pixels, with no content overflow or JavaScript errors.
- Desktop and mobile screenshots were reviewed. The three pages of the existing August 2026 CV were rendered and inspected; its final text matches the end of CV.tex.
- The CV PDF is copied unchanged from the user's local Resume folder. Its LaTeX source and res.cls are preserved separately in the handoff's cv-source folder.

No GitHub deployment or DNS change has been made. GitHub Actions is configured but has not run remotely. External publisher links may enforce their own access restrictions.
