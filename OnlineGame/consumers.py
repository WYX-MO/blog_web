import json
from channels.generic.websocket import AsyncWebsocketConsumer

# 存储房间信息：{房间名: {玩家1: 出拳, 玩家2: 出拳, 玩家数: 2}}
room_data = {}

class RPSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 获取房间名和当前用户（简化：用随机标识，无需登录）
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'rps_{self.room_name}'
        self.user_id = self.scope['session'].session_key or str(self.channel_name)[:8]

        # 加入房间组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # 初始化房间数据
        if self.room_name not in room_data:
            room_data[self.room_name] = {'players': {}, 'player_count': 0}
        room = room_data[self.room_name]

        # 玩家加入房间（限制最多2人）
        if room['player_count'] < 2:
            room['players'][self.user_id] = None  # 初始出拳为 None
            room['player_count'] += 1
            # 通知房间内所有玩家：新玩家加入
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_update',
                    'message': f'玩家{self.user_id[:4]}加入房间',
                    'player_count': room['player_count'],
                    'players': list(room['players'].keys())
                }
            )
        else:
            # 房间已满，拒绝连接
            await self.send(text_data=json.dumps({
                'error': '房间已满，无法加入！'
            }))
            await self.close()

    async def disconnect(self, close_code):
        # 离开房间组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # 清理房间数据
        if self.room_name in room_data:
            room = room_data[self.room_name]
            if self.user_id in room['players']:
                del room['players'][self.user_id]
                room['player_count'] -= 1
                # 通知其他玩家：有人离开
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'room_update',
                        'message': f'玩家{self.user_id[:4]}离开房间',
                        'player_count': room['player_count'],
                        'players': list(room['players'].keys())
                    }
                )
            # 房间无玩家时删除
            if room['player_count'] == 0:
                del room_data[self.room_name]

    # 接收前端发送的出拳消息
    async def receive(self, text_data):
        data = json.loads(text_data)
        choice = data.get('choice')  # rock/paper/scissors
        room = room_data.get(self.room_name)

        if not room or self.user_id not in room['players']:
            await self.send(text_data=json.dumps({'error': '无效房间或玩家！'}))
            return

        # 记录玩家出拳
        room['players'][self.user_id] = choice
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_choice',
                'user_id': self.user_id[:4],  # 简化显示玩家ID
                'choice': choice
            }
        )

        # 双方都出拳后，判定胜负
        choices = [v for v in room['players'].values() if v is not None]
        if len(choices) == 2:
            player1_id, player2_id = list(room['players'].keys())
            player1_choice = room['players'][player1_id]
            player2_choice = room['players'][player2_id]
            result = self.judge_winner(player1_choice, player2_choice)
            
            # 通知所有玩家结果
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_result',
                    'result': result,
                    'player1': {'id': player1_id[:4], 'choice': player1_choice},
                    'player2': {'id': player2_id[:4], 'choice': player2_choice}
                }
            )
            # 重置出拳状态，准备下一轮
            room['players'][player1_id] = None
            room['players'][player2_id] = None

    # 房间更新消息处理
    async def room_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'room_update',
            'message': event['message'],
            'player_count': event['player_count'],
            'players': event['players']
        }))

    # 玩家出拳消息处理
    async def player_choice(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_choice',
            'user_id': event['user_id'],
            'choice': event['choice']
        }))

    # 游戏结果消息处理
    async def game_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_result',
            'result': event['result'],
            'player1': event['player1'],
            'player2': event['player2']
        }))

    # 胜负判定逻辑
    @staticmethod
    def judge_winner(choice1, choice2):
        if choice1 == choice2:
            return '平局！'
        win_conditions = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }
        if win_conditions[choice1] == choice2:
            return f'玩家1（{choice1}）战胜玩家2（{choice2}）！'
        else:
            return f'玩家2（{choice2}）战胜玩家1（{choice1}）！'