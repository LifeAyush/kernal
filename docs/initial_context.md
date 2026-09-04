## Technical Summary — Personal Workbench (Kernal)

We are building a **personal workbench / command terminal for managing work across multiple applications**, inspired conceptually by Bloomberg Terminal.

The system should not be designed as a single-purpose automation tool. It should be a **modular platform** where each external app is integrated as an app module, and each capability inside that app is implemented as an independent workflow.

### Core Architecture

The system consists of:

* **Kernal Core**

  * Workflow execution
  * Scheduling / cron jobs
  * Shared storage
  * User context / memory
  * LLM access
  * Notifications
  * Action / approval handling

* **App Modules**

  * LinkedIn
  * GitHub
  * Gmail
  * Google Calendar
  * Jira
  * More apps later

* **Workflows**

  * Each app exposes multiple independent workflows.
  * Workflows can be scheduled, manually triggered, or eventually composed across apps.

Example naming:

`linkedin.find_people`
`linkedin.engage_posts`
`linkedin.create_content`
`github.review_prs`
`gmail.triage_inbox`
`calendar.prepare_meetings`

### First App: LinkedIn

We are intentionally starting very small with only three workflows.

#### 1. `linkedin.find_people`

Runs daily.

* Discover a larger pool of relevant LinkedIn profiles.
* Score/rank profiles using configurable relevance criteria.
* Deduplicate against people previously surfaced/contacted.
* Return the top 10 people.
* Store the result/history.
* User manually sends connection requests initially.

#### 2. `linkedin.engage_posts`

Runs daily.

* Discover relevant LinkedIn posts.
* Rank them based on relevance to the user's interests/profile.
* Select approximately 5 posts.
* Generate a contextual suggested comment for each.
* Store the recommendations/history.
* User reviews and manually comments initially.

#### 3. `linkedin.create_content`

Runs weekly.

* Identify a relevant topic based on the user's expertise, interests, recent discussions, and potentially external trends.
* Research the topic.
* Generate a LinkedIn post.
* Generate an accompanying carousel/slide deck.
* Store generated assets.
* User reviews and manually publishes.

### Important Design Principle

**Apps and workflows must be decoupled from the underlying execution infrastructure.**

A workflow should mostly define:

`input → discovery/data → processing → ranking/reasoning → output → optional action`

For example:

`discover candidates → enrich → score → dedupe → select top 10 → persist → notify`

LinkedIn-specific logic should live inside the LinkedIn module, while scheduling, storage, LLM access, notifications, and execution lifecycle should come from shared Workbench Core services.

### Context / Memory Layer

The platform should maintain persistent context that workflows can reuse.

Examples:

* previously discovered people
* previously contacted people
* posts already surfaced
* comments generated
* content previously published
* user interests
* topics the user writes about
* current projects
* interaction history

As more apps are added, this context becomes cross-application.

For example, a future workflow could use GitHub activity + Gmail conversations + Calendar meetings to decide what is important today.

### Action Model

The system should distinguish between:

`READ → ANALYZE → GENERATE → RECOMMEND → APPROVE → EXECUTE`

Initially, LinkedIn workflows should automate everything up to **RECOMMEND**, while the user manually performs sensitive external actions.

This keeps the architecture compatible with future fully automated or API-supported actions without coupling workflow logic to automation today.

### Initial Technical Shape

Suggested structure:

```text
kernal/
  core/
    workflows/
    scheduler/
    storage/
    context/
    llm/
    notifications/
    actions/

  apps/
    linkedin/
      discovery/
      ranking/
      generation/
      workflows/
        find_people.py
        engage_posts.py
        create_content.py

  config/
  data/
  cli/
```

The immediate objective is **not to build the entire Workbench**.

The objective is to build the minimum reusable core required to make the three LinkedIn workflows work well, while ensuring the architecture can later support GitHub, Gmail, Calendar, Jira, and cross-app workflows without major restructuring.

Long-term, the product should behave like a **personal intelligence and action layer over all of the user's work applications**:

**What should I know? → What requires attention? → What should I do? → What can the system do for me?**
