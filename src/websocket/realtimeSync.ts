import { Quaternion } from "@babylonjs/core";
import { App } from "../app/app";
import { SocketInterpreter } from "./interpreter";

class RealtimeSync {
  button: HTMLElement;
  app: App;
  interpreter: SocketInterpreter;
  constructor(app: App, interpreter: SocketInterpreter) {
    this.app = app;
    this.interpreter = interpreter;

    this.button = document.getElementById("realtime-sync")!;
    this.button.addEventListener("click", () => {
      this.isEnabled = !this.isEnabled;
    });
  }

  applyTransforms(id: string, pos: number[], scale: number[], q: number[]) {
    if (!this.isEnabled) {
      this.interpreter.send(["realtime sync", 0]);
      return;
    }

    const obj = this.app.blenderId.get(id);
    if (!obj) return;

    obj.position.x = pos[0];
    obj.position.y = pos[1];
    obj.position.z = pos[2];

    obj.scaling.x = scale[0];
    obj.scaling.y = scale[1];
    obj.scaling.z = scale[2];

    if (!obj.rotationQuaternion) obj.rotationQuaternion = new Quaternion();

    obj.rotationQuaternion.w = q[0];
    obj.rotationQuaternion.x = q[1];
    obj.rotationQuaternion.y = q[2];
    obj.rotationQuaternion.z = q[3];
  }

  get isEnabled() {
    return this.button.classList.contains("is-enabled");
  }
  set isEnabled(arg: boolean) {
    if (arg && !this.isEnabled) this.enable();
    if (!arg && this.isEnabled) this.disable();
  }

  enable() {
    this.button.classList.add("is-enabled");
    this.interpreter.send("sync glb");
    this.interpreter.send(["realtime sync", 1]);
  }

  disable() {
    this.button.classList.remove("is-enabled");
    this.interpreter.send(["realtime sync", 0]);
    this.interpreter.send("sync glb");
  }
}

export { RealtimeSync };
