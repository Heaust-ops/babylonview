import {
  AppendSceneAsync,
  ArcRotateCamera,
  Color4,
  Engine,
  HemisphericLight,
  Scene,
  Vector3,
} from "@babylonjs/core";

class App {
  engine: Engine;
  scene: Scene;
  private canvas: HTMLCanvasElement;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.engine = new Engine(this.canvas, true);
    this.scene = new Scene(this.engine);
    this.initScene();

    this.engine.runRenderLoop(() => {
      this.scene.render();
    });

    window.addEventListener("resize", () => {
      this.engine.resize();
    });
  }

  private initScene(): void {
    this.scene.clearColor = new Color4(0, 0, 0, 1);

    const camera = new ArcRotateCamera(
      "camera",
      Math.PI / 2,
      Math.PI / 4,
      10,
      Vector3.Zero(),
      this.scene,
    );

    const hemiLight = new HemisphericLight(
      "hemiLight",
      new Vector3(0, 1, 0),
      this.scene,
    );
    hemiLight.intensity = 0.01;

    camera.attachControl(this.canvas, true);
  }

  public async syncFromGlb(url: string): Promise<void> {
    await AppendSceneAsync(url, this.scene);
  }
}

export { App };
