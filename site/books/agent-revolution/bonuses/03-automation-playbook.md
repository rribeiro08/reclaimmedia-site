# The Agent Automation Playbook
## 30 Copy-Paste Automations for Your Personal AI Agent

---

# Communication Automations (1-8)

## Automation #1: Morning Briefing

Wake up to a personalized daily summary.

### Cron Configuration
```json5
{
  "name": "morning-briefing",
  "schedule": "0 6 * * *",  // 6 AM daily
  "channel": "telegram",
  "task": "morning_briefing"
}
```

### SOUL.md Addition
```markdown
## Morning Briefing Format

When generating the morning briefing, include:

### 🌤️ Today at a Glance
- Current weather and any weather alerts
- Today's calendar (meetings, deadlines)
- Top 3 priorities for today

### 📬 Overnight Updates
- Important messages received (summarize, don't list all)
- Any urgent items requiring immediate attention
- News relevant to my interests

### 🎯 Focus Recommendation
- Suggested 2-hour deep work block
- What to defer if time is limited
- One thing that would make today a win
```

### Prompt Template
```
Generate my morning briefing for [DATE].

Context available:
- Calendar: [calendar_data]
- Weather: [weather_data]
- Unread messages: [message_summary]
- Yesterday's incomplete tasks: [tasks]

Format using the Morning Briefing Format from SOUL.md.
Keep it scannable - I read this over coffee.
```

---

## Automation #2: Message Triage

Auto-categorize incoming messages by urgency.

### Cron Configuration
```json5
{
  "name": "message-triage",
  "schedule": "*/15 * * * *",  // Every 15 minutes
  "channel": "internal",
  "task": "triage_messages"
}
```

### SOUL.md Addition
```markdown
## Message Triage Rules

Categorize incoming messages as:

### 🔴 Respond Now (within 1 hour)
- Direct questions requiring decision
- Time-sensitive requests
- Messages from VIPs (boss, key clients, family)
- Anything with deadline today

### 🟡 Respond Today
- Questions that need research
- Non-urgent requests from colleagues
- Follow-ups on ongoing projects

### 🟢 Can Wait / FYI
- Newsletters and updates
- Social messages
- Non-time-sensitive information
- CC'd messages

Flag for me only the 🔴 items. Handle 🟢 silently.
```

### Prompt Template
```
Review these new messages and triage them:

[MESSAGE_LIST]

For each 🔴 urgent item, draft a quick acknowledgment.
For 🟡 items, add to my response queue.
Archive 🟢 items with a one-line summary.

VIP contacts: [VIP_LIST]
Current priorities: [PRIORITIES]
```

---

## Automation #3: Smart Reply Drafts

Pre-draft responses to common message types.

### SOUL.md Addition
```markdown
## Smart Reply Patterns

When you see these patterns, draft a response:

### Meeting Request
- Check calendar availability
- Suggest 2-3 time slots
- Include video link preference

### Status Update Request
- Pull from recent activity
- Format as bullet points
- Note any blockers

### Introduction Request
- Use warm intro template
- CC both parties
- Include relevant context for each

### Simple Questions
- Answer directly if confident
- Flag for my review if uncertain
- Include source if referencing facts
```

### Prompt Template
```
Message received:
[MESSAGE]

Sender context:
[RELATIONSHIP, LAST_INTERACTION]

Draft an appropriate response.
If meeting-related, check my calendar.
If uncertain, draft but flag for my review.

Match the sender's tone and formality level.
```

---

## Automation #4: Cross-Channel Sync

Mirror important messages between platforms.

### Configuration
```json5
{
  "name": "cross-channel-sync",
  "rules": [
    {
      "from": "slack",
      "to": "telegram",
      "conditions": ["@mentioned", "dm", "urgent_channel"]
    },
    {
      "from": "email",
      "to": "telegram",
      "conditions": ["from_vip", "subject_contains_urgent"]
    }
  ]
}
```

### SOUL.md Addition
```markdown
## Cross-Channel Sync Rules

### Always Sync to Primary (Telegram)
- Direct mentions in Slack
- Emails from VIP list
- Messages containing "urgent" or "ASAP"
- Calendar changes

### Never Sync
- Automated notifications
- Marketing emails
- Social media alerts
- Already-read items

### Sync Format
[Source] [Sender]: [Summary]
Full message available in [platform]
```

---

## Automation #5: Meeting Prep

Auto-compile context before meetings.

