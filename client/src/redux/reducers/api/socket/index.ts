import Centrifuge from "centrifuge";
import { HOST } from "ducks/constants";
import { TaskResponseData } from "ducks/reducers/types";
import jwtDecode from "jwt-decode";

class SocketManager {
  isCreated: boolean = false;
  private socket: Centrifuge | null = null;
  private taskCallbacks: Record<string, (data: TaskResponseData) => void> = {};
  createSocket(token: string) {
    const centrifuge = new Centrifuge(
      `ws://${HOST}/centrifugo/connection/websocket`
    );

    centrifuge.setToken(token);
    centrifuge.connect();

    const userId = (jwtDecode(token) as any).sub;
    centrifuge.subscribe(`INFO#${userId}`, (ctx) => {
      this.taskCallbacks[ctx.data.task_id]?.(ctx.data);

      delete this.taskCallbacks[ctx.data.task_id];
    });

    this.socket = centrifuge;
    this.isCreated = true;
  }
  taskSubscription(taskId: string, callback: (data: TaskResponseData) => void) {
    this.taskCallbacks[taskId] = callback;
  }
}

export const socketManager = new SocketManager();
