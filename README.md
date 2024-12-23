# Earthquake Data Engineering Pipeline

This project provides a robust data engineering pipeline for processing earthquake data using Azure, Databricks, and Azure Synapse Analytics. The pipeline automates data ingestion, processing, and storage into `bronze`, `silver`, and `gold` layers, making the data ready for analysis and visualization.

---

## **Business Case**

Earthquake data is vital for understanding seismic events and mitigating risks. Stakeholders such as government agencies, research institutions, and insurance companies rely on accurate, up-to-date information for:

- Planning emergency responses.
- Assessing risks.
- Making data-driven decisions.

This automated pipeline ensures stakeholders receive reliable and accessible data, improving decision-making while saving time.

---

## **Pipeline Architecture**

1. **Azure Databricks**: For distributed data processing.
2. **Azure Data Factory**: For orchestrating data workflows.
3. **Azure Data Lake Storage**: For scalable data storage in bronze, silver, and gold containers.
4. **Azure Synapse Analytics**: For querying and analyzing processed data.

---

## **Setup Instructions**

### Prerequisites

- An Azure account.
- Basic knowledge of Azure services and Databricks.

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

Refer to the uploaded notebooks:
- [Bronze Notebook](./Bronze%20Notebook.ipynb)
- [Silver Notebook](./Silver%20Notebook.ipynb)
- [Gold Notebook](./Gold%20Notebook.ipynb)

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