### Cron Configuration
```json5
{
  "name": "meeting-prep",
  "schedule": "*/15 * * * *",
  "task": "check_upcoming_meetings"
}
```

### SOUL.md Addition
```markdown
## Meeting Prep Format

15 minutes before any meeting, prepare:

### 📋 Meeting Brief
**[Meeting Title]** with [Attendees]
**Purpose:** [Extracted from invite or inferred]

### 👥 Attendee Context
For each attendee:
- Role and relationship to me
- Last interaction summary
- Current projects/priorities
- Communication style notes

### 📝 Suggested Agenda
1. [Opening/check-in]
2. [Main topics from invite]
3. [Follow-up from previous meeting]
4. [Next steps/action items]

### ❓ Questions to Ask
- [Relevant question based on context]

### ⚠️ Watch Out For
- [Any sensitivities or landmines]
```

### Prompt Template
```
Prepare me for this meeting:

Meeting: [TITLE]
Time: [START_TIME]
Attendees: [ATTENDEE_LIST]
Invite Description: [DESCRIPTION]

Previous meeting notes: [NOTES]
Recent email threads with attendees: [EMAILS]
Their recent LinkedIn/social updates: [UPDATES]

My goal for this meeting: [GOAL or infer]
```

---

## Automation #6: Follow-Up Tracker

Detect commitments and create reminders.

### SOUL.md Addition
```markdown
## Commitment Detection

Scan messages for phrases that indicate commitments:

### I Committed To
- "I'll send you..."
- "Let me get back to you..."
- "I'll have it by..."
- "I can do that"
- "Will do"

### They Committed To
- "I'll send..."
- "We'll get back to you..."
- "Expect it by..."
- "I'll follow up..."

### Create Follow-Up
For each commitment detected:
1. Extract the deliverable
2. Extract the deadline (or infer reasonable one)
3. Create reminder for day before deadline
4. Add to follow-up list
```

### Prompt Template
```
Analyze this conversation for commitments:

[CONVERSATION]

For each commitment found:
- Who made it (me or them)
- What was promised
- Deadline (explicit or inferred)
- Suggested follow-up date
- Draft follow-up message
```

---

## Automation #7: OOO Auto-Responder

Intelligent out-of-office that handles contacts differently.

### Configuration
```json5
{
  "name": "ooo-responder",
  "enabled": false,  // Toggle when away
  "start": "2026-03-01T00:00:00",
  "end": "2026-03-07T23:59:59",
  "emergencyContact": "colleague@company.com"
}
```

### SOUL.md Addition
```markdown
## OOO Response Tiers

### Tier 1: VIPs (boss, key clients, family)
- Respond immediately with personal message
- Provide emergency contact
- Offer to check in if truly urgent

### Tier 2: Colleagues
- Standard OOO with return date
- Point to coverage person
- Note response delay expectation

### Tier 3: External/Unknown
- Brief professional response
- Return date only
- No emergency contact

### Never Auto-Respond To
- Newsletters
- Automated systems
- Marketing emails
- Social media notifications
```

---

## Automation #8: Weekly Relationship Check

Identify contacts you haven't engaged with recently.

### Cron Configuration
```json5
{
  "name": "relationship-check",
  "schedule": "0 9 * * 1",  // Monday 9 AM
  "task": "check_relationships"
}
```

### SOUL.md Addition
```markdown
## Relationship Maintenance

### Key Relationships to Track
- Direct reports and manager
- Key clients and stakeholders
- Mentors and mentees
- Close friends and family

### Check-In Cadences
- Manager: Weekly minimum
- Direct reports: Weekly minimum
- Key clients: Bi-weekly
- Mentors: Monthly
- Extended family: Monthly

### Alert When
- No interaction in 2x expected cadence
- Important date approaching (birthday, work anniversary)
- Life event mentioned but not followed up
```

### Prompt Template
```
Review my communication history:

[CONTACT_LIST with last_interaction_date]

Flag anyone where:
1. Interaction gap exceeds their cadence
2. I owe them a response
3. Upcoming important date

For each flagged contact, suggest:
- Reason to reach out
- Draft message or talking points
- Suggested timing
```

---

# Productivity Automations (9-16)

## Automation #9: Web Research Pipeline

Multi-step research with synthesis.

