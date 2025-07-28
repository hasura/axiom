# PromptQL Build Workflow Guide

## How This Workflow Works

When you push changes to any `demos/` directory, this workflow springs into action:

1. **Detects changed demos** - Only builds what actually changed (saves time and money)
2. **Builds each demo** - Creates PromptQL builds with proper secrets and environment files
3. **Comments on your PR** - Adds a shiny comment with build links and playground URLs
4. **Notifies Slack** - Posts to the `#ci_act-axiom` channel, threading replies for the same PR
5. **Handles subsequent commits** - New commits = new builds, new comments, replies in the same Slack thread

If no demo changes are detected, the workflow skips everything and exits cleanly.

## Adding New Demo Secrets

When you add a new demo or need new secrets for an existing one, you'll need to update the `create-build.yml` workflow
in exactly three places. Miss one and your build will fail in creative ways.

### Step 1: Add to 1Password Vault

All secrets live in the **Product ACT** vault in 1Password. Create your secrets there first:

```
Vault: Product ACT
Item: axiom_[demo_name]
Fields:
  - ddn-service-account (for HASURA_DDN_PAT)
  - JWT_SECRET
  - [your database/api secrets]
```

### Step 2: Load Secrets from 1Password

Find the `Load secrets from 1Password` step (around line 30). Look for this section:

```yaml
- name: Load secrets from 1Password
  uses: 1password/load-secrets-action@v1
  with:
    export-env: true
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
    # Telco secrets
    TELCO_HASURA_DDN_PAT: "op://Product ACT/axiom_telco/ddn-service-account"
    TELCO_JWT_SECRET: "op://Product ACT/axiom_telco/JWT_SECRET"
    # AML secrets
    AML_HASURA_DDN_PAT: "op://Product ACT/axiom_aml/ddn-service-account"
    AML_JWT_SECRET: "op://Product ACT/axiom_aml/JWT_SECRET"
    # Healthcare secrets
    HEALTHCARE_HASURA_DDN_PAT: "op://Product ACT/axiom_healthcare/ddn-service-account"
    HEALTHCARE_JWT_SECRET: "op://Product ACT/axiom_healthcare/JWT_SECRET"
```

Add your secrets following the existing pattern:

```yaml
# Your new demo secrets
NEWDEMO_HASURA_DDN_PAT: "op://Product ACT/axiom_newdemo/ddn-service-account"
NEWDEMO_JWT_SECRET: "op://Product ACT/axiom_newdemo/JWT_SECRET"
NEWDEMO_DATABASE_URL: "op://Product ACT/axiom_newdemo/DATABASE_URL"
```

**Pro tip:** Use the demo name as a prefix (like `TELCO_`, `AML_`) to avoid collisions.

### Step 3: Export Secrets and Create .env.cloud File

Find the `Build all changed demos` step (around line 80). You'll need to add your demo to both switch statements in this
step:

**First switch - Export secrets:**

```yaml
case $demo in telco) export HASURA_DDN_PAT="$TELCO_HASURA_DDN_PAT" export JWT_SECRET="$TELCO_JWT_SECRET" ;;
```

**Second switch - Create .env.cloud:**

```yaml
case $demo in telco) cat > .env.cloud << EOF JWT_SECRET=$JWT_SECRET EOF ;;
```

Add your demo to both:

```yaml
newdemo) export HASURA_DDN_PAT="$NEWDEMO_HASURA_DDN_PAT" export JWT_SECRET="$NEWDEMO_JWT_SECRET" export
DATABASE_URL="$NEWDEMO_DATABASE_URL" ;;
```

```yaml
newdemo) cat > .env.cloud << EOF JWT_SECRET=$JWT_SECRET DATABASE_URL=$DATABASE_URL EOF ;;
```

## Real Example: Adding a "Finance" Demo

Let's say you're adding a finance demo with a PostgreSQL database and Redis cache:

### 1Password Setup

```
Vault: Product ACT
Item: axiom_finance
Fields:
  - ddn-service-account: [your DDN token]
  - JWT_SECRET: [your JWT secret]
  - POSTGRES_URL: [your database URL]
  - REDIS_URL: [your Redis URL]
```

### Workflow Updates

**Load secrets (Step 2):**

```yaml
# Finance secrets
FINANCE_HASURA_DDN_PAT: "op://Product ACT/axiom_finance/ddn-service-account"
FINANCE_JWT_SECRET: "op://Product ACT/axiom_finance/JWT_SECRET"
FINANCE_POSTGRES_URL: "op://Product ACT/axiom_finance/POSTGRES_URL"
FINANCE_REDIS_URL: "op://Product ACT/axiom_finance/REDIS_URL"
```

**Export in build loop (Step 3):**

```yaml
finance) export HASURA_DDN_PAT="$FINANCE_HASURA_DDN_PAT" export JWT_SECRET="$FINANCE_JWT_SECRET" export
POSTGRES_URL="$FINANCE_POSTGRES_URL" export REDIS_URL="$FINANCE_REDIS_URL" ;;
```

**Create .env.cloud (Step 4):**

```yaml
finance) cat > .env.cloud << EOF JWT_SECRET=$JWT_SECRET POSTGRES_URL=$POSTGRES_URL REDIS_URL=$REDIS_URL EOF ;;
```

## Common Gotchas

- **Naming consistency:** If you call it `FINANCE_POSTGRES_URL` in the load step, use `FINANCE_POSTGRES_URL` everywhere
- **Case sensitivity:** Demo names in the switch statements are lowercase (`finance`, not `Finance`)
- **Missing semicolons:** Each case needs `;;` at the end or the shell will hate you
- **Forgetting .env.cloud:** Your demo won't work without the environment file

## Testing Your Changes

1. Make a small change to your demo directory (add a comment to a file)
2. Push to a PR branch
3. Watch the workflow run and check for your demo in the build output
4. If it fails, you probably missed one of the places above

The workflow only builds demos that have changes, so you need to actually modify something in `demos/[your-demo]/` to
trigger a build.
