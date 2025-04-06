import { Camera, Engine, PostProcess, Effect, Color3 } from "@babylonjs/core";
import { fragAmbientLight } from "./fragAmbientLight";
import { App } from "../../app/app";

class AmbientLightPP {
  camera: Camera;
  engine: Engine;
  pp: PostProcess;

  constructor(camera: Camera, engine: Engine, app: App) {
    this.camera = camera;
    this.engine = engine;
    this.pp = this._ambientLightPass(app);
  }

  _ambientLightPass(app: App) {
    Effect.ShadersStore["AmbientLightFragmentShader"] = fragAmbientLight;
    const pp = new PostProcess(
      "AmbientLight Post Process",
      "AmbientLight",
      ["ambientColor"],
      [],
      1.0,
      this.camera,
      undefined,
      this.engine,
    );

    pp.onApply = (effect) => {
      effect.setColor3(
        "ambientColor",
        app.useClearColorFromPost ? app.clearColor : Color3.Black(),
      );
    };

    return pp;
  }
}

export { AmbientLightPP };
