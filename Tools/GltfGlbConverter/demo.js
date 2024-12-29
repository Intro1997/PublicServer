import {
  ConvertGLBtoGltf,
  // ConvertGltfToGLB,
  // ConvertToGLB,
} from "gltf-import-export";

import { existsSync, mkdirSync } from "fs";
import { exec } from "child_process";

if (existsSync("output")) {
  exec("rm -rf output", function (err, out) {
    console.log(out);
    err && console.log(err);
  });
} else {
  mkdirSync("output");
}

const inputGlb = "Soldier.glb";
const extractedGltfFilename = "output/Soldier.gltf";

// Perform the conversion; output paths are overwritten
ConvertGLBtoGltf(inputGlb, extractedGltfFilename);

// let gltfContent = fs.readFileSync(extractedGltfFilename, "utf8");
// let gltf = JSON.parse(gltfContent);

// const outputGlb = "newfile.glb";

// // Perform the conversion; output path is overwritten
// ConvertToGLB(gltf, extractedGltfFilename, outputGlb);

// const gltfFilename = "pathtoyour.gltf";

// // optionally if you haven't already parsed the gltf JSON
// ConvertGltfToGLB(gltfFilename, outputGlb);
