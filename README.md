# Salman Haider GIS Portfolio

A static GIS portfolio for Salman Haider, a GIS professional in Canada, published through GitHub Pages at https://salmanhaider.pro. GitHub Pages deploys the root of the `main` branch.

## Preview

Serve this folder with a static server, then open http://127.0.0.1:4173.

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

The checked-in HTML works directly on GitHub Pages. There are no runtime packages, external fonts or build service requirements.

## Content and pages

* `index.html`: introduction and four selected projects.
* `work.html`: all 18 projects with category filters.
* `projects/`: individual stories covering all 15 original maps and eight coding projects.
* `about.html`: experience, education, capabilities and personal photographs.
* `articles/`: article HTML pages and their landing page. The empty landing page is excluded from indexing until the first article is added.
* `content/maps.json`, `content/tools.json`, `content/profile.json`: editable source content.
* `scripts/build-site.py`: generates HTML and the sitemap from those content files using the Python standard library. Run after editing the content or page templates.
* `portfolio.css`, `portfolio.js`: shared design and accessible navigation, filters and image inspection.

```powershell
python scripts/build-site.py
```

Maps retain their complete layouts and aspect ratios. Compressed display images are in `assets/images/maps/display/`; originals remain in `assets/images/maps/full/`. Image inspection opens originals, with mouse, keyboard and touch controls. `scripts/prepare-images.py` rebuilds display copies and dimension metadata with Pillow. Coding visuals include actual project outputs and diagrams drawn from the documented workflow.

`scripts/create-project-charts.py` uses matplotlib to regenerate the Geo Copilot overview and three charts from report scores. Its seven accepted projection warnings are explicitly labelled, so evaluation scores are not presented as execution success rates. `scripts/create-method-visuals.py` draws the forestry selection criteria. `scripts/create-social-preview.py` uses Pillow for the social sharing card. These packages are needed only to regenerate assets, not to build or serve the site.

The original resume PDF and custom domain configuration are preserved. Analytics run only on the production domain. Existing section and project hash links are redirected to the appropriate pages. Old cropped thumbnails, unused illustrations and unused personal photos have been removed from the site; a verified archive is retained outside the repository.

## Search, sharing and crawler access

The stories are complete static HTML, with real internal links, headings, image descriptions and captions. Search engines and text-based readers do not need JavaScript to read them. Each page has a unique canonical URL, description and social sharing metadata. The home and About pages identify Salman as a GIS professional in Canada with over four years of applied GIS experience, a completed Master of Geographic Information Systems from the University of Calgary, and an interest in opportunities across Canada. These descriptions are edited in `content/profile.json` under `seo`. Structured data describes the author, country, degree, GIS skills, website, profile, project work and source repositories; future posts receive BlogPosting metadata.

The sitemap includes the 21 current indexable pages and the project images. `robots.txt` retains its general allow rule and sitemap reference, which also permits search crawlers such as OAI-SearchBot. The 404 page and empty Articles landing page are marked `noindex, follow`. Articles join the sitemap when actual posts are added.

Google Analytics retains property `G-M8922B3N0S`. The script loads on `salmanhaider.pro` and `www.salmanhaider.pro`, but not on localhost. The custom domain and original resume are unchanged. Search Console, Bing Webmaster Tools, search rankings and Analytics account reception are separate from the site's metadata and deployment checks.

No special AI-only text or `llms.txt` was added. The approach follows [Google's AI optimization guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) and [OpenAI's crawler documentation](https://developers.openai.com/api/docs/bots). Crawler access makes discovery possible; it does not guarantee indexing or inclusion in an answer.

`python scripts/check-site.py` checks page structure, local links, all original maps and repositories, image dimensions, canonical URLs, sharing metadata, structured data and sitemap coverage.

## Adding an article

Create an HTML fragment at `content/articles/my-article.html`, using paragraphs, headings starting at `h2`, figures and code blocks as needed. The builder supplies the page title, navigation and footer. Add a matching entry to `content/articles.json`:

```json
{
  "slug": "my-article",
  "title": "The article title",
  "description": "A short summary of what the reader will learn.",
  "date": "YYYY-MM-DD",
  "image": "assets/images/path-to-a-sharing-image.png"
}
```

The optional `modified` field records a real revision date. Use lowercase words separated by hyphens for the slug. In the HTML fragment, image paths start with `../assets/` because the finished page lives in `articles/`.

Run `python scripts/prepare-images.py` when adding images, then `python scripts/build-site.py` and `python scripts/check-site.py`. The builder creates the complete page in `articles/`, adds it to the Articles index and sitemap, and supplies author, publication date and BlogPosting structured data. The empty Articles landing page automatically becomes indexable once a real post exists. Files are ready for a separately approved publication through GitHub Pages.

## Backup and review

A byte-verified backup of all 73 originally tracked files is stored outside this repository in the sibling source-material folder:

`../Data reated to maps/Portfolio backups/portfolio-before-redesign-2026-09-24-53862a5.zip`

The adjacent JSON file records the original commit and archive checksum. The original commit is `53862a5b7753a197a5d36304846c15a18e707f66`.

Review future changes locally before pushing `main`, which triggers publication. The content and source images include older project limitations; the relevant pages explain them without changing the original maps.
