# Quick-Start Config Templates
## Ready-to-Use Configuration Files for OpenClaw

---

# Configuration Templates

## Template 1: Solo User, Single Channel (Simplest)

Perfect for getting started with one messaging platform.

```json5
// config.json5 - Minimal Setup
{
  // Your AI provider
  "provider": "anthropic",
  "model": "claude-sonnet-4-20260514",
  
  // Single channel (Telegram example)
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN",
      "allowedUsers": ["your_telegram_id"]
    }
  },
  
  // Basic settings
  "persona": {
    "name": "Assistant",
    "soulPath": "./SOUL.md"
  },
  
  // Keep it simple
  "features": {
    "memory": true,
    "webSearch": true,
    "fileAccess": true
  }
}
```

---

## Template 2: Multi-Channel Personal Assistant

WhatsApp + Telegram + Discord for complete coverage.

```json5
// config.json5 - Multi-Channel Personal
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20260514",
  
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "allowedUsers": ["your_id"],
      "features": {
        "voiceMessages": true,
        "reactions": true
      }
    },
    
    "whatsapp": {
      "enabled": true,
      "phoneNumber": "YOUR_WHATSAPP_NUMBER",
      "sessionPath": "./whatsapp-session",
      "allowedNumbers": ["+1234567890"]
    },
    
    "discord": {
      "enabled": true,
      "botToken": "YOUR_DISCORD_BOT_TOKEN",
      "allowedServers": ["server_id"],
      "allowedChannels": ["channel_id"]
    }
  },
  
  "persona": {
    "name": "Jarvis",
    "soulPath": "./SOUL.md",
    "memoryPath": "./MEMORY.md"
  },
  
  "features": {
    "memory": true,
    "webSearch": true,
    "browserAutomation": true,
    "codeExecution": true,
    "fileAccess": true,
    "calendar": true
  },
  
  "routing": {
    "default": "personal",
    "rules": [
      {
        "channel": "discord",
        "server": "work_server_id",
        "agent": "work"
      }
    ]
  }
}
```

---

## Template 3: Developer Setup

Slack + GitHub + automation for engineering workflows.

```json5
// config.json5 - Developer
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20260514",
  
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-YOUR-SLACK-BOT-TOKEN",
      "appToken": "xapp-YOUR-APP-TOKEN",
      "allowedWorkspaces": ["workspace_id"],
      "mentionOnly": false
    },
    
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "allowedUsers": ["your_id"]
    }
  },
  
  "integrations": {
    "github": {
      "enabled": true,
      "token": "ghp_YOUR_GITHUB_TOKEN",
      "defaultOrg": "your-org",
      "webhooks": true
    },
    
    "linear": {
      "enabled": true,
      "apiKey": "YOUR_LINEAR_API_KEY",
      "teamId": "YOUR_TEAM_ID"
    }
  },
  
  "persona": {
    "name": "DevBot",
    "soulPath": "./souls/developer.md"
  },
  
  "features": {
    "memory": true,
    "webSearch": true,
    "codeExecution": true,
    "fileAccess": true,
    "gitOperations": true,
    "shell": {
      "enabled": true,
      "allowedCommands": ["git", "npm", "yarn", "docker", "kubectl"]
    }
  },
  
  "cron": {
    "enabled": true,
    "jobs": [
      {
        "name": "morning-standup",
        "schedule": "0 9 * * 1-5",
        "task": "Generate standup update from yesterday's commits and today's calendar"
      },
      {
        "name": "pr-review-reminder",
        "schedule": "0 14 * * 1-5",
        "task": "Check for PRs awaiting my review"
      },
      {
        "name": "dependency-check",
        "schedule": "0 10 * * 1",
        "task": "Weekly dependency vulnerability scan"
      }
    ]
  }
}
```

---

## Template 4: Family/Household Agent

Shared access with per-user routing.

