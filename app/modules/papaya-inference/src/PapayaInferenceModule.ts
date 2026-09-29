import { NativeModule, requireOptionalNativeModule } from 'expo';

export type NativeBox = { x: number; y: number; width: number; height: number; label: string; confidence: number };
export type NativeResult = { label: string; confidence: number; boxes: NativeBox[] };

declare class PapayaInferenceModule extends NativeModule<{}> {
  analyzeImageAsync(uri: string): Promise<NativeResult>;
}

export default requireOptionalNativeModule<PapayaInferenceModule>('PapayaInference');
