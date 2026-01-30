# Architectural Decision Records (ADR)
## Movie Ticket Management System

**Project:** Movie Ticket Management System  
**Created:** January 30, 2026  
**Status:** Active  
**Technology Stack:** Python + MongoDB + FastAPI

---

## ADR 001: Backend Framework Selection

### Context
The project requires a robust backend framework that can handle concurrent user requests for ticket booking, real-time seat management, and payment processing. The framework must support async operations for I/O-heavy operations (database queries, API calls to payment gateways, email/SMS services).

### Options Considered

**Option 1: FastAPI**
- Modern Python web framework (released 2018)
- Built on Starlette (async ASGI framework)
- Automatic API documentation (Swagger/OpenAPI)
- Type hints support using Pydantic
- High performance (competes with Node.js)
- Growing ecosystem and community

**Option 2: Node.js (Express.js)**
- Mature JavaScript runtime (released 2009)
- Express: Simple, flexible web framework
- Non-blocking I/O by default
- Large ecosystem of npm packages
- JavaScript/TypeScript support
- Established in industry

**Option 3: Node.js (NestJS)**
- Full-featured TypeScript framework for Node.js
- Strongly opinionated architecture
- Built-in dependency injection
- Middleware and pipe support
- Larger learning curve
- More boilerplate code

### Decision
**FastAPI** has been selected as the backend framework.

### Rationale

1. **Performance:** FastAPI achieves near-identical performance to Node.js Express for I/O-bound operations. Benchmarks show FastAPI handling ~12,000 requests/second on standard hardware, sufficient for the project's 1000+ concurrent users requirement.

2. **Async Capabilities:** FastAPI is built on async/await at its core. Starlette provides true async support compared to Express.js which requires additional middleware for async handling. Critical for database queries, payment gateway API calls, and real-time seat locking.

3. **Type Safety:** Pydantic models provide automatic data validation and serialization. Every API request/response is validated against defined schemas, reducing runtime errors.

4. **Development Speed:** Automatic API documentation generation, built-in request validation, and type hints catch errors at development time.

5. **Ecosystem Maturity:** SQLAlchemy, Motor for async MongoDB, python-jose for JWT, Passlib for password hashing - all well-established libraries.

6. **Documentation Quality:** Comprehensive official documentation, auto-generated Swagger UI, large community support.

7. **Python Advantage:** Easier for team onboarding, extensive libraries, better code readability.

### Consequences

**Benefits:**
- ✅ Fast development and deployment
- ✅ Automatic API documentation
- ✅ Type safety catches bugs early
- ✅ Built-in async support for high performance
- ✅ Easy integration with Python ecosystem
- ✅ Smaller codebase
- ✅ Better for rapid prototyping

**Trade-offs:**
- ❌ Smaller community compared to Express.js
- ❌ Fewer third-party integrations than Node.js
- ❌ Python GIL may limit CPU-bound operations (not applicable here)
- ❌ Less suitable for real-time applications with WebSockets

**Mitigation:**
- Use Uvicorn as production ASGI server
- Implement proper async patterns throughout
- Use Celery for CPU-bound tasks if needed

---

## ADR 002: Programming Language for Backend

### Context
The backend must support async operations, have strong typing capabilities, and maintain good development velocity. Choice impacts hiring, team expertise, ecosystem access, and long-term maintainability.

### Options Considered

**Option 1: Python**
- Interpreted language with dynamic typing
- Rich ecosystem (NumPy, Pandas, TensorFlow, OpenAI SDK)
- Excellent async support (asyncio, FastAPI)
- Easy to learn and read
- Large community for backend development
- Good for rapid development

**Option 2: JavaScript/TypeScript**
- JavaScript: Dynamic, single-threaded (async via event loop)
- TypeScript: Adds optional static typing
- Node.js provides server-side runtime
- npm has largest package ecosystem
- Strong for full-stack development
- Industrial standard for web backends