### Prompt Template
```
Research topic: [TOPIC]

Step 1: Search for recent, authoritative sources (last 2 years preferred)
Step 2: Extract key findings from top 5 sources
Step 3: Identify areas of consensus and disagreement
Step 4: Synthesize into summary with citations

Output format:
## Executive Summary (3 sentences)

## Key Findings
- Finding 1 [source]
- Finding 2 [source]

## Different Perspectives
- View A: [summary]
- View B: [summary]

## Implications for [MY_CONTEXT]

## Sources
[Numbered list with URLs and credibility notes]

Confidence level: [high/medium/low]
```

---

## Automation #10: Content Clipper

Save and summarize content mentioned in chats.

### SOUL.md Addition
```markdown
## Content Clipping Rules

When I share a URL or mention an article/video:

### Auto-Clip
- Articles I explicitly say to save
- Resources shared by others I should review
- Reference material for current projects

### Clip Format
**Title:** [extracted]
**Source:** [domain]
**Saved:** [date]
**Summary:** [3-5 bullet points]
**Why Saved:** [context from conversation]
**Tags:** [auto-generated]

### Storage
Save to: [Notion/Obsidian/folder]
Organize by: [topic/date/project]
```

---

## Automation #11: Task Extraction

Pull action items from conversations.

### SOUL.md Addition
```markdown
## Task Detection Patterns

Identify tasks from:

### Explicit Assignments
- "Can you..." / "Could you..."
- "Please [verb]..."
- "I need you to..."
- "Your action item is..."

### Implicit Commitments
- "I should..." / "I need to..."
- "Let me..." / "I'll..."
- "We should..." (if I'm the logical owner)

### Task Format
- [ ] [Action verb] [Object] by [Deadline]
  - Context: [Conversation/source]
  - Priority: [High/Medium/Low]
  - Project: [If applicable]
```

### Prompt Template
```
Extract tasks from this conversation:

[CONVERSATION]

For each task:
1. Who owns it (me or them)
2. Clear action statement
3. Deadline (explicit or suggested)
4. Priority based on context
5. Dependencies

Output as task list, my tasks first.
```

---

## Automation #12: Daily Journal Prompt

End-of-day reflection.

### Cron Configuration
```json5
{
  "name": "journal-prompt",
  "schedule": "0 21 * * *",  // 9 PM daily
  "task": "evening_reflection"
}
```

### Prompt Template
```
Generate my evening journal prompt based on today:

What I had planned: [MORNING_PRIORITIES]
What actually happened: [CALENDAR_EVENTS, COMPLETED_TASKS]
Open items: [INCOMPLETE_TASKS]

Ask me:
1. One specific question about today's highlight
2. One question about something that didn't go as planned
3. One prompt about tomorrow's intention

Keep it conversational, not clinical.
```

---

## Automation #13: Expense Tracker

Parse receipts and purchase messages.

### SOUL.md Addition
```markdown
## Expense Tracking

### Auto-Capture From
- Bank/credit card notifications
- Receipt photos
- Purchase confirmation emails
- Subscription renewal notices

### Capture Format
| Date | Vendor | Amount | Category | Notes |
|------|--------|--------|----------|-------|

### Categories
- Business: Travel, Software, Office
- Personal: Food, Shopping, Entertainment
- Recurring: Subscriptions, Bills

### Monthly Summary
On the 1st, generate:
- Total by category
- Comparison to last month
- Unusual expenses flagged
- Subscription audit
```

---

## Automation #14: Reading List Manager

Curate and prioritize reading backlog.

### SOUL.md Addition
```markdown
## Reading List Management

### Add to List When
- I share a link with "save" or "read later"
- Someone recommends content
- I bookmark in browser

### Prioritization Factors
- Relevance to current projects (high priority)
- Time sensitivity (news vs evergreen)
- Source credibility
- Estimated read time

### Weekly Reading Digest
Sundays, suggest:
- 1 long-form piece for deep reading
- 3-5 articles for the week
- Remove stale items (>30 days old, no longer relevant)
```

---

## Automation #15: Project Status Updates

Auto-generate status from activity.

### Cron Configuration
```json5
{
  "name": "project-status",
  "schedule": "0 17 * * 5",  // Friday 5 PM
  "task": "generate_status"
}
```

### Prompt Template
```
Generate project status update:

Project: [PROJECT_NAME]
Period: [LAST_WEEK_DATES]

Data sources:
- Git commits: [COMMIT_SUMMARY]
- Completed tasks: [TASK_LIST]
- Messages/discussions: [KEY_THREADS]
- Calendar events: [MEETINGS]

Format as:

## [Project Name] Status - Week of [Date]

### Completed
- [Accomplishment with impact]

### In Progress
- [Work item] - [% complete, ETA]

### Blocked
- [Blocker] - [What's needed]

### Next Week
- [Priority 1]
- [Priority 2]

### Metrics
- [Relevant numbers]
```

