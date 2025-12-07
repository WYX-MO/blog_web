import json
import uuid
import time
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pusher

# 初始化 Pusher 客户端
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

# 房间数据结构：{room_name: {players: {pid: {choice: None, last_active: 时间戳}}, count: 2}}
game_rooms = {}

# 生成/获取玩家ID（后端辅助函数，可选）
def get_player_id(request, room_name):
    # 从Cookie读取玩家ID
    player_id = request.COOKIES.get(f'rps_player_{room_name}')
    if not player_id:
        # 生成8位唯一ID
        player_id = str(uuid.uuid4())[:8]
    return player_id

# 清理超时无效玩家（3分钟无活跃）
def clean_invalid_players(room_name):
    if room_name not in game_rooms:
        return
    room = game_rooms[room_name]
    current_time = time.time()
    invalid_players = []
    # 标记超时玩家
    for pid, info in room['players'].items():
        if current_time - info['last_active'] > 180:
            invalid_players.append(pid)
    # 移除超时玩家
    for pid in invalid_players:
        del room['players'][pid]
        room['count'] -= 1
        pusher_client.trigger(f'room-{room_name}', 'player-leave', {
            'player_id': pid,
            'count': room['count'],
            'msg': f'玩家{pid[:4]}超时离开'
        })
    # 清空空房间
    if room['count'] == 0:
        del game_rooms[room_name]

# 首页
def index(request):
    return render(request, 'rps/index.html')

# 游戏房间（写入玩家ID到Cookie）
def game_room(request, room_name):
    # 生成/获取玩家ID
    player_id = get_player_id(request, room_name)
    # 渲染页面并设置Cookie（有效期1天）
    response = render(request, 'rps/game_room.html', {
        'room_name': room_name,
        'player_id': player_id,
        'pusher_key': settings.PUSHER_KEY,
        'pusher_cluster': settings.PUSHER_CLUSTER
    })
    # 设置Cookie，有效期1天（86400秒）
    response.set_cookie(f'rps_player_{room_name}', player_id, max_age=86400)
    return response

# 加入房间（AJAX接口）
@csrf_exempt
def join_room(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'msg': '仅支持POST'})
    
    data = json.loads(request.body)
    room_name = data.get('room_name')
    player_id = data.get('player_id')
    
    # 清理超时玩家
    clean_invalid_players(room_name)
    
    # 初始化房间
    if room_name not in game_rooms:
        game_rooms[room_name] = {'players': {}, 'count': 0}
    room = game_rooms[room_name]
    
    # 重连：复用已有ID，更新活跃时间
    if player_id in room['players']:
        room['players'][player_id]['last_active'] = time.time()
        return JsonResponse({
            'status': 'success',
            'count': room['count'],
            'msg': f'玩家{player_id[:4]}重连成功'
        })
    # 新玩家加入（限制2人）
    elif room['count'] < 2:
        room['players'][player_id] = {
            'choice': None,
            'last_active': time.time()
        }
        room['count'] += 1
        pusher_client.trigger(f'room-{room_name}', 'player-join', {
            'player_id': player_id,
            'count': room['count'],
            'msg': f'玩家{player_id[:4]}加入房间'
        })
        return JsonResponse({
            'status': 'success',
            'count': room['count'],
            'msg': f'玩家{player_id[:4]}加入成功'
        })
    else:
        return JsonResponse({'status': 'error', 'msg': '房间已满'})

# 出拳&判定胜负（AJAX接口）
@csrf_exempt
def make_choice(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'msg': '仅支持POST'})
    
    data = json.loads(request.body)
    room_name = data.get('room_name')
    player_id = data.get('player_id')
    choice = data.get('choice')
    
    # 清理超时玩家
    clean_invalid_players(room_name)
    
    # 验证房间/玩家
    if room_name not in game_rooms:
        return JsonResponse({'status': 'error', 'msg': '房间不存在'})
    room = game_rooms[room_name]
    if player_id not in room['players']:
        return JsonResponse({'status': 'error', 'msg': '无效玩家（已超时/未加入）'})
    
    # 更新活跃时间（防止被清理）
    room['players'][player_id]['last_active'] = time.time()
    # 记录出拳
    room['players'][player_id]['choice'] = choice
    
    # 推送出拳消息
    pusher_client.trigger(f'room-{room_name}', 'player-choice', {
        'player_id': player_id,
        'choice': choice,
        'msg': f'玩家{player_id[:4]}出拳：{translate_choice(choice)}'
    })
    
    # 判定胜负（双方都出拳后）
    choices = []
    for pid, info in room['players'].items():
        if info['choice'] is not None:
            choices.append((pid, info['choice']))
    if len(choices) == 2:
        (p1_id, p1_choice), (p2_id, p2_choice) = choices
        result = judge_winner(p1_id, p1_choice, p2_id, p2_choice)
        
        # 推送结果
        pusher_client.trigger(f'room-{room_name}', 'game-result', {
            'result': result,
            'p1_id': p1_id[:4],
            'p1_choice': translate_choice(p1_choice),
            'p2_id': p2_id[:4],
            'p2_choice': translate_choice(p2_choice)
        })
        
        # 重置出拳（保留玩家ID）
        room['players'][p1_id]['choice'] = None
        room['players'][p2_id]['choice'] = None
    
    return JsonResponse({'status': 'success'})

# 辅助函数：翻译出拳
def translate_choice(choice):
    choice_map = {'rock': '石头', 'paper': '布', 'scissors': '剪刀'}
    return choice_map.get(choice, choice)

# 辅助函数：判定胜负
def judge_winner(p1_id, p1_choice, p2_id, p2_choice):
    if p1_choice == p2_choice:
        return '平局！'
    win_rules = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    if win_rules[p1_choice] == p2_choice:
        return f'玩家{p1_id[:4]}（{translate_choice(p1_choice)}）战胜玩家{p2_id[:4]}（{translate_choice(p2_choice)}）！'
    else:
        return f'玩家{p2_id[:4]}（{translate_choice(p2_choice)}）战胜玩家{p1_id[:4]}（{translate_choice(p1_choice)}）！'

# 手动清除玩家ID（可选接口）
@csrf_exempt
def clear_player_id(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        response = JsonResponse({'status': 'success', 'msg': 'ID已清除'})
        response.delete_cookie(f'rps_player_{room_name}')
        return response
    return JsonResponse({'status': 'error', 'msg': '仅支持POST'})