python get_3d_results.py
python find_gap_results_v2.py

taskkill /f /fi "WINDOWTITLE eq excel_*"
python excel_results.py
start excel "excel_results.xlsx"

pause