**Option 3: Go**
- Compiled language with excellent performance
- Built-in concurrency with goroutines
- Fast compilation and startup
- Simple syntax
- Growing ecosystem
- Better for high-performance systems

**Option 4: Java/Spring Boot**
- Strongly typed, mature ecosystem
- Enterprise-grade reliability
- Complex setup and verbose code
- Steep learning curve
- Overkill for this project
- Slower development velocity

### Decision
**Python** has been selected as the programming language.

### Rationale

1. **Development Speed:** Python syntax is clear and concise, reducing boilerplate code. FastAPI framework minimizes repetitive code. Team can develop features 30-40% faster.

2. **Type Safety:** Python 3.9+ supports type hints (PEP 484). FastAPI uses Pydantic for automatic validation. Type checking tools (mypy) available for static analysis.

3. **Library Ecosystem:** Rich libraries for web development (FastAPI, SQLAlchemy, Pydantic). Razorpay SDK, SendGrid/Twilio, Motor for async MongoDB, python-jose, Passlib all available.

4. **Async Integration:** Native async/await syntax. FastAPI leverages asyncio. Motor provides async MongoDB driver. Httpx for async HTTP requests.

5. **AI Integration Capabilities:** Official OpenAI Python SDK. Direct integration with LLMs for future features. NumPy, Pandas, TensorFlow available for ML.

6. **Scalability:** Scales horizontally well with FastAPI + Uvicorn. Async support handles thousands of concurrent connections. Works well with Docker and load balancing.

7. **Team Expertise:** Python widely taught, easier onboarding for junior developers, faster ramp-up time.

### Consequences

**Benefits:**
- ✅ Rapid development and faster time-to-market
- ✅ Easier code maintenance and readability
- ✅ Strong async support with FastAPI
- ✅ Excellent library ecosystem
- ✅ Better for AI/ML integration
- ✅ Easier team onboarding
- ✅ Less boilerplate code

**Trade-offs:**
- ❌ Slower execution speed compared to compiled languages
- ❌ Python GIL limits true parallelism for CPU-bound tasks (not relevant for I/O-bound work)
- ❌ Slightly larger memory footprint than Go
- ❌ Smaller community than JavaScript/Node.js
- ❌ Less suitable for real-time systems

**Mitigation:**
- Use async operations for all I/O
- Use Celery task queue for CPU-intensive tasks
- Deploy with proper resource allocation
- Use PyPy if performance becomes critical

---

## ADR 003: Database Selection

### Context
The system requires persistent storage for users, movies, theaters, shows, bookings, payments, and seats. Must support complex querying, scalability, real-time updates, and ACID properties for financial transactions.

### Options Considered

**Option 1: MongoDB (NoSQL)**
- Document-oriented database
- Flexible schema (JSON-like documents)
- Horizontal scalability
- Fast reads and writes
- No strict relationships required
- Schema can evolve over time

**Option 2: PostgreSQL (Relational SQL)**
- ACID compliance guaranteed
- Strong data relationships (Foreign keys)
- Complex SQL queries and JOINs
- Mature and battle-tested
- Excellent query optimization
- Less flexible schema

**Option 3: MySQL (Relational SQL)**
- Open-source SQL database
- Simpler than PostgreSQL
- Good for structured data
- Wide hosting support
- Established industry standard
- Not as feature-rich as PostgreSQL

**Option 4: DynamoDB (AWS NoSQL)**
- Fully managed NoSQL database
- Automatic scaling
- Pay-per-request pricing
- Low latency
- Vendor lock-in
- Limited query flexibility

### Decision
**MongoDB** has been selected as the primary database.

### Rationale

1. **Data Structure Flexibility:** Movie, Show, Theater documents have varying attributes. Schema-less design allows rapid iteration without complex migrations.

2. **Relationships Not Rigid:** Bookings reference shows, users, and payments but relationships aren't complex. Denormalization acceptable for read-heavy operations.

