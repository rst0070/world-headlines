# System design
The first version of `world-headline-updater` was using connection b/w python functions and classes (with model, service and repository concepts).  
However, that kind of system design was not fit to airflow workflows.  
Thus, I'm going to organize what style would be fit to airflow workflow design in this document.  
  
## 1. My idea
I got these features of airflow by hands on experience.  
  
- Try to avoid `xcom` (data transfer system b/w tasks)
    - since it provides less space and unpretty style to access the data, not using is better
    - Making connection b/w DB and each task was common usuage to break xcom dependency, when I searched stackoverflow

## 2. Chat gpt's answer
Designing a data pipeline with Apache Airflow can be challenging, but by following some best practices and design patterns, you can build a more robust, maintainable, and scalable workflow. Here are some key suggestions:

### 1. **Modular and Reusable DAGs**
   - **Modular Design**: Break down your pipeline into smaller, modular DAGs (Directed Acyclic Graphs) that are reusable and focus on a single task or group of related tasks. This makes debugging and scaling easier.
   - **SubDAGs**: Use SubDAGs when you have repeatable workflows within a DAG. However, be cautious as they can have performance issues. Consider using TaskGroups (introduced in Airflow 2.0) as a better alternative.

### 2. **Separation of Concerns**
   - **Hooks and Operators**: Use Airflow Hooks for connections and Operators for performing specific tasks. By separating logic from orchestration, your DAGs will be cleaner and easier to maintain. Custom operators or hooks (like your SQLAlchemy-based hook) can encapsulate complex logic and improve code reuse.
   - **Avoid Logic in DAG Definitions**: Keep the DAG definition itself simple by avoiding excessive logic. Instead, move complex logic into separate Python modules or scripts.

### 3. **Task Dependencies and Flow Control**
   - **Explicit Dependencies**: Clearly define task dependencies using `set_upstream` or `set_downstream`. This makes it easier to visualize the flow and avoid cyclic dependencies.
   - **Avoid Cross-DAG Dependencies**: As much as possible, avoid having dependencies across different DAGs. Instead, use external triggers or message-based communication (e.g., via XComs or pub-sub systems) to manage interactions between DAGs.
   - **Idempotency**: Ensure tasks are idempotent (i.e., running the task multiple times yields the same result). This is crucial for handling retries or failures.

### 4. **Parallelism and Scalability**
   - **Task Parallelism**: Leverage Airflow’s parallel execution by configuring parallelism in your tasks. Define task concurrency and pools where needed to avoid resource contention.
   - **Scale Executors**: For large workflows, consider scaling out the executors (e.g., use CeleryExecutor or KubernetesExecutor) to distribute tasks efficiently across multiple workers.

### 5. **Data Passing**
   - **Use XCom Sparingly**: Airflow’s XComs allow tasks to pass small amounts of data between them. However, avoid passing large datasets this way. Instead, store data in a database or a file storage system and pass references or paths via XComs.
   - **Decouple Data and Logic**: Store intermediate data outside the Airflow environment (e.g., cloud storage, databases) to avoid bottlenecks and ensure your system is resilient to failures.

### 6. **Error Handling and Retries**
   - **Retries and Timeouts**: Set task-level retries and timeouts to handle transient issues. Use exponential backoff for retries to avoid overwhelming systems during failure.
   - **Alerting**: Implement notification systems (e.g., Slack, email) for task failures or anomalies using Airflow’s built-in alerting mechanisms.

### 7. **Version Control and Continuous Integration**
   - **DAG Versioning**: Use version control for your DAGs. You can also version your DAGs themselves to handle different workflows or data models over time.
   - **CI/CD Pipelines**: Set up continuous integration/continuous deployment (CI/CD) pipelines for testing and deploying your Airflow code. This ensures you can test DAGs in a staging environment before deploying to production.

### 8. **Environment Configuration**
   - **Dynamic Configuration**: Use Airflow Variables, Connections, or environment variables to keep your DAGs dynamic and flexible across different environments (development, staging, production).
   - **Separation of Dev/Prod Environments**: Maintain separate Airflow instances or isolated namespaces (especially with KubernetesExecutor) for development, staging, and production environments.

