Designing a service for A/B Testing involves building a system that allows product teams to test different variants (A, B, C, etc.) of a feature and measure which one performs better based on user interactions.

##  ✅ What is A/B Testing?**
It’s an experiment where:
-  Users are split into groups.
-  Each group gets a different variant of a feature/page.
-  Their actions (clicks, conversions, etc.) are tracked.
-  After a period, you evaluate which variant performed best.

##  🧩 Requirements for A/B Testing Service**
**Functional Requirements:**
-  Create Experiment
-  Add Variants to Experiment
-  Assign Users randomly to variants
-  Track events per user (clicks, conversions, etc.)
-  View aggregated results for each variant
-  Support multiple experiments in parallel

**Non-Functional (not implemented in memory, but worth knowing):**
-  Scalable & real-time user assignment
-  Metrics API for dashboards
-  Low-latency routing

##  ✅ Class Design (In-Memory, Python)

```
ABTestingService
├── create_experiment(name)
├── add_variant(experiment_id, variant_name)
├── assign_user(experiment_id, user_id) → variant
├── record_event(experiment_id, user_id, event)
├── get_results(experiment_id)

Experiment
├── id
├── name
├── variants: Dict[str, Variant]
├── user_to_variant: Dict[user_id, variant_name]

Variant
├── name
├── events: Dict[event_type, count]

```