3. **Scalability:** Horizontal scaling through sharding. Distributed architecture supports growth. Handles thousands of concurrent read/write operations.

4. **Real-time Seat Locking:** Atomic operations for seat status updates. TTL (Time-to-Live) indexes for automatic lock expiration. Fast in-place updates prevent double booking.

5. **Query Flexibility:** Aggregation pipeline for complex queries. Filter movies by multiple criteria. Group bookings by date, status, user. Geospatial queries for theater location.

6. **Development Speed:** No schema creation overhead. Documents map naturally to Python objects. Motor (async driver) integrates seamlessly with FastAPI.

7. **Payment Transaction Safety:** MongoDB 4.0+ supports multi-document ACID transactions. Ensures booking and payment consistency.

### Consequences

**Benefits:**
- ✅ Flexible schema for evolving requirements
- ✅ Horizontal scalability
- ✅ Fast read/write operations
- ✅ Natural document structure matches application objects
- ✅ Good async driver (Motor) available
- ✅ TTL indexes for automatic cleanup
- ✅ Atomic operations for seat locking
- ✅ Faster development iteration

**Trade-offs:**
- ❌ No foreign key constraints (referential integrity not enforced)
- ❌ Manual enforcement of data relationships required
- ❌ Larger storage footprint due to denormalization
- ❌ Denormalized data can become inconsistent
- ❌ Complex JOINs not possible
- ❌ Less mature than PostgreSQL
- ❌ Eventual consistency in distributed scenarios

**Mitigation:**
- Implement application-level validation for relationships
- Use transactions for booking and payment operations
- Design indexes carefully for query performance
- Monitor data consistency with periodic audits
- Implement backup and disaster recovery procedures

---

## ADR 004: Authentication Strategy

### Context
The system requires secure user authentication. Authentication strategy impacts security, scalability, session management, and user experience. Must support customer and admin roles with different permissions.

### Options Considered

**Option 1: JWT (JSON Web Tokens)**
- Stateless token-based authentication
- Token contains user information (encrypted)
- Server doesn't store session state
- Tokens included in Authorization header
- Tokens expire after set duration
- No server-side session storage needed

**Option 2: Session-based (Traditional)**
- Server stores session data (usually in Redis or database)
- User gets session ID cookie after login
- Client includes cookie in every request
- Server looks up session information
- Stateful approach
- Server maintains session storage

**Option 3: OAuth2**
- Delegated authorization using third-party provider
- User logs in with Google, GitHub, Facebook, etc.
- Provider verifies identity and returns tokens
- Application receives verified user information
- No password stored in application
- Reduces login friction

### Decision
**JWT (JSON Web Tokens)** has been selected as the primary authentication strategy.

### Rationale

1. **Stateless Architecture:** No server-side session storage required. Reduces database load. Easy horizontal scaling. No session synchronization issues across servers. Microservices-friendly design.

2. **Scalability:** Multiple backend instances can validate tokens independently. No sticky sessions required. No need for distributed session store (Redis). Reduces infrastructure complexity.

3. **Security:** Tokens signed with server secret key. Tampering detected immediately. Short expiration time (30 minutes) reduces compromise window. Refresh tokens for longer-lived sessions (7 days).

4. **Token Management:** Access Token (30 minutes) + Refresh Token (7 days). Clear expiration prevents token reuse. Token refresh flow transparent to user. Logout invalidates refresh token.

5. **Performance:** Token validation via cryptographic signature (no database lookup). Fast verification process. No additional database calls for auth check. Better API response times.

6. **Mobile & API-Friendly:** Native support for mobile applications. No cookie handling required. Works with stateless REST APIs. Easy integration with third-party services. CORS-friendly.

7. **Future Extensibility:** Can add OAuth2 as additional login method. Tokens can include user metadata. Easy to implement role-based access control (RBAC).

