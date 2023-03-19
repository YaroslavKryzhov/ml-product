import Centrifuge from "centrifuge";
import { HOST } from "ducks/constants";
import { TaskObservePayload, TaskResponseData } from "ducks/reducers/types";
import jwtDecode from "jwt-decode";

class SocketManager {
  private socket: Centrifuge | null = null;
  private taskCallbacks: Record<string, (data: TaskResponseData) => void> = {};
  private createSocket(token: string) {
    const centrifuge = new Centrifuge(
      `ws://localhost:6060/centrifugo/connection/websocket`
    );

    centrifuge.setToken(token);
    centrifuge.connect();

    const userId = (jwtDecode(token) as any).sub;
    centrifuge.subscribe(`INFO#${userId}`, (ctx) => {
      this.taskCallbacks[ctx.data.task_id]?.(ctx.data);

      delete this.taskCallbacks[ctx.data.task_id];
    });

    this.socket = centrifuge;
  }
  taskSubscription(
    payload: TaskObservePayload,
    callback: (data: TaskResponseData) => void
  ) {
    if (!this.socket) this.createSocket(payload.jwt_token);

    this.taskCallbacks[payload.task_id] = callback;
  }
}

export const socketManager = new SocketManager();
