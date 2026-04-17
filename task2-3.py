import csv
import glob
import os

DATA_DIR = './data'
OUTPUT_FILE = 'task2-3output.csv'
INPUT_FILES = [
	os.path.join(DATA_DIR, f'daily_sales_data_{i}.csv') for i in range(3)
]

output_rows = []

for file_path in INPUT_FILES:
	with open(file_path, mode='r', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['product'] == 'pink morsel':
				try:
					price = float(row['price'][1:])
					quantity = int(row['quantity'])
					sales = price * quantity
				except (ValueError, KeyError):
					print('error')
					continue
				output_rows.append({
					'sales': f'{sales:.2f}',
					'date': row['date'],
					'region': row['region']
				})

with open(OUTPUT_FILE, mode='w', newline='') as outfile:
	fieldnames = ['sales', 'date', 'region']
	writer = csv.DictWriter(outfile, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(output_rows)