### Consequences

**Benefits:**
- ✅ Stateless authentication (no server-side session storage)
- ✅ Excellent scalability across multiple instances
- ✅ Fast token validation (no database lookup)
- ✅ Mobile-friendly authentication
- ✅ Reduced infrastructure complexity
- ✅ Clear token expiration and refresh mechanism
- ✅ Supports role-based access control
- ✅ Better API performance

**Trade-offs:**
- ❌ Cannot revoke token immediately (until expiration)
- ❌ Token size larger than session ID
- ❌ Token stored on client-side (XSS vulnerability risk)
- ❌ No real-time session termination across devices
- ❌ Requires HTTPS to prevent token interception
- ❌ Refresh token management adds complexity

**Mitigation:**
- Use short-lived access tokens (30 minutes)
- Store tokens in httpOnly cookies (prevent JavaScript access)
- Implement token blacklist for logout
- Use HTTPS everywhere
- Implement CSRF protection
- Monitor for suspicious token usage patterns
- Add refresh token rotation

---

## ADR 005: AI Model Selection

### Context
The project may benefit from AI/ML capabilities for movie recommendations, smart seat suggestions, dynamic pricing, and user preference analysis. AI model selection for potential future features.

### Options Considered

**Option 1: OpenAI (GPT-4, GPT-3.5-turbo)**
- State-of-the-art language models
- High accuracy and versatility
- Fine-tuning capabilities available
- Excellent documentation and SDK
- Wide industry adoption
- Higher cost per API call

**Option 2: Anthropic (Claude)**
- Advanced language model with long context window
- Strong reasoning and analysis capabilities
- Cost-effective compared to GPT-4
- Excellent for complex tasks
- Growing community
- Fewer enterprise integrations

**Option 3: Google Gemini**
- Multimodal capabilities (text, image, audio)
- Integrated with Google Cloud ecosystem
- Strong performance in various tasks
- Competitive pricing
- Growing adoption
- Less mature than OpenAI

**Option 4: Open-source LLMs (LLaMA, Mistral)**
- Self-hosted, no API dependency
- Full control over data and privacy
- Lower operational cost at scale
- Requires GPU infrastructure
- Smaller model size = less capability
- Significant engineering effort required

### Decision
**OpenAI (GPT-3.5-turbo with path to GPT-4)** has been selected.

### Rationale

1. **Industry Standard:** Most widely adopted LLM for production applications. Largest ecosystem of tools. Best documentation and community examples. Proven in billions of API calls.

2. **Capability & Quality:** GPT-3.5-turbo offers excellent balance of cost and quality. GPT-4 available for advanced features. Flexible model selection based on use case. Continuous improvements.

3. **Ease of Integration:** Official Python SDK (openai library). Simple integration with FastAPI. Excellent error handling. Works seamlessly with async operations.

4. **Cost Management:** GPT-3.5-turbo ~$0.0005 per 1K tokens (input). Suitable for high-volume operations. Token counting helps estimate costs. Cost-effective for recommendation engine.

5. **Reliability & Uptime:** 99.9% SLA for API availability. Distributed infrastructure ensures reliability. Automatic failover and redundancy. Regular maintenance with minimal downtime.

6. **Security & Privacy:** HTTPS encryption for API calls. Tokens not logged by OpenAI (with settings). SOC 2 Type II compliant. No data retention on servers (if configured).

7. **Scalability:** No infrastructure limitations. Handles unlimited concurrent requests. Automatic scaling. No database or GPU management required.

### Consequences

**Benefits:**
- ✅ Best-in-class language model quality
- ✅ Easy integration with Python/FastAPI
- ✅ No infrastructure management required
- ✅ Proven reliability and uptime
- ✅ Excellent documentation and examples
- ✅ Flexible model selection
- ✅ Strong community and support
- ✅ Regular improvements and updates

