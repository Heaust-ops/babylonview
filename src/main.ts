import * as BABYLON from "@babylonjs/core";
import "@babylonjs/loaders";
import "./style.css";

import { App } from "./app/app";
import { Comms } from "./websocket/comms";
import { SocketInterpreter } from "./websocket/interpreter";

const main = async () => {
  const comms = new Comms("ws://localhost:8000");
  const app = new App(document.getElementById("babylon") as HTMLCanvasElement);

  const interpreter = new SocketInterpreter(app, comms);
  await interpreter.loadCommandsMap();
  interpreter.send("sync glb");

  document.getElementById("glb-sync")!.addEventListener("click", () => {
    interpreter.send("sync glb");
  });

  /**
   * INSPECTOR TOGGLE
   */
  let isInspector = false;
  document.getElementById("inspector-toggle")!.addEventListener("click", () => {
    if (!isInspector) {
      app.inspector.show();
      isInspector = true;
      return;
    }

    app.inspector.hide();
    isInspector = false;
  });

  app.onNewSceneObservable.add(() => {
    if (!isInspector) return;
    app.inspector.show();
  });

  /** for debug */
  (window as any).comms = comms;
  (window as any).app = app;
  (window as any).interpreter = interpreter;
  (window as any).scene = app.scene;
  (window as any).engine = app.engine;
  (window as any).BABYLON = BABYLON;
};

main();
