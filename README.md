# logreport
testcase workmate

- Настройка оружения:  
python -m venv venv  
source venv/script/activate #win  
source venv/bin/activate #linux  
pip install --upgrade pip  
pip install -r requirements.txt  

- Использование:  
    python main.py --file example1.log --report average --date 2025-06-22 --log_dir test/examples  
    py main.py -f "example1.log, example2.log" -r average -d 2025-06-22 -l test/examples  
    py main.py -f example1.log -f example2.log -r average -l test/examples  

- Аргументы:  
    --file/-f     Список лог-файлов, формат json (через запятую или несколько флагов)  
    --report/-r   Тип отчёта: average или count  
    --date/-d     Фильтр по дате (формат YYYY-MM-DD)  
    --log_dir/-l  Каталог с логами (по умолчанию — текущий)  
