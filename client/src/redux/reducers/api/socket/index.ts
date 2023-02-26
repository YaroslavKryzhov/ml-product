import Centrifuge from "centrifuge";
import { HOST } from "ducks/constants";
import { TaskObservePayload } from "ducks/reducers/types";

class SocketManager {
  private socket: Centrifuge | null = null;
  createSocket(token: string) {
    this.socket = new Centrifuge(
      `ws://${HOST}/centrifugo/connection/websocket`
    );

    this.socket.setToken(token);
    this.socket.connect();
  }
  oneTimeSubscription<T = unknown>(
    payload: TaskObservePayload,
    callback: (data: T) => void
  ) {
    if (!this.socket) this.createSocket(payload.jwt_token);

    const sub = this.socket!.subscribe(`${payload.task_id}`, (ctx) => {
      callback(ctx.data);
      sub.unsubscribe();
    });
  }
}

export const socketManager = new SocketManager();
