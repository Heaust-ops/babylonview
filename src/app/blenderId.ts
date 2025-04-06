import { AbstractMesh, Scene } from "@babylonjs/core";

class BlenderId {
  private map = {} as Record<number, AbstractMesh>;
  refresh(scene: Scene) {
    this.map = {};
    scene.meshes.forEach((m) => {
      const blenderUniqueId = m.metadata?.gltf?.extras?.blenderUniqueId;
      if (!blenderUniqueId) return;
      this.map[+blenderUniqueId] = m;
    });
  }

  get(id: number) {
    return this.map[id];
  }
}

export { BlenderId };
