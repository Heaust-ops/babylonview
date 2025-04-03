import * as BABYLON from "@babylonjs/core";
import "@babylonjs/loaders";
import "./style.css";

import { App } from "./app/app";
import { Comms } from "./websocket/comms";

const comms = new Comms("ws://localhost:8000");
const app = new App(document.getElementById("babylon") as HTMLCanvasElement);

try {
  app.syncFromGlb("http://localhost:8001/scene.glb");
} catch {
  /** oh well */
}

/**
 * GLB SYNC
 */
comms.addMessageListener((msg) => {
  if (msg !== "sync glb") return;
  console.log("loading scene");
  app.syncFromGlb("http://localhost:8001/scene.glb");
});

document.getElementById("glb-sync")!.addEventListener("click", () => {
  comms.send("sync glb");
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
(window as any).scene = app.scene;
(window as any).engine = app.engine;
(window as any).BABYLON = BABYLON;