**Trade-offs:**
- ❌ Per-API-call cost (recurring expense)
- ❌ API dependency (requires internet connection)
- ❌ Rate limiting and quota restrictions
- ❌ Data sent to external servers (privacy consideration)
- ❌ Less control over model training
- ❌ Potential price increases over time

**Mitigation:**
- Implement prompt caching for repeated queries
- Monitor API usage and costs
- Implement rate limiting on application side
- Cache results for common recommendations
- Use GPT-3.5-turbo for cost optimization
- Add privacy disclaimers for data sent to OpenAI

---

## ADR 006: Voice AI Framework Selection

### Context
The project may benefit from voice AI capabilities for voice-based movie search, natural conversation for ticket purchase, and accessibility features. Framework must enable real-time voice interactions with minimal latency.

### Options Considered

**Option 1: PipeCat**
- Open-source framework for real-time voice AI
- Python-based, integrates with FastAPI
- Transport agnostic (WebRTC, HTTP, etc.)
- Supports multiple STT/LLM/TTS providers
- Community-driven development
- Smaller ecosystem

**Option 2: LiveKit**
- Real-time communication infrastructure
- Focuses on WebRTC connectivity
- Scalable architecture for multiple participants
- Good for multi-user scenarios
- Requires additional complexity for voice AI
- Good documentation

**Option 3: Vapi**
- Dedicated voice AI platform
- Managed infrastructure (no server management)
- Excellent latency and reliability
- Higher cost for production scale
- Limited customization
- Growing ecosystem

**Option 4: Retell AI**
- Voice AI focused solution
- Natural conversation capabilities
- Latency-optimized
- Good for Indian accent support
- Managed service (no infrastructure)
- Smaller ecosystem

**Option 5: Custom Implementation**
- Use STT → LLM → TTS pipeline independently
- Maximum control and customization
- Significant engineering effort required
- Potential latency issues
- Cost-effective at scale
- Requires voice technology expertise

### Decision
**PipeCat (Open-source)** with **Retell AI as managed fallback** for production.

### Rationale

1. **Integration with Python/FastAPI:** Native Python support. Works seamlessly with existing backend. No additional language learning. Async-compatible with FastAPI. Direct control over voice pipeline.

2. **Flexibility & Customization:** Can swap STT, LLM, and TTS providers freely. Not locked into single provider. Can optimize for Indian English and code-switching. Full control over conversation logic.

3. **Cost Optimization:** Open-source (no licensing cost). Pay only for STT/LLM/TTS providers. Can negotiate better rates. Potential cost savings at scale.

4. **Real-time Performance:** Pipelined architecture reduces latency. Can optimize each component independently. Direct control over buffering. Suitable for < 500ms latency requirements.

5. **Managed Service Backup:** Retell AI as fallback for production stability. Use PipeCat for development. Can migrate if custom solution becomes complex. Best of both worlds.

6. **Indian English & Code-switching:** Full control over STT provider selection. Can choose providers with Indian English support (Deepgram, Google). Custom LLM prompts for code-switching.

### Consequences

**Benefits:**
- ✅ Native Python integration
- ✅ Full customization control
- ✅ No vendor lock-in with open-source
- ✅ Flexible provider selection
- ✅ Cost-effective for custom scenarios
- ✅ Can optimize for Indian English
- ✅ Community-driven improvements
- ✅ Easier debugging with full code access

**Trade-offs:**
- ❌ Requires significant engineering effort
- ❌ Ongoing maintenance and updates
- ❌ No managed infrastructure support
- ❌ Debugging distributed voice pipeline complex
- ❌ Scalability requires careful infrastructure design
- ❌ Smaller community than commercial solutions
- ❌ Potential latency issues if not optimized
- ❌ No built-in monitoring/analytics

**Mitigation:**
- Start with simple pipeline and optimize gradually
- Use Retell AI as managed fallback for production
- Implement comprehensive monitoring and logging
- Create fallback to text-based booking if voice fails
- Document custom implementation thoroughly
- Test extensively with Indian English speakers

