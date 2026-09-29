import { Platform } from 'react-native';
import PapayaInferenceModule from '../../modules/papaya-inference/src/PapayaInferenceModule';
import { LABELS, type DiseaseId, type LabelId } from '../data/labels';

// Coordinates are normalized relative to the original image.
export type Box = { x: number; y: number; width: number; height: number; label: DiseaseId; confidence?: number };
export type InferenceResult = { label: LabelId; boxes: Box[]; confidence: number };

export class ModelsUnavailableError extends Error {
  constructor() {
    super('Bản build này chưa có module AI. Hãy chạy npx expo run:android từ thư mục app để cài lại ứng dụng.');
  }
}

export const modelsReady = Platform.OS === 'android' && PapayaInferenceModule !== null;

function isLabel(value: string): value is LabelId {
  return LABELS.some((label) => label.id === value);
}

export async function analyzeImage(imageUri: string): Promise<InferenceResult> {
  if (!modelsReady || !PapayaInferenceModule) throw new ModelsUnavailableError();
  const result = await PapayaInferenceModule.analyzeImageAsync(imageUri);
  if (!isLabel(result.label) || !Number.isFinite(result.confidence) || !Array.isArray(result.boxes)) {
    throw new Error('Model trả về kết quả không hợp lệ.');
  }
  const boxes: Box[] = result.boxes.map((box) => {
    if (!isLabel(box.label) || box.label === 'Healthy' ||
      ![box.x, box.y, box.width, box.height].every(Number.isFinite) ||
      box.x < 0 || box.y < 0 || box.width <= 0 || box.height <= 0 ||
      box.x + box.width > 1.001 || box.y + box.height > 1.001) {
      throw new Error('Tọa độ hoặc nhãn bounding box không hợp lệ.');
    }
    return { x: box.x, y: box.y, width: box.width, height: box.height, label: box.label, confidence: box.confidence };
  });
  return { label: result.label, confidence: result.confidence, boxes: result.label === 'Healthy' ? [] : boxes };
}