```json5
// config.json5 - Family Household
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20260514",
  
  "channels": {
    "whatsapp": {
      "enabled": true,
      "phoneNumber": "FAMILY_WHATSAPP_NUMBER",
      "sessionPath": "./whatsapp-session"
    },
    
    "telegram": {
      "enabled": true,
      "botToken": "FAMILY_BOT_TOKEN"
    }
  },
  
  "users": {
    "parent1": {
      "id": "parent1_phone_or_id",
      "name": "Mom",
      "role": "admin",
      "permissions": ["all"]
    },
    "parent2": {
      "id": "parent2_phone_or_id",
      "name": "Dad",
      "role": "admin",
      "permissions": ["all"]
    },
    "child1": {
      "id": "child1_phone_or_id",
      "name": "Alex",
      "role": "member",
      "permissions": ["homework", "reminders", "general"],
      "restrictions": {
        "noFinancial": true,
        "filteredContent": true,
        "parentNotify": ["unusual_requests"]
      }
    }
  },
  
  "groups": {
    "family-chat": {
      "id": "group_id",
      "allMembers": true,
      "agent": "family-shared"
    }
  },
  
  "persona": {
    "name": "Family Helper",
    "soulPath": "./souls/family.md"
  },
  
  "features": {
    "memory": true,
    "sharedCalendar": true,
    "groceryList": true,
    "chores": true,
    "reminders": true
  },
  
  "cron": {
    "jobs": [
      {
        "name": "morning-family",
        "schedule": "0 7 * * *",
        "task": "Family morning briefing with weather, calendar, and reminders"
      },
      {
        "name": "chore-reminder",
        "schedule": "0 16 * * 1-5",
        "task": "Remind kids about today's chores"
      }
    ]
  }
}
```

---

## Template 5: Business Professional

Calendar, email, meeting prep for executives.

```json5
// config.json5 - Business Professional
{
  "provider": "anthropic",
  "model": "claude-opus-4-20260514",  // Opus for complex reasoning
  
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN",
      "allowedUsers": ["your_id"]
    },
    
    "slack": {
      "enabled": true,
      "botToken": "xoxb-YOUR-BOT-TOKEN",
      "appToken": "xapp-YOUR-APP-TOKEN"
    },
    
    "email": {
      "enabled": true,
      "provider": "gmail",
      "address": "you@company.com",
      "watchFolders": ["INBOX"],
      "autoRespond": false
    }
  },
  
  "integrations": {
    "calendar": {
      "enabled": true,
      "provider": "google",
      "calendarId": "primary",
      "readWrite": true
    },
    
    "hubspot": {
      "enabled": true,
      "apiKey": "YOUR_HUBSPOT_API_KEY",
      "portalId": "YOUR_PORTAL_ID"
    },
    
    "notion": {
      "enabled": true,
      "apiKey": "YOUR_NOTION_KEY",
      "databases": {
        "tasks": "database_id",
        "notes": "database_id"
      }
    }
  },
  
  "persona": {
    "name": "Executive Assistant",
    "soulPath": "./souls/executive-assistant.md"
  },
  
  "features": {
    "memory": true,
    "webSearch": true,
    "emailDrafting": true,
    "calendarManagement": true,
    "meetingPrep": true,
    "travelPlanning": true
  },
  
  "cron": {
    "jobs": [
      {
        "name": "morning-briefing",
        "schedule": "0 6 * * 1-5",
        "task": "Generate executive morning briefing with calendar, priorities, and overnight updates"
      },
      {
        "name": "meeting-prep",
        "schedule": "*/30 * * * *",
        "task": "Check for meetings in next 30 mins and prepare context"
      },
      {
        "name": "end-of-day",
        "schedule": "0 18 * * 1-5",
        "task": "Summarize day, flag incomplete items, preview tomorrow"
      },
      {
        "name": "weekly-review",
        "schedule": "0 17 * * 5",
        "task": "Generate weekly accomplishments and next week preview"
      }
    ]
  }
}
```

---

## Template 6: Content Creator

Social media, content calendar, audience engagement.

```json5
// config.json5 - Content Creator
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20260514",
  
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN",
      "allowedUsers": ["your_id"]
    },
    
    "discord": {
      "enabled": true,
      "botToken": "YOUR_DISCORD_BOT_TOKEN",
      "communityServer": "server_id"
    }
  },
  
  "integrations": {
    "twitter": {
      "enabled": true,
      "apiKey": "YOUR_TWITTER_API_KEY",
      "apiSecret": "YOUR_TWITTER_API_SECRET",
      "accessToken": "YOUR_ACCESS_TOKEN",
      "accessSecret": "YOUR_ACCESS_SECRET"
    },
    
    "youtube": {
      "enabled": true,
      "channelId": "YOUR_CHANNEL_ID",
      "apiKey": "YOUR_YOUTUBE_API_KEY"
    },
    
    "typefully": {
      "enabled": true,
      "apiKey": "YOUR_TYPEFULLY_KEY"
    },
    
    "notion": {
      "enabled": true,
      "apiKey": "YOUR_NOTION_KEY",
      "contentCalendar": "database_id"
    }
  },
  
  "persona": {
    "name": "Content Strategist",
    "soulPath": "./souls/content-creator.md"
  },
  
  "features": {
    "memory": true,
    "webSearch": true,
    "imageGeneration": true,
    "contentCalendar": true,
    "analytics": true
  },
  
  "cron": {
    "jobs": [
      {
        "name": "content-ideas",
        "schedule": "0 8 * * 1",
        "task": "Generate 10 content ideas based on trending topics and past performance"
      },
      {
        "name": "engagement-check",
        "schedule": "0 */3 * * *",
        "task": "Check social mentions and flag important ones for response"
      },
      {
        "name": "analytics-digest",
        "schedule": "0 9 * * 1",
        "task": "Weekly analytics summary across all platforms"
      },
      {
        "name": "schedule-reminder",
        "schedule": "0 20 * * *",
        "task": "Review tomorrow's scheduled content"
      }
    ]
  }
}
```