---

## ADR 007: STT (Speech-to-Text) Provider Selection

### Context
Accurate speech recognition is critical for voice-based movie booking. STT provider must support Indian English accent, code-switching (English-Hindi), real-time transcription with low latency, and cost-effective pricing.

### Options Considered

**Option 1: ElevenLabs**
- High-quality voice synthesis (primarily TTS)
- Recent STT capabilities added
- Limited STT accuracy data
- Higher cost model
- Better known for text-to-speech

**Option 2: Deepgram**
- Specialized STT provider
- Excellent accuracy (99%+)
- Low latency (<100ms)
- Competitive pricing
- Good Indian English support
- Real-time streaming available

**Option 3: OpenAI Whisper**
- Robust speech recognition
- Supports multiple languages
- Good Indian English handling
- Good price per minute
- Works well with code-switching
- Community-driven improvements

**Option 4: Cartesia**
- Emerging STT provider
- Real-time streaming focus
- Low latency
- Competitive pricing
- Growing Indian English support
- Smaller provider

**Option 5: Google Speech-to-Text**
- Enterprise-grade accuracy
- Multiple language support
- Good documentation
- Higher cost
- Best Indian English accent support
- HIPAA and compliance certifications

### Decision
**Deepgram** as primary with **OpenAI Whisper as fallback** for code-switching scenarios.

### Rationale

1. **Speech Recognition Accuracy:** Deepgram 99%+ accuracy on English. Handles various accents well. Good for Indian English speakers. Real-time streaming for < 100ms latency. Continuously improving model.

2. **Indian English Support:** Deepgram trained on diverse English accents. Good performance with Indian accent. Handles regional pronunciation variations. No need for extensive accent training.

3. **Code-switching Capability:** Deepgram good with English-Hindi mixing. Whisper better for complex code-switching scenarios. Use both providers in combination. Route complex queries to Whisper.

4. **Latency Requirements:** Deepgram < 100ms latency. Real-time streaming reduces waiting time. Better user experience for voice interactions. Suitable for conversational flow.

5. **Cost Efficiency:** Deepgram ~$0.0043 per minute. Volume discounts available. Lower cost than Google Speech-to-Text. Suitable for high-volume booking queries.

6. **API Integration:** REST and WebSocket APIs available. Easy integration with PipeCat. Real-time streaming support. Good error handling and documentation.

7. **Fallback Strategy:** Use OpenAI Whisper for complex code-switching. Automatically route to Whisper if confidence low. Cost-effective hybrid approach. Maintains service availability.

### Consequences

**Benefits:**
- ✅ High accuracy (99%+)
- ✅ Low latency (< 100ms)
- ✅ Good Indian English support
- ✅ Competitive pricing
- ✅ Real-time streaming
- ✅ Good code-switching support
- ✅ Reliable API
- ✅ Clear documentation

**Trade-offs:**
- ❌ Smaller provider than Google
- ❌ Less enterprise support features
- ❌ Limited HIPAA compliance
- ❌ Rate limiting on free tier
- ❌ Code-switching may need Whisper fallback
- ❌ Less established track record than Google

**Mitigation:**
- Implement Whisper as fallback for complex scenarios
- Monitor accuracy metrics continuously
- Use confidence scores to route queries
- Cache common phrases for faster recognition
- Implement retry logic with different providers

---

## ADR 008: Voice Architecture

### Context
The voice AI system requires an architecture that balances latency, debugging complexity, cost, and conversation naturalness. Two main approaches exist: Speech-to-Speech (end-to-end) vs Cascaded (STT → LLM → TTS).

### Options Considered

**Option 1: Speech-to-Speech (Direct)**
- End-to-end voice-to-voice in single operation
- Lowest end-to-end latency (200-300ms)
- Single point of failure
- Difficult to debug individual components
- Limited customization
- Best conversation naturalness
- Less visibility into processing stages