### 9. **Monitoring and Logging**
   - **Task Logging**: Ensure proper logging within your tasks to make troubleshooting easier. Configure Airflow to push logs to external systems (e.g., Elasticsearch, S3) if required.
   - **Monitoring DAGs**: Use Airflow’s built-in tools or external monitoring tools like Prometheus to track the performance and reliability of your DAGs.

### 10. **Security**
   - **Role-Based Access Control (RBAC)**: Use Airflow's RBAC to restrict access to sensitive DAGs or actions within your environment.
   - **Secure Connections**: Ensure that connections (like database or cloud connections) use secure methods (e.g., SSH, TLS) and store credentials securely in Airflow's connections or a secrets management service (e.g., AWS Secrets Manager).

By following these design patterns and best practices, you'll be able to create a more efficient and maintainable Airflow workflow. Let me know if you want more details on any of these suggestions!  
  
## 3. Best practices - [official doc](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## 4. Metadata in DB - chat gpt
Yes, it is quite common to store metadata used in an application within a database. Metadata typically includes descriptive information about other data (e.g., data schema, data lineage, or operational metrics), and it plays an essential role in many systems, including data pipelines, analytics platforms, and applications that deal with large-scale data management.

Here are some design principles to consider when storing metadata in a database:

### 1. **Separation of Concerns**
   - **Metadata vs. Application Data**: Keep metadata distinct from your application’s primary data. This separation ensures clarity, allowing you to manage the two types of data differently in terms of permissions, storage, and access patterns.
   - You could use a different schema or even a dedicated database for metadata.

### 2. **Schema Flexibility**
   - **Dynamic Structure**: Metadata schemas might evolve over time as the nature of data changes. Consider flexible schema designs (e.g., JSON columns in relational databases or NoSQL databases like MongoDB) for metadata that may frequently change in structure.
   - **Versioning**: Maintain a version history of metadata to track changes over time, especially when schema or data sources evolve.

### 3. **Indexing and Performance**
   - **Optimized Access**: Metadata is often queried by various applications or workflows. Index the metadata appropriately to enable fast reads based on common access patterns (e.g., searching by entity type, timestamp, or unique IDs).
   - **Batch vs. Real-time Processing**: Design your database to handle either real-time or batch processing, depending on how metadata is consumed.

### 4. **Data Lineage and Traceability**
   - **Provenance**: Capture metadata that describes the origin and transformations of the data (data lineage). This is particularly important in data pipelines, where knowing how and where data was generated and processed is critical.
   - **Auditability**: Store logs or version information for each change made to the metadata. This will help with troubleshooting and historical tracking.

### 5. **Security and Access Control**
   - **Granular Permissions**: Metadata may contain sensitive information (e.g., data ownership, access rules). Implement role-based access control (RBAC) to ensure that only authorized users can access or modify certain parts of the metadata.
   - **Encryption**: Depending on the sensitivity, encrypt metadata at rest and in transit.

### 6. **Normalization and Redundancy**
   - **Normalized Structure**: Follow good database design principles by normalizing the metadata structure to reduce redundancy, especially if there are relationships between different metadata types.
   - **Caching for Read-heavy Workloads**: For frequent access patterns, consider caching the metadata to reduce database load.

### 7. **Scalability**
   - **Horizontal Scaling**: Design for scalability, especially if the metadata grows as fast as or faster than the actual data. Use partitioning, sharding, or distributed databases if necessary.
   - **Archiving and Purging**: Implement strategies to archive or purge obsolete metadata that is no longer relevant to the application.

### 8. **Monitoring and Health Checks**
   - **Operational Metrics**: Store metadata about the system’s performance, like latency, failure rates, and uptime, to monitor the health of the application and track anomalies.
   - **Self-Descriptive Data**: Store metadata about the metadata itself (e.g., last updated timestamps, data size) to ensure that it can be validated or cleaned as needed.

By considering these principles, you can ensure that your metadata storage is efficient, maintainable, and scalable, providing a solid foundation for your application’s needs.