---

## Automation #16: Knowledge Base Builder

Auto-index information from conversations.

### SOUL.md Addition
```markdown
## Knowledge Capture

### Auto-Index When
- I explain something to someone (I'm teaching)
- I receive explanation/answer (I'm learning)
- Decision is made with rationale
- Process or how-to is discussed

### Index Format
**Topic:** [Subject]
**Type:** [How-to / Decision / Fact / Opinion]
**Summary:** [2-3 sentences]
**Source:** [Conversation/date]
**Related:** [Other topics]
**Confidence:** [High/Medium/Low]

### Organization
Group by: Project → Topic → Type
Update existing entries rather than duplicate
Link related entries bidirectionally
```

---

# Technical Automations (17-24)

## Automation #17: Server Health Monitor

Periodic checks with alert escalation.

### Cron Configuration
```json5
{
  "name": "server-health",
  "schedule": "*/30 * * * *",
  "task": "check_server_health"
}
```

### Script Template
```bash
#!/bin/bash
# Health check script

# Disk space
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
  echo "ALERT: Disk usage at ${DISK_USAGE}%"
fi

# Memory
MEM_USAGE=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
if [ $MEM_USAGE -gt 90 ]; then
  echo "ALERT: Memory usage at ${MEM_USAGE}%"
fi

# Key services
for service in nginx postgresql redis; do
  if ! systemctl is-active --quiet $service; then
    echo "ALERT: $service is not running"
  fi
done

# Response time
RESPONSE=$(curl -o /dev/null -s -w '%{time_total}' https://myapp.com/health)
if (( $(echo "$RESPONSE > 2.0" | bc -l) )); then
  echo "ALERT: Slow response time: ${RESPONSE}s"
fi
```

### SOUL.md Addition
```markdown
## Health Alert Escalation

### Level 1: Log Only
- Disk > 70%
- Memory > 80%
- Response time > 1s

### Level 2: Notify Me
- Disk > 85%
- Memory > 90%
- Service restart detected
- Response time > 2s

### Level 3: Alert Immediately
- Disk > 95%
- Any service down
- Response time > 5s or timeout
- Error rate spike
```

---

## Automation #18: Deployment Notifier

Watch CI/CD and report results.

### SOUL.md Addition
```markdown
## Deployment Notifications

### On Deployment Start
- Note: [env] deployment started by [user]
- Link to pipeline

### On Success
- ✅ [env] deployed successfully
- Version: [tag/commit]
- Duration: [time]
- Changes: [summary]

### On Failure
- 🔴 [env] deployment FAILED
- Stage: [where it failed]
- Error: [summary]
- Last successful: [version]
- Rollback: [instructions]

### Environments
- Production: Always notify immediately
- Staging: Notify on failure only
- Dev: Log only
```

---

## Automation #19: Code Review Prep

Pre-analyze PRs before review.

### Prompt Template
```
Analyze this pull request for my review:

PR Title: [TITLE]
Author: [AUTHOR]
Files changed: [FILE_LIST]
Lines: +[ADDITIONS] -[DELETIONS]

Diff:
[DIFF_CONTENT]

Provide:

## Summary
What this PR does in 2-3 sentences

## Key Changes
- [File/area]: [What changed and why it matters]

## Review Focus Areas
1. [Most important thing to check]
2. [Second priority]
3. [Third priority]

## Potential Issues
- [Any red flags or concerns]

## Questions for Author
- [Clarifying questions]

## Testing Suggestions
- [What to test manually]
```

---

## Automation #20: Documentation Generator

Auto-generate docs from code changes.

### Prompt Template
```
Generate documentation for these code changes:

Files changed:
[FILE_LIST with diffs]

Generate:

## API Changes
[New/modified endpoints with request/response examples]

## Configuration Changes
[New environment variables or config options]

## Migration Notes
[Any data migrations or breaking changes]

## Usage Examples
[Code snippets showing new functionality]

Format for: [README / API docs / Changelog]
```

---

## Automation #21: API Monitor

Track uptime and response times.

