import { Camera, Engine, PassPostProcess, Scene } from "@babylonjs/core";
import { AmbientLightPP } from "./ambientLight/ambientLightPP";
import { App } from "../app/app";

class PostProcessManager {
  static init(scene: Scene, camera: Camera, app: App) {
    const engine = scene.getEngine() as Engine;
    const pass = new PassPostProcess("init", 1, camera);
    pass.samples = 16;
    new AmbientLightPP(camera, engine, app);
  }
}

export { PostProcessManager };
