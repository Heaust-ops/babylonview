export const fragAmbientLight = `precision highp float;

in vec2 vUV;
uniform sampler2D textureSampler;
uniform vec3 ambientColor;

void main(void) {
  vec4 color = texture2D(textureSampler, vUV);
  color.rgb += ambientColor;

  gl_FragColor = color;
}
`;
