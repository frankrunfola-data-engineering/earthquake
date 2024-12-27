# Earthquake Data Engineering Pipeline

This project provides a robust data engineering pipeline for processing earthquake data using Azure, Databricks, and Azure Synapse Analytics. The pipeline automates data ingestion, processing, and storage into `bronze`, `silver`, and `gold` layers, preparing the data for analysis and visualization.

---

## **Business Case**

Earthquake data is vital for understanding seismic events and mitigating risks. Stakeholders such as government agencies, research institutions, and insurance companies rely on accurate, up-to-date information for:

- Planning emergency responses.
- Assessing risks.
- Making data-driven decisions.

By automating the processing and categorization of seismic data, this pipeline empowers stakeholders to predict, prepare for, and respond to earthquake events with precision and speed. This ensures timely and actionable insights that improve decision-making while saving time.

---

## **Pipeline Architecture**

1. **Azure Databricks**: For distributed data processing.
2. **Azure Data Factory**: For orchestrating data workflows.
3. **Azure Data Lake Storage**: For scalable data storage in bronze, silver, and gold containers.
4. **Azure Synapse Analytics**: For querying and analyzing processed data.
![Data Engineering vs Software Engineering (6)](https://github.com/user-attachments/assets/21f7cf7a-d022-4a80-b0f6-eb1f705c6266)

---

## **Setup Instructions**

### Prerequisites

- Set up an Azure account

### Step 1: Create Required Azure Resources

1. **Azure Databricks**:
   - Create a Databricks resource with a trial subscription.
   - Use the **Standard LTS** version.

2. **Azure Storage Account**:
   - Enable hierarchical namespaces in advanced settings.
   - Create containers: `bronze`, `silver`, `gold`.

3. **Access Permissions**:
   - Assign the `Storage Blob Data Contributor` role to Databricks' managed identity.

---

### Step 2: Set Up Databricks

1. Launch Databricks workspace.
2. Configure the compute cluster.
3. Set up storage credentials and external locations for `bronze`, `silver`, and `gold` containers.
4. Create notebooks for each stage:
   - `bronze`: Raw data ingestion.
   - `silver`: Data cleansing and transformation.
   - `gold`: Aggregated and ready-to-query data.

#### Key Vault vs. One-Time Access Keys

While Azure Key Vault enhances security by centralizing and encrypting secrets, it can introduce complexity and potential points of failure if misconfigured. Using a one-time access key avoids this complexity but risks exposure if the key is stored insecurely. For production systems, Key Vault is preferred as it:
- Simplifies secret rotation.
- Reduces exposure to hardcoded secrets.
- Centralizes access control.

However, for one-time configurations in small-scale or personal projects, securely managing a one-time key may be simpler.

Refer to the uploaded notebooks:
- [Bronze Notebook](./Bronze%20Notebook.ipynb)
- [Silver Notebook](./Silver%20Notebook.ipynb)
- [Gold Notebook](./Gold%20Notebook.ipynb)

#### **Before and After Schema**

![ER_Diagram](https://github.com/user-attachments/assets/c6ea0240-db77-48fb-baf9-ca3c0fc08298)

##### **Bronze Layer (Raw Data)**
- **Description**: Contains raw earthquake data as ingested from the source. No transformations are applied.
- **Schema**:
  | Column Name        | Data Type   | Description                                    |
  |--------------------|-------------|------------------------------------------------|
  | id                 | String      | Unique identifier for the earthquake event.   |
  | time               | Timestamp   | Timestamp of the event.                       |
  | latitude           | Float       | Latitude of the earthquake's epicenter.       |
  | longitude          | Float       | Longitude of the earthquake's epicenter.      |
  | depth              | Float       | Depth of the earthquake in kilometers.        |
  | magnitude          | Float       | Magnitude of the earthquake.                  |
  | place              | String      | Description of the location.                  |
  | status             | String      | Status of the event (e.g., reviewed, automatic). |
  | alert              | String      | Alert level issued (if any).                  |

---

##### **Silver Layer (Cleansed and Transformed Data)**
- **Description**: Cleansed and partially transformed data. Invalid or incomplete records are removed, and key fields are standardized.
- **Schema**:
  | Column Name        | Data Type   | Description                                    |
  |--------------------|-------------|------------------------------------------------|
  | id                 | String      | Unique identifier for the earthquake event.   |
  | time               | DateTime    | Converted to ISO 8601 format.                 |
  | latitude           | Float       | Latitude of the earthquake's epicenter.       |
  | longitude          | Float       | Longitude of the earthquake's epicenter.      |
  | depth              | Float       | Depth of the earthquake in kilometers.        |
  | magnitude          | Float       | Magnitude of the earthquake.                  |
  | magnitude_category | String      | Categorized as low, medium, or high.          |
  | country_code       | String      | ISO country code based on geolocation.        |
  | place              | String      | Standardized location description.            |

---

##### **Gold Layer (Aggregated and Enriched Data)**
- **Description**: Aggregated and enriched data ready for analysis and visualization. Includes counts and averages by country and severity.
- **Schema**:
  | Column Name         | Data Type   | Description                                    |
  |---------------------|-------------|------------------------------------------------|
  | country_code        | String      | ISO country code based on geolocation.        |
  | total_earthquakes   | Integer     | Total number of earthquakes in the region.    |
  | avg_magnitude       | Float       | Average magnitude of earthquakes.             |
  | max_magnitude       | Float       | Maximum magnitude recorded.                   |
  | depth_category      | String      | Shallow (<70km), Intermediate (70-300km), or Deep (>300km). |
  | low_count           | Integer     | Count of low-magnitude earthquakes.           |
  | medium_count        | Integer     | Count of medium-magnitude earthquakes.        |
  | high_count          | Integer     | Count of high-magnitude earthquakes.          |

---

#### **Transformation Highlights**
1. **Bronze to Silver**:
   - **Data Cleansing**: Remove invalid or incomplete records.
   - **Standardization**: Format timestamps, normalize location fields, and derive country codes.
   - **Categorization**: Derive `magnitude_category` (low, medium, high).

2. **Silver to Gold**:
   - **Aggregation**: Group data by `country_code` and summarize key metrics.
   - **Enrichment**: Calculate derived metrics such as average and maximum magnitude.
   - **Additional Insights**: Categorize depths into `shallow`, `intermediate`, and `deep`.

---

### Step 3: Integrate with Azure Data Factory

1. Create a new Azure Data Factory resource.
2. Set up pipelines to orchestrate the Databricks notebooks.
3. Pass parameters such as `start_date` and `end_date` to dynamically filter data.
4. Test and debug the pipeline, then schedule it for automated runs.

---

### Step 4: Optimize Processing

- Replace Python UDFs with vectorized operations or precomputed lookup tables for better performance in distributed environments.
- Use cluster-level libraries for consistent environments.

---

### Step 5: Query Processed Data in Azure Synapse Analytics

1. Create a Synapse workspace and link it to the storage account.
2. Use serverless SQL pools to query data from the `gold` layer.
3. Optimize queries with indexing, caching, and partitioning.

Sample Query:
```sql
SELECT
    country_code,
    COUNT(CASE WHEN LOWER(sig_class) = 'low' THEN 1 END) AS low_count,
    COUNT(CASE WHEN LOWER(sig_class) IN ('medium', 'moderate') THEN 1 END) AS medium_count,
    COUNT(CASE WHEN LOWER(sig_class) = 'high' THEN 1 END) AS high_count
FROM
    OPENROWSET(
        BULK 'https://<storage_account>.dfs.core.windows.net/gold/earthquake_events_gold/**',
        FORMAT = 'PARQUET'
    ) AS [result]
GROUP BY
    country_code;
```

---

### Step 6: Optional Visualization with Power BI

- Connect Power BI to Synapse Analytics for creating interactive dashboards.

---

## **Key Benefits**

1. **Scalability**: Handles large datasets efficiently.
2. **Performance**: Optimized for distributed processing and analytics.
3. **Automation**: End-to-end orchestration reduces manual intervention.
4. **Integration**: Seamlessly connects Azure services for a cohesive workflow.

---

## **Future Enhancements**

- Incorporate real-time data ingestion.
- Add ML models for earthquake prediction.
- Extend visualization capabilities with Power BI or Tableau.

---

## **References**

- [Pathfinder Analytics Databricks Tutorial](https://www.youtube.com/watch?v=kRfNXFh9T3U&ab_channel=PathfinderAnalytics)
- Azure Documentation for [Databricks](https://learn.microsoft.com/en-us/azure/databricks/) and [Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/)

---

Happy Engineering!
