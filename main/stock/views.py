from django.shortcuts import render
from django.contrib.auth import get_user_model
from .simulator import simulate_trader, read_from_mongodb
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.http import JsonResponse

User= get_user_model()
simulate_trader(100,7200,10)

def user_dashboard(request):
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    trades_data = read_from_mongodb(user_id=1,type='read', timestamp=ten_minutes_ago, limit=10)
    prices = []
    timestamps = []
    
    for data in trades_data:
        prices.append(data['price'])
        timestamp = datetime.fromtimestamp(data['timestamp']).time()
        minute = str(timestamp.minute).zfill(2)  # Add leading zero if minute is a single digit
        timestamps.append(f"{timestamp.hour}:{minute}")

    
    context = {'timestamps': mark_safe(timestamps), 'prices': prices}
    return render(request, 'user_dashboard.html', context)
   
def poll(request):
    timestamp = datetime.now()
    trade = read_from_mongodb(user_id=1, type='poll',limit=1, timestamp=timestamp)
    
    if trade:
        price = trade[0]['price']
        timestamp_str = f"{datetime.fromtimestamp(trade[0]['timestamp']).time().hour}:{datetime.fromtimestamp(trade[0]['timestamp']).time().minute}"
    else:
        price = None
        timestamp_str = None
        
    return JsonResponse({'price': price, 'timestamp': mark_safe(timestamp_str)})


def admin_dashboard(request):
    colors = ['#f10075', '#00ff00', '#0000ff', '#ff00ff', '#ffff00', '#00ffff', '#ff0000', '#800080', '#008000', '#000080']
    user_data = {}
    timestamps = []
    for id in range(1,11):
        ten_minutes_ago = datetime.now() - timedelta(minutes=10)
        trades_data = read_from_mongodb(user_id=id,type='read', timestamp=ten_minutes_ago, limit=10)
        for data in trades_data:
            user_id = data.get('user')
            if user_id not in user_data:
                user_data[user_id] = {
                    'prices': [],
                    'color': colors.pop(0) if colors else None
                }
            user_data[user_id]['prices'].append(data['price'])
            # timestamp = f"{datetime.fromtimestamp(data['timestamp']).time().hour}:{datetime.fromtimestamp(data['timestamp']).time().minute}"
            timestamp_str = datetime.fromtimestamp(data['timestamp']).time()
            minute = str(timestamp_str.minute).zfill(2)  # Add leading zero if minute is a single digit
            timestamp=f"{timestamp_str.hour}:{minute}"
            if timestamp not in timestamps:
                timestamps.append(timestamp)
    print(user_data)
    context = {'user_data': user_data, 'timestamps': mark_safe(timestamps)}
    return render(request, 'admin.html', context)

