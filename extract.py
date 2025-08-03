from utils import query
from queries import QUERIES
import os  

os.makedirs('data', exist_ok=True)

print("Extracting Data for Analysis...")
# query(QUERIES['unique_suppliers']).to_parquet('data/unique_suppliers.parquet')
# query(QUERIES['unique_item_types']).to_parquet('data/unique_item_types.parquet')
# query(QUERIES['total_retail_sales']).to_parquet('data/total_retail_sales.parquet')
# query(QUERIES['total_warehouse_sales']).to_parquet('data/total_warehouse_sales.parquet')
# query(QUERIES['overtime_sales']).to_parquet('data/overtime_sales.parquet')
# query(QUERIES['total_retail_transfers']).to_parquet('data/total_retail_transfers.parquet')
# query(QUERIES['supplierContribution']).to_parquet('data/supplierContribution.parquet')
# query(QUERIES['monthly_sales_by_supplier']).to_parquet('data/monthly_sales_by_supplier.parquet')
# query(QUERIES['retail_analysis']).to_parquet('data/retail_analysis.parquet')
query(QUERIES['item_details_2019']).to_parquet('data/item_details_2019.parquet')


print("Extracting Data for Overview...")
# query(QUERIES['time_scope']).to_parquet('data/time_scope.parquet')

print('Done!')