**Option 2: Cascaded (STT → LLM → TTS)**
- Modular architecture (separate components)
- Slightly higher latency (500-800ms total)
- Can debug/optimize each stage
- Component-level flexibility
- Better error visibility
- Easier to implement fallbacks
- More control over conversation flow

### Decision
**Cascaded Architecture (STT → LLM → TTS)** with optimizations for latency.

### Rationale

1. **Debugging Complexity:** Each stage produces visible outputs (text). Easy to identify which component failed. Can log STT result, LLM response, TTS generation. Simpler to test components independently.

2. **Control Flexibility:** Full control over each stage. Can optimize LLM prompt independently. Can swap STT providers without affecting TTS. Can implement custom logic between stages.

3. **Cost Implications:** Pay per component (STT, LLM, TTS). Can optimize expensive parts (usually LLM). Can use cheaper fallback providers. More granular cost tracking.

4. **Latency Optimization:** Can parallelize some operations. Use streaming for faster responses. Cache common queries and responses. Optimize LLM prompt length. Target: 800ms total latency acceptable.

5. **Conversation Naturalness:** LLM can be prompted for natural conversation. TTS with voice cloning available. Can implement interruptions and turn-taking. Better user experience possible.

6. **Fallback Mechanisms:** If STT fails, retry with different provider. If LLM times out, use template response. If TTS fails, fall back to text. Graceful degradation possible.

7. **Extensibility:** Easy to add sentiment analysis. Can implement voice emotion detection. Can add custom business logic between stages. Easy logging for future training.

### Architecture Flow
```
User speaks → STT (200ms) → LLM (300ms) → TTS (300ms) → User hears

Total Latency: ~800ms-1000ms (acceptable for booking context)
```

### Consequences

**Benefits:**
- ✅ Each component visible and debuggable
- ✅ Full customization control
- ✅ Component-level optimization possible
- ✅ Easy to implement fallbacks
- ✅ Better error handling and logging
- ✅ Easier to test components independently
- ✅ Flexible provider selection per stage
- ✅ Better for development/maintenance

**Trade-offs:**
- ❌ Slightly higher latency (~800ms vs ~300ms for Speech-to-Speech)
- ❌ Multiple API calls = higher complexity
- ❌ Higher operational cost per request
- ❌ Requires careful orchestration
- ❌ More failure points (3 vs 1)
- ❌ Requires robust error handling

**Mitigation for Latency:**
- Use streaming STT for faster recognition
- Implement prompt caching for common queries
- Use GPT-3.5-turbo instead of GPT-4
- Optimize TTS generation
- Cache frequently asked questions
- Use parallelization where possible
- Target acceptable latency: 800ms-1s

**Mitigation for Complexity:**
- Implement comprehensive logging at each stage
- Use structured error handling
- Create monitoring dashboard for latency
- Implement graceful fallbacks
- Use PipeCat framework for orchestration
- Document data flow thoroughly

---

## Decision Summary

| ADR | Topic | Decision | Status |
|-----|-------|----------|--------|
| 001 | Backend Framework | FastAPI | ✅ Accepted |
| 002 | Programming Language | Python | ✅ Accepted |
| 003 | Database | MongoDB | ✅ Accepted |
| 004 | Authentication | JWT Tokens | ✅ Accepted |
| 005 | AI Model | OpenAI GPT-3.5-turbo | ✅ Accepted |
| 006 | Voice AI Framework | PipeCat + Retell AI | ✅ Accepted |
| 007 | STT Provider | Deepgram + Whisper | ✅ Accepted |
| 008 | Voice Architecture | Cascaded (STT→LLM→TTS) | ✅ Accepted |

---

**Document Created:** January 30, 2026  
**Status:** Active & Approved  
**Last Review:** January 30, 2026  
**Next Review:** April 30, 2026

