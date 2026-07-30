# Alignbase plugin submission sheet

Reviewed against the public store documentation on July 30, 2026.

## Submission status

The three packages have store-native manifests, dynamic OAuth configuration, the same 400 by 400 Alignbase logo with a blue background, and public source paths in this repository. Codex uses the PNG from its `interface` metadata, and Cursor uses the repo-relative SVG from both its marketplace entry and plugin manifest. Claude's plugin manifest and marketplace schema do not support a logo field, and the current plugin submission form does not ask for one. Anthropic stores the icon as separate directory-listing metadata after publication.

The public terms, privacy, and support pages were verified on July 30, 2026. Do not make the final policy attestations yet. These items remain open:

1. Anthropic's Software Directory Policy section 2F bars instructional software from dynamically pulling behavioral instructions from an external source for Claude to execute. Alignbase's startup context is that exact product behavior. Get written approval from Anthropic or ship a Claude-specific design that does not pull behavioral instructions before submitting.
2. Create a reviewer account with sample context and Skills. OpenAI requires credentials that work without MFA, SMS, email confirmation, or a private network. Anthropic also requires a standard test account with sample data.
3. OpenAI generates the domain verification token during submission. Deploy that exact token at `https://app.alignbase.ai/.well-known/openai-apps-challenge` before the final tool scan.

The metadata does not claim an endorsement, compare Alignbase with another product, hide paid actions, or promise unsupported features. The plugins contain no API keys, fixed OAuth client IDs, passwords, or telemetry configuration.

## Logo delivery by host

| Host | Supported path |
| --- | --- |
| OpenAI | Codex package cards and composer surfaces read `interface.logo` and `interface.composerIcon` from `.codex-plugin/plugin.json`. Both paths start with `./` and point to the 400 by 400 PNG inside the plugin. OpenAI accepts square PNG, JPEG, WebP, or SVG files up to 5 MiB. Raster images must be between 48 by 48 and 4,096 by 4,096 pixels. Our PNG is 88,013 bytes, decodes as 8-bit RGBA, and is comfortably inside every limit. |
| Claude | Claude's plugin manifest schema and marketplace schema have no logo field. Adding one produces an unrecognized-field warning and fails `--strict` validation. The current plugin submission form also has no image field. After publication, set the directory icon in **Admin settings > Directory > Submissions**. The bundled 400 by 400 PNG is prepared for that listing edit, but it does not control the card by itself. |
| Cursor | Cursor reads `logo` as a repo-relative path or an absolute URL and recommends committing the file to the repository. Cursor does not publish size, aspect-ratio, or file-size limits. The catalog and plugin manifest both point to a valid, self-contained 400 by 400 SVG, which matches Cursor's documented `assets/logo.svg` example. |

## Shared production details

| Field | Prepared value |
| --- | --- |
| Product name | Alignbase |
| Developer | Alignbase |
| Contact email | `support@alignbase.ai` |
| Website | `https://alignbase.ai` |
| Repository | `https://github.com/Sunpeak-AI/alignbase-marketplace` |
| MCP server | `https://app.alignbase.ai/mcp` |
| Authentication | OAuth 2.0 authorization code flow with PKCE and dynamic client registration |
| OAuth scopes | `context.read`, `context.write` |
| Short description | Your team's approved context. |
| Package description | Load your team's approved Alignbase context and Skills at session start. |
| Listing category | Productivity |
| Logo | `assets/alignbase-logo.png`, 400 by 400 PNG, white Alignbase mark on a blue background. Cursor also includes the equivalent SVG. |
| Support URL | `https://alignbase.ai/support/` |
| Privacy policy URL | `https://alignbase.ai/privacy/` |
| Terms URL | `https://alignbase.ai/terms/` |

## OpenAI universal plugin directory

One approved submission is published to the universal directory shared by ChatGPT and Codex.

### Official links

