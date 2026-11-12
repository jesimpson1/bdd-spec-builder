# Cucumber.js execution

Read the project's installed `@cucumber/cucumber` version, Node requirements and module conventions before configuring the suite. Use the existing package manager and a reproducible dependency lock. The bundled shop demonstrates JavaScript ESM with Cucumber.js 13.3.0. Match other versions to their documentation.

## Establish execution scope

Before executing a suite, trace the side effects of its steps, hooks, application startup and background processing. Identify the effective destinations for the app, database, queue, storage, callbacks and provider clients, including configuration overrides. Check environment settings by destination and credential type, redacting secrets in reports. Even an in-process driver can reach remote resources through the application it calls.

Set up a test launcher that validates explicit test configuration before starting Cucumber or the application. Support files and application imports can initialize clients or cause side effects, so a scenario hook alone may run too late. A Cucumber dry run also loads support code and requires this check. An unknown target or inherited live credential should cause refusal before resource access. Resource names such as test, staging or sandbox are hints to inspect, not evidence of ownership or isolation.

For ordinary acceptance execution:

- Use synthetic fixtures and an explicitly configured disposable database, queue namespace and storage area owned by the run. Seed and cleanup commands must target those resources. Keep fixture resets away from shared or developer data.
- Build a controlled runtime environment with test credentials instead of inheriting the developer's full shell environment or loading their ordinary application secrets. Make provider bindings select a local simulator, stub or recording adapter, with missing configuration causing failure. Verify that failure and retry paths use the same isolated bindings.
- Enforce runtime network restrictions across the runner, application, workers and browser so only intended test resources are reachable. For example, use an isolated container network or equivalent host controls. Browser request interception alone leaves server and worker egress uncontrolled. Apply destination rules to redirects and callbacks too. Dependency downloads can use a separate preparation phase before the isolated application run.
- Bound fixture counts, duration and resource consumption. A functional broadcast example can use a few synthetic recipients. A separately requested large workload needs explicit volume and resource limits, an abort condition and retained evidence. Its size must not silently propagate into external provider traffic.
- Stop background producers and drain or remove run-owned work before cleanup. Preserve unrelated data and resources. Report failures and incomplete cleanup rather than retrying against a different environment.

If there is no local substitute for a dependency, identify what a simple fake would establish and what still requires provider validation. Continue with the supported local checks. A stubbed provider verifies application behaviour against that stub's contract. Any external run is a separate scoped action requiring explicit authorization, including exact target, recipients or accounts, permitted operations, maximum volume/spend and stopping conditions. A generic confirmation prompt or an environment variable called safe does not replace those controls.

The skill specifies this policy. Each adopting repository must implement and verify its launcher and isolation controls. Exercise refusal cases using dummy remote targets and synthetic credential sentinels while network access is blocked, before relying on a suite for large workloads. Record the controls actually verified and any gaps. Never prove a refusal mechanism by sending traffic to a real recipient or production endpoint.

## Connect features to executable steps

Store the agreed examples in `.feature` files. Bind phrases with Cucumber expressions in `Given`, `When` and `Then` definitions imported from `@cucumber/cucumber`. Await asynchronous driver operations and assert observed results against the values in the scenarios. A missing definition is an integration issue to resolve before judging product behaviour.

Keep the feature paths and support-file imports explicit in the project's Cucumber command or configuration. Give the user a repeatable focused command and the corresponding broader verification command. A dry run checks wiring; an executed assertion establishes a behavioural result. Check the report's scenario counts, statuses and filters before describing coverage as passing. [Configuration reference](https://github.com/cucumber/cucumber-js/blob/v13.3.0/docs/configuration.md)

## Own the scenario lifecycle

Keep scenario-specific drivers, entity IDs and observations in Cucumber's World. Each scenario receives its own instance. Use regular functions when accessing it through `this`, as the shop's steps demonstrate. Isolate external application data as well as test state. [World reference](https://github.com/cucumber/cucumber-js/blob/v13.3.0/docs/support_files/world.md)

Use Cucumber `Before` and `After` hooks for per-scenario setup and cleanup. Shared resources can use `BeforeAll` and `AfterAll`; account for their worker scope when running in parallel. Extract reusable setup from other test suites into ordinary helpers if needed, then call it through these hooks. Capture failure evidence before closing the resources needed to collect it. [Hooks reference](https://github.com/cucumber/cucumber-js/blob/v13.3.0/docs/support_files/hooks.md)

## Exercise the chosen interface

- A direct driver calls the actual application operation and returns observations. The shop example uses this approach.
- An HTTP driver submits requests and reads outcomes from the running application or its supported request-injection interface. Configure the target and identities through the test environment.
- A browser driver uses Playwright to navigate the configured base URL, interact through stable locators and observe the page. Use a fresh browser context for each scenario. Cucumber owns execution, hooks and scenario state when Playwright is used as a library. Configure browser cleanup, screenshots and traces through that lifecycle. Use condition-based waits for visible outcomes. [Playwright library guidance](https://playwright.dev/docs/library)

Choose the interface from the promised behaviour and any explicit user requirement. Describe which interface was exercised in the result so a reader can understand what the run establishes.

## Keep feedback useful

Reuse expensive infrastructure safely across independent scenarios while resetting their data. Use bounded waits for asynchronous completion and start parallel workers only when fixtures and resources support them. Record setup and execution time separately when assessing speed. Save reports locally or as CI artifacts according to project conventions, keeping sensitive observations appropriately redacted. Include scenario results and failure evidence in the review.
