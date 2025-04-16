import { AbstractMesh, Scene } from "@babylonjs/core";

class BlenderId {
  private map = {} as Record<string, AbstractMesh>;
  refresh(scene: Scene) {
    this.map = {};
    scene.meshes.forEach((m) => {
      this.map[m.name] = m;
    });
  }

  get(id: string) {
    return this.map[id];
  }
}

export { BlenderId };
