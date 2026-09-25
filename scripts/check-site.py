"""Check generated static pages, project coverage, links and image dimensions.

Run after build-site.py. Pillow enables independent raster dimension checks;
other checks use Python's standard library. This script never edits the site.
"""

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {"salmanhaider.pro", "www.salmanhaider.pro"}
EXPECTED_MAPS = {
    "calgary-park-accessibility.jpg", "calgary-new-park-location.jpg",
    "heathrow-global-reach.jpg", "heathrow-north-america-tourism.jpg",
    "paradise-valley-trail-run.jpg", "friends-of-greens-tree-canopy.jpg",
    "flood-affected-settlements.jpg", "housing-cost-da-vs-ct.png",
    "housing-affordability-ct-2016-2021.png", "housing-cost-ct-2016-2021.png",
    "town-of-olds-reference-map.jpg", "red-carpet-community-overview.jpg",
    "pakistan-prhps-coverage-map.jpg", "stillbirths-neonatal-deaths-asia.jpg",
    "global-stillbirths-population.jpg",
}
EXPECTED_REPOS = {
    "arcgis-geo-copilot-llm", "Logistics-Routing-MVP-Demo",
    "arcgis-drone-route-report-automation", "arcpy-forestry-sampling-point-generator",
    "GEE_NDVI_ZonalStats", "arcpy-spatial-reference-checker",
    "csv-survey-points-arcpy", "ascii-xyz-lidar-metadata-extractor",
}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = Counter()
        self.references = []
        self.images = []
        self.aria_refs = []
        self.text = []
        self.h1s = 0
        self.figures = 0
        self.ignore_text = 0
        self.meta = {}
        self.canonical = None
        self.schema = []
        self.in_schema = False
        self.schema_buffer = ''
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style"}:
            self.ignore_text += 1
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema = True
            self.schema_buffer = ''
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property', ''))] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "h1":
            self.h1s += 1
        if tag == "figure" and "project-figure" in attrs.get("class", "").split():
            self.figures += 1
        for name in ("href", "src"):
            if attrs.get(name):
                self.references.append((tag, name, attrs[name]))
        if tag == "meta" and attrs.get("property") in {"og:image", "og:url"}:
            self.references.append((tag, "content", attrs.get("content", "")))
        if tag == "img":
            self.images.append(attrs)
        for name in ("aria-labelledby", "aria-describedby", "aria-controls"):
            for item in attrs.get(name, "").split():
                self.aria_refs.append(item)

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schema.append(self.schema_buffer)
            self.in_schema = False
        if tag in {"script", "style"}:
            self.ignore_text = max(0, self.ignore_text - 1)

    def handle_data(self, data):
        if self.in_schema:
            self.schema_buffer += data
        if not self.ignore_text:
            self.text.append(data)


def local_target(page, value):
    url = urlsplit(value)
    if url.scheme in {"mailto", "tel", "data", "javascript"}:
        return None
    if url.netloc and url.netloc not in HOSTS:
        return None
    path = unquote(url.path)
    if not path:
        target = page.path
    elif path.startswith("/") or url.netloc:
        target = ROOT / path.lstrip("/")
    else:
        target = page.path.parent / path
    target = target.resolve()
    if target.is_dir():
        target /= "index.html"
    return target, unquote(url.fragment)


def actual_size(path):
    if path.suffix.lower() == ".svg":
        root = ET.parse(path).getroot()
        viewbox = root.get("viewBox", "").replace(",", " ").split()
        if len(viewbox) == 4:
            return float(viewbox[2]), float(viewbox[3])
        return None
    if Image is not None:
        with Image.open(path) as im:
            return im.size
    return None


