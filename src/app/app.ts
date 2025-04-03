import {
  ArcRotateCamera,
  Color4,
  Engine,
  LoadSceneAsync,
  Observable,
  Scene,
  Vector3,
} from "@babylonjs/core";
import { Inspector } from "@babylonjs/inspector";

class App {
  engine: Engine;
  scene: Scene;
  private canvas: HTMLCanvasElement;

  cameraBackup: {
    alpha: number;
    beta: number;
    target: Vector3;
    radius: number;
  } | null;

  inspector: { show: () => void; hide: () => void };

  onNewSceneObservable = new Observable<Scene>();

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.engine = new Engine(this.canvas, true);

    this.engine.displayLoadingUI = function () { };
    this.engine.hideLoadingUI = function () { };

    this.scene = new Scene(this.engine);
    this.cameraBackup = null;

    this.initScene(this.scene);

    this.engine.runRenderLoop(() => {
      this.scene.render();
    });

    window.addEventListener("resize", () => {
      this.engine.resize();
    });

    this.inspector = {
      show: () => {
        Inspector.Show(this.scene, {
          embedMode: true,
        });
      },
      hide: () => {
        Inspector.Hide();
      },
    };
  }

  private initScene(scene: Scene): void {
    scene.clearColor = new Color4(0, 0, 0, 1);

    const camera = new ArcRotateCamera(
      "camera",
      Math.PI / 2,
      Math.PI / 4,
      10,
      Vector3.Zero(),
      scene,
    );

    if (!this.cameraBackup) {
      this.cameraBackup = {
        alpha: 0,
        beta: 0,
        target: Vector3.Zero(),
        radius: 0,
      };

      if (scene.cameras.length) {
        camera.position = scene.cameras[0].position;
        camera.rotationQuaternion = scene.cameras[0].absoluteRotation;
      }
    } else {
      camera.alpha = this.cameraBackup.alpha;
      camera.beta = this.cameraBackup.beta;
      camera.target = this.cameraBackup.target;
      camera.radius = this.cameraBackup.radius;
    }

    camera.onViewMatrixChangedObservable.add(() => {
      this.cameraBackup!.alpha = camera.alpha;
      this.cameraBackup!.beta = camera.beta;
      this.cameraBackup!.target = camera.target;
      this.cameraBackup!.radius = camera.radius;
    });

    camera.attachControl(this.canvas, true);
  }

  public async syncFromGlb(url: string): Promise<void> {
    const scene = await LoadSceneAsync(url, this.engine);

    this.scene.onDisposeObservable.add(() => {
      this.inspector.hide();
    });
    this.scene.dispose();

    this.initScene(scene);
    this.scene = scene;
    (window as any).scene = scene;

    this.onNewSceneObservable.notifyObservers(scene);
  }
}

export { App };
