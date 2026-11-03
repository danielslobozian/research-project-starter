# Research Project Starter — website

A complete static website for presenting Research Project Starter and its benchmark engineering. It preserves the five-page primary architecture and runs on GitHub Pages without a backend, framework, package installation or build step. The existing historical benchmark route is also bundled unchanged for deployment compatibility; it is not a new page in the primary navigation.

Preparing this archive did not modify or commit to the GitHub repository, or publish a website. Copying it into the configured publishing source is a separate action.

## Package contents

The complete replacement package contains **34 files**, including this README, `CHANGES.md` and `VALIDATION.md`. Preserve its relative folder structure and place `index.html` at the publishing root.

| Path | Purpose |
| --- | --- |
| `index.html` | Product overview: agreed question and boundaries, investigation and outputs, later scope comparison, supporting evidence and setup. |
| `engine.html` | Canonical setup destination, project files, execution instructions and operating limits. |
| `demos.html` | Recorded scope conversations, attributed A/B research findings and limitations, integrated original report previews, and guided scope comparison. |
| `benchmark.html` | October 2026 experimental design, A/B/C findings, judging, ranking and cost boundaries. |
| `engineering.html` | Independently accessible engineering case study, suitable for a direct CV link. |
| `benchmark-2026-10.html` | Byte-preserved copy of the already-published historical benchmark page. Its original stylesheet is included at `assets/css/style.css`. |
| `assets/` | Shared CSS/JavaScript, favicon, original report previews and social-preview images. Copy the entire directory. |
| `samples/` | Original approved RBs, Markdown reports, narrative appendix and PDFs. Copy the entire directory unchanged. |
| `accessible-text/` | Clearly labeled plain-text reading copies of the two Claude PDF-only reports. |
| `.nojekyll` | Tells GitHub Pages to serve this static package without Jekyll processing. This preserves the original Markdown downloads, including their YAML front matter. Keep it together with the bundled historical HTML and stylesheet. |
| `CHANGES.md` | Implemented refinements and recommendations deliberately deferred or rejected. |
| `VALIDATION.md` | Verification results, methods and outstanding limits. |

Desktop and mobile website screenshots are supplied separately as review deliverables. They are not needed for deployment. The report thumbnails in `assets/previews/` and social images in `assets/social/` are website assets and must be deployed.

## Preview locally

Extract the archive, open a terminal in the folder containing `index.html`, and use any static server you already have. For example, with Python installed:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. With an existing Node.js environment, `npx serve .` is another option; follow its printed local URL. Neither Python nor Node.js is required by the deployed website. Opening `index.html` directly also permits basic inspection, but an HTTP preview is preferable for checking browser navigation and downloads.

The five primary pages work at the server root. To preview the unchanged historical page with its original stylesheet, place the website in a folder named `research-project-starter`, start the server from its **parent folder**, and visit <http://127.0.0.1:8000/research-project-starter/>. The historical HTML deliberately retains its published `/research-project-starter/` stylesheet path; its bytes have not been rewritten for a different preview base.

## Optional deployment to GitHub Pages

1. In the repository’s **Settings → Pages**, identify the actual publishing source. It may be the selected branch’s root, its `docs/` directory, or an artifact supplied by the repository’s existing deployment workflow. Do not assume the folder is `docs/`.
2. Copy the **complete package contents** into that publishing directory: **all five primary HTML pages and the bundled `benchmark-2026-10.html`**, **all of `assets/`, `samples/` and `accessible-text/`**, **`.nojekyll`**, and the three documentation files. Place `index.html` at its root, rather than adding an extra archive-folder level. If an existing workflow publishes an artifact, include the same complete contents at that artifact’s root. This package requires no new build process.
3. Preserve the historical route as a complete set: **`benchmark-2026-10.html` and `assets/css/style.css`**. The inspected repository previously generated this route from `docs/benchmark-2026-10.md`, `_config.yml`, `_includes/ranking-table.md` and `_data/`. Adding `.nojekyll` without the bundled rendered page would lose that route. Conversely, processing the supplied `samples/` through Jekyll would convert Markdown files with YAML front matter instead of preserving the original `.md` download URLs. Deploy this package as static files, with both the historical HTML and original downloads present. Keep the historical Markdown, data and templates in the repository unchanged; they are source evidence even when no longer needed to serve the copied historical HTML. Avoid a competing generated `index.md`/`index.html` landing-page route.
4. Publish through the repository’s existing Pages configuration. Then check the five page URLs, in-page destinations, sample downloads and external evidence links. See `VALIDATION.md` for checks already completed and limits that still apply.