### Cron Configuration
```json5
{
  "name": "api-monitor",
  "schedule": "*/5 * * * *",
  "endpoints": [
    {"url": "https://api.example.com/health", "expected": 200},
    {"url": "https://api.example.com/v1/users", "expected": 401}
  ]
}
```

### SOUL.md Addition
```markdown
## API Monitoring Rules

### Check Frequency
- Critical endpoints: Every 1 minute
- Standard endpoints: Every 5 minutes
- Non-critical: Every 15 minutes

### Alert Thresholds
- Response time > 2x baseline
- Status code != expected
- 3 consecutive failures

### Reporting
Daily summary at 9 AM:
- Uptime percentage
- Average response time
- Slowest endpoints
- Any incidents
```

---

## Automation #22: Log Analyzer

Periodic log review with anomaly detection.

### Cron Configuration
```json5
{
  "name": "log-analyzer",
  "schedule": "0 */6 * * *",  // Every 6 hours
  "task": "analyze_logs"
}
```

### Prompt Template
```
Analyze these log entries from the last 6 hours:

[LOG_ENTRIES]

Identify:

## Errors
- Error type: [count] occurrences
- Sample: [example]
- Impact: [assessment]

## Warnings
[Same format]

## Anomalies
- [Unusual patterns compared to baseline]

## Recommendations
- [Suggested actions]

Compare to baseline:
- Normal error rate: [X per hour]
- Current: [Y per hour]
```

---

## Automation #23: Backup Verifier

Confirm backups ran successfully.

### Cron Configuration
```json5
{
  "name": "backup-verify",
  "schedule": "0 3 * * *",  // 3 AM daily
  "task": "verify_backups"
}
```

### Script Template
```bash
#!/bin/bash
# Backup verification

BACKUP_DIR="/backups"
MAX_AGE=86400  # 24 hours in seconds

# Check latest backup exists
LATEST=$(ls -t $BACKUP_DIR/*.tar.gz 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
  echo "ALERT: No backups found"
  exit 1
fi

# Check age
AGE=$(($(date +%s) - $(stat -f %m "$LATEST")))
if [ $AGE -gt $MAX_AGE ]; then
  echo "ALERT: Latest backup is $(($AGE / 3600)) hours old"
fi

# Check size (should be > 1MB for real backup)
SIZE=$(stat -f %z "$LATEST")
if [ $SIZE -lt 1048576 ]; then
  echo "ALERT: Backup suspiciously small: $SIZE bytes"
fi

# Test integrity
if ! tar -tzf "$LATEST" > /dev/null 2>&1; then
  echo "ALERT: Backup file corrupted"
fi

echo "OK: Backup verified - $LATEST"
```

---

## Automation #24: Dependency Checker

Weekly scan for outdated packages.

### Cron Configuration
```json5
{
  "name": "dependency-check",
  "schedule": "0 10 * * 1",  // Monday 10 AM
  "task": "check_dependencies"
}
```

### Prompt Template
```
Analyze dependency report:

[npm outdated / pip list --outdated / etc. output]

Categorize updates:

## 🔴 Security Updates (Do Now)
- [package]: [current] → [latest]
  - CVE: [if applicable]
  - Risk: [assessment]

## 🟡 Major Updates (Plan)
- [package]: [current] → [latest]
  - Breaking changes: [summary]
  - Migration effort: [estimate]

## 🟢 Minor Updates (Batch)
- [package]: [current] → [latest]

## Recommended Action Plan
1. [First priority]
2. [Second priority]

Generate PR description for security updates.
```

---

# Life Automations (25-30)

## Automation #25: Grocery List Aggregator

Collect food mentions from family chats.

### SOUL.md Addition
```markdown
## Grocery Detection

### Trigger Phrases
- "We need..."
- "We're out of..."
- "Pick up..."
- "Add to list..."
- "Running low on..."
- [Photo of empty container]

### List Management
- Add items with quantity if mentioned
- Group by store section (produce, dairy, etc.)
- Remove duplicates
- Clear purchased items when confirmed

### Sharing
- Sync to shared note/app
- Send summary before shopping trip
```

---

## Automation #26: Birthday/Anniversary Reminder

Proactive gift and message suggestions.

### Cron Configuration
```json5
{
  "name": "special-dates",
  "schedule": "0 9 * * *",
  "task": "check_special_dates"
}
```

