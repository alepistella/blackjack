# GitHub Pages / adoption and later unification

## The current boundary

This kit is outside both repositories. It is not an instruction to push, deploy, enable Pages, replace a README or modify an existing workflow. Adoption is a separate user-authorised step.

The generator uses Python 3.10+ standard library only. There is no install step. `site.json` supplies the project name, actual final URL, wordmark, author, theme and related sites. `dist/` is generated output.

## Adopt into a repository

Suggested target layout:

```text
your-repository/
  site/                       Contents of starter, without its .github or dist
    site.json
    assets/
    content/
    templates/
    build.py
    check.py
    smoke_test.py
    new_post.py
    AGENTS.md                 Site-level instructions, adapted from kit
  docs/site-identity/          Copy of this kit's rules and source references
  .github/workflows/pages.yml Workflow copied to repository root, then reviewed
```

Do not copy a `.github` folder into `site/.github` and expect Actions to discover it. GitHub reads workflows at the repository root. If the target already has Pages, inspect and adapt its existing workflow. Do not create two deployments that race to publish different artifacts.

Before copying, inspect the target's instructions, licensing, working-tree changes, current branch and existing publishing setup. Copy explicitly into a new `site/` folder; do not use a destructive synchronisation command over the repository root.

For Blackjack, confirm the exact repository URL rather than deriving it from a local folder name. The supplied candidate is `https://alepistella.github.io/blackjack`; this kit has not enabled or deployed that site. Keep `theme` set to `tactical-dark` and retain `wordmark_image`.

## Preview and check

Run from the adopted `site/` directory (or `starter/` here):

```bash
python3 build.py
python3 check.py
python3 smoke_test.py
python3 -m http.server 8769 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8769/`, `/blog/` and one article. Inspect at 390 px, an intermediate width and desktop. Search and category filters work after JS loads; all notes remain visible without JS. The theme switch exists only in the local component reference, not in the published project navigation.

`check.py` verifies local asset/link targets and anchor IDs, one h1/main/title, description/canonical presence, image alternatives/dimensions, stylesheet imports, RSS and sitemap XML. It does not validate external URLs, scientific claims or all WCAG requirements. The smoke test exercises the production gate, draft exclusion, slug collision, a production build and nested deployment URLs.

## Add a blog post

```bash
python3 new_post.py a-specific-engineering-question
```

This creates a **draft** in `content/posts.json` and a body file in `content/posts/`. Fill in the metadata and replace every TODO in the body. The body is a trusted HTML fragment; the generator does not accept untrusted web submissions.

Use h2 headings with unique stable IDs, for example `<h2 id="method">Method</h2>`. The index is generated from those h2 elements. Use `{{root}}assets/...` for local images and related files in a body: the builder expands that prefix to the correct relative depth. Provide dimensions and useful alt text. Standard HTML handles tables, code, figures, details and lists without a Markdown dialect or plugin dependency.

Set `draft` to false only when the post is ready. Dates do not schedule posts: every non-draft note is included regardless of its date. The publication date is metadata, not an automation. The archive sorts by date, then slug; the homepage shows the latest three. It currently renders the full archive, suitable for a small notebook. Add pagination when there is a real volume of posts, not before.

For an update, preserve the slug and original date and add `updated` with the true date. Do not rename a published slug without preserving its former URL. If you need Markdown authoring later, choose and lock an explicit converter, then extend the tests; do not silently run prose through an unspecified parser.

## Remove demonstration content

The two supplied notes have `demo: true`. Production fails while a visible demo remains. Either replace each note with genuine project material and review its metadata, or set its `draft` to true so it is excluded. Do not merely flip the demo flag without replacing the content.

```bash
python3 build.py --production
python3 check.py
```

The production build removes the preview banner, component-reference page and its navigation link. It generates ordinary HTML, CSS and JS plus RSS, sitemap and `.nojekyll`. SEO metadata uses the configured final URL. A valid sitemap helps discovery; this kit makes no search-ranking promise.

## Workflow and GitHub settings

The included workflow assumes site sources live in `site/` on branch `main`. Adapt both if the target uses a different structure. It builds and checks pull requests without deploying them. On main, it uploads only `site/dist` and deploys through the `github-pages` environment. It does not upload source files or the rest of the repository.

Once the user authorises deployment, select **Settings → Pages → Build and deployment → Source: GitHub Actions**. Review the environment rules, branch restrictions and repository visibility. Then commit the reviewed source and root workflow and inspect the actual run. A successful local build is not proof of a successful remote deployment.

Workflow action versions follow the official GitHub Pages custom-workflow documentation consulted on 15 November 2026: checkout v6, configure-pages v5, upload-pages-artifact v4 and deploy-pages v4. Setup Python v6 provisions Python 3.12. Review current action releases and permissions when adopting later; pin full action SHAs if the repository's security policy requires it.

Sources: [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) and [custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). A project site normally lives under `/<repository>/`; this is why links must tolerate a subpath.

## Keep dum-e and Blackjack recognisable together

Now: use the same author identity and reciprocal related-project links. Keep each project name, logo and theme. An eventual author homepage can link to both without redesigning either.

Later: the same starter can generate sites under paths such as `/projects/blackjack` and `/projects/dum-e`. Set each project's final URL and preserve local relative links; CSS components do not depend on an absolute repository path. Article URLs, source links, canonical tags, RSS and sitemap all need a migration check. GitHub Pages has no general server-side redirect configuration: plan old-URL compatibility explicitly rather than assuming 301 redirects exist.

This starter is a shared source contract, not a package manager. If copied into multiple repositories, record the kit version and keep a change log. Port component/token changes deliberately and verify both themes. Do not let a Blackjack-only change rewrite dum-e's mark or vice versa.