---

# Model Provider Configurations

## Anthropic (Claude)

```json5
{
  "provider": "anthropic",
  "apiKey": "sk-ant-YOUR_KEY",
  "models": {
    "default": "claude-sonnet-4-20260514",
    "complex": "claude-opus-4-20260514",
    "fast": "claude-haiku-3-20260307"
  },
  "settings": {
    "maxTokens": 4096,
    "temperature": 0.7
  }
}
```

## OpenAI (GPT)

```json5
{
  "provider": "openai",
  "apiKey": "sk-YOUR_OPENAI_KEY",
  "models": {
    "default": "gpt-4o",
    "complex": "gpt-4o",
    "fast": "gpt-4o-mini"
  },
  "settings": {
    "maxTokens": 4096,
    "temperature": 0.7
  }
}
```

## Google (Gemini)

```json5
{
  "provider": "google",
  "apiKey": "YOUR_GOOGLE_AI_KEY",
  "models": {
    "default": "gemini-2.0-flash",
    "complex": "gemini-2.0-pro",
    "fast": "gemini-2.0-flash"
  }
}
```

## DeepSeek

```json5
{
  "provider": "deepseek",
  "apiKey": "YOUR_DEEPSEEK_KEY",
  "baseUrl": "https://api.deepseek.com",
  "models": {
    "default": "deepseek-chat",
    "reasoning": "deepseek-reasoner"
  }
}
```

## Local (Ollama)

```json5
{
  "provider": "ollama",
  "baseUrl": "http://localhost:11434",
  "models": {
    "default": "llama3.2:latest",
    "code": "codellama:latest"
  },
  "settings": {
    "keepAlive": "5m"
  }
}
```

---

# Channel Setup Checklists

## Telegram Setup

1. **Create Bot**
   - Message @BotFather
   - Send `/newbot`
   - Choose name and username
   - Save the token

2. **Get Your User ID**
   - Message @userinfobot
   - Copy your numeric ID

3. **Configure**
   ```json5
   "telegram": {
     "botToken": "123456:ABC-DEF...",
     "allowedUsers": ["your_numeric_id"]
   }
   ```

4. **Start Chat**
   - Find your bot by username
   - Send `/start`

## WhatsApp Setup

1. **Generate Session**
   - Run `openclaw whatsapp setup`
   - Scan QR code with WhatsApp

2. **Configure**
   ```json5
   "whatsapp": {
     "sessionPath": "./whatsapp-session",
     "allowedNumbers": ["+1234567890"]
   }
   ```

## Discord Setup

1. **Create Application**
   - Go to discord.com/developers
   - New Application → Name it
   - Bot → Add Bot → Copy token

2. **Set Permissions**
   - OAuth2 → URL Generator
   - Scopes: bot, applications.commands
   - Permissions: Send Messages, Read History, Add Reactions

3. **Invite Bot**
   - Use generated URL
   - Select your server

4. **Configure**
   ```json5
   "discord": {
     "botToken": "YOUR_BOT_TOKEN",
     "allowedServers": ["server_id"]
   }
   ```

## Slack Setup

1. **Create App**
   - api.slack.com/apps → Create New App
   - From manifest or from scratch

2. **Enable Socket Mode**
   - Socket Mode → Enable
   - Generate App-Level Token (connections:write)

3. **Bot Permissions**
   - OAuth & Permissions → Bot Token Scopes
   - Add: chat:write, channels:history, im:history, users:read

4. **Install to Workspace**
   - Install App → Install to Workspace
   - Copy Bot User OAuth Token