The five primary pages use relative local navigation and asset references, including below `/research-project-starter/`. The preserved historical page retains its original base path and existing Google Fonts references. Its stylesheet must be available at **`/research-project-starter/assets/css/style.css`**. Serving only the package at `/` is sufficient for the five primary pages, but does not supply that historical stylesheet path. For another host, retain the `/research-project-starter/` prefix or provide an equivalent server mapping for the preserved assets. Do not rewrite the frozen historical HTML or stylesheet to change the preview base or presentation.

### Canonical and sharing URLs

The absolute canonical, Open Graph and social-image URLs are configured for:

<https://danielslobozian.github.io/research-project-starter/>

When publishing at another hostname or base path, update `link[rel="canonical"]`, `og:url`, `og:image` and `twitter:image` in **all five pages**. Keep the original benchmark/evidence URLs as source references unless the historical archive itself has a verified new permanent location. A local preview does not change these publication metadata values.

## Versions and evidence

The website describes the **v1.6 workflow** and its historically supported RB-only default. The instructions, protocol, RB template, optional guide and README installation destination are pinned to commit **`f74aa2d31c910cd960a190d202b4888b158baf48`**. The instructions are pasted into project instructions; the protocol and template are uploaded as project files. The guide is optional explanatory reading, not a fourth active configuration file. Its 20 October 2026 evaluation commentary predates the completed benchmark.

The separately labeled **latest-release** route resolved to v1.6 on **3 November 2026**. It may advance as development continues; the version-matched links above remain the source for the behavior explained by this package.

The **October 2026 benchmark is an immutable historical edition**. Its source data, exclusions and conclusions remain unchanged. The C-versus-B table presents the published estimates; it does not rerun the experiment or statistical analysis. Historical evidence links on the primary pages are commit-pinned. The primary site's archive link opens the bundled relative `benchmark-2026-10.html` route. That historical HTML and its dedicated stylesheet retain their original bytes, including known accessibility limitations; the current Benchmark page supplies the C/B comparison and arm-B ranking with its current presentation. Preservation results and limits are recorded in `VALIDATION.md`.

The November demonstrations use simulated user scenarios and genuine model executions. The four Case A/B executions received their approved RBs alone. Their on-page findings and material limitations are attributed to the specific reports; they do not demonstrate the full engine's JSON companion or independently validate the reports' scientific conclusions. Original previews and report access sit with the corresponding cases. Case C introduced selected RB files in two stages and issued no new RB; it does not show automatic discovery across a repository or establish that earlier research was completed. Its private reference RBs are not included.

All original sample artifacts and four original report-preview images are preserved byte for byte. The two files under `accessible-text/` are additional reading/search aids, with provenance and extraction limitations at their start. They do not replace the PDFs or claim complete accessibility remediation. The Case B ChatGPT evidence-and-methods appendix remains an RB-only narrative artifact, distinct from the full engine’s structured JSON companion.

## Direct engineering links

The case study is independently readable from a CV. Useful destinations at the configured publication address include [system architecture](https://danielslobozian.github.io/research-project-starter/engineering.html#system), [operational failures and handling](https://danielslobozian.github.io/research-project-starter/engineering.html#incidents), and [the changed recommendation](https://danielslobozian.github.io/research-project-starter/engineering.html#learned). Additional section targets are `#question`, `#runtimes`, `#pipeline` and `#economics`.

These are publication destinations, not a claim that this replacement package has already been deployed. See `VALIDATION.md` for the checks actually performed on the packaged files.
