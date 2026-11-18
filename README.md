# AgentSEO Claude SEO Starter

Use Claude Code to make a decision from a Search Console export or draft a content brief from dated search results. The skill and bundled data are free. The sample workflows require Claude Code access and use its configured model. They require no AgentSEO key or paid SEO data.

Install this public source into a project with Git:

```sh
git clone https://github.com/AgentSEO-dev/agentseo-claude-seo.git /tmp/agentseo-claude-seo
mkdir -p .claude/skills
cp -R /tmp/agentseo-claude-seo .claude/skills/agentseo-claude-seo
claude
```

Use an empty temporary destination for the clone. Check for an existing project skill before copying. This repository contains the MIT-licensed starter skill and example files published on AgentSEO. The product repository has a separate license.

Download `agentseo-claude-seo.zip` from the [Claude SEO guide](https://www.agentseo.dev/blog/claude-seo). In a project where you want the skill available, extract the archive under `.claude/skills`:

```sh
mkdir -p .claude/skills
unzip -n /path/to/agentseo-claude-seo.zip -d .claude/skills
claude
```

If you already installed the skill, compare the folders before replacing it. Invoke one of these commands inside Claude Code:

```text
/agentseo-claude-seo sample refresh
/agentseo-claude-seo sample create
/agentseo-claude-seo sample investigate
/agentseo-claude-seo brief .claude/skills/agentseo-claude-seo/examples/serp-claude-seo.json
```

The three decision cases use synthetic Search Console rows and page notes. Their expected decisions were written for comparison. The brief uses four selected results from an observed Google snapshot. [Search Console walkthrough](https://www.agentseo.dev/blog/claude-code-search-console) · [Filled content brief](https://www.agentseo.dev/blog/claude-code-seo-content-brief)

For your own export, use the same columns as the sample and keep one row per window, query, page, and search segment. Dates are inclusive in the Search Console time zone (Pacific time). Use `prior` and `current` for the two windows. Use final data, preserve missing rows as missing, and supply notes about existing pages and relevant result formats when you have them.

```text
/agentseo-claude-seo console data/query-page.csv data/page-notes.md
/agentseo-claude-seo brief data/dated-serp.json
```

Use the bundled SERP JSON as the format for a dated export. The sample includes `examples/search-console-comparison.csv`, generated from the source CSV by the Python helper. To check a query's arithmetic without Claude, run:

```sh
python3 .claude/skills/agentseo-claude-seo/scripts/compare-search-console.py \
  .claude/skills/agentseo-claude-seo/examples/search-console.csv \
  --query "seo audit checklist"
```

For a fresh Google result, [connect AgentSEO to Claude Code](https://www.agentseo.dev/integrations/claude-code) and explicitly request a live run. This path uses an AgentSEO key and credits.

```text
/agentseo-claude-seo live brief claude seo | United States | en | desktop
```

If AgentSEO is still processing, copy the resume command from the response. The format is `/agentseo-claude-seo resume <job-id> | desktop`. Replace the placeholder with the returned ID and use the requested device. If a result contains redirect links with no clear destinations, use the rank and title for a provisional brief and supply a dated export with direct result URLs to finish it.

Keep credentials and private exports out of shared folders. Claude Code processes the selected inputs using its configured model. Use data you are allowed to process with that provider.