5. **Configure**
   ```json5
   "slack": {
     "botToken": "xoxb-...",
     "appToken": "xapp-..."
   }
   ```

---

# Cron Job Templates

## Morning Briefing
```json5
{
  "name": "morning-briefing",
  "schedule": "0 6 * * *",  // 6 AM daily
  "task": "Generate morning briefing with weather, calendar, priorities, and overnight messages"
}
```

## Daily Digest
```json5
{
  "name": "daily-digest",
  "schedule": "0 20 * * *",  // 8 PM daily
  "task": "Summarize today's accomplishments, pending items, and tomorrow's preview"
}
```

## Weekly Review
```json5
{
  "name": "weekly-review",
  "schedule": "0 17 * * 5",  // Friday 5 PM
  "task": "Generate weekly review with completed tasks, wins, learnings, and next week priorities"
}
```

## Health Check
```json5
{
  "name": "system-health",
  "schedule": "*/30 * * * *",  // Every 30 minutes
  "task": "Check system health, disk space, and service status"
}
```

## Backup Reminder
```json5
{
  "name": "backup-check",
  "schedule": "0 2 * * *",  // 2 AM daily
  "task": "Verify last backup completed successfully"
}
```

## Meeting Prep
```json5
{
  "name": "meeting-prep",
  "schedule": "*/15 * * * *",  // Every 15 minutes
  "task": "Check for meetings starting in next 15 mins and prepare context"
}
```

## Content Scheduler
```json5
{
  "name": "content-reminder",
  "schedule": "0 9 * * *",  // 9 AM daily
  "task": "Review today's scheduled content and confirm ready to post"
}
```

## Inbox Zero
```json5
{
  "name": "inbox-review",
  "schedule": "0 */4 * * *",  // Every 4 hours
  "task": "Triage new emails and flag urgent items"
}
```

---

# Docker Compose Files

## Basic Deployment

```yaml
# docker-compose.yml - Basic
version: '3.8'

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    ports:
      - "3000:3000"
```

## With Redis (Recommended)

```yaml
# docker-compose.yml - With Redis
version: '3.8'

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    depends_on:
      - redis
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://redis:6379
    ports:
      - "3000:3000"

  redis:
    image: redis:alpine
    container_name: openclaw-redis
    restart: unless-stopped
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

volumes:
  redis-data:
```

## Production Setup

```yaml
# docker-compose.yml - Production
version: '3.8'

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    restart: always
    depends_on:
      - redis
    volumes:
      - ./config:/app/config:ro
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - NODE_ENV=production
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=info
    ports:
      - "127.0.0.1:3000:3000"
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:alpine
    container_name: openclaw-redis
    restart: always
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru

  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 86400 openclaw

volumes:
  redis-data:
```

---

# Security Hardening

## Production Security Config

```json5
{
  "security": {
    // Restrict to specific users
    "allowedUsers": ["user_id_1", "user_id_2"],
    
    // Rate limiting
    "rateLimit": {
      "enabled": true,
      "maxRequests": 60,
      "windowMs": 60000
    },
    
    // Command restrictions
    "shell": {
      "enabled": true,
      "allowlist": ["git", "npm", "docker"],
      "blocklist": ["rm -rf", "sudo", "curl | sh"],
      "requireConfirmation": ["docker", "kubectl"]
    },
    
    // File access restrictions
    "fileAccess": {
      "allowedPaths": ["./workspace", "./data"],
      "blockedPaths": ["/etc", "/var", "~/.ssh"],
      "maxFileSize": "10MB"
    },
    
    // Network restrictions
    "network": {
      "allowedDomains": ["api.anthropic.com", "api.openai.com"],
      "blockPrivateIPs": true
    },
    
    // Logging
    "audit": {
      "enabled": true,
      "logAllCommands": true,
      "logSensitiveActions": true,
      "retentionDays": 90
    }
  }
}
```

## Environment Variables

```bash
# .env - Production
NODE_ENV=production

# API Keys (never commit these)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Channel Tokens
TELEGRAM_BOT_TOKEN=...
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
DISCORD_BOT_TOKEN=...

# Database
REDIS_URL=redis://localhost:6379

# Security
ENCRYPTION_KEY=generate-a-32-byte-key
SESSION_SECRET=generate-a-random-string

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/openclaw/app.log
```

---

*Quick-Start Config Templates v2026.1*
*Part of The Personal Agent Revolution bonus bundle*
