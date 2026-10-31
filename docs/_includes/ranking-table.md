{% assign edition = site.data[include.data] %}
| # | Model | Effort | Score [95% CI] | Price / report | Median min |
|---|---|---|---|---|---|
{% for r in edition.rows %}{% if r.arm == include.arm %}| {{ r.rank }} | {{ r.model }} | {{ r.effort }} | {{ r.score }} {{ r.ci95 }} | {{ r.price }} | {{ r.minutes }} |
{% endif %}{% endfor %}