### SOUL.md Addition
```markdown
## Special Date Reminders

### Timeline
- 2 weeks before: Alert + gift suggestions
- 1 week before: Gift order reminder
- 1 day before: Message draft
- Day of: Send reminder + finalize message

### Gift Suggestions
Based on:
- Past gifts given
- Interests from conversations
- Price range by relationship
- Shipping time if ordering

### Message Templates
- Birthday: Personal + specific memory/wish
- Anniversary: Acknowledge years + highlight
- Work anniversary: Professional but warm
```

---

## Automation #27: Fitness Log

Parse workout messages into tracking.

### SOUL.md Addition
```markdown
## Workout Detection

### Trigger Recognition
- "Just finished..." / "Did..."
- Workout app shares
- Gym check-ins
- Exercise descriptions

### Data Extraction
- Type: [cardio/strength/flexibility/sport]
- Duration: [minutes]
- Intensity: [easy/moderate/hard]
- Exercises: [if strength, log sets/reps]
- Notes: [how it felt]

### Tracking
Log to: [spreadsheet/app]
Weekly summary: [totals, streaks, progress]
```

---

## Automation #28: Recipe Finder

Search based on available ingredients.

### Prompt Template
```
Find recipes using these ingredients:

Available: [INGREDIENT_LIST]
Must use: [ITEMS_EXPIRING_SOON]
Dietary restrictions: [RESTRICTIONS]
Time available: [MINUTES]
Skill level: [BEGINNER/INTERMEDIATE/ADVANCED]

Suggest 3 recipes:

## Recipe 1: [Name]
- Time: [prep + cook]
- Uses: [which ingredients from list]
- Need to buy: [missing items]
- Steps: [simplified]

[Repeat for recipes 2-3]

Include:
- One quick option (<30 min)
- One "use up ingredients" option
- One "worth the effort" option
```

---

## Automation #29: Travel Planner

Compile trip options from conversations.

### SOUL.md Addition
```markdown
## Travel Planning

### When Trip Mentioned
Capture:
- Destination
- Dates (flexible or fixed)
- Purpose (business/leisure/both)
- Companions
- Budget hints
- Preferences mentioned

### Research Package
When asked to plan:
1. Flight options (3 price points)
2. Hotel options (3 styles)
3. Ground transport
4. Key activities/restaurants
5. Packing list based on weather
6. Logistics (visa, currency, etc.)

### Booking Reminders
- Optimal booking window
- Price drop alerts
- Seat selection reminder
- Document checklist
```

---

## Automation #30: News Digest

Curated daily news based on interests.

### Cron Configuration
```json5
{
  "name": "news-digest",
  "schedule": "0 7 * * *",
  "task": "morning_news"
}
```

### SOUL.md Addition
```markdown
## News Curation

### Topic Priorities
1. [Industry/professional news]
2. [Technology relevant to work]
3. [Personal interests]
4. [Local news if relevant]
5. [World news highlights only]

### Format
## 📰 Daily Digest - [Date]

### Must Know
[1-2 stories that affect me directly]

### Industry
[3-4 relevant professional news]

### Tech
[2-3 technology updates]

### Interesting
[1-2 general interest pieces]

### Skip Today
[Ongoing stories with no new developments]

### Sources
Prefer: [trusted sources]
Avoid: [sources to skip]
Diverse perspectives on controversial topics
```

### Prompt Template
```
Generate my daily news digest.

My interests: [INTEREST_LIST]
My industry: [INDUSTRY]
Location: [CITY]
Time available: [MINUTES to read]

Sources to check: [SOURCE_LIST]
Stories to skip: [ONGOING_STORIES_ALREADY_COVERED]

Format using News Curation template.
Prioritize actionable/impactful over interesting.
Include one "palate cleanser" (positive/fun story).
```

---

# Implementation Checklist

## Before You Start
- [ ] OpenClaw installed and running
- [ ] Primary channel configured
- [ ] API keys set up
- [ ] Basic SOUL.md in place

## For Each Automation
1. [ ] Copy the configuration to config.json5
2. [ ] Add SOUL.md additions to your soul file
3. [ ] Test the prompt manually first
4. [ ] Enable the cron job
5. [ ] Monitor for first few runs
6. [ ] Adjust thresholds and prompts as needed

## Maintenance
- [ ] Weekly: Review automation logs
- [ ] Monthly: Audit which automations are useful
- [ ] Quarterly: Update prompts based on learnings
- [ ] As needed: Disable unused automations

---

*The Agent Automation Playbook v2026.1*
*Part of The Personal Agent Revolution bonus bundle*
