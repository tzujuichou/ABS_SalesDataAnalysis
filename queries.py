QUERIES = {
    'unique_suppliers': '''
        SELECT COUNT(DISTINCT ds.supplier)
        FROM dim_supplier ds
        JOIN fact_transaction ft USING (supplier_id)
        JOIN dim_date dd USING (date_id)
        WHERE dd.year = 2019
    ''',

    'unique_item_types': """
        SELECT DISTINCT di.item_type 
        FROM dim_item di
        JOIN fact_transaction ft USING(item_id)
        JOIN dim_date dd USING (date_id)
        WHERE dd.year = 2019
    """,

    'total_retail_sales': '''
        SELECT SUM(retail_sales) as total_retail_sales FROM fact_transaction ft
        JOIN dim_date dd USING (date_id)
        WHERE dd.year = 2019
    ''',

    'total_warehouse_sales': '''
        SELECT SUM(warehouse_sales) as total_warehouse_sales FROM fact_transaction ft
        JOIN dim_date dd USING (date_id)
        WHERE dd.year = 2019
    ''',

    'total_retail_transfers':'''
        SELECT SUM(retail_transfers) as total_retail_transfers FROM fact_transaction ft
        JOIN dim_date dd USING (date_id)
        WHERE dd.year = 2019
    ''',

    'overtime_sales': '''
        SELECT CONCAT(dd.year, '-', LPAD(dd.month::text, 2, '0')) as time, 
               dd.quarter,
               SUM(ft.retail_sales) as retail_sales,
               SUM(ft.retail_transfers) as retail_transfers, 
               SUM(ft.warehouse_sales) as warehouse_sales
        FROM public.fact_transaction ft
        JOIN public.dim_date dd USING (date_id)
        WHERE dd.year = 2019
        GROUP BY dd.year, dd.month, dd.quarter
        ORDER BY time;
    ''',

    'time_scope':'''
        SELECT
            d.year,
            d.month
        FROM dim_date d
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    ''',

    'supplierContribution':'''
        WITH CTE AS (
        SELECT
            ds.supplier,
            SUM(ft.retail_sales + ft.warehouse_sales) AS total_sales
        FROM
            public.fact_transaction ft
            JOIN public.dim_supplier ds ON ft.supplier_id = ds.supplier_id
            JOIN public.dim_date dd ON ft.date_id = dd.date_id
        WHERE
            dd.year = 2019
        GROUP BY
            ds.supplier
        )
        SELECT supplier, total_sales, 
            (total_sales/SUM(total_sales) OVER ()) * 100 as percentage_as_a_whole,
            ((SUM(total_sales) OVER (ORDER BY total_sales DESC))/(SUM(total_sales) OVER())) * 100 as rolling_percentage
        FROM CTE
        ORDER BY total_sales DESC
    ''',
    'monthly_sales_by_supplier': """
        SELECT
            ds.supplier,
            dd.month,
            SUM(ft.retail_sales + ft.warehouse_sales) AS monthly_sales
        FROM
            fact_transaction ft
            JOIN dim_supplier ds USING (supplier_id)
            JOIN dim_date dd USING (date_id)
        WHERE
            dd.year = 2019
        GROUP BY
            ds.supplier, dd.month
        ORDER BY
            ds.supplier, dd.month
    """,
    'retail_analysis': """
        SELECT 
            SUM(retail_sales) retail_sales, 
            SUM(retail_transfers) as retail_transfers, 
            CONCAT(dd.year, '-', LPAD(dd.month::text, 2, '0')) as time, 
            dd.quarter, 
            di.item_type
        FROM fact_transaction ft 
        JOIN dim_date dd USING (date_id)
        JOIN dim_item di USING (item_id)
        WHERE year=2019
        GROUP BY item_type, month, quarter, year
        ORDER BY month, item_type
    """,
    'item_details_2019': """
    SELECT DISTINCT
        di.item_type,
        di.item_description
    FROM
        fact_transaction ft
        JOIN dim_item di USING (item_id)
        JOIN dim_date dd USING (date_id)
    WHERE
        dd.year = 2019
    ORDER BY
        di.item_type, di.item_description;
    """
}