import {
  ArcRotateCamera,
  Camera,
  Color4,
  Engine,
  LoadSceneAsync,
  Observable,
  Scene,
  Vector3,
} from "@babylonjs/core";
import { Inspector } from "@babylonjs/inspector";
import { BlenderId } from "./blenderId";
import { PostProcessManager } from "../postprocess/postprocess";
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
  blenderId: BlenderId;

  clearColor = new Color4(0, 0, 0, 1);
  private _useClearColorFromPost = true;
  get useClearColorFromPost() {
    return this._useClearColorFromPost;
  }
  set useClearColorFromPost(arg: boolean) {
    if (!arg) {
      this.scene.clearColor = this.clearColor.clone();
      this.clearColor = new Color4(0, 0, 0, 1);
    } else {
      this.clearColor = this.scene.clearColor.clone();
      this.scene.clearColor = new Color4(0, 0, 0, 1);
    }
    this._useClearColorFromPost = arg;
  }

  private sceneDirty = false;
  isSceneDirty() {
    return this.sceneDirty;
  }

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.engine = new Engine(this.canvas, true);

    this.engine.displayLoadingUI = function () {};
    this.engine.hideLoadingUI = function () {};

    this.blenderId = new BlenderId();

    this.scene = new Scene(this.engine);
    this.cameraBackup = null;

    this.onNewSceneObservable.add(() => {
      this.scene.onNewCameraAddedObservable.add((camera) => {
        PostProcessManager.init(this.scene, camera, this);
      });
    });

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
    this.sceneDirty = true;

    const scene = await LoadSceneAsync(url, this.engine);
    this.blenderId.refresh(scene);
    scene.imageProcessingConfiguration.isEnabled = false;

    this.scene.onDisposeObservable.add(() => {
      this.inspector.hide();
    });
    this.scene.dispose();

    this.initScene(scene);
    this.scene = scene;
    (window as any).scene = scene;

    this.sceneDirty = false;

    this.onNewSceneObservable.notifyObservers(scene);
  }
}

export { App };
