# URL Shortner System Design
A URL shortener is an online tool that converts a long web address (URL) into a shorter, concise, and shareable link, 
commonly used to improve readability and character limitations on social media. When clicked, the shortened link instantly 
redirects the user to the original, long URL.

## 🧠 1. Understand the Problem
A URL shortener converts:
```
https://example.com/very/long/url/with/query?params=123
↓
https://short.ly/abc123
```

### Core Requirements
- Convert long URL → short URL
- Redirect short URL → original URL
- High availability & low latency
- Handle massive traffic (read-heavy)

### Optional Features
- Custom aliases (short.ly/myname)
- Expiration time
- Analytics (clicks, location, device)


## 🏗️ 2. High-Level Architecture
```
Client → API Server → Database
             ↓
         Cache (Redis)
```

### Components:
- API Layer → handles requests
- Encoding Service → generates short keys
- Database → stores mappings
- Cache → speeds up redirection


## 🔑 3. URL Shortening Logic

### Step 1: Generate Unique ID
Each URL gets a unique number:
```
1 → first URL
2 → second URL
```

### Step 2: Convert ID → Short Code (Base62)
Base62 uses:
```
[a-z][A-Z][0-9] → 62 characters
```
Example
```
125 → "cb"
```

Why Base62?
- Shorter URLs
- URL-safe characters

  
## 🧩 4. Core APIs

### 1. Create Short URL 
```
POST /shorten
Body: { long_url }
Response: { short_url }
```

### Redirect
```
GET /{short_code}
→ 302 Redirect to original URL
```


## 🗄️ 5. Database Design
Table: URL Mapping

| id | short_code | long_url | created_at | expiry |
| -- | ---------- | -------- | ---------- | ------ |

### Notes:
- id → auto-increment or distributed ID
- short_code → indexed (fast lookup)


## ⚡ 6. Optimization with Cache
Use **Redis**:

**Flow**:
1. Check cache
2. If hit → return instantly
3. If miss → fetch DB → store in cache


## 🚀 7. Handling Scale

### Problem: Millions of requests/sec
#### Solutions:
1. Read-heavy Optimization
  - Use CDN (like Cloudflare)
  - Cache popular URLs
2. Database Scaling
  - Sharding (split data across DBs)
  - Use NoSQL (like Cassandra)
3. Load Balancing
  - Distribute traffic across servers


## 🔄 8. Avoiding Collisions
Two approaches:
### Option A: Auto-increment ID (preferred)
- Always unique
- Needs distributed ID generator (e.g., Snowflake)
## Option B: Hashing (MD5/SHA)
- Risk of collisions
- Needs collision handling


## 🧮 9. Capacity Estimation (Example)
Assume:
- 100M URLs/day
- 500B total URLs in years

Storage:
- 500B × 500 bytes ≈ 250 TB

## 🔐 10. Security Considerations
- Prevent spam URLs
- Rate limiting
- Blacklist malicious domains
- HTTPS support


## 📊 11. Analytics (Optional)

Track:
- Click count
- Geo location
- Device type
Store separately in analytics DB (e.g., Apache Kafka + warehouse)


## 🔁 12. End-to-End Flow
Shortening Flow:
1. User sends long URL
2. Generate ID
3. Convert to Base62
4. Store in DB
5. Return short URL

Redirect Flow:
1. User hits short URL
2. Check cache
3. If miss → DB lookup
4. Redirect (HTTP 302)


## 🧱 13. Final Architecture (Scaled)

```
            ┌────────────┐
            │ Load Balancer │
            └──────┬─────┘
                   ↓
            ┌────────────┐
            │ API Servers │
            └──────┬─────┘
         ┌─────────┴─────────┐
         ↓                   ↓
   ┌──────────┐       ┌──────────┐
   │  Cache   │       │ Database │
   │ (Redis)  │       │ (Shard)  │
   └──────────┘       └──────────┘
```


## 💡 Key Tradeoffs

| Choice      | Pros          | Cons               |
| ----------- | ------------- | ------------------ |
| Base62 IDs  | Short, simple | Needs ID generator |
| Hashing     | No central ID | Collisions         |
| Cache-heavy | Fast          | Cache invalidation |


## 🧾 Summary

A URL shortener is:

- Write-light, read-heavy
- Needs fast redirection
- Requires efficient ID generation
- Scales via caching + sharding
  
