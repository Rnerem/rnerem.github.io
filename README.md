# Riley Nerem — academic website

A minimalist Quarto website for Robert Riley Nerem, deployed through GitHub Actions at https://rnerem.github.io/. Cloudflare DNS and the custom domain are configured separately.

## Preview

Install [Quarto 1.10.18](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.18), the version used by the included workflow. Python 3 is also required: a small standard-library script generates the publications page and BibTeX before each render. No additional Python packages, R, or Node.js are required.

From this directory:

```sh
quarto preview --no-browser
```

Open the localhost URL printed by Quarto. To build without a live preview:

```sh
quarto render
python3 scripts/check_site.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Then open http://127.0.0.1:8000. Python 3 also runs the optional local server and link checker. A rendered `_site/` is included with this handoff; edit the `.qmd` source and rebuild to update it. Generated output is ignored by Git.

## Edit content

| File | Purpose |
| --- | --- |
| `index.qmd` | Bio, portrait, research overview, selected papers |
| `research.qmd` | Common topics in neural algorithmic reasoning |
| `publications.json` | Edit all 15 publication records, author markers, and figure captions here |
| `publications.qmd` | Generated single-page bibliography; rebuilt automatically before rendering |
| `papers.bib` | Downloadable citations generated from `publications.json` |
| `cv.qmd` | August 2026 CV download and education summary |
| `assets/riley-nerem-cv.pdf` | Current 3-page CV copied from the matching local LaTeX project |
| `contact.qmd` | Public email and verified Google Scholar profile |
| `theme.scss`, `styles.css` | Colors, typography, spacing, responsive layout |
| `_quarto.yml` | Navigation and build configuration |
| `CONTENT_REVIEW.md` | Editorial items to verify before publication |
| `SOURCES.md` | Content and portrait provenance |

The publications page includes all 15 entries supplied by Riley, with publication venues reconciled against primary records and the current CV. Edit `publications.json`, then run `quarto render`; the pre-render script updates both the page and citations. `equal` contains zero-based author indices for the primary-author asterisks requested by Riley. Figures are in `assets/publications/`; captions distinguish extracted paper figures from original conceptual schematics. Figure provenance is documented in `SOURCES.md`.

## Publish to a temporary GitHub Pages URL when ready

The repository is `Rnerem/rnerem.github.io`. Pushing changes to `main` rebuilds and deploys the site. The steps below also describe how to reproduce the setup.

1. Create an empty GitHub repository. A repository such as `academic-site` will use `https://USERNAME.github.io/academic-site/`. A repository named exactly `USERNAME.github.io` uses `https://USERNAME.github.io/`.
2. Put the **contents of this folder**, including `.github/`, at the repository root. Do not put them inside an extra `riley-nerem-site/` directory. Commit the source files and portrait; exclude `_site/` and `.quarto/`.
3. Use `main` as the default branch. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source. Leave **Custom domain** blank.
4. Push to `main`, or use **Actions → Build and deploy Quarto site → Run workflow** after enabling Pages. The workflow renders with the pinned Quarto version, checks internal links, and publishes `_site/`. Pull requests build and check without deploying.
5. Review the URL displayed by the deployment. Test navigation, portrait, paper links, the CV link, and mobile layout.

The workflow reads GitHub Pages' configured URL and supplies it to Quarto for deployment metadata. Relative internal links support both a project subdirectory and a domain root. No personal access token, `gh-pages` branch, or `_publish.yml` is required for this artifact-based workflow. Keep Pages environment deployment rules restricted to `main`.

See [GitHub's custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [Quarto's GitHub Pages guide](https://quarto.org/docs/publishing/github-pages.html).

## Custom domain — later, after reviewing the published preview

**Do not change Cloudflare DNS during this review stage.** The project intentionally contains no active custom-domain configuration or `CNAME` file.

When the temporary site is approved:

1. Review [GitHub's current custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). Verify domain ownership through GitHub as part of the later domain setup.
2. Save `robertrileynerem.com` in the repository's **Settings → Pages → Custom domain** before changing the website's DNS records.
3. Preserve an export of the existing Cloudflare records. Update only the relevant website records, preserving email and verification records. The current GitHub apex A addresses are `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`; re-check them at cutover. If using `www`, its CNAME target is `USERNAME.github.io` without a repository path.
4. Complete GitHub's DNS checks and certificate provisioning, then enable **Enforce HTTPS**. Confirm both apex and `www` behavior. Review Cloudflare proxy/TLS settings as part of that future cutover.
5. Rerun the workflow so deployment metadata reflects the new domain. For local production builds, create `_quarto-deploy.yml` with the contents below and run `quarto render --profile deploy`.

```yaml
website:
  site-url: https://robertrileynerem.com
```

A `CNAME` file is not required for this custom GitHub Actions workflow; GitHub's repository settings control the domain. If you later switch deployment methods, consult the documentation for that method.

## Assets and privacy

The portrait is a local copy of Riley's existing public WordPress portrait, retained for his requested website rebuild. See `SOURCES.md`. The site uses system fonts, local Quarto assets, and no analytics, third-party embeds, or contact-form backend. Email links open the visitor's mail application.