- Submission portal: <https://platform.openai.com/plugins>
- Submission instructions: <https://developers.openai.com/plugins/deploy/submission>
- Review requirements: <https://developers.openai.com/plugins/deploy/app-review>
- Plugin guidelines: <https://developers.openai.com/plugins/app-guidelines>
- Metadata guide: <https://developers.openai.com/plugins/guides/optimize-metadata>
- Package format: <https://developers.openai.com/plugins/build/plugins>
- Submission errors: <https://developers.openai.com/plugins/deploy/submission-errors>
- Organization roles: <https://platform.openai.com/settings/organization/people/roles>
- Organization verification: <https://platform.openai.com/settings/organization/general>

### Source and listing fields

| Portal field | Value or action |
| --- | --- |
| Submission type | With MCP |
| Plugin name | Alignbase |
| Short description | Your team's approved context. |
| Long description | Connect ChatGPT and Codex to the context and Skills assigned to the current agent in Alignbase. MCP tools load or manage Alignbase context when the agent has permission. In Codex, a user-approved startup hook loads context when a session starts. |
| Developer Identity | Select the verified Alignbase business identity |
| Category | Productivity |
| Logo | Upload `plugins/codex/alignbase/assets/alignbase-logo.png` |
| Website | `https://alignbase.ai` |
| Support URL | `https://alignbase.ai/support/` |
| Privacy policy URL | `https://alignbase.ai/privacy/` |
| Terms URL | `https://alignbase.ai/terms/` |
| Screenshots | None. The plugin has no UI, and OpenAI says not to submit screenshots for plugins without UI |
| MCP URL type | Universal |
| MCP server URL | `https://app.alignbase.ai/mcp` |
| Authentication | OAuth 2.0 |
| Demo credentials | Add the reviewer account after it is created |
| UI content security policy | Not applicable because the MCP server returns no UI |
| Countries and regions | Select only markets covered by Alignbase's terms, privacy policy, support, and export review |
| Release notes | Initial submission of Alignbase. Loads approved context and Skills assigned to an agent and provides permission-scoped MCP tools for reading, drafting, writing, and publishing Alignbase context. OAuth uses dynamic client registration and PKCE. No UI is included. |

The package manifest is `plugins/codex/alignbase/.codex-plugin/plugin.json`. It points to `.mcp.json` and the square PNG, while Codex discovers the startup hook from the package's standard `hooks/hooks.json` path. The listing logo and composer icon use the same blue-background asset. The public universal directory also has its own logo upload in the OpenAI submission form.

### Starter prompts

1. Load the Alignbase context assigned to this agent.
2. List the Alignbase Skills available to this agent.
3. Read the published version of the release-check Skill from Alignbase.
4. Show me the context alignments this agent can read and which ones it can edit.
5. Propose a new context alignment for our release review policy, but do not publish it.

### Positive test cases

1. **Load current context**
   - Prompt: `Load the Alignbase context assigned to this agent.`
   - Expected tools: `get_current_context`
   - Expected result: Published context and available Skill summaries for the demo agent, with no write.
   - Fixture: Demo agent tagged to at least one published context alignment and one published Skill.
2. **List available Skills**
   - Prompt: `List the Alignbase Skills available to this agent.`
   - Expected tools: `list_skills`
   - Expected result: A concise list with names, versions, and permissions.
   - Fixture: At least two published Skills.
3. **Read a published Skill**
   - Prompt: `Read the published release-check Skill from Alignbase.`
   - Expected tools: `list_skills`, then `read_skill` with the published version.
   - Expected result: The Skill package and install metadata.
   - Fixture: A published `release-check` Skill.
4. **Create a review proposal**
   - Prompt: `Propose a new context alignment for our release review policy. Do not publish it.`
   - Expected tools: `propose_context_alignment`
   - Expected result: A proposal ID and confirmation that no saved or published context was created.
   - Fixture: Demo agent with write permission.
5. **Publish an explicitly requested version**
   - Prompt: `Publish the latest saved version of the release-review context alignment.`
   - Expected tools: `list_context_alignments` or `read_context_alignment`, then `publish_context_alignment`
   - Expected result: The requested version is published after the agent resolves the current ID and version.
   - Fixture: Demo agent with publish permission and an unpublished saved version.

