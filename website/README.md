# MOSS-Image project page

A static academic project page, following the presentation structure of the
MOSS-Speech homepage. HTML, CSS, and JavaScript are self-contained; no build step
or external fonts are required.

From the MOSS-Image repository root:

```bash
python -m http.server 5173 --bind 0.0.0.0 --directory website
```

Open `http://localhost:5173/` or use your environment's forwarded port URL.
All local resource paths are relative, so a proxy subdirectory works without
environment-specific routing code. Keep the trailing slash in the base URL.

Content follows the repository README, including
Base/SFT model links and comparison, Diffusers Quick Start, CFG 3, user guides,
ComfyUI Manager installation, the Prompt Enhancer skill, and the QQ community link. The two showcase overview mosaics retain the
README’s original image arrangement and proportions; the introductory teaser appears above the introductory paragraph in the hero section.
The layout diagram illustrates an input specification; the showcase figures are
copied from `assets/showcase/` in the repository. Images open at full resolution.
The Live Demo button links to the Hugging Face Space.

The report is linked in the repository READMEs as
`paper/MOSS_Image_Technical_Report.pdf`. A copy lives at the same relative path
inside `website/` so the static site can be served independently. When the report
or showcase assets change, refresh the corresponding website copies too.

Starting the local preview does not publish the site.

The official homepage is https://openmoss.github.io/MOSS-Image/.
In the OpenMOSS/MOSS-Image repository, select **Settings → Pages → Source →
GitHub Actions**. The `Deploy homepage` workflow publishes `website/` when changes
to that directory or the workflow are pushed to `main`. It can also be started
manually from Actions. The workflow deploys only from the official repository;
development forks are skipped.
