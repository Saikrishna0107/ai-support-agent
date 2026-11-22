# Data

`raw/` holds the knowledge base for **Kestrel Electronics**, a fictional online electronics store made up for this project. All company names, products, prices, policies, phone numbers, and email addresses are invented. The phone numbers use the reserved 555-01xx range and the emails use the reserved `.example` domain.

| Folder | Contents |
|---|---|
| `raw/policies/` | Shipping, returns, warranty, protection plans, payments, orders |
| `raw/account/` | Rewards program, login help, privacy, contact and escalation rules |
| `raw/products/` | Product pages with specs, prices, and box contents |
| `raw/troubleshooting/` | Step-by-step fixes for common problems |

Each file starts with a metadata header (title, category, last_updated) that the ingestion step uses for citations.

The facts are deliberately specific and consistent so the evaluation suite can check the agent's answers against them. Some rules have exceptions on purpose (for example, opened earbuds are returnable only if defective, and drones can't ship Next-Day) to test whether retrieval finds the right passage.
