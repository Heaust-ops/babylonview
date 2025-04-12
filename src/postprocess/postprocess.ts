import { Camera, Engine, PassPostProcess, Scene } from "@babylonjs/core";
import { AmbientLightPP } from "./ambientLight/ambientLightPP";
import { App } from "../app/app";
import { AGX } from "./tonemapping/agx";

class PostProcessManager {
  static init(scene: Scene, camera: Camera, app: App) {
    const engine = scene.getEngine() as Engine;
    const pass = new PassPostProcess("init", 1, camera);
    pass.samples = 16;
    new AmbientLightPP(camera, engine, app);
    new AGX(camera, engine, app);
  }
}

export { PostProcessManager };