def main():
    paths = sorted(ROOT.glob("*.html")) + sorted((ROOT / "projects").glob("*.html")) + sorted((ROOT / "articles").glob("*.html"))
    pages = {path.resolve(): Page(path.resolve()) for path in paths}
    failures, warnings = [], []
    links_checked = 0
    images_checked = 0
    size_cache = {}
    canonicals = set()
    indexable = set()
    map_refs, repo_refs = set(), set()

    def fail(page, message):
        failures.append(f"{page.path.relative_to(ROOT)}: {message}")

    for page in pages.values():
        expected_url = 'https://salmanhaider.pro/' + page.path.relative_to(ROOT).as_posix().removesuffix('index.html')
        if page.canonical != expected_url:
            fail(page, f'Incorrect canonical URL: {page.canonical}')
        if page.canonical in canonicals:
            fail(page, 'Duplicate canonical URL')
        canonicals.add(page.canonical)
        if 'noindex' not in page.meta.get('robots', ''):
            indexable.add(page.canonical)
        for key in ('description', 'robots', 'og:image', 'og:image:alt', 'og:title', 'twitter:image'):
            if not page.meta.get(key):
                fail(page, f'Missing metadata: {key}')
        if not page.schema:
            fail(page, 'Missing structured data')
        for raw in page.schema:
            try:
                schema = json.loads(raw)
                if schema.get('@context') != 'https://schema.org' or not schema.get('@graph'):
                    raise ValueError('Expected schema.org graph')
            except (ValueError, TypeError) as error:
                fail(page, f'Invalid structured data: {error}')
        if page.h1s != 1:
            fail(page, f"Expected one h1; found {page.h1s}")
        for key, count in page.ids.items():
            if count > 1:
                fail(page, f"Duplicate id: {key}")
        for key in page.aria_refs:
            if key not in page.ids:
                fail(page, f"ARIA reference has no target: {key}")

        for tag, attr, value in page.references:
            url = urlsplit(value)
            if url.netloc == "github.com" and url.path.startswith("/salman12haider13/"):
                parts = url.path.strip("/").split("/")
                if len(parts) == 2:
                    repo_refs.add(parts[1])
            target = local_target(page, value)
            if target is None:
                continue
            destination, fragment = target
            links_checked += 1
            if not destination.exists():
                fail(page, f"Missing {tag} {attr} target: {value}")
            if fragment and destination in pages and fragment not in pages[destination].ids:
                fail(page, f"Missing fragment target: {value}")
            if page.path.parent.name == "projects" and "/maps/full/" in value:
                map_refs.add(destination.name)

        for attrs in page.images:
            if "alt" not in attrs:
                fail(page, "Image has no alt attribute")
            # The viewer has one intentionally empty image populated on demand.
            if not attrs.get("src"):
                if "hidden" not in attrs:
                    fail(page, "Visible image has no source")
                continue
            target = local_target(page, attrs["src"])
            if target is None or not target[0].exists():
                continue
            path = target[0]
            if path not in size_cache:
                size_cache[path] = actual_size(path)
            real = size_cache[path]
            if real is None:
                warnings.append(f"Could not inspect image dimensions: {path.relative_to(ROOT)}")
                continue
            images_checked += 1
            try:
                width, height = float(attrs["width"]), float(attrs["height"])
                if width <= 0 or height <= 0:
                    raise ValueError
            except (KeyError, ValueError):
                fail(page, f"Missing or invalid image width/height: {attrs['src']}")
                continue
            if abs(width / height - real[0] / real[1]) > 0.002:
                fail(page, f"Image aspect ratio differs from file: {attrs['src']}")

        text = " ".join(page.text)
        if re.search("[\u2013\u2014\u2011]", text):
            fail(page, "Prose contains an en dash, em dash or nonbreaking hyphen")
        placeholders = re.findall(r"lorem ipsum|coming soon|\bTODO\b|\bTBD\b|YOUR.USERNAME|insert (?:text|title)|from a request to commands", text, re.I)
        if placeholders:
            fail(page, f"Possible placeholder text: {placeholders}")

    for missing in sorted(EXPECTED_MAPS - map_refs):
        failures.append(f"Original map not linked from a project page: {missing}")
    for missing in sorted(EXPECTED_REPOS - repo_refs):
        failures.append(f"Original repository link missing: {missing}")

    sitemap = ET.parse(ROOT/'sitemap.xml').getroot()
    sitemap_urls = [loc.text for loc in sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if set(sitemap_urls) != indexable or len(sitemap_urls) != len(set(sitemap_urls)):
        failures.append(f'Sitemap does not match indexable pages: missing {indexable-set(sitemap_urls)}, extra {set(sitemap_urls)-indexable}')
    for loc in sitemap.findall('.//{http://www.google.com/schemas/sitemap-image/1.1}loc'):
        if not (ROOT/unquote(urlsplit(loc.text).path).lstrip('/')).exists():
            failures.append(f'Sitemap image is missing: {loc.text}')
    robots = (ROOT/'robots.txt').read_text(encoding='utf-8')
    if 'Allow: /' not in robots or 'https://salmanhaider.pro/sitemap.xml' not in robots:
        failures.append('Crawler access or sitemap declaration is missing from robots.txt')
    if 'G-M8922B3N0S' not in (ROOT/'portfolio.js').read_text(encoding='utf-8'):
        failures.append('Original Google Analytics property is missing')

    project_count = 0
    figure_count = 0
    for source in ("maps.json", "tools.json"):
        for project in json.loads((ROOT / "content" / source).read_text(encoding="utf-8")):
            project_count += 1
            path = (ROOT / "projects" / (project["slug"] + ".html")).resolve()
            page = pages.get(path)
            if page is None:
                failures.append(f"Missing project page: {project['slug']}")
                continue
            expected = len(project["figures"])
            figure_count += expected
            if page.figures != expected:
                fail(page, f"Expected {expected} complete figures; found {page.figures}")

    print(f"Checked {len(pages)} pages and {project_count} project entries.")
    print(f"Checked {links_checked} local references and {images_checked} image dimension declarations.")
    print(f'SEO: {len(indexable)} indexable pages match sitemap; canonical URLs, structured data and sharing metadata checked.')
    print(f"Coverage: {len(EXPECTED_MAPS & map_refs)}/15 original maps, {len(EXPECTED_REPOS & repo_refs)}/8 repositories, {figure_count} expected project figures.")
    for warning in sorted(set(warnings)):
        print("WARNING:", warning)
    for failure in failures:
        print("FAIL:", failure)
    print(f"Result: {len(failures)} failures, {len(set(warnings))} warnings.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
