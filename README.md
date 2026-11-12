# BDD Spec Builder

Discover requirements through focused questions, write readable Gherkin scenarios, and use Cucumber.js acceptance tests to guide development. The skill identifier is `bdd-spec-builder`.

## Install

From the project where you want to use the skill, run:

```sh
npx skills add jesimpson1/bdd-spec-builder --skill bdd-spec-builder
```

The installer lets you select supported agents, including Codex, GitHub Copilot and Claude Code. Installation is project-scoped by default. To make the skill available across your projects, add `-g` to the command. Node.js is required to run the installer. [Skills CLI documentation](https://github.com/vercel-labs/skills)

Start a fresh agent session after installation. The skill supports automatic discovery and explicit invocation. The installed skill contains instructions and optional examples; the shop dependency setup below is a separate action.

## Quick start

Describe the product behaviour in ordinary language:

> Use bdd-spec-builder. Help me define how discount codes should work in this shop. Ask about any unclear business rules and show me the scenarios before implementing them.

The agent should inspect relevant project context, ask focused product questions when needed, and draft Gherkin examples for you to review. Once you agree with the behaviour, continue:

> Implement the agreed behaviour and make the scenarios executable. Run the acceptance tests using isolated local test resources.

The agent should establish the local execution scope, use Cucumber.js to exercise the agreed behaviour, and report the results and any verification gaps. A draft-only request ends with the scenarios for review.

The execution stack is Gherkin `.feature` files, Cucumber.js and JavaScript step definitions. HTTP, Playwright browser and direct application-call drivers exercise the relevant product interface beneath the same four-layer model. JavaScript is demonstrated by the runnable example. TypeScript integration can follow an existing verified Cucumber.js setup. The [execution guide](references/cucumber-js.md) covers runner configuration, scenario state and driver lifecycle. The application itself may use any technology reachable through the chosen interface.

Read [SKILL.md](SKILL.md) as the instructions an agent receives. The [feature file](examples/shop/features/promotions.feature) is the example a product owner reviews. A shopper applies SAVE10 to £80 of eligible goods and expects a £72 total.

## Execution scope

Acceptance runs default to disposable local resources, synthetic data and simulated external effects. The agent must inspect the full configuration and establish runtime isolation before execution, including application workers and provider clients. A local browser URL can still lead to a remote database or a real payment or messaging action. When local dependencies are missing, the agent should prepare a substitute or explain the verification gap. External validation requires separately scoped authorization.

The [execution guide](references/cucumber-js.md#establish-execution-scope) describes launcher checks, network restrictions, workload limits and cleanup ownership. Those controls must be implemented in each adopting suite. The shop example only creates baskets in memory and calls local JavaScript methods. It demonstrates the specification layers, with no application database or provider integration. Dependency installation downloads public npm packages.

## Optional shop example

The shop is a standalone worked demonstration of the four layers. You can read its files as a reference or run it to see a Gherkin scenario pass and fail. Using the skill in your own project does not require running the shop example.

The example's `package.json` declares its own Cucumber.js dependency and test command. Its `package-lock.json` records the resolved dependency versions. These files belong to `examples/shop/`; installing or invoking the skill does not automatically install the shop's dependencies, run its tests or add its dependencies to your application. Your project's acceptance suite uses its own package configuration and dependencies, which the agent should establish for that project.

To try the optional demonstration, run the following from this skill directory using Node.js 22 or 24 and npm. The `npm ci` command installs dependencies inside the shop example directory.

```sh
cd examples/shop
npm ci
npm test
```

The expected result is one passing scenario and three passing steps. Each run creates a fresh basket in memory. [Cucumber.js steps](examples/shop/features/steps.js) supply the domain vocabulary. The [driver](examples/shop/features/checkout-driver.js) translates between pounds and pence and calls the [checkout implementation](examples/shop/src/basket.js). The assertion gets £72 from the feature file and the observed total from checkout.

The example follows the four-layer model:

| Layer | Example file |
| --- | --- |
| Test cases | [promotions.feature](examples/shop/features/promotions.feature) |
| DSL | [steps.js](examples/shop/features/steps.js) |
| Driver | [checkout-driver.js](examples/shop/features/checkout-driver.js) |
| System under test | [basket.js](examples/shop/src/basket.js) |

This driver calls checkout in-process. A browser version would put navigation and interactions in a Playwright driver and observe the displayed total. The Gherkin can then state the promise about the checkout display while step definitions retain the business vocabulary. That browser driver is a future extension to the runnable example.

To see a meaningful failure, use a disposable copy of the shop. Change the discount rate in `src/basket.js` from `0.10` to `0.05` and run `npm test`. Checkout will return £76 and the final step should fail with £72 expected. Restore `0.10` and rerun. This exercises the pricing rule through the in-process driver. A claim about scanning a coupon at a till would need a driver that exercises that input.

## Try the same task in three agents

Use a disposable repository for each trial. Copy the contents of `examples/shop/` into its root as the starting application. Copy the whole `bdd-spec-builder/` skill directory to the project location below. Start a fresh local agent session in that repository. These paths are relative to the trial repository.

| Agent | Project location for the skill | Discovery guide |
| --- | --- | --- |
| Codex | `.agents/skills/bdd-spec-builder/` | [OpenAI Docs](https://developers.openai.com/codex/skills/) |
| GitHub Copilot CLI | `.agents/skills/bdd-spec-builder/` | [GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| Claude Code | `.claude/skills/bdd-spec-builder/` | [Claude Code Docs](https://code.claude.com/docs/en/skills) |

Give each agent the same request:

> Use the bdd-spec-builder skill. Our shop wants a new SAVE20 promotion giving 20% off eligible goods. Help me work out what to check before we build it.

The skill should turn this request into reviewable examples, choosing simple illustrative amounts. Look for Gherkin scenarios presented first, a correct expected discount and a brief explanation of how to check the result. For example, a £50 basket should cost £40 after the promotion. The user should be able to judge the scenario without choosing terminology, a runner or a driver. Any invented quantities should be identified as illustrative. Once you agree with its wording, continue:

> That looks right. Make the shop behave that way and check it works.

For the £50 example, the existing checkout should initially return £50 for SAVE20. A missing step is an intermediate wiring issue. The meaningful red result is an executed assertion showing £50 against the agreed £40. After the change, the new example and the original SAVE10 example should pass. Compare the agents on those observations and on whether you could review the rule from the feature file alone. The agent should select and report the execution command and outcomes from the project context.

## Try discovering a new feature

In a fresh session with the same shop, try:

> Use bdd-spec-builder. I want to add loyalty rewards to the shop, but I haven't worked out the details. Help me decide how it should work.

The agent should inspect the existing shop and identify which reward rules need a product decision. Look for a short statement of its understanding followed by a focused question about earning or using rewards. Any suggested earning rate should be presented for you to decide. Answer in ordinary language. The agent should retain each decision and use the answers to develop the first concrete scenario. Later questions can cover further rules as needed.

Check that later questions build on your answers. If rewards might mean points or a discount voucher, that decision should precede questions about point expiry. A recommendation should explain its reason and remain available for you to accept or change. If you say rewards follow a completed purchase, the agent should clarify what completed means when that affects eligibility, such as payment received versus goods delivered. Confirmed answers should appear consistently in the resulting scenarios.

When a decision is needed, look for the question near the start of the response with enough context to answer it. Example quantities and their assumptions should be visible before the scenarios that use them. For a claim that a reward is available immediately after a purchase, the proposed verification should identify when processing is complete and the reward can be observed. A concurrency claim should be exercised with overlapping operations. Compare those observations with the user-visible promise.

In a fresh session, check the provenance of any claimed prior agreement. For example, if the agent says you already chose how returns affect rewards, it should identify the earlier instruction or project decision supporting that statement. An unavailable source should become a question. The first review should focus on the main requested outcomes, with additional failure and recovery coverage identified for later discussion. Judge whether you can make the next decision without reading implementation terminology.

Repeat this prompt in an empty disposable repository to exercise discovery when no application exists. The conversation should establish intended users and an observable outcome without relying on existing code. Compare whether the questions helped you make decisions and whether the resulting Gherkin matches your answers. This is a manual trial procedure; executing the shop example alone does not establish the quality of an agent's interview.

## Try execution-scope decisions

In a disposable trial repository, describe a messaging feature with a local app configured to use a remote database and a real provider. Ask the agent to prepare local acceptance tests. It should identify those dependencies and establish test substitutes and isolation before running the app. Use dummy configuration and keep outbound network access blocked for the trial.

Then describe a missing local provider simulator. Check that the agent proposes a controlled adapter or reports the blocked provider verification. A request to run the acceptance tests should keep the target local. A scenario mentioning a large broadcast should trigger a volume/resource check before execution. Evaluate whether any implemented preflight refuses dummy remote destinations before loading clients or starting workers, with no outbound attempt or data mutation. These refusal checks belong to the adopting suite and have not been demonstrated by the in-memory shop example.

## Repository checks

GitHub Actions validates the skill frontmatter and local Markdown references, then installs and runs the standalone shop example on Node.js 22 and 24. It runs for pull requests and pushes to `main`, and can also be started manually. The workflow exercises in-memory baskets with synthetic values. Dependency preparation downloads public packages.

To run the metadata and documentation check locally from the repository root, use Python 3.9 or later:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install PyYAML==6.0.3
.venv/bin/python .github/scripts/validate_skill.py
```

The validator's Python dependency belongs to repository maintenance. The shop's npm dependencies remain scoped to its example directory. The workflow checks executable packaging and example behaviour; discovery conversations and browser integrations need their own trials.

## Licence

This skill, its documentation and the shop example are licensed under the [MIT licence](LICENSE). Third-party dependencies retain their respective licences.
