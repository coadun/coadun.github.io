# Coadun

Website for [Coadun](https://coadun.github.io) — a transformation service for Open Source-Enabled Statistical Computing Environments (SCEs), delivered in collaboration by [Achieve Intelligence](https://www.achieveintelligence.com/) and [Jumping Rivers](https://www.jumpingrivers.com/).

---

## Repository Structure

| File               | Purpose                                                                                                                                                                                                                               |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index.html`       | The main (and only) page of the site. Contains all content sections: About, Challenges, Service, Process, and Contact.                                                                                                                |
| `llms.txt`         | A plain-text file describing Coadun for AI crawlers and large language models, following the [llms.txt convention](https://llmstxt.org/). Helps AI-powered search tools (Perplexity, ChatGPT, etc.) accurately represent the service. |
| `robots.txt`       | Instructs web crawlers which parts of the site to index. Points crawlers to `sitemap.xml` and blocks the privacy notice document from being indexed.                                                                                  |
| `sitemap.xml`      | Lists the URLs that search engines should index. Submitted to Google Search Console and Bing Webmaster Tools to accelerate discovery.                                                                                                 |
| `site.webmanifest` | Web app manifest file. Defines metadata (name, icons, theme colour) used when the site is added to a mobile home screen or installed as a Progressive Web App (PWA).                                                                  |
| `_config.yml`      | Jekyll configuration file used by GitHub Pages. Configures site-level settings and can be used to set the site URL, title, and build options.                                                                                         |

## Contact

For enquiries about SCE transformation: [hello@coadun.net](mailto:hello@coadun.net)
