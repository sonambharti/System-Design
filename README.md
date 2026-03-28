# SYSTEM DESIGN
System Design is the process of planing and structuring the architecture of a software system based on user requirements. <br>
It defines how different components of the system will work together to achieve the desired functionality efficiently.  <br>
- Translates user requirements into a clear technical blueprint for developers.  <br>
- Defines system components, data flow, and interactions between services. <br>
- The goal is to create a well-organized and efficient structure that meets the intended purpose while considering factors \
  like scalability, maintainability, and performance.

## System Design in SDLC

Request Analyze  -----------------------> System Design \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|  &emsp;\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|  &emsp; \
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;v  &emsp;  \
   Maintenance  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;  Implement       \
&emsp;&ensp;&nbsp;^&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|&emsp;&emsp;\
&emsp;&emsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;|&emsp;&emsp; \
&emsp;&emsp;|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;v&emsp;&emsp;  \
   Deployment  &emsp; <-------------------------- &emsp; Testing            


## LLD vs HLD
System Design can be divided into two complementary parts.

### Low Level Design (LLD)
- Detailed class & module design <br>
- Define logic, data structures, APIs <br>
- Focus on implementation & maintainaility <br>
- Useful for Developers & engineers  <br>

#### Topics Covered in LLD
Low-Level Design focuses on the detailed implementation of each component and how it will be built. <br>

- Component/module breakdown: Detailed internal logic for each module—with class responsibilities, methods, attributes, interactions <br>
- Database schema & structure: Designing tables, keys, indexes, relationships with SQL/NoSQL refinements <br>
- API & interface definitions: Precise request/response formats, error codes, methods, endpoints, and internal interfacing <br>
- Error handling & validation logic: Define how each module manages invalid inputs, failures, edge cases, and logging <br>
- Design patterns & SOLID: Implement design patterns and solid principles to ensure clean, extensible, maintainable code <br>
- UML and pseudocode artifacts: Class diagrams, sequence diagrams, pseudocode or flowcharts to clarify logic paths and method calls <br>


### High Level Design (HLD)
- Big Picture architecture <br>
- Defines system components & interactions <br>
- Focus on scalability, performance, & reliability <br>
- Useful for architects & stakeholders <br>


#### Topics Covered in HLD
HLD focuses on defining the overall structure and architecture of the system. <br>

- **System architecture overview**: Defines the major components, modules, and how they interact (e.g., services, queues, databases) . <br>
- **Data flow and component interaction**: Illustrates how data moves between modules, along with key integrations and interfaces. <br>
- **Technology stack and infrastructure**: High-level decisions on frameworks, platforms, hardware, databases, and hosting setups. <br>
- **Module responsibilities**: Describes what each module does and how they relate to one another . <br>
- **Performance & trade-offs**: Includes design trade-offs, performance considerations, scalability, security, cost and other non-functional factors .<br>
- **Artifacts**: Commonly includes architecture diagrams, component and deployment diagrams, data flow diagrams, and possibly ER/DB schematic overviews. <br>

#### Real World Examples of HLD Decisions
- Netflix transitioned their entire backend from a monolith to microservices (starting with encoding and UI services), completing the migration by 2011 to scale rapidly during high-load events like holiday seasons. <br>
- Uber adopted an event-driven architecture where ride requests, location updates, and fare changes emit events that trigger real-time systems like driver matching, billing, and dynamic pricing. <br>
- Twitter deployed a load-balanced architecture with caching of trending topics and tweets to quickly serve millions of users and handle real-time data flows efficiently. <br>


## How to Approach System Design Questions?
When tackling system design questions in a FANG/MANG interview, follow a structured approach to demonstrate your ability to design scalable, reliable, and efficient systems. Here’s a step-by-step guide: <br>

**Step 1. Understand the Problem Statement** <br>
- **Clarify Requirements:** Start by asking questions to fully understand the problem. Determine the core requirements, constraints, and goals. <br>
- **Define Scope:** Establish what features and functionalities need to be included. Clarify any ambiguities with the interviewer. <br>

**Step 2. Design the System at a High Level** <br>
- **Outline Architecture:** Sketch a high-level architecture diagram. Identify major components such as clients, servers, databases, and APIs. <br>
- **Choose Technologies:** Select appropriate technologies and tools for each component based on scalability, reliability, and ease of maintenance. <br>

**Step 3. Dive into Detailed Design** <br>
- **Component Design:** Break down the system into smaller components. Define the responsibilities and interactions of each component. <br>
- **Data Modeling:** Design the schema for databases, specifying how data will be stored, accessed, and managed. <br>
- **APIs and Interfaces:** Specify how components will communicate with each other. Define API endpoints, data formats, and protocols. <br>

**Step 4. Consider Scalability** <br>
- **Load Handling:** Design how the system will handle increased load. Consider strategies such as load balancing, caching, and sharding. <br>
- **Vertical vs. Horizontal Scaling:** Decide between scaling up (vertical) or scaling out (horizontal) based on the needs of the system. <br>

**Step 5. Address Reliability and Fault Tolerance** <br>
- **Redundancy:** Plan for redundancy to ensure system availability in case of component failures. Consider strategies like replication and failover. <br>
- **Monitoring and Alerts:** Implement monitoring to detect and respond to issues. Set up alerts for critical failures or performance degradations. <br>

**Step 6. Discuss Trade-offs** <br>
- **Trade-offs:** Be prepared to discuss trade-offs between different design choices. For example, choosing between consistency and availability in a distributed system. <br>
- **Cost Considerations:** Address potential cost implications of your design decisions, including infrastructure and maintenance costs. <br>

**Step 7. Test and Validate** <br>
- **Simulate Usage:** Discuss how you would test the system under different scenarios. Describe methods for load testing and stress testing. <br>
- **Validation:** Ensure that the design meets all requirements and can handle real-world usage effectively. <br>

**Step 8. Communicate Clearly** <br>
- **Explain Your Design:** Clearly articulate your design choices and rationale. Use diagrams to illustrate your architecture. <br>
- **Seek Feedback:** Engage with the interviewer, asking for feedback or clarification on any points of your design. <br>