### Negative test cases

1. **Unsupported tag administration**
   - Prompt: `Create a new Finance tag and assign it to every agent.`
   - Expected behavior: Explain that the MCP tools cannot create tags or change tag assignments. Do not misuse another write tool.
2. **Unsupported deletion**
   - Prompt: `Delete the release-review context alignment permanently.`
   - Expected behavior: Explain that no delete tool is available. Do not overwrite the document with empty content.
3. **Permission boundary**
   - Prompt: `Publish the security policy even if this agent lacks publish access.`
   - Expected behavior: Do not bypass permission checks. Report the permission failure and ask the user to use an authorized agent or administrator.

### Tool annotation review

All tools operate inside a private Alignbase tenant, so `openWorldHint` is `false`. Read and list tools use `readOnlyHint: true` and `destructiveHint: false`. Create, proposal, publish, and sync-report tools use `readOnlyHint: false` and `destructiveHint: false`. Full-document replacement tools use `readOnlyHint: false` and `destructiveHint: true`.

Before submission, scan the production MCP server in the portal and inspect every response. OpenAI asks developers to remove personal data, authentication secrets, debug payloads, internal identifiers, and timestamps unless the user needs them for the stated workflow. Pay particular attention to draft author email fields and IDs in list and read responses.

### Submission steps

1. Give the submitter Apps Management Write access in the OpenAI Platform organization.
2. Complete Alignbase business verification in the same organization.
3. Confirm the support, privacy, and terms pages are live.
4. Create and seed the reviewer account.
5. Open the portal, choose **Create plugin**, then choose **With MCP**.
6. Complete the Info fields above.
7. Enter the Universal MCP URL and OAuth details.
8. Deploy the generated domain challenge token at the exact well-known path.
9. Select **Scan Tools**. Review every tool name, description, input schema, output, and annotation.
10. Add the starter prompts and eight test cases above.
11. Select the approved countries and regions, add the release notes, and make the policy attestations only after the blockers are closed.
12. Submit for review. After approval, return to the portal and publish the approved version.

Do not add upgrade, checkout, or subscription sales flows to the plugin. OpenAI's plugin rules bar using plugins to sell digital services or subscriptions, including indirect freemium upsells.

## Claude plugin directory

The same Claude directory listing is available in Cowork and Claude Code. In Claude Code it appears through the `claude-plugins-official` marketplace.

### Official links

- Submission guide: <https://claude.com/docs/plugins/submit>
- Claude.ai submission form: <https://claude.ai/admin-settings/directory/submissions/plugins/new>
- Console submission form: <https://platform.claude.com/plugins/submit>
- Plugin reference: <https://code.claude.com/docs/en/plugins-reference>
- Directory policy: <https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy>
- Directory terms: <https://support.claude.com/en/articles/13145338-anthropic-software-directory-terms>

### Submission fields

| Field | Value or action |
| --- | --- |
| Plugin GitHub link | `https://github.com/Sunpeak-AI/alignbase-marketplace/tree/main/plugins/claude/alignbase` |
| Repository visibility | Public |
| Name | Alignbase |
| Description | Load your team's approved Alignbase context and Skills at session start. |
| Developer | Alignbase |
| Contact | `support@alignbase.ai` |
| Homepage | `https://alignbase.ai` |
| Privacy policy | `https://alignbase.ai/privacy/` |
| Terms | `https://alignbase.ai/terms/` |
| Support | `https://alignbase.ai/support/` |
| Logo | The plugin form has no image field. After publication, set the listing icon in **Admin settings > Directory > Submissions** using `plugins/claude/alignbase/assets/alignbase-logo.png`. |
| Test account | Add the reviewer account after it is created |
| MCP endpoint | `https://app.alignbase.ai/mcp` |
| Example prompts | Use the first three starter prompts below |

Starter prompts:

1. Load the Alignbase context assigned to this agent.
2. List the Alignbase Skills available to this agent.
3. Show me the context alignments this agent can read and which ones it can edit.

### Policy decision required

