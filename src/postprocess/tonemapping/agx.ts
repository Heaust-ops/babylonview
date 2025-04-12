import { Camera, Engine, PostProcess, Effect } from "@babylonjs/core";
import { fragAgx } from "./fragAgx";
import { App } from "../../app/app";

class AGX {
  camera: Camera;
  engine: Engine;
  pp: PostProcess;
  app: App;

  constructor(camera: Camera, engine: Engine, app: App) {
    this.camera = camera;
    this.engine = engine;
    this.app = app;
    this.pp = this._AGXPass();
  }

  _AGXPass() {
    Effect.ShadersStore["TonemappingAgxFragmentShader"] = fragAgx;
    const pp = new PostProcess(
      "TonemappingAgx Post Process",
      "TonemappingAgx",
      ["toneMappingExposure", "isEnabled"],
      [],
      1.0,
      this.camera,
      undefined,
      this.engine,
    );

    pp.onApply = (e) => {
      e.setFloat("toneMappingExposure", this.app.AGXTonemappingExposure);
      e.setBool("isEnabled", this.app.useAGXTonemapping);
    };

    return pp;
  }
}

export { AGX };
