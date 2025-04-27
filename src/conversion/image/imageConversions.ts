import parseExr from "parse-exr";

const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d")!;

const exrToJpegBlobUrl = async (exrUrl: string): Promise<string> => {
  const resp = await fetch(exrUrl);
  if (!resp.ok) throw new Error(`Failed to load EXR: ${resp.statusText}`);
  const buffer = await resp.arrayBuffer();

  const FloatType = 1015;
  const { data, width, height } = parseExr(buffer, FloatType);

  const out = new Uint8ClampedArray(width * height * 4);
  const toneMap = (v: number) => {
    const mapped = v / (1 + v);
    return Math.pow(mapped, 1 / 2.2);
  };

  for (let i = 0; i < width * height; i++) {
    const r = toneMap(data[i * 4 + 0]);
    const g = toneMap(data[i * 4 + 1]);
    const b = toneMap(data[i * 4 + 2]);
    const a = data[i * 4 + 3];

    out[i * 4 + 0] = Math.round(Math.min(1, r) * 255);
    out[i * 4 + 1] = Math.round(Math.min(1, g) * 255);
    out[i * 4 + 2] = Math.round(Math.min(1, b) * 255);
    out[i * 4 + 3] = Math.round(Math.min(1, a) * 255);
  }

  canvas.width = width;
  canvas.height = height;
  const imgData = new ImageData(out, width, height);
  ctx.putImageData(imgData, 0, 0);

  return new Promise<string>((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (!blob) return reject(new Error("JPEG conversion failed"));
      resolve(URL.createObjectURL(blob));
    }, "image/jpeg");
  });
};

export { exrToJpegBlobUrl };