Do not submit the current Claude package until Anthropic answers the section 2F issue in writing. The package's session hook asks Claude to call `get_current_context`, and that tool returns externally managed behavioral instructions for Claude to follow. Anthropic's current Directory Policy prohibits that behavior for instructional software.

Removing the hook alone does not fully resolve the issue because the MCP tool still returns behavioral instructions. A compliant alternative would need Anthropic's approval or a Claude-specific mode that returns reference material without asking Claude to execute it as behavioral guidance. That would change the product behavior, so it should be a product decision.

Apart from section 2F, the package now uses the current manifest schema, has narrow package copy, contains no fixed OAuth client ID, and uses the production OAuth discovery flow. The remote MCP server uses Streamable HTTP, secure OAuth 2.0, and tool annotations. Claude's manifest and marketplace schemas have no logo field. The directory listing icon must be set as listing metadata after publication. The privacy policy and support page are public. A reviewer account and at least three examples are still required.

### Submission steps after policy approval

1. Create the reviewer account.
2. Run `claude plugin validate plugins/claude/alignbase --strict`.
3. Test the plugin from the public GitHub source in a new Cowork session and a new Claude Code session.
4. Use the Claude.ai form if the submitter belongs to a Team or Enterprise organization and has directory management access. Otherwise use the Console form with a Developer, Admin, or Owner role.
5. Submit the public plugin subdirectory URL, listing fields, reviewer account, and three examples.
6. Accept the Directory Terms only after the section 2F question and privacy review are resolved.
7. After publication, open **Admin settings > Directory > Submissions** and set the listing icon to the prepared 400 by 400 PNG.
8. Push reviewed plugin updates to GitHub. Anthropic mirrors repository updates and runs automated screening, so the form does not need to be submitted again for each update.

## Cursor Marketplace

### Official links

- Plugin reference and checklist: <https://cursor.com/docs/reference/plugins>
- Publisher application: <https://cursor.com/marketplace/publish>
- Publisher Terms: <https://cursor.com/marketplace-publisher-terms>
- Publisher support: `marketplace-publishing@cursor.com`

### Publisher application fields

| Application field | Prepared value |
| --- | --- |
| Organization name | Alignbase |
| Organization handle | `alignbase` |
| Contact email | `support@alignbase.ai` |
| Logotype URL | `https://raw.githubusercontent.com/Sunpeak-AI/alignbase-marketplace/main/plugins/cursor/alignbase/assets/alignbase-logo.svg` |
| Organization description | Alignbase gives teams one place to manage and distribute approved context and Skills to their AI agents. |
| GitHub repository | `https://github.com/Sunpeak-AI/alignbase-marketplace` |
| Owner | Select the signed-in company account or team |
| Website URL | `https://alignbase.ai` |
| Publisher Terms | Accept after the company approves the remaining license grant, indemnity, and data obligations |

The repository-level Cursor catalog is `.cursor-plugin/marketplace.json`. Its `alignbase` entry points to `plugins/cursor/alignbase`, where `.cursor-plugin/plugin.json` declares the MCP server, hook, metadata, and relative logo.

### Submission steps

1. Confirm the privacy, terms, and support pages are live.
2. Test the package as a local plugin under `~/.cursor/plugins/local/alignbase`. Confirm the startup hook, OAuth flow, `get_current_context`, read tools, and permission failures.
3. Push the package and logo to the public repository. Confirm the raw logo URL returns the square blue-background SVG.
4. Sign in at the publisher application and complete the fields above.
5. Accept the Publisher Terms after the company approves the remaining license grant, indemnity, and data obligations.
6. Submit the repository for manual review. Address review feedback and request re-indexing after later updates.

The repository and all three plugin manifests use the MIT License. The company has confirmed that a free Cursor plugin may connect to the paid Alignbase service. The current copy calls the product `Cursor` exactly, makes no endorsement claim, and contains no comparative or unsupported claims. The plugin only sends requests to Alignbase and contains no model training, advertising, data sale, or third-party transfer behavior. Confirm those statements against production telemetry before making the publisher warranty.
