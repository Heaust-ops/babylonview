import {
  Color3,
  Color4,
  EquiRectangularCubeTexture,
  MeshBuilder,
  PBRMaterial,
  Quaternion,
  RectAreaLight,
  Scene,
  Texture,
  TransformNode,
  Vector3,
} from "@babylonjs/core";
import { App } from "../app/app";
import { Comms } from "./comms";
import { RealtimeSync } from "./realtimeSync";
import { exrToJpegBlobUrl } from "../conversion/image/imageConversions";

type ExtraGLBData = {
  areaLights: {
    name: string;
    color: string;
    shape: string;
    energy: number;
    location: number[];
    rotation: number[];
    scale: number[];
    size: [number, number];
  }[];
  world:
    | {
        type: "image";
        info: string[];
      }
    | {
        type: "color";
        info: string;
      };
};

class SocketInterpreter {
  app: App;
  comms: Comms;

  socketCommandToId: Record<string, string | number>;
  socketCommandFromId: Record<string | number, string>;

  rtSync: RealtimeSync;

  constructor(app: App, comms: Comms) {
    this.app = app;
    this.comms = comms;

    this.socketCommandToId = {};
    this.socketCommandFromId = {};

    this.rtSync = new RealtimeSync(app, this);

    comms.addMessageListener((msg) => {
      if (msg.startsWith("Echo")) return;
      this.interpret(JSON.parse(msg));
    });
  }

  send(commandArr: (string | number)[] | string) {
    if (typeof commandArr === "string") {
      commandArr = [commandArr];
    }

    const command = this.socketCommandToId[commandArr[0]];
    if (typeof command === "undefined") {
      console.error("malformed command: undefined");
    }

    commandArr[0] = command ?? commandArr[0];

    const serialized = JSON.stringify(commandArr);
    this.comms.send(serialized);
  }

  private async parseExtraData(scene: Scene, extraData: ExtraGLBData) {
    /**
     * World color / skyboxes
     */
    if (extraData.world.type === "color") {
      const colorArr = Color3.FromHexString(extraData.world.info).asArray();

      if (this.app.useClearColorFromPost) {
        this.app.clearColor = new Color4(...colorArr, 1);
      } else {
        this.app.scene.clearColor = new Color4(...colorArr, 1);
      }
    }

    if (extraData.world.type === "image") {
      const [url, _, projection, __, ___, ____] = extraData.world.info;
      if (projection === "EQUIRECTANGULAR") {
        let jpegUrl = url;
        if (url.toLowerCase().endsWith(".exr")) {
          jpegUrl = await exrToJpegBlobUrl(`http://localhost:8001/${url}`);
        }

        const eqTexture = new EquiRectangularCubeTexture(jpegUrl, scene, 1024);

        // to follow blender's z-up coordinate system, this matrix = identity -> rotation.x of 90deg
        (eqTexture.getReflectionTextureMatrix() as any)._m = new Float32Array([
          1, 0, 0, 0, 0, 2.220446049250313e-16, 1, 0, 0, -1,
          2.220446049250313e-16, 0, 12.5, -12.5, 17.677669525146484, 1,
        ]);

        scene.materials.forEach((mat) => {
          if (!(mat instanceof PBRMaterial)) return;
          if (mat.name === "skyBox") return;
          mat.reflectionTexture = eqTexture;
        });
        scene.onNewMaterialAddedObservable.add((mat) => {
          if (!(mat instanceof PBRMaterial)) return;
          if (mat.name === "skyBox") return;
          mat.reflectionTexture = eqTexture;
        });

        const hdrSkybox = MeshBuilder.CreateBox(
          "hdrSkyBox",
          { size: 1000.0 },
          scene,
        );

        const hdrSkyboxMaterial = new PBRMaterial("skyBox", scene);
        hdrSkyboxMaterial.backFaceCulling = false;
        hdrSkyboxMaterial.reflectionTexture = eqTexture.clone();
        hdrSkyboxMaterial.reflectionTexture.coordinatesMode =
          Texture.SKYBOX_MODE;
        hdrSkyboxMaterial.microSurface = 1.0;
        hdrSkyboxMaterial.disableLighting = false;
        hdrSkybox.material = hdrSkyboxMaterial;
        hdrSkybox.infiniteDistance = true;
      }
    }

    /**
     * Area Lights
     */
    extraData.areaLights.forEach((item) => {
      const rectAreaLight = new RectAreaLight(
        item.name,
        Vector3.Zero(),
        ...item.size,
        scene,
      );
      const transformNode = new TransformNode(
        item.name + ":__transform-helper__",
      );
      rectAreaLight.parent = transformNode;
      rectAreaLight.intensity = item.energy / (4 * Math.PI);

      const pos = Vector3.FromArray(item.location);
      const q = Quaternion.FromArray(item.location);
      const scale = Vector3.FromArray(item.scale);
      transformNode.position = pos;
      transformNode.rotationQuaternion = q;
      transformNode.scaling = scale;
    });
  }

  interpret(msg: Array<any> | string | number) {
    if (!(msg instanceof Array)) msg = [msg];

    const msg_rev = msg.reverse();
    const cmdId = msg_rev.pop();

    if (typeof cmdId === "undefined") {
      console.error("malformed message", msg);
      return;
    }

    const command = this.socketCommandFromId[cmdId];
    switch (command) {
      case "sync glb":
        const extraData = msg_rev.pop();
        this.app.onNewSceneObservable.addOnce(() => {
          this.parseExtraData(this.app.scene, extraData);
        });
        this.app.syncFromGlb("http://localhost:8001/scene.glb");
        break;
      case "update world color":
        break;
      case "transform update":
        this.rtSync.applyTransforms(
          msg_rev.pop(),
          msg_rev.pop(),
          msg_rev.pop(),
          msg_rev.pop(),
        );
        break;
    }
  }

  async loadCommandsMap() {
    try {
      const response = await fetch("http://localhost:8001/commands.json");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: Record<string | number, string | number> =
        await response.json();

      const flipped: Record<string, string> = Object.fromEntries(
        Object.entries(data).map(([key, value]) => [value, key]),
      );

      this.socketCommandToId = data;
      this.socketCommandFromId = flipped;
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  }
}

export { SocketInterpreter };
