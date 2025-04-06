import { Color3, Color4 } from "@babylonjs/core";
import { App } from "../app/app";
import { Comms } from "./comms";

class SocketInterpreter {
  app: App;
  comms: Comms;

  socketCommandToId: Record<string, string | number>;
  socketCommandFromId: Record<string | number, string>;

  constructor(app: App, comms: Comms) {
    this.app = app;
    this.comms = comms;

    this.socketCommandToId = {};
    this.socketCommandFromId = {};

    comms.addMessageListener((msg) => {
      if (msg.startsWith("Echo")) return;
      this.interpret(JSON.parse(msg));
    });
  }

  send(commandArr: (string | number)[] | string) {
    if (typeof commandArr === "string") {
      commandArr = [commandArr];
    }

    const command = this.socketCommandToId[commandArr[0]];
    if (typeof command === "undefined") {
      console.error("malformed command");
    }

    commandArr[0] = command ?? commandArr[0];

    const serialized = JSON.stringify(commandArr);
    this.comms.send(serialized);
  }

  interpret(msg: Array<string | number> | string | number) {
    if (!(msg instanceof Array)) msg = [msg];

    const msg_rev = msg.reverse();
    const cmdId = msg_rev.pop();

    if (typeof cmdId === "undefined") {
      console.error("malformed message", msg);
      return;
    }

    const command = this.socketCommandFromId[cmdId];
    switch (command) {
      case "sync glb":
        this.app.syncFromGlb("http://localhost:8001/scene.glb");
        break;
      case "update world color":
        const colorArr = Color3.FromHexString(
          msg_rev.pop() as string,
        ).asArray();

        if (this.app.isSceneDirty()) {
          this.app.onNewSceneObservable.addOnce(() => {
            this.app.scene.clearColor = new Color4(...colorArr, 1);
          });
        } else {
          this.app.scene.clearColor = new Color4(...colorArr, 1);
        }
        break;
    }
  }

  async loadCommandsMap() {
    try {
      const response = await fetch("http://localhost:8001/commands.json");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: Record<string | number, string | number> =
        await response.json();

      const flipped: Record<string, string> = Object.fromEntries(
        Object.entries(data).map(([key, value]) => [value, key]),
      );

      this.socketCommandToId = data;
      this.socketCommandFromId = flipped;
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  }
}

export { SocketInterpreter };
