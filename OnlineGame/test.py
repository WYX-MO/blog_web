import websocket
import threading

def on_message(ws, message):
    print(f"收到消息：{message}")

def on_error(ws, error):
    print(f"错误：{error}")

def on_close(ws, close_code, reason):
    print(f"关闭（{close_code}）：{reason}")

def on_open(ws):
    print("连接成功！")
    ws.send("测试消息")

if __name__ == "__main__":
    websocket.enableTrace(True)  # 打印详细日志
    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:8000/ws/rps/111/",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()