import * as BABYLON from "@babylonjs/core";
import "@babylonjs/loaders";
import "./style.css";

import { App } from "./app/app";
import { Comms } from "./websocket/comms";

const comms = new Comms("ws://localhost:8000");
const app = new App(document.getElementById("babylon") as HTMLCanvasElement);

comms.addMessageListener((msg) => {
  if (msg !== "sync glb") return;
  console.log("loading scene");
  app.syncFromGlb("http://localhost:8001/scene.glb");
});

/** for debug */
(window as any).comms = comms;
(window as any).app = app;
(window as any).scene = app.scene;
(window as any).engine = app.engine;
(window as any).BABYLON = BABYLON;
